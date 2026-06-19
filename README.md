# OpenArmsX

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
openarmsx/
├── __init__.py           # Package exports
├── config_openarmsx.py   # OpenArmsXConfig, host/client configs
├── openarmsx.py          # OpenArmsX Robot class
├── lift_axis.py          # Lift axis with stall-detection homing
├── openarmsx_host.py     # ZMQ host (robot-side, for dual-machine mode)
└── openarmsx_client.py   # ZMQ client (teleop-side)
examples/
├── single_machine.py     # Single machine operation
└── teleop_keyboard.py    # Keyboard teleoperation via ZMQ
```

## Quick Start

```bash
# 1. Install lerobot with feetech support
pip install lerobot[feetech]

# 2. Install OpenArmsX (editable)
pip install -e /path/to/OpenArmsX

# 3. Single-machine operation
python -c "
from openarmsx import OpenArmsX, OpenArmsXConfig
config = OpenArmsXConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1')
robot = OpenArmsX(config)
robot.connect()
print(robot.get_observation().keys())
"

# 4. Dual-machine ZMQ mode (run on robot)
from openarmsx.openarmsx_host import OpenArmsXHost
OpenArmsXHost(OpenArmsXConfig()).run()
```

## License

Apache 2.0
