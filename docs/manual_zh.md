# HumanaLite 完整入门教程

本手册面向第一次接触 HumanaLite 的开发者，从零开始安装环境、接线、测试电机、校准、采集数据、训练模型到部署，全部步骤都经过本项目的实际测试验证。文中所有参数以代码为准（`config_humanalite.py` 和 `lift_axis.py`），凡标注 ⚠️ 的地方都是实际踩过的坑，请务必留意。

## 概述

HumanaLite 是一款基于 LeRobot 的开源半人形机器人，拥有：

- **双臂**：2 × 7 自由度 + 夹爪（各 8 个 ST3215 C018 舵机）
- **头部**：2 自由度（ST3215 C018 舵机 × 2）
- **升降**：丝杆驱动（ST3250 舵机 × 1，T8 丝杆，直驱）
- **底盘**：双轮差速驱动（ST3215 C018 舵机 × 2）
- **相机**：头部 × 1 + 左腕 × 1 + 右腕 × 1（默认 640×480 @ 30fps）

完整的遥操-学习闭环与 LeRobot 官方流程一致：`lerobot-record` 采集 → `lerobot-train` 训练 → `lerobot-rollout` 部署。

---

## 一、硬件准备

### 1.1 舵机清单

| 位置 | 舵机 | 数量 | 舵机 ID | 控制模式 |
|------|------|------|---------|----------|
| 左从臂 J1-J7 + 夹爪 | ST3215 C018 | 8 | 1-8 | POSITION |
| 右从臂 J1-J7 + 夹爪 | ST3215 C018 | 8 | 1-8 | POSITION |
| 头部 Pan / Tilt | ST3215 C018 | 2 | 12, 13 | POSITION |
| 升降丝杆 | ST3250 | 1 | 9 | VELOCITY |
| 左轮 / 右轮 | ST3215 C018 | 2 | 10, 11 | VELOCITY |
| **左主臂** J1-J7 + 夹爪（遥操） | STS3215 C046 | 8 | 1-8 | POSITION |
| **右主臂** J1-J7 + 夹爪（遥操） | STS3215 C046 | 8 | 1-8 | POSITION |

### 1.2 总线拓扑

> **左右臂定义**：以机器人自身为参考系。站在机器人身后、与其面朝同一方向时，位于你左手侧的机械臂为**左臂**（`port1`），右手侧为**右臂**（`port2`）。接线决定物理左右，软件只映射 `left_arm_*` → `port1`、`right_arm_*` → `port2`。

**3 总线模式（默认配置）：**

```
Bus 1 ── 左从臂(1-8) + 头部(12,13) ── POSITION
Bus 2 ── 右从臂(1-8) ── POSITION
Bus 3 ── 升降(9) + 左轮(10) + 右轮(11) ── VELOCITY
```

**2 总线模式（port3=None，本项目实际使用）：**

```
Bus 1 ── 左从臂(1-8) + 头部(12,13) ── POSITION
Bus 2 ── 右从臂(1-8) + 升降(9) + 左轮(10) + 右轮(11) ── 混合模式
```

⚠️ 2 总线模式下 bus2 同时挂着 POSITION 模式的右臂和 VELOCITY 模式的升降/轮子，这是代码支持的（每个电机单独设置 `Operating_Mode`），互不干扰，已实测可用。

`enable_base=False` 时轮子和升降都会自动禁用（`bus3` 不创建，升降也拿不到总线），此时连升降归零都不会执行，适合纯双臂测试。

### 1.3 主臂（遥操端）

主臂使用 STS3215 C046（7.4V），通过另一台电脑（笔记本）连接，与机器人端通过 ZMQ 或直接接同一台机器通信。

### 1.4 供电与菊花链接线（新手必读）

- 从臂 / 升降 / 轮子共 12V 供电，主臂 C046 用 7.4V 独立供电，两者电压不同，切勿混用。
- 同一总线上所有舵机是**菊花链**串联的，中间任何一处断线，会同时失去它之后的所有舵机（详见 FAQ 中 "Missing motor IDs" 的排查）。
- 升降舵机（ID 9）负载大，注意 12V 电源的电流余量，电机多时建议分级供电。

---

## 二、软件安装

### 2.1 创建 conda 环境

推荐用 conda 管理环境，Python 3.12：

```bash
conda create -n lerobot python=3.12
conda activate lerobot
```

⚠️ 之后所有命令都必须在这个 `lerobot` 环境里跑。系统自带 python（比如 conda base 的 3.13）很可能缺 numpy 等依赖，直接 import 就会报错。

### 2.2 安装 lerobot（本地源码）

