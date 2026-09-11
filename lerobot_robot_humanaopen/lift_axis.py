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
    # BIT2=0 (Phase=8): unit = 50 step/s per raw unit.
    #   home_down_speed 10  = 500 step/s  (equivalent to the old BIT2=1 500, safe low speed)
    home_down_speed: int = 10
    home_stall_current_ma: int = 200
    home_backoff_deg: float = 5.0

    # Velocity-loop P controller
    # BIT2=0: kp_vel 10 = equivalent to old 500 (10×50=500 step/s per mm error)
    kp_vel: float = 10.0
    v_max: int = 110  # BIT2=0 physical upper limit 110 raw = 5500 step/s = 10.7 mm/s
    on_target_mm: float = 1.0

    dir_sign: int = 1

    # Persist zero position: after home() the absolute position is stored in this
    # file so the next connection can recover without re-homing.
    # The leadscrew is self-locking, so the mechanical position is unchanged after
    # power-off -> encoder reading is reproducible; restoring the absolute position suffices.
    # None = disable persistence (re-home on every connection).
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
        # absolute position at the last home (for persistence recovery)
        self._abs_tick_at_home: float | None = None
        self._cached_height_mm: float = 0.0

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
        self._mode_is_velocity = True
        # Acceleration (SRAM addr 41) resets to 0 on every power cycle. 0 means
        # a very slow velocity ramp, so a Goal_Velocity command never actually
        # reaches its target speed (measured: raw=110 -> ~1.7mm/s instead of
        # ~10.7mm/s). Match lerobot's configure_motors() default (254 = fastest
        # ramp) so the lift tracks commanded speed.
        self._bus.write("Acceleration", self.cfg.name, 254)
        # Phase BIT2 selects the Goal_Velocity unit: 0 = 50 step/s/raw
        # (0.732 RPM/raw), 1 = 1 step/s/raw. All lift speed constants in this
        # module assume BIT2=0; a firmware default or re-flash resets it to
        # BIT2=1 which silently caps every speed command by 50x. Fix it here on
        # every connect (EPROM write, survives reboot).
        phase = int(self._bus.read("Phase", self.cfg.name, normalize=False))
        if phase & 0x04:
            import logging

            logger = logging.getLogger(__name__)
            logger.info("lift Phase=0x%02X BIT2=1 (1 step/s/raw) -> switching to BIT2=0", phase)
            self._bus.write("Torque_Enable", self.cfg.name, 0)
            self._bus.write("Lock", self.cfg.name, 0)
            self._bus.write("Phase", self.cfg.name, phase & ~0x04)
            time.sleep(0.2)
            self._bus.write("Lock", self.cfg.name, 1)
            verify = int(self._bus.read("Phase", self.cfg.name, normalize=False))
            logger.info("lift Phase after switch = 0x%02X (BIT2=%d)", verify, (verify >> 2) & 1)
        self._last_tick = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        self._extended_ticks = 0.0
        self._configured = True

    # ------------------------------------------------------------------
    # Zero persistence (recover absolute position without re-homing)
    # ------------------------------------------------------------------

    def save_zero(self) -> None:
        """Persist the current multi-turn tracking state to a file (for recovery on next connection)."""
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
                "model_number": self._read_model_number(),
            }
            with open(self.cfg.zero_file, "w") as f:
                json.dump(state, f)
        except Exception:
            pass

    def _read_model_number(self) -> int | None:
        """Read the servo's Model_Number register (identifies the motor)."""
        try:
            return int(self._bus.read("Model_Number", self.cfg.name, normalize=False))
        except Exception:
            return None

    def restore_zero(self) -> bool:
        """Try to restore the absolute position from the file, avoiding re-homing.

        Precondition: the leadscrew is self-locking, so the mechanical position is
        unchanged after power-off -> encoder reading is reproducible.
        If the current encoder reading matches the recorded last_tick (within
        tolerance), restore the multi-turn tracking state and return True;
        otherwise return False (the caller should re-home).
        """
        import logging

        logger = logging.getLogger(__name__)
        if not self.enabled or not self.cfg.zero_file:
            logger.info("restore_zero: SKIP (enabled=%s zero_file=%s)", self.enabled, self.cfg.zero_file)
            return False
        import json
        import os

        if not os.path.isfile(self.cfg.zero_file):
            logger.info("restore_zero: no zero file at %s → re-home", self.cfg.zero_file)
            return False
        try:
            with open(self.cfg.zero_file) as f:
                state = json.load(f)
        except Exception:
            logger.info("restore_zero: zero file unreadable → re-home")
            return False

        try:
            cur = float(self._bus.read("Present_Position", self.cfg.name, normalize=False))
        except Exception:
            logger.info("restore_zero: read Present_Position failed → re-home")
            return False

        last = float(state.get("last_tick", -1))
        tol = 30  # ±30 ticks ≈ ±0.06mm, tolerates small encoder drift after power-cycled restart
        if abs(cur - last) > tol:
            logger.info("restore_zero: MISMATCH cur=%s last=%s (tol=%s) → re-home", cur, last, tol)
            return False

        # Motor identity check: if the servo was replaced (different model), the
        # old zero state is meaningless — re-home. Model_Number was only added to
        # the file after this change; older files simply have no check.
        saved_model = state.get("model_number")
        cur_model = self._read_model_number()
        if saved_model is not None and cur_model is not None and saved_model != cur_model:
            logger.info(
                "restore_zero: MOTOR CHANGED (file model=%s current model=%s) → re-home",
                saved_model,
                cur_model,
            )
            return False

        # Triangle consistency: extended_ticks is the multi-turn displacement
        # accumulated since home, so it must agree with (cur - abs_tick_at_home)
        # modulo one revolution. A replacement motor has a different encoder
        # origin — even if the raw tick coincidentally matches, this relation
        # breaks. This catches same-model swaps the raw-match check cannot.
        saved_abs = state.get("abs_tick_at_home")
        if saved_abs is not None:
            expected = (cur - float(saved_abs)) % self._ticks_per_rev
            actual = float(state.get("extended_ticks", 0.0)) % self._ticks_per_rev
            diff = abs(expected - actual)
            diff = min(diff, self._ticks_per_rev - diff)
            if diff > tol:
                logger.info(
                    "restore_zero: ENCODER ORIGIN CHANGED — triangle check "
                    "expected %.0f got %.0f (diff %.0f ticks) → re-home",
                    expected,
                    actual,
                    diff,
                )
                return False

        # Sanity check: restore the state, then confirm the resulting height is
        # physically plausible. A replacement motor (or re-assembly) can leave the
        # old extended_ticks pointing at a height outside the mechanical range,
        # even when the raw tick happens to match. Re-home if implausible.
        saved_ext = float(state.get("extended_ticks", 0.0))
        saved_abs = state.get("abs_tick_at_home")
        self._extended_ticks = saved_ext
        self._last_tick = cur
        self._abs_tick_at_home = saved_abs
        try:
            h = self.get_height_mm()
        except Exception:
            h = float("nan")
        margin = max(self.cfg.soft_max_mm * 1.25, 50.0)
        if not (self.cfg.soft_min_mm - margin <= h <= self.cfg.soft_max_mm + margin):
            # Roll back the speculative state before re-homing.
            self._extended_ticks = 0.0
            self._last_tick = cur
            self._abs_tick_at_home = None
            logger.info(
                "restore_zero: IMPLAUSIBLE height %.1fmm from old zero (range %.0f~%.0f) → re-home",
                h,
                self.cfg.soft_min_mm,
                self.cfg.soft_max_mm,
            )
            return False

        logger.info("restore_zero: MATCH cur=%s last=%s — restoring position, no re-home", cur, last)

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
        # When the displacement within a sampling interval may exceed half a turn
        # (crossing the 0 boundary inverts the delta sign), use Present_Velocity's
        # sign to determine the true wrap direction (velocity direction = real motion direction).
        # Only read in the ambiguous zone to avoid needless bus overhead.
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
        # Refresh the shared cache so apply_action()'s safety guards (which use
        # the cache to avoid a per-frame real-time bus read) always see the
        # latest height whenever any code path reads it.
        self._cached_height_mm = (self._extended_deg() - self._z0_deg) * self._mm_per_deg
        return self._cached_height_mm

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
        import logging

        logger = logging.getLogger(__name__)
        # Torque is NOT enabled by bus.connect() (handshake only) and NOT by
        # self.configure() either; if home() runs before parent.configure() it
        # would write Goal_Velocity to a torque-disabled motor, "stall" instantly
        # (position never moves) and save a garbage zero. Enable torque here so
        # homing actually drives the carriage down.
        from lerobot.motors.feetech import TorqueMode

        self._bus.write("Torque_Enable", name, TorqueMode.ENABLED.value)
        if hasattr(self.cfg, "motor_lock_needed"):
            self._bus.write("Lock", name, 0)
        logger.info("home(): driving %s DOWN at vel=%s until stall", name, -self.cfg.home_down_speed)

        # Downward homing = negative velocity (positive = up, negative = down).
        self._bus.write("Goal_Velocity", name, -self.cfg.home_down_speed)

        stuck = 0
        last_tick = int(self._bus.read("Present_Position", name, normalize=False))

        try:
            for _ in range(6000):  # ~300 s at 50 ms (low-speed homing needs a longer timeout)
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
        # get_height_mm() refreshes the cache used by apply_action()'s safety
        # guards; this is also the only place that updates it at observation
        # time, so the cached height stays within one slow-bus sample.
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
                # Use the cached height (refreshed by contribute_observation at a
                # lower rate) instead of a real-time bus read: the lift shares
                # bus2 with the right arm, and a per-frame Present_Position read
                # here adds a full serial round-trip that delays the right arm.
                # The cache is fresh enough for the 3/200mm soft-limit guards.
                cur_mm = self._cached_height_mm
                v = int(self._apply_safety_limits(v, cur_mm))
                orig_v = int(action[key_v])
                if orig_v != 0:
                    import logging

                    logging.getLogger(__name__).info(
                        "apply_action vel: raw=%s clamped=%s cur_mm=%.2f final=%s mode_set=%s",
                        orig_v,
                        max(-self.cfg.v_max, min(self.cfg.v_max, orig_v)),
                        cur_mm,
                        v,
                        getattr(self, "_mode_is_velocity", "unknown"),
                    )
            except Exception:
                pass
            # Positive velocity = up (consistent with the P-controller path; dir_sign semantics in docstring)
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
