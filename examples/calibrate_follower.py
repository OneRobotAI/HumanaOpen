"""Follower-side full-body interactive calibration script (both arms + head + wheels + lift).

Procedure (with lerobot interactive prompts):
1. Left arm + head: set the zero pose -> ENTER; move each joint through full range -> ENTER
2. Right arm: set the zero pose -> ENTER; move each joint through full range -> ENTER
3. Automatic: wheels full range + lift stall homing
4. Save the calibration file

Notes:
- Calibrates the follower side (follower: ST3215 C018 both arms + head, wheels, lift), calibration file id="follower"
- The leader side (leader, C046) is out of scope for this script; it is calibrated separately later for teleoperation, with id="leader"
  The two ids generate separate calibration files that do not overwrite each other:
    ~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json  (follower side)
    ~/.cache/huggingface/lerobot/calibration/robots/humanaopen/leader.json    (leader side)
- Cameras are skipped, does not affect calibration
- Zero-pose convention: gravity-hanging joints (shoulder_lift/elbow_flex) naturally hanging down = zero;
  rotation joints (shoulder_pan/forearm_rotation/wrist_yaw) at midpoint; gripper half-open

Usage:
    python3 examples/calibrate_follower.py
"""

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

config = HumanaOpenConfig(
    id="follower",          # Follower-side calibration file name (follower.json); leader side will later use id="leader"
    port1="/dev/ttyACM0",   # Left arm + head
    port2="/dev/ttyACM1",   # Right arm + lift + wheels
    port3=None,             # 2-bus mode
    cameras={},             # Skip cameras
)

print("=" * 55)
print("HumanaOpen follower calibration (arms + head + wheels + lift)")
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

robot = HumanaOpen(config)
try:
    robot.connect(calibrate=True)
    print()
    print("✅ Calibration complete!")
    print("Calibration file:", robot.calibration_fpath)

    # After calibration read one observation frame to verify joint positions are readable (normalized)
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
