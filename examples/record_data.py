"""Record episodes for HumanaOpen — Python API with lerobot-record-style CLI args.

lerobot-record's CLI hardcodes the official robot types, so self-registered robots
like `humanaopen` are rejected ('invalid choice: humanaopen'). This script calls
`record()` directly via the Python API after registering third-party plugins,
while exposing the SAME argument names as lerobot-record (--robot.*, --teleop.*,
--dataset.*) so nothing is hidden.

Usage (all args optional — defaults match the tested hardware setup):
    python3 examples/record_data.py
    python3 examples/record_data.py --dataset.num_episodes=10 --dataset.single_task="pick up the cup"
    python3 examples/record_data.py --robot.cameras='{"head": {...}, ...}' --dataset.push_to_hub=false
    python3 examples/record_data.py --robot.confirm_lift_after_home=false

Controls (same as lerobot-record):
    C = start recording episode, Q = quit, A = re-record current episode
"""

import argparse
import json
import sys

sys.path.insert(0, "/home/zach/HumanaOpen")

from lerobot.utils.import_utils import register_third_party_devices
register_third_party_devices()  # must run before constructing configs

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.scripts.lerobot_record import DatasetRecordConfig, RecordConfig, record

from lerobot_robot_humanaopen.config_humanaopen import HumanaOpenConfig
from lerobot_robot_humanaopen.leader import HumanaOpenTeleopConfig

# ── Default camera devices (tested) ─────────────────────────────────────
# head/left_wrist/chest: MJPG 30fps; right_wrist: MJPG 30fps
DEFAULT_CAMERAS_JSON = json.dumps(
    {
        "head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
        "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"},
    }
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Record HumanaOpen episodes (Python API, lerobot-record-style args)"
    )
    # --robot.*
    p.add_argument("--robot.type", default="humanaopen")
    p.add_argument("--robot.id", default="follower")
    p.add_argument("--robot.port1", default="/dev/ttyACM0")
    p.add_argument("--robot.port2", default="/dev/ttyACM1")
    p.add_argument("--robot.port3", default=None, help="None = 2-bus mode (wheels+lift on port2)")
    p.add_argument("--robot.cameras", default=DEFAULT_CAMERAS_JSON, help='JSON dict of cameras, e.g. \'{"head": {...}}\'')
    p.add_argument("--robot.confirm_lift_after_home", default="true", choices=["true", "false"])
    # --teleop.*
    p.add_argument("--teleop.type", default="humanaopen_teleop")
    p.add_argument("--teleop.left_arm_port", default="/dev/ttyACM2")
    p.add_argument("--teleop.right_arm_port", default="/dev/ttyACM3")
    p.add_argument("--teleop.flip_joints", default='{"left": [], "right": []}')
    p.add_argument("--teleop.joint_remap", default="{}")
    # --dataset.*
    p.add_argument("--dataset.repo_id", default="zonglin11/humanaopen_act_demo")
    p.add_argument("--dataset.single_task", default="wave hello with both arms")
    p.add_argument("--dataset.num_episodes", type=int, default=2)
    p.add_argument("--dataset.episode_time_s", type=float, default=15.0)
    p.add_argument("--dataset.reset_time_s", type=float, default=10.0)
    p.add_argument("--dataset.fps", type=int, default=30)
    p.add_argument("--dataset.push_to_hub", default="true", choices=["true", "false"])
    p.add_argument("--dataset.root", default=None)
    p.add_argument("--dataset.video", default="true", choices=["true", "false"])
    p.add_argument("--dataset.private", default="false", choices=["true", "false"])
    p.add_argument("--dataset.tags", default=None, help="comma-separated tags")
    # convenience aliases (short flags)
    p.add_argument("--chest", action="store_true", help="add 4th chest camera (/dev/video6)")
    p.add_argument("--episodes", dest="dataset.num_episodes", type=int, default=None)
    p.add_argument("--task", dest="dataset.single_task", default=None)
    p.add_argument("--no-hub", dest="dataset.push_to_hub", action="store_const", const="false", default=None)
    return p


def _parse_bool(s: str) -> bool:
    return s.strip().lower() == "true"


def _load_cameras(json_str: str) -> dict:
    """Parse cameras JSON (lerobot-record style) into OpenCVCameraConfig dict."""
    data = json.loads(json_str)
    cams = {}
    for name, spec in data.items():
        if "type" not in spec or spec["type"] != "opencv":
            raise ValueError(f"Camera '{name}': only type='opencv' supported, got {spec.get('type')}")
        if "width" not in spec or "height" not in spec or "fps" not in spec:
            raise ValueError(
                f"Camera '{name}': width/height/fps required, got {list(spec.keys())}"
            )
        cams[name] = OpenCVCameraConfig(
            index_or_path=spec["index_or_path"],
            fps=int(spec["fps"]),
            width=int(spec["width"]),
            height=int(spec["height"]),
            fourcc=spec.get("fourcc", "MJPG"),
        )
    return cams


