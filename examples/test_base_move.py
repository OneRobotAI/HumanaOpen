"""底盘 (差速驱动) 移动测试脚本.

测 4 个基本动作:
1. 前进: 两轮同向正转
2. 后退: 两轮同向反转
3. 左转: 左轮反转 + 右轮正转
4. 右转: 左轮正转 + 右轮反转

说明:
- 用 HumanaLite 类, 走真实 send_action 差速解算链路 (x.vel/theta.vel → 轮子 raw)
- 轮速反馈直接读 bus2 的 Present_Velocity (不需要校准)
- 不读 get_observation() (它会读手臂位置, 未校准时会报错)
- Ctrl+C 紧急停止

安全:
- ⚠️ 强烈建议把机器人架起来 (轮子离地) 再测!
- 若落地测试, 确保前方/周围无障碍物、有足够空间
"""

import time

from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

# 2 总线模式: 左臂+头 / 右臂+升降+轮子
config = HumanaLiteConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,  # 测底盘, 跳过升降归零
)

robot = HumanaLite(config)


def read_wheel_raw() -> dict[str, int]:
    """直接读 bus2 的轮子速度 raw 值 (绕过 get_observation 的校准依赖)."""
    if robot.bus3 is not None:
        bus = robot.bus3
    else:
        bus = robot.bus2
    return bus.sync_read("Present_Velocity", robot.wheel_motors)


def show_wheels(label: str) -> None:
    v = read_wheel_raw()
    print(f"    [{label}] 左轮={v.get('base_left_wheel', 0):>6}  右轮={v.get('base_right_wheel', 0):>6}")


def test_move(label: str, action: dict, duration: float = 2.0) -> None:
    print(f"[{label}] {action}")
    robot.send_action(action)
    time.sleep(duration)
    show_wheels(label)
    robot.send_action({"x.vel": 0.0, "theta.vel": 0.0})
    time.sleep(0.5)
    show_wheels("停 " + label)
    print()


try:
    print("[0] 连接中... (升降会自动归零, 到底即停)")
    robot.connect(calibrate=False)
    print("    连接完成\n")

    # 低速起步, 确认方向正确后再加码
    test_move("前进", {"x.vel": 0.1, "theta.vel": 0.0})
    test_move("后退", {"x.vel": -0.1, "theta.vel": 0.0})
    test_move("左转", {"x.vel": 0.0, "theta.vel": 30.0})
    test_move("右转", {"x.vel": 0.0, "theta.vel": -30.0})

    print("=" * 45)
    print("测试完成。轮速 raw 值方向正确即通过 (前进=两轮同正, 左转=左负右正)。")

except KeyboardInterrupt:
    print("\n⛔ 紧急停止...")
    try:
        robot.send_action({"x.vel": 0.0, "theta.vel": 0.0})
    except Exception:
        pass

finally:
    try:
        robot.disconnect()
    except Exception as e:
        print(f"断开: {e}")
    print("已断开 (轮子已停, 扭矩已释放)")
