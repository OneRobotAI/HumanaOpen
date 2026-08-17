"""遥操关节方向诊断脚本 — 逐关节实测主从臂映射.

用法:
    python3 examples/diagnose_teleop.py

原理:
    用"无翻转、无重映射"的原始映射逐个关节测试:
    - 你手动把主臂某关节向一个方向转动
    - 脚本记录主臂该关节的读数变化 Δ_leader
    - 同时把动作发给从臂
    - 记录从臂各关节的读数变化
    - 判断: 从臂哪个关节动了 (映射), 方向是否一致 (是否需要翻转)

诊断后根据输出配置:
    flip_joints:  方向反的关节 → 加入该侧翻转表
    joint_remap:  映射错位 (从臂动的是别的关节) → 建立重映射

准备:
    1. 主臂、从臂都已校准 (从臂用自然下垂+夹爪闭合零位)
    2. 从臂 12V, 主臂 7.4V 供电
    3. 确保周围无障碍物, 从臂手臂会动
"""

import time

from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
from lerobot_robot_humanalite.leader import (
    BiHumanaLiteLeader,
    BiHumanaLiteLeaderConfig,
    JOINT_NAMES,
)

follower_cfg = HumanaLiteConfig(
    id="follower",
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,
)

# 诊断模式: 无翻转、无重映射, 用原始 1:1 映射
leader_cfg = BiHumanaLiteLeaderConfig(
    id="leader",
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
    # flip_joints / joint_remap 不传 → 默认官方表; 诊断时需原始映射, 见下方构造
)

follower = HumanaLite(follower_cfg)
# 手动构造 leader: 用空翻转表和空重映射
leader_left = BiHumanaLiteLeader(leader_cfg)
# 强制原始映射: 清空翻转和重映射
for arm in (leader_left.left_arm, leader_left.right_arm):
    arm._motors_to_flip = []
    arm._joint_remap = {}

SIDES = [("left", "left_arm"), ("right", "right_arm")]

# 每个关节建议的"正方向"转动提示 (供操作者参考)
JOINT_DIR_HINT = {
    "shoulder_pan": "rotate left (horizontal)",
    "shoulder_lift": "raise up",
    "shoulder_roll": "rotate around axis (right-arm direction)",
    "elbow_flex": "bend (upward)",
    "forearm_rotation": "rotate forearm (clockwise viewed)",
    "wrist_flex": "flex wrist up",
    "wrist_yaw": "rotate wrist horizontally",
    "gripper": "open gripper",
}


def main():
    follower.connect(calibrate=False)
    leader_left.connect(calibrate=False)
    print("Leader & follower connected (raw mapping diagnosis mode)")
    print("=" * 60)

    for side, prefix in SIDES:
        print(f"\n### {side.upper()} SIDE DIAGNOSIS ###")
        for joint in [j for j in JOINT_NAMES if j != "gripper"] + ["gripper"]:
            action_key = f"{prefix}_{joint}.pos"
            print(f"\n--- {joint} ---")
            print(f"  Move the leader {side} arm's {joint} joint ({JOINT_DIR_HINT.get(joint, 'rotate')})")
            input("  Press ENTER to record baseline...")

            # 记录主臂和从臂的初始值
            # 主臂读数: 直接读
            la = leader_left.left_arm if side == "left" else leader_left.right_arm
            l0 = la.get_action().get(f"{joint}.pos", 0.0)
            # 从臂读数
            obs0 = follower.get_observation()
            f0 = obs0.get(action_key, 0.0)

            input("  Now move the leader joint (hold it), then press ENTER...")

            # 读取主臂动作 (完整双臂, 原始映射) → 发送到从臂
            action = leader_left.get_action()
            # 保留从臂非双臂部分不动 (头部保持, 轮子/升降停)
            obs_static = follower.get_observation()
            for k, v in obs_static.items():
                if k.startswith("head_") and k.endswith(".pos"):
                    action[k] = v
            action["x.vel"] = 0.0
            action["theta.vel"] = 0.0
            action["lift_axis.height_mm"] = obs_static.get("lift_axis.height_mm", 0)
            follower.send_action(action)

            # 等待从臂电机跟上 (速度受 max_relative_target 限制, 给足时间)
            time.sleep(0.5)

            l1 = la.get_action().get(f"{joint}.pos", 0.0)
            obs1 = follower.get_observation()
            f1 = obs1.get(action_key, 0.0)

            d_leader = l1 - l0
            d_follower = f1 - f0

            # 同时显示从臂其他关节是否也有明显变化 (映射错位检测)
            others = []
            for k, v in obs1.items():
                if k.startswith(prefix) and k.endswith(".pos") and k != action_key:
                    d = v - obs0.get(k, 0.0)
                    if abs(d) > 1.0:
                        others.append(f"{k}={d:+.1f}")

            print(f"  Leader {joint}: Δ={d_leader:+.1f}")
            print(f"  Follower {joint}: Δ={d_follower:+.1f}")
            if others:
                print(f"  ⚠️ Other follower joints moved too: {others}  <- mapping misaligned!")

            if abs(d_leader) < 0.5:
                print("  ⚠️ Leader reading barely changed, please retry")
                continue

            if abs(d_follower) < 0.5:
                print("  ⚠️ Follower joint did not move - maybe mapped to another joint, or follower not calibrated")
                continue

            if (d_leader > 0) == (d_follower > 0):
                print(f"  ✅ Same direction (no flip needed)")
            else:
                print(f"  ❌ Opposite direction (add to flip_joints)")

    print("\n" + "=" * 60)
    print("Diagnosis complete! Configure flip_joints / joint_remap from the results")

    leader_left.disconnect()
    follower.disconnect()


if __name__ == "__main__":
    main()
