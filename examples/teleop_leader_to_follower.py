"""全身遥操: 主臂 (leader) 控双臂 + 键盘控头部/底盘/升降.

控制分配:
- 主臂: 双臂 (left_arm_*/right_arm_*) 实时跟随
- 键盘 (pynput, 按住移动松开停):
    头部:   w/s = 点头 (上下), a/d = 摇头 (左右)
    底盘:   i/k = 前进/后退, j/l = 左转/右转, n/m = 加速/减速 (3 档)
    升降:   u/h = 升/降 (钳位在 3~200mm)
    b      = 退出

摄像头 (参数控制):
    默认加载 3 个: head + left_wrist + right_wrist
    --no-cameras               跳过所有摄像头 (纯遥操)
    --cameras=head,left_wrist  只加载指定摄像头 (逗号分隔)
    --head-camera /dev/video0  覆盖 head 设备号 (同理 --left-wrist-camera/--right-wrist-camera)
    --chest-camera /dev/video6 额外加载胸口摄像头 (最多 4 个)

说明:
- 从臂头部/底盘/升降通过键盘控制, 其余时间保持当前姿态
- 主臂读数方向与从臂天然一致 (diagnose_teleop 实测), 禁用官方翻转表

用法:
    python3 examples/teleop_leader_to_follower.py
    python3 examples/teleop_leader_to_follower.py --no-cameras
    python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

安全:
- ⚠️ 从臂全身会动, 确保周围无障碍物
- 底盘移动前建议架起机器人
- Ctrl+C 停止
"""

import argparse
import threading
import time

from pynput import keyboard

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

FPS = 30

# 键盘控制速率 (单位/秒)
HEAD_PAN_SPEED = 20.0     # 头部 pan (归一化单位/s)
HEAD_TILT_SPEED = 20.0    # 头部 tilt
BASE_LINEAR_SPEED = 0.2   # 底盘线速度 m/s (基础档, ×档位倍率)
BASE_ANGULAR_SPEED = 30.0  # 底盘角速度 deg/s (基础档, ×档位倍率)
BASE_SPEED_LEVELS = [0.3, 0.6, 1.0]  # 底盘速度档位倍率 (n/m 切换)
LIFT_SPEED_MM = 15.0      # 升降 mm/s
LIFT_MIN_MM = 3.0         # 升降软下限 (descent_floor 硬保护 3mm)
LIFT_MAX_MM = 200.0       # 升降软上限 (200mm, 用户指定)

CAMERA_FPS = 30
CAMERA_W, CAMERA_H = 640, 480
CAMERA_FOURCC = "MJPG"  # 压缩格式, 带宽小, 多数摄像头可跑满 30fps (YUYV 裸流只有 25)

# 默认 3 摄像头设备号 (插好后用 lerobot-find-cameras 确认, 可用参数覆盖)
DEFAULT_CAM_DEVICES = {
    "head": "/dev/video0",
    "left_wrist": "/dev/video2",
    "right_wrist": "/dev/video4",
}

# 各摄像头实际支持的 fps (v4l2-ctl 实测: video4 在 640x480 下 MJPG 最大 25fps, 其余 30)
CAMERA_FPS_MAP = {"head": 30, "left_wrist": 30, "right_wrist": 25, "chest": 30}


def build_cameras(args) -> dict[str, OpenCVCameraConfig]:
    """按参数构建摄像头 dict. --no-cameras 或 --cameras 为空 → 返回空 dict."""
    if args.no_cameras or not args.cameras:
        return {}
    cams = {}
    # 若显式传了某摄像头设备号, 即使不在 --cameras 列表也自动加入
    names = [n.strip() for n in args.cameras.split(",") if n.strip()]
    for n in ("head", "left_wrist", "right_wrist", "chest"):
        if getattr(args, f"{n}_camera") and n not in names:
            names.append(n)
    for name in names:
        dev = getattr(args, f"{name}_camera") or DEFAULT_CAM_DEVICES.get(name)
        if dev is None:
            print(f"  ⚠️ Unknown camera name '{name}', skipped (available: head/left_wrist/right_wrist/chest)")
            continue
        cams[name] = OpenCVCameraConfig(
            index_or_path=dev,
            fps=CAMERA_FPS_MAP.get(name, CAMERA_FPS),
            width=CAMERA_W,
            height=CAMERA_H,
            fourcc=CAMERA_FOURCC,
        )
        print(f"  📷 {name}: {dev} @{cams[name].fps}fps {CAMERA_FOURCC}")
    return cams


