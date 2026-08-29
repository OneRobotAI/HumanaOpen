"""HumanaOpen robot configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from lerobot.cameras.configs import CameraConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.robots.config import RobotConfig

from .lift_axis import LiftAxisConfig


def default_cameras() -> dict[str, CameraConfig]:
    """Default camera setup — 3 × USB webcams (MJPG, 30fps except right_wrist).

    Adjust indices/paths to match your actual hardware.
    """
    return {
        "head": OpenCVCameraConfig(
            index_or_path="/dev/video0",
            fps=30,
            width=640,
            height=480,
            fourcc="MJPG",
        ),
        "left_wrist": OpenCVCameraConfig(
            index_or_path="/dev/video2",
            fps=30,
            width=640,
            height=480,
            fourcc="MJPG",
        ),
        "right_wrist": OpenCVCameraConfig(
            index_or_path="/dev/video4",
            fps=25,
            width=640,
            height=480,
            fourcc="MJPG",
        ),
    }


def chest_camera() -> OpenCVCameraConfig:
    """Optional 4th camera — chest view (MJPG, 30fps on current hardware)."""
    return OpenCVCameraConfig(
        index_or_path="/dev/video6",
        fps=30,
        width=640,
        height=480,
        fourcc="MJPG",
    )


@RobotConfig.register_subclass("humanaopen")
@dataclass
class HumanaOpenConfig(RobotConfig):
    """Configuration for the HumanaOpen semi-humanoid robot.

    Follower motors (12V — all ST3215 C018 except lift uses ST3250):

    +---------------------+------+--------+----------+-----------------+
    | Group               | IDs  | Count  | Mode     | Motor           |
    +---------------------+------+--------+----------+-----------------+
    | Left arm (7-DOF+G)  | 1-8  | 8      | POSITION | ST3215 C018     |
    | Right arm (7-DOF+G) | 1-8  | 8      | POSITION | ST3215 C018     |
    | Head pan/tilt       | 12,13| 2      | POSITION | ST3215 C018     |
    | Lift                | 9    | 1      | VELOCITY | **ST3250**      |
    | Left/Right wheel    | 10,11| 2      | VELOCITY | ST3215 C018     |
    +---------------------+------+--------+----------+-----------------+

    Leader arms (teleop, separate machine): STS3215 C046, 7.4V.

    Bus topology (3-bus default)
    ----------------------------
    ``port1`` — Left arm (IDs 1-8) + Head pan/tilt (IDs 12,13) … POSITION mode
    ``port2`` — Right arm (IDs 1-8) … POSITION mode
    ``port3`` — Lift (ID 9) + Left wheel (ID 10) + Right wheel (ID 11)

    To run 2-bus mode set ``port3 = None``:
        bus2 then also hosts the lift and wheel motors.

    Follower arm kinematics (human-like):
        3 shoulder (pan/lift/roll) + 1 elbow + 1 forearm rotation + 2 wrist (flex/yaw) + 1 gripper.
    """

    # ---- Serial ports (leave empty to skip the bus entirely) ----------------
    id: str = "follower"
    port1: str = "/dev/ttyACM0"
    port2: str = "/dev/ttyACM1"
    port3: str | None = "/dev/ttyACM2"
    disable_torque_on_disconnect: bool = True

    # ---- Lift homing on connect ---------------------------------------------
    # Handling of the lift on connect(): prefer restoring the absolute position from
    # the persistent file (no re-homing; the self-locking leadscrew keeps the
    # position unchanged so it is reproducible); only home to the bottom via
    # stall-detection when recovery fails.
    # Set to ``False`` to skip both entirely (only when lift position is known good).
    home_lift_on_connect: bool = True

    # Wait for manual adjustment after homing: if automatic homing is triggered
    # (lift stops at the bottom, 0mm), after homing prompt and wait for the operator
    # to manually raise the lift to the desired height, pressing ENTER to continue.
    # For scenarios that need to start from a specific height, e.g. data collection;
    # set False for pure teleoperation (adjustable anytime after startup).
    confirm_lift_after_home: bool = False

    # ---- Enable the differential-drive base (wheels) ------------------------
    # Set to ``False`` when the base is not wired up yet (e.g. arms-only testing).
    # In 2-bus mode (port3=None) this also removes the wheel motors from bus 2.
    enable_base: bool = True

    # ---- Safety limiter ----------------------------------------------------
    # Clamp per-step position changes to this value (degrees or %).
    max_relative_target: int | None = None

    # ---- Cameras -----------------------------------------------------------
    cameras: dict[str, CameraConfig] = field(default_factory=default_cameras)

    # ---- Normalisation (degrees vs -100..100) ------------------------------
    use_degrees: bool = False

    # ---- Differential-drive parameters -------------------------------------
    wheel_radius: float = 0.0635  # metres (127mm wheel diameter)
    wheelbase: float = 0.30      # metres (distance between left & right wheels)
    max_wheel_raw: int = 3000    # maximum raw velocity command

    # ---- Wheel direction signs ----------------------------------------------
    # ``+1`` = positive raw velocity drives the wheel forward.
    # ``-1`` = inverted wheel (motor mounted mirrored). If forward turns the
    # robot into a spin, flip the sign of the wheel that is mounted backwards.
    wheel_dir_signs: dict[str, int] = field(
        default_factory=lambda: {
            "base_left_wheel": -1,
            "base_right_wheel": 1,
        }
    )
    # ---- Lift Axis ---------------------------------------------------------
    # Zero persistence enabled by default: save the absolute position after home
    # so subsequent connections recover without re-homing.
    lift: LiftAxisConfig = field(
        default_factory=lambda: LiftAxisConfig(
            zero_file=os.path.expanduser("~/.cache/humanaopen/lift_zero.json")
        )
    )

    # ---- Keyboard teleop keymap (used by examples / base driver) -----------
    teleop_keys: dict[str, str] = field(
        default_factory=lambda: {
            "forward": "i",
            "backward": "k",
            "rotate_left": "j",
            "rotate_right": "l",
            "speed_up": "n",
            "speed_down": "m",
            "lift_up": "u",
            "lift_down": "h",
            "quit": "b",
        }
    )


# ---------------------------------------------------------------------------
# ZMQ remote configs
# ---------------------------------------------------------------------------

@dataclass
class HumanaOpenHostConfig:
    """Configuration for the robot-side ZMQ host process."""

    port_zmq_cmd: int = 5555
    port_zmq_observations: int = 5556
    connection_time_s: int = 3600
    watchdog_timeout_ms: int = 500
    max_loop_freq_hz: int = 30
    # Image capture frequency: under the threaded scheme this does not affect action
    # latency, so it is fixed at 30Hz (high quality)
    image_fps: int = 30


@RobotConfig.register_subclass("humanaopen_client")
@dataclass
class HumanaOpenClientConfig(RobotConfig):
    """Configuration for the teleoperation-side ZMQ client."""

    remote_ip: str = "127.0.0.1"
    port_zmq_cmd: int = 5555
    port_zmq_observations: int = 5556

    # Differential-drive parameters (mirrored from host)
    wheel_radius: float = 0.06
    wheelbase: float = 0.30

    teleop_keys: dict[str, str] = field(
        default_factory=lambda: {
            "forward": "i",
            "backward": "k",
            "rotate_left": "j",
            "rotate_right": "l",
            "speed_up": "n",
            "speed_down": "m",
            "lift_up": "u",
            "lift_down": "h",
            "quit": "b",
        }
    )
    cameras: dict[str, CameraConfig] = field(default_factory=dict)

    polling_timeout_ms: int = 15
    connect_timeout_s: int = 5
