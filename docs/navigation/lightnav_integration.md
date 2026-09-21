# HumanaOpen 导航 — LightNav-0 集成调研与实施方案

> 状态：**调研完成，模拟验证通过，实机接入完成（直行 + 转向测试通过）**
> 日期：2026-09-17（调研）/ 2026-09-18（实机接入）
> 硬件：PC (RTX 5060 Ti 16GB) 为 GPU 推理服务器，Jetson 为机器人端

## 一、结论摘要

- **LightNav-0 可行**：已在 PC 上完成环境安装、模型加载、MuJoCo 模拟语言导航全链路验证（全 PASS）。
- **HumanaOpen 代码零修改**：导航作为"外挂"，通过约 50 行 ZMQ adapter 与 HumanaOpen 底盘接口衔接。
- **不需要 ROS 层**（最小方案）；ROS 2 完整栈是可选升级，非前提。
- **传感器需求极简**：只需一个前向 RGB 摄像头（无激光雷达、无深度、无地图、无里程计）。

## 二、LightNav-0 是什么

- **VLM 导航模型**（Qwen3-VL-4B 底座）：输入单目 RGB 历史帧 + 自然语言指令 → 输出 10 个 SE(2) 未来航点 `[forward_m, lateral_m, yaw_rad]`。
- **不是 SLAM / move_base / 地图框架**：无定位、无建图、无障碍感知层；纯端到端视觉语言 → 航点，每帧重规划。
- 单模型覆盖：语言指令导航（VLN）、开放词汇找物（ObjectNav）、视觉目标追踪（EVT），跨机器人零样本迁移（官方演示过 humanoid/quadruped/wheeled/aerial）。
- 项目主页/源码：`lightorigins/LightNav-0`，Apache 2.0，arXiv 2608.30935。
- 模型权重：HuggingFace `LightOriginsHQ/LightNav-0`（需 HF 登录；仓库内文件 ~9.6GB）。

## 三、硬件与运行要求

| 项 | 要求 | 实测（本机 5060 Ti） |
|---|---|---|
| GPU | ~15GB 显存（4B bf16 ~10GB + KV cache ~2.3GB）| ✅ 16GB 可用，占用 ~8.7GiB |
| 架构 | 官方验证 sm_103 (B300)；消费级 Blackwell (sm_120) 实测可跑 | ✅ |
| Python | >=3.11, <3.12 | ✅ 独立 conda 环境 `lightnav` |
| torch | >=2.9；**Blackwell 需 cu129 wheel**（2.10.0+cu129）| ✅ |
| vLLM | **0.19.1 精确锁定**（绑定私有 API）| ✅ |
| 推理延迟 | 官方 60-150ms/步；本机实测 644ms/步（warmup 后）| 可用 |

传感器：**单目 RGB 前向摄像头**（参考：Orbbec Gemini 330, 640×360@30；任意 rgb8 相机可）。
机器人：任意移动底盘；官方参考 Unitree Go2 / LimX TRON1；**MuJoCo demo 用差速 TurtleBot（与 HumanaOpen 同运动学）**。

## 四、部署架构（与 HumanaOpen 的关系）

```
┌─ LightNav 世界 ─────────────┐      ┌─ HumanaOpen 世界 ─────────────┐
│ GPU 服务器 (PC)              │      │ Jetson 机器人端                 │
│  lightnav-serve :8050        │      │  HumanaOpenHost (ZMQ 5555/5556) │
│  ←WebSocket JSON→            │      │  底盘吃 x.vel / theta.vel       │
│        │                     │      │                                │
│        └─ 航点 → ZMQ adapter ─┼────▶│  差速电机                      │
│    (adapter 约 50 行 Python) │      │                                │
└──────────────────────────────┘      └────────────────────────────────┘
```

- **模型服务器**：GPU 机器（PC），跑 `lightnav-serve`，是独立 conda 环境 `lightnav`。
- **客户端（adapter）**：Jetson 上，相机 → JPEG → WebSocket `next` → 拿航点 → 换算 `v=forward/dt, w=yaw/dt` → ZMQ 发给 HumanaOpenHost 的 `x.vel/theta.vel`。
- **HumanaOpen 代码不改**：adapter 只向已有的 ZMQ action 塞值。

### 可选：ROS 2 完整栈（暂不采用）
官方 `robot_deploy/` 是 ROS 2 Humble 栈（相机驱动 + vln_client + vln_mpc + vln_web + 适配器），提供 MPC 平滑、Web 控制面板、看门狗、手自动切换。**需要装 ROS 2 + 写 humano_adapter**，工作量大，暂缓。

## 五、安装步骤（已在 PC 完成，存档）