class KeyState:
    """线程安全地记录哪些键当前被按住."""

    def __init__(self):
        self._pressed: set[str] = set()
        self._consumed: set[str] = set()
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

    def pressed_once(self, char: str) -> bool:
        """True only on the rising edge of a key (False→True transition).

        Based on is_down state, not on_press events — OS key-repeat sends
        repeated press events while held, which would otherwise re-trigger.
        """
        with self._lock:
            down = char in self._pressed
            was = char in self._consumed  # _consumed doubles as "was pressed"
            if down:
                self._consumed.add(char)
            else:
                self._consumed.discard(char)
            return down and not was


def main():
    parser = argparse.ArgumentParser(description="HumanaOpen 全身遥操 (主臂 + 键盘)")
    parser.add_argument("--no-cameras", action="store_true", help="跳过所有摄像头 (纯遥操)")
    parser.add_argument(
        "--cameras",
        default="head,left_wrist,right_wrist",
        help="要加载的摄像头名, 逗号分隔 (head/left_wrist/right_wrist/chest)",
    )
    for name in ("head", "left_wrist", "right_wrist", "chest"):
        parser.add_argument(
            f"--{name}-camera",
            default=None,
            help=f"{name} 摄像头设备号 (默认 {DEFAULT_CAM_DEVICES.get(name, '未定义')})",
        )
    parser.add_argument("--display", action="store_true", help="用 rerun 实时显示摄像头画面和关节状态")
    args = parser.parse_args()

    cams = build_cameras(args)
    follower_cfg = HumanaOpenConfig(
        id="follower",
        port1="/dev/ttyACM0",
        port2="/dev/ttyACM1",
        port3=None,
        cameras=cams,
        # 升降: connect 时优先恢复持久化位置 (免归零), 失败才自动归零.
        # 默认 zero_file 已启用, 无需显式指定.
        # 现象: i(前进指令) 变左转 → 两轮反向 → 单轮装反
        # 左轮取反使两轮同向; 万向轮卡住曾干扰判断, 现已修复
        wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
    )
    leader_cfg = BiHumanaOpenLeaderConfig(
        id="leader",
        left_arm_port="/dev/ttyACM2",
        right_arm_port="/dev/ttyACM3",
        # 主从臂方向天然一致, 禁用官方默认翻转表.
        flip_joints={"left": [], "right": []},
        joint_remap={},
    )

    follower = HumanaOpen(follower_cfg)
    leader = BiHumanaOpenLeader(leader_cfg)

    keys = KeyState()
    listener = keyboard.Listener(on_press=keys.on_press, on_release=keys.on_release)
    listener.start()

    try:
        print("[1] Connecting follower...")
        follower.connect(calibrate=False)
        # connect 内已处理: 优先恢复持久化位置 (免归零), 失败才自动归零
        print(f"    Follower connected (cameras: {list(cams.keys()) or 'none'}, lift {follower.lift_axis.get_height_mm():.1f}mm)")

        print("[2] Connecting leader...")
        leader.connect(calibrate=False)
        print("    Leader connected")

        obs = follower.get_observation()

        # rerun 实时可视化 (摄像头画面 + 关节状态), 可选
        if args.display:
            try:
                from lerobot.utils.visualization_utils import init_rerun, log_rerun_data
                init_rerun(session_name="humanaopen_teleop")
                log_rerun_data(observation=obs)
                print("  👁 Rerun visualization started (view in rerun viewer)")
            except Exception as e:
                print(f"  ⚠️ Rerun startup failed (ignored): {str(e)[:60]}")

        print()
        print("=" * 60)
        print("Teleoperation started!")
        print("  Arms:   leader follows")
        print("  Head:   w/s = nod (up/down), a/d = shake (left/right)")
        print("  Base:   i/k = forward/back, j/l = turn, n/m = speed (0.3x/0.6x/1.0x)")
        print("  Lift:   u/h = up/down (clamped 3~200mm)")
        print("  Quit:   b or Ctrl+C")
        print("=" * 60)
        print()

        # 初始化头部位置 + 从校准文件读取头部限位 (校准时录的 MIN/MAX)
        head_pan = obs.get("head_pan.pos", 0.0)
        head_tilt = obs.get("head_tilt.pos", 0.0)
        cal = follower.calibration
        head_pan_lim = (cal["head_pan"].range_min, cal["head_pan"].range_max)
        head_tilt_lim = (cal["head_tilt"].range_min, cal["head_tilt"].range_max)
        # 归一化空间: use_degrees=False → RANGE_M100_100, 限位就是 ±100
        # (obs 值域 [-100,100] 线性映射到校准 range 两端, 见 motors_bus._normalize)
        head_pan_min, head_pan_max = -100.0, 100.0
        head_tilt_min, head_tilt_max = -100.0, 100.0
        print(f"  Head limits: pan range {head_pan_lim}, tilt range {head_tilt_lim} (normalized ±100)")
        lift_h = obs.get("lift_axis.height_mm", 0.0)
        speed_idx = 1  # 底盘速度档位 (1 = 基础)
        _last_lift_print = 0.0  # 升降状态显示节流
        _last_display = 0.0  # rerun 日志节流
        _rerun = args.display  # rerun 是否启用

        while True:
            # 主臂读数 → 双臂动作
            action = leader.get_action()

            # 键盘 → 头部 (WASD 标准语义: w/s=点头, a/d=摇头)
            # head_pan(ID12)=摇头, head_tilt(ID13)=点头 (物理已按此烧录)
            if keys.is_down("w"):
                head_tilt -= HEAD_TILT_SPEED / FPS
            if keys.is_down("s"):
                head_tilt += HEAD_TILT_SPEED / FPS
            if keys.is_down("a"):
                head_pan -= HEAD_PAN_SPEED / FPS
            if keys.is_down("d"):
                head_pan += HEAD_PAN_SPEED / FPS
            head_pan = max(head_pan_min, min(head_pan_max, head_pan))
            head_tilt = max(head_tilt_min, min(head_tilt_max, head_tilt))
            action["head_pan.pos"] = head_pan
            action["head_tilt.pos"] = head_tilt

            # 键盘 → 底盘 (速度档位: 按一下 n/m 切换一档, 边沿触发)
            if keys.pressed_once("n"):
                speed_idx = min(speed_idx + 1, len(BASE_SPEED_LEVELS) - 1)
                print(f"  [Speed level {speed_idx+1}/{len(BASE_SPEED_LEVELS)}: {BASE_SPEED_LEVELS[speed_idx]}x]")
            if keys.pressed_once("m"):
                speed_idx = max(speed_idx - 1, 0)
                print(f"  [Speed level {speed_idx+1}/{len(BASE_SPEED_LEVELS)}: {BASE_SPEED_LEVELS[speed_idx]}x]")
            scale = BASE_SPEED_LEVELS[speed_idx]
            x, theta = 0.0, 0.0
            if keys.is_down("i"):
                x += BASE_LINEAR_SPEED * scale
            if keys.is_down("k"):
                x -= BASE_LINEAR_SPEED * scale
            if keys.is_down("j"):
                theta += BASE_ANGULAR_SPEED * scale
            if keys.is_down("l"):
                theta -= BASE_ANGULAR_SPEED * scale
            action["x.vel"] = x
            action["theta.vel"] = theta

            # 键盘 → 升降: 按住 u/h 时目标递增, 松开保持
            # 按下瞬间记录初始高度, 之后在初始值上累加 (不回读实际高度,
            # 否则慢速 P 控制器追赶会把目标拉回实际值, 导致几乎不动)
            if keys.pressed_once("u") or keys.pressed_once("h"):
                try:
                    lift_h = follower.lift_axis.get_height_mm()
                except Exception:
                    pass
            if keys.is_down("u"):
                lift_h += LIFT_SPEED_MM / FPS
            elif keys.is_down("h"):
                lift_h -= LIFT_SPEED_MM / FPS
            lift_h = max(LIFT_MIN_MM, min(LIFT_MAX_MM, lift_h))
            action["lift_axis.height_mm"] = lift_h

            # 实时显示升降状态 (每0.5秒刷一次)
            if time.time() - _last_lift_print > 0.5:
                _last_lift_print = time.time()
                _actual_h = follower.lift_axis.get_height_mm()
                _lim = "▲MAX" if _actual_h >= LIFT_MAX_MM else ("▼MIN" if _actual_h <= LIFT_MIN_MM else "")
                print(f"\rLift: actual={_actual_h:6.1f}mm  target={lift_h:6.1f}mm  limits[{LIFT_MIN_MM:.0f}~{LIFT_MAX_MM:.0f}]  {_lim}", end="", flush=True)

            follower.send_action(action)

            # rerun 日志 (5Hz, 避免拖慢 30FPS 控制循环)
            if _rerun and time.time() - _last_display > 0.2:
                _last_display = time.time()
                try:
                    log_rerun_data(observation=follower.get_observation(), action=action)
                except Exception:
                    pass

            if keys.is_down("b"):
                print("\nQuitting...")
                break

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        print("\n⛔ Teleoperation stopped...")

    finally:
        # 保存升降绝对位置 (下次连接免归零)
        try:
            follower.lift_axis.save_zero()
        except Exception:
            pass
        if args.display:
            try:
                import rerun as rr
                rr.rerun_shutdown()
            except Exception:
                pass
        try:
            leader.disconnect()
        except Exception:
            pass
        try:
            follower.disconnect()
        except Exception:
            pass
        try:
            listener.stop()
        except Exception:
            pass
        print("Disconnected")


if __name__ == "__main__":
    main()
