"""主臂 (leader, open-arms-mini) 交互式校准脚本 (录真实行程).

流程 (配合交互提示, 每臂):
1. 自然下垂 + 夹爪闭合 → 回车 (设为零点)
2. 逐个关节走满行程 (录真实 min/max, 与从臂归一化空间一致)
3. 夹爪: 闭合位置 → 回车; 张开位置 → 回车
4. 保存校准文件 (id="leader", 与从臂 follower.json 分开)

说明:
- 默认 calibration_mode="full" (录真实行程). 遥操和录数据共用同一份校准,
  录数据前无需重校. 若只需纯实时遥操可改 "quick" (关节全量程, 官方简化方式).
- 主臂: STS3215 C046 (7.4V), 左右各 8 舵机 (ID 1-8), 结构与从臂一致
- 左臂接 /dev/ttyACM2, 右臂接 /dev/ttyACM3 (按实际调整)
- 校准文件:
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_left.json
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_right.json
- 关节命名与从臂一致 (left_arm_*/right_arm_*), 遥操时 get_action() 可直接喂给 follower.send_action()

用法:
    python3 examples/calibrate_leader.py
"""

from lerobot_robot_humanalite.leader import BiHumanaLiteLeader, BiHumanaLiteLeaderConfig

config = BiHumanaLiteLeaderConfig(
    id="leader",                # 主臂校准文件名 (leader_left/leader_right.json)
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
    # calibration_mode 默认 "full" (录真实行程); 纯实时遥操可改 "quick"
)

print("=" * 55)
print("HumanaLite leader calibration (dual-arm, records real ranges)")
print("=" * 55)
print("Per arm:")
print("  1. Arm hanging straight down + gripper closed -> ENTER (zero pose)")
print("  2. Move each joint through full range (end to end) -> ENTER (record real limits)")
print("  3. Gripper closed position -> ENTER")
print("  4. Gripper open position -> ENTER")
print("  5. Save calibration")
print("Note: leader runs at 7.4V, torque released during calibration, arms move freely")
print("=" * 55)
print()

leader = BiHumanaLiteLeader(config)
try:
    leader.connect(calibrate=True)
    print()
    print("✅ Leader calibration complete!")
    print("Left arm:", leader.left_arm.calibration_fpath)
    print("Right arm:", leader.right_arm.calibration_fpath)

    # 读取一帧动作验证
    action = leader.get_action()
    print(f"✅ Actions readable: {len(action)} joints")
    for k in list(action)[:4]:
        print(f"   {k} = {action[k]:.1f}")

except KeyboardInterrupt:
    print("\n⛔ Calibration interrupted...")

finally:
    leader.disconnect()
    print("Disconnected")
