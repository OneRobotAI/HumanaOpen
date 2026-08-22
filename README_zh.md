# HumanaOpen
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

[English](README.md) | [中文](README_zh.md) | [Français](README_fr.md) | [한국어](README_ko.md)
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

**开源半人形机器人 — 7自由度双臂、差速底盘、丝杠升降。**
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

基于 [LeRobot](https://github.com/huggingface/lerobot) 和
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini) 构建。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 硬件
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 子系统 | 电机 | 型号 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|-----------|--------|-------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 左从臂 | 8（7-DOF + 夹爪）| ST3215 C018 (1:345) |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 右从臂 | 8（7-DOF + 夹爪）| ST3215 C018 (1:345) |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 头部（pan/tilt）| 2 | ST3215 C018 (1:345) |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 升降（丝杠）| 1 | ST3250（直驱，无皮带）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 差速底盘 | 2 | ST3215 C018 (1:345) |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 主臂（遥操）| 2 × 8 | STS3215 C046 (1:147) |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> **左右约定**：以机器人自身坐标系为准。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 站在机器人后方面向同一方向，你左手边的臂是**左臂**（`port1`），
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 右手边是**右臂**（`port2`）。接线决定物理臂的位置；
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 软件将 `left_arm_*` 映射到 `port1`，`right_arm_*` 映射到 `port2`。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 软件
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

lerobot_robot_humanaopen/
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── __init__.py              # 包导出
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── config_humanaopen.py     # HumanaOpenConfig, host/client 配置
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── humanaopen.py            # HumanaOpen Robot 类（从动侧）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── lift_axis.py             # 升降轴（堵转检测归零）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── leader.py                # 主臂遥操作器（单臂/双臂）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── humanaopen_host.py       # ZMQ 主机端（机器人侧，双机模式）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

└── humanaopen_client.py     # ZMQ 客户端（遥操侧）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

examples/
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── record_data.py              # 数据采集（Python API，全参数）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── eval_data.py                # 推理（ACT 策略部署）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── single_machine.py           # 单机操作
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── teleop_keyboard.py          # 键盘遥操作（ZMQ）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── teleop_leader_to_follower.py  # 全身遥操：主臂 + 键盘
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── calibrate_follower.py       # 从动侧完整校准（臂+头+轮+升降）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── calibrate_leader.py         # 主臂校准（open-arms-mini）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── diagnose_teleop.py          # 遥操关节方向诊断
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── test_base_keyboard.py       # 底盘键盘测试（不含升降/手臂）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── test_lift_only.py           # 升降轴测试（归零 + 升降）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

└── check_phase.py              # 检查舵机速度单位（Phase BIT2）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 诊断与调参工具
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 脚本 | 用途 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|--------|---------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `diag_head_tilt_limits.py` | 头部俯仰机械行程探测（解锁前/后）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `diag_head_tilt_range.py` | 头部俯仰行程诊断 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `diag_regression.py` | 回归测试（升降 + 摄像头 + 遥操序列）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `diag_st3250_speed.py` | ST3250 电机速度分析（Phase BIT2=1）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `diag_follower_gripper.py` | 夹爪关节诊断 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `recover_lift_ping.py` | 升降电机通信 ping |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `speed_test_bit2_0.py` | BIT2=0 速度验证 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `switch_phase_bit2.py` | 切换 ST3250 Phase BIT2 寄存器 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 快速开始
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 1. 创建 conda 环境
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

conda create -n humanaopen python=3.12
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

conda activate humanaopen
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 2. 安装 LeRobot（必需依赖）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

pip install "lerobot[feetech]"
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 3. 安装 HumanaOpen（editable 模式）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

cd /path/to/HumanaOpen
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

pip install -e . --no-deps
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 可选：安装 SmolVLA 依赖（transformers, num2words）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

pip install -e ".[smolvla]" 2>/dev/null || pip install transformers>=4.48 num2words
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 可选：GPU CUDA 12.8+（Blackwell / RTX 5060+）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 4. 验证安装
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python -c "from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig; print('✅ OK')"
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 5. 单机操作
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python -c "
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

config = HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

robot = HumanaOpen(config)
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

robot.connect()
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

print(robot.get_observation().keys())
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

"
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 6. 双机 ZMQ 模式（⚠️ 仅限 Jetson/树莓派双机部署 — 单机跳过）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 在机器人端 (Jetson/RPi) 运行，不在开发机上运行
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python -c "
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

