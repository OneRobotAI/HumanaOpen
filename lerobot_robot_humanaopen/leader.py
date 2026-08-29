"""HumanaOpen leader-arm teleoperator.

Leader arm: open-arms-mini structure, 7-DOF + gripper, STS3215 C046 (7.4V),
8 servos per arm (IDs 1-8).

Design notes:
- Joint naming matches the follower arm exactly; the dual-arm class outputs
  left_arm_*/right_arm_* prefixes, so during teleoperation
  leader.get_action() can feed directly into follower.send_action() with zero conversion.
- Calibration: natural hang + gripper closed is the zero point (consistent with
  the follower's mid-position convention).
- Direction flips / wrist remapping reference the official lerobot openarm_mini
  (same-source hardware, verified).

Usage (dual-arm):
    from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig
    cfg = BiHumanaOpenLeaderConfig(
        id="leader",
        left_arm_port="/dev/ttyACM2",
        right_arm_port="/dev/ttyACM3",
    )
    leader = BiHumanaOpenLeader(cfg)
    leader.connect(calibrate=True)

Calibration files:
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/{id}_left.json
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/{id}_right.json
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from lerobot.motors import Motor, MotorCalibration, MotorNormMode
from lerobot.motors.feetech import FeetechMotorsBus, OperatingMode
from lerobot.teleoperators.config import TeleoperatorConfig
from lerobot.teleoperators.teleoperator import Teleoperator

logger = logging.getLogger(__name__)

# Global registry of connected robots: registered by HumanaOpen.connect() so
# HumanaOpenTeleop can read the head/lift initial positions (during record the
# teleop has no direct reference to the robot).
_CONNECTED_ROBOTS: list[Any] = []

# Globally shared pynput keyboard listener: avoids multiple Listeners competing
# for the keyboard on Linux/X11, which would scramble key events (record's
# init_keyboard_listener also starts its own Listener).
_KB_LISTENER = None
_KB_CALLBACKS: list[Any] = []


def _kb_on_press(key) -> None:
    try:
        ch = key.char
    except AttributeError:
        return
    if ch:
        for cb in _KB_CALLBACKS:
            try:
                cb(ch, True)
            except Exception:
                pass


def _kb_on_release(key) -> None:
    try:
        ch = key.char
    except AttributeError:
        return
    if ch:
        for cb in _KB_CALLBACKS:
            try:
                cb(ch, False)
            except Exception:
                pass


def register_keyboard_callback(callback) -> None:
    """Register a callback(ch, is_pressed) for global shared keyboard events."""
    global _KB_LISTENER
    _KB_CALLBACKS.append(callback)
    if _KB_LISTENER is None or not _KB_LISTENER.is_alive():
        from pynput import keyboard as kb

        _KB_LISTENER = kb.Listener(on_press=_kb_on_press, on_release=_kb_on_release)
        _KB_LISTENER.start()


def get_connected_robot() -> Any | None:
    """Return the most recently connected HumanaOpen robot, or None."""
    return _CONNECTED_ROBOTS[-1] if _CONNECTED_ROBOTS else None


def register_robot(robot: Any) -> None:
    """Register a connected robot (called from HumanaOpen.connect)."""
    _CONNECTED_ROBOTS.append(robot)

# Joint naming matches the follower (see humanaopen.py _make_arm_joint_names)
JOINT_NAMES = [
    "shoulder_pan",
    "shoulder_lift",
    "shoulder_roll",
    "elbow_flex",
    "forearm_rotation",
    "wrist_flex",
    "wrist_yaw",
    "gripper",
]

# Per-side direction flips (inverted on read), referencing the official
# openarm_mini SIDE_MOTORS_TO_FLIP.
# Note: this is the direction signature for this specific "official leader x
# official follower" hardware pairing. If your leader/follower assembly or
# servo mounting differs from the official one, adjust per joint based on tests
# (see examples/diagnose_teleop.py).
DEFAULT_SIDE_MOTORS_TO_FLIP: dict[str, list[str]] = {
    "left": ["shoulder_pan", "shoulder_roll", "elbow_flex", "forearm_rotation", "wrist_flex", "wrist_yaw"],
    "right": ["shoulder_pan", "shoulder_lift", "shoulder_roll", "elbow_flex", "forearm_rotation", "wrist_yaw"],
}

# Wrist flex<->yaw remapping (symmetric, its own inverse), referencing the
# official JOINT_REMAP.
# Official note: "deliberately swapped... feels more natural given how the human wrist moves".
# If your follower's wrist structure does not need the swap, empty the dict (adjust per testing).
DEFAULT_JOINT_REMAP = {"wrist_flex": "wrist_yaw", "wrist_yaw": "wrist_flex"}


@TeleoperatorConfig.register_subclass("humanaopen_leader")
@dataclass
class HumanaOpenLeaderConfig(TeleoperatorConfig):
    """Single-arm leader configuration.

    calibration_mode:
        - "full" (default): zero + record real ranges per joint. The
          action/observation normalization space is strictly consistent with
          the follower, teleoperation and data recording share the same
          calibration, no re-calibration needed.
        - "quick": zero + full joint range [0, 4095] (official openarm_mini
          simplified approach). Suitable for pure realtime teleoperation;
          re-calibrate to "full" before recording data for training.

    flip_joints:
        List of joints that need direction flips per side. Defaults to the
        official table; adjust per testing (diagnose_teleop.py).
    joint_remap:
        Joint remapping dict (source joint -> target joint). Defaults to the
        wrist flex<->yaw swap; empty it if not needed.
    """

    port: str
    side: str | None = None  # "left" / "right" / None
    use_degrees: bool = True
    calibration_mode: str = "full"
    flip_joints: dict[str, list[str]] | None = None  # None -> use official default table
    joint_remap: dict[str, str] | None = None  # None -> use official default remapping


@TeleoperatorConfig.register_subclass("bi_humanaopen_leader")
@dataclass
class BiHumanaOpenLeaderConfig(TeleoperatorConfig):
    """Dual-arm leader configuration.

    flip_joints / joint_remap: passed through to each single arm; see
    HumanaOpenLeaderConfig.
    """

    left_arm_port: str
    right_arm_port: str
    flip_joints: dict[str, list[str]] | None = None  # None -> use official default table
    joint_remap: dict[str, str] | None = None  # None -> use official default remapping


@TeleoperatorConfig.register_subclass("humanaopen_teleop")
@dataclass
class HumanaOpenTeleopConfig(BiHumanaOpenLeaderConfig):
    """Full-body teleoperator configuration (dual arms + keyboard head/lift/base, 21 DOF).

    robot: optional follower reference, used to initialize the current head/lift positions.
    """

    robot: Any = None  # set at runtime by the record script


class HumanaOpenLeader(Teleoperator):
    """HumanaOpen single-arm leader teleoperator (open-arms-mini, 7-DOF + gripper)."""

    config_class = HumanaOpenLeaderConfig
    name = "humanaopen_leader"

    def __init__(self, config: HumanaOpenLeaderConfig):
        super().__init__(config)
        self.config = config

        if config.side is not None and config.side not in DEFAULT_SIDE_MOTORS_TO_FLIP:
            raise ValueError(f"Invalid side '{config.side}'; expected 'left', 'right', or None.")
        flip_table = config.flip_joints or DEFAULT_SIDE_MOTORS_TO_FLIP
        self._motors_to_flip: list[str] = flip_table.get(config.side, []) if config.side else []
        self._joint_remap: dict[str, str] = config.joint_remap if config.joint_remap is not None else DEFAULT_JOINT_REMAP

        motors = {}
        for id_, name in enumerate(JOINT_NAMES, start=1):
            if name == "gripper":
                motors[name] = Motor(id_, "sts3215", MotorNormMode.RANGE_0_100)
            else:
                motors[name] = Motor(id_, "sts3215", MotorNormMode.DEGREES)

        self.bus = FeetechMotorsBus(
            port=config.port,
            motors=motors,
            calibration=self.calibration,
        )

    @property
    def action_features(self) -> dict[str, type]:
        return {f"{motor}.pos": float for motor in self.bus.motors}

    @property
    def feedback_features(self) -> dict[str, type]:
        return self.action_features

    @property
    def is_connected(self) -> bool:
        return self.bus.is_connected

    def connect(self, calibrate: bool = True) -> None:
        self.bus.connect()
        if calibrate:
            # Always enter calibrate(); it asks whether to reuse the existing
            # calibration file or run a new one.
            self.calibrate()
        self.configure()
        logger.info("%s connected.", self)

    @property
    def is_calibrated(self) -> bool:
        return self.bus.is_calibrated

    def calibrate(self) -> None:
        """Calibrate a single arm.

        - Zero: natural hang + gripper closed
        - "full" mode: record real ranges per joint (consistent with follower's normalization space)
        - "quick" mode: full joint range [0, 4095] (official openarm_mini simplification)
        - Gripper: closed/open two-point calibration
        """
        if self.calibration:
            user_input = input(
                f"Press ENTER to use existing calibration for {self.id}, "
                f"or type 'c' and press ENTER to run new calibration: "
            )
            if user_input.strip().lower() != "c":
                logger.info(f"Using existing calibration for {self.id}")
                self.bus.write_calibration(self.calibration)
                return

        logger.info(f"\nRunning calibration for {self}")
        self.bus.disable_torque()

        # Reference official openarm_mini: phase set to 12 (angle feedback mode)
        for motor in self.bus.motors:
            self.bus.write("Phase", motor, 12)
        for motor in self.bus.motors:
            self.bus.write("Operating_Mode", motor, OperatingMode.POSITION.value)

        input(
            "\nCalibration: Zero Position\n"
            "Position the arm in the following configuration:\n"
            "  - Arm hanging straight down\n"
            "  - Gripper closed\n"
            "Press ENTER when ready..."
        )

        homing_offsets = self.bus.set_half_turn_homings()
        logger.info("Arm zero position set.")

        if self.calibration is None:
            self.calibration = {}

        max_res = self.bus.model_resolution_table["sts3215"] - 1  # 4095

        # Record real ranges: run all motors (including gripper) sequentially
        # through their full travel; the table shows each joint's MIN | POS | MAX
        # — consistent with the follower calibration.
        if self.config.calibration_mode == "full":
            print(
                "\nMove all joints (including gripper) sequentially through their "
                "entire ranges of motion.\nRecording positions. Press ENTER to stop..."
            )
            range_mins, range_maxes = self.bus.record_ranges_of_motion(list(self.bus.motors))

        for motor_name, motor in self.bus.motors.items():
            if self.config.calibration_mode == "full":
                range_min = int(range_mins.get(motor_name, 0))
                range_max = int(range_maxes.get(motor_name, max_res))
                if motor_name == "gripper":
                    # Closed end is at zero (near 2048; set_half_turn_homings already
                    # put the zero at 2048).
                    # Closed end near min -> open end is max (drive_mode=0);
                    # closed end near max -> open end is min (drive_mode=1).
                    mid = (range_min + range_max) / 2
                    drive_mode = 1 if 2048 > mid else 0
                else:
                    drive_mode = 0
                logger.info(f"  {motor_name}: range [{range_min}, {range_max}] (recorded)")
            else:
                range_min, range_max, drive_mode = 0, max_res, 0

            self.calibration[motor_name] = MotorCalibration(
                id=motor.id,
                drive_mode=drive_mode,
                homing_offset=homing_offsets[motor_name],
                range_min=range_min,
                range_max=range_max,
            )

        self.bus.write_calibration(self.calibration)
        self._save_calibration()
        print(f"\nCalibration complete and saved to {self.calibration_fpath}")

    def configure(self) -> None:
        self.bus.disable_torque()
        self.bus.configure_motors()
        for motor in self.bus.motors:
            self.bus.write("Operating_Mode", motor, OperatingMode.POSITION.value)

    def setup_motors(self) -> None:
        for motor in reversed(self.bus.motors):
            input(f"Connect the controller board to the '{motor}' motor only and press enter.")
            self.bus.setup_motor(motor)
            print(f"'{motor}' motor id set to {self.bus.motors[motor].id}")

    def get_action(self) -> dict[str, float]:
        """Read joint positions -> action (direction flips + wrist remapping).

        The gripper outputs its normalized [0,100] value directly (0=closed,
        100=open), isomorphic with the follower's RANGE_0_100.
        """
        positions = self.bus.sync_read("Present_Position")
        action: dict[str, float] = {}
        for motor, val in positions.items():
            target = self._joint_remap.get(motor, motor)
            if motor == "gripper":
                action[f"{target}.pos"] = val
            else:
                action[f"{target}.pos"] = -val if motor in self._motors_to_flip else val
        return action

    def enable_torque(self) -> None:
        self.bus.enable_torque()

    def disable_torque(self) -> None:
        self.bus.disable_torque()

    def write_goal_positions(self, positions: dict[str, float]) -> None:
        goals: dict[str, float] = {}
        for key, val in positions.items():
            if not key.endswith(".pos"):
                continue
            base = key.removesuffix(".pos")
            target = self._joint_remap.get(base, base)
            if base == "gripper":
                goals[target] = val
            else:
                goals[target] = -val if target in self._motors_to_flip else val
        if goals:
            self.bus.sync_write("Goal_Position", goals)

    def send_feedback(self, feedback: dict[str, float]) -> None:
        self.write_goal_positions(feedback)

    def disconnect(self) -> None:
        self.bus.disconnect()
        logger.info("%s disconnected.", self)


class BiHumanaOpenLeader(Teleoperator):
    """HumanaOpen dual-arm leader teleoperator — combines left and right single arms.

    Output actions carry left_arm_*/right_arm_* prefixes, matching the HumanaOpen
    follower's action/observation naming, so they can feed directly into
    follower.send_action().
    """

    config_class = BiHumanaOpenLeaderConfig
    name = "bi_humanaopen_leader"

    def __init__(self, config: BiHumanaOpenLeaderConfig):
        super().__init__(config)
        self.config = config

        left_config = HumanaOpenLeaderConfig(
            id=f"{config.id}_left" if config.id else None,
            calibration_dir=config.calibration_dir,
            port=config.left_arm_port,
            side="left",
            flip_joints=config.flip_joints,
            joint_remap=config.joint_remap,
        )
        right_config = HumanaOpenLeaderConfig(
            id=f"{config.id}_right" if config.id else None,
            calibration_dir=config.calibration_dir,
            port=config.right_arm_port,
            side="right",
            flip_joints=config.flip_joints,
            joint_remap=config.joint_remap,
        )

        self.left_arm = HumanaOpenLeader(left_config)
        self.right_arm = HumanaOpenLeader(right_config)

    @property
    def action_features(self) -> dict[str, type]:
        return {f"left_arm_{k}": v for k, v in self.left_arm.action_features.items()} | {
            f"right_arm_{k}": v for k, v in self.right_arm.action_features.items()
        }

    @property
    def feedback_features(self) -> dict[str, type]:
        return {}

    @property
    def is_connected(self) -> bool:
        return self.left_arm.is_connected and self.right_arm.is_connected

    def connect(self, calibrate: bool = True) -> None:
        self.left_arm.connect(calibrate)
        self.right_arm.connect(calibrate)

    @property
    def is_calibrated(self) -> bool:
        return self.left_arm.is_calibrated and self.right_arm.is_calibrated

    def calibrate(self) -> None:
        self.left_arm.calibrate()
        self.right_arm.calibrate()

    def configure(self) -> None:
        self.left_arm.configure()
        self.right_arm.configure()

    def setup_motors(self) -> None:
        self.left_arm.setup_motors()
        self.right_arm.setup_motors()

    def get_action(self) -> dict[str, float]:
        action: dict[str, float] = {}
        action.update({f"left_arm_{k}": v for k, v in self.left_arm.get_action().items()})
        action.update({f"right_arm_{k}": v for k, v in self.right_arm.get_action().items()})
        return action

    def enable_torque(self) -> None:
        self.left_arm.enable_torque()
        self.right_arm.enable_torque()

    def disable_torque(self) -> None:
        self.left_arm.disable_torque()
        self.right_arm.disable_torque()

    def send_feedback(self, feedback: dict[str, float]) -> None:
        left = {k.removeprefix("left_arm_"): v for k, v in feedback.items() if k.startswith("left_arm_")}
        right = {k.removeprefix("right_arm_"): v for k, v in feedback.items() if k.startswith("right_arm_")}
        if left:
            self.left_arm.write_goal_positions(left)
        if right:
            self.right_arm.write_goal_positions(right)

    def disconnect(self) -> None:
        self.left_arm.disconnect()
        self.right_arm.disconnect()
        logger.info("%s disconnected.", self)


class HumanaOpenTeleop(BiHumanaOpenLeader):
    """Full-body teleoperator: leader arms + keyboard for head/lift/base.

    Extends BiHumanaOpenLeader so the action dict includes all 21 DOF
    (16 arm joints + head_pan/head_tilt + x.vel/theta.vel + lift height),
    matching HumanaOpen's full action_features — required for data
    collection where every DOF is recorded for training.

    Head/lift/base are driven by keyboard (same keys as the teleop script)
    and held at their current value otherwise. The robot reference is used
    to read the current head/lift state as the starting point.
    """

    HEAD_PAN_SPEED = 20.0    # normalized units/s (RANGE_M100_100 space)
    HEAD_TILT_SPEED = 20.0
    BASE_LINEAR_SPEED = 0.2  # m/s
    BASE_ANGULAR_SPEED = 30.0  # deg/s
    BASE_SPEED_LEVELS = [0.3, 0.6, 1.0]
    LIFT_SPEED_MM = 15.0
    LIFT_MIN_MM = 3.0
    LIFT_MAX_MM = 200.0
    FPS = 30

    def __init__(self, config: BiHumanaOpenLeaderConfig, robot=None):
        super().__init__(config)
        self._robot = robot
        self._head_pan = 0.0
        self._head_tilt = 0.0
        self._lift_h = 0.0
        self._speed_idx = 1
        self._keys: set[str] = set()
        self._prev_keys: set[str] = set()
        self._listener = None
        self._kb_active = True  # whether the keyboard is active: set to False on override to block key updates

    @cached_property
    def action_features(self) -> dict[str, type]:
        arms = super().action_features
        extras = {
            "head_pan.pos": float,
            "head_tilt.pos": float,
            "x.vel": float,
            "theta.vel": float,
            "lift_axis.height_mm": float,
        }
        return {**arms, **extras}

    def _start_keyboard(self) -> None:
        # Reuse the global shared listener (multiple pynput Listeners on
        # Linux/X11 would conflict over the keyboard)
        def cb(ch: str, is_pressed: bool) -> None:
            if not self._kb_active:
                return
            if is_pressed:
                self._keys.add(ch)
            else:
                self._keys.discard(ch)

        self._kb_cb = cb
        register_keyboard_callback(cb)

    def connect(self, calibrate: bool = True) -> None:
        super().connect(calibrate)
        self._start_keyboard()
        # Try to read the current head/lift positions from config.robot or the global registry
        robot = self._robot
        if robot is None:
            robot = get_connected_robot()
        if robot is not None:
            try:
                obs = robot.get_observation()
                self._head_pan = obs.get("head_pan.pos", 0.0)
                self._head_tilt = obs.get("head_tilt.pos", 0.0)
                self._lift_h = obs.get("lift_axis.height_mm", self.LIFT_MIN_MM)
            except Exception:
                pass

    def _edge_pressed(self, char: str) -> bool:
        down = char in self._keys
        was = char in self._prev_keys
        return down and not was

    def _update_keyboard_state(self) -> None:
        """Apply keyboard to head/lift/base target values (same keys as teleop script)."""
        # speed levels (n/m, edge-triggered)
        if self._edge_pressed("n"):
            self._speed_idx = min(self._speed_idx + 1, len(self.BASE_SPEED_LEVELS) - 1)
        if self._edge_pressed("m"):
            self._speed_idx = max(self._speed_idx - 1, 0)

        # head (w/s = tilt, a/d = pan)
        if "w" in self._keys:
            self._head_tilt -= self.HEAD_TILT_SPEED / self.FPS
        if "s" in self._keys:
            self._head_tilt += self.HEAD_TILT_SPEED / self.FPS
        if "a" in self._keys:
            self._head_pan -= self.HEAD_PAN_SPEED / self.FPS
        if "d" in self._keys:
            self._head_pan += self.HEAD_PAN_SPEED / self.FPS
        # clamp to calibration range (±100 in RANGE_M100_100 space)
        self._head_pan = max(-100.0, min(100.0, self._head_pan))
        self._head_tilt = max(-100.0, min(100.0, self._head_tilt))

        # lift (u/h)
        if "u" in self._keys:
            self._lift_h += self.LIFT_SPEED_MM / self.FPS
        if "h" in self._keys:
            self._lift_h -= self.LIFT_SPEED_MM / self.FPS
        self._lift_h = max(self.LIFT_MIN_MM, min(self.LIFT_MAX_MM, self._lift_h))

    def get_action(self) -> dict[str, float]:
        action = super().get_action()  # 16 arm joints

        self._update_keyboard_state()

        # head (normalized space, matching robot observation)
        action["head_pan.pos"] = self._head_pan
        action["head_tilt.pos"] = self._head_tilt

        # base: velocity commands (same mapping as teleop script)
        scale = self.BASE_SPEED_LEVELS[self._speed_idx]
        x, theta = 0.0, 0.0
        if "i" in self._keys:
            x += self.BASE_LINEAR_SPEED * scale
        if "k" in self._keys:
            x -= self.BASE_LINEAR_SPEED * scale
        if "j" in self._keys:
            theta += self.BASE_ANGULAR_SPEED * scale
        if "l" in self._keys:
            theta -= self.BASE_ANGULAR_SPEED * scale
        action["x.vel"] = x
        action["theta.vel"] = theta

        # lift height target
        action["lift_axis.height_mm"] = self._lift_h

        self._prev_keys = set(self._keys)
        return action

    def disconnect(self) -> None:
        if self._listener is not None:
            try:
                self._listener.stop()
            except Exception:
                pass
        super().disconnect()
