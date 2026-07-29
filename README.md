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
| Lift (leadscrew) | 1 | ST3215 C018 (1:345) + timing belt |
| Differential drive base | 2 | ST3215 C018 (1:345) |
| Leader arms (teleop) | 2 × 8 | STS3215 C046 (1:147) |

## Software

```
lerobot_robot_humanalite/
├── __init__.py              # Package exports
├── config_humanalite.py     # HumanaLiteConfig, host/client configs
├── humanalite.py            # HumanaLite Robot class
├── lift_axis.py             # Lift axis with stall-detection homing
├── humanalite_host.py       # ZMQ host (robot-side, for dual-machine mode)
└── humanalite_client.py     # ZMQ client (teleop-side)
examples/
├── single_machine.py        # Single machine operation
└── teleop_keyboard.py       # Keyboard teleoperation via ZMQ
```

## Quick Start

```bash
# 1. Install lerobot with feetech support
pip install lerobot[feetech]

# 2. Install HumanaLite (editable)
pip install -e /path/to/HumanaLite

# 3. Single-machine operation
python -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
config = HumanaLiteConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1')
robot = HumanaLite(config)
robot.connect()
print(robot.get_observation().keys())
"

# 4. Dual-machine ZMQ mode (run on robot)
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
```

## License

Apache 2.0
