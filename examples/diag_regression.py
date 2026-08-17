"""升降 + 头部回归诊断 — 一次性定位两个问题.

问题1: 升降上限位消失 + 降不到底
问题2: 头部下降无最低限位

诊断项:
A. 校准加载: bus1/bus2 的 calibration 实际内容 (head_tilt 范围是否 1367)
B. 舵机 EPROM: ID13 (头部) / ID9 (升降) 的 Min/Max_Position_Limit
C. 升降配置: lift.cfg 实际值 (v_max/kp_vel/home_down_speed 是否新值)
D. 升降高度: get_height_mm() 读数 + 多圈跟踪状态
E. 实测: send_action 头部 -100 → 舵机实际位置

用法:
    python3 examples/diag_regression.py
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaLite")
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

robot = HumanaLite(HumanaLiteConfig(
    id="follower", port1="/dev/ttyACM0", port2="/dev/ttyACM1",
    port3=None, cameras={}, home_lift_on_connect=False,
    wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
))
_orig = builtins.input
builtins.input = lambda *a, **k: ""
try:
    robot.connect(calibrate=False)
except Exception as e:
    print(f"connect 警告: {e}")

print("=" * 55)
print("[A] 校准加载 (bus1/bus2 calibration keys):")
for bk in ["bus1", "bus2"]:
    bus = getattr(robot, bk, None)
    if bus is None:
        continue
    print(f"  {bk}: {list(bus.calibration.keys()) if bus.calibration else '空!'}")

print("\n[B] 舵机 EPROM 位置限制:")
for bk, mid, label in [("bus1", 13, "head_tilt"), ("bus2", 9, "lift")]:
    bus = getattr(robot, bk, None)
    if bus is None:
        continue
    try:
        vmin = bus._read(9, 2, mid, raise_on_error=True)[0]
        vmax = bus._read(11, 2, mid, raise_on_error=True)[0]
        print(f"  {label} (ID{mid}): Min={vmin} Max={vmax}")
    except Exception as e:
        print(f"  {label}: {str(e)[:60]}")

print("\n[C] 升降配置:")
lift = robot.lift_axis
print(f"  v_max={lift.cfg.v_max} kp_vel={lift.cfg.kp_vel} home_down_speed={lift.cfg.home_down_speed}")
print(f"  soft_max={lift.cfg.soft_max_mm}mm descent_floor={lift.cfg.descent_floor_mm}mm")

print("\n[D] 升降高度跟踪:")
lift._extended_ticks = 0.0
lift._z0_deg = 0.0
try:
    lift._last_tick = float(lift._bus.read("Present_Position", "lift_axis", normalize=False))
except Exception as e:
    print(f"  read pos 失败: {str(e)[:60]}")
try:
    h = lift.get_height_mm()
    print(f"  get_height_mm = {h:.1f} mm (重置跟踪后)")
except Exception as e:
    print(f"  get_height_mm 异常: {str(e)[:80]}")

print("\n[E] 头部实测 (只读 + 安全范围测试):")
try:
    obs = robot.get_observation()
    print(f"  当前 head_tilt.pos = {obs.get('head_tilt.pos', 'N/A')}")
    print(f"  当前 head_pan.pos  = {obs.get('head_pan.pos', 'N/A')}")
    # 只发 -50 (校准正常时 -50 ↔ raw ~1794, 绝对安全范围)
    action = {k: obs[k] for k in obs if k.endswith(".pos")}
    action["head_tilt.pos"] = -50.0
    action["x.vel"] = 0.0
    action["theta.vel"] = 0.0
    action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)
    robot.send_action(action)
    time.sleep(1.0)
    bus1 = robot.bus1
    raw = bus1.read("Present_Position", "head_tilt", normalize=False)
    print(f"  发送 -50 后 head_tilt raw = {raw} (校准正常时应在 1750~1850 附近)")
except Exception as e:
    print(f"  实测异常: {str(e)[:80]}")

try:
    robot.bus1.write("Goal_Position", "head_tilt", 2048, normalize=False)
    time.sleep(0.5)
except Exception:
    pass

robot.disconnect()
print("\n✅ 诊断完成")
