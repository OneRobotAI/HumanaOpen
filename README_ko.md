# HumanaOpen
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

[English](README.md) | [中文](README_zh.md) | [Français](README_fr.md) | [한국어](README_ko.md)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

**오픈소스 줜휴머노이드 로봇 — 7-DOF 듀얼 암, 차동 구동, 리드스크류 리프트.**
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

[LeRobot](https://github.com/huggingface/lerobot) 및
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini) 기반.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 하드웨어
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 서브시스템 | 모터 | 모델 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|-----------|--------|-------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 왼쪽 팔로워 암 | 8 (7-DOF + 그리퍼) | ST3215 C018 (1:345) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 오른쪽 팔로워 암 | 8 (7-DOF + 그리퍼) | ST3215 C018 (1:345) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 헤드 (pan/tilt) | 2 | ST3215 C018 (1:345) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 리프트 (리드스크류) | 1 | ST3250 (직접 구동, 벨트 없음) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 차동 구동 베이스 | 2 | ST3215 C018 (1:345) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 리더 암 (텔레옵) | 2 × 8 | STS3215 C046 (1:147) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> **좌우 규약**: 로봇 자체 좌표계 기준.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> 로봇 뒤에서 같은 방향을 바라볼 때, 왼손 쪽이 **왼쪽 암**(`port1`),
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> 오른손 쪽이 **오른쪽 암**(`port2`). 배선이 물리적 암 위치를 결정하며,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> 소프트웨어는 `left_arm_*` → `port1`, `right_arm_*` → `port2`로 매핑합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 소프트웨어
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

lerobot_robot_humanaopen/
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── __init__.py              # 패키지 export
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── config_humanaopen.py     # HumanaOpenConfig, host/client 설정
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── humanaopen.py            # HumanaOpen Robot 클래스 (팔로워)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── lift_axis.py             # 스톨 감지 호밍 리프트 축
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── leader.py                # 리더 텔레오퍼레이터 (단일/바이매뉴얼)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── humanaopen_host.py       # ZMQ 호스트 (로봇 측, 듀얼 머신 모드)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

└── humanaopen_client.py     # ZMQ 클라이언트 (텔레옵 측)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

examples/
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── record_data.py              # 데이터 수집 (Python API, 전체 파라미터)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── eval_data.py                # 추론 (ACT 정책 배포)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── single_machine.py           # 단일 머신 작업
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── teleop_keyboard.py          # ZMQ 키보드 텔레오퍼레이션
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── teleop_leader_to_follower.py  # 전신 텔레옵: 리더 암 + 키보드
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── calibrate_follower.py       # 팔로워 전체 캘리브레이션 (암+헤드+휠+리프트)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── calibrate_leader.py         # 리더 암 캘리브레이션 (open-arms-mini)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── diagnose_teleop.py          # 텔레옵 조인트 방향 진단
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── test_base_keyboard.py       # 베이스 전용 키보드 테스트 (리프트/암 제외)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── test_lift_only.py           # 리프트 축 테스트 (호밍 + 상승/하강)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

└── check_phase.py              # 서보 속도 단위 확인 (Phase BIT2)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 진단 및 튜닝 도구
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 스크립트 | 용도 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|--------|---------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `diag_head_tilt_limits.py` | 헤드 틸트 기계 범위 탐침 (잠금 해제 전/후) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `diag_head_tilt_range.py` | 헤드 틸트 범위 진단 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `diag_regression.py` | 회귀 테스트 (리프트 + 카메라 + 텔레옵 시퀀스) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `diag_st3250_speed.py` | ST3250 모터 속도 프로파일링 (Phase BIT2=1) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `diag_follower_gripper.py` | 그리퍼 조인트 진단 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `recover_lift_ping.py` | 리프트 모터 통신 ping |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `speed_test_bit2_0.py` | BIT2=0 속도 검증 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `switch_phase_bit2.py` | ST3250 Phase BIT2 레지스터 전환 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 빠른 시작
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 1. conda 환경 생성
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

