# HumanaLite

**Open-source semi-humanoid robot — 7-DOF dual arms, differential drive, and leadscrew lift.**

Built on [LeRobot](https://github.com/huggingface/lerobot) and
[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini).

## Hardware

| Subsystem | Motors | Model |
|-----------|--------|-------|
| Left follower arm | 8 (7-DOF + gripper) | ST3215 C018 (1:345) |
| Right follower arm | 8 (7-DOF + gripper) | ST3215 C018 (1:345) |
| Head (pan/tilt) | 2 | ST3215 C018 (1:345) |
| Lift (leadscrew) | 1 | ST3250 (direct drive, no belt) |
| Differential drive base | 2 | ST3215 C018 (1:345) |
| Leader arms (teleop) | 2 × 8 | STS3215 C046 (1:147) |

> **Left/right convention**: Defined from the robot's own frame of reference.
> Standing behind the robot and facing the same direction as it, the arm on your
> left-hand side is the **left arm** (`port1`), the arm on your right-hand side is
> the **right arm** (`port2`). Wiring decides which physical arm is which; the
> software simply maps `left_arm_*` → `port1` and `right_arm_*` → `port2`.

## Software

```
lerobot_robot_humanalite/
├── __init__.py              # Package exports
├── config_humanalite.py     # HumanaLiteConfig, host/client configs
├── humanalite.py            # HumanaLite Robot class (follower)
├── lift_axis.py             # Lift axis with stall-detection homing
├── leader.py                # Leader teleoperator (single/bimanual)
├── humanalite_host.py       # ZMQ host (robot-side, for dual-machine mode)
└── humanalite_client.py     # ZMQ client (teleop-side)
examples/
├── record_data.py              # Data collection (Python API, all parameters)
├── eval_data.py                # Inference (ACT policy rollout)
├── single_machine.py           # Single machine operation
├── teleop_keyboard.py          # Keyboard teleoperation via ZMQ
├── teleop_leader_to_follower.py  # Full-body teleop: leader arms + keyboard
├── calibrate_follower.py       # Full follower-side calibration (arms+head+wheels+lift)
├── calibrate_leader.py         # Leader arm calibration (open-arms-mini)
├── diagnose_teleop.py          # Teleop joint direction diagnosis
├── test_base_keyboard.py       # Base-only keyboard test (no lift/arms)
├── test_lift_only.py           # Lift axis test (homing + raise/lower)
└── check_phase.py              # Check servo velocity unit (Phase BIT2)

### Diagnostics & Tuning Tools

| Script | Purpose |
|--------|---------|
| `diag_head_tilt_limits.py` | Head tilt mechanical range probe (before/after unlock) |
| `diag_head_tilt_range.py` | Head tilt range diagnostic |
| `diag_regression.py` | Regression test (lift + camera + teleop sequence) |
| `diag_st3250_speed.py` | ST3250 motor speed profiling (Phase BIT2=1) |
| `diag_follower_gripper.py` | Gripper joint diagnosis |
| `recover_lift_ping.py` | Lift motor communication ping |
| `speed_test_bit2_0.py` | BIT2=0 speed verification |
| `switch_phase_bit2.py` | Toggle ST3250 Phase BIT2 register |
```

## Quick Start

```bash
# 1. Create a conda env and install HumanaLite (editable)
conda create -n lerobot python=3.12
conda activate lerobot
cd /path/to/HumanaLite
pip install -e . --no-deps

# 2. Single-machine operation
python -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
config = HumanaLiteConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
robot = HumanaLite(config)
robot.connect()
print(robot.get_observation().keys())
"

# 3. Dual-machine ZMQ mode (run on robot)
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
```

## Teleoperation

### Full-body teleop (leader arms + keyboard)

`teleop_leader_to_follower.py` drives the follower's arms from the leader arms, and
head/base/lift from the keyboard:

| Control | Keys |
|---------|------|
| Arms | leader arms follow (flips disabled — verified same-direction) |
| Head | `w`/`s` nod (up/down), `a`/`d` shake (left/right) |
| Base | `i`/`k` forward/back, `j`/`l` turn, `n`/`m` speed (0.3x/0.6x/1.0x) |
| Lift | `u`/`h` up/down (clamped 3–200mm) |
| Quit | `b` or Ctrl+C |

```bash
# Default: 3 cameras (head + left_wrist + right_wrist)
python3 examples/teleop_leader_to_follower.py

# Add the 4th chest camera
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

# Live camera view via Rerun (画面)
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6 --display

# Teleop only, no cameras
python3 examples/teleop_leader_to_follower.py --no-cameras
```

Camera arguments: `--cameras=head,left_wrist` (subset), `--head-camera /dev/videoN`,
`--left-wrist-camera`, `--right-wrist-camera`, `--chest-camera` (each overrides the
device path; passing a `--*-camera` arg auto-adds that camera).

### Camera devices & fps (tested)

| Camera | Device | Format | FPS |
|--------|--------|--------|-----|
| head | /dev/video0 | MJPG | 30 |
| left_wrist | /dev/video2 | MJPG | 30 |
| right_wrist | /dev/video4 | MJPG | **25** (hardware limit at 640x480) |
| chest | /dev/video6 | MJPG | 30 |

Verify with `lerobot-find-cameras opencv`. right_wrist cannot exceed 25fps in MJPG
at 640x480 (v4l2-ctl verified) — keep its `fps=25` in config or connect fails.

### Lift axis — zero persistence (免归零)

The lift is a 12-bit single-turn encoder (4096 ticks/rev) driving a leadscrew
(25 revs = 200mm). Absolute position is tracked in software via multi-turn wrap
tracking. Because the leadscrew is self-locking, the mechanical position survives
power cycles — so the zero position is persisted to `~/.cache/humanalite/lift_zero.json`
and restored on the next connect, **skipping re-homing**:

- First connect: homes to the bottom (stall detection), saves the zero.
- Later connects: restores the saved absolute position (no movement needed).
- If the position changed (e.g. the lift was moved manually), restore fails and
  auto-homing runs instead.

Lift tuning (tested): `v_max=110` (raw), `kp_vel=10`, `home_down_speed=10` with
Phase BIT2=0 (50 step/s per raw unit). Max speed ≈ 8.7mm/s (200mm in ~23s).

### Lift speed boost (BIT2=0)

The ST3250 firmware maps `Goal_Velocity` with Phase BIT2=1 at 1 step/s per raw unit,
where raw > 1000 wraps direction (triangular wave) — unsafe. Switching Phase BIT2=0
changes the unit to 50 step/s per raw, so full speed (5500 step/s) is just raw 110,
entirely inside the reliable range. **After switching, all velocity params must be
divided by 50** (`home_down_speed`, `kp_vel`, `v_max`). Tools:
`examples/switch_phase_bit2.py` (toggle), `examples/speed_test_bit2_0.py` (verify).

### Head tilt range unlock

The head tilt servo had its EPROM position limits baked to [1430, 2096] (~58°),
which the calibration file copied — limiting tilt to -54°/+4°. Writing
`Min=0 / Max=4095` unlocks the mechanical range [1367, 2242] (-61.6°/+17.1°):
`examples/unlock_head_tilt.py --probe`. After unlocking, the calibration file
(`~/.cache/huggingface/lerobot/calibration/robots/humanalite/follower.json`) was
updated to the real range.

## Data Collection

The `lerobot-record` CLI hardcodes official robot types and rejects `humanalite`
as an unrecognized choice. Use the Python API wrapper `examples/record_data.py`
instead — it exposes the **same parameter names** as `lerobot-record` and prints
the equivalent CLI command on startup for reference.

### 3 cameras (default)

```bash
python3 examples/record_data.py \
    --robot.type=humanalite \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
    --robot.confirm_lift_after_home=true \
    --teleop.type=humanalite_teleop \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=your-name/humanalite_demo \
    --dataset.single_task="describe your task" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true
```

### 4 cameras (with chest for navigation)

Same as above, but replace the `--robot.cameras` JSON to include chest:

```bash
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
```

> **Note**: camera names must be consistent across record / train / rollout.
> right_wrist is limited to **25fps** at 640x480 (hardware limit); all others are 30fps.

### Controls during recording

| Control | Keys |
|---------|------|
| Arms | leader arms follow (16 DOF) |
| Head | `w`/`s` nod, `a`/`d` shake (2 DOF) |
| Base | `i`/`k` forward/back, `j`/`l` turn (2 DOF, speed `n`/`m`) |
| Lift | `u`/`h` up/down with safety limits (1 DOF, clamped 3–200mm) |
| Record | `C` start, `Q` quit, `A` re-record episode |
| Confirm | After homing, hold `u`/`h` to position, `ENTER` to confirm |

The `--teleop.type=humanalite_teleop` teleoperator records **all 21 DOF** — the
leader arms (16 joints) plus keyboard-controlled head/lift/base (5 DOF). Both are
saved into the dataset for ACT training.

### Lift behavior during recording

- On first connect: lift **homes to bottom** (stall detection), saves the zero
  position to `~/.cache/humanalite/lift_zero.json`.
- On subsequent connects: lift **restores the saved position** (no homing needed),
  unless the position changed (manual push → restore fails → auto-home).
- After homing: keyboard hold `u`/`h` adjusts height with safety limits
  (3mm–200mm), `ENTER` to confirm and start recording.

### Resuming / cleaning datasets

If a dataset directory already exists from a previous run, delete it or resume:

```bash
rm -rf ~/.cache/huggingface/lerobot/your-name/humanalite_demo    # fresh start
# or add --dataset.resume=true to the record_data.py command     # continue from last episode
```

## Training

Train an ACT policy on a recorded dataset. The only required arguments are the
policy type, dataset, and output directory — all other parameters use ACT defaults.

### Quick start (test pipeline)

```bash
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanalite_act_policy \
    --dataset.repo_id=your-name/humanalite_act_demo \
    --output_dir=outputs/humanalite_act_demo \
    --batch_size=3 \
    --steps=5
```

### Production training (>50 episodes)

```bash
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanalite_act_policy \
    --dataset.repo_id=your-name/humanalite_act_demo \
    --output_dir=outputs/humanalite_act_demo \
    --batch_size=32 \
    --steps=50000
```

### Key parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--policy.type` | — | **Required.** Algorithm: `act`, `diffusion`, `smolvla`, `pi0`, etc. |
| `--policy.device` | `cuda` | Training device (`cuda` / `cpu`). |
| `--policy.push_to_hub` | `true` | Push model weights to HuggingFace Hub after training. |
| `--policy.repo_id` | — | Hub repo for the trained model (separate from dataset). Required when pushing. |
| `--dataset.repo_id` | — | **Required.** Hub repo of the training dataset. |
| `--output_dir` | — | Local directory for checkpoints and logs. |
| `--batch_size` | 8 | Samples per training step. Higher is more stable but uses more VRAM. |
| `--steps` | 100000 | Total training steps. For 900 frames (2 episodes), 50K steps is ~550 epochs. |

### ACT defaults (no need to set)

These are already the ACT defaults — setting them is optional:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `--policy.dim_model` | 512 | Transformer hidden dimension |
| `--policy.n_heads` | 8 | Attention heads |
| `--policy.n_encoder_layers` | 4 | Encoder layers |
| `--policy.n_decoder_layers` | 1 | Decoder layers |
| `--policy.n_action_steps` | 150 | Prediction horizon (frames) |
| `--policy.chunk_size` | 100 | Action chunking size |
| `--policy.vision_backbone` | resnet18 | Image encoder |
| `--policy.optimizer_lr` | 1e-05 | Learning rate |
| `--policy.optimizer_weight_decay` | 0.0001 | Weight decay |
| `--policy.optimizer_grad_clip_norm` | 10.0 | Gradient clipping |

### Outputs

```
outputs/humanalite_act_demo/
├── pretrained_model/           # Full model (config + weights)
├── last/pretrained_model       # Latest checkpoint
├── train_logs/                 # Training metrics (TensorBoard-compatible)
└── training_state.json         # Optimizer/scheduler state for resume
```

The pushed model will be at `https://huggingface.co/your-name/humanalite_act_policy`.

## Inference (Deployment)

Run a trained ACT policy on the real robot. Supports human override for safety.

```bash
python3 examples/eval_data.py \
    --policy.repo_id=your-name/humanalite_act_policy \
    --policy.device=cuda \
    --robot.type=humanalite \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
    --teleop.type=humanalite_teleop \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --num-episodes=5 \
    --duration=30 \
    --fps=30
```

### Controls during inference

| Control | Keys |
|---------|------|
| Policy toggle | `e` — switch between policy control and human override |
| Quit | `q` |

### Human override

- **Default** (policy mode): ACT model controls all 21 DOF automatically.
- **Press `e`** (override ON): arms follow leader, head/lift/base controlled by keyboard
- **Press `e` again** (override OFF): back to policy control

When overriding, keyboard controls remain active:
- Head: `w`/`s` (nod), `a`/`d` (shake)
- Base: `i`/`k` (forward/back), `j`/`l` (turn)
- Lift: `u`/`h` (up/down, clamped 3–200mm)

### Key parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--policy.repo_id` | — | **Required.** Hub repo of the trained model. |
| `--policy.device` | `cuda` | Inference device (`cuda` / `cpu`). |
| `--robot.*` | — | Robot config (same as record). |
| `--teleop.*` | — | Leader arm config (same as record). |
| `--num-episodes` | 5 | Number of inference episodes. |
| `--duration` | 30 | Seconds per episode. |
| `--fps` | 30 | Inference frequency (Hz). |

## License

Apache 2.0
