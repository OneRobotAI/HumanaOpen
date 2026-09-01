# HumanaOpen

[English](README.md) | [中文](README_zh.md) | [Français](README_fr.md) | [한국어](README_ko.md)

**开源半人形机器人 — 7自由度双臂、差速底盘、丝杠升降。**

基于 [LeRobot](https://github.com/huggingface/lerobot) 和
[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini) 构建。

## 硬件

| 子系统 | 电机 | 型号 |
|-----------|--------|-------|
| 左从臂 | 8（7-DOF + 夹爪）| ST3215 C018 (1:345) |
| 右从臂 | 8（7-DOF + 夹爪）| ST3215 C018 (1:345) |
| 头部（pan/tilt）| 2 | ST3215 C018 (1:345) |
| 升降（丝杠）| 1 | ST3250（直驱，无皮带）|
| 差速底盘 | 2 | ST3215 C018 (1:345) |
| 主臂（遥操）| 2 × 8 | STS3215 C046 (1:147) |

> **左右约定**：以机器人自身坐标系为准。
> 站在机器人后方面向同一方向，你左手边的臂是**左臂**（`port1`），
> 右手边是**右臂**（`port2`）。接线决定物理臂的位置；
> 软件将 `left_arm_*` 映射到 `port1`，`right_arm_*` 映射到 `port2`。

## 软件

```
lerobot_robot_humanaopen/
├── __init__.py              # 包导出
├── config_humanaopen.py     # HumanaOpenConfig, host/client 配置
├── humanaopen.py            # HumanaOpen Robot 类（从动侧）
├── lift_axis.py             # 升降轴（堵转检测归零）
├── leader.py                # 主臂遥操作器（单臂/双臂）
├── humanaopen_host.py       # ZMQ 主机端（机器人侧，双机模式）
└── humanaopen_client.py     # ZMQ 客户端（遥操侧）
examples/
├── record_data.py              # 数据采集（Python API，全参数）
├── eval_data.py                # 推理（ACT 策略部署）
├── single_machine.py           # 单机操作
├── teleop_keyboard.py          # 键盘遥操作（ZMQ）
├── teleop_leader_to_follower.py  # 全身遥操：主臂 + 键盘
├── calibrate_follower.py       # 从动侧完整校准（臂+头+轮+升降）
├── calibrate_leader.py         # 主臂校准（open-arms-mini）
├── diagnose_teleop.py          # 遥操关节方向诊断
├── test_base_keyboard.py       # 底盘键盘测试（不含升降/手臂）
├── test_lift_only.py           # 升降轴测试（归零 + 升降）
└── check_phase.py              # 检查舵机速度单位（Phase BIT2）

### 诊断与调参工具

| 脚本 | 用途 |
|--------|---------|
| `diag_head_tilt_limits.py` | 头部俯仰机械行程探测（解锁前/后）|
| `diag_head_tilt_range.py` | 头部俯仰行程诊断 |
| `diag_regression.py` | 回归测试（升降 + 摄像头 + 遥操序列）|
| `diag_st3250_speed.py` | ST3250 电机速度分析（Phase BIT2=1）|
| `diag_follower_gripper.py` | 夹爪关节诊断 |
| `recover_lift_ping.py` | 升降电机通信 ping |
| `speed_test_bit2_0.py` | BIT2=0 速度验证 |
| `switch_phase_bit2.py` | 切换 ST3250 Phase BIT2 寄存器 |
```

## 快速开始

```bash
# 1. 创建 conda 环境
conda create -n humanaopen python=3.12
conda activate humanaopen

# 2. 安装 LeRobot（必需依赖）
pip install "lerobot[dataset,training,feetech,viz,transformers-dep,hardware,smolvla]"

# 3. 安装 HumanaOpen（editable 模式）
cd /path/to/HumanaOpen
pip install -e . --no-deps


# Required: SOCKS proxy support (for HuggingFace upload behind proxy)
pip install httpx[socks] num2words


# 可选：安装 SmolVLA 依赖（transformers, num2words）
pip install -e ".[smolvla]" 2>/dev/null || pip install transformers>=4.48 num2words

# 可选：GPU CUDA 12.8+（Blackwell / RTX 5060+）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 4. 验证安装
python -c "from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig; print('✅ OK')"

# 5. 单机操作
python -c "
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
config = HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
robot = HumanaOpen(config)
robot.connect(calibrate=False)
print(robot.get_observation().keys())
"

# 6. 双机 ZMQ 模式（⚠️ 仅限 Jetson/树莓派双机部署 — 单机跳过）
# 在机器人端 (Jetson/RPi) 运行，不在开发机上运行
# 启动 Host（带摄像头）。纯摇操不需要画面？改用 cameras={} 即可。
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 第4路相机 — 去掉注释即启用
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

## 双机部署

正式部署时，机器人硬件连接到嵌入式板（Jetson 或树莓派），策略推理在独立 GPU 机器上运行。
两者通过 ZMQ 通信。

```
┌──────────────────────┐       ZMQ TCP        ┌──────────────────────┐
│   开发机 (GPU)       │ ←──────────────────→ │  Jetson / RPi (Host) │
│                      │   obs ──────────→    │                      │
│  • 策略推理          │   ←── action (21DOF) │  • 读舵机/摄像头      │
│  • ACT / SmolVLA     │                       │  • 执行动作          │
│  • 无需接舵机        │                       │  • 舵机 + 摄像头接线 │
└──────────────────────┘                       └──────────────────────┘
```

### 树莓派（仅 Host — 无 GPU 推理）

```bash
# 树莓派 (ARM64)
conda create -n humanaopen python=3.12
conda activate humanaopen

# Host 依赖（轻量 — 不需要 torch/transformers）
pip install pyzmq feetech-servo-sdk
# 可选：视频编码用（仅 ZMQ 流式传输则不需要）
# conda install -y ffmpeg=7.1.1 -c conda-forge

# 安装 HumanaOpen
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（带摄像头）。纯摇操不需要画面？改用 cameras={} 即可。
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 第4路相机 — 去掉注释即启用
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

### NVIDIA Jetson（Host + 可选本地推理）

```bash
# Jetson (JetPack 6.x, CUDA 12.x)
# 安装方式与树莓派相同 — Host 不需要 torch/transformers
conda create -n humanaopen python=3.12
conda activate humanaopen

pip install pyzmq feetech-servo-sdk
# conda install -y ffmpeg=7.1.1 -c conda-forge  # 可选

cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps

# 启动 Host（带摄像头）。纯摇操不需要画面？改用 cameras={} 即可。
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # 按板子上 lerobot-find-cameras 的输出改成实际设备号
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 第4路相机 — 去掉注释即启用
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

> **注意**：Jetson 也可以本地运行 ACT 推理（Orin 上约 100ms/帧），
> 但 SmolVLA 需要独立 GPU，应在开发机上运行。

### 双机模式 (--remote_ip)

所有脚本（record/eval/teleop）通过 `--remote_ip` 参数支持双机模式。单机模式（默认）直接串口；双机加 ZMQ：

```bash
# 单机模式（默认，无需 --remote_ip）
python3 examples/record_data.py ...

# 双机模式（加 --remote_ip）
python3 examples/record_data.py --remote_ip=192.168.1.100 ...
python3 examples/eval_data.py --remote_ip=192.168.1.100 ...
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 ...
```

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 网络要求

- 两台机器在同一局域网（建议以太网优于 WiFi 以降低延迟）
- 端口 **5555**（命令）和 **5556**（观测）必须开放
- 图像流带宽：每摄像头约 10 Mbps（640x480 MJPG）

### 性能

- 控制循环：30Hz（关节状态读取 + 动作命令）
- 图像采集：30fps（独立后台线程 — 不阻塞控制）
- 低延迟：图像采集与控制循环解耦，30fps 全速图像流下遥操臂仍即时响应
- 可配置：`image_fps_divider`（控制/图像频率比）和 `max_loop_freq_hz`（控制率）在

### 轮子方向（双机）

机器人左轮镜像安装，Host 使用 `wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}`。这也是 `HumanaOpenConfig` 的默认值。

## 校准

校准记录每个关节的 min/max 范围。**只需一次** — 结果保存后每次连接自动恢复。

### 什么时候需要校准

- **首次安装**（必需）
- 拆装过手臂或舵机后
- 更换舵机电机后
- 解锁新的运动范围后（如头部俯仰 EPROM 解锁）

### 主臂校准

```bash
python3 examples/calibrate_leader.py
```

步骤（每臂）：
1. 手臂自然下垂 + 夹爪闭合 → `ENTER`（设零点）
2. 每个关节走满行程 → `ENTER`（录真实限制）
3. 夹爪：完全闭合 → `ENTER`，完全张开 → `ENTER`
4. 自动保存校准

> 主臂需接 **7.4V** 电源，`/dev/ttyACM2`（左）和 `/dev/ttyACM3`（右）。

保存到：
```
~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/
├── leader_left.json
└── leader_right.json
```

### 从臂校准（双臂 + 头部 + 轮子 + 升降）

```bash
python3 examples/calibrate_follower.py
```

步骤：
1. 左臂 + 头部：零位 → `ENTER`；每个关节走满行程 → `ENTER`
2. 右臂：零位 → `ENTER`；每个关节走满行程 → `ENTER`
3. 自动：轮子全范围 + 升降堵转归零到底部

> 从臂需接 **12V** 电源。校准期间扭矩释放 — 手臂可自由移动。

保存到：
```
~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json
```


## 遥操作

### 全身遥操（主臂 + 键盘）

`teleop_leader_to_follower.py` 通过主臂控制从臂，键盘控制头部/底盘/升降：

| 控制 | 按键 |
|---------|------|
| 双臂 | 主臂跟随（已禁用翻转 — 方向实测一致）|
| 头部 | `w`/`s` 点头（上下），`a`/`d` 摇头（左右）|
| 底盘 | `i`/`k` 前进/后退，`j`/`l` 转向，`n`/`m` 速度（0.3x/0.6x/1.0x）|
| 升降 | `u`/`h` 升/降（限位 3–200mm）|
| 退出 | `b` 或 Ctrl+C |

```bash
# 默认：3 个摄像头（head + left_wrist + right_wrist）
python3 examples/teleop_leader_to_follower.py