HumanaLite 依赖的是**本地源码安装的 lerobot**（版本 0.4.x，本项目位于 `/home/zach/lerobot-so101-bimanual/lerobot`）。注意 PyPI 上的 lerobot 没有 1.0，最新只有 0.6.x，API 有差异。所以 HumanaLite 的 `pyproject.toml` 刻意**不依赖 PyPI 上的 lerobot**，只声明了 `numpy` 和 `pyzmq`。

```bash
cd /home/zach/lerobot-so101-bimanual/lerobot
pip install -e . --no-deps
```

（如果在自己机器上，把路径换成你的 lerobot 源码路径。`-e` 是 editable 安装，之后改 lerobot 源码实时生效，不用重装。）

### 2.3 安装 HumanaLite

```bash
cd /home/zach/HumanaLite
pip install -e . --no-deps
```

⚠️ 一定要带 `--no-deps`。否则 pip 会尝试从 PyPI 拉取 lerobot，和本地源码版冲突。

### 2.4 验证安装

验证必须在**非项目目录**进行，否则当前目录会被 Python 自动加入 path，误以为装好了：

```bash
cd /tmp
python -c "import lerobot_robot_humanalite; print('OK')"
```

看到 `OK` 才算装好。如果报 `ModuleNotFoundError`，多半是（a）没在 lerobot 环境里，或（b）pip 装到了别的环境。

### 2.5 常见安装失败

| 症状 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError: No module named 'numpy'` | 用了系统 python（非 lerobot 环境） | `conda activate lerobot` 后再跑 |
| 项目目录里 import 成功，换目录失败 | 当前目录被 Python 自动加入 path，不是真装好 | 重新 `pip install -e . --no-deps`，在 `/tmp` 下验证 |
| 运行时 lerobot API 报错 | 装到了 PyPI lerobot | `pip show lerobot` 查版本，重装本地源码版 |

---

## 三、舵机 ID 配置（首次使用）

只有新舵机需要配置 ID。**每个舵机逐个连接到 Waveshare 板进行配置：**

### 3.1 接线

- 将 Waveshare 板通过 USB 连接到电脑
- **每次只连接一个舵机**到 Waveshare 板
- 给舵机供电（12V 电源）

### 3.2 运行配置

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(port1="/dev/ttyACM0", port2="/dev/ttyACM1")
robot = HumanaLite(config)

# 这会逐个提示你连接舵机并设置 ID
robot.setup_motors()
```

按提示操作，每次只连接提示的舵机，然后按 Enter。

⚠️ 提示顺序是**倒着**来的（从大 ID 到小 ID）。新舵机出厂 ID 都是 1，如果先把 1 号设好再插别的舵机，会和新插舵机的出厂 ID 冲突。

### 3.3 主臂舵机 ID 设置

主臂的 C046 舵机 ID 同样设置为 1-8（左右臂各一套），通过另一个 Waveshare 板连接。可以用相同的 `setup_motors()` 方法，但修改端口指向主臂的 Waveshare 板。

### 3.4 Missing motor IDs 排查

`connect()` 报 `Missing motor IDs: ...` 说明总线上有舵机没被找到。按顺序检查：

1. **菊花链断线**：同一总线是串联的，比如 6→7 之间断线，会导致 7 及之后全部失联，报错里会同时缺 7、8。用 `broadcast_ping` 扫描（见 5.3）从断点往前查线。
2. **舵机 ID 未烧录**：新舵机出厂 ID 都是 1，重复 ID 或 ID 与预期不符也会失联。用 `setup_motors()` 重新烧录。
3. **供电不足**：舵机太多时 12V 电源电流不够，末端舵机会随机失联。

---

## 四、校准

### 4.1 完整校准（从动侧）

lerobot 的完整管线（record / train / rollout）**必须先校准**。校准包含：

- **关节舵机**：半圈归中 + 全行程录制
- **车轮**：设置为连续旋转全范围
- **升降**：堵转检测自动归零

推荐用校准脚本（带完整步骤提示和校准后验证）：

```bash
python3 examples/calibrate_follower.py
```

