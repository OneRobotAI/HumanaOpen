"""HumanaOpen — Bimanual 7-DOF mobile robot with lift and differential drive."""

from __future__ import annotations

import logging
import time
from functools import cached_property
from itertools import chain
from typing import Any

import numpy as np

from lerobot.cameras.utils import make_cameras_from_configs
from lerobot.motors import Motor, MotorCalibration, MotorNormMode
from lerobot.motors.feetech import FeetechMotorsBus, OperatingMode
from lerobot.robots.robot import Robot
from lerobot.robots.utils import ensure_safe_goal_position
from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError

from .config_humanaopen import HumanaOpenConfig
from .lift_axis import HumanaOpenLiftAxis

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_arm_joint_names(prefix: str) -> list[str]:
    """Return joint names for a 7-DOF + gripper arm."""
    return [
        f"{prefix}_shoulder_pan",
        f"{prefix}_shoulder_lift",
        f"{prefix}_shoulder_roll",
        f"{prefix}_elbow_flex",
        f"{prefix}_forearm_rotation",
        f"{prefix}_wrist_flex",
        f"{prefix}_wrist_yaw",
        f"{prefix}_gripper",
    ]


LEFT_ARM_JOINTS = _make_arm_joint_names("left_arm")
RIGHT_ARM_JOINTS = _make_arm_joint_names("right_arm")
HEAD_JOINTS = ["head_pan", "head_tilt"]
WHEEL_JOINTS = ["base_left_wheel", "base_right_wheel"]


def _joint_names() -> list[str]:
    return LEFT_ARM_JOINTS + RIGHT_ARM_JOINTS + HEAD_JOINTS


def _state_keys() -> list[str]:
    return [f"{j}.pos" for j in _joint_names()] + ["x.vel", "theta.vel", "lift_axis.height_mm"]


def _motor_specs(use_degrees: bool) -> dict[str, tuple[int, str, MotorNormMode]]:
    """Return {name: (motor_id, model, norm_mode)} for every motor on the robot.

    The caller decides which bus each motor lands on — this is just the central
    registry so we never accidentally duplicate ID assignments.
    """
    arm_norm = MotorNormMode.DEGREES if use_degrees else MotorNormMode.RANGE_M100_100
    specs: dict[str, tuple[int, str, MotorNormMode]] = {}

    for i, name in enumerate(LEFT_ARM_JOINTS, start=1):
        mode = MotorNormMode.RANGE_0_100 if name.endswith("gripper") else arm_norm
        specs[name] = (i, "sts3215", mode)
    for i, name in enumerate(RIGHT_ARM_JOINTS, start=1):
        mode = MotorNormMode.RANGE_0_100 if name.endswith("gripper") else arm_norm
        specs[name] = (i, "sts3215", mode)
    specs["head_pan"] = (12, "sts3215", arm_norm)
    specs["head_tilt"] = (13, "sts3215", arm_norm)
    # Wheels — velocity mode, never calibrated in position space
    specs["base_left_wheel"] = (10, "sts3215", MotorNormMode.RANGE_M100_100)
    specs["base_right_wheel"] = (11, "sts3215", MotorNormMode.RANGE_M100_100)
    return specs


# ---------------------------------------------------------------------------
# Robot class
# ---------------------------------------------------------------------------

