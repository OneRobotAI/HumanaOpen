"""Run a trained policy on a real HumanaOpen robot.

Pure inference — loads model, connects robot, runs policy loop.
No teleop/override. Press q to quit.

Usage:
    # ACT
    python3 examples/eval_data.py \
        --policy.type=act \
        --policy.repo_id=your-name/humanaopen_act_policy

    # SmolVLA (requires --task)
    python3 examples/eval_data.py \
        --policy.type=smolvla \
        --policy.repo_id=your-name/humanaopen_smolvla_policy \
        --task="wave hello with both arms"
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch
import rerun as rr

sys.path.insert(0, "/home/zach/HumanaOpen")

from lerobot.utils.import_utils import register_third_party_plugins
register_third_party_plugins()

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenConfig
from lerobot_robot_humanaopen.humanaopen import HumanaOpen

DEFAULT_CAMERAS_JSON = json.dumps(
    {
        "head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
    }
)


def build_cameras(json_str: str) -> dict:
    data = json.loads(json_str)
    return {
        name: OpenCVCameraConfig(
            index_or_path=spec["index_or_path"],
            fps=int(spec["fps"]),
            width=int(spec["width"]),
            height=int(spec["height"]),
            fourcc=spec.get("fourcc", "MJPG"),
        )
        for name, spec in data.items()
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="HumanaOpen policy rollout")
    p.add_argument("--robot.type", default="humanaopen")
    p.add_argument("--robot.id", default="follower")
    p.add_argument("--robot.port1", default="/dev/ttyACM0")
    p.add_argument("--robot.port2", default="/dev/ttyACM1")
    p.add_argument("--robot.port3", default=None)
    p.add_argument("--robot.cameras", default=DEFAULT_CAMERAS_JSON)
    p.add_argument("--policy.type", default="act", choices=["act", "smolvla"])
    p.add_argument("--policy.repo_id", required=True)
    p.add_argument("--policy.device", default="cuda")
    p.add_argument("--num-episodes", type=int, default=5)
    p.add_argument("--duration", type=float, default=30.0)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--task", default="", help="Language instruction (required for smolvla)")
    p.add_argument("--enable-base", default="false", choices=["true", "false"], help="Allow policy to control base wheels")
    p.add_argument("--no-display", action="store_true")
    # --teleop.* (optional leader arms for manual control)
    p.add_argument("--teleop.left_arm_port", default="/dev/ttyACM2")
    p.add_argument("--teleop.right_arm_port", default="/dev/ttyACM3")
    p.add_argument("--teleop.flip_joints", default='{"left": [], "right": []}')
    p.add_argument("--teleop.joint_remap", default="{}")
    return p


def _build_policy_obs(obs, policy, cameras, device, robot, task=""):
    batch = {}
    for cam_name in cameras:
        img = obs.get(cam_name)
        if img is not None:
            t = torch.from_numpy(np.ascontiguousarray(img.transpose(2, 0, 1))).float().unsqueeze(0) / 255.0
            batch[f"observation.images.{cam_name}"] = t.to(device)

    state_keys = sorted([
        k for k in robot.observation_features
        if not k.startswith("observation.") and k not in cameras
    ])
    batch["observation.state"] = torch.tensor(
        [[obs[k] for k in state_keys]], dtype=torch.float32
    ).to(device)

    if hasattr(policy.config, "vlm_model_name") and policy.config.vlm_model_name:
        from transformers import AutoProcessor
        processor = AutoProcessor.from_pretrained(policy.config.vlm_model_name)
        tokenized = processor.tokenizer(
            task + "\n",
            return_tensors="pt",
            padding="max_length",
            max_length=policy.config.tokenizer_max_length,
            truncation=True,
        )
        batch["observation.language.tokens"] = tokenized["input_ids"].to(device)
        batch["observation.language.attention_mask"] = tokenized["attention_mask"].bool().to(device)

    return batch


def _action_to_dict(action_np, robot, enable_base=False):
    action_keys = list(robot.action_features.keys())
    action_dict = {}
    for i, key in enumerate(action_keys):
        val = float(action_np[i]) if i < len(action_np) else 0.0
        if not enable_base and key in ("x.vel", "theta.vel"):
            val = 0.0
        action_dict[key] = val
    return action_dict


def _log_rerun(obs, action_dict, step, episode):
    try:
        for cam_key in ("head", "left_wrist", "right_wrist"):
            img = obs.get(cam_key)
            if img is not None:
                rr.log(f"observation.images.{cam_key}", rr.Image(img))
        for key, val in sorted(action_dict.items()):
            if val != 0.0:
                rr.log(f"action.{key}", rr.Scalars(float(val)))
        rr.log("step", rr.Scalars(step))
    except Exception:
        pass


def main():
    parser = build_parser()
    args = parser.parse_args()
    d = vars(args)

    port3 = d["robot.port3"]
    if port3 and str(port3).strip().lower() == "none":
        port3 = None

    cameras = build_cameras(d["robot.cameras"])
    enable_base = d.get("enable_base", "false").strip().lower() == "true"

    print("=" * 60)
    print("HumanaOpen Policy Rollout")
    print(f"  Policy:   {d['policy.type'].upper()} — {d['policy.repo_id']}")
    print(f"  Device:   {d['policy.device']}")
    print(f"  Cameras:  {list(cameras.keys())}")
    print(f"  Episodes: {d['num_episodes']} x {d['duration']}s @ {d['fps']}Hz")
    print(f"  Base:     {'enabled' if enable_base else 'disabled'}")
    if d.get("task"):
        print(f"  Task:     \"{d['task']}\"")
    print("=" * 60)
    print()

    # Load model
    print(f"Loading {d['policy.type'].upper()} policy...")
    if d["policy.type"] == "smolvla":
        from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
        policy = SmolVLAPolicy.from_pretrained(d["policy.repo_id"])
    else:
        from lerobot.policies.act.modeling_act import ACTPolicy
        policy = ACTPolicy.from_pretrained(d["policy.repo_id"])
    policy = policy.to(d["policy.device"])
    policy.eval()
    print(f"  Loaded ({sum(p.numel() for p in policy.parameters())/1e6:.1f}M params)")

    # Connect robot
    print("Connecting robot...")
    robot = HumanaOpen(HumanaOpenConfig(
        id=d["robot.id"],
        port1=d["robot.port1"],
        port2=d["robot.port2"],
        port3=port3,
        cameras=cameras,
    ))
    robot.connect(calibrate=True)
    print("  Robot connected")

    # Optional: connect leader arms for manual dual-arm control
    from lerobot_robot_humanaopen.leader import BiHumanaOpenLeader, BiHumanaOpenLeaderConfig
    leader = None
    print("Connecting leader arms...")
    try:
        leader = BiHumanaOpenLeader(BiHumanaOpenLeaderConfig(
            id="leader",
            left_arm_port=d["teleop.left_arm_port"],
            right_arm_port=d["teleop.right_arm_port"],
            flip_joints=json.loads(d["teleop.flip_joints"]),
            joint_remap=json.loads(d["teleop.joint_remap"]),
        ))
        leader.connect(calibrate=False)
        print("  Leader arms connected (dual-arm manual control active)")
    except Exception as e:
        print(f"  ⚠️ Leader arms not available: {e}")

    # Rerun display
    if not d["no_display"]:
        try:
            rr.init("humanaopen_rollout", spawn=True)
            print("  Rerun viewer started")
        except Exception as e:
            print(f"  ⚠️ Rerun unavailable: {e}")

    # Quit key (pynput, lightweight)
    from pynput import keyboard as kb
    quit_flag = [False]

    def on_press(key):
        try:
            if key.char == "q":
                quit_flag[0] = True
        except AttributeError:
            pass

    quit_listener = kb.Listener(on_press=on_press)
    quit_listener.start()

    # Rollout loop
    try:
        for ep in range(d["num_episodes"]):
            if quit_flag[0]:
                break
            print(f"\n  Episode {ep + 1}/{d['num_episodes']}")
            print("  Policy control active")
            episode_start = time.time()

            for step in range(int(d["duration"] * d["fps"])):
                if quit_flag[0]:
                    break
                t_start = time.perf_counter()

                obs = robot.get_observation()

                policy_obs = _build_policy_obs(obs, policy, cameras, d["policy.device"], robot, task=d.get("task", ""))
                with torch.no_grad():
                    action_tensor = policy.select_action(policy_obs)
                action_np = action_tensor.cpu().numpy().flatten()
                action_dict = _action_to_dict(action_np, robot, enable_base=enable_base)
                robot.send_action(action_dict)

                if not d["no_display"] and step % 5 == 0:
                    _log_rerun(obs, action_dict, step, ep)

                elapsed = time.perf_counter() - t_start
                if elapsed < 1.0 / d["fps"]:
                    time.sleep(1.0 / d["fps"] - elapsed)

                if step % 30 == 0 and step > 0:
                    fps_actual = (step + 1) / (time.time() - episode_start)
                    eta_min = int(d["duration"]) / fps_actual / 60 if fps_actual > 0 else 0
                    print(f"  Step {step} | {fps_actual:.1f} fps | ETA {eta_min:.1f}min")

            print(f"  Episode {ep + 1} complete")
            robot.send_action({k: 0.0 for k in robot.action_features if k.endswith(".vel")})
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n  Stopped")
    finally:
        try:
            robot.lift_axis.save_zero()
        except Exception:
            pass
        try:
            robot.send_action({k: 0.0 for k in robot.action_features if k.endswith(".vel")})
            robot.send_action({"lift_axis.height_mm": robot.lift_axis.get_height_mm()})
        except Exception:
            pass
        quit_listener.stop()
        robot.disconnect()
        print("Done")


if __name__ == "__main__":
    main()
