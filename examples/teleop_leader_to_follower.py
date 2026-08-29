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
import threading
import time

import numpy as np
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
    parser.add_argument("--display", action="store_true", help="use rerun to display camera feeds and joint states in real time")
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
        _client_cfg = HumanaOpenClientConfig(
            remote_ip=args.remote_ip, port_zmq_cmd=args.port_zmq_cmd,
            port_zmq_observations=args.port_zmq_obs,
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
            # Show which image keys the Host actually streams (may differ from --cameras).
            # ZMQ PUB/SUB has a slow-joiner window (~1s) during which the first frames are
            # dropped, so wait a moment and sample a few times before deciding.
            obs0 = {}
            for _ in range(10):
                obs0 = follower.get_observation()
                if any(isinstance(v, np.ndarray) and v.ndim == 3 for v in obs0.values()):
                    break
                time.sleep(0.2)
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

        # optional rerun live visualization (camera feeds + joint states)
        if args.display:
            try:
                from lerobot.utils.visualization_utils import init_rerun, log_rerun_data
                init_rerun(session_name="humanaopen_teleop")
                log_rerun_data(observation=_strip_images(obs))
                print("  👁 Rerun visualization started (view in rerun viewer)")
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
        _last_display = 0.0  # throttles rerun logging
        _rerun = args.display  # whether rerun is enabled

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

            # rerun logging (5Hz, to avoid slowing the 30FPS control loop)
            if _rerun and time.time() - _last_display > 0.2:
                _last_display = time.time()
                try:
                    log_rerun_data(observation=_strip_images(follower.get_observation()), action=action)
                except Exception:
                    pass

            if keys.is_down("b"):
                print("\nQuitting...")
                break

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        print("\n⛔ Teleoperation stopped...")

    finally:
        # save the lift absolute position (no re-zeroing needed on next connect)
        try:
            follower.lift_axis.save_zero()
        except Exception:
            pass
        if args.display:
            try:
                import rerun as rr
                rr.rerun_shutdown()
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
