"""Full-body teleoperation: the leader arm controls both arms; the keyboard controls head/base/lift.

Control assignment:
- Leader arm: both arms (left_arm_*/right_arm_*) follow in real time
- Keyboard (pynput, hold to move, release to stop):
    Head:   w/s = nod (up/down), a/d = shake (left/right)
    Base:   i/k = forward/backward, j/l = turn left/right, n/m = speed up/down (3 levels)
    Lift:   u/h = up/down (clamped to 3~200mm)
    b      = quit

Cameras (parameter-controlled):
    3 loaded by default: head + left_wrist + right_wrist
    --no-cameras               skip all cameras (pure teleoperation)
    --cameras=head,left_wrist  load only the specified cameras (comma-separated)
    --head-camera /dev/video0  override the head device (similarly --left-wrist-camera/--right-wrist-camera)
    --chest-camera /dev/video6 additionally load the chest camera (up to 4 total)

Notes:
- The follower head/base/lift are keyboard-controlled and otherwise hold their current pose
- Leader readings are naturally consistent with the follower direction (verified with diagnose_teleop), so the official flip table stays disabled

Usage:
    python3 examples/teleop_leader_to_follower.py
    python3 examples/teleop_leader_to_follower.py --no-cameras
    python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

Safety:
- ⚠️ The follower's whole body moves; make sure there are no obstacles around
- It is recommended to prop the robot up before moving the base
- Ctrl+C to stop
"""

import argparse
import os
import sys
import threading
import time

import numpy as np
import rerun
from pynput import keyboard

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

FPS = 30

# Keyboard control rates (units/second)
HEAD_PAN_SPEED = 20.0     # head pan (normalized units/s)
HEAD_TILT_SPEED = 20.0    # head tilt
BASE_LINEAR_SPEED = 0.2   # base linear speed m/s (base level, × level multiplier)
BASE_ANGULAR_SPEED = 30.0  # base angular speed deg/s (base level, × level multiplier)
BASE_SPEED_LEVELS = [0.3, 0.6, 1.0]  # base speed level multipliers (toggled with n/m)
LIFT_SPEED_MM = 15.0      # lift mm/s
LIFT_MIN_MM = 3.0         # lift soft lower limit (descent_floor hard-protects at 3mm)
LIFT_MAX_MM = 200.0       # lift soft upper limit (200mm, user-specified)

CAMERA_FPS = 30
CAMERA_W, CAMERA_H = 640, 480
CAMERA_FOURCC = "MJPG"  # compressed format, low bandwidth; most cameras sustain 30fps (YUYV raw stream is only 25)

# default device numbers for the 3 cameras (confirm with lerobot-find-cameras after plugging in; overridable via arguments)
DEFAULT_CAM_DEVICES = {
    "head": "/dev/video0",
    "left_wrist": "/dev/video2",
    "right_wrist": "/dev/video4",
}

# per-camera fps settings - adjust to your actual hardware capabilities
# use v4l2-ctl -d /dev/videoN --list-formats-ext to inspect supported resolutions and frame rates
# defaults measured on current hardware: video4 tops out at 25fps in 640x480 MJPG, the rest at 30fps
CAMERA_FPS_MAP = {"head": 30, "left_wrist": 30, "right_wrist": 30, "chest": 30}


def build_cameras(args) -> dict[str, OpenCVCameraConfig]:
    """Build the camera dict from arguments. --no-cameras or an empty --cameras → returns an empty dict."""
    if args.no_cameras or not args.cameras:
        return {}
    cams = {}
    # if a camera device number was passed explicitly, add it even if it is not in the --cameras list
    names = [n.strip() for n in args.cameras.split(",") if n.strip()]
    for n in ("head", "left_wrist", "right_wrist", "chest"):
        if getattr(args, f"{n}_camera") and n not in names:
            names.append(n)
    for name in names:
        dev = getattr(args, f"{name}_camera") or DEFAULT_CAM_DEVICES.get(name)
        if dev is None:
            print(f"  ⚠️ Unknown camera name '{name}', skipped (available: head/left_wrist/right_wrist/chest)")
            continue
        cams[name] = OpenCVCameraConfig(
            index_or_path=dev,
            fps=CAMERA_FPS_MAP.get(name, CAMERA_FPS),
            width=CAMERA_W,
            height=CAMERA_H,
            fourcc=CAMERA_FOURCC,
        )
        print(f"  📷 {name}: {dev} @{cams[name].fps}fps {CAMERA_FOURCC}")
    return cams


