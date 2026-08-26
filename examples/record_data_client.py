"""Record data via ZMQ client — for dual-machine deployment.

Host: Jetson/RPi (runs HumanaOpenHost, reads servos/cameras)
Client: GPU machine (runs this script, records data via ZMQ)

Usage:
    # 1. On Jetson/RPi: start Host
    python3 -c "
    from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
    from lerobot_robot_humanaopen import HumanaOpenConfig
    HumanaOpenHost(HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})).run()
    "

    # 2. On PC: run this script
    python3 examples/record_data_client.py \
        --remote_ip=192.168.1.100 \
        --dataset.repo_id=your-name/humanaopen_demo \
        --dataset.single_task="wave hello"
"""

import argparse
import json
import sys
import time

sys.path.insert(0, "/home/zach/HumanaOpen")

from lerobot.utils.import_utils import register_third_party_plugins
register_third_party_plugins()

import numpy as np
from lerobot.robots.robot import Robot
from lerobot.robots.config import RobotConfig

from lerobot_robot_humanaopen.humanaopen_client import HumanaOpenClient
from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenClientConfig


class ClientRobot(Robot):
    """Minimal Robot implementation that wraps HumanaOpenClient over ZMQ."""

    name = "humanaopen_client"

    def __init__(self, config: HumanaOpenClientConfig):
        super().__init__(config)
        self._client = HumanaOpenClient(config)
        self._client_config = config

    def connect(self, calibrate=True):
        self._client.connect()
        # Probe features from first observation
        obs = self._client.get_observation()
        self._obs_keys = list(obs.keys())
        # Include lift_axis.height_mm in action (not in .pos keys)
        self._act_keys = [k for k in self._obs_keys if k.endswith(".pos")]
        if "lift_axis.height_mm" not in self._act_keys:
            self._act_keys.append("lift_axis.height_mm")

    def disconnect(self):
        self._client.disconnect()

    def get_observation(self):
        return self._client.get_observation()

    def send_action(self, action):
        self._client.send_action(action)

    @property
    def observation_features(self) -> dict:
        return {k: float for k in self._obs_keys}

    @property
    def action_features(self) -> dict:
        return {k: float for k in self._act_keys}

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected

    @property
    def is_calibrated(self) -> bool:
        return True  # no local calibration in client mode

    def calibrate(self):
        pass

    def configure(self):
        pass


def main():
    parser = argparse.ArgumentParser(description="Record data via ZMQ client (dual-machine)")
    parser.add_argument("--remote_ip", default="127.0.0.1")
    parser.add_argument("--port_zmq_cmd", type=int, default=5555)
    parser.add_argument("--port_zmq_obs", type=int, default=5556)
    parser.add_argument("--teleop.left_arm_port", default="/dev/ttyACM2")
    parser.add_argument("--teleop.right_arm_port", default="/dev/ttyACM3")
    parser.add_argument("--teleop.flip_joints", default='{"left": [], "right": []}')
    parser.add_argument("--teleop.joint_remap", default="{}")
    parser.add_argument("--dataset.repo_id", default="zonglin11/humanaopen_demo")
    parser.add_argument("--dataset.single_task", default="wave hello")
    parser.add_argument("--dataset.num_episodes", type=int, default=2)
    parser.add_argument("--dataset.episode_time_s", type=float, default=15.0)
    parser.add_argument("--dataset.reset_time_s", type=float, default=10.0)
    parser.add_argument("--dataset.fps", type=int, default=30)
    parser.add_argument("--dataset.push_to_hub", default="false")
    args = parser.parse_args()
    d = vars(args)

    from lerobot.scripts.lerobot_record import DatasetRecordConfig, RecordConfig, record
    from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig

    # Monkey-patch make_robot_from_config to handle humanaopen_client
    import lerobot.robots.utils as robot_utils
    _original_make_robot = robot_utils.make_robot_from_config

    def _patched_make_robot(config):
        if config.type == "humanaopen_client":
            return ClientRobot(config)
        return _original_make_robot(config)

    robot_utils.make_robot_from_config = _patched_make_robot

    client_config = HumanaOpenClientConfig(
        remote_ip=d["remote_ip"],
        port_zmq_cmd=d["port_zmq_cmd"],
        port_zmq_observations=d["port_zmq_obs"],
    )

    teleop = BiHumanaOpenLeaderConfig(
        id="leader",
        left_arm_port=d["teleop.left_arm_port"],
        right_arm_port=d["teleop.right_arm_port"],
        flip_joints=json.loads(d["teleop.flip_joints"]),
        joint_remap=json.loads(d["teleop.joint_remap"]),
    )

    cfg = RecordConfig(
        robot=client_config,  # make_robot_from_config → ClientRobot via monkey-patch
        dataset=DatasetRecordConfig(
            repo_id=d["dataset.repo_id"],
            single_task=d["dataset.single_task"],
            num_episodes=d["dataset.num_episodes"],
            episode_time_s=d["dataset.episode_time_s"],
            reset_time_s=d["dataset.reset_time_s"],
            fps=d["dataset.fps"],
            push_to_hub=d["dataset.push_to_hub"] == "true",
        ),
        teleop=teleop,
        display_data=True,
    )

    print("=" * 60)
    print("HumanaOpen Dual-Machine Recording")
    print(f"  Host:  {d['remote_ip']}:{d['port_zmq_obs']}/{d['port_zmq_cmd']}")
    print(f"  Task:  {d['dataset.single_task']}")
    print(f"  Episodes: {d['dataset.num_episodes']} x {d['dataset.episode_time_s']}s")
    print("=" * 60)
    record(cfg)


if __name__ == "__main__":
    main()
