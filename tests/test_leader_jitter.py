"""Verify leader adaptive-EMA + deadband jitter suppression WITHOUT hardware.

Simulates a FeetechMotorsBus whose Present_Position reads are fed from a
scripted sequence (stationary noise, fast motion step, slow ramp). Checks:

1. Stationary: encoder self-noise (±0.1 units) must NOT move the output at all.
2. Fast step: output must reach within tolerance of the target quickly.
3. No drift: deadband holds the last emitted value; when a real move exceeds
   the band the EMA tracks it (output eventually equals the input plateau).
"""

import sys
import types

# --- Stub out the 'pynput' and 'lerobot' imports so the module loads standalone.
sys.modules.setdefault("pynput", types.ModuleType("pynput"))

lerobot = types.ModuleType("lerobot")
lerobot_motors = types.ModuleType("lerobot.motors")


class _NormMode:
    DEGREES = "deg"
    RANGE_M100_100 = "m100"
    RANGE_0_100 = "0_100"


class _Motor:
    def __init__(self, motor_id, model, norm_mode):
        self.id = motor_id
        self.model = model
        self.norm_mode = norm_mode


class _OperatingMode:
    POSITION = 0


class _MotorCalibration:
    pass


from dataclasses import dataclass, field

@dataclass(kw_only=True)
class _TeleoperatorConfig:
    id: str | None = None
    calibration_dir: str | None = None
    _registry = {}

    @classmethod
    def register_subclass(cls, name):
        def deco(sub):
            cls._registry[name] = sub
            return sub
        return deco


class _Teleoperator:
    config_class = None

    def __init__(self, config=None):
        self.id = getattr(config, "id", "test") if config else "test"
        self.calibration = {}
        self._param_suffix = ""


lerobot_motors.Motor = _Motor
lerobot_motors.MotorCalibration = _MotorCalibration
lerobot_motors.MotorNormMode = _NormMode
lerobot_motors.feetech = types.ModuleType("lerobot.motors.feetech")
lerobot_motors.feetech.OperatingMode = _OperatingMode


class _FakeFeetechBus:
    def __init__(self, *args, **kwargs):
        pass

    motors = {}


lerobot_motors.feetech.FeetechMotorsBus = _FakeFeetechBus
lerobot_motors.feetech.Motor = _Motor
lerobot_motors.feetech.MotorCalibration = _MotorCalibration
lerobot_motors.feetech.MotorNormMode = _NormMode
lerobot.robots = types.ModuleType("lerobot.robots")
lerobot.robots.robot = types.ModuleType("lerobot.robots.robot")
lerobot.robots.robot.Robot = object
lerobot.teleoperators = types.ModuleType("lerobot.teleoperators")
lerobot.teleoperators.config = types.ModuleType("lerobot.teleoperators.config")
lerobot.teleoperators.config.TeleoperatorConfig = _TeleoperatorConfig
lerobot.teleoperators.teleoperator = types.ModuleType("lerobot.teleoperators.teleoperator")
lerobot.teleoperators.teleoperator.Teleoperator = _Teleoperator
lerobot.cameras = types.ModuleType("lerobot.cameras")
lerobot.cameras.utils = types.ModuleType("lerobot.cameras.utils")


def _make_cameras_from_configs(cfgs):
    return {}


lerobot.cameras.utils.make_cameras_from_configs = _make_cameras_from_configs
sys.modules["lerobot"] = lerobot
sys.modules["lerobot.motors"] = lerobot_motors
sys.modules["lerobot.motors.feetech"] = lerobot_motors.feetech
sys.modules["lerobot.robots"] = lerobot.robots
sys.modules["lerobot.robots.robot"] = lerobot.robots.robot
sys.modules["lerobot.teleoperators"] = lerobot.teleoperators
sys.modules["lerobot.teleoperators.config"] = lerobot.teleoperators.config
sys.modules["lerobot.teleoperators.teleoperator"] = lerobot.teleoperators.teleoperator
sys.modules["lerobot.cameras"] = lerobot.cameras
sys.modules["lerobot.cameras.utils"] = lerobot.cameras.utils

# Stub the package __init__ so importing .leader does not cascade into
# humanaopen.py (which imports the real lerobot FeetechMotorsBus).
_lrh = types.ModuleType("lerobot_robot_humanaopen")
_lrh.__path__ = [__import__("os").path.dirname(__import__("os").path.dirname(__file__)) + "/lerobot_robot_humanaopen"]
_lrh.HumanaOpen = object
_lrh.HumanaOpenConfig = object
_lrh.humanaopen = types.ModuleType("lerobot_robot_humanaopen.humanaopen")
_lrh.humanaopen.HumanaOpen = object
_lrh.config_humanaopen = types.ModuleType("lerobot_robot_humanaopen.config_humanaopen")
_lrh.config_humanaopen.HumanaOpenConfig = object
_lrh.lift_axis = types.ModuleType("lerobot_robot_humanaopen.lift_axis")
_lrh.lift_axis.HumanaOpenLiftAxis = object
_lrh.lift_axis.LiftAxisConfig = object
sys.modules["lerobot_robot_humanaopen"] = _lrh
sys.modules["lerobot_robot_humanaopen.humanaopen"] = _lrh.humanaopen
sys.modules["lerobot_robot_humanaopen.config_humanaopen"] = _lrh.config_humanaopen
sys.modules["lerobot_robot_humanaopen.lift_axis"] = _lrh.lift_axis

