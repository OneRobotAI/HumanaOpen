# OpenArmsX 操作手册

## 概述

OpenArmsX 是一款基于 LeRobot 的开源半人形机器人，拥有：

- **双臂**：2 × 7 自由度 + 夹爪（各 8 个 ST3215 C018 舵机）
- **头部**：2 自由度（ST3215 C018 舵机 × 2）
- **升降**：丝杠驱动（ST3250 舵机 × 1）
- **底盘**：双轮差速驱动（ST3215 C018 舵机 × 2）
- **相机**：头部 × 1 + 左腕 × 1 + 右腕 × 1

---

## 一、硬件准备

### 1.1 舵机清单

| 位置 | 舵机 | 数量 | 舵机 ID |
|------|------|------|---------|
| 左从臂 J1-J7 + 夹爪 | ST3215 C018 | 8 | 1-8 |
| 右从臂 J1-J7 + 夹爪 | ST3215 C018 | 8 | 1-8 |
| 头部 Pan / Tilt | ST3215 C018 | 2 | 12, 13 |
| 升降丝杠 | ST3250 | 1 | 9 |
| 左轮 / 右轮 | ST3215 C018 | 2 | 10, 11 |
| **左主臂** J1-J7 + 夹爪（遥操） | STS3215 C046 | 8 | 1-8 |
| **右主臂** J1-J7 + 夹爪（遥操） | STS3215 C046 | 8 | 1-8 |

### 1.2 总线拓扑

**3 总线模式（推荐）：**

```
Bus 1 ── 左从臂(1-8) + 头部(12,13) ── POSITION
Bus 2 ── 右从臂(1-8) ── POSITION
Bus 3 ── 升降(9) + 左轮(10) + 右轮(11) ── VELOCITY
```

**2 总线模式（port3=None）：**

```
Bus 1 ── 左从臂(1-8) + 头部(12,13) ── POSITION
Bus 2 ── 右从臂(1-8) + 升降(9) + 左轮(10) + 右轮(11) ── 混合模式
```

### 1.3 主臂（遥操端）

主臂使用 STS3215 C046（7.4V），通过另一台电脑（笔记本）连接，与机器人端通过 ZMQ 或直接接同一台机器通信。

---

## 二、软件安装

### 2.1 安装 LeRobot

```bash
pip install lerobot[feetech]
```

### 2.2 安装 OpenArmsX

```bash
git clone <你的仓库地址> /home/zach/OpenArmsX
pip install -e /home/zach/OpenArmsX
```

### 2.3 验证安装

```bash
python3 -c "from lerobot_robot_openarmsx import OpenArmsX; print('OK')"
```

---

## 三、舵机 ID 配置（首次使用）

只有新舵机需要配置 ID。**每个舵机逐个连接到 Waveshare 板进行配置：**

### 3.1 接线

- 将 Waveshare 板通过 USB 连接到电脑
- **每次只连接一个舵机**到 Waveshare 板
- 给舵机供电（12V 电源）

### 3.2 运行配置

```python
from lerobot_robot_openarmsx import OpenArmsX, OpenArmsXConfig

config = OpenArmsXConfig(port1="/dev/ttyACM0", port2="/dev/ttyACM1")
robot = OpenArmsX(config)

# 这会逐个提示你连接舵机并设置 ID
robot.setup_motors()
```

按提示操作，每次只连接提示的舵机，然后按 Enter。

### 3.3 主臂舵机 ID 设置

主臂的 C046 舵机 ID 同样设置为 1-8（左右臂各一套），通过另一个 Waveshare 板连接。可以用相同的 `setup_motors()` 方法，但修改端口指向主臂的 Waveshare 板。

---

## 四、校准

### 4.1 从臂校准

校准包含：
- **关节舵机**：半圈归中 + 全行程录制
- **车轮**：设置为连续旋转全范围
- **升降**：堵转检测自动归零

```bash
python3 -c "
from lerobot_robot_openarmsx import OpenArmsX, OpenArmsXConfig
robot = OpenArmsX(OpenArmsXConfig())
robot.connect(calibrate=True)
"
```

按提示操作：
1. 将有校准文件的提示输入回车（自动恢复）或输入 `c` 手动校准
2. 如果选择手动校准：
   - 将左臂和头部关节移到中间位置 → 按 Enter
   - 依次移动每个关节走完全范围 → 按 Enter 停止录制
   - 同样的步骤操作右臂