# 加第 4 个胸口摄像头
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

# 双机模式：Host 在机器人端，teleop 在 PC 端
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --chest-camera /dev/video6

# 纯遥操，无摄像头
python3 examples/teleop_leader_to_follower.py --no-cameras
```

#### 实时画面显示模式

`teleop_leader_to_follower.py` 支持两种可视化后端。图像在控制线程解码一次后交给后台显示线程，**不阻塞 30Hz 控制循环**。

| 参数 | 后端 | 说明 |
|------|------|------|
| `--display` | [Rerun](https://rerun.io) 原生窗口 | gRPC 通信，`rr.spawn` 桌面端，`--serve-web` 备选 |
| `--display-foxglove` | [Foxglove Studio](https://foxglove.dev) WebSocket | 连接桌面版或 foxglove.dev，端口 `ws://127.0.0.1:8765`。**推荐**——两者中渲染延迟最低 |

```bash
# Foxglove（推荐）
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --display-foxglove

# Rerun
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --display
```

> **画面延迟说明**：两个后端均有固定的渲染管线延迟（桌面版 Foxglove ≈ 0.5–1.5 s，Rerun ≈ 2 s），这是可视化库本身的特性，与 HumanaOpen 无关。**动作指令实时无延迟**；画面延迟不影响采集数据质量——录制时 observation 与 action 帧严格同步采样。