from lerobot_robot_humanaopen import HumanaOpenConfig
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

HumanaOpenHost(HumanaOpenConfig(port1=/dev/ttyACM0, port2=/dev/ttyACM1, port3=None, cameras={})).run()
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

"
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

HumanaOpenHost(HumanaOpenConfig()).run()
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 遥操作
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 全身遥操（主臂 + 键盘）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`teleop_leader_to_follower.py` 通过主臂控制从臂，键盘控制头部/底盘/升降：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 控制 | 按键 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|---------|------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 双臂 | 主臂跟随（已禁用翻转 — 方向实测一致）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 头部 | `w`/`s` 点头（上下），`a`/`d` 摇头（左右）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 底盘 | `i`/`k` 前进/后退，`j`/`l` 转向，`n`/`m` 速度（0.3x/0.6x/1.0x）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 升降 | `u`/`h` 升/降（限位 3–200mm）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 退出 | `b` 或 Ctrl+C |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 默认：3 个摄像头（head + left_wrist + right_wrist）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/teleop_leader_to_follower.py
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 加第 4 个胸口摄像头
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# Rerun 实时画面
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6 --display
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 纯遥操，无摄像头
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/teleop_leader_to_follower.py --no-cameras
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

摄像头参数：`--cameras=head,left_wrist`（子集），`--head-camera /dev/videoN`，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`--left-wrist-camera`，`--right-wrist-camera`，`--chest-camera`（每个覆盖设备路径；
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

传入 `--*-camera` 参数会自动添加该摄像头）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 摄像头设备与帧率（实测）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 摄像头 | 设备 | 格式 | FPS |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|--------|--------|--------|-----|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| head | /dev/video0 | MJPG | 30 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| left_wrist | /dev/video2 | MJPG | 30 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| right_wrist | /dev/video4 | MJPG | **25**（640x480 硬件限制）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| chest | /dev/video6 | MJPG | 30 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

用 `lerobot-find-cameras opencv` 验证。right_wrist 在 MJPG 640x480 下不能超过 25fps
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

（v4l2-ctl 已验证）— 配置中保持 `fps=25` 否则连接失败。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 升降轴 — 零位持久化（免归零）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

升降使用 12 位单圈编码器（4096 ticks/圈）驱动丝杠（25 圈 = 200mm）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

绝对位置通过软件多圈环绕跟踪。由于丝杠自锁，断电后机械位置不变——
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

零位持久化到 `~/.cache/humanaopen/lift_zero.json`，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

下次连接时恢复，**跳过重新归零**：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 首次连接：下降到底部（堵转检测），保存零位。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 后续连接：恢复保存的绝对位置（无需移动）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 如果位置变了（如手动推动升降），恢复失败，自动执行归零。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

升降调参（实测）：`v_max=110`（raw），`kp_vel=10`，`home_down_speed=10`，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

Phase BIT2=0（50 step/s per raw unit）。最大速度 ≈ 8.7mm/s（200mm 约 23s）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 升降提速（BIT2=0）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

ST3250 固件将 `Goal_Velocity` 在 Phase BIT2=1 时映射为 1 step/s per raw unit，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

raw > 1000 会方向反转（三角波回绕）— 不安全。切换 Phase BIT2=0 后单位变为
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

50 step/s per raw unit，满速（5500 step/s）只需 raw 110，完全在可靠范围内。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

**切换后所有速度参数必须除以 50**（`home_down_speed`, `kp_vel`, `v_max`）。工具：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`examples/switch_phase_bit2.py`（切换），`examples/speed_test_bit2_0.py`（验证）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 头部俯仰行程解锁
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

头部俯仰舵机的 EPROM 位置限制被固定为 [1430, 2096]（~58°），
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

校准文件复制了这个限制 — 俯仰被限制在 -54°/+4°。写入
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`Min=0 / Max=4095` 解锁机械行程 [1367, 2242]（-61.6°/+17.1°）：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`examples/unlock_head_tilt.py --probe`。解锁后校准文件
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

（`~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json`）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

已更新为真实范围。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 数据采集
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`lerobot-record` CLI 硬编码了官方机器人类型，会拒绝 `humanaopen`
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

作为未识别的选项。使用 Python API 封装 `examples/record_data.py`
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