3. 升降会自动进行堵转归零

### 4.2 标定文件存储位置

`~/.cache/huggingface/lerobot/calibration/robots/openarmsx/{id}.json`

下次连接时会自动加载。

---

## 五、运行模式

### 5.1 单机模式（全插一台机器）

所有 Waveshare 板和相机都插在同一台电脑（笔记本或 Jetson）：

```python
from lerobot_robot_openarmsx import OpenArmsX, OpenArmsXConfig

config = OpenArmsXConfig(
    port1="/dev/ttyACM0",   # 左臂+头
    port2="/dev/ttyACM1",   # 右臂
    port3="/dev/ttyACM2",   # 升降+车轮
)
robot = OpenArmsX(config)
robot.connect()

# 采集一帧观察
obs = robot.get_observation()
print(obs.keys())

# 发送动作（保持静止）
action = {k: obs[k] for k in obs if k.endswith(".pos")}
action["x.vel"] = 0.0
action["theta.vel"] = 0.0
action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0)
robot.send_action(action)

robot.disconnect()
```

### 5.2 双机 ZMQ 模式（笔记本遥操 + Jetson/树莓派机器端）

**机器端（Jetson/树莓派）:**

```bash
python3 -c "
from lerobot_robot_openarmsx import OpenArmsXConfig
from lerobot_robot_openarmsx.openarmsx_host import OpenArmsXHost

host = OpenArmsXHost(OpenArmsXConfig())
host.run()
"
```

默认端口：obs 5556 / cmd 5555。

**遥操端（笔记本）：**

```python
from lerobot_robot_openarmsx.openarmsx_client import OpenArmsXClient
from lerobot_robot_openarmsx import OpenArmsXClientConfig

client = OpenArmsXClient(
    OpenArmsXClientConfig(remote_ip="192.168.1.100")  # Jetson/树莓派 IP
)
client.connect()

obs = client.get_observation()
# 接入主臂遥操或键盘控制
# ...

client.send_action(action)
client.disconnect()
```

---

## 六、数据采集

### 6.1 使用 lerobot-record（推荐）

```bash
lerobot-record \
    --robot.type=openarmsx \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": 0, "fps": 30, "width": 640, "height": 480}, "left_wrist": {"type": "opencv", "index_or_path": 2, "fps": 30, "width": 640, "height": 480}, "right_wrist": {"type": "opencv", "index_or_path": 4, "fps": 30, "width": 640, "height": 480}}' \
    --teleop.type=openarm_mini \
    --teleop.port=/dev/ttyACM_leader \
    --dataset.repo_id=你的名字/my_openarmsx_data \
    --dataset.num_episodes=10 \
    --dataset.single_task="描述你的任务"
```

### 6.2 双机 ZMQ 模式数据采集

**机器端：**

```bash
# 运行 ZMQ host（它会自动发布 obs 并接收 action）
python3 -c "
from lerobot_robot_openarmsx import OpenArmsXConfig
from lerobot_robot_openarmsx.openarmsx_host import OpenArmsXHost
OpenArmsXHost(OpenArmsXConfig()).run()
"
```

**遥操端：**

```bash
# 遥操端运行记录脚本，从 ZMQ 获取 obs，发送 action
# 数据集保存在遥操端（或可以配置保存路径）
```

---

## 七、模型训练

数据采集完成后，直接在任意机器上训练：

```bash
lerobot-train \
    --policy=act \
    --dataset.repo_id=你的名字/my_openarmsx_data \
    --output_dir=./outputs
```

训练参数可在命令行覆盖：

```bash
lerobot-train --policy=act --dataset.repo_id=... --training.batch_size=32 --training.epochs=100
```

支持的政策类型：`act`, `diffusion`, `pi0` 等。

---

## 八、模型部署（推理）

### 8.1 单机推理

```bash
lerobot-rollout \
    --policy.path=./outputs/checkpoints/last \
    --robot.type=openarmsx \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2
```

### 8.2 双机 ZMQ 推理

**机器端运行 ZMQ host，遥操端运行 rollout：**

