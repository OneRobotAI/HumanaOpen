"""Leader arm (leader, open-arms-mini) interactive calibration script (records real travel).

Procedure (with interactive prompts, per arm):
1. Arms hanging naturally + gripper closed -> ENTER (set as zero pose)
2. Move each joint through full range (records real min/max, consistent with follower normalized space)
3. Gripper: closed position -> ENTER; open position -> ENTER
4. Save the calibration file (id="leader", separate from follower.json)

Notes:
- Default calibration_mode="full" (records real travel). Teleoperation and data recording share the
  same calibration, no need to re-calibrate before recording. Change to "quick" if only real-time
  teleoperation is needed (full joint range, official simplified method).
- Leader arms: STS3215 C046 (7.4V), 8 servos per arm left/right (IDs 1-8), same structure as follower arms
- Left arm on /dev/ttyACM2, right arm on /dev/ttyACM3 (adjust as needed)
- Calibration files:
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/leader_left.json
    ~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/leader_right.json
- Joint naming matches the follower arms (left_arm_*/right_arm_*), so during teleoperation get_action()
  can feed directly into follower.send_action()

Usage:
    python3 examples/calibrate_leader.py
"""

from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

config = BiHumanaOpenLeaderConfig(
    id="leader",                # Leader-arm calibration file name (leader_left/leader_right.json)
    left_arm_port="/dev/ttyACM0",
    right_arm_port="/dev/ttyACM1",
    # calibration_mode defaults to "full" (records real travel); change to "quick" for pure real-time teleoperation
)

print("=" * 55)
print("HumanaOpen leader calibration (dual-arm, records real ranges)")
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

leader = BiHumanaOpenLeader(config)
try:
    leader.connect(calibrate=True)
    print()
    print("✅ Leader calibration complete!")
    print("Left arm:", leader.left_arm.calibration_fpath)
    print("Right arm:", leader.right_arm.calibration_fpath)

    # Read one action frame to verify
    action = leader.get_action()
    print(f"✅ Actions readable: {len(action)} joints")
    for k in list(action)[:4]:
        print(f"   {k} = {action[k]:.1f}")

except KeyboardInterrupt:
    print("\n⛔ Calibration interrupted...")

finally:
    leader.disconnect()
    print("Disconnected")