或手动运行：

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig
robot = HumanaLite(HumanaLiteConfig(id='follower'))
robot.connect(calibrate=True)
"
```

按提示操作：

1. 有校准文件时提示输入回车（自动恢复）或输入 `c` 手动校准
2. 如果选择手动校准：
   - 将左臂和头部关节移到**零位姿态**（手臂自然下垂、夹爪闭合）→ 按 Enter
   - 依次移动每个关节走完全范围 → 按 Enter 停止录制
   - 右臂做同样操作
   - 夹爪有专门的闭合/张开两步标定（0=闭合，100=张开）
3. 升降会自动进行堵转归零

⚠️ 校准过程中手臂是**掉扭矩**的，需要手动移动关节。移动时要温柔，不要硬掰。

**零位约定（重要）**：从臂和主臂统一用"**手臂自然下垂 + 夹爪闭合**"作为零位。这样遥操时主臂下垂 → 从臂也下垂（姿态一一对应），录数据时 action/obs 的归一化空间物理一致。走行程时尽量**绕零位对称**地移动（两端都走到），让量程中点 ≈ 零位。

### 4.2 标定文件存储位置

**从动侧（follower）**：`~/.cache/huggingface/lerobot/calibration/robots/humanalite/{id}.json`

```
.../humanalite/follower.json   ← 从动侧校准 (id="follower")
```

校准过的机器人下次 `connect()` 会自动加载，并提示按 Enter 恢复校准或输入 `c` 重新校准。

**主动侧（leader）**：存储在 teleoperators 目录（见 4.3），与从动侧完全分开。

### 4.3 主臂（leader）校准

主臂是 open-arms-mini 结构（STS3215 C046，7.4V），左右各 8 舵机（ID 1-8），关节命名与从臂一致。用校准脚本：

```bash
python3 examples/calibrate_leader.py
```

每臂交互流程（默认 `calibration_mode="full"`，录真实行程）：

1. **手臂自然下垂 + 夹爪闭合** → 回车（设为零点）
2. **逐个关节走满行程**（两端之间）→ 回车（录真实 min/max，与从臂归一化空间一致）
3. **夹爪闭合位置** → 回车
4. **夹爪张开位置** → 回车
5. 保存校准

**为什么主臂也要录真实行程？** 录数据训练时，`action` 来自主臂、`observation` 来自从臂。若主臂用全量程而从臂录行程，同一物理姿态下两套归一化空间含义不同（主臂 50 ≠ 从臂 50），模型学到错误映射，部署时动作不到位。主臂录真实行程后，两套空间物理对齐，**遥操和录数据共用同一份校准，无需重校**。

> 若只需纯实时遥操（人实时补偿），可设 `calibration_mode="quick"`（关节全量程 [0,4095]，官方 openarm_mini 简化方式）。但录数据训练前必须改回 `"full"` 并重校。

校准文件（与从臂分开，互不覆盖）：

```
~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_left.json
~/.cache/huggingface/lerobot/calibration/teleoperators/humanalite_leader/leader_right.json
```

主臂实现（`lerobot_robot_humanalite/leader.py`）：

- `humanalite_leader`：单臂 teleoperator（`calibration_mode`: `full`/`quick`）
- `bi_humanalite_leader`：双臂 teleoperator（输出 `left_arm_*`/`right_arm_*` 前缀）

遥操时 `leader.get_action()` 的动作键与从臂 `follower.send_action()` 完全对齐，可零转换对接。

**方向翻转 / 腕部重映射（可配置）**：

默认 `flip_joints` / `joint_remap` 采用官方 openarm_mini 的值（针对官方主从臂配对）。**如果你的主从臂装配与官方不同，部分关节方向会反、腕部映射会错**——这是硬件相关，不是 bug。用诊断脚本逐关节实测：

```bash
python3 examples/diagnose_teleop.py
```

根据诊断结果配置（`BiHumanaLiteLeaderConfig` / `HumanaLiteLeaderConfig`）：

```python
config = BiHumanaLiteLeaderConfig(
    left_arm_port="/dev/ttyACM2",
    right_arm_port="/dev/ttyACM3",
    # 方向反的关节加入对应侧列表; 不需要腕部交换则置空 dict
    flip_joints={"left": ["shoulder_pan", ...], "right": [...]},
    joint_remap={},  # 不需要腕部 flex↔yaw 交换
)
```

夹爪输出直接是 [0,100]（0=闭，100=开），与从臂 `RANGE_0_100` 同构，无额外缩放。

⚠️ 主臂 7.4V 供电（与从臂 12V 分开），校准中扭矩释放可手动摆动。

### 4.4 未校准时的正常报错：no calibration registered

没有校准文件就 `connect(calibrate=False)`，再用 `robot.get_observation()` 读关节位置时，会看到类似 "no calibration registered" 的报错。

⚠️ **这是正常的**。未校准时电机读数无法归一化到 -100..100（或角度），`get_observation()` 自然读不了。升降测试应绕过它：直接用 `robot.lift_axis.get_height_mm()` 读高度，完全不需要校准。

### 4.5 摄像头查找

摄像头不在默认位置（`/dev/video0`、`/dev/video2`、`/dev/video4`）时，用官方命令找设备号：

```bash
lerobot-find-cameras opencv
```

它会列出检测到的摄像头及对应的设备号/索引，把结果填进 `HumanaLiteConfig` 的 `cameras` 字段（或 record 命令行的 `--robot.cameras`）。

---

## 五、运行模式

### 5.1 单机模式（全插一台机器）

所有 Waveshare 板和相机都插在同一台电脑（笔记本或 Jetson）：

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(
    port1="/dev/ttyACM0",   # 左臂+头
    port2="/dev/ttyACM1",   # 右臂
    port3="/dev/ttyACM2",   # 升降+车轮（3 总线模式）
)
robot = HumanaLite(config)
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

⚠️ 用 2 总线模式就把 `port3=None`；还没装相机就加 `cameras={}` 跳过，电机照样能测。参考 `examples/single_machine.py`。

### 5.2 连接测试与排障（快速自检）

**推荐流程**：先用 `cameras={}` 把电机这半边测通，再逐步加相机：

```python
from lerobot_robot_humanalite import HumanaLite, HumanaLiteConfig

config = HumanaLiteConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,          # 2 总线模式（本项目实际使用）
    cameras={},          # 跳过摄像头
)
robot = HumanaLite(config)
robot.connect(calibrate=False)   # 不校准也能连接、能测升降
print("connected:", robot.is_connected)
robot.disconnect()
```

⚠️ 注意 `connect(calibrate=False)` 仍然会**自动执行升降归零**（向下找底堵转即停），这是设计行为。

### 5.3 总线电机扫描

某条总线上不确定哪些舵机在线时，用 `broadcast_ping` 扫描。**必须先 `bus.connect()`**，否则会报 `'NoneType'` 对象没有 `flush` 的错误：

```python
from lerobot.motors.feetech import FeetechMotorsBus

bus = FeetechMotorsBus(port="/dev/ttyACM0", motors={})
bus.connect()
print(bus.broadcast_ping())   # 返回 {舵机ID: 型号编号}
bus.disconnect()
```

输出形如 `{1: 45, 2: 45, ..., 12: 45, 13: 45}`，一眼就能看出哪些 ID 在线、哪些失联，是排查菊花链断点最快的办法。

### 5.4 端口漂移确认

⚠️ 断电重插后，`/dev/ttyACM0` 和 `/dev/ttyACM1` **可能互换**。判断实际端口用序列号：

```bash
ls -l /dev/serial/by-id/
```

`by-id` 下的符号链接按 USB 序列号命名，拔插后稳定不变。如果每块 Waveshare 板序列号不同，可以用 udev 规则绑定固定名字（见 FAQ）。

### 5.5 键盘控制与权限

**键盘库选择（Linux 必读）**

两个键盘监听库，权限要求不同：

- **`pynput`（推荐）**：桌面 X11 环境下**无需 root**，直接运行。需已设置 `DISPLAY`（桌面终端默认有）。
- **`keyboard`**：在 Linux 上**强制要求 root**（`ensure_root()` 硬检查），加 `input` 组也没用。要么 sudo 运行，要么换 pynput。

```bash
# 安装 pynput
pip install pynput
```

**底盘键盘手动测试**

只有底盘、不碰手臂和升降的键盘控制脚本（无需校准）：

```bash
python3 examples/test_base_keyboard.py
```

键位：`i/k` 前进/后退，`j/l` 左转/右转，`n/m` 加减速（3 档：0.05/0.10/0.20 m/s），`b` 退出。按住移动，松开即停。

> ⚠️ 建议把机器人架起（轮子离地）再测试底盘方向；落地测试要确保周围无障碍物。

> 若使用 `keyboard` 库且需 sudo：`sudo /home/zach/miniconda3/envs/lerobot/bin/python examples/test_base_keyboard.py`（必须用 conda 环境 python 完整路径，否则 sudo 会用系统 python 找不到包）。

**底盘方向修正（左右轮装反）**

如果按 `i`（前进）实际变成原地转向、`j`（左转）变成前进，说明**某一侧轮子物理装反了**（正转=后退）。差速指令会让两轮相向而转，看起来就是前进/转向互换了。

修复：在配置里把装反的那一侧设成 `-1`：

```python
config = HumanaLiteConfig(
    ...
    wheel_dir_signs={
        "base_left_wheel": -1,   # 左轮装反 → 取反
        "base_right_wheel": 1,   # 右轮正常
    },
)
```

`+1` = 正 raw 速度驱动轮子向前；`-1` = 该轮装反。指令路径（`_body_to_wheel_raw`）和反馈路径（`_wheel_raw_to_body`）都会应用该符号，保持体坐标系一致。判断哪个轮反了：按 `i` 若往左转，则左轮反；往右转则右轮反。

**跳过升降归零**

`connect()` 默认会自动执行升降归零。测试底盘或其他子系统、且升降已在已知位置时，可跳过：

```python
config = HumanaLiteConfig(
    port1="/dev/ttyACM0",
    port2="/dev/ttyACM1",
    port3=None,
    cameras={},
    home_lift_on_connect=False,   # 跳过自动升降归零
)
```

升降只会被注册和配置（不会运动）。

### 5.6 双机 ZMQ 模式（笔记本遥操 + Jetson/树莓派机器端）

**机器端（Jetson/树莓派）：**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost

host = HumanaLiteHost(HumanaLiteConfig())
host.run()
"
```