摄像头参数：`--cameras=head,left_wrist`（子集），`--head-camera /dev/videoN`，
`--left-wrist-camera`，`--right-wrist-camera`，`--chest-camera`（每个覆盖设备路径；
传入 `--*-camera` 参数会自动添加该摄像头）。

### 摄像头设备与帧率（实测）

| 摄像头 | 设备 | 格式 | FPS |
|--------|--------|--------|-----|
| head | /dev/video0 | MJPG | 30 |
| left_wrist | /dev/video2 | MJPG | 30 |
| right_wrist | /dev/video4 | MJPG | 30 |
| chest | /dev/video6 | MJPG | 30 |

> **调整帧率**：用 `v4l2-ctl -d /dev/videoN --list-formats-ext` 查看摄像头实际能力，
> 然后在脚本中修改 `fps` 值。设置不支持的 fps 会在启动时导致连接错误。



### 升降轴 — 零位持久化（免归零）

升降使用 12 位单圈编码器（4096 ticks/圈）驱动丝杠（25 圈 = 200mm）。
绝对位置通过软件多圈环绕跟踪。由于丝杠自锁，断电后机械位置不变——
零位持久化到 `~/.cache/humanaopen/lift_zero.json`，
下次连接时恢复，**跳过重新归零**：

- 首次连接：下降到底部（堵转检测），保存零位。
- 后续连接：恢复保存的绝对位置（无需移动）。
- 如果位置变了（如手动推动升降），恢复失败，自动执行归零。

