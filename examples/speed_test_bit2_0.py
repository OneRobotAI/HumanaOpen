"""BIT2=0 完整测速 — 先归零到底, 再逐步测 raw=20/60/110.

前提: 舵机 Phase 已切换为 BIT2=0 (50 step/s/raw), 见 switch_phase_bit2.py.

流程:
1. home(): 下行至机械底部 (堵转检测), 归零
2. 从底部向上测速 (安全, 不会撞顶):
   raw=20  → 3s (期望 ~1.9mm/s)
   raw=60  → 3s (期望 ~5.7mm/s)
   raw=110 → 3s (期望 ~10.7mm/s)
3. 每样本间短暂停, 累计多圈编码器 (逐样本 Δ 累积, 避免单次环绕误判)

⚠️ 测试后电机停在中间高度, 可继续用或手动归零.
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

# BIT2=0 单位下, 强制安全 home 参数 (防止再次暴冲)
lift.cfg.home_down_speed = 10   # 10×50 = 500 step/s, 与旧 BIT2=1 的 500 等价
lift.cfg.v_max = 110            # 110×50 = 5500 step/s = 物理上限

phase = int(bus.read("Phase", name, normalize=False))
print(f"Phase = {phase} (0x{phase:02X}) BIT2={'1' if phase & 0x04 else '0'}")
if phase & 0x04:
    print("⚠️  BIT2=1! 请先运行 switch_phase_bit2.py 切换")

# 1. 归零到底
print("\n[1] 归零到底 (home)...")
try:
    lift.home()
    print(f"    归零完成, 高度 = {lift.get_height_mm():.1f} mm")
except Exception as e:
    print(f"    home 失败: {str(e)[:80]}, 继续 (可能已在底部)")
    lift._extended_ticks = 0.0
    lift._last_tick = float(bus.read("Present_Position", name, normalize=False))
    lift._z0_deg = 0.0

# 2. 逐样本 Δ 累积测速 (正确处理多圈环绕)
def probe(raw, dur=3.0):
    # 重置跟踪
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
            # 多圈环绕修正 (可多次)
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
    time.sleep(1.0)  # 停稳

print("\n[2] BIT2=0 测速 (从底部向上):")
for raw in [20, 60, 110]:
    probe(raw)

# 3. 回到底部
print("\n[3] 回到底部...")
try:
    lift.home()
    print(f"    完成, 高度 = {lift.get_height_mm():.1f} mm")
except Exception as e:
    print(f"    home: {str(e)[:80]}")

robot.disconnect()
print("\n✅ 测速完成")
