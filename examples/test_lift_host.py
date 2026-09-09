"""Host-side bare-metal lift test — run on the robot machine (the Host).

Run with NO host running (serial ports must be free). Tests the lift motor
(ID 9) directly:
  1. reads current state (pos/vel/current/load)
  2. pulses DOWN (-40) for 1.5s  → should visibly lower
  3. pulses UP   (+40) for 1.5s  → should visibly raise
  4. reports actual ticks moved per second
"""
import time

from lerobot.motors.feetech import FeetechMotorsBus, OperatingMode, TorqueMode
from lerobot.motors import Motor, MotorNormMode
from lerobot_robot_humanaopen.humanaopen import _motor_specs, RIGHT_ARM_JOINTS, WHEEL_JOINTS

specs = _motor_specs(False)
motors = {n: Motor(*specs[n]) for n in RIGHT_ARM_JOINTS + WHEEL_JOINTS}
motors["lift_axis"] = Motor(9, "sts3250", MotorNormMode.DEGREES)

bus = FeetechMotorsBus(port="/dev/ttyACM1", motors=motors)
bus.connect()
print("handshake OK; motors:", sorted(bus.motors))


def rd(name):
    return bus.read(name, "lift_axis", normalize=False)


print("\n--- Lift state (torque off) ---")
for reg in ("Present_Position", "Present_Velocity", "Present_Current",
            "Present_Temperature", "Operating_Mode", "Torque_Enable", "Lock"):
    try:
        print(f"  {reg} = {rd(reg)}")
    except Exception as e:
        print(f"  {reg} = ERR {str(e)[:60]}")

bus.write("Operating_Mode", "lift_axis", OperatingMode.VELOCITY.value)
bus.write("Torque_Enable", "lift_axis", TorqueMode.ENABLED.value)
bus.write("Lock", "lift_axis", 1)
print(f"\nAfter config: Mode={rd('Operating_Mode')} Torque={rd('Torque_Enable')} Lock={rd('Lock')}")


def pulse(label, vel, dt=1.5):
    p0 = rd("Present_Position")
    bus.write("Goal_Velocity", "lift_axis", vel)
    best_vel = 0
    samples = []
    stalled = False
    t0 = time.time()
    while time.time() - t0 < dt:
        time.sleep(0.2)
        p = rd("Present_Position")
        v = rd("Present_Velocity")
        c = rd("Present_Current")
        samples.append((p, v, c))
        if abs(v) > best_vel:
            best_vel = abs(v)
        # Stall detection (same heuristic as lift home()): raw current * 6.5
        # >= 200mA means the carriage is jammed at a mechanical limit.
        # Stop immediately instead of waiting out the pulse.
        if c * 6.5 >= 200:
            stalled = True
            break
    bus.write("Goal_Velocity", "lift_axis", 0)
    time.sleep(0.2)
    p1 = rd("Present_Position")
    dt_real = time.time() - t0
    tag = "  [STALLED-DETECTED, stopped early]" if stalled else ""
    print(f"\n  {label}: vel={vel:+d} Δpos={(p1-p0):+d} ticks in {dt_real:.1f}s "
          f"= {(p1-p0)/dt_real:+.1f} ticks/s (peak motor vel={best_vel}){tag}")
    for (p, v, c) in samples:
        print(f"    pos={p} vel={v} cur={c}")


pulse("DOWN -40", -40)
time.sleep(0.5)
pulse("UP   +40", +40)
time.sleep(0.5)
pulse("DOWN -110", -110)
time.sleep(0.5)
pulse("UP   +110", +110)

bus.write("Goal_Velocity", "lift_axis", 0)
print("\nFinal pos:", rd("Present_Position"))
try:
    bus.disconnect()
except Exception:
    pass
print("done")