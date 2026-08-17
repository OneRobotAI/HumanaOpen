"""从动侧全身交互式校准脚本 (双臂 + 头部 + 轮子 + 升降).

流程 (配合 lerobot 交互提示):
1. 左臂 + 头部: 摆中位 → 回车; 逐个关节走满行程 → 回车
2. 右臂: 摆中位 → 回车; 逐个关节走满行程 → 回车
3. 自动: 轮子全范围 + 升降堵转归零
4. 保存校准文件

说明:
- 校准的是从动侧 (follower: ST3215 C018 双臂 + 头部, 轮子, 升降), 校准文件 id="follower"
- 主动侧 (leader, C046) 不在此脚本范围, 后续遥操时单独校准, 用 id="leader"
  两个 id 生成不同的校准文件, 互不覆盖:
    ~/.cache/huggingface/lerobot/calibration/robots/humanalite/follower.json  (从动侧)
    ~/.cache/huggingface/lerobot/calibration/robots/humanalite/leader.json    (主动侧)
- 摄像头跳过, 不影响校准
- 中位约定: 重力下垂关节 (shoulder_lift/elbow_flex) 自然下垂=零点;
  旋转关节 (shoulder_pan/forearm_rotation/wrist_yaw) 中间位; 夹爪半开

用法:
    python3 examples/calibrate_follower.py
"""

from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(
    id="follower",          # 从动侧校准文件名 (follower.json); 主动侧后续用 id="leader"
    port1="/dev/ttyACM0",   # 左臂 + 头
    port2="/dev/ttyACM1",   # 右臂 + 升降 + 轮子
    port3=None,             # 2 总线模式
    cameras={},             # 跳过摄像头
)

print("=" * 55)
print("HumanaLite follower calibration (arms + head + wheels + lift)")
print("=" * 55)
print("Steps:")
print("  1. Left arm + head: set zero pose (hanging joints at natural rest, rotation joints centered)")
print("  2. Left arm + head: move each joint through full range (end to end)")
print("  3. Right arm: set zero pose")
print("  4. Right arm: move each joint through full range")
print("  5. Auto: wheels full range + lift stall homing")
print("Note: torque is released during calibration, arms can be moved freely by hand")
print("=" * 55)
print()

robot = HumanaLite(config)
try:
    robot.connect(calibrate=True)
    print()
    print("✅ Calibration complete!")
    print("Calibration file:", robot.calibration_fpath)

    # 校准后读取一帧观察, 验证关节位置可读 (归一化)
    obs = robot.get_observation()
    pos_keys = [k for k in obs if k.endswith(".pos")]
    print(f"✅ Joint positions readable: {len(pos_keys)} joints")
    for k in pos_keys[:5]:
        print(f"   {k} = {obs[k]:.1f}")
    if len(pos_keys) > 5:
        print(f"   ... {len(pos_keys)} total")

except KeyboardInterrupt:
    print("\n⛔ Calibration interrupted...")

finally:
    robot.disconnect()
    print("Disconnected")