默认端口：obs 5556 / cmd 5555。

**遥操端（笔记本）：**

```python
from lerobot_robot_humanalite.humanalite_client import HumanaLiteClient
from lerobot_robot_humanalite import HumanaLiteClientConfig

client = HumanaLiteClient(
    HumanaLiteClientConfig(remote_ip="192.168.1.100")  # Jetson/树莓派 IP
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
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": 0, "fps": 30, "width": 640, "height": 480}, "left_wrist": {"type": "opencv", "index_or_path": 2, "fps": 30, "width": 640, "height": 480}, "right_wrist": {"type": "opencv", "index_or_path": 4, "fps": 30, "width": 640, "height": 480}}' \
    --teleop.type=openarm_mini \
    --teleop.port=/dev/ttyACM_leader \
    --dataset.repo_id=你的名字/my_humanalite_data \
    --dataset.num_episodes=10 \
    --dataset.single_task="描述你的任务"
```

要点：

- 摄像头设备号先用 `lerobot-find-cameras opencv` 确认，再填 `index_or_path`。
- 摄像头名（`head`、`left_wrist`、`right_wrist`）**必须**与训练、部署时保持一致，分辨率也一样（见 8.1 的警告）。
- 纯双臂采集（还没装轮子/升降）时加 `--robot.enable_base=false`。
- 在 Jetson 上 `index_or_path` 可能是 `/dev/video*` 路径而不是整数，按 `lerobot-find-cameras opencv` 的输出填。

### 6.2 双机 ZMQ 模式数据采集

**机器端：**

```bash
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
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
    --dataset.repo_id=你的名字/my_humanalite_data \
    --output_dir=./outputs
```

训练参数可在命令行覆盖：

```bash
lerobot-train --policy=act --dataset.repo_id=... --training.batch_size=32 --training.epochs=100
```

支持的策略类型：`act`、`diffusion`、`smolvla`、`pi0`、`pi05`、`groot` 等。**同一份数据无需重新采集**，只需改 `--policy.type` 即可切换策略对比效果。

---

## 八、模型部署（推理）

### 8.1 单机推理

```bash
lerobot-rollout \
    --policy.path=./outputs/checkpoints/last \
    --robot.type=humanalite \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=/dev/ttyACM2
```

⚠️ **摄像头名和分辨率必须与采集时完全一致**（`head` / `left_wrist` / `right_wrist`，同 640×480）。rollout 时改了摄像头名或分辨率，策略的特征维度对不上，会直接报错。

### 8.2 双机 ZMQ 推理

**机器端运行 ZMQ host，遥操端运行 rollout：**

```bash
# 机器端
python3 -c "
from lerobot_robot_humanalite import HumanaLiteConfig
from lerobot_robot_humanalite.humanalite_host import HumanaLiteHost
HumanaLiteHost(HumanaLiteConfig()).run()
"
```

遥操端目前需要手动加载策略并通过 ZMQ client 发送动作。

---

## 九、升降操作（重点）

升降使用 ST3250 舵机 + T8 丝杆（导程 8mm，行程 300mm，直驱无皮带）。**这是本项目踩坑最多的地方，请完整读这一节。**

### 9.1 归零流程

`connect()` 时升降会自动归零，流程是：

1. 向下走（`Goal_Velocity = -home_down_speed`）
2. **堵转检测**（双保险）：`Present_Current` 电流超过阈值（`home_stall_current_ma=200`），或编码器位置连续两次读数不动（位置冻结），都判定已到底
3. **回退 5°**（`home_backoff_deg=5`，切到 POSITION 模式微抬一下，释放丝杆应力）
4. 记录零点
5. 恢复：写 `Goal_Velocity=0` → 切回 VELOCITY 模式 → 重新上扭矩 → 零点微调