升降调参（实测）：`v_max=110`（raw），`kp_vel=10`，`home_down_speed=10`，
Phase BIT2=0（50 step/s per raw unit）。最大速度 ≈ 8.7mm/s（200mm 约 23s）。

### 升降提速（BIT2=0）

ST3250 固件将 `Goal_Velocity` 在 Phase BIT2=1 时映射为 1 step/s per raw unit，
raw > 1000 会方向反转（三角波回绕）— 不安全。切换 Phase BIT2=0 后单位变为
50 step/s per raw unit，满速（5500 step/s）只需 raw 110，完全在可靠范围内。
**切换后所有速度参数必须除以 50**（`home_down_speed`, `kp_vel`, `v_max`）。工具：
`examples/switch_phase_bit2.py`（切换），`examples/speed_test_bit2_0.py`（验证）。

### 头部俯仰行程解锁

头部俯仰舵机的 EPROM 位置限制被固定为 [1430, 2096]（~58°），
校准文件复制了这个限制 — 俯仰被限制在 -54°/+4°。写入
`Min=0 / Max=4095` 解锁机械行程 [1367, 2242]（-61.6°/+17.1°）：
`examples/unlock_head_tilt.py --probe`。解锁后校准文件
（`~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json`）
已更新为真实范围。

## 数据采集

`lerobot-record` CLI 硬编码了官方机器人类型，会拒绝 `humanaopen`
作为未识别的选项。使用 Python API 封装 `examples/record_data.py`
代替 — 它暴露与 `lerobot-record` **相同的参数名**，启动时打印等效 CLI 命令供参考。

### 3 摄像头（默认）

```bash
python3 examples/record_data.py \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --robot.confirm_lift_after_home=true \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=your-name/humanaopen_demo \
    --dataset.single_task="描述你的任务" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true
```

### 4 摄像头

与上面相同，替换 `--robot.cameras` JSON 加入 chest：

```bash
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
```

> **注意**：摄像头名称必须在采集/训练/推理之间保持一致。
**所有摄像头：30fps MJPG。**

### 双机模式（ZMQ）：机器人端跑 Host，PC 端采集

当 follower 在机器人上运行（自带摄像头）、主臂插在 PC 上时，通过 ZMQ 采集。
**先启动 Host**，然后在 PC 上运行 `record_data.py`：

```bash
# 1) 机器人端（Jetson 或树莓派，见上面"安装：树莓派 / Jetson"章节）— 先启动 Host 并保持运行
#    （HumanaOpenHost(...).run()，带 port1/port2 + 3 个摄像头）

# 2) PC 端 — 采集（follower 走 ZMQ，主臂走本机串口 ttyACM0/1）
python3 examples/record_data.py \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --teleop.left_arm_port=/dev/ttyACM0 \
    --teleop.right_arm_port=/dev/ttyACM1 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=your-name/humanaopen_demo \
    --dataset.single_task="describe your task" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true \
    --display-foxglove
```

- `--remote_ip` 切换为双机模式：follower 通过 ZMQ 连 Host（**不需要** `--robot.type/id/port1-3`），
  主臂用 PC 本机串口。
- `--robot.cameras` 作为 *schema*（名称+分辨率）传入；真实相机由 Host 持有并通过 ZMQ 传图。
- `--display-foxglove`（可选）在 PC 上把摄像头+状态流到 Foxglove 应用（连接 Studio 到 `ws://127.0.0.1:8765`）。

### 录制时的控制

| 控制 | 按键 |
|---------|------|
| 双臂 | 主臂跟随（16 DOF）|
| 头部 | `w`/`s` 点头，`a`/`d` 摇头（2 DOF）|
| 底盘 | `i`/`k` 前后，`j`/`l` 转向（2 DOF，速度 `n`/`m`）|
| 升降 | `u`/`h` 升/降带安全限位（1 DOF，限位 3–200mm）|
| 录制 | `C` 开始，`Q` 退出，`A` 重录当前 episode |
| 确认 | 归零后按住 `u`/`h` 定位，`ENTER` 确认 |

