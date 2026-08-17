"""底盘 (差速驱动) 键盘手动控制测试.

只控制底盘, 不碰手臂和升降:
- 不读 get_observation() (无需校准)
- 不触发升降归零 (home_lift_on_connect=False)
- send_action 只发 x.vel/theta.vel, 手臂/升降完全不动

键位
----
i/k : 前进 / 后退
j/l : 左转 / 右转
n/m : 加速档 / 减速档
b   : 退出

说明:
- 使用 pynput 库 (桌面环境无需 root), 需有 X11 显示 (DISPLAY 已设置)
- 替代方案: keyboard 库需要 root 权限

安全:
- ⚠️ 建议架起机器人 (轮子离地) 测试
- 落地测试确保周围无障碍物
"""

import time
import threading

from pynput import keyboard

from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

FPS = 30

speed_levels = [
    {"linear": 0.05, "angular": 15},
    {"linear": 0.10, "angular": 30},
    {"linear": 0.20, "angular": 60},
]


class KeyState:
    """线程安全地记录哪些键当前被按住."""

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
    config = HumanaLiteConfig(
        port1="/dev/ttyACM0",
        port2="/dev/ttyACM1",
        port3=None,
        cameras={},
        home_lift_on_connect=False,  # 跳过升降归零
        # 左轮装反 → 取反使两轮同向 (万向轮卡住曾干扰判断)
        wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
    )
    robot = HumanaLite(config)
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
