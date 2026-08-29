"""BIT2=0 full speed test — first home to the bottom, then probe raw=20/60/110 step by step.

Prerequisite: the servo Phase has been switched to BIT2=0 (50 step/s/raw), see switch_phase_bit2.py.

Procedure:
1. home(): go down to the mechanical bottom (stall detection), zero the position
2. Measure speed upward from the bottom (safe, cannot hit the top):
   raw=20  -> 3s (expected ~1.9mm/s)
   raw=60  -> 3s (expected ~5.7mm/s)
   raw=110 -> 3s (expected ~10.7mm/s)
3. Short pause between samples; accumulate the multi-turn encoder (per-sample delta accumulation, avoids misjudging a single wrap)

⚠️ After the test the motor stops at mid height; it can be reused or homed manually.
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

# In BIT2=0 units, force safe home parameters (prevents another sudden surge)
lift.cfg.home_down_speed = 10   # 10x50 = 500 step/s, equivalent to the old 500 in BIT2=1
lift.cfg.v_max = 110            # 110x50 = 5500 step/s = physical upper limit

phase = int(bus.read("Phase", name, normalize=False))
print(f"Phase = {phase} (0x{phase:02X}) BIT2={'1' if phase & 0x04 else '0'}")
if phase & 0x04:
    print("⚠️  BIT2=1! 请先运行 switch_phase_bit2.py 切换")

# 1. Home to the bottom
print("\n[1] 归零到底 (home)...")
try:
    lift.home()
    print(f"    归零完成, 高度 = {lift.get_height_mm():.1f} mm")
except Exception as e:
    print(f"    home 失败: {str(e)[:80]}, 继续 (可能已在底部)")
    lift._extended_ticks = 0.0
    lift._last_tick = float(bus.read("Present_Position", name, normalize=False))
    lift._z0_deg = 0.0

# 2. Per-sample delta accumulation speed test (correctly handles multi-turn wraps)
def probe(raw, dur=3.0):
    # Reset tracking
    lift._extended_ticks = 0.0
    lift._last_tick = float(bus.read("Present_Position", name, normalize=False))
    lift._z0_deg = 0.0

    h0 = lift.get_height_mm()
    bus.write("Goal_Velocity", name, raw)

    last = lift._last_tick
    samples = 0
    t0 = time.time()
    try:
        while time.time() - t0 < dur:
            time.sleep(0.1)
            cur = int(bus.read("Present_Position", name, normalize=False))
            d = cur - last
            # Multi-turn wrap correction (can happen multiple times)
            half = 2048
            for _ in range(8):
                if d > half:
                    d -= 4096
                elif d < -half:
                    d += 4096
                else:
                    break
            lift._extended_ticks += d
            last = cur
            samples += 1
    except KeyboardInterrupt:
        pass
    bus.write("Goal_Velocity", name, 0)
    time.sleep(0.3)

    h1 = lift.get_height_mm()
    dt = time.time() - t0
    dist = h1 - h0
    print(f"  raw={raw:>4}: {dt:4.1f}s 走了 {dist:6.1f} mm = {dist/dt:5.2f} mm/s  (Δticks={lift._extended_ticks:.0f})")
    time.sleep(1.0)  # Let it settle

print("\n[2] BIT2=0 测速 (从底部向上):")
for raw in [20, 60, 110]:
    probe(raw)

# 3. Return to the bottom
print("\n[3] 回到底部...")
try:
    lift.home()
    print(f"    完成, 高度 = {lift.get_height_mm():.1f} mm")
except Exception as e:
    print(f"    home: {str(e)[:80]}")

robot.disconnect()
print("\n✅ 测速完成")
