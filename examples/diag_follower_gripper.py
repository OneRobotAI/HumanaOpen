"""Follower-arm gripper reading diagnostics — read the raw encoder value directly to confirm whether the reading changes with physical motion.

Note: after connecting, first release the gripper torque (otherwise the follower-arm gripper locks and cannot be pried open).

Usage:
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
    # Release torque on both arm grippers (to prevent the opposite side from locking)
    for name in ("left_arm_gripper", "right_arm_gripper"):
        bus = robot.bus1 if name.startswith("left") else robot.bus2
        print(f"Releasing {name} torque...")
        bus.write("Torque_Enable", name, 0)
    time.sleep(0.3)

    bus = robot.bus1 if side == "left" else robot.bus2
    print(f"Follower arm {side} connected, gripper: {gripper_name}")
    print("Manually open/close the follower-arm gripper and watch the reading change (Ctrl+C to exit)")
    print("=" * 55)
    print(f"{'Raw encoder':>10} | {'Normalized(0-100)':>14}")
    print("-" * 55)

    while True:
        raw = bus.read("Present_Position", gripper_name, normalize=False)
        norm = bus.read("Present_Position", gripper_name)
        print(f"{raw:>10} | {norm:>14.1f}")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nExiting")

finally:
    robot.disconnect()