conda create -n humanaopen python=3.12
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

conda activate humanaopen
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 2. LeRobot 설치 (필수 의존성)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

pip install "lerobot[feetech]"
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 3. HumanaOpen 설치 (editable)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

cd /path/to/HumanaOpen
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

pip install -e . --no-deps
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 선택: SmolVLA 의존성 설치 (transformers, num2words)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

pip install -e ".[smolvla]" 2>/dev/null || pip install transformers>=4.48 num2words
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 선택: CUDA 12.8+ GPU (Blackwell / RTX 5060+)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 4. 설치 확인
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python -c "from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig; print('✅ OK')"
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 5. 단일 머신 작업
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python -c "
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

config = HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

robot = HumanaOpen(config)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

robot.connect()
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

print(robot.get_observation().keys())
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

"
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 6. 듀얼 머신 ZMQ 모드 (로봇에서 실행)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python -c "
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

from lerobot_robot_humanaopen import HumanaOpenConfig
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

HumanaOpenHost(HumanaOpenConfig(port1=/dev/ttyACM0, port2=/dev/ttyACM1, port3=None, cameras={})).run()
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

"
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

HumanaOpenHost(HumanaOpenConfig()).run()
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 텔레오퍼레이션
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 전신 텔레옵 (리더 암 + 키보드)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`teleop_leader_to_follower.py`는 리더 암으로 팔로워의 팔을 구동하고,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

키보드로 헤드/베이스/리프트를 제어합니다:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 제어 | 키 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|---------|------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 팔 | 리더 암 따름 (플립 비활성화 — 동일 방향 확인됨) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 헤드 | `w`/`s` 끄덕임 (상/하), `a`/`d` 흔들기 (좌/우) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 베이스 | `i`/`k` 전진/후진, `j`/`l` 회전, `n`/`m` 속도 (0.3x/0.6x/1.0x) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 리프트 | `u`/`h` 상승/하강 (3–200mm 제한) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 종료 | `b` 또는 Ctrl+C |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 기본: 3개 카메라 (head + left_wrist + right_wrist)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/teleop_leader_to_follower.py
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 4번째 chest 카메라 추가
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# Rerun 실시간 카메라 뷰
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6 --display
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 카메라 없이 텔레옵만
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/teleop_leader_to_follower.py --no-cameras
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

카메라 인자: `--cameras=head,left_wrist` (부분 집합), `--head-camera /dev/videoN`,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`--left-wrist-camera`, `--right-wrist-camera`, `--chest-camera` (각각 디바이스 경로 재정의;
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`--*-camera` 인자를 전달하면 해당 카메라가 자동 추가됩니다).
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 카메라 디바이스 및 fps (테스트됨)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 카메라 | 디바이스 | 포맷 | FPS |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|--------|--------|--------|-----|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| head | /dev/video0 | MJPG | 30 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| left_wrist | /dev/video2 | MJPG | 30 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| right_wrist | /dev/video4 | MJPG | **25** (640x480 하드웨어 한계) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| chest | /dev/video6 | MJPG | 30 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`lerobot-find-cameras opencv`로 확인하세요. right_wrist는 MJPG 640x480에서
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

25fps를 초과할 수 없습니다 (v4l2-ctl 검증) — 설정에서 `fps=25`을 유지하지 않으면 연결 실패.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 리프트 축 — 영점 영속화 (免归零)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

리프트는 12비트 싱글턴 엔코더(4096 ticks/rev)가 리드스크류(25회전 = 200mm)를 구동합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

절대 위치는 소프트웨어 멀티턴 랩 어라운드 트래킹으로 추적됩니다. 리드스크류가 자체 잠금되므로
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

전원 사이클 후에도 기계적 위치가 유지됩니다 — 영점 위치가 `~/.cache/humanaopen/lift_zero.json`에
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