```bash
# 机器端
python3 -c "
from lerobot_robot_openarmsx import OpenArmsXConfig
from lerobot_robot_openarmsx.openarmsx_host import OpenArmsXHost
OpenArmsXHost(OpenArmsXConfig()).run()
"
```

遥操端目前需要手动加载策略并通过 ZMQ client 发送动作。

---

## 九、升降操作

升降使用 ST3250 舵机 + 8mm 导程丝杠，支持两种控制方式：

### 9.1 高度控制（推荐）

```python
# 读取当前高度
height = obs["lift_axis.height_mm"]

# 设置目标高度
action["lift_axis.height_mm"] = 200.0  # 单位 mm
```

### 9.2 直接速度控制

```python
action["lift_axis.vel"] = 500  # 原始速度值，正=上升，负=下降
```

### 9.3 安全保护

- **下限保护**：低于 `descent_floor_mm` 时拒绝下行指令
- **软限位**：在 `soft_min_mm` 和 `soft_max_mm` 范围内的运动保护
- **堵转检测**：归零时自动检测

---

## 十、配置参数说明

### 10.1 OpenArmsXConfig

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `port1` | `/dev/ttyACM0` | 左臂+头部总线端口 |
| `port2` | `/dev/ttyACM1` | 右臂总线端口 |
| `port3` | `/dev/ttyACM2` | 升降+车轮总线端口（设为 None 启用 2 总线模式） |
| `use_degrees` | `False` | 是否使用角度值（False 使用 -100..100 范围） |
| `wheel_radius` | 0.06 m | 车轮半径 |
| `wheelbase` | 0.30 m | 轮距 |
| `max_wheel_raw` | 3000 | 最大车轮速度原始值 |

### 10.2 LiftAxisConfig

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `motor_id` | 9 | 升降舵机 ID |
| `motor_model` | "sts3215" | 寄存器映射表型号（ST3250 兼容） |
| `lead_mm_per_rev` | 8.0 | 丝杠导程 (mm) |
| `belt_ratio` | 1.0 | 同步带增速比（直驱=1） |
| `home_stall_current_ma` | 200 | 堵转检测电流阈值 |
| `v_max` | 1500 | 最大速度指令 |
| `kp_vel` | 300.0 | 位置→速度 P 控制器增益 |

---

## 十一、常见问题

### Q: 舵机 ID 如何烧录？

A: 使用 `robot.setup_motors()`，每次只连接一个舵机到 Waveshare 板，按提示操作。

### Q: 设备端口 (/dev/ttyACM0) 每次重启后变化？

A: 使用 udev 规则绑定固定设备名：

```bash
# /etc/udev/rules.d/99-waveshare.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A1", SYMLINK+="tty_left_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A2", SYMLINK+="tty_right_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A3", SYMLINK+="tty_base"
```

然后在 Config 中使用 `/dev/tty_left_arm` 等固定路径。

### Q: 主臂和从臂的电压不同怎么办？

A: 主臂 C046（7.4V）和从臂 C018（12V）分别用不同的电源供电。如果通过 ZMQ 模式运行，两台机器各自供电。如果单机模式，使用两个电源分别给 Waveshare 板供电。

### Q: 升降速度太慢？

A: 直驱 8mm 导程的升降速度约 10mm/s（400mm 约 40 秒）。如需加速，可增大 `belt_ratio` 值（加同步带增速），或换更大导程的丝杠。

### Q: 相机找不到？

A: 检查 `/dev/video*` 设备是否存在。可能需要调整 `default_cameras()` 中的视频设备索引。

---

## 十二、项目结构

```
/home/zach/OpenArmsX/
├── pyproject.toml                          # 包配置 + lerobot 入口点
├── lerobot_robot_openarmsx/               # 主包
│   ├── __init__.py                        # 导出 OpenArmsX
│   ├── config_openarmsx.py               # 配置类
│   ├── openarmsx.py                      # 主 Robot 类
│   ├── lift_axis.py                      # 升降轴控制
│   ├── openarmsx_host.py                 # ZMQ 双机模式 Host
│   └── openarmsx_client.py               # ZMQ 双机模式 Client
├── examples/
│   ├── single_machine.py                 # 单机使用示例
│   └── teleop_keyboard.py                # 键盘遥操示例
├── docs/
│   ├── manual_zh.md                      # 本文件
│   └── manual_en.md                      # English manual
└── README.md
```