import random
import math

from lerobot_robot_humanaopen.leader import (
    HumanaOpenLeader,
    HumanaOpenLeaderConfig,
    DEFAULT_SIDE_MOTORS_TO_FLIP,
    DEFAULT_JOINT_REMAP,
)


class FakeBus:
    """Returns a scripted sequence of Present_Position dicts, one per get_action()."""

    def __init__(self, sequence):
        self._seq = list(sequence)
        self._i = 0
        self.motors = {
            name: _Motor(i + 1, "sts3215", _NormMode.RANGE_M100_100)
            for i, name in enumerate(
                ["shoulder_pan", "shoulder_lift", "shoulder_roll", "elbow_flex",
                 "forearm_rotation", "wrist_flex", "wrist_yaw", "gripper"]
            )
        }

    def sync_read(self, item):
        return self._seq[min(self._i, len(self._seq) - 1)]

    def step(self):
        self._i += 1


def make_leader(seq, **cfg_overrides):
    cfg = HumanaOpenLeaderConfig(
        id="test_leader",
        port="/dev/ttyNULL",
        side="left",
        flip_joints={"left": [], "right": []},
        joint_remap={},
        **cfg_overrides,
    )
    leader = HumanaOpenLeader(cfg)
    leader.bus = FakeBus(seq)
    return leader


def stationary_noise_test():
    rng = random.Random(42)
    base = 10.0
    frames = 2000
    seq = []
    for _ in range(frames):
        vals = {}
        for name in ["shoulder_pan", "shoulder_lift", "shoulder_roll"]:
            vals[name] = base + rng.uniform(-0.1, 0.1)  # ±0.1 normalized self-noise
        vals["gripper"] = 3.0 + rng.uniform(-0.1, 0.1)
        seq.append(vals)

    leader = make_leader(seq)
    outputs = []
    for _ in range(frames):
        a = leader.get_action()
        leader.bus.step()
        outputs.append(dict(a))

    # Output must be essentially frozen at the initial value.
    emitted = [a["shoulder_pan.pos"] for a in outputs]
    spread = max(emitted) - min(emitted)
    distinct = len(set(round(v, 4) for v in emitted))
    assert spread < 1e-9, f"stationary output moved {spread:.4f} units"
    assert distinct == 1, f"output not frozen: {distinct} distinct values"
    # And the first emitted value should be near the mean (not the first noise spike).
    first = emitted[0]
    assert 9.9 <= first <= 10.1, f"output anchored away from signal: {first}"


def fast_step_test():
    # 10 frames at 0, then a step to 50 (both noise-free).
    seq = []
    for _ in range(10):
        seq.append({n: 0.0 for n in ["shoulder_pan", "shoulder_lift", "shoulder_roll"]})
    for _ in range(60):
        seq.append({n: 50.0 for n in ["shoulder_pan", "shoulder_lift", "shoulder_roll"]})
    for v in seq:
        v["gripper"] = 3.0

    leader = make_leader(seq)
    emitted = []
    for _ in range(len(seq)):
        a = leader.get_action()
        leader.bus.step()
        emitted.append(a["shoulder_pan.pos"])

    # With deadband, output must jump toward 50 within a few frames.
    # Alpha max = smoothing (0.35) gives geometric convergence: reaching 98%
    # of a full-scale step takes ~19 frames at 60Hz (~0.3s). That is
    # unchanged from the pre-deadband behavior, so motion latency is not
    # degraded. Assert a comfortable upper bound on the same convergence.
    settle = next(i for i, v in enumerate(emitted) if v >= 49.0)
    assert settle <= 25, f"step not tracked quickly enough (settled at frame {settle})"
    final = emitted[-1]
    assert abs(final - 50.0) < 0.5, f"output did not reach target plateau: {final}"


def slow_ramp_no_drift_test():
    seq = []
    for i in range(500):
        v = {}
        # Slow drift 0->20 over 500 frames (~0.04 units/frame — under the 0.1 band).
        for n in ["shoulder_pan", "shoulder_lift", "shoulder_roll"]:
            v[n] = 20.0 * i / 500.0
        v["gripper"] = 3.0
        seq.append(v)

    leader = make_leader(seq)
    emitted = []
    for _ in range(len(seq)):
        a = leader.get_action()
        leader.bus.step()
        emitted.append(a["shoulder_pan.pos"])

    # Even a too-slow ramp must STILL reach the input value at the end: the
    # deadband holds the value but the EMA keeps integrating, so once the gap
    # exceeds the band the output steps to the current EMA value.
    final = emitted[-1]
    assert abs(final - 20.0) < 2.0, f"slow ramp drifted: final {final:.3f} (target 20.0)"
    # And there must be a strictly increasing trend overall, not oscillation.
    deltas = [b - a for a, b in zip(emitted, emitted[1:])]
    assert all(d >= -1e-9 for d in deltas), "output oscillated backwards at some point"


if __name__ == "__main__":
    stationary_noise_test()
    print("PASS stationary_noise_test")
    fast_step_test()
    print("PASS fast_step_test")
    slow_ramp_no_drift_test()
    print("PASS slow_ramp_no_drift_test")
    print("\nAll leader jitter-suppression tests passed.")