영속화되어 다음 연결 시 복원되며, **재호밍을 건너뜁니다**:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 첫 연결: 하단까지 하강 (스톨 감지), 영점 저장.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 이후 연결: 저장된 절대 위치 복원 (이동 불필요).
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 위치가 변경된 경우 (예: 수동으로 리프트 이동), 복원 실패 시 자동 호밍 실행.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

리프트 튜닝 (테스트됨): `v_max=110` (raw), `kp_vel=10`, `home_down_speed=10`,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

Phase BIT2=0 (raw 유닛당 50 step/s). 최대 속도 ≈ 8.7mm/s (200mm 약 23s).
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 리프트 속도 부스트 (BIT2=0)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

ST3250 펌웨어는 Phase BIT2=1에서 `Goal_Velocity`를 raw 유닛당 1 step/s로 매핑하며,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

raw > 1000에서 방향이 반전됩니다 (삼각파) — 위험합니다. Phase BIT2=0으로 전환하면
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

단위가 raw 유닛당 50 step/s로 변경되어, 최대 속도(5500 step/s)는 raw 110에 해당하며
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

완전히 신뢰 가능한 범위 내입니다. **전환 후 모든 속도 파라미터를 50으로 나눠야 합니다**
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

(`home_down_speed`, `kp_vel`, `v_max`). 도구:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`examples/switch_phase_bit2.py` (전환), `examples/speed_test_bit2_0.py` (검증).
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 헤드 틸트 범위 잠금 해제
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

헤드 틸트 서보의 EPROM 위치 한계가 [1430, 2096] (~58°)로 고정되어 있었고,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

캘리브레이션 파일이 이를 복사했습니다 — 틸트가 -54°/+4°로 제한됩니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`Min=0 / Max=4095`를 쓰면 기계적 범위 [1367, 2242] (-61.6°/+17.1°)이 잠금 해제됩니다:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`examples/unlock_head_tilt.py --probe`. 잠금 해제 후 캘리브레이션 파일
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

(`~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json`)이
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

실제 범위로 업데이트되었습니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 데이터 수집
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`lerobot-record` CLI는 공식 로봇 타입만 하드코딩하여 `humanaopen`을
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

인식 불가능한 선택으로 거부합니다. 대신 Python API 래퍼 `examples/record_data.py`를
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

사용하세요 — `lerobot-record`와 **동일한 파라미터 이름**을 노출하며 시작 시
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

참조용 동등 CLI 명령을 출력합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 3개 카메라 (기본)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/record_data.py \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.type=humanaopen \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.id=follower \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port1=/dev/ttyACM0 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port2=/dev/ttyACM1 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port3=None \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.confirm_lift_after_home=true \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.type=humanaopen_teleop \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.left_arm_port=/dev/ttyACM2 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.right_arm_port=/dev/ttyACM3 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.flip_joints='{"left": [], "right": []}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.joint_remap='{}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.repo_id=your-name/humanaopen_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.single_task="작업을 설명하세요" \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.num_episodes=2 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.episode_time_s=15 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.reset_time_s=10 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.fps=30 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.push_to_hub=true
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 4개 카메라 (네비게이션용 chest 포함)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

위와 동일하며 `--robot.cameras` JSON에 chest를 추가:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> **주의**: 카메라 이름은 수집/학습/배포 간 일치해야 합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> right_wrist는 640x480에서 **25fps**로 제한됩니다 (하드웨어 한계); 나머지는 30fps.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 녹화 중 컨트롤
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 제어 | 키 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|---------|------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 팔 | 리더 암 따름 (16 DOF) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 헤드 | `w`/`s` 끄덕임, `a`/`d` 흔들기 (2 DOF) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 베이스 | `i`/`k` 전진/후진, `j`/`l` 회전 (2 DOF, 속도 `n`/`m`) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 리프트 | `u`/`h` 안전 한계 포함 상승/하강 (1 DOF, 3–200mm 제한) |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 녹화 | `C` 시작, `Q` 종료, `A` 에피소드 재녹화 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 확인 | 호밍 후 `u`/`h`로 위치 조정, `ENTER`로 확인 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