`--teleop.type=humanaopen_teleop` 遥操作器记录**全部 21 自由度** —
主臂（16 关节）加键盘控制的头部/升降/底盘（5 DOF）。两者都保存到数据集用于 ACT 训练。

### 录制时升降行为

- 首次连接：升降**归零到底部**（堵转检测），保存零位到 `~/.cache/humanaopen/lift_zero.json`。
- 后续连接：升降**恢复保存的位置**（无需归零），除非位置变了（手动推动 → 恢复失败 → 自动归零）。
- 归零后：键盘按住 `u`/`h` 带安全限位调整高度（3mm–200mm），`ENTER` 确认开始录制。

### 数据集恢复/清理

如果数据集目录已存在，删除或恢复：

```bash
rm -rf ~/.cache/huggingface/lerobot/your-name/humanaopen_demo    # 全新开始
# 或在 record_data.py 命令中添加 --dataset.resume=true            # 从上一条继续
```

### 录制时实时画面（可选）

默认录制为无画面运行。要在遥操作时实时查看摄像头和状态，添加显示参数：

```bash
# Rerun 查看器
python3 examples/record_data.py ... --display

# Foxglove 应用（推荐——渲染延迟更低，与 teleop 同后端）
python3 examples/record_data.py ... --display-foxglove
# 连接 Foxglove Studio 到 ws://127.0.0.1:8765
```

> 显示与录制循环解耦，不影响录制的 `(observation, action)` 帧对齐。与 teleop 一样，
> 查看器有固定 ~1–1.5s 渲染延迟，**不影响数据质量**。

## 训练

### ACT（动作分块 Transformer）

```bash
# 快速测试（2 条 episode）
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --dataset.repo_id=your-name/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_act_demo \
    --batch_size=3 \
    --steps=5

# 正式训练（>50 条 episode）
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --dataset.repo_id=your-name/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_act_demo \
    --batch_size=32 \
    --steps=50000
```

### SmolVLA（视觉语言动作模型）

SmolVLA 需要录制时的语言指令（来自 `--dataset.single_task`）。
VLM 权重（~500M）首次运行时自动从 HuggingFace 下载。

```bash
# 快速测试（2 条 episode）
lerobot-train \
    --policy.type=smolvla \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanaopen_smolvla_policy \
    --dataset.repo_id=your-name/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_smolvla_demo \
    --batch_size=4 \
    --steps=20
```

> **注意**：SmolVLA（~450M 参数）比 ACT（~52M）重约 20 倍，占用更多 VRAM，
> 训练更慢。Batch size 4 适配 8GB VRAM（RTX 5060 Ti）。超过 50 条数据时，
> 增加 steps 到 20000+。

### 关键参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `--policy.type` | — | **必需。** `act`, `smolvla`, `diffusion` 等。|
| `--policy.device` | `cuda` | `cuda` / `cpu`。|
| `--policy.push_to_hub` | `true` | 训练完推送模型到 HuggingFace Hub。|
| `--policy.repo_id` | — | 训练模型的 Hub 仓库。推送时必需。|
| `--dataset.repo_id` | — | **必需。** 训练数据集的 Hub 仓库。|
| `--output_dir` | — | 本地 checkpoint 目录。|
| `--batch_size` | 8 | 每步样本数。ACT: 32，SmolVLA: 4（8GB VRAM 限制）。|
| `--steps` | 100000 | 总训练步数。ACT: 50K，SmolVLA: 20K。|

### 输出

```
outputs/humanaopen_act_demo/
├── pretrained_model/           # 完整模型（配置 + 权重）
├── last/pretrained_model       # 最新 checkpoint
├── train_logs/                 # 训练指标（兼容 TensorBoard）
└── training_state.json         # 优化器/调度器状态（可恢复训练）
```

推送的模型位于 `https://huggingface.co/your-name/humanaopen_act_policy`。

## 推理（部署）

> **依赖**：SmolVLA 需要 `transformers>=4.48` 和 `num2words`。
> 运行 SmolVLA 推理前安装：`pip install transformers>=4.48 num2words`。

