"""Wheel direction precision check — drive one wheel at a time to determine the physical rotation direction of each wheel.

Usage:
    python3 examples/diag_wheel_direction.py --remote_ip=192.168.1.100

Keys:
    a  = send only left wheel +3000 (right wheel untouched)
    d  = send only right wheel +3000 (left wheel untouched)
    1  = x.vel=+10 (straight driving test)
    2  = theta.vel=+30 (turning test)
    q  = quit

Observe the actual rotation direction of each wheel to identify mirror-installed wheels and the correct signs.
"""

import sys
import time

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot_robot_humanaopen.humanaopen_client import HumanaOpenClient, HumanaOpenClientConfig
from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenClientConfig

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--remote_ip", default="127.0.0.1")
args = parser.parse_args()

cfg = HumanaOpenClientConfig(remote_ip=args.remote_ip, port_zmq_cmd=5555, port_zmq_observations=5556)
client = HumanaOpenClient(cfg)
client.connect()
print(f"已连接 {args.remote_ip}")
print("按键:")
print("  a = 左轮 +3000")
print("  d = 右轮 +3000")
print("  1 = x.vel=+10 (直行)")
print("  2 = theta.vel=+30 (转向)")
print("  3 = x.vel=-10")
print("  4 = theta.vel=-30")
print("  q = 退出")

from pynput import keyboard as kb
_pressed = {}
def on_press(key):
    try:
        if key.char: _pressed[key.char] = True
    except: pass
def on_release(key):
    try:
        if key.char: _pressed.pop(key.char, None)
    except: pass
kb.Listener(on_press=on_press, on_release=on_release).start()

def send_and_hold(label, action, hold=1.0):
    client.send_action(action)
    print(f"  → {label} (观察轮子)")
    time.sleep(hold)
    client.send_action({"x.vel": 0.0, "theta.vel": 0.0,
                        "base_left_wheel": 0, "base_right_wheel": 0})
    time.sleep(0.3)

try:
    while True:
        if "q" in _pressed: break
        if "a" in _pressed:
            send_and_hold("左轮 +3000 (不碰右轮)", {"base_left_wheel": 3000, "base_right_wheel": 0}); _pressed.pop("a", None)
        elif "d" in _pressed:
            send_and_hold("右轮 +3000 (不碰左轮)", {"base_left_wheel": 0, "base_right_wheel": 3000}); _pressed.pop("d", None)
        elif "1" in _pressed:
            send_and_hold("x.vel=+10 (应直行)", {"x.vel": 10.0, "theta.vel": 0.0}); _pressed.pop("1", None)
        elif "2" in _pressed:
            send_and_hold("theta.vel=+30 (应转向)", {"x.vel": 0.0, "theta.vel": 30.0}); _pressed.pop("2", None)
        elif "3" in _pressed:
            send_and_hold("x.vel=-10", {"x.vel": -10.0, "theta.vel": 0.0}); _pressed.pop("3", None)
        elif "4" in _pressed:
            send_and_hold("theta.vel=-30", {"x.vel": 0.0, "theta.vel": -30.0}); _pressed.pop("4", None)
        else:
            client.send_action({"x.vel": 0.0, "theta.vel": 0.0})
            time.sleep(0.05)
finally:
    client.send_action({"x.vel": 0.0, "theta.vel": 0.0})
    client.disconnect()
    print("Done")