归零后系统自动恢复 VELOCITY 模式 + 扭矩，**可以直接控制**，无需额外操作。

### 9.2 速度单位（关键！）

ST3250 的速度单位由**相位寄存器（地址 18）的 BIT2** 决定：

| BIT2 | 速度单位 | 达到 7.5mm/s 所需 v_max |
|------|----------|--------------------------|
| 0 | 0.732 RPM/raw | ≈ 77 |
| 1 | 0.0146 RPM/raw | ≈ 3853 |

**本机实测 BIT2 = 1**（0.0146 RPM/raw），所以 `v_max=3853` 对应约 7.5mm/s，300mm 行程约 40 秒。

⚠️ 速度单位用错是"升降不动"和"升降猛冲"两大症状的根源：

- 以为单位是 0.732，把 `v_max` 设成 80（0.732 单位下 ≈ 58 RPM）：实际 80 × 0.0146 ≈ 1.2 RPM，**几乎不动**
- 以为单位是 0.732，把 `v_max` 设成 4200（旧文档值）：实际 4200 × 0.0146 ≈ 61 RPM，位置环震荡**过冲**

改 `v_max` 之前，先用 `check_phase.py` 确认自己舵机的 BIT2：

```bash
cd /home/zach/HumanaLite
python3 examples/check_phase.py
```

输出会直接告诉你 BIT2 是 0 还是 1，以及对应的 v_max 建议值。**不要照抄别人的 v_max，先跑这个脚本。**

### 9.3 高度控制（推荐）

```python
# 读取当前高度
height = obs["lift_axis.height_mm"]

# 设置目标高度
action["lift_axis.height_mm"] = 200.0  # 单位 mm
```

内部是 P 控制器：`v_cmd = kp_vel × (目标 - 当前)`，夹在 `±v_max` 之间，再经过安全限位。

### 9.4 直接速度控制

```python
action["lift_axis.vel"] = 500  # 原始速度值，正=上升，负=下降
```

同样会被 `±v_max` 夹住并经过安全限位。

### 9.5 安全保护

- **下限硬保护**：`descent_floor_mm=3`。当前高度 ≤ 3mm 时，任何下行指令都会被压成 0。⚠️ 测试目标高度不能低于 3mm。
- **软限位**：`soft_min_mm=0`、`soft_max_mm=280`，越界方向的速度被钳 0。280mm 是为 300mm 丝杆行程预留 20mm 机械安全余量，避免惯性过冲撞顶。
- **堵转检测**：归零时自动检测（电流 + 位置冻结双保险）。

### 9.6 升降轴测试

验证升降硬件和软件是否正常，无需手臂/摄像头：

```bash
conda activate lerobot
cd /home/zach/HumanaLite
python3 examples/test_lift_only.py
```

流程：连接 → 自动向下归零（堵转即停）→ 升 50mm → 降回 3mm。

- **安全**：脚本含 Ctrl+C 紧急停止（写 `Goal_Velocity=0` + `Torque_Enable=0`）
- **前置**：升降舵机（ID 9）需接在 bus2（`/dev/ttyACM1`）上，12V 供电
- **无需**：手臂、轮子、摄像头、校准
- 该脚本绕过了 `HumanaLite` 类，直接创建只含升降电机的总线，**不碰右臂/轮子/手臂**，排查时最干净

### 9.7 Ctrl+C 紧急停止（重要）

⚠️ **舵机是硬件，不是 Python 对象。** 收到速度指令后会持续转，`Ctrl+C` 退出 Python 进程**不会自动让它停**。必须显式给总线写：

```python
bus.write("Goal_Velocity", "lift_axis", 0)     # 停
bus.write("Torque_Enable", "lift_axis", 0)     # 掉扭矩（可选，让它完全放松）
```

正确写法是把业务逻辑包在 `try/finally`（或 `except KeyboardInterrupt`）里，参考 `test_lift_only.py`：

```python
try:
    lift.home()
    # ... 测试逻辑 ...
except KeyboardInterrupt:
    print("紧急停止...")
    bus.write("Goal_Velocity", "lift_axis", 0)
    bus.write("Torque_Enable", "lift_axis", 0)
finally:
    bus.disconnect()
```

`lift_axis.py` 内部的 `home()` 也做了同样的处理：Ctrl+C 时先停再抛，不会让丝杆继续往下钻。

---

## 十、配置参数说明

