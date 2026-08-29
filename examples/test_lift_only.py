"""Test only the lift axis — operate the lift motor on bus2 directly, without touching the right arm/wheels/arms.

Procedure:
1. Create the bus, registering only the lift motor (id=9, sts3250)
2. Home: drive down to the bottom until stall, then stop
3. Raise 50mm → stop → lower back to 0
"""

import time

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

from lerobot_robot_humanaopen.lift_axis import LiftAxisConfig, HumanaOpenLiftAxis

# Register only the lift motor — right arm/wheels are not touched at all
bus = FeetechMotorsBus(
    port="/dev/ttyACM1",
    motors={"lift_axis": Motor(9, "sts3250", MotorNormMode.DEGREES)},
)
bus.connect()

try:
    lift = HumanaOpenLiftAxis(LiftAxisConfig(), bus)
    lift.attach()
    lift.configure()

    print("[1] Homing (drive down until stall)...")
    lift.home()
    h0 = lift.get_height_mm()
    print(f"    Homing done, height = {h0:.1f} mm")
    print()

    print("[2] Raise to 50mm...")
    lift.apply_action({"lift_axis.height_mm": 50.0})
    h = h0
    for _ in range(400):  # up to 20 s
        time.sleep(0.05)  # 20Hz sampling: at 8.7mm/s max, ~89 ticks/sample << half-turn
        h = lift.get_height_mm()
        if h >= 49.0:
            break
    print(f"    Height = {h:.1f} mm")
    print()

    print("[3] Lower to 3mm (descent_floor guard, cannot go below 3mm)...")
    lift.apply_action({"lift_axis.height_mm": 3.0})
    for _ in range(400):
        time.sleep(0.05)
        h = lift.get_height_mm()
        if h <= 3.5:
            break
    print(f"    Height = {h:.1f} mm")
    print()

    print("=" * 40)
    print(f"Result: {h0:.1f} → {h:.1f}  (lift test done)")

except KeyboardInterrupt:
    print("\n⛔ Emergency stop...")
    try:
        bus.write("Goal_Velocity", "lift_axis", 0)
        bus.write("Torque_Enable", "lift_axis", 0)
    except Exception:
        pass

finally:
    try:
        bus.disconnect()
    except Exception as e:
        print(f"Disconnect: {e}")
    print("Disconnected")
