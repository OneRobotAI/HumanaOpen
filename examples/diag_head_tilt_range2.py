"""Clean head tilt (ID 13) true travel probing — after unlocking, slow bidirectional movement + current monitoring.

Background: Min=0/Max=4095 have been written to unlock the servo limits. Last time the probe went down to 1327 and the upward test then behaved abnormally.
This script: probes independently in both directions from the center position (each step 30 ticks, 0.3s wait),
monitors Present_Current to determine stall, and locates the true mechanical travel.

Usage:
    python3 examples/diag_head_tilt_range2.py
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

STEP = 30
WAIT = 0.3

bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()
name = "head_tilt"


def move_to(target):
    bus.write("Goal_Position", name, target, normalize=False)
    time.sleep(WAIT)
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
    start = int(bus.read("Present_Position", name, normalize=False))
    print(f"起始 raw={start}")

    # First return to center position 2048
    pos, _ = move_to(2048)
    print(f"中位 raw={pos}")

    # Probe downward (each step -STEP from the current position, stop on stall/no movement)
    print("\n向下探测:")
    cur = pos
    for i in range(100):
        target = cur - STEP
        new_pos, current = move_to(target)
        moved = abs(new_pos - cur) >= 2
        if not moved:
            print(f"  ⛔ 向下限位 raw={cur} ({(cur-2048)*360/4096:+.1f}°)  current={current}mA")
            break
        cur = new_pos
        if i % 4 == 0:
            print(f"  步 {i:2d}: raw={cur:>5} ({(cur-2048)*360/4096:+.1f}°)  I={current}")

    down_limit = cur

    # Probe upward (reverse from the limit point, confirm it can return + find the upper limit)
    print("\n向上探测 (从向下限位点):")
    cur = down_limit
    for i in range(120):
        target = cur + STEP
        new_pos, current = move_to(target)
        moved = abs(new_pos - cur) >= 2
        if not moved:
            print(f"  ⛔ 向上限位 raw={cur} ({(cur-2048)*360/4096:+.1f}°)  current={current}mA")
            break
        cur = new_pos
        if i % 5 == 0:
            print(f"  步 {i:2d}: raw={cur:>5} ({(cur-2048)*360/4096:+.1f}°)  I={current}")

    up_limit = cur
    print(f"\n真实行程: [{down_limit} ({-63.4 if down_limit<1327 else '?'}°) ... {up_limit} ({up_limit-2048})°]")

    # Return to center position
    pos, _ = move_to(2048)
    print(f"回中位 raw={pos}")

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