class HumanaOpen(Robot):
    """7-DOF dual-arm semi-humanoid robot with differential drive and lift.

    Motor bus topology
    ------------------
    **3-bus** (``port3`` is set — default):

    + ``port1`` — left arm (IDs 1-8) + head pan/tilt (IDs 12,13) … POSITION
    + ``port2`` — right arm (IDs 1-8) … POSITION
    + ``port3`` — lift (ID 9) + left wheel (ID 10) + right wheel (ID 11)

    **2-bus** (``port3 = None``):

    + ``port1`` — left arm + head
    + ``port2`` — right arm + lift + wheels  (mixed POSITION / VELOCITY)

    All arms are 7-DOF (3 shoulder + 1 elbow + 1 forearm + 2 wrist) + 1 gripper.
    """

    config_class = HumanaOpenConfig
    name = "humanaopen"

    def __init__(self, config: HumanaOpenConfig):
        super().__init__(config)
        self.config = config
        self._motor_specs = _motor_specs(config.use_degrees)

        # ── Calibration split ────────────────────────────────────────────
        # The calibration JSON stores *position* calibrations.  Wheels &
        # lift are velocity-controlled and use homing / full-range instead.
        cal = self.calibration

        def _maybe_cal(name: str) -> dict:
            return {k: v for k, v in cal.items() if k.startswith(name)}

        # Bus 1 hosts left arm AND head — both calibration prefixes must go
        # together (left_arm_* and head_*). Merging (|) instead of or-else
        # guarantees head calibration is not dropped.
        cal_left = _maybe_cal("left_arm") | _maybe_cal("head") or None
        cal_right = _maybe_cal("right_arm") or None
        cal_wheels = _maybe_cal("base") or None

        # ── Bus 1: left arm + head ──────────────────────────────────────
        self.bus1 = FeetechMotorsBus(
            port=self.config.port1,
            motors={
                n: Motor(*self._motor_specs[n])
                for n in LEFT_ARM_JOINTS + HEAD_JOINTS
            },
            calibration=cal_left or {},
        )

        # ── Bus 2: right arm + (optionally lift + wheels) ──────────────
        bus2_motors: dict[str, Motor] = {
            n: Motor(*self._motor_specs[n]) for n in RIGHT_ARM_JOINTS
        }

        if self.config.port3 is None and self.config.enable_base:
            # 2-bus mode — wheels & lift share bus 2
            for n in WHEEL_JOINTS:
                bus2_motors[n] = Motor(*self._motor_specs[n])
            wheel_cal = cal_wheels
        else:
            wheel_cal = cal_wheels

        self.bus2 = FeetechMotorsBus(
            port=self.config.port2,
            motors=bus2_motors,
            calibration=cal_right or {},
        )
        if self.config.port3 is None and self.config.enable_base:
            # 2-bus mode — lift shares bus 2 (bus2 now exists)
            lift_bus = self.bus2
        else:
            lift_bus = None

        # ── Bus 3 (3-bus mode only) ──────────────────────────────────────
        if self.config.port3 is not None and self.config.enable_base:
            self.bus3 = FeetechMotorsBus(
                port=self.config.port3,
                motors={
                    n: Motor(*self._motor_specs[n]) for n in WHEEL_JOINTS
                },
                calibration=wheel_cal or {},
            )
            lift_bus = self.bus3
        else:
            self.bus3 = None
            # already set lift_bus = self.bus2 above

        # ── Lift Axis (always separate from the main feature dict) ──────
        self.lift_axis = HumanaOpenLiftAxis(self.config.lift, lift_bus)

        # ── Motor-group listings (for sync_read/write) ──────────────────
        self.left_arm_motors = LEFT_ARM_JOINTS[:]
        self.right_arm_motors = RIGHT_ARM_JOINTS[:]
        self.head_motors = HEAD_JOINTS[:]
        self.wheel_motors = WHEEL_JOINTS[:]
        self.arm_motors = self.left_arm_motors + self.right_arm_motors + self.head_motors

        # ── Cameras ──────────────────────────────────────────────────────
        self.cameras = make_cameras_from_configs(config.cameras)

    # ── Feature descriptors ───────────────────────────────────────────────

    @property
    def _state_ft(self) -> dict[str, type]:
        return dict.fromkeys(_state_keys(), float)

    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        return {
            cam: (self.config.cameras[cam].height, self.config.cameras[cam].width, 3)
            for cam in self.cameras
        }

    @cached_property
    def observation_features(self) -> dict[str, type | tuple]:
        return {**self._state_ft, **self._cameras_ft}

    @cached_property
    def action_features(self) -> dict[str, type]:
        return self._state_ft

    # ── Connection ────────────────────────────────────────────────────────

    @property
    def is_connected(self) -> bool:
        ok = self.bus1.is_connected and self.bus2.is_connected
        if self.bus3 is not None:
            ok = ok and self.bus3.is_connected
        ok = ok and all(cam.is_connected for cam in self.cameras.values())
        return ok

    @property
    def is_calibrated(self) -> bool:
        return self.bus1.is_calibrated and self.bus2.is_calibrated

    def connect(self, calibrate: bool = True) -> None:
        if self.is_connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")

        self.bus1.connect()
        self.bus2.connect()
        if self.bus3 is not None:
            self.bus3.connect()

        # ── Calibration ─────────────────────────────────────────────────
        # Only run interactive calibration if no file exists OR user requests it.
        if self.calibration_fpath.is_file():
            logger.info(f"Calibration file found at {self.calibration_fpath}")
            if calibrate:
                ans = input(
                    "Press ENTER to restore calibration, or type 'c' to re-calibrate: "
                ).strip().lower()
                if ans != "c":
                    self._restore_calibration()
                else:
                    self.calibrate()
            else:
                # calibrate=False: silently restore, no prompt
                self._restore_calibration()
        elif calibrate:
            self.calibrate()

        # ── Lift homing / zero restoration ─────────────────────────────
        self.lift_axis.attach()
        self.lift_axis.configure()
        # 优先从持久化文件恢复绝对位置 (免归零); 恢复失败才降到底部归零.
        # home_lift_on_connect=False 时完全跳过 (需自行保证位置正确).
        if not getattr(self, "_lift_homed", False):
            if self.config.home_lift_on_connect and not self.lift_axis.restore_zero():
                logger.info("Running lift homing (stall-detection) ...")
                self.lift_axis.home()
                # 数据采集场景: 归零后升降在底部, 允许操作者手动升到期望高度,
                # 按 ENTER 确认后才继续 (保证第 0 条数据从期望高度开始).
                if self.config.confirm_lift_after_home:
                    self._confirm_lift_height_with_keyboard()
            self._lift_homed = True

        # ── Cameras ─────────────────────────────────────────────────────
        for cam in self.cameras.values():
            cam.connect()

        self.configure()
        logger.info(f"{self} connected.")
        # 注册到全局表, 供 HumanaOpenTeleop 读取头部/升降初始位置 (record 场景)
        try:
            from .leader import register_robot
            register_robot(self)
        except Exception:
            pass

    def _confirm_lift_height_with_keyboard(self) -> None:
        """归零后手动升降确认: 后台线程轮询 u/h 驱动升降, 直到回车.

        input() 是阻塞的, 期间没有任何代码调用 get_action/send_action,
        升降不会动. 此方法在 input() 期间用后台线程轮询全局键盘回调,
        按住 u/h 直接写 Goal_Velocity 驱动升降, 回车后停止.
        """
        import threading

        from .leader import register_keyboard_callback

        stop = threading.Event()
        lift = self.lift_axis
        name = lift.cfg.name
        vel = 0.0
        lock = threading.Lock()
        lift_speed = 60  # raw velocity (BIT2=0: 60*50=3000 step/s ≈ 5.9mm/s)

        def on_key(ch: str, is_pressed: bool) -> None:
            nonlocal vel
            if ch in ("u", "h"):
                with lock:
                    vel = (lift_speed if ch == "u" else -lift_speed) if is_pressed else 0.0

        def drive():
            while not stop.is_set():
                with lock:
                    v = vel
                # 走 apply_action → _apply_safety_limits (soft_max 200mm /
                # descent_floor 3mm 限位生效); v=0 时写 0 停止电机
                try:
                    lift.apply_action({f"{name}.vel": v})
                except Exception:
                    pass
                time.sleep(0.05)

        register_keyboard_callback(on_key)
        thread = threading.Thread(target=drive, daemon=True)
        thread.start()
        try:
            input(
                "Lift homed to bottom (0mm). Hold u/h to raise/lower the lift to the desired "
                "height, then press ENTER to start recording..."
            )
        finally:
            stop.set()
            thread.join(timeout=0.5)
            try:
                lift._bus.write("Goal_Velocity", name, 0)
            except Exception:
                pass
            # 保存用户手动调整后的位置, 下次连接免归零
            lift.save_zero()

    def _restore_calibration(self) -> None:
        """Load saved calibration data into bus memory and write to motors."""
        for bus_key in ["bus1", "bus2", "bus3"]:
            bus = getattr(self, bus_key, None)
            if bus is None:
                continue
            motor_names = list(bus.motors.keys())
            bus_cal = {k: v for k, v in self.calibration.items() if k in motor_names}
            if bus_cal:
                bus.calibration = bus_cal
                try:
                    bus.write_calibration(bus_cal)
                except Exception as e:
                    logger.warning(f"Failed to write cal to {bus_key}: {e}")

    # ── Calibration ────────────────────────────────────────────────────────

    def calibrate(self) -> None:
        """Interactive calibration: half-turn homing + range recording.

        * Arm/head motors: zero at natural hanging pose + gripper closed →
          record ranges (gripper gets a dedicated closed/open two-point calibration).
        * Wheel motors: full 0-4095 range (continuous rotation).
        * Lift motor: uses stall-detection homing (run separately).

        Zero convention: arms hanging straight down, gripper closed — matching
        the leader teleoperator so teleoperation maps pose-to-pose.
        """
        logger.info("Running calibration of %s", self)
        self.bus1.disable_torque()
        self.bus2.disable_torque()
        if self.bus3 is not None:
            self.bus3.disable_torque()

        # Set all position-mode motors to POSITION operating mode
        for name in self.left_arm_motors + self.head_motors:
            self.bus1.write("Operating_Mode", name, OperatingMode.POSITION.value)
        for name in self.right_arm_motors:
            self.bus2.write("Operating_Mode", name, OperatingMode.POSITION.value)

        # ── Bus 1: left arm + head ──────────────────────────────────────
        input(
            "Move LEFT ARM and HEAD motors to zero pose (arms hanging straight down, "
            "gripper closed), then press ENTER..."
        )
        homing1 = self.bus1.set_half_turn_homings(self.left_arm_motors + self.head_motors)
        print("Move all left arm + head joints through full range.\nPress ENTER when done...")
        rmin1, rmax1 = self.bus1.record_ranges_of_motion(
            self.left_arm_motors + self.head_motors
        )
        cal1 = {}
        for name in self.left_arm_motors + self.head_motors:
            if name.endswith("gripper"):
                cal1[name] = self._calibrate_gripper(self.bus1, name, homing1)
            else:
                cal1[name] = MotorCalibration(
                    id=self.bus1.motors[name].id,
                    drive_mode=0,
                    homing_offset=homing1.get(name, 0),
                    range_min=rmin1.get(name, 0),
                    range_max=rmax1.get(name, 4095),
                )
        self.bus1.write_calibration(cal1)

        # ── Bus 2: right arm ────────────────────────────────────────────
        input(
            "Move RIGHT ARM motors to zero pose (arms hanging straight down, "
            "gripper closed), then press ENTER..."
        )
        homing2 = self.bus2.set_half_turn_homings(self.right_arm_motors)
        print("Move all right arm joints through full range.\nPress ENTER when done...")
        rmin2, rmax2 = self.bus2.record_ranges_of_motion(self.right_arm_motors)
        cal2 = {}
        for name in self.right_arm_motors:
            if name.endswith("gripper"):
                cal2[name] = self._calibrate_gripper(self.bus2, name, homing2)
            else:
                cal2[name] = MotorCalibration(
                    id=self.bus2.motors[name].id,
                    drive_mode=0,
                    homing_offset=homing2.get(name, 0),
                    range_min=rmin2.get(name, 0),
                    range_max=rmax2.get(name, 4095),
                )

        # Wheels & lift on same bus (2-bus mode)
        if self.config.port3 is None:
            wheel_bus = self.bus2
            for name in self.wheel_motors:
                cal2[name] = MotorCalibration(
                    id=wheel_bus.motors[name].id,
                    drive_mode=0,
                    homing_offset=0,
                    range_min=0,
                    range_max=4095,
                )
        self.bus2.write_calibration(cal2)

        # ── Bus 3: wheels (3-bus mode) ──────────────────────────────────
        if self.bus3 is not None:
            cal3 = {}
            for name in self.wheel_motors:
                cal3[name] = MotorCalibration(
                    id=self.bus3.motors[name].id,
                    drive_mode=0,
                    homing_offset=0,
                    range_min=0,
                    range_max=4095,
                )
            self.bus3.write_calibration(cal3)

        # ── Merge & save ────────────────────────────────────────────────
        self.calibration = {}
        self.calibration.update(cal1)
        self.calibration.update(cal2)
        if self.bus3 is not None:
            self.calibration.update(cal3)
        self._save_calibration()
        print("Calibration saved to", self.calibration_fpath)

    # ── Configure ──────────────────────────────────────────────────────────

    def _calibrate_gripper(
        self, bus, name: str, homing_offsets: dict
    ) -> MotorCalibration:
        """Two-point gripper calibration: closed → 0, open → 100 (RANGE_0_100).

        Mirrors the leader's gripper convention so teleoperation maps open/close
        pose-to-pose.
        """
        input(f"\nGripper '{name}' calibration\nStep 1: CLOSE the gripper fully\nPress ENTER when closed...")
        # 等待舵机停稳再读数 (防运动中被读成中间值)
        closed_pos = self._read_stable(bus, "Present_Position", name)
        input("Step 2: OPEN the gripper fully\nPress ENTER when fully open...")
        open_pos = self._read_stable(bus, "Present_Position", name)

        if closed_pos < open_pos:
            range_min, range_max, drive_mode = int(closed_pos), int(open_pos), 0
        else:
            range_min, range_max, drive_mode = int(open_pos), int(closed_pos), 1
        logger.info(
            f"  {name}: closed={closed_pos} open={open_pos} → range "
            f"[{range_min}, {range_max}] (0=closed, 100=open, drive_mode={drive_mode})"
        )
        return MotorCalibration(
            id=bus.motors[name].id,
            drive_mode=drive_mode,
            homing_offset=homing_offsets.get(name, 0),
            range_min=range_min,
            range_max=range_max,
        )

    @staticmethod
    def _read_stable(bus, item: str, name: str, num_tries: int = 8, tolerance: float = 1.0) -> float:
        """Read a register until two consecutive readings agree (within tolerance)."""
        prev = None
        for _ in range(num_tries):
            val = bus.read(item, name, normalize=False)
            if prev is not None and abs(val - prev) <= tolerance:
                return val
            prev = val
            time.sleep(0.15)
        return prev

    def configure(self) -> None:
        """Set operating modes and PID gains after connection/calibration."""
        self.bus1.disable_torque()
        self.bus2.disable_torque()
        if self.bus3 is not None:
            self.bus3.disable_torque()

        def _config_arm(bus, names):
            for n in names:
                bus.write("Operating_Mode", n, OperatingMode.POSITION.value)
                bus.write("P_Coefficient", n, 16)
                bus.write("I_Coefficient", n, 0)
                bus.write("D_Coefficient", n, 43)

        def _config_wheels(bus, names):
            for n in names:
                bus.write("Operating_Mode", n, OperatingMode.VELOCITY.value)

        _config_arm(self.bus1, self.left_arm_motors + self.head_motors)
        _config_arm(self.bus2, self.right_arm_motors)

        if self.config.port3 is None:
            # 2-bus: wheels live on bus 2
            _config_wheels(self.bus2, self.wheel_motors)
        elif self.bus3 is not None:
            _config_wheels(self.bus3, self.wheel_motors)

        self.bus1.enable_torque()
        self.bus2.enable_torque()
        if self.bus3 is not None:
            self.bus3.enable_torque()

        # Lift is configured by LiftAxis.configure()
        self.lift_axis.configure()

    # ── Setup motors (initial ID assignment) ───────────────────────────────

    def setup_motors(self) -> None:
        """Assign motor IDs one-at-a-time (run once during assembly)."""
        bus1_motor_names = self.left_arm_motors + self.head_motors
        bus2_motor_names = self.right_arm_motors[:]
        if self.config.port3 is None:
            bus2_motor_names += self.wheel_motors

        for name in reversed(bus1_motor_names):
            input(f"Plug only the '{name}' motor into bus 1, then press ENTER...")
            self.bus1.setup_motor(name)
            print(f"  → {name} set to ID {self.bus1.motors[name].id}")

        for name in reversed(bus2_motor_names):
            input(f"Plug only the '{name}' motor into bus 2, then press ENTER...")
            self.bus2.setup_motor(name)
            print(f"  → {name} set to ID {self.bus2.motors[name].id}")

        if self.bus3 is not None and self.config.port3:
            for name in reversed(self.wheel_motors):
                input(f"Plug only the '{name}' motor into bus 3, then press ENTER...")
                self.bus3.setup_motor(name)
                print(f"  → {name} set to ID {self.bus3.motors[name].id}")

    # ── Differential drive kinematics ──────────────────────────────────────

    @staticmethod
    def _degps_to_raw(degps: float) -> int:
        steps_per_deg = 4096.0 / 360.0
        v = int(round(degps * steps_per_deg))
        return max(-0x7FFF, min(0x7FFF, v))

    @staticmethod
    def _raw_to_degps(raw: int) -> float:
        return raw / (4096.0 / 360.0)

    def _body_to_wheel_raw(self, x: float, theta: float) -> dict[str, int]:
        """Body-frame velocity → wheel raw commands (differential drive)."""
        r = self.config.wheel_radius
        L = self.config.wheelbase
        max_raw = self.config.max_wheel_raw

        theta_rad = np.deg2rad(theta)
        left = (x - theta_rad * L / 2) / r
        right = (x + theta_rad * L / 2) / r

        left_degps = np.rad2deg(left)
        right_degps = np.rad2deg(right)

        # Scale down if exceeds max_raw
        steps_per_deg = 4096.0 / 360.0
        raw_vals = [abs(d) * steps_per_deg for d in (left_degps, right_degps)]
        peak = max(raw_vals)
        if peak > max_raw:
            scale = max_raw / peak
            left_degps *= scale
            right_degps *= scale

        return {
            "base_left_wheel": self.config.wheel_dir_signs["base_left_wheel"] * self._degps_to_raw(left_degps),
            "base_right_wheel": self.config.wheel_dir_signs["base_right_wheel"] * self._degps_to_raw(right_degps),
        }

    def _wheel_raw_to_body(self, left_raw: int, right_raw: int) -> dict[str, float]:
        """Wheel raw feedback → body-frame velocity."""
        r = self.config.wheel_radius
        L = self.config.wheelbase

        # Undo the direction signs applied in _body_to_wheel_raw so the
        # body-frame estimate stays consistent with commanded motion.
        left_raw = self.config.wheel_dir_signs["base_left_wheel"] * left_raw
        right_raw = self.config.wheel_dir_signs["base_right_wheel"] * right_raw

        left_radps = np.deg2rad(self._raw_to_degps(left_raw))
        right_radps = np.deg2rad(self._raw_to_degps(right_raw))

        left_lin = left_radps * r
        right_lin = right_radps * r

        x_vel = (left_lin + right_lin) / 2
        theta_vel = np.rad2deg((right_lin - left_lin) / L)
        return {"x.vel": x_vel, "theta.vel": theta_vel}

    # ── Observation ────────────────────────────────────────────────────────

    def get_observation(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        obs: dict[str, Any] = {}
        t0 = time.perf_counter()

        # Read arm & head positions
        left_pos = self.bus1.sync_read("Present_Position", self.left_arm_motors)
        head_pos = self.bus1.sync_read("Present_Position", self.head_motors)
        right_pos = self.bus2.sync_read("Present_Position", self.right_arm_motors)

        for k, v in left_pos.items():
            obs[f"{k}.pos"] = v
        for k, v in head_pos.items():
            obs[f"{k}.pos"] = v
        for k, v in right_pos.items():
            obs[f"{k}.pos"] = v

        # Read wheel velocities
        if self.wheel_motors:
            wheel_bus = self.bus3 if self.bus3 is not None else self.bus2
            wheel_vel = wheel_bus.sync_read("Present_Velocity", self.wheel_motors)
            body = self._wheel_raw_to_body(
                wheel_vel.get("base_left_wheel", 0),
                wheel_vel.get("base_right_wheel", 0),
            )
            obs["x.vel"] = body["x.vel"]
            obs["theta.vel"] = body["theta.vel"]

        # Lift
        self.lift_axis.contribute_observation(obs)

        # Cameras
        for cam_key, cam in self.cameras.items():
            obs[cam_key] = cam.async_read()

        dt_ms = (time.perf_counter() - t0) * 1e3
        logger.debug("get_observation: %.1f ms", dt_ms)
        return obs

    # ── Action ─────────────────────────────────────────────────────────────

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        # Split action by domain
        left_pos = {k: v for k, v in action.items() if k.startswith("left_arm_") and k.endswith(".pos")}
        right_pos = {k: v for k, v in action.items() if k.startswith("right_arm_") and k.endswith(".pos")}
        head_pos = {k: v for k, v in action.items() if k.startswith("head_") and k.endswith(".pos")}
        base_cmd = {k: v for k, v in action.items() if k in ("x.vel", "theta.vel")}
        # lift handled by lift_axis.apply_action

        # ── Safety clamp ────────────────────────────────────────────────
        if self.config.max_relative_target is not None:
            present = {}
            present.update(self.bus1.sync_read("Present_Position", self.left_arm_motors + self.head_motors))
            present.update(self.bus2.sync_read("Present_Position", self.right_arm_motors))
            all_goals = {}
            for d in (left_pos, right_pos, head_pos):
                all_goals.update(d)
            goal_present = {k: (v, present.get(k.replace(".pos", ""), 0)) for k, v in all_goals.items()}
            safe = ensure_safe_goal_position(goal_present, self.config.max_relative_target)
            left_pos = {k: v for k, v in safe.items() if k in left_pos}
            right_pos = {k: v for k, v in safe.items() if k in right_pos}
            head_pos = {k: v for k, v in safe.items() if k in head_pos}

        # ── Write arm positions ─────────────────────────────────────────
        if left_pos:
            self.bus1.sync_write("Goal_Position", {k.replace(".pos", ""): v for k, v in left_pos.items()})
        if right_pos:
            self.bus2.sync_write("Goal_Position", {k.replace(".pos", ""): v for k, v in right_pos.items()})
        if head_pos:
            self.bus1.sync_write("Goal_Position", {k.replace(".pos", ""): v for k, v in head_pos.items()})

        # ── Wheel velocity commands ─────────────────────────────────────
        if base_cmd and self.wheel_motors:
            wheel_raw = self._body_to_wheel_raw(base_cmd.get("x.vel", 0.0), base_cmd.get("theta.vel", 0.0))
            wheel_bus = self.bus3 if self.bus3 is not None else self.bus2
            wheel_bus.sync_write("Goal_Velocity", wheel_raw)

        # ── Lift command ────────────────────────────────────────────────
        self.lift_axis.apply_action(action)

        return action

    # ── Shutdown ───────────────────────────────────────────────────────────

    def stop_base(self) -> None:
        if self.wheel_motors:
            wheel_bus = self.bus3 if self.bus3 is not None else self.bus2
            wheel_bus.sync_write("Goal_Velocity", dict.fromkeys(self.wheel_motors, 0), num_retry=5)
        # Stop lift too (only if its motor was actually attached to a bus)
        lift_bus = getattr(self.lift_axis, "_bus", None)
        if lift_bus is not None and self.lift_axis.cfg.name in lift_bus.motors:
            self.lift_axis.apply_action({"lift_axis.vel": 0})
        logger.info("Base & lift motors stopped")

    def disconnect(self) -> None:
        # Tolerate partial connection state (e.g. connect() failed midway).
        # Each bus/camera knows whether it is connected and disconnects accordingly.
        if self.is_connected:
            self.stop_base()
        for bus in (self.bus1, self.bus2, self.bus3):
            if bus is not None and bus.is_connected:
                bus.disconnect(self.config.disable_torque_on_disconnect)
        for cam in self.cameras.values():
            if cam.is_connected:
                cam.disconnect()
        logger.info("%s disconnected.", self)
