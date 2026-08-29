"""Main-arm gripper reading diagnostics — read the raw encoder value directly to confirm whether the reading changes with physical motion.

Note: after connecting, first release the gripper torque (otherwise the main-arm gripper locks and cannot be pried open).

Usage:
    python3 examples/diag_gripper.py [left|right]

Procedure:
1. Connect the specified main arm
2. Loop and display the gripper (ID 8) raw encoder value + normalized value
3. Manually open/close the gripper and observe whether the reading changes
"""

import sys
import time

from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

side = sys.argv[1] if len(sys.argv) > 1 else "left"

config = BiHumanaOpenLeaderConfig(
    id="leader",
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
)
leader = BiHumanaOpenLeader(config)

try:
    leader.connect(calibrate=False)
    arm = leader.left_arm if side == "left" else leader.right_arm

    # Explicitly release gripper torque so it can be pried by hand
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
        norm = arm.bus.read("Present_Position", "gripper")  # normalized
        act = arm.get_action().get("gripper.pos", float("nan"))
        print(f"{raw:>10} | {norm:>14.1f} | {act:>10.1f}")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n退出")

finally:
    leader.disconnect()
