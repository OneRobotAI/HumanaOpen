"""Head tilt (ID 13) real travel range diagnostic — small steps, stop at the mechanical limit.

Why: the calibration file shows head_tilt range=[1430, 2096], only 666 ticks (~58°),
and the user reports the tilt cannot be lowered to the very bottom. This script bypasses
the calibration limits and directly drives ID 13, inching from the current position toward
"down", checking each time whether the position changed (no change = mechanical limit), to
determine the real physical travel range, for recalibration or correcting the limits.

Usage:
    python3 examples/diag_head_tilt_range.py [--step 50] [--max-steps 60]

Safety:
- small steps (default 50 ticks ≈ 4.4°) + position-change detection, auto-stop at the limit
- only move the head tilt, never touch any other motor
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

STEP = 50
MAX_STEPS = 60
if "--step" in sys.argv:
    STEP = int(sys.argv[sys.argv.index("--step") + 1])
if "--max-steps" in sys.argv:
    MAX_STEPS = int(sys.argv[sys.argv.index("--max-steps") + 1])

# register only the head tilt (ID 13) — on the port1 bus
bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()

try:
    # current position
    cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
    print(f"Starting raw position = {cur}")
    print(f"Calibration range: [1430, 2096] (current telop upper limit)")

    # probe toward "down" from the calibration lower bound (small steps + mechanical limit detection)
    target = cur
    print(f"\nProbing 'down' (STEP={STEP} ticks/step)...")
    for i in range(MAX_STEPS):
        target -= STEP
        bus.write("Goal_Position", "head_tilt", target, normalize=False)
        time.sleep(0.15)

        new_cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
        moved = new_cur != cur
        if not moved:
            print(f"  ⛔ Mechanical limit! Stopped at raw={new_cur} (step {i})")
            break
        cur = new_cur
        if i % 5 == 0 or i == MAX_STEPS - 1:
            print(f"  step {i:2d}: raw={cur:>5}")

    print(f"\nDownward true lower limit ≈ raw {cur}")
    print(f"  = normalized {(cur-2048)*360/4096:+.1f}° (calibration file is {(1430-2048)*360/4096:+.1f}°)")

    # return to the middle of the calibration range (avoid leaving it at the limit position)
    print(f"\nReturn to the middle of the calibration range (raw 1763)...")
    bus.write("Goal_Position", "head_tilt", 1763, normalize=False)
    time.sleep(0.5)
    cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
    print(f"  current raw = {cur}")

except KeyboardInterrupt:
    print("\n⛔ Interrupted")

finally:
    try:
        bus.disconnect()
    except Exception:
        pass
    print("Disconnected")
