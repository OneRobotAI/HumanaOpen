"""诊断双机模式轮子方向 — 找出正确的 wheel_dir_signs.

用法:
    1. Host 在 Jetson 运行 (HumanaOpenHost)
    2. 本脚本从 Client 端发送不同的 x.vel/theta.vel, 观察轮子实际转向
    3. 根据结果确定 wheel_dir_signs

按压序列:
    按 1: x.vel=+10  (期望直行前进, 两轮都正转)
    按 2: theta.vel=+30 (期望左转)
    按 q: 退出
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
print("命令:")
print("  1 = x.vel=+10 (直行)")
print("  2 = theta.vel=+30 (转)")
print("  3 = x.vel=-10 (后退)")
print("  4 = theta.vel=-30 (反转)")
print("  q = 退出, 每次后先观察轮子再按 next")

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

try:
    while True:
        if "q" in _pressed: break
        if "1" in _pressed:
            client.send_action({"x.vel": 10.0, "theta.vel": 0.0})
            print("发送: x.vel=10 → 应直行前进 (观察两轮)")
            time.sleep(1); _pressed.pop("1", None)
        elif "2" in _pressed:
            client.send_action({"x.vel": 0.0, "theta.vel": 30.0})
            print("发送: theta.vel=30 → 应左转 (观察)")
            time.sleep(1); _pressed.pop("2", None)
        elif "3" in _pressed:
            client.send_action({"x.vel": -10.0, "theta.vel": 0.0})
            print("发送: x.vel=-10 → 应后退")
            time.sleep(1); _pressed.pop("3", None)
        elif "4" in _pressed:
            client.send_action({"x.vel": 0.0, "theta.vel": -30.0})
            print("发送: theta.vel=-30 → 应右转")
            time.sleep(1); _pressed.pop("4", None)
        else:
            client.send_action({"x.vel": 0.0, "theta.vel": 0.0})
            time.sleep(0.05)
finally:
    client.send_action({"x.vel": 0.0, "theta.vel": 0.0})
    client.disconnect()
    print("Done")
