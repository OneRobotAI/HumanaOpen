"""Rollout an ACT policy on a real HumanaOpen robot.

Records observations, runs the policy, and sends actions at 30Hz.
The robot's cameras and state are fed to the ACT model which predicts
action chunks. The first action of each chunk is executed, then the
next chunk is predicted on the new observation.

Usage:
    python3 examples/eval_data.py \
        --policy.repo_id=zonglin11/humanaopen_act_demo_policy \
        --robot.type=humanaopen

    # With human teleop as safety override (hold keys to override policy):
    python3 examples/eval_data.py \
        --policy.repo_id=zonglin11/humanaopen_act_demo_policy \
        --robot.type=humanaopen \
        --teleop.type=humanaopen_teleop \
        --teleop.left_arm_port=/dev/ttyACM2 --teleop.right_arm_port=/dev/ttyACM3 \
        --teleop.flip_joints='{"left": [], "right": []}' --teleop.joint_remap='{}' \
        --num-episodes=5 --duration=30

Press 'e' to enable/disable human override, 'q' to quit.
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
from lerobot.policies.act.modeling_act import ACTPolicy

from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenConfig
from lerobot_robot_humanaopen.humanaopen import HumanaOpen
from lerobot_robot_humanaopen.leader import HumanaOpenTeleop, HumanaOpenTeleopConfig

# ── Default camera devices ──────────────────────────────────────────────
DEFAULT_CAMERAS_JSON = json.dumps(
    {
        "head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
    }
)


def build_cameras(json_str: str) -> dict:
    data = json.loads(json_str)
    cams = {}
    for name, spec in data.items():
        cams[name] = OpenCVCameraConfig(
            index_or_path=spec["index_or_path"],
            fps=int(spec["fps"]),
            width=int(spec["width"]),
            height=int(spec["height"]),
            fourcc=spec.get("fourcc", "MJPG"),
        )
    return cams


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Rollout ACT policy on HumanaOpen")
    # --robot.*
    p.add_argument("--robot.type", default="humanaopen")
    p.add_argument("--robot.id", default="follower")
    p.add_argument("--robot.port1", default="/dev/ttyACM0")
    p.add_argument("--robot.port2", default="/dev/ttyACM1")
    p.add_argument("--robot.port3", default=None)
    p.add_argument("--robot.cameras", default=DEFAULT_CAMERAS_JSON)
    # --teleop.* (optional safety override)
    p.add_argument("--teleop.type", default=None)
    p.add_argument("--teleop.left_arm_port", default="/dev/ttyACM2")
    p.add_argument("--teleop.right_arm_port", default="/dev/ttyACM3")
    p.add_argument("--teleop.flip_joints", default='{"left": [], "right": []}')
    p.add_argument("--teleop.joint_remap", default="{}")
    # --policy.*
    p.add_argument("--policy.type", default="act", choices=["act", "smolvla"], help="Policy type: act or smolvla")
    p.add_argument("--policy.repo_id", default="zonglin11/humanaopen_act_demo_policy")
    p.add_argument("--policy.device", default="cuda")
    # rollout
    p.add_argument("--num-episodes", type=int, default=5)
    p.add_argument("--duration", type=float, default=30.0, help="seconds per episode")
    p.add_argument("--fps", type=int, default=30)
    # display
    p.add_argument("--no-display", action="store_true", help="skip rerun visualization")
    p.add_argument("--task", default="wave hello with both arms", help="Language instruction for SmolVLA (required for VLA policies)")
    p.add_argument("--save-video", default=None, help="save rollout video to this path")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    d = vars(args)

    port3 = d["robot.port3"]
    if port3 and port3.strip().lower() == "none":
        port3 = None

    cameras = build_cameras(d["robot.cameras"])
    has_teleop = d["teleop.type"] is not None and policy_type != "smolvla"

    print("=" * 60)
    print("HumanaOpen ACT Policy Rollout")
    print(f"  Model:     {d['policy.repo_id']} ({d['policy.type'].upper()})")
    print(f"  Device:    {d['policy.device']}")
    print(f"  Cameras:   {list(cameras.keys())}")
    print(f"  Episodes:  {d['num_episodes']} x {d['duration']}s @ {d['fps']}Hz")
    print(f"  Teleop:    {'human override enabled' if has_teleop else 'policy only'}")
    print(f"  Task:      \"{d.get('task', 'wave hello with both arms')}\"")
    print("=" * 60)
    print()

    # ── Load model ───────────────────────────────────────────────────
    policy_type = d.get("policy.type", "act")
    print(f"Loading {policy_type.upper()} policy...")
    if policy_type == "smolvla":
        from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
        policy = SmolVLAPolicy.from_pretrained(d["policy.repo_id"])
    else:
        from lerobot.policies.act.modeling_act import ACTPolicy
        policy = ACTPolicy.from_pretrained(d["policy.repo_id"])
    policy = policy.to(d["policy.device"])
    policy.eval()
    print(f"  Model loaded ({sum(p.numel() for p in policy.parameters())/1e6:.1f}M params)")

    # ── Connect robot ────────────────────────────────────────────────
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

    # ── Optional teleop (safety override) ────────────────────────────
    leader = None
    if has_teleop:
        print("Connecting teleop...")
        leader = HumanaOpenTeleop(HumanaOpenTeleopConfig(
            id="leader",
            left_arm_port=d["teleop.left_arm_port"],
            right_arm_port=d["teleop.right_arm_port"],
            flip_joints=json.loads(d["teleop.flip_joints"]),
            joint_remap=json.loads(d["teleop.joint_remap"]),
        ), robot=robot)
        leader.connect(calibrate=True)
        print("  Teleop connected (press 'e' to enable/disable override)")

    # ── Rerun display ────────────────────────────────────────────────
    if not args.no_display:
        try:
            rr.init("humanaopen_rollout", spawn=True)
            print("  Rerun viewer started")
        except Exception as e:
            print(f"  ⚠️ Rerun unavailable: {e}")

    # ── Keyboard listener ────────────────────────────────────────────
    from lerobot_robot_humanaopen.leader import register_keyboard_callback

    override_enabled = [False]
    quit_flag = [False]
    _pressed = set()

    # 注册全局共享键盘回调 — 不创建独立 listener (Linux/X11 多个 pynput Listener 会抢占)
    def eval_kb_cb(ch: str, is_pressed: bool) -> None:
        if is_pressed:
            _pressed.add(ch)
            if ch == "q":
                quit_flag[0] = True
        else:
            _pressed.discard(ch)

    register_keyboard_callback(eval_kb_cb)

    # ── Rollout loop ─────────────────────────────────────────────────
    try:
        for ep in range(d["num_episodes"]):
            if quit_flag[0]:
                break
            print(f"\n  Episode {ep + 1}/{d['num_episodes']}")

            # Keyboard state
            keys = _pressed.copy()
            override_enabled[0] = False
            print("  Policy control active (press 'e' to override)" if has_teleop else "  Running inference...")
            episode_start = time.time()

            for step in range(int(d["duration"] * d["fps"])):
                if quit_flag[0]:
                    break
                t_start = time.perf_counter()

                # Override: hold 'e' = override, release = policy
                new_override = "e" in _pressed
                if new_override != override_enabled[0]:
                    override_enabled[0] = new_override
                    if override_enabled[0]:
                        print("  🟢 Override ON — arms from leader, head/lift/base from keyboard")
                    else:
                        print("  🔴 Override OFF — policy control")
                obs = robot.get_observation()

                # ── Apply action ──────────────────────────────────────
                if override_enabled[0] and leader is not None:
                    # Override: skip policy inference, use leader directly
                    action_dict = leader.get_action()
                    robot.send_action(action_dict)
                else:
                    # Policy inference (expensive for VLA models)
                    policy_obs = _build_policy_obs(obs, policy, cameras, d["policy.device"], robot, task=d.get("task", ""))
                    with torch.no_grad():
                        action_tensor = policy.select_action(policy_obs)
                    action_np = action_tensor.cpu().numpy().flatten()
                    action_dict = _action_to_dict(action_np, policy, robot)
                    robot.send_action(action_dict)

                # ── Log to rerun ──────────────────────────────────────
                if not args.no_display and step % 5 == 0:
                    _log_rerun(obs, action_dict, step, ep)

                time.sleep(1.0 / d["fps"])

                # Progress display (every 30 steps)
                if step % 30 == 0 and step > 0:
                    elapsed = time.time() - episode_start
                    fps_actual = (step + 1) / elapsed if elapsed > 0 else 0
                    total_time = d["duration"] * d["fps"] / fps_actual if fps_actual > 0 else float("inf")
                    print(f"  Step {step}/{int(d['duration'] * d['fps'])} | {fps_actual:.1f} fps | ETA: {total_time/60:.1f}min per episode")

            print(f"  Episode {ep + 1} complete")
            # stop motors between episodes
            robot.send_action({k: 0.0 for k in robot.action_features if k.endswith(".vel")})
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n  Stopped")
    finally:
        # stop all motors
        try:
            robot.send_action({k: 0.0 for k in robot.action_features if k.endswith(".vel")})
            robot.send_action({"lift_axis.height_mm": robot.lift_axis.get_height_mm()})
        except Exception:
            pass
        if leader:
            try:
                leader.disconnect()
            except Exception:
                pass
        robot.disconnect()
        print("Done")


def _build_policy_obs(obs, policy, cameras, device, robot, task: str = ""):
    """Convert robot observation dict to policy batch format."""
    batch = {}
    # Images
    for cam_name in cameras:
        img = obs.get(cam_name)
        if img is not None:
            t = torch.from_numpy(np.ascontiguousarray(img.transpose(2, 0, 1))).float().unsqueeze(0) / 255.0
            batch[f"observation.images.{cam_name}"] = t.to(device)

    # State
    state_keys = sorted([
        k for k in robot.observation_features
        if not k.startswith("observation.") and k not in cameras
    ])
    state_vals = [obs[k] for k in state_keys]
    batch["observation.state"] = torch.tensor([state_vals], dtype=torch.float32).to(device)

    # SmolVLA: tokenize language instruction
    if hasattr(policy.config, 'vlm_model_name') and policy.config.vlm_model_name:
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


def _action_to_dict(action_np, policy, robot):
    """Convert 21-dim action array to robot send_action dict."""
    action_keys = list(robot.action_features.keys())
    action_dict = {}
    for i, key in enumerate(action_keys):
        action_dict[key] = float(action_np[i]) if i < len(action_np) else 0.0
    return action_dict


def _log_rerun(obs, action_dict, step, episode):
    """Log current state to Rerun."""
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


if __name__ == "__main__":
    main()