`--teleop.type=humanaopen_teleop` 텔레오퍼레이터는 **전체 21 DOF**를 기록합니다 —
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

리더 암(16 조인트)과 키보드 제어 헤드/리프트/베이스(5 DOF). 둘 다 ACT 학습용
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

데이터셋에 저장됩니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 녹화 중 리프트 동작
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 첫 연결: 리프트가 **하단으로 호밍** (스톨 감지), 영점을 `~/.cache/humanaopen/lift_zero.json`에 저장.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 이후 연결: 리프트가 **저장된 위치 복원** (호밍 불필요),
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

  위치가 변경된 경우 제외 (수동 밀기 → 복원 실패 → 자동 호밍).
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- 호밍 후: 키보드 `u`/`h`를 눌러 안전 한계 내에서 높이 조정
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

  (3mm–200mm), `ENTER`로 확인 후 녹화 시작.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 데이터셋 재개/정리
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

이전 실행에서 데이터셋 디렉토리가 이미 존재하는 경우 삭제하거나 재개:
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

rm -rf ~/.cache/huggingface/lerobot/your-name/humanaopen_demo    # 새로 시작
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 또는 record_data.py 명령에 --dataset.resume=true 추가           # 마지막 에피소드부터 계속
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 학습
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### ACT (action chunking transformer)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 빠른 테스트 (2 에피소드)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

lerobot-train \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.type=act \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.device=cuda \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.push_to_hub=true \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.repo_id=your-name/humanaopen_act_policy \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --output_dir=outputs/humanaopen_act_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --batch_size=3 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --steps=5
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 프로덕션 (>50 에피소드)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

lerobot-train \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.type=act \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.device=cuda \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.push_to_hub=true \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.repo_id=your-name/humanaopen_act_policy \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --output_dir=outputs/humanaopen_act_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --batch_size=32 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --steps=50000
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### SmolVLA (vision-language-action model)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

SmolVLA는 녹화 중 사용된 `--dataset.single_task`의 언어 지시가 필요합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

VLM 가중치(~500M)는 첫 실행 시 HuggingFace에서 자동 다운로드됩니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

# 빠른 테스트 (2 에피소드)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

