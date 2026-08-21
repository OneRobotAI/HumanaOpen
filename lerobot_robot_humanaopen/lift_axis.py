"""Lift axis module for HumanaOpen — linear leadscrew with stall-detection homing."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Protocol


class BusLike(Protocol):
    """Minimal bus interface that lift_axis depends on."""

    motors: dict[str, object]

    def read(self, item: str, name: str, **kwargs) -> float: ...
    def write(self, item: str, name: str, value: float) -> None: ...
    def sync_write(self, item: str, values: dict[str, float]) -> None: ...


@dataclass
class LiftAxisConfig:
    """Configuration for the leadscrew-driven lift axis.

    Parameters
    ----------
    enabled :
        Set ``False`` to disable the lift entirely.
    name :
        Motor name used as key in the motors dict.
    motor_id :
        Servo ID on the bus (1-253).
    motor_model :
        Servo model string passed to ``Motor()``.
    lead_mm_per_rev :
        Leadscrew travel in mm per full revolution of the **output** shaft.
    belt_ratio :
        Leadscrew revolutions per motor revolution.
        - ``1`` = direct drive (no belt).
        - ``2`` = leadscrew turns 2× per motor revolution (speed increase, torque reduction).
        - ``0.5`` = leadscrew turns 0.5× per motor revolution (speed reduction, torque increase).
        
        Example: ST3215 C018 (1:345, ~20 rpm at output) with a 1:3 speed-up pulley
        (belt_ratio=3) gives ~60 rpm at leadscrew → 8 mm × 60 rpm = 480 mm/min.  
    soft_min_mm :
        Software lower limit (mm).  Motion below this is blocked.
    soft_max_mm :
        Software upper limit (mm).  Motion above this is blocked.
    descent_floor_mm :
        Hard guard — refuse downward commands when height ≤ this value.
    home_down_speed :
        Velocity command sent while homing downward (raw velocity units).
    home_stall_current_ma :
        Stall current threshold in mA.  Homing stops when exceeded.
    home_backoff_deg :
        After stall, back off this many degrees upward to relieve gear stress.
    kp_vel :
        Proportional gain that maps height error (mm) → velocity command.
        ``v_cmd = kp_vel * error_mm``.
    v_max :
        Maximum absolute velocity command (raw units).
    on_target_mm :
        Deadband — considered "at target" when error ≤ this value (mm).
    dir_sign :
        ``+1`` = positive velocity raises the lift; ``-1`` = inverted.
    """

    enabled: bool = True
    name: str = "lift_axis"
    motor_id: int = 9
    motor_model: str = "sts3250"

    # Mechanical
    lead_mm_per_rev: float = 8.0
    belt_ratio: float = 1.0  # leadscrew_rev / motor_rev.  1 = direct drive (no belt)
    soft_min_mm: float = 0.0
    soft_max_mm: float = 200.0  # 200mm mechanical upper limit (user-specified)
    descent_floor_mm: float = 3.0

    # Homing
    # BIT2=0 (Phase=8): 单位 = 50 step/s per raw unit.
    #   home_down_speed 10  = 500 step/s  (与旧 BIT2=1 的 500 等价, 安全低速)
    home_down_speed: int = 10
    home_stall_current_ma: int = 200
    home_backoff_deg: float = 5.0

    # Velocity-loop P controller
    # BIT2=0: kp_vel 10 = 旧 500 等价 (10×50=500 step/s per mm error)
    kp_vel: float = 10.0
    v_max: int = 110  # BIT2=0 物理上限 110 raw = 5500 step/s = 10.7 mm/s
    on_target_mm: float = 1.0

    dir_sign: int = 1

    # 持久化零位: home() 后把绝对位置存到该文件, 下次连接免归零恢复.
    # 丝杠自锁, 断电后机械位置不变 → 编码器读数可复现, 恢复绝对位置即可.
    # None = 禁用持久化 (每次连接都重新归零).
    zero_file: str | None = None

    def __post_init__(self):
        if self.soft_max_mm > 1000:
            raise ValueError(f"soft_max_mm={self.soft_max_mm} seems excessive; check units (mm).")


class HumanaOpenLiftAxis:
    """Linear lift axis driven by a Feetech servo + leadscrew + timing belt.

    Key features
    -----------
    *   **Stall-detection homing** — drives downward until the motor stalls
        (detected via ``Present_Current`` or position freeze), then sets zero.
    *   **Multi-turn tracking** — unwraps the 0-4095 encoder so the axis
        can measure absolute height across many revolutions.
    *   **P-controller** — maps a height setpoint (mm) to a velocity command
        written to ``Goal_Velocity``.
    """

    def __init__(self, cfg: LiftAxisConfig, bus: BusLike | None):
        self.cfg = cfg
        self._bus = bus
        self.enabled = bool(cfg.enabled and bus is not None)

        # derived constants
        self._ticks_per_rev = 4096.0
        self._deg_per_tick = 360.0 / self._ticks_per_rev
        # mm per motor-degree = (lead / 360°) × belt_ratio
        # belt_ratio=2 means the leadscrew moves half the angle the motor turns
        self._mm_per_deg = (cfg.lead_mm_per_rev * cfg.belt_ratio) / 360.0

        # multi-turn state
        self._last_tick: float = 0.0
        self._extended_ticks: float = 0.0
        self._z0_deg: float = 0.0
        self._configured = False
        # 上次 home 时的绝对位置 (供持久化恢复)
        self._abs_tick_at_home: float | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def attach(self) -> None:
        """Register the motor with the bus if not already present."""
        if not self.enabled:
            return
        from lerobot.motors import Motor, MotorNormMode

        if self.cfg.name not in self._bus.motors:
            self._bus.motors[self.cfg.name] = Motor(
                self.cfg.motor_id, self.cfg.motor_model, MotorNormMode.DEGREES
            )
            # Refresh MotorsBus internal caches (motors were injected after bus creation)
            bus = self._bus
            if hasattr(bus, "_id_to_model_dict"):
                bus._id_to_model_dict = {m.id: m.model for m in bus.motors.values()}
                bus._id_to_name_dict = {m.id: n for n, m in bus.motors.items()}
                bus._model_nb_to_model_dict = {v: k for k, v in bus.model_number_table.items()}

    def configure(self) -> None:
        """Set operating mode to VELOCITY and reset multi-turn tracking."""
        if not self.enabled or self._configured:
            return
        from lerobot.motors.feetech import OperatingMode

        self._bus.write("Operating_Mode", self.cfg.name, OperatingMode.VELOCITY.value)
        self._last_tick = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        self._extended_ticks = 0.0
        self._configured = True

    # ------------------------------------------------------------------
    # Zero persistence (免归零恢复绝对位置)
    # ------------------------------------------------------------------

    def save_zero(self) -> None:
        """把当前多圈跟踪状态持久化到文件 (供下次连接恢复)."""
        if not self.enabled or not self.cfg.zero_file:
            return
        import json
        import os

        try:
            os.makedirs(os.path.dirname(self.cfg.zero_file), exist_ok=True)
            state = {
                "extended_ticks": self._extended_ticks,
                "last_tick": self._last_tick,
                "abs_tick_at_home": self._abs_tick_at_home,
            }
            with open(self.cfg.zero_file, "w") as f:
                json.dump(state, f)
        except Exception:
            pass

    def restore_zero(self) -> bool:
        """尝试从文件恢复绝对位置, 免归零.

        前提: 丝杠自锁, 断电后机械位置不变 → 编码器读数可复现.
        若当前编码器读数与文件记录的 last_tick 一致 (±容差), 则恢复
        多圈跟踪状态并返回 True; 否则返回 False (调用方应重新归零).
        """
        if not self.enabled or not self.cfg.zero_file:
            return False
        import json
        import os

        if not os.path.isfile(self.cfg.zero_file):
            return False
        try:
            with open(self.cfg.zero_file) as f:
                state = json.load(f)
        except Exception:
            return False

        try:
            cur = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        except Exception:
            return False

        last = float(state.get("last_tick", -1))
        tol = 30  # ±30 ticks ≈ ±0.06mm, 容纳断电重启后编码器微小漂移
        if abs(cur - last) > tol:
            return False

        self._extended_ticks = float(state.get("extended_ticks", 0.0))
        self._last_tick = cur
        self._abs_tick_at_home = state.get("abs_tick_at_home")
        return True

    # ------------------------------------------------------------------
    # Multi-turn tracking
    # ------------------------------------------------------------------

    def _update_extended_ticks(self) -> None:
        if not self.enabled:
            return
        cur = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        delta = cur - self._last_tick
        half = self._ticks_per_rev * 0.5
        # 当采样间隔内位移可能超过半圈时 (跨 0 边界导致 delta 符号反转),
        # 用 Present_Velocity 的符号决定真实环绕方向 (速度方向 = 真实运动方向).
        # 仅模糊区才读, 避免无谓总线开销。
        vel = 0.0
        if abs(delta) > half * 0.75:
            try:
                vel = float(self._bus.read("Present_Velocity", self.cfg.name, normalize=False))
            except Exception:
                vel = 0.0
        if vel > 0:
            if delta < 0:
                delta += self._ticks_per_rev
        elif vel < 0:
            if delta > 0:
                delta -= self._ticks_per_rev
        else:
            for _ in range(8):
                if delta > half:
                    delta -= self._ticks_per_rev
                elif delta < -half:
                    delta += self._ticks_per_rev
                else:
                    break
        self._extended_ticks += delta
        self._last_tick = cur

    def _extended_deg(self) -> float:
        return self.cfg.dir_sign * self._extended_ticks * self._deg_per_tick

    def get_height_mm(self) -> float:
        """Return current lift height in mm (relative to homed zero)."""
        if not self.enabled:
            return 0.0
        self._update_extended_ticks()
        return (self._extended_deg() - self._z0_deg) * self._mm_per_deg

    # ------------------------------------------------------------------
    # Homing
    # ------------------------------------------------------------------

    def home(self) -> None:
        """Drive downward until stall → back off → record zero.

        Stall is detected when either:
        * ``Present_Current`` exceeds ``home_stall_current_ma``, or
        * the encoder position stops changing.
        """
        if not self.enabled:
            return
        self.configure()
        name = self.cfg.name

        # Downward homing = negative velocity (positive = up, negative = down).
        self._bus.write("Goal_Velocity", name, -self.cfg.home_down_speed)

        stuck = 0
        last_tick = int(self._bus.read("Present_Position", name, normalize=False))

        try:
            for _ in range(6000):  # ~300 s at 50 ms (低速归零需要更长超时)
                time.sleep(0.05)
                self._update_extended_ticks()
                now_tick = self._last_tick
                moved = abs(now_tick - last_tick) > 10
                last_tick = now_tick

                stalled = False
                # Prefer current-based detection
                try:
                    raw_cur = int(self._bus.read("Present_Current", name, normalize=False))
                    if raw_cur * 6.5 >= self.cfg.home_stall_current_ma:
                        stalled = True
                except Exception:
                    pass

                if not stalled and not moved:
                    stalled = True

                if stalled:
                    stuck += 1
                else:
                    stuck = 0

                if stuck >= 2:
                    break
        except KeyboardInterrupt:
            # Emergency stop: halt the motor immediately on Ctrl+C.
            self._bus.write("Goal_Velocity", name, 0)
            self._bus.write("Torque_Enable", name, 0)
            raise

        # Release torque
        self._bus.write("Torque_Enable", name, 0)
        time.sleep(0.5)

        # Back off slightly
        if self.cfg.home_backoff_deg > 0:
            from lerobot.motors.feetech import OperatingMode

            self._bus.write("Torque_Enable", name, 1)
            self._bus.write("Operating_Mode", name, OperatingMode.POSITION.value)  # POSITION mode
            current_pos = self._bus.read("Present_Position", name, normalize=False)
            self._bus.write(
                "Goal_Position", name, int(current_pos + self.cfg.home_backoff_deg), normalize=False
            )
            time.sleep(0.3)
            self._bus.write("Torque_Enable", name, 0)

        self._update_extended_ticks()
        self._z0_deg = self._extended_deg()

        # Restore to a controllable state: zero velocity first (avoid runaway on re-enable),
        # then switch back to VELOCITY mode and re-enable torque.
        from lerobot.motors.feetech import OperatingMode

        self._bus.write("Goal_Velocity", name, 0)
        self._bus.write("Operating_Mode", name, OperatingMode.VELOCITY.value)
        self._bus.write("Torque_Enable", name, 1)

        # Re-zero after the motor settles under torque (small positional drift expected).
        # IMPORTANT: reset multi-turn tracking to zero here — the homing run crosses the
        # encoder zero several times, corrupting _extended_ticks (observed at -23404).
        # The homed position IS the new origin, so start tracking fresh from it.
        time.sleep(0.5)
        self._extended_ticks = 0.0
        self._last_tick = float(self._bus.read("Present_Position", name, normalize=False))
        self._z0_deg = 0.0
        self._abs_tick_at_home = self._last_tick
        self.save_zero()

    # ------------------------------------------------------------------
    # Observation / Action helpers
    # ------------------------------------------------------------------

    def contribute_observation(self, obs: dict[str, float]) -> None:
        """Add ``{name}.height_mm`` and ``{name}.vel`` to the observation dict."""
        if not self.enabled:
            return
        obs[f"{self.cfg.name}.height_mm"] = self.get_height_mm()
        try:
            obs[f"{self.cfg.name}.vel"] = float(
                self._bus.read("Present_Velocity", self.cfg.name, normalize=False)
            )
        except Exception:
            pass

    def apply_action(self, action: dict[str, Any]) -> None:
        """Apply either a height setpoint or direct velocity command.

        Recognised keys (in priority order):

        * ``{name}.height_mm`` — target height → P-controller → velocity
        * ``{name}.vel`` — direct velocity command (raw units)
        """
        if not self.enabled:
            return

        name = self.cfg.name
        key_h = f"{name}.height_mm"
        key_v = f"{name}.vel"

        if key_h in action:
            target_mm = float(action[key_h])
            cur_mm = self.get_height_mm()
            err = target_mm - cur_mm

            v_cmd = 0
            if abs(err) > self.cfg.on_target_mm:
                v_cmd = self.cfg.kp_vel * err
                v_cmd = max(-self.cfg.v_max, min(self.cfg.v_max, v_cmd))

            # Safety guards
            v_cmd = self._apply_safety_limits(v_cmd, cur_mm)

            self._bus.write("Goal_Velocity", name, int(v_cmd))

        elif key_v in action:
            v = int(action[key_v])
            v = max(-self.cfg.v_max, min(self.cfg.v_max, v))
            try:
                cur_mm = self.get_height_mm()
                v = int(self._apply_safety_limits(v, cur_mm))
            except Exception:
                pass
            # 正速度 = 上升 (与 P 控制器路径一致; dir_sign 语义见 docstring)
            self._bus.write("Goal_Velocity", name, v)

    def _apply_safety_limits(self, v_cmd: float, cur_mm: float) -> float:
        """Clamp velocity when at soft limits or descent floor."""
        if v_cmd < 0 and cur_mm <= self.cfg.descent_floor_mm:
            return 0.0
        if cur_mm >= self.cfg.soft_max_mm and v_cmd > 0:
            return 0.0
        if cur_mm <= self.cfg.soft_min_mm and v_cmd < 0:
            return 0.0
        return v_cmd
