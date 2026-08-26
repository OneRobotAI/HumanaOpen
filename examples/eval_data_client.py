"""Run policy inference via ZMQ client (dual-machine).

Host: Jetson/RPi (runs HumanaOpenHost)
Client: GPU machine (runs this script, loads model locally)

Usage:
    # 1. On Jetson/RPi: start Host
    python3 -c "
    from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
    from lerobot_robot_humanaopen import HumanaOpenConfig
    HumanaOpenHost(HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})).run()
    "

    # 2. On PC: run inference
    python3 examples/eval_data_client.py \
        --remote_ip=192.168.1.100 \
        --policy.type=act \
        --policy.repo_id=your-name/humanaopen_act_policy \
        --num-episodes=5 --duration=30
"""

import argparse
import json
import sys
import time

import numpy as np
import torch

sys.path.insert(0, "/home/zach/HumanaOpen")

from lerobot.utils.import_utils import register_third_party_plugins
register_third_party_plugins()

from lerobot_robot_humanaopen.humanaopen_client import HumanaOpenClient
from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenClientConfig


def build_policy_obs(obs, policy, client, device):
    """Convert ZMQ observation to policy input format."""
    batch = {}
    for cam_name in ("head", "left_wrist", "right_wrist"):
        img = obs.get(cam_name)
        if img is not None:
            t = torch.from_numpy(np.ascontiguousarray(img.transpose(2, 0, 1))).float().unsqueeze(0) / 255.0
            batch[f"observation.images.{cam_name}"] = t.to(device)

    state_keys = sorted([k for k in obs if k.endswith(".pos") or k == "lift_axis.height_mm"])
    batch["observation.state"] = torch.tensor([[obs[k] for k in state_keys]], dtype=torch.float32).to(device)

    if hasattr(policy.config, "vlm_model_name") and policy.config.vlm_model_name:
        from transformers import AutoProcessor
        processor = AutoProcessor.from_pretrained(policy.config.vlm_model_name)
        tokenized = processor.tokenizer(
            task + "\n", return_tensors="pt", padding="max_length",
            max_length=policy.config.tokenizer_max_length, truncation=True,
        )
        batch["observation.language.tokens"] = tokenized["input_ids"].to(device)
        batch["observation.language.attention_mask"] = tokenized["attention_mask"].bool().to(device)
    return batch


def action_to_dict(action_np, obs):
    """Convert action array to dict, using obs keys for action mapping."""
    action_keys = sorted([k for k in obs if k.endswith(".pos") or k == "lift_axis.height_mm"])
    d = {}
    for i, key in enumerate(action_keys):
        d[key] = float(action_np[i]) if i < len(action_np) else 0.0
    d["x.vel"] = 0.0
    d["theta.vel"] = 0.0
    return d


def main():
    parser = argparse.ArgumentParser(description="Inference via ZMQ client (dual-machine)")
    parser.add_argument("--remote_ip", default="127.0.0.1")
    parser.add_argument("--port_zmq_cmd", type=int, default=5555)
    parser.add_argument("--port_zmq_obs", type=int, default=5556)
    parser.add_argument("--policy.type", default="act", choices=["act", "smolvla"])
    parser.add_argument("--policy.repo_id", required=True)
    parser.add_argument("--policy.device", default="cuda")
    parser.add_argument("--task", default="")
    parser.add_argument("--num-episodes", type=int, default=5)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()
    d = vars(args)

    # Load policy
    print(f"Loading {d['policy.type'].upper()}...")
    if d["policy.type"] == "smolvla":
        from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
        policy = SmolVLAPolicy.from_pretrained(d["policy.repo_id"])
    else:
        from lerobot.policies.act.modeling_act import ACTPolicy
        policy = ACTPolicy.from_pretrained(d["policy.repo_id"])
    policy = policy.to(d["policy.device"]).eval()
    print(f"  Loaded ({sum(p.numel() for p in policy.parameters())/1e6:.1f}M params)")

    # Connect to Host
    print(f"Connecting to Host {d['remote_ip']}...")
    client_config = HumanaOpenClientConfig(
        remote_ip=d["remote_ip"],
        port_zmq_cmd=d["port_zmq_cmd"],
        port_zmq_observations=d["port_zmq_obs"],
    )
    client = HumanaOpenClient(client_config)
    client.connect()
    print("  Connected")

    # Quit key
    from pynput import keyboard as kb
    quit_flag = [False]
    def on_press(key):
        try:
            if key.char == "q": quit_flag[0] = True
        except AttributeError: pass
    quit_listener = kb.Listener(on_press=on_press)
    quit_listener.start()

    # Rollout
    try:
        for ep in range(d["num_episodes"]):
            if quit_flag[0]: break
            print(f"\n  Episode {ep+1}/{d['num_episodes']}")
            ep_start = time.time()

            for step in range(int(d["duration"] * d["fps"])):
                if quit_flag[0]: break
                obs = client.get_observation()
                batch = build_policy_obs(obs, policy, client, d["policy.device"])
                with torch.no_grad():
                    action = policy.select_action(batch)
                client.send_action(action_to_dict(action.cpu().numpy().flatten(), obs))
                time.sleep(1.0 / d["fps"])

                if step % 30 == 0 and step > 0:
                    fps = (step+1) / (time.time() - ep_start)
                    print(f"  Step {step} | {fps:.1f} fps")

            print(f"  Episode {ep+1} done")
            client.send_action({k: 0.0 for k in obs if k.endswith(".vel")})
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        quit_listener.stop()
        client.send_action({k: 0.0 for k in obs if k.endswith(".vel")})
        client.disconnect()
        print("Done")


if __name__ == "__main__":
    main()
