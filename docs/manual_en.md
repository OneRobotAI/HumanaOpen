# HumanaLite Complete Beginner Tutorial

Welcome to HumanaLite, an open-source semi-humanoid robot built on
[HuggingFace LeRobot](https://github.com/huggingface/lerobot). This tutorial is
written for people who just received the hardware and want to go from "box on
the table" to "robot following learned policies". Every parameter below was
verified against the actual code, and every pitfall in the FAQ is a real
problem we hit and fixed during field testing.

**Hardware overview:**

- **Dual arms**: 2 × 7 DOF + gripper (8× ST3215 C018 servos each)
- **Head**: 2 DOF (2× ST3215 C018 servos)
- **Lift**: Leadscrew-driven (1× **ST3250** servo, T8 leadscrew)
- **Base**: Differential drive (2× ST3215 C018 servos)
- **Cameras**: Head ×1 + left wrist ×1 + right wrist ×1
- **Leader arms** (teleop): 2 × 8 STS3215 C046 servos, run on a separate machine

> This project uses LeRobot **0.4.x**. PyPI has no `lerobot>=1.0` (the latest
> published version is 0.6.x), so HumanaLite no longer installs lerobot from
> PyPI. You install lerobot from a local source checkout instead, see
> [Section 2](#2-software-installation).

---

## 1. Hardware Setup

### 1.1 Servo Bill of Materials

| Position | Servo | Qty | ID |
|----------|-------|-----|----|
| Left follower arm J1-J7 + gripper | ST3215 C018 | 8 | 1-8 |
| Right follower arm J1-J7 + gripper | ST3215 C018 | 8 | 1-8 |
| Head Pan / Tilt | ST3215 C018 | 2 | 12, 13 |
| Lift leadscrew | **ST3250** | 1 | **9** |
| Left / Right wheel | ST3215 C018 | 2 | 10, 11 |
| **Left leader arm** J1-J7 + gripper (teleop) | STS3215 C046 | 8 | 1-8 |
| **Right leader arm** J1-J7 + gripper (teleop) | STS3215 C046 | 8 | 1-8 |

⚠️ **Follower servos run at 12V, leader servos at 7.4V.** Do not plug a leader
arm into a 12V board, and do not share a power supply between the two. Each
machine in a dual-machine setup powers its own servos.

### 1.2 Bus Topology

> **Left/right convention**: defined from the robot's own frame of reference.
> Standing behind the robot and facing the same direction as it, the arm on
> your left-hand side is the **left arm** (`port1`), the arm on your right-hand
> side is the **right arm** (`port2`). Wiring decides which physical arm is
> which; the software simply maps `left_arm_*` → `port1` and `right_arm_*` →
> `port2`.

**3-bus mode** (`port3="/dev/ttyACM2"`, the default):

```
Bus 1 ── Left follower arm (1-8) + Head (12,13) ── POSITION mode
Bus 2 ── Right follower arm (1-8) ── POSITION mode
Bus 3 ── Lift (9) + Left wheel (10) + Right wheel (11) ── VELOCITY mode
```

**2-bus mode** (`port3=None`): ⚠️ **this is what the project actually uses
on the test bench**:

```
Bus 1 ── Left follower arm (1-8) + Head (12,13) ── POSITION mode
Bus 2 ── Right follower arm (1-8) + Lift (9) + Wheels (10,11) ── mixed mode
```

In 2-bus mode, bus 2 carries both POSITION-mode servos (right arm) and
VELOCITY-mode servos (lift, wheels). The code handles this fine; each motor
group is written with its own operating mode.

⚠️ **`enable_base=False` disables the wheels *and* the lift.** This is meant
for arms-only bring-up (e.g. before the base is wired). If your wheels or lift
don't respond at all, check that `enable_base` is `True`.

### 1.3 First Connection Sanity Test

Do this right after wiring, before anything else. It verifies the USB buses
and motor power without needing cameras or calibration:

```bash
conda activate lerobot
python3 -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
config = HumanaLiteConfig(
    port1='/dev/ttyACM0',   # left arm + head
    port2='/dev/ttyACM1',   # right arm + lift + wheels (2-bus)
    port3=None,
    cameras={},             # skip cameras, motor tests work without them
)
robot = HumanaLite(config)
robot.connect(calibrate=False)
print('Connected OK')
robot.disconnect()
"
```

What to expect:

- `connect()` opens both buses, then **auto-homes the lift** (drives it down
  until stall, see [Section 9](#9-lift-operation)). Make sure the lift has
  room to travel down and 12V power.
- A warning about missing calibration is **normal** at this stage. See
  [Section 4](#4-calibration) and the FAQ.
- If you only wired the arms (no base, no lift), add `enable_base=False` to
  the config so `connect()` skips the lift entirely.

⚠️ If you already ran calibration before, `connect()` will print
`Press ENTER to restore calibration, or type 'c' to re-calibrate` and **block
waiting for keyboard input**. Interactive use is fine; for scripts, either
answer the prompt or calibrate first.

---

## 2. Software Installation

### 2.1 Create a Conda Environment

Use Python 3.12. A dedicated env avoids conflicts with the system Python.

```bash
conda create -n lerobot python=3.12
conda activate lerobot
```

⚠️ **Always use the lerobot env.** The system `python3` (e.g. conda base,
Python 3.13) often has no `numpy` installed, and the import will fail with a
confusing error. If `python3` from your shell does not say
`(lerobot)` in the prompt, activate the env first.

### 2.2 Install LeRobot from Local Source

As noted above, `lerobot>=1.0` does not exist on PyPI (latest is 0.6.x), and
this project targets the 0.4.x line. We install from a local source checkout:

```bash
pip install -e /home/zach/lerobot-so101-bimanual/lerobot
```

Adjust the path if your checkout lives elsewhere.

### 2.3 Install HumanaLite

HumanaLite's `pyproject.toml` deliberately has **no lerobot dependency** (the
locally installed lerobot provides it). Install the package itself with
`--no-deps` so pip does not try to resolve or upgrade lerobot:

```bash
cd /home/zach/HumanaLite
pip install -e . --no-deps
```

The editable install (`-e`) means any change you make to the HumanaLite
package takes effect immediately, no reinstall needed.

### 2.4 Verify the Installation (Important!)

```bash
cd /tmp && python -c "import lerobot_robot_humanalite; print('OK')"
```

⚠️ Run the check **outside** the project directory. If you run it from
`/home/zach/HumanaLite`, Python automatically adds the current directory to
the import path, so the import can succeed even when the package is not
actually installed. Running from `/tmp` forces a real installed-package check.

Expected output: `OK`.

---

## 3. Servo ID Configuration (First Use Only)

New servos ship with default IDs, so before first use you must burn the
correct IDs. **Connect one servo at a time to the Waveshare board.**

### 3.1 Wiring

- Connect the Waveshare board to the computer via USB
- **Connect only one servo** to the board at a time
- Power the servo (12V supply)

### 3.2 Run Setup

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(port1="/dev/ttyACM0", port2="/dev/ttyACM1")
robot = HumanaLite(config)

# Prompts you to connect each servo one by one
robot.setup_motors()
```

Follow the prompts: connect the indicated servo, press Enter, wait for the ID
to be written, repeat.

### 3.3 Leader Arm IDs

Leader arm C046 servos also use IDs 1-8 (one set per arm), connected via
another Waveshare board. Use the same `setup_motors()` method with the leader
arm's port.

### 3.4 Scan a Bus for Servos (Debug Tool)

To see which IDs are actually reachable on a bus, use a ping scan. **Call
`bus.connect()` first**, otherwise you get a `'NoneType'` flush error:

```python
from lerobot.motors.feetech import FeetechMotorsBus

bus = FeetechMotorsBus(port="/dev/ttyACM1", motors={})
bus.connect()                 # required before ping!
ids = bus.broadcast_ping()    # returns the set of reachable servo IDs
print("Found servo IDs:", ids)
bus.disconnect()
```

If a servo does not show up, see "Missing motor IDs" in
[Section 11](#11-troubleshooting).

---

## 4. Calibration

Calibration tells the software where each joint's zero and range are. It is
required for the full LeRobot pipeline (record / train / rollout), because
`get_observation()` can only return normalized joint positions once
calibration exists.

### 4.1 What Gets Calibrated

- **Joint servos** (arms, head): half-turn homing + full range recording
- **Wheels**: full continuous rotation range (0-4095)
- **Lift**: stall-detection auto homing (see [Section 9](#9-lift-operation))

### 4.2 Run Calibration

Recommended: use the calibration script (full step hints + post-calibration
verification):

```bash
conda activate lerobot
python3 examples/calibrate_follower.py
```

Or run manually:

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
robot = HumanaLite(HumanaLiteConfig(id='follower'))
robot.connect(calibrate=True)
"
```

Interactive flow, step by step:

1. If a calibration file already exists, you are asked:
   `Press ENTER to restore calibration, or type 'c' to re-calibrate`.
   Type `c` to re-calibrate.
2. **Bus 1**: move all left arm and head joints to the **zero pose** (arms
   hanging straight down, gripper closed) → press Enter.
   Then move each joint through its full range of motion → press Enter when
   done. The software records min/max positions per joint.
3. **Bus 2**: repeat for the right arm joints. The gripper gets a dedicated
   closed/open two-point calibration (0=closed, 100=open).
4. Wheels get a full 0-4095 range automatically, no interaction needed.
5. The lift homes automatically via stall detection.

**Zero convention (important)**: the follower and leader both use "**arms
hanging straight down + gripper closed**" as the zero pose. This way
teleoperation maps pose-to-pose (leader hanging → follower hanging), and
during data recording the `action`/`observation` normalization spaces are
physically consistent. When sweeping the ranges, move each joint **symmetrically
around the zero pose** so the range midpoint ≈ the zero pose.

⚠️ Move each joint slowly and through its real physical limits. The recorded
range is what the policy will treat as the full travel, so don't cheat it.

### 4.3 Calibration File Location

**Follower side**: `~/.cache/huggingface/lerobot/calibration/robots/humanalite/{id}.json`

```
.../humanalite/follower.json   ← follower calibration (id="follower")
```

The file is loaded automatically on the next `connect()`.

**Leader side** (teleop arms): stored under the teleoperators directory (see
Section 4.4), fully separate from the follower.

### 4.4 Leader (Teleop Arms) Calibration

The leader arms are open-arms-mini (STS3215 C046, 7.4 V), 8 servos per arm
(ID 1-8), with joint names matching the follower. Use the calibration script:

```bash
python3 examples/calibrate_leader.py
```

Per-arm interactive flow (default `calibration_mode="full"`, records real
travel):

1. **Arm hanging straight down + gripper closed** → Enter (sets zero point)
2. **Move each joint through its full travel** → Enter (records real min/max,
   consistent with the follower's normalization space)
3. **Gripper closed position** → Enter
4. **Gripper fully open position** → Enter
5. Calibration saved

**Why record real travel on the leader too?** When recording data for
training, `action` comes from the leader and `observation` from the follower.
If the leader used the full range while the follower records travel, the same
physical pose maps to different normalized values on each side (leader 50 ≠
follower 50), so the model learns a wrong mapping and the follower under/overshoots
at deployment. Recording real travel on the leader aligns both spaces
physically, so **one calibration serves both teleoperation and data
recording — no re-calibration needed**.

> If you only need real-time teleoperation (human compensates live), set
> `calibration_mode="quick"` (joints full range [0,4095], the official
> openarm_mini simplification). But switch back to `"full"` and re-calibrate
> before recording data for training.

Calibration files (separate from the follower, never overwrite):

```
~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_left.json
~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_right.json
```

Leader implementation (`lerobot_robot_humanalite/leader.py`):

- `humanalite_leader`: single-arm teleoperator (`calibration_mode`: `full`/`quick`)
- `bi_humanalite_leader`: bimanual teleoperator (outputs `left_arm_*` /
  `right_arm_*` prefixed actions)

During teleoperation, `leader.get_action()` produces action keys that match
`follower.send_action()` exactly, so the two connect with zero conversion.

**Direction flips / wrist remap (configurable)**:

The default `flip_joints` / `joint_remap` come from the official openarm_mini
(they encode the direction signature for the *official* leader+follower
pairing). **If your arms are assembled differently from official, some joints
rotate the wrong way and the wrist mapping may be off** — this is
hardware-related, not a bug. Characterize each joint with the diagnostic
script:

```bash
python3 examples/diagnose_teleop.py
```

Then configure per the results:

```python
config = BiHumanaLiteLeaderConfig(
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
    flip_joints={"left": ["shoulder_pan", ...], "right": [...]},  # reversed joints
    joint_remap={},  # empty dict if no wrist flex↔yaw swap needed
)
```

The gripper outputs [0,100] directly (0=closed, 100=open), matching the
follower's `RANGE_0_100` — no extra scaling.

⚠️ Leader arms run on 7.4 V (separate from the follower's 12 V); torque is
released during calibration so they can be moved by hand.

### 4.5 "No Calibration Registered" Is Expected Before Calibration

If you call `get_observation()` before calibrating, normalization has no
ranges to work with and the call fails (or returns unusable readings). This is
**normal**, not a bug. Two ways around it:

- Calibrate once (`connect(calibrate=True)`), then use `get_observation()`.
- For lift-only work, skip the full robot class and use the direct lift test,
  see [Section 9.4](#94-lift-axis-test).

---

## 5. Operation Modes

### 5.1 Single Machine Mode (All devices on one computer)

All Waveshare boards and cameras connected to the same machine:

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(
    port1="/dev/ttyACM0",   # left arm + head
    port2="/dev/ttyACM1",   # right arm
    port3="/dev/ttyACM2",   # lift + wheels (3-bus) or None for 2-bus
)
robot = HumanaLite(config)
robot.connect()

# Read observation
obs = robot.get_observation()
print(obs.keys())

# Hold current position: copy .pos keys, stop base and lift
action = {k: obs[k] for k in obs if k.endswith(".pos")}
action["x.vel"] = 0.0
action["theta.vel"] = 0.0
action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)
robot.send_action(action)

robot.disconnect()
```

Observation keys: one `.pos` per arm/head joint, plus `x.vel`, `theta.vel`,
`lift_axis.height_mm`, optionally `lift_axis.vel`, plus one entry per camera.

Ready-made examples:

```bash
# Single machine loop (read observation, hold position)
python3 examples/single_machine.py

# Keyboard teleoperation of base + lift (needs the `keyboard` package)
python3 examples/teleop_keyboard.py
```

### 5.2 Keyboard Teleop Keymap

From `teleop_keys` in the config (`teleop_keyboard.py`):

| Key | Action |
|-----|--------|
| `i` | Forward |
| `k` | Backward |
| `j` | Rotate left |
| `l` | Rotate right |
| `n` | Speed up |
| `m` | Speed down |
| `u` | Lift up |
| **`h`** | **Lift down** ⚠️ (project-specific: it is `h`, **not** `d`) |
| `b` | Quit |

⚠️ **Lift down is `h`, not `d`.** This is a deliberate project modification.
Muscle-memory from other robots will make you press `d` and nothing happens.

### 5.3 Dual-machine ZMQ Mode

**Robot side (Jetson / Raspberry Pi):**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost

host = HumanaLiteHost(HumanaLiteConfig())
host.run()
"
```

Default ZMQ ports: observations 5556 / commands 5555.

**Teleop side (Laptop):**

```python
from lerobot_robot_humanalite.humanalite_client import HumanaLiteClient
from lerobot_robot_humanalite import HumanaLiteClientConfig

client = HumanaLiteClient(
    HumanaLiteClientConfig(remote_ip="192.168.1.100")  # Robot IP
)
client.connect()

obs = client.get_observation()
# Connect leader arms or keyboard teleop here
# ...

client.send_action(action)
client.disconnect()
```

### 5.4 Arms-Only Mode

During bring-up, before the base is wired:

```python
config = HumanaLiteConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    enable_base=False,   # wheels AND lift are disabled
    cameras={},
)
```

With `enable_base=False`, the lift and wheel motors are never attached to any
bus, so bring-up of the arms won't touch them. Full observation keys that
depend on the base/lift are not available in this mode.

### 5.5 Keyboard Permissions & Base Test

**Keyboard library choice (Linux must-read)**

Two keyboard libraries with different permission requirements:

- **`pynput` (recommended)**: works **without root** on a desktop X11 session.
  Requires `DISPLAY` to be set (a desktop terminal has it by default).
- **`keyboard`**: **hard-requires root** on Linux (`ensure_root()` check);
  adding yourself to the `input` group does not help. Either run with `sudo`
  or switch to pynput.

```bash
# Install pynput
pip install pynput
```

**Base-only keyboard test**

A keyboard script that drives only the base, never touching arms or lift (no
calibration required):

```bash
python3 examples/test_base_keyboard.py
```

Keys: `i`/`k` forward/backward, `j`/`l` rotate left/right, `n`/`m` speed up/down
(3 levels: 0.05/0.10/0.20 m/s), `b` quit. Hold to move, release to stop.

> ⚠️ Lift the robot off the ground (wheels in the air) when testing base
> direction; if testing on the ground, make sure the area is clear.

> If you use the `keyboard` library and need `sudo`:
> `sudo /home/zach/miniconda3/envs/lerobot/bin/python examples/test_base_keyboard.py`
> (must use the full conda python path, otherwise sudo uses the system python
> and won't find the packages).

**Base direction fix (wheel mounted mirrored)**

If pressing `i` (forward) actually spins the robot in place, and `j` (rotate
left) drives it forward, one wheel is **mounted mirrored** (positive raw
velocity drives it backward). The differential command then makes the two
wheels counter-rotate, which reads as forward/rotate being swapped.

Fix: set the mirrored wheel to `-1` in the config:

```python
config = HumanaLiteConfig(
    ...
    wheel_dir_signs={
        "base_left_wheel": -1,   # left wheel mirrored → invert
        "base_right_wheel": 1,   # right wheel OK
    },
)
```

`+1` = positive raw velocity drives the wheel forward; `-1` = wheel is
mirrored. The sign is applied on both the command path
(`_body_to_wheel_raw`) and the feedback path (`_wheel_raw_to_body`) so the
body-frame estimate stays consistent. To tell which wheel is mirrored: press
`i`; if the robot turns left, the left wheel is mirrored; right, the right
wheel.

**Skipping lift homing**

`connect()` auto-homes the lift by default. When testing other subsystems and
the lift is at a known position, skip it:

```python
config = HumanaLiteConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,   # skip automatic lift homing
)
```

The lift is then only registered and configured (it never moves).

---

## 6. Data Collection

### 6.1 Using lerobot-record

```bash
conda activate lerobot
lerobot-record \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "fps": 30, "width": 640, "height": 480}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "fps": 30, "width": 640, "height": 480}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "fps": 30, "width": 640, "height": 480}}' \
    --teleop.type=openarm_mini \
    --teleop.port=/dev/ttyACM_leader \
    --dataset.repo_id=your_name/my_humanalite_data \
    --dataset.num_episodes=10 \
    --dataset.single_task="describe your task"
```

For a **2-bus** machine (what this project runs on the bench), just drop the
`--robot.port3` argument:

```bash
lerobot-record \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.cameras='{...same as above...}' \
    --teleop.type=openarm_mini \
    --teleop.port=/dev/ttyACM_leader \
    --dataset.repo_id=your_name/my_humanalite_data \
    --dataset.num_episodes=10 \
    --dataset.single_task="describe your task"
```

### 6.2 Finding Camera Indices

The default camera config in the code uses `/dev/video0` (head),
`/dev/video2` (left wrist) and `/dev/video4` (right wrist). To enumerate what
is actually present on your machine:

```bash
lerobot-find-cameras opencv
```

Adjust `index_or_path` in the `--robot.cameras` argument (or in
`default_cameras()` inside `config_humanalite.py`) to match. ⚠️ **Use the same
camera names and resolutions for collection, training and deployment.** The
pipeline keys observations by camera name, so `head` during recording must be
`head` during rollout.

### 6.3 Dual-machine ZMQ Data Collection

**Robot side:**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
"
```

**Teleop side:** run the recording script connected to the ZMQ stream.
Observations come from the robot; actions come from the leader arms connected
to the laptop.

---

## 7. Model Training

After data collection, training runs on any machine (even one without the
robot attached):

```bash
conda activate lerobot
lerobot-train \
    --policy.type=act \
    --dataset.repo_id=your_name/my_humanalite_data \
    --output_dir=./outputs
```

Override training parameters via CLI:

```bash
lerobot-train --policy.type=act --dataset.repo_id=... \
    --training.batch_size=32 --training.epochs=100
```

**Supported policies**: `act`, `diffusion`, `smolvla`, `pi0`, `pi05`,
`groot`, and more. The dataset format is shared, so switching policies is just
changing `--policy.type` and retraining.

---

## 8. Model Deployment (Inference)

### 8.1 Single Machine

```bash
conda activate lerobot
lerobot-rollout \
    --policy.path=./outputs/checkpoints/last \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2
```

⚠️ Before rollout, make sure the robot is calibrated (Section 4) and the
cameras are connected. Rollout sends learned actions directly to the hardware,
so keep a hand on the power switch and keep the emergency stop in mind
([Section 9.5](#95-emergency-stop-ctrl-c-does-not-stop-the-lift)).

### 8.2 Dual-machine ZMQ Inference

**Robot side runs the ZMQ host, teleop side loads the policy:**

```bash
# Robot side
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
"
```

The teleop side needs a custom script that loads the policy and sends the
resulting actions through the ZMQ client.

---

## 9. Lift Operation

The lift is a **ST3250** servo (ID 9) driving a **T8 leadscrew** (8.0 mm lead
per revolution) through a **direct drive** (`belt_ratio=1.0`, there is no
timing belt in the current build). Total travel is **300 mm** (`soft_max_mm`).

### 9.1 How connect() Homes the Lift

Every `connect()` call auto-homes the lift:

1. Drive **down** at `home_down_speed=1500` (raw velocity units).
2. Stop on stall, detected by a **dual safety** condition:
   - `Present_Current` exceeds `home_stall_current_ma=200`, **or**
   - the encoder position stops changing (position freeze).
   Two consecutive stall observations end homing.
3. Back off **5°** upward (`home_backoff_deg`) to relieve gear stress.
4. Record the current position as height zero.
5. Restore **VELOCITY mode + torque** automatically. The lift is now ready to
   control, no manual mode switching needed.

### 9.2 Height Control (recommended)

```python
# Read current height (mm, relative to homed zero)
height = obs["lift_axis.height_mm"]

# Set a target height (mm)
action["lift_axis.height_mm"] = 200.0
```

The lift runs a P controller in software:
`velocity = kp_vel * (target_height - current_height)`, clamped to `±v_max`.
With `kp_vel=500` and `on_target_mm=1`, it is considered "at target" when the
error is within 1 mm.

### 9.3 Direct Velocity Control

```python
action["lift_axis.vel"] = 500  # raw velocity units, positive=up, negative=down
```

### 9.4 Safety Guards

- **Descent floor**: `descent_floor_mm=3` is a hard guard. Downward commands
  are refused once height ≤ 3 mm. ⚠️ **Test targets must never go below 3 mm.**
- **Soft limits**: motion is blocked outside `soft_min_mm=0` … `soft_max_mm=280` (280mm leaves a 20mm mechanical safety margin on the 300mm leadscrew travel, so inertial overshoot can't hard-hit the mechanical top).
- **Stall detection**: homing stops automatically via current + freeze checks.

### 9.5 Emergency Stop: Ctrl+C Does NOT Stop the Lift ⚠️

Servos are hardware. Once the lift receives a velocity command, it keeps
spinning even if the Python process exits. Killing the script with Ctrl+C
alone **will not stop the lift**. Any script that commands the lift must handle
`KeyboardInterrupt` (or use `try/finally`) and explicitly write:

```python
bus.write("Goal_Velocity", "lift_axis", 0)
bus.write("Torque_Enable", "lift_axis", 0)
```

The example script below already does this. If you write your own scripts,
copy that pattern.

### 9.6 Lift Axis Test

Validate the lift hardware and software without arms, wheels or cameras:

```bash
conda activate lerobot
cd /home/zach/HumanaLite
python3 examples/test_lift_only.py
```

**Flow**: connect (only the lift motor, ID 9 on `/dev/ttyACM1`) → auto home
downward (stops on stall) → raise 50 mm → lower to 3 mm (the descent floor).

- ⚠️ **Safety**: the script handles Ctrl+C (writes `Goal_Velocity=0` +
  `Torque_Enable=0`, see Section 9.5).
- **Prerequisite**: lift servo (ID 9) wired on bus2 (`/dev/ttyACM1`), 12V
  powered.
- **Not needed**: arms, wheels, cameras, calibration. This test bypasses the
  full robot class and drives the motor directly, so it works before any
  calibration exists.

### 9.7 Velocity Unit Mismatch (Check Your Servo!)

The ST3250 velocity unit is set by the **Phase register (address 18), BIT2**:

| BIT2 | Velocity unit | Notes |
|------|---------------|-------|
| `0` | 0.732 RPM/raw | factory-style default, coarse |
| `1` | 0.0146 RPM/raw | fine-grained, **measured on this bench** |

The `v_max=3853` default in the code was tuned for **BIT2=1**
(0.0146 RPM/raw) and gives roughly **7.5 mm/s** (300 mm travel ≈ 40 s).

- If you assume the 0.732 unit, the equivalent `v_max` is about **77**. Using
  such a small value makes the lift barely move.
- A very large `v_max` value makes the lift shoot to full speed and overshoot.

To confirm **your** servo's unit before trusting the numbers:

```bash
python3 examples/check_phase.py
```

It reads the Phase register, prints BIT2, and tells you the matching `v_max`.
If your servo reports BIT2=0, set `v_max` accordingly (see
[Section 10.2](#102-liftaxisconfig)).

---

## 10. Configuration Reference

All values below are copied from the code. If the manual and the code ever
disagree, **the code wins**.

### 10.1 HumanaLiteConfig

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port1` | `/dev/ttyACM0` | Left arm + head bus port |
| `port2` | `/dev/ttyACM1` | Right arm bus port |
| `port3` | `/dev/ttyACM2` | Lift + wheels bus port (`None` = 2-bus mode) |
| `enable_base` | `True` | `False` = arms-only testing; wheels and lift are auto-disabled |
| `home_lift_on_connect` | `True` | `False` = skip the automatic lift homing in `connect()` (when testing other subsystems) |
| `disable_torque_on_disconnect` | `True` | Release torque on all servos at `disconnect()` |
| `max_relative_target` | `None` | Clamp per-step position changes (degrees or %); `None` = no clamp |
| `use_degrees` | `False` | Normalize joints in degrees vs the `-100..100` range |
| `cameras` | 3 × OpenCV | `head` = `/dev/video0`, `left_wrist` = `/dev/video2`, `right_wrist` = `/dev/video4` |
| `wheel_radius` | `0.0635` m | Wheel radius (127 mm wheel diameter) |
| `wheelbase` | `0.30` m | Distance between wheels |
| `max_wheel_raw` | `3000` | Max wheel velocity raw value |
| `wheel_dir_signs` | both `+1` | Wheel direction signs; set `-1` for a mirrored wheel (see 5.5) |
| `lift` | `LiftAxisConfig()` | Lift axis configuration (see 10.2) |
| `teleop_keys` | keymap | Keyboard teleop keys (see 10.3) |

### 10.2 LiftAxisConfig

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enabled` | `True` | Set `False` to disable the lift entirely |
| `name` | `"lift_axis"` | Motor name used as key on the bus |
| `motor_id` | `9` | Lift servo ID |
| `motor_model` | `"sts3250"` | Lift servo model (ST3250) |
| `lead_mm_per_rev` | `8.0` | Leadscrew travel in mm per output-shaft revolution (T8) |
| `belt_ratio` | `1.0` | Leadscrew revs per motor rev; `1` = direct drive, no belt |
| `soft_min_mm` | `0.0` | Software lower limit (mm) |
| `soft_max_mm` | `280.0` | Software upper limit (mm; 20mm safety margin on the 300mm travel) |
| `descent_floor_mm` | `3.0` | Hard guard; downward commands refused at or below this |
| `home_down_speed` | `1500` | Velocity command while homing downward (raw units) |
| `home_stall_current_ma` | `200` | Stall current threshold in mA |
| `home_backoff_deg` | `5.0` | Back off this many degrees after stall |
| `kp_vel` | `500.0` | P gain: `v_cmd = kp_vel * error_mm` |
| `v_max` | `3853` | Max absolute velocity command; ≈7.5 mm/s at BIT2=1 unit |
| `on_target_mm` | `1.0` | Deadband: "at target" when error ≤ 1 mm |
| `dir_sign` | `1` | `+1` = positive velocity raises the lift |

### 10.3 Keyboard Teleop Keymap (`teleop_keys`)

| Key | Action |
|-----|--------|
| `i` / `k` | Forward / Backward |
| `j` / `l` | Rotate left / Rotate right |
| `n` / `m` | Speed up / Speed down |
| `u` / **`h`** | Lift up / **Lift down** ⚠️ (`h`, not `d`) |
| `b` | Quit |

### 10.4 Host / Client Configs

| Config | Key fields | Defaults |
|--------|-----------|----------|
| `HumanaLiteHostConfig` | `port_zmq_cmd` / `port_zmq_observations` | 5555 / 5556 |
| `HumanaLiteClientConfig` | `remote_ip` | `127.0.0.1` |

---

## 11. Troubleshooting (Real Field Experience)

### Q: "Missing motor IDs" error

**Symptoms**: `connect()` fails because some servos are not found on a bus.

**Causes**:

1. **Daisy-chain break**: servos are chained bus-to-bus. A single broken wire
   or loose connector (e.g. between servo 6 and 7) makes servo 7 and everything
   after it unreachable.
2. **IDs not burned**: new servos still have factory/default IDs.

**Fix**: run the bus scan from [Section 3.4](#34-scan-a-bus-for-servos-debug-tool)
on each bus to see exactly which IDs respond. Then either fix the wiring or
run `setup_motors()`.

### Q: Device port (/dev/ttyACM0) changes after power cycle

**Symptom**: `connect()` fails with "port not found", or the arms are swapped
(left on the right bus).

**Explanation**: after power-cycling, Linux may reassign `ttyACM0`/`ttyACM1`
to different boards, and the two ports effectively swap.

**Fix**: confirm by serial number before connecting:

```bash
ls -l /dev/serial/by-id/
```

Then either update the ports in your config, or create udev symlinks:

```bash
# /etc/udev/rules.d/99-waveshare.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A1", SYMLINK+="tty_left_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A2", SYMLINK+="tty_right_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A3", SYMLINK+="tty_base"
```

Then use `/dev/tty_left_arm` etc. in your config.

### Q: "No calibration registered" when reading observations

**Symptom**: `get_observation()` fails before any calibration has been run.

**Explanation**: this is **expected**. Without calibration there are no
min/max ranges, so the bus cannot normalize raw positions into usable joint
values. It is not a hardware fault.

**Fix**: run calibration once (`connect(calibrate=True)`, Section 4). For
lift-only work that does not need calibration at all, use
`examples/test_lift_only.py`, which drives the lift motor directly and reads
`get_height_mm()` instead of `get_observation()`.

### Q: Lift does not move at all

Check, in order:

1. **Power**: the lift servo needs 12V. No power = no motion, no errors.
2. **Bus**: is the lift on the bus the config expects? In 2-bus mode
   (`port3=None`) it is on bus2 (`/dev/ttyACM1`). Wrong port = unreachable.
3. **enable_base**: with `enable_base=False` the lift is not attached at all.
4. **Mode and torque**: the lift must be in **VELOCITY** operating mode with
   **torque enabled**. `home()` restores both automatically; if you disabled
   torque manually, re-enable it. A position command while in velocity mode
   (or vice versa) does nothing useful.
5. **Command clamped**: if height is at the descent floor (≤ 3 mm) or the soft
   limits, downward/upward commands are refused by design. The lift is not
   broken, it is being guarded.

### Q: Lift moves, but way too slow or barely at all

**Cause**: velocity unit mismatch. The Phase register (address 18) BIT2 sets
the ST3250's velocity unit (Section 9.7). If the code's `v_max=3853` was tuned
for BIT2=1 but your servo is at BIT2=0 (0.732 RPM/raw), commands that look
right in code are far too small in hardware.

**Fix**: run `python3 examples/check_phase.py`, confirm BIT2, and set `v_max`
to the value it prints.

### Q: Lift overshoots or slams to full speed

**Cause**: `v_max` larger than what the actual velocity unit supports. With
the old-style value the servo hits full speed for the slightest height error
and overshoots the target badly.

**Fix**: keep `v_max=3853` for a BIT2=1 servo (verified on this bench), or the
value `check_phase.py` reports for your servo. If overshoot persists, lower
`kp_vel` (the P gain maps height error to velocity) so approach slows down
near the target.

### Q: Ctrl+C does not stop the lift

**Symptom**: you kill the script but the lift keeps going.

**Explanation**: servos are hardware. Once they receive a velocity command
they keep spinning; exiting Python does not stop them.

**Fix**: your script must catch `KeyboardInterrupt` (or use `try/finally`) and
explicitly write `Goal_Velocity=0` and `Torque_Enable=0` to the lift motor,
exactly like `examples/test_lift_only.py` does.

### Q: Pressing `d` does not lower the lift

**Answer**: lift down is **`h`**, not `d`. This is a deliberate project
modification (see `teleop_keys`). Use `u`/`h` for lift up/down.

### Q: Camera not found

**Fix**: check `/dev/video*` exists, then run
`lerobot-find-cameras opencv` to enumerate the real device indices. Update
`index_or_path` in your camera configs (`default_cameras()` or the
`--robot.cameras` argument). Keep names consistent across collect/train/deploy.

### Q: How to set servo IDs?

Use `robot.setup_motors()`. Connect one servo at a time to the Waveshare board
and follow the prompts (Section 3).

### Q: Different voltages for leader and follower?

Leader C046 servos run at 7.4V, follower C018 at 12V, with separate power
supplies. In ZMQ dual-machine mode each machine powers its own servos. In
single-machine mode use two power supplies for the two Waveshare boards.

### Q: Does `pip install -e /home/zach/HumanaLite` without `--no-deps` work?

No. HumanaLite deliberately declares no lerobot dependency, so `--no-deps` is
required to avoid pip resolving/upgrading anything. And remember to verify the
import from `/tmp` (Section 2.4), not from inside the repo.

---

## 12. Project Structure

```
/home/zach/HumanaLite/
├── pyproject.toml                              # Package config + lerobot entry points (no lerobot dep)
├── lerobot_robot_humanalite/                   # Main package
│   ├── __init__.py                             # Exports HumanaLite
│   ├── config_humanalite.py                    # Config classes (HumanaLiteConfig, LiftAxisConfig, ...)
│   ├── humanalite.py                           # Main Robot class (follower side)
│   ├── lift_axis.py                            # Lift axis with stall-detection homing
│   ├── leader.py                               # Leader teleoperator (single/bimanual, Section 4.4)
│   ├── humanalite_host.py                      # ZMQ host (robot side)
│   └── humanalite_client.py                    # ZMQ client (teleop side)
├── examples/
│   ├── single_machine.py                       # Single machine example (Section 5.1)
│   ├── teleop_keyboard.py                      # Keyboard teleop: i/k/j/l/n/m/u/h/b (Section 5.2)
│   ├── calibrate_follower.py                   # Full follower-side calibration (Section 4.2)
│   ├── calibrate_leader.py                     # Leader arm calibration (Section 4.4)
│   ├── diagnose_teleop.py                      # Teleop direction diagnosis (Section 4.4)
│   ├── test_base_keyboard.py                   # Base-only keyboard test (Section 5.5)
│   ├── test_lift_only.py                       # Lift axis test, homes + 50mm up + 3mm down (Section 9.6)
│   └── check_phase.py                          # Check lift servo velocity unit via Phase BIT2 (Section 9.7)
├── docs/
│   ├── manual_en.md                            # This file
│   └── manual_zh.md                            # 中文手册
└── README.md
```

---

## Quick Start Summary

```bash
# 1. Environment
conda create -n lerobot python=3.12
conda activate lerobot

# 2. LeRobot (local source, 0.4.x)
pip install -e /home/zach/lerobot-so101-bimanual/lerobot

# 3. HumanaLite
cd /home/zach/HumanaLite
pip install -e . --no-deps

# 4. Verify (from OUTSIDE the project dir!)
cd /tmp && python -c "import lerobot_robot_humanalite; print('OK')"

# 5. First connection (2-bus, no cameras)
cd /home/zach/HumanaLite
python3 -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
robot = HumanaLite(HumanaLiteConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}))
robot.connect(calibrate=False)
robot.disconnect()
print('Bring-up OK')
"

# 6. Lift alone
python3 examples/test_lift_only.py

# 7. Full pipeline
lerobot-record    --robot.type=humanalite --dataset.repo_id=you/data ...
lerobot-train     --policy.type=act --dataset.repo_id=you/data ...
lerobot-rollout   --policy.path=./outputs/checkpoints/last --robot.type=humanalite ...
```