class KeyState:
    """Thread-safely track which keys are currently held down."""

    def __init__(self):
        self._pressed: set[str] = set()
        self._consumed: set[str] = set()
        self._lock = threading.Lock()

    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            return
        if char is not None:
            with self._lock:
                self._pressed.add(char)

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            return
        if char is not None:
            with self._lock:
                self._pressed.discard(char)

    def is_down(self, char: str) -> bool:
        with self._lock:
            return char in self._pressed

    def pressed_once(self, char: str) -> bool:
        """True only on the rising edge of a key (False→True transition).

        Based on is_down state, not on_press events — OS key-repeat sends
        repeated press events while held, which would otherwise re-trigger.
        """
        with self._lock:
            down = char in self._pressed
            was = char in self._consumed  # _consumed doubles as "was pressed"
            if down:
                self._consumed.add(char)
            else:
                self._consumed.discard(char)
            return down and not was


def main():
    _web_servers: list = []  # running rerun --serve-web subprocesses (--display-web mode)
    parser = argparse.ArgumentParser(description="HumanaOpen full-body teleoperation (leader arm + keyboard)")
    parser.add_argument("--remote_ip", default=None, help="Host IP for ZMQ (omit for direct serial)")
    parser.add_argument("--port_zmq_cmd", type=int, default=5555)
    parser.add_argument("--port_zmq_obs", type=int, default=5556)
    parser.add_argument("--no-cameras", action="store_true", help="skip all cameras (pure teleoperation; takes effect in single-machine mode, only suppresses rerun image display in dual-machine mode)")
    parser.add_argument(
        "--cameras",
        default="head,left_wrist,right_wrist",
        help="camera names to load, comma-separated (head/left_wrist/right_wrist/chest)",
    )
    for name in ("head", "left_wrist", "right_wrist", "chest"):
        parser.add_argument(
            f"--{name}-camera",
            default=None,
            help=f"{name} camera device (default {DEFAULT_CAM_DEVICES.get(name, 'undefined')})",
        )
    parser.add_argument(
        "--display",
        choices=["rerun", "foxglove"],
        default=None,
        help="enable live display: 'rerun' (native Rerun viewer) or 'foxglove' "
        "(Foxglove app, recommended — lower render latency). Omit to run headless.",
    )
    args = parser.parse_args()

    cams = build_cameras(args)
    is_dual = args.remote_ip is not None

    # In dual-machine mode the camera HARDWARE lives on the Host (it owns the
    # /dev/video* devices and streams the frames over ZMQ). The PC-side camera
    # args (--cameras/--no-cameras) only apply to single-machine mode; here they
    # merely tell rerun which received image keys to display.
    if args.no_cameras and is_dual:
        # Client-side: suppress image frames before visualization (Host keeps streaming)
        def _strip_images(obs: dict) -> dict:
            return {k: v for k, v in obs.items() if not (isinstance(v, np.ndarray) and v.ndim == 3)}

    else:

        def _strip_images(obs: dict) -> dict:
            return obs

    if is_dual:
        # Warn about PC-side camera args that have no effect in dual-machine mode:
        # a non-default --cameras list or any explicit --<name>-camera device only
        # configures local/single-machine cameras; the Host decides what is streamed.
        explicit_dev_args = {n for n in ("head", "left_wrist", "right_wrist", "chest")
                             if getattr(args, f"{n}_camera") is not None}
        if explicit_dev_args or args.cameras != "head,left_wrist,right_wrist":
            extra = "".join(f"    --{n}-camera is ignored in dual-machine mode; configure '{n}' on the Host\n"
                            for n in sorted(explicit_dev_args))
            if extra:
                extra = "\n" + extra
            print(f"  ⚠️ Camera args ({', '.join(sorted(explicit_dev_args)) or args.cameras}) are ignored "
                  f"in dual-machine mode — set up cameras on the Host side instead.{extra}")
        # ── ZMQ dual-machine mode ────────────────────────────
        from lerobot_robot_humanaopen.humanaopen_client import HumanaOpenClient, HumanaOpenClientConfig
        # cams is passed as the *schema* (names + shapes): the client needs it to
        # know which camera frames to accept from the multipart obs stream (the
        # Host owns the physical cameras and sends the actual JPEG frames).
        _client_cfg = HumanaOpenClientConfig(
            remote_ip=args.remote_ip, port_zmq_cmd=args.port_zmq_cmd,
            port_zmq_observations=args.port_zmq_obs,
            cameras=cams,
        )
        _client = HumanaOpenClient(_client_cfg)

        class _ZMQRobot:
            """Minimal robot adapter for ZMQ — provides .connect / .get_observation / .send_action / .calibration / .lift_axis."""
            def connect(self, calibrate=True):
                _client.connect()
                self._obs = _client.get_observation()
            def get_observation(self):
                self._obs = _client.get_observation()
                return self._obs
            def send_action(self, action):
                _client.send_action(action)
            @property
            def calibration(self):
                return {}
            @property
            def lift_axis(self):
                _obs_ref = self._obs
                class _Lift:
                    def get_height_mm(_s):
                        return _obs_ref.get("lift_axis.height_mm", 0.0)
                return _Lift()

        follower = _ZMQRobot()
        print(f"  Mode: ZMQ (Host: {args.remote_ip})")
    else:
        # ── Direct serial mode ──────────────────────────────
        follower_cfg = HumanaOpenConfig(
            id="follower", port1="/dev/ttyACM0", port2="/dev/ttyACM1",
            port3=None, cameras=cams,
            wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
        )
        follower = HumanaOpen(follower_cfg)
        print("  Mode: direct serial")

    leader_cfg = BiHumanaOpenLeaderConfig(
        id="leader",
        left_arm_port="/dev/ttyACM0",
        right_arm_port="/dev/ttyACM1",
        flip_joints={"left": [], "right": []},
        joint_remap={},
    )
    leader = BiHumanaOpenLeader(leader_cfg)

    keys = KeyState()
    listener = keyboard.Listener(on_press=keys.on_press, on_release=keys.on_release)
    listener.start()

    try:
        print("[1] Connecting follower...")
        follower.connect(calibrate=True)
        # connect handles this internally: prefer restoring the persisted position (no re-zeroing); only auto-home on failure
        if is_dual:
            # Show which image keys the Host actually streams (may differ from
            # --cameras). The PUSH/PULL connect handshake already guarantees an
            # observation; images arrive every image_fps_divider frames, so a
            # brief settle makes the status line reflect the real cameras.
            obs0 = {}
            for _ in range(5):
                obs0 = follower.get_observation()
                if any(isinstance(v, np.ndarray) and v.ndim == 3 for v in obs0.values()):
                    break
                time.sleep(0.1)
            received = [k for k in obs0 if isinstance(obs0[k], np.ndarray) and obs0[k].ndim == 3]
            if args.no_cameras:
                print(f"    Follower connected (--no-cameras: image display suppressed; Host still streams: {received or 'none'})")
            else:
                print(f"    Follower connected (Host cameras received: {received or 'none'})")
        else:
            print(f"    Follower connected (cameras: {list(cams.keys()) or 'none'}, lift {follower.lift_axis.get_height_mm():.1f}mm)")

        print("[2] Connecting leader...")
        leader.connect(calibrate=True)
        print("    Leader connected")

        obs = follower.get_observation()

        # optional live visualization — foxglove (official lerobot backend, in-process
        #         WebSocket server; render in the Foxglove app, no native wgpu, no subprocesses)
        if args.display == "foxglove":
            try:
                from lerobot.utils.visualization_utils import (
                    init_foxglove,
                    log_foxglove_data,
                    shutdown_foxglove,
                )

                init_foxglove(port=8765)
                # The server exposes the OFFICIAL viewer link: app.foxglove.dev with
                # ds=foxglove-websocket (NOT rosbridge). Opening it pre-configures the
                # correct connection type + ws URL — this is what the SDK documents.
                # Note: lerobot stores the WebSocketServer on log_foxglove_data.server.
                _app = getattr(getattr(log_foxglove_data, "server", None), "app_url", None)
                if _app is not None:
                    _u = _app()
                    print(f"  🦊 Foxglove viewer — open in browser:\n     {_u}")
                    try:
                        import webbrowser

                        webbrowser.open(_u)
                    except Exception:
                        pass
                    print(
                        "      (in Foxglove Studio: connection type must be "
                        "'Foxglove WebSocket', not Rosbridge; topics: "
                        "/observation/state, /action/state, /observation/images/*)"
                    )
                else:
                    print(
                        f"  🦊 Foxglove viewer: connect Foxglove Studio (type=Foxglove "
                        f"WebSocket) to ws://127.0.0.1:8765"
                    )
                # One-shot diagnostic: which image/state keys actually reach Foxglove
                # (if wrist is missing here, the Host/schema is the problem, not Foxglove)
                _fobs = follower.get_observation()
                _fimgs = sorted(
                    k for k, v in _fobs.items()
                    if isinstance(v, np.ndarray) and v.ndim == 3
                )
                _fstate = sorted(k for k in _fobs if k not in _fimgs)
                print(f"  📋 Foxglove sees: images={_fimgs or 'NONE'} state_keys={len(_fstate)}")

                # Generate a ready-made layout (3 image panels + obs/action plots) so the
                # user does NOT have to manually add panels: Foxglove only auto-shows the
                # first image topic in its default layout. One-time "Layouts -> Import
                # from file -> humanoopen_foxglove.layout.json" then it repeats.
                # Writes next to the script (uses HEAD/LEFT/chest keys once known).
                try:
                    import foxglove.layouts as _fl

                    _img_titles = {
                        "head": "Head",
                        "left_wrist": "Left Wrist",
                        "right_wrist": "Right Wrist",
                        "chest": "Chest",
                    }
                    _imgs = sorted(
                        k for k in _fimgs if k in _img_titles
                    ) or _fimgs[:3]
                    _items = [
                        _fl.SplitItem(
                            proportion=1,
                            content=_fl.ImagePanel(
                                config=_fl.ImageConfig(
                                    image_mode=_fl.ImageModeConfig(
                                        image_topic=f"/observation/images/{k}"
                                    )
                                ),
                                title=_img_titles.get(k, k),
                            ),
                        )
                        for k in _imgs
                    ]
                    _layout = _fl.Layout(
                        content=_fl.SplitContainer(
                            direction="column",
                            items=[
                                _fl.SplitItem(proportion=3, content=_fl.SplitContainer(
                                    direction="row", items=_items
                                )),
                                _fl.SplitItem(proportion=1, content=_fl.PlotPanel(
                                    config=_fl.PlotConfig(paths=[_fl.PlotSeries(
                                        value="/observation.state.scalars[:].value", label="observation")]),
                                    title="Observation",
                                )),
                                _fl.SplitItem(proportion=1, content=_fl.PlotPanel(
                                    config=_fl.PlotConfig(paths=[_fl.PlotSeries(
                                        value="/action.state.scalars[:].value", label="action")]),
                                    title="Action",
                                )),
                            ],
                        )
                    )
                    _lay_path = os.path.join(os.path.dirname(__file__), "humanoopen_foxglove.layout.json")
                    with open(_lay_path, "w") as _f:
                        _f.write(_layout.to_json())
                    print(
                        f"  📐 Ready-made layout written: {_lay_path}\n"
                        f"     In Foxglove: Layouts -> Import from file -> pick it "
                        f"(one-time; shows all {len(_imgs)} images + obs/action plots)"
                    )
                except Exception as _e:
                    print(f"  ⚠️ Layout generation skipped: {str(_e)[:60]}")
            except Exception as e:
                print(f"  ⚠️ Foxglove startup failed: {str(e)[:80]}")

        # optional rerun live visualization (camera feeds + joint states)
        _display_web = False  # removed --display-web flag; keep var for shutdown safety
        if args.display == "rerun":
            try:
                from lerobot.utils.visualization_utils import init_rerun, log_rerun_data

                # rr.spawn() needs a `rerun` executable in PATH; if the shell
                # didn't activate the conda env (or put it elsewhere), spawn
                # fails silently and only a viewer-less gRPC server starts
                # (rerun shows nothing + "Sender blocked" warnings). Make sure
                # the command is discoverable before calling init_rerun.
                import shutil

                if shutil.which("rerun") is None:
                    _candidates = [
                        # (a) this conda env's bin (when running via env python)
                        os.path.dirname(sys.executable),
                        # (b) bundled rerun_cli executable inside rerun_sdk
                        os.path.join(os.path.dirname(rerun.__file__), "..", "rerun_cli"),
                    ]
                    for _c in _candidates:
                        _p = os.path.abspath(_c)
                        if os.path.isdir(_p) and any(
                            f in os.listdir(_p) for f in ("rerun", "rerun.exe")
                        ):
                            os.environ["PATH"] = _p + os.pathsep + os.environ.get("PATH", "")
                            print(f"  📌 Added {_p} to PATH for rerun viewer")
                            break

                # WEB viewer mode: rerun --serve-web hosts a gRPC proxy + HTTP web
                # viewer; the browser renders with WebGL. This bypasses the native
                # wgpu present bug seen on NVIDIA Blackwell + 580 drivers (window
                # opens but stays black and unresponsive). init_rerun(ip, port)
                # connects the SDK to that gRPC proxy instead of rr.spawn.
                import subprocess

                if _display_web:
                    _rerun_bin = shutil.which("rerun")
                    _g = args.web_grpc_port  # gRPC endpoint the SDK connects to
                    _wp = args.web_port
                    # Auto-clean stale serve-web leftovers from previous runs:
                    # if teleop exited abnormally (kill -9 / crash), the
                    # earlier serve-web orphan still owns the ports and the new
                    # one would crash with "Address already in use" (no data).
                    import subprocess as _sp

                    try:
                        # Pattern only matches the rerun viewer binary itself
                        # (path contains rerun_cli/rerun), never this script or
                        # unrelated processes.
                        _sp.run(
                            ["pkill", "-f", r"rerun_cli/rerun.*--serve-web"],
                            capture_output=True, timeout=3,
                        )
                        time.sleep(0.3)
                    except Exception:
                        pass
                    # Sanity: only fail if the ports are STILL busy after the
                    # pkill (e.g. a non-rerun process owns them).
                    _s = __import__("socket").socket()
                    _grpc_busy = _s.connect_ex(("127.0.0.1", _g)) == 0
                    _s.close()
                    _s2 = __import__("socket").socket()
                    _web_busy = _s2.connect_ex(("127.0.0.1", _wp)) == 0
                    _s2.close()
                    if _grpc_busy or _web_busy:
                        raise RuntimeError(
                            f"Port {_g} (gRPC) or {_wp} (web) still in use after pkill — "
                            f"another process owns it. Check: ss -tlnp | grep -E '{_g}|{_wp}'"
                        )
                    _web = subprocess.Popen(
                        [
                            _rerun_bin,
                            "--serve-web",
                            "--port", str(_g),
                            "--web-viewer-port", str(_wp),
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                    )
                    _web_servers.append(_web)
                    # Wait for the gRPC port to actually accept connections:
                    # connect_grpc() does NOT retry — if it runs before the
                    # serve-web process finishes binding, the SDK stays
                    # disconnected and the web UI shows no data forever.
                    _sock = __import__("socket").socket()
                    _deadline = time.time() + 10
                    while time.time() < _deadline:
                        if _sock.connect_ex(("127.0.0.1", _g)) == 0:
                            break
                        time.sleep(0.2)
                    _sock.close()
                    # The web UI only shows data when the URL carries the gRPC
                    # endpoint via the `?url=` param (URL-encoded); the bare
                    # http://127.0.0.1:PORT page is just the welcome screen.
                    _url = (
                        f"http://127.0.0.1:{args.web_port}"
                        f"?url=rerun%2Bhttp%3A%2F%2Flocalhost%3A{_g}%2Fproxy"
                    )
                    print(f"  🌐 Rerun WEB viewer (open in browser):\n     {_url}")
                    try:  # best-effort auto-open; user may open it manually
                        import webbrowser

                        webbrowser.open(_url)
                    except Exception:
                        pass
                    init_rerun(
                        session_name="humanaopen_teleop",
                        ip="127.0.0.1",
                        port=_g,
                    )
                else:
                    # NATIVE rerun viewer (--display). Use the same simple,
                    # proven path as data collection (lerobot record): call
                    # init_rerun() with no ip/port, which internally does
                    # rr.spawn() and opens the viewer window automatically.
                    # Do NOT pkill rerun here: rr.spawn() launches its detached
                    # viewer whose argv matches `rerun_cli/rerun`, so a pkill on
                    # that pattern can race/kill the freshly spawned viewer right
                    # after its window opens but before the gRPC data channel is
                    # established -> blank window + 're_grpc_client::write:
                    # transport error' (exactly what record avoids by spawning
                    # cleanly with no pkill).
                    init_rerun(session_name="humanaopen_teleop")
                # compress_images=True: 921KB raw image -> ~25KB JPEG into viewer; without it
                # 3 cams at 15Hz = ~41MB/s into the viewer process, which lags => display delay
                # First log also Sends the blueprint: it must include image views, so wait
                # until an observation carrying camera frames arrives (client image cache
                # may be empty right after connect; handler then rebuilds fields). Only
                # seed the blueprint once images are present — if we logged a state-only
                # obs here, the blueprint would lack image panels and no images would ever
                # show (only joint/state scalars), exactly the symptom observed.
                _fobs = follower.get_observation()
                for _ in range(50):
                    if _fobs and any(
                        isinstance(v, np.ndarray) and v.ndim == 3 for v in _fobs.values()
                    ):
                        break
                    time.sleep(0.2)
                    _fobs = follower.get_observation()
                if _fobs and any(
                    isinstance(v, np.ndarray) and v.ndim == 3 for v in _fobs.values()
                ):
                    log_rerun_data(observation=_strip_images(_fobs), compress_images=True)
            except Exception as e:
                print(f"  ⚠️ Rerun startup failed (ignored): {str(e)[:60]}")

        print()
        print("=" * 60)
        print("Teleoperation started!")
        print("  Arms:   leader follows")
        print("  Head:   w/s = nod (up/down), a/d = shake (left/right)")
        print("  Base:   i/k = forward/back, j/l = turn, n/m = speed (0.3x/0.6x/1.0x)")
        print("  Lift:   u/h = up/down (clamped 3~200mm)")
        print("  Quit:   b or Ctrl+C")
        print("=" * 60)
        print()

        # initialize head positions + read head limits from the calibration file (MIN/MAX recorded at calibration time)
        head_pan = obs.get("head_pan.pos", 0.0)
        head_tilt = obs.get("head_tilt.pos", 0.0)
        try:
            cal = follower.calibration
            head_pan_min = (cal["head_pan"].range_min, 2048)
            head_tilt_min = (cal["head_tilt"].range_min, 2048)
            head_pan_lim = (cal["head_pan"].range_min, cal["head_pan"].range_max)
            head_tilt_lim = (cal["head_tilt"].range_min, cal["head_tilt"].range_max)
        except (KeyError, TypeError, AttributeError):
            head_pan_lim = head_tilt_lim = (0, 4096)
        # normalized space: use_degrees=False → RANGE_M100_100, so limits are ±100
        # (the obs range [-100,100] maps linearly onto the calibration range endpoints, see motors_bus._normalize)
        head_pan_min, head_pan_max = -100.0, 100.0
        head_tilt_min, head_tilt_max = -100.0, 100.0
        print(f"  Head limits: pan range {head_pan_lim}, tilt range {head_tilt_lim} (normalized ±100)")
        lift_h = obs.get("lift_axis.height_mm", 0.0)
        _last_lift_dir = 0  # 0=none, 1=last pressed u, -1=last pressed h
        speed_idx = 1  # base speed level (1 = base)
        _last_lift_print = 0.0  # throttles the lift-status display
        _rerun = args.display == "rerun"  # whether rerun display is enabled
        _foxglove = args.display == "foxglove"  # whether foxglove display is enabled

        # ── Display decoupling ─────────────────────────────────────────
        # foxglove/rerun logging is MOVED OFF the control loop: log_foxglove_data
        # serializes images synchronously, which stalled the 30Hz control loop.
        # Consumption then fell below the host's 30Hz production, the PUSH queue
        # delivered stale obs, and image latency climbed to seconds. A daemon
        # thread logs at 15Hz from the latest observation the control loop
        # produces; the loop itself stays pure:
        # get_action -> send_action -> get_observation.
        import threading as _threading
        _disp_lock = _threading.Lock()
        _disp_state: dict = {"obs": {}, "action": {}}
        _disp_stop = _threading.Event()

        def _fresh_obs(obs: dict, last_ids: dict) -> dict:
            """Return obs stripped of images that did not change since last call.

            Keeps only state + image keys whose array OBJECT changed (id()). Returns
            the full obs as-is on the first call, thereafter drops unchanged images
            so the viewer backend does not re-encode/re-send stale frames at its own
            log rate (images arrive at host divider rate, e.g. 10Hz)."""
            if not last_ids:
                for k, v in obs.items():
                    if isinstance(v, np.ndarray) and v.ndim == 3:
                        last_ids[k] = id(v)
                return obs
            changed = False
            for k, v in obs.items():
                if isinstance(v, np.ndarray) and v.ndim == 3:
                    if last_ids.get(k) != id(v):
                        last_ids[k] = id(v)
                        changed = True
            if changed:
                return obs
            # No new image: return obs without images (state-only)
            return {
                k: v
                for k, v in obs.items()
                if not (isinstance(v, np.ndarray) and v.ndim == 3)
            }

        def _display_thread() -> None:
            _disp_last_img_ids: dict = {}
            while not _disp_stop.is_set():
                _disp_t0 = time.perf_counter()
                with _disp_lock:
                    _o = dict(_disp_state["obs"])
                    _a = dict(_disp_state["action"])
                try:
                    # foxglove is socket-based and thread-safe — keep it on the
                    # display thread. Rerun is NOT logged here: its gRPC sink
                    # backpressures (bounded channel) and a daemon thread stuck
                    # blocking on it wedges past 5s -> "Sender blocked" +
                    # "transport error" + frozen viewer. Rerun logs on the main
                    # control thread instead (like record_data.py).
                    if _foxglove:
                        log_foxglove_data(
                            observation=_strip_images(_fresh_obs(_o, _disp_last_img_ids)),
                            action=_a,
                            compress_images=True,
                        )
                except Exception as e:
                    print(f"  ⚠️ Display log error: {str(e)[:80]}")
                time.sleep(max(1.0 / 10 - (time.perf_counter() - _disp_t0), 0.0))

        # The display thread now handles FOXGLOVE only (rerun logs on the main
        # control thread to avoid gRPC backpressure in a daemon). Only spawn it
        # when foxglove is enabled.
        if _foxglove:
            _disp_thread_obj = _threading.Thread(target=_display_thread, daemon=True)
            _disp_thread_obj.start()


        while True:
            # leader readings → both-arm action
            action = leader.get_action()

            # keyboard → head (standard WASD semantics: w/s=nod, a/d=shake)
            # head_pan(ID12)=shake, head_tilt(ID13)=nod (physically flashed this way)
            if keys.is_down("w"):
                head_tilt -= HEAD_TILT_SPEED / FPS
            if keys.is_down("s"):
                head_tilt += HEAD_TILT_SPEED / FPS
            if keys.is_down("a"):
                head_pan -= HEAD_PAN_SPEED / FPS
            if keys.is_down("d"):
                head_pan += HEAD_PAN_SPEED / FPS
            head_pan = max(head_pan_min, min(head_pan_max, head_pan))
            head_tilt = max(head_tilt_min, min(head_tilt_max, head_tilt))
            action["head_pan.pos"] = head_pan
            action["head_tilt.pos"] = head_tilt

            # keyboard → base (speed levels: each n/m press switches one level, edge-triggered)
            if keys.pressed_once("n"):
                speed_idx = min(speed_idx + 1, len(BASE_SPEED_LEVELS) - 1)
                print(f"  [Speed level {speed_idx+1}/{len(BASE_SPEED_LEVELS)}: {BASE_SPEED_LEVELS[speed_idx]}x]")
            if keys.pressed_once("m"):
                speed_idx = max(speed_idx - 1, 0)
                print(f"  [Speed level {speed_idx+1}/{len(BASE_SPEED_LEVELS)}: {BASE_SPEED_LEVELS[speed_idx]}x]")
            scale = BASE_SPEED_LEVELS[speed_idx]
            x, theta = 0.0, 0.0
            if keys.is_down("i"):
                x += BASE_LINEAR_SPEED * scale
            if keys.is_down("k"):
                x -= BASE_LINEAR_SPEED * scale
            if keys.is_down("j"):
                theta += BASE_ANGULAR_SPEED * scale
            if keys.is_down("l"):
                theta -= BASE_ANGULAR_SPEED * scale
            action["x.vel"] = x
            action["theta.vel"] = theta

            # keyboard → lift: hold u/h to control speed directly (release to stop)
            # dual-machine mode uses vel control; single-machine mode also uses vel uniformly (avoids P-controller target-chasing drift)
            v = 0
            if keys.is_down("u"):
                v = 60  # lift speed (BIT2=0: 60×50=3000 step/s ≈ 5.9mm/s)
            elif keys.is_down("h"):
                v = -60  # lower speed
            action["lift_axis.vel"] = v

            # show live lift status (refreshed every 0.5s)
            if time.time() - _last_lift_print > 0.5:
                _last_lift_print = time.time()
                _actual_h = follower.lift_axis.get_height_mm()
                _lim = "▲MAX" if _actual_h >= LIFT_MAX_MM else ("▼MIN" if _actual_h <= LIFT_MIN_MM else "")
                print(f"\rLift: actual={_actual_h:6.1f}mm  target={lift_h:6.1f}mm  limits[{LIFT_MIN_MM:.0f}~{LIFT_MAX_MM:.0f}]  {_lim}", end="", flush=True)

            follower.send_action(action)

            # Consume the newest observation EVERY loop (not only inside the
            # display branches): the host PUSH+SNDHWM=1 drops NEW frames when its
            # 1-slot queue is full, keeping the oldest one — so if we consume at
            # 15Hz while the host produces at 30Hz, the queue is always full and
            # we always receive a stale frame (latency grows unbounded). Matching
            # consumption to the host rate (AlohaMini pattern) keeps the queue
            # empty and every observation fresh. No message queued -> returns the
            # cached observation at ~zero cost (no decode happens).
            try:
                latest_obs = follower.get_observation()
            except Exception as e:
                latest_obs = {}
                print(f"  ⚠️ get_observation error: {str(e)[:80]}")

            # Hand the freshest obs+action to the display thread (cheap dict
            # swap under a lock — the display thread logs foxglove only).
            if _foxglove:
                with _disp_lock:
                    _disp_state["obs"] = latest_obs
                    _disp_state["action"] = action

            # Rerun logs on the MAIN control thread (same as record_data.py):
            # its gRPC sink backpressures on a bounded channel, and calling it
            # from the daemon display thread wedged the thread >5s -> frozen
            # viewer. Interleaving with the control loop provides natural
            # pacing so the sink stays drained. Images via _fresh_obs (send
            # only on change) + compression keep volume under the channel limit.
            if _rerun:
                try:
                    _rerun_last = getattr(follower, "_rerun_last_img_ids", {})
                    log_rerun_data(
                        observation=_strip_images(_fresh_obs(latest_obs, _rerun_last)),
                        action=action,
                        compress_images=True,
                    )
                    setattr(follower, "_rerun_last_img_ids", _rerun_last)
                except Exception as e:
                    print(f"  ⚠️ Rerun log error: {str(e)[:80]}")

            if keys.is_down("b"):
                print("\nQuitting...")
                break

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        print("\n⛔ Teleoperation stopped...")

    finally:
        # stop the display thread BEFORE tearing down foxglove/rerun, otherwise
        # the daemon keeps calling log_* after shutdown and crashes at exit.
        # (Only foxglove has a display thread; rerun logs on the main thread.)
        if _foxglove:
            try:
                _disp_stop.set()
                _disp_thread_obj.join(timeout=1.0)
            except Exception:
                pass
        # save the lift absolute position (no re-zeroing needed on next connect)
        try:
            follower.lift_axis.save_zero()
        except Exception:
            pass
        if args.display == "rerun":
            try:
                rerun.rerun_shutdown()
            except Exception:
                pass
        if args.display == "foxglove":
            try:
                from lerobot.utils.visualization_utils import shutdown_foxglove

                shutdown_foxglove()  # in-process server: stops with the script, no orphan
            except Exception:
                pass
        for _w in _web_servers:
            try:
                _w.terminate()
            except Exception:
                pass
        try:
            leader.disconnect()
        except Exception:
            pass
        try:
            follower.disconnect()
        except Exception:
            pass
        try:
            listener.stop()
        except Exception:
            pass
        print("Disconnected")


if __name__ == "__main__":
    main()
