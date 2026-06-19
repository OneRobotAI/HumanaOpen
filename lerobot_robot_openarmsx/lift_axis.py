"""Lift axis module for OpenArmsX — linear leadscrew with stall-detection homing."""

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
    # ST3250 — uses same register map as STS3215 for basic operations.
    # If using a different model, change this string to match the feetech table entry.
    motor_model: str = "sts3215"

    # Mechanical
    lead_mm_per_rev: float = 8.0
    belt_ratio: float = 3.0  # leadscrew_rev / motor_rev.  3 = 1:3 speed-up pulley
    soft_min_mm: float = 0.0
    soft_max_mm: float = 400.0
    descent_floor_mm: float = 3.0

    # Homing
    home_down_speed: int = 1500
    home_stall_current_ma: int = 200
    home_backoff_deg: float = 5.0

    # Velocity-loop P controller
    kp_vel: float = 300.0
    v_max: int = 1500
    on_target_mm: float = 1.0

    dir_sign: int = 1

    def __post_init__(self):
        if self.soft_max_mm > 1000:
            raise ValueError(f"soft_max_mm={self.soft_max_mm} seems excessive; check units (mm).")


class OpenArmsXLiftAxis:
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
    # Multi-turn tracking
    # ------------------------------------------------------------------

    def _update_extended_ticks(self) -> None:
        if not self.enabled:
            return
        cur = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        delta = cur - self._last_tick
        half = self._ticks_per_rev * 0.5
        if delta > +half:
            delta -= self._ticks_per_rev
        elif delta < -half:
            delta += self._ticks_per_rev
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

        v_down = self.cfg.home_down_speed
        self._bus.write("Goal_Velocity", name, v_down)

        stuck = 0
        last_tick = int(self._bus.read("Present_Position", name, normalize=False))

        for _ in range(600):  # ~30 s at 50 ms
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

        # Release torque
        self._bus.write("Torque_Enable", name, 0)
        time.sleep(0.5)

        # Back off slightly
        if self.cfg.home_backoff_deg > 0:
            self._bus.write("Torque_Enable", name, 1)
            self._bus.write("Operating_Mode", name, 2)  # POSITION mode
            current_pos = self._bus.read("Present_Position", name, normalize=False)
            self._bus.write("Goal_Position", name, current_pos + self.cfg.home_backoff_deg)
            time.sleep(0.3)
            self._bus.write("Torque_Enable", name, 0)

        self._update_extended_ticks()
        self._z0_deg = self._extended_deg()

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
                v = self._apply_safety_limits(v, cur_mm)
            except Exception:
                pass
            self._bus.write("Goal_Velocity", name, v * self.cfg.dir_sign)

    def _apply_safety_limits(self, v_cmd: float, cur_mm: float) -> float:
        """Clamp velocity when at soft limits or descent floor."""
        if v_cmd < 0 and cur_mm <= self.cfg.descent_floor_mm:
            return 0.0
        if cur_mm >= self.cfg.soft_max_mm and v_cmd > 0:
            return 0.0
        if cur_mm <= self.cfg.soft_min_mm and v_cmd < 0:
            return 0.0
        return v_cmd
