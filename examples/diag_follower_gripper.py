"""从臂夹爪读数诊断 — 直接读原始编码器值, 确认物理运动时读数是否变化.

注意: 连接后先释放夹爪扭矩 (否则从臂夹爪锁死掰不动).

用法:
    python3 examples/diag_follower_gripper.py [left|right]
"""

import sys
import time

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

side = sys.argv[1] if len(sys.argv) > 1 else "left"
gripper_name = f"{side}_arm_gripper"

config = HumanaOpenConfig(
    id="follower",
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,
)
robot = HumanaOpen(config)

try:
    robot.connect(calibrate=False)
    # 左右臂夹爪都释放扭矩 (防止对侧锁死)
    for name in ("left_arm_gripper", "right_arm_gripper"):
        bus = robot.bus1 if name.startswith("left") else robot.bus2
        print(f"释放 {name} 扭矩...")
        bus.write("Torque_Enable", name, 0)
    time.sleep(0.3)

    bus = robot.bus1 if side == "left" else robot.bus2
    print(f"从臂 {side} 已连接, 夹爪: {gripper_name}")
    print("手动张开/闭合从臂夹爪, 观察读数变化 (Ctrl+C 退出)")
    print("=" * 55)
    print(f"{'原始编码器':>10} | {'归一化(0-100)':>14}")
    print("-" * 55)

    while True:
        raw = bus.read("Present_Position", gripper_name, normalize=False)
        norm = bus.read("Present_Position", gripper_name)
        print(f"{raw:>10} | {norm:>14.1f}")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n退出")

finally:
    robot.disconnect()
