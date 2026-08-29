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
print(f"Connected {args.remote_ip}")
print("Keys:")
print("  a = left wheel +3000")
print("  d = right wheel +3000")
print("  1 = x.vel=+10 (straight)")
print("  2 = theta.vel=+30 (turn)")
print("  3 = x.vel=-10")
print("  4 = theta.vel=-30")
print("  q = quit")

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
    print(f"  → {label} (observe the wheel)")
    time.sleep(hold)
    client.send_action({"x.vel": 0.0, "theta.vel": 0.0,
                        "base_left_wheel": 0, "base_right_wheel": 0})
    time.sleep(0.3)

try:
    while True:
        if "q" in _pressed: break
        if "a" in _pressed:
            send_and_hold("left wheel +3000 (right wheel untouched)", {"base_left_wheel": 3000, "base_right_wheel": 0}); _pressed.pop("a", None)
        elif "d" in _pressed:
            send_and_hold("right wheel +3000 (left wheel untouched)", {"base_left_wheel": 0, "base_right_wheel": 3000}); _pressed.pop("d", None)
        elif "1" in _pressed:
            send_and_hold("x.vel=+10 (should drive straight)", {"x.vel": 10.0, "theta.vel": 0.0}); _pressed.pop("1", None)
        elif "2" in _pressed:
            send_and_hold("theta.vel=+30 (should turn)", {"x.vel": 0.0, "theta.vel": 30.0}); _pressed.pop("2", None)
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