### ACT 推理

**双机（推荐）**：机器人在设备端运行 Host（Jetson/树莓派）带摄像头；`eval_data.py` 在 PC 端通过 ZMQ 连接。先启动 Host：

```bash
# 设备端（Jetson 或树莓派）— 先启动 Host 并保持运行
#   （HumanaOpenHost(...).run()，带 port1/port2 + 3 个摄像头）

# PC 端 — 运行推理
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --num-episodes=5 \
    --duration=30 \
    --fps=30 \
    --display-foxglove
```

- `--remote_ip` 切换为双机模式：follower 通过 ZMQ 连 Host（不需要 `--robot.port1/port2/port3`）；摄像头在 Host 端。
- `--display-foxglove`（可选）在 PC 上把画面流到 Foxglove 应用（连接 Studio 到 `ws://127.0.0.1:8765`）。纯推理可用 `--no-display`。

**单机**（follower 直接串口，同机）：
```bash
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --num-episodes=5 \
    --duration=30 \
    --fps=30
```

### SmolVLA 推理（语言条件）

**双机（推荐）**：与 ACT 相同——先在机器人端启动 Host，PC 端通过 ZMQ 运行：

```bash
# 设备端 — 先启动 Host 并保持运行

# PC 端
python3 examples/eval_data.py \
    --policy.type=smolvla \
    --policy.repo_id=your-name/humanaopen_smolvla_policy \
    --policy.device=cuda \
    --task="wave hello with both arms" \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --num-episodes=2 \
    --duration=10 \
    --fps=10 \
    --display-foxglove
```

**单机**（follower 直接串口）：
```bash
python3 examples/eval_data.py \
    --policy.type=smolvla \
    --policy.repo_id=your-name/humanaopen_smolvla_policy \
    --policy.device=cuda \
    --task="wave hello with both arms" \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --num-episodes=2 \
    --duration=10 \
    --fps=10
```

> **SmolVLA 性能说明**：VLM 推理约 1s/帧（450M 参数）。10s 的 episode
> 以 10fps = 100 帧 ≈ 100 秒实际等待时间。实时部署请使用 ACT（~50ms/帧）。
> SmolVLA 最适合语言条件化任务。

### 推理时实时画面（可选）

推理查看器默认用 Rerun。改用 Foxglove（推荐——渲染延迟更低），加 `--display-foxglove`：

```bash
# Foxglove 应用
python3 examples/eval_data.py ... --display-foxglove
# 连接 Foxglove Studio 到 ws://127.0.0.1:8765

# Rerun（默认开启）
python3 examples/eval_data.py ...

# 完全关闭显示
python3 examples/eval_data.py ... --no-display
```

> 显示在后台线程运行，不拖慢策略循环。与 teleop/录制一样，查看器的 ~1–1.5s
> 渲染延迟是固有的，不影响控制。

### 底盘控制（默认关闭）

默认底盘**关闭**（`--enable-base=false`）：策略预测的 `x.vel` / `theta.vel` 被强制置 0，
只有手臂、头部和升降动作。这可防止机器人意外移动，验证新策略时更安全。

```bash
# 底盘关闭（默认，更安全）— 轮子不动，只有手臂/头部/升降动作
python3 examples/eval_data.py ... --enable-base=false

# 底盘开启 — 允许策略驱动轮子
python3 examples/eval_data.py ... --enable-base=true
```

建议先用 `--enable-base=false` 直到策略表现稳定，若任务需要移动再开启底盘。

### 升降控制（默认保持当前高度）

默认升降**保持当前高度**（`--enable-lift=false`）：策略预测的 `lift_axis.height_mm`
每帧被覆盖为当前高度，升降不动（否则策略可能输出 0 把升降拉到最低）。

```bash
# 升降保持当前高度（默认，更安全）— 升降不动
python3 examples/eval_data.py ... --enable-lift=false

# 升降开启 — 允许策略控制升降高度
python3 examples/eval_data.py ... --enable-lift=true
```

建议先保持升降不动，等任务需要变高度再开启。

### 推理时的控制

| 控制 | 按键 | 说明 |
|---------|------|-------|
| 退出 | `q` | 停止所有 episode |


## 许可证

Apache 2.0
