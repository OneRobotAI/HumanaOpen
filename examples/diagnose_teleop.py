"""Teleop joint-direction diagnosis script — measures the leader→follower mapping joint by joint.

Usage:
    python3 examples/diagnose_teleop.py

Principle:
    Test each joint using the raw "no-flip, no-remap" mapping:
    - you manually rotate one joint of the leader arm in a direction
    - the script records that joint's reading change on the leader, Δ_leader
    - simultaneously sends the action to the follower
    - records the reading changes of each follower joint
    - determines: which follower joint moved (mapping) and whether the directions match (whether a flip is needed)

After diagnosis, configure from the output:
    flip_joints:  joints with the opposite direction → add to that side's flip table
    joint_remap:  misaligned mapping (a different follower joint moved) → set up a remap

Preparation:
    1. Both leader and follower calibrated (follower zeroed with arms hanging naturally + gripper closed)
    2. Follower powered at 12V, leader at 7.4V
    3. Make sure there are no obstacles around; follower arms will move
"""

import time

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
from lerobot_robot_humanaopen.leader import (
    BiHumanaOpenLeader,
    BiHumanaOpenLeaderConfig,
    JOINT_NAMES,
)

follower_cfg = HumanaOpenConfig(
    id="follower",
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,
)

# diagnosis mode: no flipping, no remapping; use the raw 1:1 mapping
leader_cfg = BiHumanaOpenLeaderConfig(
    id="leader",
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
    # not passing flip_joints / joint_remap → defaults to the official tables; diagnosis needs the raw mapping, see the construction below
)

follower = HumanaOpen(follower_cfg)
# manually construct the leader: use an empty flip table and empty remap
leader_left = BiHumanaOpenLeader(leader_cfg)
# force the raw mapping: clear flips and remaps
for arm in (leader_left.left_arm, leader_left.right_arm):
    arm._motors_to_flip = []
    arm._joint_remap = {}

SIDES = [("left", "left_arm"), ("right", "right_arm")]

# suggested "positive direction" motion per joint (for the operator's reference)
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

            # record the leader's and follower's initial readings
            # leader reading: read directly
            la = leader_left.left_arm if side == "left" else leader_left.right_arm
            l0 = la.get_action().get(f"{joint}.pos", 0.0)
            # follower reading
            obs0 = follower.get_observation()
            f0 = obs0.get(action_key, 0.0)

            input("  Now move the leader joint (hold it), then press ENTER...")

            # read leader action (full dual-arm, raw mapping) → send to the follower
            action = leader_left.get_action()
            # keep the follower's non-arm parts still (hold the head, stop wheels/lift)
            obs_static = follower.get_observation()
            for k, v in obs_static.items():
                if k.startswith("head_") and k.endswith(".pos"):
                    action[k] = v
            action["x.vel"] = 0.0
            action["theta.vel"] = 0.0
            action["lift_axis.height_mm"] = obs_static.get("lift_axis.height_mm", 0)
            follower.send_action(action)

            # wait for the follower motors to catch up (speed is capped by max_relative_target; allow enough time)
            time.sleep(0.5)

            l1 = la.get_action().get(f"{joint}.pos", 0.0)
            obs1 = follower.get_observation()
            f1 = obs1.get(action_key, 0.0)

            d_leader = l1 - l0
            d_follower = f1 - f0

            # also report whether any other follower joint moved noticeably (misalignment detection)
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
