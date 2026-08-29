"""Chassis (differential drive) manual keyboard control test.

Only controls the chassis, does not touch the arms or lift:
- Does not read get_observation() (no calibration needed)
- Does not trigger lift homing (home_lift_on_connect=False)
- send_action only sends x.vel/theta.vel; arms/lift stay completely still

Key bindings
----
i/k : forward / backward
j/l : turn left / turn right
n/m : speed up / slow down
b   : quit

Notes:
- Uses the pynput library (no root needed on a desktop environment), requires an X11 display (DISPLAY set)
- Alternative: the keyboard library needs root privileges

Safety:
- ⚠️ Recommended to test with the robot propped up (wheels off the ground)
- For floor tests make sure there are no obstacles around
"""

import time
import threading

from pynput import keyboard

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

FPS = 30

speed_levels = [
    {"linear": 0.05, "angular": 15},
    {"linear": 0.10, "angular": 30},
    {"linear": 0.20, "angular": 60},
]


class KeyState:
    """Thread-safely records which keys are currently held down."""

    def __init__(self):
        self._pressed: set[str] = set()
        self._lock = threading.Lock()

    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            return
        if char is not None:
            with self._lock:
                self._pressed.add(char)

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            return
        if char is not None:
            with self._lock:
                self._pressed.discard(char)

    def is_down(self, char: str) -> bool:
        with self._lock:
            return char in self._pressed


def main():
    config = HumanaOpenConfig(
        port1="/dev/ttyACM0",
        port2="/dev/ttyACM1",
        port3=None,
        cameras={},
        home_lift_on_connect=False,  # Skip lift homing
        # Left wheel mounted reversed -> negate so both wheels turn the same way (a stuck caster wheel previously interfered with judgment)
        wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
    )
    robot = HumanaOpen(config)
    robot.connect(calibrate=False)

    keys = KeyState()
    listener = keyboard.Listener(on_press=keys.on_press, on_release=keys.on_release)
    listener.start()

    speed_idx = 1

    try:
        print("底盘键盘控制开始。键位: i/k 前后, j/l 转向, n/m 速度, b 退出")
        print("按住按键连续移动, 松开即停。")
        while True:
            speed = speed_levels[speed_idx]
            x, theta = 0.0, 0.0
            if keys.is_down("i"):
                x += speed["linear"]
            if keys.is_down("k"):
                x -= speed["linear"]
            if keys.is_down("j"):
                theta += speed["angular"]
            if keys.is_down("l"):
                theta -= speed["angular"]
            if keys.is_down("n"):
                speed_idx = min(speed_idx + 1, len(speed_levels) - 1)
            if keys.is_down("m"):
                speed_idx = max(speed_idx - 1, 0)

            robot.send_action({"x.vel": x, "theta.vel": theta})

            if keys.is_down("b"):
                break

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        pass
    finally:
        try:
            robot.send_action({"x.vel": 0.0, "theta.vel": 0.0})
        except Exception:
            pass
        robot.disconnect()
        listener.stop()
        print("\n已退出, 轮子已停")


if __name__ == "__main__":
    main()
