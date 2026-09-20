"""ZMQ host launcher — run this ON the robot side (Jetson / Raspberry Pi).

Wraps ``HumanaOpenHost`` with the same command-line style as the
teleop / record / eval scripts, so the bus topology and cameras are
selected with flags instead of editing a ``python3 -c`` one-liner.

Usage (2-bus / 3-bus × with / without cameras):

    # 2-bus, no cameras (pure control, no video)
    python3 examples/humanaopen_host_launcher.py --no-cameras

    # 2-bus, with cameras (default bus layout + default camera devices)
    python3 examples/humanaopen_host_launcher.py

    # 3-bus (lift + wheels on their own port), with cameras
    python3 examples/humanaopen_host_launcher.py --robot.port3 /dev/ttyACM2

    # 3-bus, no cameras
    python3 examples/humanaopen_host_launcher.py --robot.port3 /dev/ttyACM2 --no-cameras

    # Override a specific camera device (or all of them)
    python3 examples/humanaopen_host_launcher.py --head-camera /dev/video1
    python3 examples/humanaopen_host_launcher.py --head-camera /dev/video1 --left-wrist-camera /dev/video3 --right-wrist-camera /dev/video5

``--robot.port3 None`` (or any empty value) = 2-bus mode; a device name =
3-bus mode. When 3-bus is selected and the listed device does not exist,
startup fails fast with a clear error instead of silently running 2-bus.

Default cameras follow the README: head=/dev/video0, left_wrist=/dev/video2,
right_wrist=/dev/video4. Check your board with ``lerobot-find-cameras``
(or ``v4l2-ctl --list-devices``) and override as needed.
"""

from __future__ import annotations

import argparse
import sys

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost

DEFAULT_CAM_DEVICES = {
    "head": "/dev/video0",
    "left_wrist": "/dev/video2",
    "right_wrist": "/dev/video4",
}
CAMERA_NAMES = ("head", "left_wrist", "right_wrist", "chest")
CAMERA_W, CAMERA_H, CAMERA_FPS, CAMERA_FOURCC = 640, 480, 30, "MJPG"


def _parse_port(s: str | None) -> str | None:
    """argparse turns 'None' into a string; convert it back to a real None (2-bus mode)."""
    if s is None or str(s).strip().lower() == "none" or str(s).strip() == "":
        return None
    return str(s)


def build_cameras(args) -> dict[str, OpenCVCameraConfig]:
    """Build the camera dict: default three cameras, or {} with --no-cameras.

    Per-camera --<name>-camera overrides the default device; a chest camera
    must be requested explicitly via --chest-camera (not enabled by default).
    """
    if args.no_cameras:
        return {}
    cams = {}
    for name in CAMERA_NAMES:
        dev = getattr(args, f"{name}_camera", None)
        if dev is None and name not in DEFAULT_CAM_DEVICES:
            continue  # chest only when explicitly requested
        dev = dev or DEFAULT_CAM_DEVICES[name]
        cams[name] = OpenCVCameraConfig(
            index_or_path=dev,
            fps=CAMERA_FPS,
            width=CAMERA_W,
            height=CAMERA_H,
            fourcc=CAMERA_FOURCC,
        )
        print(f"  📷 {name}: {dev} @{CAMERA_FPS}fps {CAMERA_FOURCC}")
    return cams


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HumanaOpen ZMQ host (robot side). Ctrl+C to stop.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--robot.port1", default="/dev/ttyACM0", help="follower bus 1 (left arm + head)")
    parser.add_argument("--robot.port2", default="/dev/ttyACM1", help="follower bus 2 (right arm)")
    parser.add_argument("--robot.port3", default=None, help="follower bus 3 (lift + wheels); 'None' = 2-bus mode (wheels+lift on port2)")
    parser.add_argument("--no-cameras", action="store_true", help="run without cameras (pure control, no video stream)")
    for name in ("head", "left_wrist", "right_wrist", "chest"):
        parser.add_argument(f"--{name}-camera", default=None, help=f"{name} camera device (default {DEFAULT_CAM_DEVICES.get(name, 'off')})")
    parser.add_argument("--port_zmq_cmd", type=int, default=5555)
    parser.add_argument("--port_zmq_obs", type=int, default=5556)
    args = parser.parse_args()

    port3 = _parse_port(getattr(args, "robot.port3", None))
    port1 = getattr(args, "robot.port1", "/dev/ttyACM0")
    port2 = getattr(args, "robot.port2", "/dev/ttyACM1")

    cam_dict = build_cameras(args)
    layout = "2-bus (wheels+lift on port2)" if port3 is None else f"3-bus (wheels+lift on {port3})"
    print(f"  Bus topology: {layout}")
    print(f"  Cameras: {', '.join(cam_dict) if cam_dict else 'none'}")

    cfg = HumanaOpenConfig(
        id="follower",
        port1=port1,
        port2=port2,
        port3=port3,
        cameras=cam_dict,
        wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
    )
    print("  🚀 Starting ZMQ host (Ctrl+C to stop)...")
    HumanaOpenHost(cfg).run()


if __name__ == "__main__":
    import faulthandler

    # Ctrl+C while hung: dump every thread's Python stack BEFORE exiting, so
    # the exact frames where connect() blocked (bus handshake / ping / lift)
    # show up instead of silently returning to the prompt.
    faulthandler.enable()
    original_int = signal.getsignal(signal.SIGINT)

    def _on_sigint(signum, frame):
        print("\n\n⏸ Ctrl+C — dumping thread stacks (use these to find the hang):", flush=True)
        for thread_id, stack in sys._current_frames().items():
            cur = sys._current_frames()[thread_id]
            print(f"\n── thread {thread_id} ──", flush=True)
            import traceback

            for f in traceback.extract_stack(stack):
                print(f"   {f.filename}:{f.lineno} in {f.name}", flush=True)
        print("\nExiting (Ctrl+C). Re-pull & rerun if you need the exact hang stack.", flush=True)
        sys.exit(130)

    signal.signal(signal.SIGINT, _on_sigint)
    signal.signal(signal.SIGTERM, _on_sigint)

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)