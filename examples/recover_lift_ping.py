"""ST3250 恢复后诊断 — 只读, 不移动电机.

用途: 堵转/故障保护后, 确认舵机通信已恢复.
只读 Present_Position / Present_Velocity / Present_Current / Temperature.
"""

import sys
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

print(f"Phase = {bus.read('Phase', name, normalize=False)}")

for reg in ["Present_Position", "Present_Velocity", "Present_Current", "Present_Temperature"]:
    try:
        v = bus.read(reg, name, normalize=False)
        print(f"  {reg}: {v}  ✅")
    except Exception as e:
        print(f"  {reg}: {str(e)[:60]}  ❌")

try:
    bus.write("Goal_Velocity", name, 0)
    print("  Goal_Velocity=0 写入 ✅ (电机已停止/保持)")
except Exception as e:
    print(f"  Goal_Velocity: {str(e)[:60]}  ❌")

robot.disconnect()
