"""Base (differential drive) movement test script.

Tests 4 basic motions:
1. Forward: both wheels rotate forward at the same speed
2. Backward: both wheels rotate backward at the same speed
3. Turn left: left wheel reverses + right wheel drives forward
4. Turn right: left wheel drives forward + right wheel reverses

Notes:
- Uses the HumanaOpen class and goes through the real send_action differential-solve chain (x.vel/theta.vel → raw wheel values)
- Wheel-speed feedback reads Present_Velocity directly from bus2 (no calibration needed)
- Does not call get_observation() (it reads arm positions and errors out when uncalibrated)
- Ctrl+C for emergency stop

Safety:
- ⚠️ Strongly recommended to prop the robot up (wheels off the ground) before testing!
- If testing on the ground, make sure there are no obstacles in front/around and enough space
"""

import time

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

# 2-bus mode: left arm + head / right arm + lift + wheels
config = HumanaOpenConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,  # testing the base; skip lift homing
)

robot = HumanaOpen(config)


def read_wheel_raw() -> dict[str, int]:
    """Read the raw wheel-speed values directly from bus2 (bypassing get_observation's calibration dependency)."""
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

    # start at low speed; ramp up only after confirming the directions are correct
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
