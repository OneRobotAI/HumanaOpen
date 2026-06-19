"""Single-machine operation: all buses + cameras on one computer."""

import time

from openarmsx import OpenArmsX, OpenArmsXConfig

# ── 3-bus mode (default) ──────────────────────────────────────
config = OpenArmsXConfig(
    port1="/dev/ttyACM0",   # left arm (1-8) + head (12,13)
    port2="/dev/ttyACM1",   # right arm (1-8)
    port3="/dev/ttyACM2",   # lift (9) + wheels (10,11)
)

# ── 2-bus mode (uncomment) ────────────────────────────────────
# config = OpenArmsXConfig(
#     port1="/dev/ttyACM0",
#     port2="/dev/ttyACM1",
#     port3=None,           # wheels & lift merge into bus 2
# )

robot = OpenArmsX(config)

try:
    robot.connect(calibrate=True)

    print(f"Observation keys: {list(robot.observation_features.keys())}")
    print(f"Action keys:      {list(robot.action_features.keys())}")

    # Hold current position for 5 seconds
    for _ in range(100):
        obs = robot.get_observation()

        # Build a hold-still action from current positions
        action = {k: obs[k] for k in obs if k.endswith(".pos")}
        action["x.vel"] = 0.0
        action["theta.vel"] = 0.0
        action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)

        robot.send_action(action)
        time.sleep(0.05)

finally:
    robot.disconnect()
