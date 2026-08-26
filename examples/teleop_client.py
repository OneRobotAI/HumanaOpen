"""Keyboard teleoperation via ZMQ client (dual-machine).

Host: Jetson/RPi (runs HumanaOpenHost)
Client: GPU machine (runs this script, controls robot remotely)

Usage:
    # 1. On Jetson/RPi: start Host
    python3 -c "
    from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
    from lerobot_robot_humanaopen import HumanaOpenConfig
    HumanaOpenHost(HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})).run()
    "

    # 2. On PC: run teleop
    python3 examples/teleop_client.py --remote_ip=192.168.1.100

Controls: i/k=fwd/back, j/l=turn, u/h=lift, w/s=head, q=quit
"""

import argparse
import sys
import time

sys.path.insert(0, "/home/zach/HumanaOpen")

from lerobot.utils.import_utils import register_third_party_plugins
register_third_party_plugins()

from lerobot_robot_humanaopen.humanaopen_client import HumanaOpenClient
from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenClientConfig


def main():
    parser = argparse.ArgumentParser(description="Keyboard teleop via ZMQ (dual-machine)")
    parser.add_argument("--remote_ip", default="127.0.0.1")
    parser.add_argument("--port_zmq_cmd", type=int, default=5555)
    parser.add_argument("--port_zmq_obs", type=int, default=5556)
    parser.add_argument("--teleop.left_arm_port", default="/dev/ttyACM2")
    parser.add_argument("--teleop.right_arm_port", default="/dev/ttyACM3")
    parser.add_argument("--teleop.flip_joints", default='{"left": [], "right": []}')
    parser.add_argument("--teleop.joint_remap", default="{}")
    args = parser.parse_args()
    d = vars(args)

    from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

    print("=" * 60)
    print("HumanaOpen Keyboard Teleop (dual-machine)")
    print(f"  Host: {d['remote_ip']}:{d['port_zmq_obs']}")
    print("  Keys: i/k=fwd/back, j/l=turn, u/h=lift, w/s=head, q=quit")
    print("=" * 60)

    # Connect to Host
    client_config = HumanaOpenClientConfig(
        remote_ip=d["remote_ip"],
        port_zmq_cmd=d["port_zmq_cmd"],
        port_zmq_observations=d["port_zmq_obs"],
    )
    client = HumanaOpenClient(client_config)
    client.connect()

    # Connect leader
    leader = BiHumanaOpenLeader(BiHumanaOpenLeaderConfig(
        id="leader",
        left_arm_port=d["teleop.left_arm_port"],
        right_arm_port=d["teleop.right_arm_port"],
        flip_joints=json.loads(d["teleop.flip_joints"]),
        joint_remap=json.loads(d["teleop.joint_remap"]),
    ))
    leader.connect(calibrate=False)

    # Keyboard teleop loop
    try:
        while True:
            obs = client.get_observation()
            action = leader.get_action()

            # Head from keyboard
            from pynput import keyboard as kb
            _held = set()
            def _on(k):
                try:
                    if k.char: _held.add(k.char)
                except: pass
            def _off(k):
                try:
                    if k.char: _held.discard(k.char)
                except: pass
            l = kb.Listener(on_press=_on, on_release=_off)
            l.start()

            # Merge: override keyboard inputs on top of leader action
            if "w" in _held: action["head_tilt.pos"] = action.get("head_tilt.pos", 0) - 0.7
            if "s" in _held: action["head_tilt.pos"] = action.get("head_tilt.pos", 0) + 0.7
            if "a" in _held: action["head_pan.pos"] = action.get("head_pan.pos", 0) - 0.7
            if "d" in _held: action["head_pan.pos"] = action.get("head_pan.pos", 0) + 0.7

            # Base
            action["x.vel"] = 0.0
            action["theta.vel"] = 0.0
            if "i" in _held: action["x.vel"] = 0.2
            if "k" in _held: action["x.vel"] = -0.2
            if "j" in _held: action["theta.vel"] = 30.0
            if "l" in _held: action["theta.vel"] = -30.0

            # Lift
            if "u" in _held: action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0) + 2
            if "h" in _held: action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0) - 2

            client.send_action(action)
            l.stop()
            time.sleep(0.05)

            if "q" in _held:
                break

    except KeyboardInterrupt:
        pass
    finally:
        client.send_action({k: 0.0 for k in obs if k.endswith(".vel")})
        client.disconnect()
        leader.disconnect()
        print("Done")


if __name__ == "__main__":
    main()
