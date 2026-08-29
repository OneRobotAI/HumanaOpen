"""Head tilt limit fine measurement — confirm mechanical hard limits + locate the interference point.

Purpose: after unlocking the servo limits, confirm whether down 1347 / up 2242 are mechanical hard limits,
and check the current change near the limits (stall signature) to judge whether there is still room for mechanical modification.

Usage:
    python3 examples/diag_head_tilt_limits.py
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()
name = "head_tilt"


def probe(target, wait=0.6):
    """Write the target position, wait, return (final position, current)."""
    bus.write("Goal_Position", name, target, normalize=False)
    time.sleep(wait)
    pos = int(bus.read("Present_Position", name, normalize=False))
    cur = 0
    try:
        cur = int(bus.read("Present_Current", name, normalize=False))
    except Exception:
        pass
    return pos, cur


try:
    bus.write("Torque_Enable", name, 1)
    time.sleep(0.5)

    # Start 100 ticks outside the known boundary, approach in 10-tick steps, watch the current rise
    print("向下极限精测 (从 1247 开始):")
    for raw in range(1247, 1367, 10):
        pos, cur = probe(raw)
        deg = (pos - 2048) * 360 / 4096
        print(f"  target={raw:>4} → pos={pos:>4} ({deg:+.1f}°)  I={cur}mA")
        if pos < raw - 30:  # Servo refuses to approach the target (hard limit)
            print(f"  ⛔ 硬限位确认在 pos={pos} 附近")
            break

    # Return to center position
    probe(2048)
    print()

    print("向上极限精测 (从 2342 开始):")
    for raw in range(2342, 2222, -10):
        pos, cur = probe(raw)
        deg = (pos - 2048) * 360 / 4096
        print(f"  target={raw:>4} → pos={pos:>4} ({deg:+.1f}°)  I={cur}mA")
        if pos > raw + 30:
            print(f"  ⛔ 硬限位确认在 pos={pos} 附近")
            break

    probe(2048)

except KeyboardInterrupt:
    print("\n⛔ 中断")

finally:
    try:
        bus.write("Goal_Position", name, 2048, normalize=False)
        time.sleep(0.5)
        bus.write("Torque_Enable", name, 0)
    except Exception:
        pass
    try:
        bus.disconnect()
    except Exception:
        pass
    print("已断开")
