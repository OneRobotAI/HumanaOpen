"""Lift + head tilt regression diagnostic — pinpoint two issues in one run.

Issue 1: lift upper limit lost + cannot descend all the way
Issue 2: head tilt has no lower min limit when descending

Diagnostic items:
A. Calibration loading: actual calibration contents of bus1/bus2 (is head_tilt range 1367)
B. Servo EPROM: Min/Max_Position_Limit of ID13 (head tilt) / ID9 (lift)
C. Lift config: actual lift.cfg values (are v_max/kp_vel/home_down_speed the new values)
D. Lift height: get_height_mm() reading + multiturn tracking state
E. Live test: send_action head_tilt -100 → actual servo position

Usage:
    python3 examples/diag_regression.py
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig

robot = HumanaOpen(HumanaOpenConfig(
    id="follower", port1="/dev/ttyACM0", port2="/dev/ttyACM1",
    port3=None, cameras={}, home_lift_on_connect=False,
    wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
))
_orig = builtins.input
builtins.input = lambda *a, **k: ""
try:
    robot.connect(calibrate=False)
except Exception as e:
    print(f"connect warning: {e}")

print("=" * 55)
print("[A] Calibration load (bus1/bus2 calibration keys):")
for bk in ["bus1", "bus2"]:
    bus = getattr(robot, bk, None)
    if bus is None:
        continue
    print(f"  {bk}: {list(bus.calibration.keys()) if bus.calibration else 'empty!'}")

print("\n[B] Servo EPROM position limits:")
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

print("\n[C] Lift config:")
lift = robot.lift_axis
print(f"  v_max={lift.cfg.v_max} kp_vel={lift.cfg.kp_vel} home_down_speed={lift.cfg.home_down_speed}")
print(f"  soft_max={lift.cfg.soft_max_mm}mm descent_floor={lift.cfg.descent_floor_mm}mm")

print("\n[D] Lift height tracking:")
lift._extended_ticks = 0.0
lift._z0_deg = 0.0
try:
    lift._last_tick = float(lift._bus.read("Present_Position", "lift_axis", normalize=False))
except Exception as e:
    print(f"  read pos failed: {str(e)[:60]}")
try:
    h = lift.get_height_mm()
    print(f"  get_height_mm = {h:.1f} mm (after resetting tracking)")
except Exception as e:
    print(f"  get_height_mm exception: {str(e)[:80]}")

print("\n[E] Head tilt live test (read-only + safe range test):")
try:
    obs = robot.get_observation()
    print(f"  current head_tilt.pos = {obs.get('head_tilt.pos', 'N/A')}")
    print(f"  current head_pan.pos  = {obs.get('head_pan.pos', 'N/A')}")
    # send only -50 (when calibration is sane, -50 ↔ raw ~1794, absolutely safe range)
    action = {k: obs[k] for k in obs if k.endswith(".pos")}
    action["head_tilt.pos"] = -50.0
    action["x.vel"] = 0.0
    action["theta.vel"] = 0.0
    action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)
    robot.send_action(action)
    time.sleep(1.0)
    bus1 = robot.bus1
    raw = bus1.read("Present_Position", "head_tilt", normalize=False)
    print(f"  after sending -50, head_tilt raw = {raw} (should be around 1750~1850 when calibration is sane)")
except Exception as e:
    print(f"  live test exception: {str(e)[:80]}")

try:
    robot.bus1.write("Goal_Position", "head_tilt", 2048, normalize=False)
    time.sleep(0.5)
except Exception:
    pass

robot.disconnect()
print("\n✅ Diagnosis complete")