代替 — 它暴露与 `lerobot-record` **相同的参数名**，启动时打印等效 CLI 命令供参考。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 3 摄像头（默认）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/record_data.py \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.type=humanaopen \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.id=follower \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port1=/dev/ttyACM0 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port2=/dev/ttyACM1 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port3=None \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.confirm_lift_after_home=true \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.type=humanaopen_teleop \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.left_arm_port=/dev/ttyACM2 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.right_arm_port=/dev/ttyACM3 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.flip_joints='{"left": [], "right": []}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.joint_remap='{}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.repo_id=your-name/humanaopen_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.single_task="描述你的任务" \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.num_episodes=2 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.episode_time_s=15 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.reset_time_s=10 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.fps=30 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.push_to_hub=true
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 4 摄像头（含胸口导航摄像头）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

与上面相同，替换 `--robot.cameras` JSON 加入 chest：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> **注意**：摄像头名称必须在采集/训练/推理之间保持一致。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> right_wrist 在 640x480 下限制为 **25fps**（硬件限制）；其他均为 30fps。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 录制时的控制
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 控制 | 按键 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|---------|------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 双臂 | 主臂跟随（16 DOF）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 头部 | `w`/`s` 点头，`a`/`d` 摇头（2 DOF）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 底盘 | `i`/`k` 前后，`j`/`l` 转向（2 DOF，速度 `n`/`m`）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 升降 | `u`/`h` 升/降带安全限位（1 DOF，限位 3–200mm）|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 录制 | `C` 开始，`Q` 退出，`A` 重录当前 episode |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 确认 | 归零后按住 `u`/`h` 定位，`ENTER` 确认 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

`--teleop.type=humanaopen_teleop` 遥操作器记录**全部 21 自由度** —
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

主臂（16 关节）加键盘控制的头部/升降/底盘（5 DOF）。两者都保存到数据集用于 ACT 训练。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 录制时升降行为
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 首次连接：升降**归零到底部**（堵转检测），保存零位到 `~/.cache/humanaopen/lift_zero.json`。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 后续连接：升降**恢复保存的位置**（无需归零），除非位置变了（手动推动 → 恢复失败 → 自动归零）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 归零后：键盘按住 `u`/`h` 带安全限位调整高度（3mm–200mm），`ENTER` 确认开始录制。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 数据集恢复/清理
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

如果数据集目录已存在，删除或恢复：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

rm -rf ~/.cache/huggingface/lerobot/your-name/humanaopen_demo    # 全新开始
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 或在 record_data.py 命令中添加 --dataset.resume=true            # 从上一条继续
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 训练
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### ACT（动作分块 Transformer）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 快速测试（2 条 episode）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

lerobot-train \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.type=act \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.device=cuda \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.push_to_hub=true \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.repo_id=your-name/humanaopen_act_policy \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --output_dir=outputs/humanaopen_act_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --batch_size=3 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --steps=5
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 正式训练（>50 条 episode）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

lerobot-train \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.type=act \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.device=cuda \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.push_to_hub=true \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.repo_id=your-name/humanaopen_act_policy \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --output_dir=outputs/humanaopen_act_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --batch_size=32 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --steps=50000
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### SmolVLA（视觉语言动作模型）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

SmolVLA 需要录制时的语言指令（来自 `--dataset.single_task`）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

VLM 权重（~500M）首次运行时自动从 HuggingFace 下载。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

# 快速测试（2 条 episode）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