def show_command(args) -> None:
    """Print the equivalent lerobot-record CLI command for reference."""
    cams_json = args.__dict__.get("robot.cameras", DEFAULT_CAMERAS_JSON)
    cameras = json.loads(cams_json)
    # 每个摄像头独立一行, 参数完整 (可读性优先)
    cam_lines = []
    for i, (name, spec) in enumerate(cameras.items()):
        sep = " \\" if i < len(cameras) - 1 else ""
        cam_lines.append(
            f'      "{name}": {{"type": "opencv", "index_or_path": "{spec["index_or_path"]}", '
            f'"width": {spec["width"]}, "height": {spec["height"]}, "fps": {spec["fps"]}, '
            f'"fourcc": "{spec.get("fourcc", "MJPG")}"}}{sep}'
        )
    lines = [
        "=" * 70,
        "Equivalent lerobot-record command (reference):",
        "lerobot-record \\",
        f"    --robot.type={args.__dict__.get('robot.type')} \\",
        f"    --robot.id={args.__dict__.get('robot.id')} \\",
        f"    --robot.port1={args.__dict__.get('robot.port1')} --robot.port2={args.__dict__.get('robot.port2')} --robot.port3={args.__dict__.get('robot.port3')} \\",
        "    --robot.cameras='{",
        *cam_lines,
        "      }' \\",
        f"    --teleop.type={args.__dict__.get('teleop.type')} \\",
        f"    --teleop.left_arm_port={args.__dict__.get('teleop.left_arm_port')} --teleop.right_arm_port={args.__dict__.get('teleop.right_arm_port')} \\",
        f"    --teleop.flip_joints='{args.__dict__.get('teleop.flip_joints')}' \\",
        f"    --teleop.joint_remap='{args.__dict__.get('teleop.joint_remap')}' \\",
        f"    --robot.confirm_lift_after_home={args.__dict__.get('robot.confirm_lift_after_home')} \\",
        f"    --dataset.repo_id={args.__dict__.get('dataset.repo_id')} \\",
        f"    --dataset.num_episodes={args.__dict__.get('dataset.num_episodes')} \\",
        f"    --dataset.episode_time_s={args.__dict__.get('dataset.episode_time_s')} \\",
        f"    --dataset.reset_time_s={args.__dict__.get('dataset.reset_time_s')} \\",
        f'    --dataset.single_task="{args.__dict__.get("dataset.single_task")}" \\',
        f"    --dataset.fps={args.__dict__.get('dataset.fps')} \\",
        f"    --dataset.push_to_hub={args.__dict__.get('dataset.push_to_hub')}",
        "",
        "Note: the lerobot-record CLI hardcodes official robot types and rejects",
        "'humanaopen'; this script runs record() via the Python API with the same",
        "parameters shown above.",
        "=" * 70,
    ]
    print("\n".join(lines))


def _parse_port(s: str | None) -> str | None:
    """argparse 把 'None' 当字符串; 这里转回真正的 None (2-bus 模式)."""
    if s is None or str(s).strip().lower() == "none" or str(s).strip() == "":
        return None
    return str(s)


def main():
    parser = build_parser()
    args = parser.parse_args()
    d = vars(args)  # args.__dict__ for dotted attrs

    # Apply convenience aliases (--episodes/--task/--no-hub) over defaults
    if d.get("episodes") is not None:
        d["dataset.num_episodes"] = d["episodes"]
    if d.get("task") is not None:
        d["dataset.single_task"] = d["task"]
    if d.get("no_hub") is not None:
        d["dataset.push_to_hub"] = "false"

    # port3='None' 字符串 → 真正的 None (2-bus 模式)
    d["robot.port3"] = _parse_port(d["robot.port3"])
    d["dataset.root"] = _parse_port(d["dataset.root"])

    show_command(args)

    cameras = _load_cameras(d["robot.cameras"])
    if d.get("chest"):
        cameras["chest"] = OpenCVCameraConfig(
            index_or_path="/dev/video6", fps=30, width=640, height=480, fourcc="MJPG"
        )
    print(f"Cameras:  {list(cameras.keys())}")
    print(f"Task:     {d['dataset.single_task']}")
    print(f"Episodes: {d['dataset.num_episodes']} x {d['dataset.episode_time_s']}s "
          f"(push_to_hub={_parse_bool(d['dataset.push_to_hub'])})")
    print()

    cfg = RecordConfig(
        robot=HumanaOpenConfig(
            id=d["robot.id"],
            port1=d["robot.port1"],
            port2=d["robot.port2"],
            port3=d["robot.port3"],
            cameras=cameras,
            confirm_lift_after_home=_parse_bool(d["robot.confirm_lift_after_home"]),
            # 与遥操脚本一致: 左轮装反需取反, 否则 i/j/k/l 方向错乱
            wheel_dir_signs={"base_left_wheel": -1, "base_right_wheel": 1},
        ),
        dataset=DatasetRecordConfig(
            repo_id=d["dataset.repo_id"],
            single_task=d["dataset.single_task"],
            num_episodes=d["dataset.num_episodes"],
            episode_time_s=d["dataset.episode_time_s"],
            reset_time_s=d["dataset.reset_time_s"],
            fps=d["dataset.fps"],
            push_to_hub=_parse_bool(d["dataset.push_to_hub"]),
            root=d["dataset.root"],
            video=_parse_bool(d["dataset.video"]),
            private=_parse_bool(d["dataset.private"]),
            tags=d["dataset.tags"].split(",") if d["dataset.tags"] else None,
        ),
        teleop=HumanaOpenTeleopConfig(
            id="leader",
            left_arm_port=d["teleop.left_arm_port"],
            right_arm_port=d["teleop.right_arm_port"],
            flip_joints=json.loads(d["teleop.flip_joints"]),
            joint_remap=json.loads(d["teleop.joint_remap"]),
        ),
        display_data=True,
    )
    try:
        record(cfg)
    finally:
        # 保存升降最新位置, 下次连接免归零 (record 结束时升降可能已移动)
        try:
            from lerobot_robot_humanaopen.leader import get_connected_robot
            r = get_connected_robot()
            if r is not None:
                r.lift_axis.save_zero()
                print(f"Lift position saved (next connect: no re-homing)")
        except Exception as e:
            print(f"Warning: lift position save failed: {e}")


if __name__ == "__main__":
    main()