### 10.1 HumanaLiteConfig

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `port1` | `/dev/ttyACM0` | 左臂+头部总线端口 |
| `port2` | `/dev/ttyACM1` | 右臂总线端口 |
| `port3` | `/dev/ttyACM2` | 升降+车轮总线端口；设 `None` 启用 2 总线模式 |
| `enable_base` | `True` | 设为 `False` 禁用底盘（轮子）和升降，纯双臂测试 |
| `home_lift_on_connect` | `True` | 设为 `False` 跳过 connect 时的自动升降归零（测试其他子系统时用） |
| `disable_torque_on_disconnect` | `True` | 断开时是否释放扭矩 |
| `max_relative_target` | `None` | 单步位置变化上限（度或 %）；`None` 不限制 |
| `use_degrees` | `False` | `False` 用 -100..100 归一化范围，`True` 用角度 |
| `cameras` | 见 `default_cameras()` | 相机配置（`head` / `left_wrist` / `right_wrist`），可传 `{}` 跳过 |
| `wheel_radius` | 0.0635 m | 车轮半径（127mm 轮径） |
| `wheelbase` | 0.30 m | 轮距 |
| `max_wheel_raw` | 3000 | 最大车轮速度原始值 |
| `wheel_dir_signs` | 两轮 `+1` | 轮子方向符号；某一侧装反时设 `-1`（见 5.5） |
| `teleop_keys` | 见 10.3 | 键盘遥操键位映射 |

### 10.2 LiftAxisConfig

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `True` | 设为 `False` 完全禁用升降 |
| `motor_id` | 9 | 升降舵机 ID |
| `motor_model` | `"sts3250"` | 升降舵机型号（ST3250） |
| `lead_mm_per_rev` | 8.0 | 丝杆导程 (mm/圈) |
| `belt_ratio` | 1.0 | 丝杆每电机转数比；`1.0` = 直驱无皮带 |
| `soft_min_mm` | 0.0 | 软下限 (mm) |
| `soft_max_mm` | 280.0 | 软上限 (mm)，300mm 丝杆行程留 20mm 安全余量 |
| `descent_floor_mm` | 3.0 | 下降硬保护高度 (mm)，低于它拒绝下行 |
| `home_down_speed` | 1500 | 归零下行速度（原始速度值） |
| `home_stall_current_ma` | 200 | 堵转电流阈值 (mA) |
| `home_backoff_deg` | 5.0 | 堵转后回退角度 (°) |
| `kp_vel` | 500.0 | 位置→速度 P 控制器增益 |
| `v_max` | **3853** | 最大速度指令（BIT2=1 时 ≈ 7.5mm/s） |
| `on_target_mm` | 1.0 | 到达判定死区 (mm) |
| `dir_sign` | 1 | 正速度方向；`+1` 表示正速度=上升 |

⚠️ `v_max` 以本机实测的 BIT2=1 为准（3853）。如果你的舵机 BIT2=0，需要改成 ≈77（先跑 `check_phase.py` 确认）。

### 10.3 键盘遥操键位（teleop_keys）

| 键 | 功能 |
|----|------|
| `i` / `k` | 前进 / 后退 |
| `j` / `l` | 左转 / 右转 |
| `n` / `m` | 加速档 / 减速档 |
| `u` / `h` | 升降升 / 升降降 |
| `b` | 退出 |

⚠️ **注意：升降下降键是 `h`，不是 `d`！** 这是本项目的自定义修改，很多初学者按 `d` 没反应。源码见 `config_humanalite.py` 的 `teleop_keys`。

---

## 十一、常见问题

### Q: 报错 "Missing motor IDs" 怎么办？

A: 总线上有舵机没被找到。按顺序排查：

1. **菊花链断线**：总线是串联的，6→7 之间断线会导致 7 及之后全部失联。用 `broadcast_ping` 扫描（见 5.3），看哪些 ID 在线。
2. **舵机 ID 未烧录**：新舵机出厂 ID=1，重复 ID 或未按预期设置都会导致失联。用 `setup_motors()` 逐个重烧。
3. **供电不足**：电机太多时 12V 电源电流不够，末端舵机会失联。单独给升降/轮子供电试试。

### Q: 设备端口 (/dev/ttyACM0) 每次重启后变化？

A: 断电重插后 `ttyACM0` / `ttyACM1` 可能互换。先看实际端口：

```bash
ls -l /dev/serial/by-id/
```

`by-id` 按序列号命名，拔插不变。再用 udev 规则绑定固定名字：

```bash
# /etc/udev/rules.d/99-waveshare.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A1", SYMLINK+="tty_left_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A2", SYMLINK+="tty_right_arm"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="A3", SYMLINK+="tty_base"
```

