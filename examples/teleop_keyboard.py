"""Keyboard teleoperation for a locally-connected HumanaOpen.

Keys
----
Movement:   i/k = forward/backward   j/l = rotate left/right
Lift:       u/d = up/down
Speed:      n/m = speed up/down
Quit:       b
"""

import time

import keyboard

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

FPS = 50

def main():
    config = HumanaOpenConfig(port1="/dev/ttyACM0", port2="/dev/ttyACM1")
    robot = HumanaOpen(config)
    robot.connect(calibrate=True)

    speed_levels = [
        {"linear": 0.1, "angular": 30},
        {"linear": 0.2, "angular": 60},
        {"linear": 0.3, "angular": 90},
    ]
    speed_idx = 1

    try:
        while True:
            obs = robot.get_observation()

            # Hold arms at current position
            action = {k: obs[k] for k in obs if k.endswith(".pos")}

            # Base
            speed = speed_levels[speed_idx]
            x, theta = 0.0, 0.0
            if keyboard.is_pressed("i"): x += speed["linear"]
            if keyboard.is_pressed("k"): x -= speed["linear"]
            if keyboard.is_pressed("j"): theta += speed["angular"]
            if keyboard.is_pressed("l"): theta -= speed["angular"]
            action["x.vel"] = x
            action["theta.vel"] = theta

            # Lift
            lift_h = obs.get("lift_axis.height_mm", 0)
            if keyboard.is_pressed("u"): lift_h += 2
            if keyboard.is_pressed("h"): lift_h -= 2
            action["lift_axis.height_mm"] = lift_h

            # Speed
            if keyboard.is_pressed("n"): speed_idx = min(speed_idx + 1, 2)
            if keyboard.is_pressed("m"): speed_idx = max(speed_idx - 1, 0)

            robot.send_action(action)

            if keyboard.is_pressed("b"):
                break

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        pass
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