```bash
# 1. 独立 Python 3.11 环境
conda create -n lightnav python=3.11 -y
conda activate lightnav

# 2. Blackwell 必需：cu129 torch（普通 cu12.8 无法 JIT）
pip install torch==2.10.0+cu129 torchvision==0.25.0+cu129 \
  --index-url https://download.pytorch.org/whl/cu129

# 3. LightNav 本体
cd ~/LightNav-0
pip install -e ".[vllm,video]"

# 4. HF 登录（代理环境需先装 socksio）
pip install "httpx[socks]"
hf auth login --token <TOKEN> --add-to-git-credential

# 5. 下载权重
mkdir -p checkpoints/LightNav-0
hf download LightOriginsHQ/LightNav-0 --local-dir checkpoints/LightNav-0

# 6. GPU 冒烟测试（全 PASS 才继续）
MODEL_PATH=checkpoints/LightNav-0 bash scripts/smoke_gpu.sh
```

## 六、启动模型服务器（GPU 机器上常驻）

```bash
cd ~/LightNav-0 && conda activate lightnav
CUDA_VISIBLE_DEVICES=0 GPU_MEM_UTIL=0.78 \
HOST=0.0.0.0 PORT=8050 lightnav-serve \
    --task vln \
    --model_path checkpoints/LightNav-0 \
    --backend vllm_local
```

- 监听 `127.0.0.1:8050`（本机）。**要让 Jetson 连接必须监听对对外地址**，启动前确认 `lightnav-serve` 的 host 参数（或设 `--host 0.0.0.0`）。
- 首次启动含模型加载+JIT 编译约 1-2 分钟；之后单步推理约 100-644ms。
- 显存不够时把 `GPU_MEM_UTIL` 降到 0.70。

## 七、MuJoCo 模拟验证（已通过）

```bash
# 服务终端保持运行，另开终端：
cd ~/LightNav-0/mujoco_demo
./run.sh --vln-server ws://127.0.0.1:8050
# 浏览器打开 http://127.0.0.1:8088，输入英文指令（如 "walk to the red trash can"）
```

- 模拟差速 TurtleBot（与 HumanaOpen 同运动学）在 ProcTHOR 室内场景语言导航。
- 模型英文训练，**中文指令不支持**，请用英文。

## 八、接入 HumanaOpen（已实施）

### ZMQ adapter（实际实现：`examples/lightnav_navigation.py`）

在 Jetson 上运行（Jetson 只需 `pip install websockets`，无需安装 LightNav/GPU 推理——模型全部在 PC 上跑）：

```bash
cd ~/HumanaOpen && git pull
# 启动 HumanaOpenHost（纯底盘，相机由 adapter 自抓）
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={},   # 导航不需要 host 传图，adapter 自己抓 chest 相机
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
# 另一个终端：跑导航 adapter
NO_PROXY="192.168.1.12" python3 examples/lightnav_navigation.py \
    --lightnav ws://192.168.1.12:8050 \
    --zmq-host 127.0.0.1 \
    --camera /dev/video0 \
    --instruction "walk forward slowly"
```

工作流程：
1. `cv2` 抓 chest 相机一帧 → JPEG（q80，640x360）→ WebSocket 发给 PC 的 lightnav-serve
2. 服务返回 10 个 SE(2) 航点 `[forward_m, lateral_m, yaw_rad]`（RVQ 量化）
3. **控制律**（移植 LightNav 官方 mujoco demo 的 `waypoint_command`，非"航点÷dt"的朴素除法）：
   - 只用 `waypoints[0]`（当前帧的动作；后面的是预测路径，用了会放大 atan2 噪声导致满档旋转）
   - distance < 0.08m → 视为量化噪声，静止 `(0,0)`
   - `angular = clamp(1.8·bearing + 0.25·target_yaw)`，bearing/yaw 各带死区滤量化电平
   - `linear = clamp(0.75·distance·cos(bearing), 0, 0.35)`；`|bearing|>65°` 时 linear=0（先转向再前进）
4. `{"x.vel": v m/s, "theta.vel": w deg/s}` 经 ZMQ PUSH 发到 HumanaOpenHost:5555

关键点：
- `stop=true` 或航点空 → 发 `{x.vel:0, theta.vel:0}`；Ctrl+C 也会主动归零（而非只靠 watchdog）
- **RVQ 量化陷阱**（实机踩坑记录）：action tokenizer 把"无转向"量化成 `yaw=±0.314`（≈±π/10），把"直行一步"量化成 `forward≈0.15m`。直接 `yaw/dt` 会得到 ±72°/s 的疯狂自转；直接 `forward/dt` 是 0.6 m/s 的冲撞速度。必须用上述官方控制律 + 死区。
- **代理变量**：`websockets` 库会读 http/socks 代理环境变量，Jetson 上连局域网 GPU 必须 `NO_PROXY=192.168.1.12`，否则连不上。
- **语音/中文**需要额外 ASR/翻译层（模型英文训练）——不在当前方案范围。

### 相机
- 实机使用 Jetson 的 `Integrated_Webcam_HD`（USB，原生 MJPG 1280x720@30 / YUYV 640x480@25）作为 **chest 前向相机 `/dev/video0`**。
- 注意：这台相机 lerobot 的 `OpenCVCamera` 无法设置分辨率（`set()` 恒返回 False），因此 host 用 `cameras={}` 纯底盘模式，图像完全由 adapter 的 `cv2` 直接抓取（`cv2.VideoCapture` 读 `/dev/video0` 正常）。
- 模型内部把任意分辨率缩放到其 `video_size`，客户端只需 JPEG 编码。