lerobot-train \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.type=smolvla \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.device=cuda \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.push_to_hub=true \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.repo_id=your-name/humanaopen_smolvla_policy \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --output_dir=outputs/humanaopen_smolvla_demo \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --batch_size=4 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --steps=20
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> **참고**: SmolVLA(~450M params)는 ACT(~52M)보다 ~20배 무겁고, 더 많은 VRAM을 사용하며,
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> 학습이 느립니다. Batch size 4는 8GB VRAM(RTX 5060 Ti)에 적합합니다. >50 에피소드의 경우
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> steps를 20000+로 증가시키세요.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 주요 파라미터
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 파라미터 | 기본값 | 설명 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|-----------|---------|-------------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--policy.type` | — | **필수.** `act`, `smolvla`, `diffusion` 등. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--policy.device` | `cuda` | `cuda` / `cpu`. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--policy.push_to_hub` | `true` | 학습 후 HuggingFace Hub에 모델 푸시. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--policy.repo_id` | — | 학습된 모델의 Hub repo. 푸시 시 필수. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--dataset.repo_id` | — | **필수.** 학습 데이터셋의 Hub repo. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--output_dir` | — | 로컬 체크포인트 디렉토리. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--batch_size` | 8 | 스텝당 샘플 수. ACT: 32, SmolVLA: 4 (8GB VRAM 한계). |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| `--steps` | 100000 | 총 학습 스텝. ACT: 50K, SmolVLA: 20K. |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 출력
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

outputs/humanaopen_act_demo/
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── pretrained_model/           # 전체 모델 (설정 + 가중치)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── last/pretrained_model       # 최신 체크포인트
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

├── train_logs/                 # 학습 메트릭 (TensorBoard 호환)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

└── training_state.json         # 옵티마이저/스케줄러 상태 (재개용)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

푸시된 모델은 `https://huggingface.co/your-name/humanaopen_act_policy`에 있습니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 추론 (배포)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> **의존성**: SmolVLA는 `transformers>=4.48` 및 `num2words`가 필요합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> SmolVLA 추론 실행 전 `pip install transformers>=4.48 num2words`로 설치하세요.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### ACT 추론 (휴먼 오버라이드 포함)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/eval_data.py \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.type=act \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.repo_id=your-name/humanaopen_act_policy \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.device=cuda \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.type=humanaopen \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.id=follower \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port1=/dev/ttyACM0 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port2=/dev/ttyACM1 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port3=None \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.type=humanaopen_teleop \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.left_arm_port=/dev/ttyACM2 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.right_arm_port=/dev/ttyACM3 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.flip_joints='{"left": [], "right": []}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --teleop.joint_remap='{}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --num-episodes=5 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --duration=30 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --fps=30
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### SmolVLA 추론 (언어 조건부, 오버라이드 없음)
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```bash
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

python3 examples/eval_data.py \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.type=smolvla \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.repo_id=your-name/humanaopen_smolvla_policy \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --policy.device=cuda \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --task="wave hello with both arms" \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.type=humanaopen \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.id=follower \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port1=/dev/ttyACM0 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port2=/dev/ttyACM1 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.port3=None \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --num-episodes=2 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --duration=10 \
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

    --fps=10
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

```
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> **SmolVLA 성능 참고**: VLM 추론은 ~1s/frame (450M params). 10s 에피소드를
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> 10fps = 100 frames로 실행하면 ≈ 100s 실제 대기 시간. 실시간 배포에는
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

> ACT(~50ms/frame)를 사용하세요. SmolVLA는 언어 조건부 작업에 가장 적합합니다.
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

### 추론 중 컨트롤
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 제어 | 키 | 참고 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

|---------|------|-------|
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| Override (ACT 전용) | `e` (누르는 중) | 팔을 리더 제어로 전환 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

| 종료 | `q` | 모든 에피소드 중지 |
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

**휴먼 오버라이드** (ACT 전용):
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- `e` 누르는 중: 팔이 리더를 따름, 헤드/리프트/베이스는 키보드, 정책 일시 중지
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

- `e` 놓기: 정책 제어로 복귀
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

## 라이선스
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)


## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

Apache 2.0
## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어(서보 + 카메라)는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도의 GPU 머신에서 실행됩니다. 두 머신은 ZMQ로 통신합니다.

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│  개발 머신 (GPU)      │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 정책 추론          │   ←── action (21DOF) │  • 서보/카메라 읽기   │
│  • ACT / SmolVLA     │                       │  • 액션 실행         │
│  • 서보 배선 불필요   │                       │  • 서보+카메라 배선  │
└──────────────────────┘                       └──────────────────────┘
```

### 라즈베리파이 (Host 전용 — GPU 추론 없음)

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson (Host + 선택적 로컬 추론)

```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **참고**: Jetson은 ACT 추론을 로컬에서 실행할 수 있습니다 (Orin에서 ~100ms/frame),
> 하지만 SmolVLA는 전용 GPU가 필요하며 개발 머신에서 실행해야 합니다.

### 개발 머신 (클라이언트 — 정책 추론)

GPU 머신에서 로봇 IP에 연결:

```bash
conda activate humanaopen
export ROBOT_IP=192.168.1.100

python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 네트워크 요구사항

- 두 머신이 동일한 LAN에 있어야 함 (지연 시간을 위해 WiFi보다 이더넷 권장)
- 포트 **5555**(명령) 및 **5556**(관측)이 열려 있어야 함
- 이미지 스트리밍 대역폭: 카메라당 ~10 Mbps (640x480 MJPG)