然后在 Config 中使用 `/dev/tty_left_arm` 等固定路径。

### Q: 报错 "no calibration registered"？

A: 正常现象。未校准时 `get_observation()` 无法归一化关节读数。要么先校准（`connect(calibrate=True)`），要么绕过它：升降测试直接用 `robot.lift_axis.get_height_mm()`。

### Q: 升降完全不动？

A: 按顺序检查：

1. **模式**：升降舵机必须是 VELOCITY 模式。归零后代码会自动恢复，但如果手动改过 `Operating_Mode`，需重新 `connect()` 或 `lift_axis.configure()`。
2. **扭矩**：`Torque_Enable` 是否为 1。舵机掉扭矩后用手能自由转动。
3. **速度单位**：见 9.2。`v_max` 设太小（比如 80）会几乎不动。
4. **下限保护**：高度已经 ≤ `descent_floor_mm=3` 时，下行指令会被压成 0，属于正常保护。
5. 检查接线/供电，用 `broadcast_ping` 看 ID 9 是否在线。

### Q: 升降猛冲 / 过冲？

A: 几乎都是**速度单位失配**。把按 0.732 单位设的 `v_max`（如 4200）直接用到 0.0146 单位的舵机上，速度会严重超预期。先跑 `check_phase.py` 确认 BIT2，再把 `v_max` 改成对应值（BIT2=1 → 3853，BIT2=0 → 77）。如果 BIT2 正确仍过冲，可降低 `kp_vel`。

### Q: Ctrl+C 后升降还在转？

A: 舵机是硬件，Python 退出不会自动停。必须显式写 `Goal_Velocity=0` + `Torque_Enable=0`。业务逻辑要包在 `try/finally` 里，参考 `test_lift_only.py` 和 9.7 节。

### Q: 主臂和从臂的电压不同怎么办？

A: 主臂 C046（7.4V）和从臂 C018（12V）分别用不同的电源供电。ZMQ 模式两台机器各自供电；单机模式用两个电源分别给 Waveshare 板供电。

### Q: 相机找不到？

A: 先跑 `lerobot-find-cameras opencv` 确认设备号，再填进 `cameras` 配置。还没装相机时用 `cameras={}` 跳过，不影响电机测试。

### Q: 升降速度太慢？

A: 直驱 8mm 导程，`v_max=3853`（BIT2=1）时约 7.5mm/s，300mm 约 40 秒，这是当前配置的正常速度。想更快可以加大 `v_max` 和 `kp_vel`，或加同步带增速（同时把 `belt_ratio` 改大，注意机械限位）。

### Q: 用 2 总线还是 3 总线？

A: 本项目实际用的是 **2 总线**（`port3=None`）：升降和轮子并入 bus2，已实测可用。3 总线模式（默认）是完整形态，Waveshare 板够多、想让升降/轮子独占一条总线时用默认即可。

---

## 十二、项目结构

```
/home/zach/HumanaLite/
├── pyproject.toml                              # 包配置 + lerobot 入口点（不依赖 PyPI lerobot）
├── lerobot_robot_humanalite/                   # 主包
│   ├── __init__.py                             # 导出 HumanaLite
 │   ├── config_humanalite.py                    # 配置类（HumanaLiteConfig / LiftAxisConfig / ZMQ 配置）
 │   ├── humanalite.py                           # 主 Robot 类（从动侧）
 │   ├── lift_axis.py                            # 升降轴控制（堵转归零 + P 控制器）
 │   ├── leader.py                               # 主臂 teleoperator（单臂/双臂，见 4.4）
 │   ├── humanalite_host.py                      # ZMQ 双机模式 Host
 │   └── humanalite_client.py                    # ZMQ 双机模式 Client
 ├── examples/
 │   ├── single_machine.py                       # 单机使用示例
 │   ├── teleop_keyboard.py                      # 键盘遥操示例
 │   ├── calibrate_follower.py                   # 从动侧全身校准（见 4.1）
 │   ├── calibrate_leader.py                     # 主臂校准（见 4.4）
 │   ├── diagnose_teleop.py                      # 遥操方向诊断（见 4.4）
 │   ├── test_base_keyboard.py                   # 底盘键盘手动测试（见 5.5）
 │   ├── test_lift_only.py                       # 升降轴测试（见 9.6）
 │   └── check_phase.py                          # 检查舵机速度单位（见 9.2）
├── docs/
│   ├── manual_zh.md                            # 本文件
│   └── manual_en.md                            # English manual
└── README.md
```
