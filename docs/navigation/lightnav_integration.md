# HumanaOpen 导航 — LightNav-0 集成调研与实施方案

> 状态：**调研完成，模拟验证通过，软硬件对接未实施**
> 日期：2026-09-17
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
PORT=8050 lightnav-serve \
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

## 八、接入 HumanaOpen（方案设计，未实施）

### 最小 ZMQ adapter（推荐路径，~50 行 Python）

```python
# 伪代码 — 在 Jetson 上运行
import websockets, cv2, zmq, json, asyncio

async def main():
    # ZMQ 连 HumanaOpenHost: x.vel / theta.vel 动作
    ctx = zmq.Context(); pub = ctx.socket(zmq.PUSH)
    pub.connect(f"tcp://<host_ip>:5555")

    async with websockets.connect("ws://<gpu_ip>:8050") as ws:
        await ws.send(json.dumps({"action":"login","data":{"clientId":"humanaopen"}}))
        await ws.send(json.dumps({"action":"reset","data":{}}))

        cap = cv2.VideoCapture(0)   # 前向 RGB 相机
        while True:
            ok, frame = cap.read()
            _, jpg = cv2.imencode(".jpg", frame)
            await ws.send(json.dumps({
                "action":"next","data":{
                    "seq": n, "image": jpg.tobytes().hex(),
                    "instruction": "walk forward slowly"}}))
            resp = json.loads(await ws.recv())
            fwd, lat, yaw = resp["data"]["actions"]["actions"][0]  # 取最近一步
            dt = 0.25   # 控制周期
            v, w = fwd/dt, yaw/dt
            pub.send_string(json.dumps({"x.vel": v, "theta.vel": w}))
            await asyncio.sleep(dt)
```

关键点：
- `x.vel` / `theta.vel` 直接对应 LightNav 航点的前进/偏航。
- 取 `actions[0]`（下一时刻）即可；用 MPC/滑动平均可平滑。
- `stop=true` 时发 `{x.vel:0, theta.vel:0}`。
- **语音/中文**需要额外 ASR/翻译层（不在本方案范围）。

### 相机
- Jetson 需要一个前向 RGB 相机（当前 /dev/video0 可能是主臂/头部用，需确认/新增）。
- 模型内部会把任意分辨率缩放到其 `video_size`，客户端只需 JPEG 编码即可。

## 九、风险与注意

| 项 | 说明 |
|---|---|
| **无避障** | 模型只看 RGB，感知不到视野外的障碍；紧急停止靠 `stop` 标志 + 用户 WASD/手动控制 |
| **延迟** | 本机单步 644ms（约 1.5Hz 重规划）；远距离移动建议用平滑器，不能每步都突变 |
| **中文指令** | 模型英文训练；中文需要先做翻译/ASR |
| **服务对外** | 必须让 lightnav-serve 监听 `0.0.0.0` 才能被 Jetson 连 |
| **显存** | 16GB 偏紧；跑服务时关闭其他 GPU 大程序 |
| **换伺服/换环境** | 不影响导航（导航只依赖相机+GPU） |

## 十、文件结构

```
docs/navigation/
└── lightnav_integration.md    # 本文档（HumanaOpen 侧）
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
- [ ] 确认 Jetson 前向相机
- [ ] 让服务监听 0.0.0.0
- [ ] 编写 ZMQ adapter（Jetson 上）
- [ ] HumanaOpen + LightNav 实机端到端测试