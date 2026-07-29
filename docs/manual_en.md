# HumanaLite Operation Manual

## Overview

HumanaLite is an open-source semi-humanoid robot built on LeRobot, featuring:

- **Dual arms**: 2 × 7 DOF + gripper (8× ST3215 C018 servos each)
- **Head**: 2 DOF (2× ST3215 C018 servos)
- **Lift**: Leadscrew-driven (1× ST3250 servo)
- **Base**: Differential drive (2× ST3215 C018 servos)
- **Cameras**: Head ×1 + left wrist ×1 + right wrist ×1

---

## 1. Hardware Setup

### 1.1 Servo Bill of Materials

| Position | Servo | Qty | ID |
|----------|-------|-----|----|
| Left follower arm J1-J7 + gripper | ST3215 C018 | 8 | 1-8 |
| Right follower arm J1-J7 + gripper | ST3215 C018 | 8 | 1-8 |
| Head Pan / Tilt | ST3215 C018 | 2 | 12, 13 |
| Lift leadscrew | ST3250 | 1 | 9 |
| Left / Right wheel | ST3215 C018 | 2 | 10, 11 |
| **Left leader arm** J1-J7 + gripper (teleop) | STS3215 C046 | 8 | 1-8 |
| **Right leader arm** J1-J7 + gripper (teleop) | STS3215 C046 | 8 | 1-8 |

### 1.2 Bus Topology

**3-bus mode (recommended):**

```
Bus 1 ── Left follower arm (1-8) + Head (12,13) ── POSITION mode
Bus 2 ── Right follower arm (1-8) ── POSITION mode
Bus 3 ── Lift (9) + Left wheel (10) + Right wheel (11) ── VELOCITY mode
```

**2-bus mode (port3=None):**

```
Bus 1 ── Left follower arm (1-8) + Head (12,13) ── POSITION mode
Bus 2 ── Right follower arm (1-8) + Lift (9) + Wheels (10,11) ── mixed mode
```

### 1.3 Leader Arms (Teleop)

Leader arms use STS3215 C046 servos (7.4V), connected to a separate laptop. Communication with the robot side can be via ZMQ (dual-machine) or direct USB (single-machine).

---

## 2. Software Installation

### 2.1 Install LeRobot

```bash
pip install lerobot[feetech]
```

### 2.2 Install HumanaLite

```bash
git clone <your-repo-url> /home/zach/HumanaLite
pip install -e /home/zach/HumanaLite
```

### 2.3 Verify Installation

```bash
python3 -c "from lerobot_robot_humanalite import HumanaLite; print('OK')"
```

---

## 3. Servo ID Configuration (First Use Only)

Configure IDs for new servos. **Connect one servo at a time to the Waveshare board.**

### 3.1 Wiring

- Connect Waveshare board to computer via USB
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

Follow the prompts: connect the indicated servo, press Enter, repeat.

### 3.3 Leader Arm IDs

Leader arm C046 servos also use IDs 1-8 (one set per arm), connected via another Waveshare board. Use the same `setup_motors()` method with the leader arm's port.

---

## 4. Calibration

### 4.1 Follower Robot Calibration

Calibration covers:
- **Joint servos**: half-turn homing + full range recording
- **Wheels**: full continuous rotation range (0-4095)
- **Lift**: stall-detection auto homing

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
robot = HumanaLite(HumanaLiteConfig())
robot.connect(calibrate=True)
"
```

Follow the prompts:
1. Press Enter to restore existing calibration, or type `c` for manual calibration
2. If manual:
   - Move left arm and head joints to mid-range → press Enter
   - Move each joint through full range → press Enter to stop recording
   - Repeat for right arm
3. Lift homes automatically via stall detection

### 4.2 Calibration File Location

`~/.cache/huggingface/lerobot/calibration/robots/humanalite/{id}.json`

Auto-loaded on next connection.

---

## 5. Operation Modes

### 5.1 Single Machine Mode (All devices on one computer)

All Waveshare boards and cameras connected to the same machine (laptop or Jetson):

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(
    port1="/dev/ttyACM0",   # left arm + head
    port2="/dev/ttyACM1",   # right arm
    port3="/dev/ttyACM2",   # lift + wheels
)
robot = HumanaLite(config)
robot.connect()

# Read observation
obs = robot.get_observation()
print(obs.keys())

# Send action (hold current position)
action = {k: obs[k] for k in obs if k.endswith(".pos")}
action["x.vel"] = 0.0
action["theta.vel"] = 0.0
action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)
robot.send_action(action)

robot.disconnect()
```

### 5.2 Dual-machine ZMQ Mode

**Robot side (Jetson / Raspberry Pi):**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost

host = HumanaLiteHost(HumanaLiteConfig())
host.run()
"
```

Default ports: obs 5556 / cmd 5555.

**Teleop side (Laptop):**

```python
from lerobot_robot_humanalite.humanalite_client import HumanaLiteClient
from lerobot_robot_humanalite import HumanaLiteClientConfig

client = HumanaLiteClient(
    HumanaLiteClientConfig(remote_ip="192.168.1.100")  # Robot IP
)
client.connect()

obs = client.get_observation()
# Connect leader arms or keyboard teleop
# ...