## 九、实机验证结果（2026-09-18）

### 环境
- Jetson（host，`humanaopen` conda env，Python 3.12）：HumanaOpenHost 纯底盘模式 + adapter；唯一外设：chest 相机 `/dev/video0`
- PC（GPU，`lightnav` env）：lightnav-serve 常驻 `0.0.0.0:8050`，模型 8.7GiB 显存

### 关键数据
| 项 | 实测 |
|---|---|
| 单帧推理延迟（Jetson→PC→Jetson RTT） | **~200-350ms**（比 644ms 的纯本机 warmup 快，服务常驻后更稳）|
| 直行 `"walk forward slowly"` | **0.113 m/s 平稳直行**，无自转、无抖动 |
| 左转弧线 `"go to the object on your left"` | **0.11 m/s + 15°/s 左转**（模型输出 lateral=0.022m → bearing=8.4° → 1.8×=15°/s）|
| 静止（噪声航点）| **精确归零**——RVQ 量化噪声（yaw=±0.314）被死区滤掉，不再 ±72°/s 狂转 |
| Watchdog 联动 | host 500ms 超时正常；adapter 4Hz 控制周期在超时内 |

### 踩坑记录（按时间顺序）
1. **`host+cameras` 启动崩溃**：`OpenCVCamera(/dev/video0)` 校验失败——这台 USB 相机 `set(CAP_PROP_*)` 恒返 False，`lerobot` 把它当失败。→ 改用 `cameras={}` 纯底盘模式。
2. **±72°/s 自转**（首批测试）：直接 `yaw/dt`，量化 `±0.314rad` 变成满档旋转。→ 引入官方 `waypoint_command`。
3. **±45°/s 抖动**（第二批）：官方 0.35m 距离门槛在 0.15m 步长下全被当噪声，回退 `valid[-1]` 放大 atan2 符号噪声。→ 门槛降到 0.08m + bearing/yaw 死区。
4. **-45°/s 残留**（第三批）：搜索"第一个够远点"时，序列后面的远点 bearing 极大，overrode waypoint[0]。→ 只用 `waypoint[0]` 作为当前帧动作。

### 结论
- **导航链路完整可用**：相机 → GPU 推理 → 控制律 → 底盘，全部打通。
- 模型对"左右/前进"的语义理解正确，会输出对应的横向位移 + 转向组合。
- 当前速度保守（0.11 m/s、15°/s）；调参可改 `--max-linear` / `--max-angular`。

## 十、风险与注意

| 项 | 说明 |
|---|---|
| **无避障** | 模型只看 RGB，感知不到视野外的障碍；紧急停止靠 `stop` 标志 + 用户 WASD/手动控制 |
| **延迟** | 实测单步 ~200-350ms（约 3-5Hz 重规划）；远距离移动建议用平滑器，不能每步都突变 |
| **中文指令** | 模型英文训练；中文需要先做翻译/ASR |
| **服务对外** | lightnav-serve 必须监听 `0.0.0.0` 才能被 Jetson 连（`HOST=0.0.0.0` 环境变量） |
| **代理** | Jetson 连 `ws://192.168.1.12:8050` 需 `NO_PROXY=192.168.1.12`（websockets 读代理变量） |
| **显存** | 16GB 偏紧；跑服务时关闭其他 GPU 大程序 |
| **换伺服/换环境** | 不影响导航（导航只依赖相机+GPU） |

## 文件结构

```
docs/navigation/
└── lightnav_integration.md    # 本文档（HumanaOpen 侧）
HumanaOpen 侧实现:
examples/lightnav_navigation.py  # ZMQ adapter：相机抓帧 → ws → 控制律 → 底盘
External:
~/LightNav-0/                   # LightNav 仓库（独立项目，不并入 HumanaOpen）
  ├── src/lightnav/             # 模型推理 + WebSocket 服务
  ├── robot_deploy/             # （可选）ROS2 参考栈
  ├── mujoco_demo/              # 差速机器人仿真（已验证）
  └── docs/                     # PROTOCOL/DEPLOYMENT/CONFIGURATION
```

## 十一、后续路线

- [x] 环境安装 + GPU 冒烟测试（全 PASS）
- [x] 模型服务启动
- [x] MuJoCo 模拟语言导航验证
- [x] 确认 Jetson 前向相机（chest `/dev/video0`，`Integrated_Webcam_HD`）
- [x] 让服务监听 0.0.0.0
- [x] 编写 ZMQ adapter（Jetson 上，`examples/lightnav_navigation.py`）
- [x] HumanaOpen + LightNav 实机端到端测试（直行 + 左转弧线均通过）
- [ ] 避障增强（当前模型无避障，仅 RGB 语义导航）
- [ ] 调参优化速度/转向手感（`--max-linear` / `--max-angular`）
- [ ] 目标点停止精度验证（`stop` 标志在实机上的到位表现）