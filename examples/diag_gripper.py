"""主臂夹爪读数诊断 — 直接读原始编码器值, 确认物理运动时读数是否变化.

注意: 连接后先释放夹爪扭矩 (否则主臂夹爪锁死掰不动).

用法:
    python3 examples/diag_gripper.py [left|right]

流程:
1. 连接指定主臂
2. 循环显示夹爪 (ID 8) 的原始编码器值 + 归一化值
3. 你手动张开/闭合夹爪, 观察读数是否变化
"""

import sys
import time

from lerobot_robot_humanalite.leader import BiHumanaLiteLeader, BiHumanaLiteLeaderConfig

side = sys.argv[1] if len(sys.argv) > 1 else "left"

config = BiHumanaLiteLeaderConfig(
    id="leader",
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
)
leader = BiHumanaLiteLeader(config)

try:
    leader.connect(calibrate=False)
    arm = leader.left_arm if side == "left" else leader.right_arm

    # 显式释放夹爪扭矩, 才能手动掰动
    print("释放 gripper 扭矩...")
    arm.bus.write("Torque_Enable", "gripper", 0)
    time.sleep(0.3)

    print(f"主臂 {side} 已连接, 夹爪电机名: {list(arm.bus.motors.keys())}")
    print("现在手动张开/闭合主臂夹爪, 观察读数变化 (Ctrl+C 退出)")
    print("=" * 55)
    print(f"{'原始编码器':>10} | {'归一化(0-100)':>14} | {'get_action':>10}")
    print("-" * 55)

    while True:
        raw = arm.bus.read("Present_Position", "gripper", normalize=False)
        norm = arm.bus.read("Present_Position", "gripper")  # 归一化
        act = arm.get_action().get("gripper.pos", float("nan"))
        print(f"{raw:>10} | {norm:>14.1f} | {act:>10.1f}")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n退出")

finally:
    leader.disconnect()
