"""Switch ST3250 Phase BIT2 and verify speed — test the BIT2=0 speed-up approach.

Background:
- BIT2=1 (current): 1 step/s/raw → raw 1000 = 1000 steps/s (1.94mm/s)
- BIT2=0 (candidate): 50 step/s/raw → raw 20 = 1000 steps/s (same speed)
               → physical upper limit 5500 steps/s = raw 110 → 10.7mm/s!

Principle: with BIT2=0, the same speed only needs raw÷50 (0~110 range), fully avoiding the >1000 wrap-around region.

⚠️ This modifies the servo EPROM configuration (Phase register). Switch back with --restore.

Usage:
    python3 examples/switch_phase_bit2.py [--restore]
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

RESTORE = "--restore" in sys.argv

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

# current Phase
phase = int(bus.read("Phase", name, normalize=False))
print(f"当前 Phase = {phase} (0x{phase:02X}) BIT2={'1' if phase & 0x04 else '0'}")

new_phase = (phase & ~0x04) if not RESTORE else (phase | 0x04)
action = "清除 BIT2 (→50step/s/raw)" if not RESTORE else "恢复 BIT2 (→1step/s/raw)"
print(f"执行: {action} → Phase = {new_phase} (0x{new_phase:02X})")

# modify Phase: need Torque_Enable=0, Lock=0, write Phase, then write Lock=1
try:
    bus.write("Torque_Enable", name, 0)
    time.sleep(0.2)
    bus.write("Lock", name, 0)
    time.sleep(0.2)
    bus.write("Phase", name, new_phase)
    time.sleep(0.2)
    bus.write("Lock", name, 1)
    time.sleep(0.3)
    # power-cycle to confirm? not needed, just read back
    verify = int(bus.read("Phase", name, normalize=False))
    print(f"验证 Phase = {verify} (0x{verify:02X}) BIT2={'1' if verify & 0x04 else '0'}")
except Exception as e:
    print(f"修改失败: {str(e)[:100]}")
    robot.disconnect()
    sys.exit(1)

if not RESTORE:
    # speed test with BIT2=0 (50 step/s/raw)
    print("\nBIT2=0 测速 (50 step/s/raw):")
    def probe(raw, dur=2):
        try:
            e0 = bus.read("Present_Position", name, normalize=False)
            bus.write("Goal_Velocity", name, raw)
            time.sleep(dur)
            e1 = bus.read("Present_Position", name, normalize=False)
            pv = bus.read("Present_Velocity", name, normalize=False)
            bus.write("Goal_Velocity", name, 0)
            d = e1 - e0
            if d > 2048: d -= 4096
            elif d < -2048: d += 4096
            mm = abs(d)/4096*8
            speed = mm/dur
            print(f"  raw={raw:>4}: Δenc={d:>6} ({speed:.2f}mm/s) 反馈vel={pv:>5} → {'↑' if d>0 else '↓'}")
            time.sleep(0.5)
        except Exception as e:
            print(f"  raw={raw}: {str(e)[:40]}")
            time.sleep(0.5)

    # physical upper limit 5500 steps/s = raw 110
    for raw in [20, 60, 110]:
        probe(raw)
    print("\n若 raw 110 → ~10mm/s 且方向正确 = 提速成功!")
    print("记住用 --restore 切回, 或保持 BIT2=0 并修改 v_max/kp_vel")

robot.disconnect()