lerobot-train \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.type=smolvla \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.device=cuda \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.push_to_hub=true \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.repo_id=your-name/humanaopen_smolvla_policy \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --dataset.repo_id=your-name/humanaopen_act_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --output_dir=outputs/humanaopen_smolvla_demo \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --batch_size=4 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --steps=20
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> **注意**：SmolVLA（~450M 参数）比 ACT（~52M）重约 20 倍，占用更多 VRAM，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 训练更慢。Batch size 4 适配 8GB VRAM（RTX 5060 Ti）。超过 50 条数据时，
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 增加 steps 到 20000+。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 关键参数
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 参数 | 默认值 | 说明 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|-----------|---------|-------------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--policy.type` | — | **必需。** `act`, `smolvla`, `diffusion` 等。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--policy.device` | `cuda` | `cuda` / `cpu`。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--policy.push_to_hub` | `true` | 训练完推送模型到 HuggingFace Hub。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--policy.repo_id` | — | 训练模型的 Hub 仓库。推送时必需。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--dataset.repo_id` | — | **必需。** 训练数据集的 Hub 仓库。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--output_dir` | — | 本地 checkpoint 目录。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--batch_size` | 8 | 每步样本数。ACT: 32，SmolVLA: 4（8GB VRAM 限制）。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| `--steps` | 100000 | 总训练步数。ACT: 50K，SmolVLA: 20K。|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 输出
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

outputs/humanaopen_act_demo/
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── pretrained_model/           # 完整模型（配置 + 权重）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── last/pretrained_model       # 最新 checkpoint
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

├── train_logs/                 # 训练指标（兼容 TensorBoard）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

└── training_state.json         # 优化器/调度器状态（可恢复训练）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

推送的模型位于 `https://huggingface.co/your-name/humanaopen_act_policy`。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 推理（部署）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> **依赖**：SmolVLA 需要 `transformers>=4.48` 和 `num2words`。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 运行 SmolVLA 推理前安装：`pip install transformers>=4.48 num2words`。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### ACT 推理（支持人工接管）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/eval_data.py \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.type=act \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.repo_id=your-name/humanaopen_act_policy \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.device=cuda \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.type=humanaopen \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.id=follower \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port1=/dev/ttyACM0 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port2=/dev/ttyACM1 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port3=None \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.type=humanaopen_teleop \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.left_arm_port=/dev/ttyACM2 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.right_arm_port=/dev/ttyACM3 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.flip_joints='{"left": [], "right": []}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --teleop.joint_remap='{}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --num-episodes=5 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --duration=30 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --fps=30
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### SmolVLA 推理（语言条件，无 override）
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```bash
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

python3 examples/eval_data.py \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.type=smolvla \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.repo_id=your-name/humanaopen_smolvla_policy \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --policy.device=cuda \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --task="wave hello with both arms" \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.type=humanaopen \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.id=follower \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port1=/dev/ttyACM0 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port2=/dev/ttyACM1 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.port3=None \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --num-episodes=2 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --duration=10 \
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

    --fps=10
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

```
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> **SmolVLA 性能说明**：VLM 推理约 1s/帧（450M 参数）。10s 的 episode
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> 以 10fps = 100 帧 ≈ 100 秒实际等待时间。实时部署请使用 ACT（~50ms/帧）。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

> SmolVLA 最适合语言条件化任务。
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 推理时的控制
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 控制 | 按键 | 说明 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

|---------|------|-------|
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| Override（仅 ACT）| `e`（按住）| 切换双臂到主臂控制 |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

| 退出 | `q` | 停止所有 episode |
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

**人工接管**（仅 ACT）：
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 按住 `e`：双臂跟随主臂，头部/升降/底盘由键盘控制，策略暂停
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

- 松开 `e`：恢复策略控制
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

## 许可证
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）


## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

Apache 2.0
## 双机部署

正式部署时，机器人硬件（舵机 + 摄像头）连接到嵌入式板（Jetson 或树莓派），
策略推理在独立的 GPU 机器上运行。两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头     │
│  • ACT / SmolVLA     │                       │  • 执行动作         │
│  • 无需接舵机        │                       │  • 舵机+摄像头接线   │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 在树莓派上 (ARM64, 推荐树莓派 OS Lite)
sudo apt update && sudo apt install -y python3-pip
pip3 install lerobot[feetech]

# 安装 HumanaOpen
cd ~/
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip3 install -e . --no-deps

# 启动 Host（读传感器，执行动作）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={'head': {'type': 'opencv', 'index_or_path': '/dev/video0', 'width': 640, 'height': 480, 'fps': 30}},
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# 在 Jetson 上 (JetPack 6.x, CUDA 12.x)
# 安装 Jetson 版 PyTorch（NVIDIA 构建，非 pip）
# 参考: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform.html

pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（与树莓派相同）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 开发机（Client — 策略推理）

在 GPU 机器上连接机器人的 IP：

```bash
conda activate humanaopen
cd /path/to/HumanaOpen

# 设置机器人 IP（Jetson/RPi 局域网地址）
export ROBOT_IP=192.168.1.100

# 远程运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen_client \
    --robot.remote_ip=$ROBOT_IP \
    --num-episodes=5 --duration=30 --fps=30
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

