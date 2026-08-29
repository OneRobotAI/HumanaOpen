"""ST3250 Goal_Velocity encoding discriminator — confirm the firmware behavior of reversing above >1000.

Usage:
    python3 examples/diag_st3250_speed.py

Principle:
    with BIT2=1 (current, 1 step/s/raw) write different raws in sequence and observe the direction:
    - 11-bit signed truncation: 1024→-1024 fast reverse, 2048→0 stops, 3071→+1023 forward
    - sign-magnitude BIT10: 1024→-0 stops, 2048→-1024 reverse, 3071→-1023 reverse
    - normal sign-magnitude BIT15: all forward and increasing

    two points are enough to discriminate: raw=1024 and raw=2048
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

robot = HumanaOpen(HumanaOpenConfig(
    id="follower", port1="/dev/ttyACM0", port2="/dev/ttyACM1",
    port3=None, cameras={}, home_lift_on_connect=False,
))
_orig = builtins.input
builtins.input = lambda *a, **k: ""
try:
    robot.connect(calibrate=False)
except Exception as e:
    print(f"connect 警告: {e}")

lift = robot.lift_axis
name = "lift_axis"
bus = lift._bus

print(f"当前 Phase = {bus.read('Phase', name, normalize=False)} (BIT2={'1' if bus.read('Phase', name, normalize=False) & 0x04 else '0'})")
print("=" * 60)

def test(raw, dur=1.5):
    try:
        e0 = bus.read("Present_Position", name, normalize=False)
        v0 = bus.read("Present_Velocity", name, normalize=False)
        bus.write("Goal_Velocity", name, raw)
        time.sleep(dur)
        e1 = bus.read("Present_Position", name, normalize=False)
        v1 = bus.read("Present_Velocity", name, normalize=False)
        bus.write("Goal_Velocity", name, 0)
        d = e1 - e0
        if d > 2048: d -= 4096
        elif d < -2048: d += 4096
        direction = "上升" if d > 0 else ("下降" if d < 0 else "停")
        print(f"  raw={raw:>5}: Δenc={d:>5} ({abs(d)/4096*8:.1f}mm) Present_Vel={v0}→{v1} → {direction}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  raw={raw} 失败: {str(e)[:60]}")
        time.sleep(0.5)

print("判别实验: 写不同 raw 观察方向")
print("(升降会小幅移动, 确保无障碍)")
print()
for raw in [500, 1000, 1024, 1025, 1500, 2048, 3071]:
    test(raw)

print()
print("=" * 60)
print("判别标准:")
print("  raw=1024 → 若快速反转 → 11位有符号截断 (BIT2=1下最高只能~1000)")
print("  raw=2048 → 若停住     → 11位有符号截断")
print("  raw=3071 → 若正向     → 11位有符号截断 (3071-2048=1023)")
robot.disconnect()