client.send_action(action)
client.disconnect()
```

---

## 6. Data Collection

### 6.1 Using lerobot-record

```bash
lerobot-record \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": 0, "fps": 30, "width": 640, "height": 480}, "left_wrist": {"type": "opencv", "index_or_path": 2, "fps": 30, "width": 640, "height": 480}, "right_wrist": {"type": "opencv", "index_or_path": 4, "fps": 30, "width": 640, "height": 480}}' \
    --teleop.type=openarm_mini \
    --teleop.port=/dev/ttyACM_leader \
    --dataset.repo_id=your_name/my_humanalite_data \
    --dataset.num_episodes=10 \
    --dataset.single_task="describe your task"
```

### 6.2 Dual-machine ZMQ Data Collection

**Robot side:**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
"
```

**Teleop side:** Run the recording script connected to the ZMQ stream. Observation comes from the robot, actions come from the leader arms connected to the laptop.

---

## 7. Model Training

After data collection, train on any machine:

```bash
lerobot-train \
    --policy=act \
    --dataset.repo_id=your_name/my_humanalite_data \
    --output_dir=./outputs
```

Override training parameters via CLI:

```bash
lerobot-train --policy=act --dataset.repo_id=... --training.batch_size=32 --training.epochs=100
```

Supported policies: `act`, `diffusion`, `pi0`, etc.

---

## 8. Model Deployment (Inference)

### 8.1 Single Machine

```bash
lerobot-rollout \
    --policy.path=./outputs/checkpoints/last \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2
```

### 8.2 Dual-machine ZMQ Inference

**Robot side runs ZMQ host, teleop side loads policy:**

```bash
# Robot side
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
"
```

Teleop side needs a custom script that loads the policy and sends actions via the ZMQ client.

---

## 9. Lift Operation

The lift uses an ST3250 servo driving an 8mm-lead leadscrew. Two control modes:

### 9.1 Height Control (recommended)

```python
# Read current height
height = obs["lift_axis.height_mm"]

# Set target height
action["lift_axis.height_mm"] = 200.0  # mm
```

### 9.2 Direct Velocity Control

```python
action["lift_axis.vel"] = 500  # raw velocity, positive=up, negative=down
```

### 9.3 Safety Guards

- **Descent floor**: blocks downward motion below `descent_floor_mm`
- **Soft limits**: protects motion within `soft_min_mm`..`soft_max_mm`
- **Stall detection**: automatic homing via current monitoring

---

## 10. Configuration Reference

### 10.1 HumanaLiteConfig

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port1` | `/dev/ttyACM0` | Left arm + head bus port |
| `port2` | `/dev/ttyACM1` | Right arm bus port |
| `port3` | `/dev/ttyACM2` | Lift + wheels bus port (None = 2-bus mode) |
| `use_degrees` | `False` | Use degrees vs -100..100 range |
| `wheel_radius` | 0.06 m | Wheel radius |
| `wheelbase` | 0.30 m | Distance between wheels |
| `max_wheel_raw` | 3000 | Max wheel velocity raw value |

### 10.2 LiftAxisConfig

| Parameter | Default | Description |
|-----------|---------|-------------|
| `motor_id` | 9 | Lift servo ID |
| `motor_model` | "sts3215" | Register table model (ST3250 compatible) |
| `lead_mm_per_rev` | 8.0 | Leadscrew lead (mm) |
| `belt_ratio` | 1.0 | Timing belt ratio (1 = direct drive) |
| `home_stall_current_ma` | 200 | Stall detection current threshold |
| `v_max` | 1500 | Max velocity command |
| `kp_vel` | 300.0 | Position→velocity P controller gain |

---

## 11. Troubleshooting

### Q: How to set servo IDs?

A: Use `robot.setup_motors()`. Connect one servo at a time to the Waveshare board and follow the prompts.

### Q: Device port (/dev/ttyACM0) changes after reboot?

A: Use udev rules to create symlinks:

```bash
# /etc/udev/rules.d/99-waveshare.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A1", SYMLINK+="tty_left_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A2", SYMLINK+="tty_right_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A3", SYMLINK+="tty_base"
```

Then use `/dev/tty_left_arm` etc. in your Config.

### Q: Different voltages for leader and follower?

A: Leader C046 servos (7.4V) and follower C018 servos (12V) use separate power supplies. In ZMQ dual-machine mode, each machine powers its own servos. In single-machine mode, use two power supplies for two Waveshare boards.

### Q: Lift too slow?

A: Direct-drive with 8mm lead gives ~10mm/s (400mm in ~40s). To speed up, increase `belt_ratio` (add timing belt) or use a larger-lead leadscrew.

### Q: Camera not found?

A: Check `/dev/video*` devices exist. Adjust camera indices in `default_cameras()`.

---

## 12. Project Structure

```
/home/zach/HumanaLite/
├── pyproject.toml                              # Package config + lerobot entry points
├── lerobot_robot_humanalite/                   # Main package
│   ├── __init__.py                             # Exports HumanaLite
│   ├── config_humanalite.py                    # Config classes
│   ├── humanalite.py                          # Main Robot class
│   ├── lift_axis.py                           # Lift axis control
│   ├── humanalite_host.py                     # ZMQ host (robot side)
│   └── humanalite_client.py                   # ZMQ client (teleop side)
├── examples/
│   ├── single_machine.py                      # Single machine example
│   └── teleop_keyboard.py                     # Keyboard teleop example
├── docs/
│   ├── manual_en.md                           # This file
│   └── manual_zh.md                           # 中文手册
└── README.md
```
