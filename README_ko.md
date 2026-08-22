# HumanaOpen

[English](README.md) | [中文](README_zh.md) | [Français](README_fr.md) | [한국어](README_ko.md)

**오픈소스 줜휴머노이드 로봇 — 7-DOF 듀얼 암, 차동 구동, 리드스크류 리프트.**

[LeRobot](https://github.com/huggingface/lerobot) 및
[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini) 기반.

## 하드웨어

| 서브시스템 | 모터 | 모델 |
|-----------|--------|-------|
| 왼쪽 팔로워 암 | 8 (7-DOF + 그리퍼) | ST3215 C018 (1:345) |
| 오른쪽 팔로워 암 | 8 (7-DOF + 그리퍼) | ST3215 C018 (1:345) |
| 헤드 (pan/tilt) | 2 | ST3215 C018 (1:345) |
| 리프트 (리드스크류) | 1 | ST3250 (직접 구동, 벨트 없음) |
| 차동 구동 베이스 | 2 | ST3215 C018 (1:345) |
| 리더 암 (텔레옵) | 2 × 8 | STS3215 C046 (1:147) |

> **좌우 규약**: 로봇 자체 좌표계 기준.
> 로봇 뒤에서 같은 방향을 바라볼 때, 왼손 쪽이 **왼쪽 암**(`port1`),
> 오른손 쪽이 **오른쪽 암**(`port2`). 배선이 물리적 암 위치를 결정하며,
> 소프트웨어는 `left_arm_*` → `port1`, `right_arm_*` → `port2`로 매핑합니다.

## 소프트웨어

```
lerobot_robot_humanaopen/
├── __init__.py              # 패키지 export
├── config_humanaopen.py     # HumanaOpenConfig, host/client 설정
├── humanaopen.py            # HumanaOpen Robot 클래스 (팔로워)
├── lift_axis.py             # 스톨 감지 호밍 리프트 축
├── leader.py                # 리더 텔레오퍼레이터 (단일/바이매뉴얼)
├── humanaopen_host.py       # ZMQ 호스트 (로봇 측, 듀얼 머신 모드)
└── humanaopen_client.py     # ZMQ 클라이언트 (텔레옵 측)
examples/
├── record_data.py              # 데이터 수집 (Python API, 전체 파라미터)
├── eval_data.py                # 추론 (ACT 정책 배포)
├── single_machine.py           # 단일 머신 작업
├── teleop_keyboard.py          # ZMQ 키보드 텔레오퍼레이션
├── teleop_leader_to_follower.py  # 전신 텔레옵: 리더 암 + 키보드
├── calibrate_follower.py       # 팔로워 전체 캘리브레이션 (암+헤드+휠+리프트)
├── calibrate_leader.py         # 리더 암 캘리브레이션 (open-arms-mini)
├── diagnose_teleop.py          # 텔레옵 조인트 방향 진단
├── test_base_keyboard.py       # 베이스 전용 키보드 테스트 (리프트/암 제외)
├── test_lift_only.py           # 리프트 축 테스트 (호밍 + 상승/하강)
└── check_phase.py              # 서보 속도 단위 확인 (Phase BIT2)

### 진단 및 튜닝 도구

| 스크립트 | 용도 |
|--------|---------|
| `diag_head_tilt_limits.py` | 헤드 틸트 기계 범위 탐침 (잠금 해제 전/후) |
| `diag_head_tilt_range.py` | 헤드 틸트 범위 진단 |
| `diag_regression.py` | 회귀 테스트 (리프트 + 카메라 + 텔레옵 시퀀스) |
| `diag_st3250_speed.py` | ST3250 모터 속도 프로파일링 (Phase BIT2=1) |
| `diag_follower_gripper.py` | 그리퍼 조인트 진단 |
| `recover_lift_ping.py` | 리프트 모터 통신 ping |
| `speed_test_bit2_0.py` | BIT2=0 속도 검증 |
| `switch_phase_bit2.py` | ST3250 Phase BIT2 레지스터 전환 |
```

## 빠른 시작

```bash
# 1. conda 환경 생성
conda create -n humanaopen python=3.12
conda activate humanaopen

# 2. LeRobot 설치 (필수 의존성)
pip install "lerobot[feetech]"

# 3. HumanaOpen 설치 (editable)
cd /path/to/HumanaOpen
pip install -e . --no-deps


# 선택: SmolVLA 의존성 설치 (transformers, num2words)
pip install -e ".[smolvla]" 2>/dev/null || pip install transformers>=4.48 num2words

# 선택: CUDA 12.8+ GPU (Blackwell / RTX 5060+)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 4. 설치 확인
python -c "from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig; print('✅ OK')"

# 5. 단일 머신 작업
python -c "
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
config = HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
robot = HumanaOpen(config)
robot.connect()
print(robot.get_observation().keys())
"

# 6. 듀얼 머신 ZMQ 모드 (로봇에서 실행)
python -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(port1=/dev/ttyACM0, port2=/dev/ttyACM1, port3=None, cameras={})).run()
"
HumanaOpenHost(HumanaOpenConfig()).run()
```

## 듀얼 머신 배포

프로덕션 배포 시 로봇 하드웨어는 임베디드 보드(Jetson 또는 라즈베리파이)에 연결되고,
정책 추론은 별도 GPU 머신에서 실행됩니다. ZMQ로 통신합니다.
전체 설정은 [Dual-Machine Deployment](README.md#dual-machine-deployment) 섹션을 참조하세요.

아키텍처: 개발 머신(GPU) ←→ Jetson/RPi(Host), ZMQ 포트 5555/5556.

### 라즈베리파이 (Host 전용)
```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})).run()
"
```

### Jetson (Host + 선택적 로컬 추론)
```bash
pip3 install lerobot[feetech]
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
HumanaOpenHost(HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})).run()
"
```

### 네트워크 요구사항
- 동일 LAN, 포트 5555 및 5556 개방
- 대역폭: 카메라당 ~10 Mbps


## 텔레오퍼레이션

### 전신 텔레옵 (리더 암 + 키보드)

`teleop_leader_to_follower.py`는 리더 암으로 팔로워의 팔을 구동하고,
키보드로 헤드/베이스/리프트를 제어합니다:

| 제어 | 키 |
|---------|------|
| 팔 | 리더 암 따름 (플립 비활성화 — 동일 방향 확인됨) |
| 헤드 | `w`/`s` 끄덕임 (상/하), `a`/`d` 흔들기 (좌/우) |
| 베이스 | `i`/`k` 전진/후진, `j`/`l` 회전, `n`/`m` 속도 (0.3x/0.6x/1.0x) |
| 리프트 | `u`/`h` 상승/하강 (3–200mm 제한) |
| 종료 | `b` 또는 Ctrl+C |

```bash
# 기본: 3개 카메라 (head + left_wrist + right_wrist)
python3 examples/teleop_leader_to_follower.py

# 4번째 chest 카메라 추가
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

# Rerun 실시간 카메라 뷰
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6 --display

# 카메라 없이 텔레옵만
python3 examples/teleop_leader_to_follower.py --no-cameras
```

카메라 인자: `--cameras=head,left_wrist` (부분 집합), `--head-camera /dev/videoN`,
`--left-wrist-camera`, `--right-wrist-camera`, `--chest-camera` (각각 디바이스 경로 재정의;
`--*-camera` 인자를 전달하면 해당 카메라가 자동 추가됩니다).

### 카메라 디바이스 및 fps (테스트됨)

| 카메라 | 디바이스 | 포맷 | FPS |
|--------|--------|--------|-----|
| head | /dev/video0 | MJPG | 30 |
| left_wrist | /dev/video2 | MJPG | 30 |
| right_wrist | /dev/video4 | MJPG | **25** (640x480 하드웨어 한계) |
| chest | /dev/video6 | MJPG | 30 |

`lerobot-find-cameras opencv`로 확인하세요. right_wrist는 MJPG 640x480에서
25fps를 초과할 수 없습니다 (v4l2-ctl 검증) — 설정에서 `fps=25`을 유지하지 않으면 연결 실패.

### 리프트 축 — 영점 영속화 (免归零)

리프트는 12비트 싱글턴 엔코더(4096 ticks/rev)가 리드스크류(25회전 = 200mm)를 구동합니다.
절대 위치는 소프트웨어 멀티턴 랩 어라운드 트래킹으로 추적됩니다. 리드스크류가 자체 잠금되므로
전원 사이클 후에도 기계적 위치가 유지됩니다 — 영점 위치가 `~/.cache/humanaopen/lift_zero.json`에
영속화되어 다음 연결 시 복원되며, **재호밍을 건너뜁니다**:

- 첫 연결: 하단까지 하강 (스톨 감지), 영점 저장.
- 이후 연결: 저장된 절대 위치 복원 (이동 불필요).
- 위치가 변경된 경우 (예: 수동으로 리프트 이동), 복원 실패 시 자동 호밍 실행.

리프트 튜닝 (테스트됨): `v_max=110` (raw), `kp_vel=10`, `home_down_speed=10`,
Phase BIT2=0 (raw 유닛당 50 step/s). 최대 속도 ≈ 8.7mm/s (200mm 약 23s).

### 리프트 속도 부스트 (BIT2=0)

ST3250 펌웨어는 Phase BIT2=1에서 `Goal_Velocity`를 raw 유닛당 1 step/s로 매핑하며,
raw > 1000에서 방향이 반전됩니다 (삼각파) — 위험합니다. Phase BIT2=0으로 전환하면
단위가 raw 유닛당 50 step/s로 변경되어, 최대 속도(5500 step/s)는 raw 110에 해당하며
완전히 신뢰 가능한 범위 내입니다. **전환 후 모든 속도 파라미터를 50으로 나눠야 합니다**
(`home_down_speed`, `kp_vel`, `v_max`). 도구:
`examples/switch_phase_bit2.py` (전환), `examples/speed_test_bit2_0.py` (검증).

### 헤드 틸트 범위 잠금 해제

헤드 틸트 서보의 EPROM 위치 한계가 [1430, 2096] (~58°)로 고정되어 있었고,
캘리브레이션 파일이 이를 복사했습니다 — 틸트가 -54°/+4°로 제한됩니다.
`Min=0 / Max=4095`를 쓰면 기계적 범위 [1367, 2242] (-61.6°/+17.1°)이 잠금 해제됩니다:
`examples/unlock_head_tilt.py --probe`. 잠금 해제 후 캘리브레이션 파일
(`~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json`)이
실제 범위로 업데이트되었습니다.

## 데이터 수집

`lerobot-record` CLI는 공식 로봇 타입만 하드코딩하여 `humanaopen`을
인식 불가능한 선택으로 거부합니다. 대신 Python API 래퍼 `examples/record_data.py`를
사용하세요 — `lerobot-record`와 **동일한 파라미터 이름**을 노출하며 시작 시
참조용 동등 CLI 명령을 출력합니다.

### 3개 카메라 (기본)

```bash
python3 examples/record_data.py \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
    --robot.confirm_lift_after_home=true \
    --teleop.type=humanaopen_teleop \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=your-name/humanaopen_demo \
    --dataset.single_task="작업을 설명하세요" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true
```

### 4개 카메라 (네비게이션용 chest 포함)

위와 동일하며 `--robot.cameras` JSON에 chest를 추가:

```bash
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
```

> **주의**: 카메라 이름은 수집/학습/배포 간 일치해야 합니다.
> right_wrist는 640x480에서 **25fps**로 제한됩니다 (하드웨어 한계); 나머지는 30fps.

### 녹화 중 컨트롤

| 제어 | 키 |
|---------|------|
| 팔 | 리더 암 따름 (16 DOF) |
| 헤드 | `w`/`s` 끄덕임, `a`/`d` 흔들기 (2 DOF) |
| 베이스 | `i`/`k` 전진/후진, `j`/`l` 회전 (2 DOF, 속도 `n`/`m`) |
| 리프트 | `u`/`h` 안전 한계 포함 상승/하강 (1 DOF, 3–200mm 제한) |
| 녹화 | `C` 시작, `Q` 종료, `A` 에피소드 재녹화 |
| 확인 | 호밍 후 `u`/`h`로 위치 조정, `ENTER`로 확인 |

`--teleop.type=humanaopen_teleop` 텔레오퍼레이터는 **전체 21 DOF**를 기록합니다 —
리더 암(16 조인트)과 키보드 제어 헤드/리프트/베이스(5 DOF). 둘 다 ACT 학습용
데이터셋에 저장됩니다.

### 녹화 중 리프트 동작

- 첫 연결: 리프트가 **하단으로 호밍** (스톨 감지), 영점을 `~/.cache/humanaopen/lift_zero.json`에 저장.
- 이후 연결: 리프트가 **저장된 위치 복원** (호밍 불필요),
  위치가 변경된 경우 제외 (수동 밀기 → 복원 실패 → 자동 호밍).
- 호밍 후: 키보드 `u`/`h`를 눌러 안전 한계 내에서 높이 조정
  (3mm–200mm), `ENTER`로 확인 후 녹화 시작.

### 데이터셋 재개/정리

이전 실행에서 데이터셋 디렉토리가 이미 존재하는 경우 삭제하거나 재개:

```bash
rm -rf ~/.cache/huggingface/lerobot/your-name/humanaopen_demo    # 새로 시작
# 또는 record_data.py 명령에 --dataset.resume=true 추가           # 마지막 에피소드부터 계속
```

## 학습

### ACT (action chunking transformer)

```bash
# 빠른 테스트 (2 에피소드)
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=your-name/humanaopen_act_policy \
    --dataset.repo_id=your-name/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_act_demo \
    --batch_size=3 \
    --steps=5

# 프로덕션 (>50 에피소드)
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

### SmolVLA (vision-language-action model)

SmolVLA는 녹화 중 사용된 `--dataset.single_task`의 언어 지시가 필요합니다.
VLM 가중치(~500M)는 첫 실행 시 HuggingFace에서 자동 다운로드됩니다.

```bash
# 빠른 테스트 (2 에피소드)
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

> **참고**: SmolVLA(~450M params)는 ACT(~52M)보다 ~20배 무겁고, 더 많은 VRAM을 사용하며,
> 학습이 느립니다. Batch size 4는 8GB VRAM(RTX 5060 Ti)에 적합합니다. >50 에피소드의 경우
> steps를 20000+로 증가시키세요.

### 주요 파라미터

| 파라미터 | 기본값 | 설명 |
|-----------|---------|-------------|
| `--policy.type` | — | **필수.** `act`, `smolvla`, `diffusion` 등. |
| `--policy.device` | `cuda` | `cuda` / `cpu`. |
| `--policy.push_to_hub` | `true` | 학습 후 HuggingFace Hub에 모델 푸시. |
| `--policy.repo_id` | — | 학습된 모델의 Hub repo. 푸시 시 필수. |
| `--dataset.repo_id` | — | **필수.** 학습 데이터셋의 Hub repo. |
| `--output_dir` | — | 로컬 체크포인트 디렉토리. |
| `--batch_size` | 8 | 스텝당 샘플 수. ACT: 32, SmolVLA: 4 (8GB VRAM 한계). |
| `--steps` | 100000 | 총 학습 스텝. ACT: 50K, SmolVLA: 20K. |

### 출력

```
outputs/humanaopen_act_demo/
├── pretrained_model/           # 전체 모델 (설정 + 가중치)
├── last/pretrained_model       # 최신 체크포인트
├── train_logs/                 # 학습 메트릭 (TensorBoard 호환)
└── training_state.json         # 옵티마이저/스케줄러 상태 (재개용)
```

푸시된 모델은 `https://huggingface.co/your-name/humanaopen_act_policy`에 있습니다.

## 추론 (배포)

> **의존성**: SmolVLA는 `transformers>=4.48` 및 `num2words`가 필요합니다.
> SmolVLA 추론 실행 전 `pip install transformers>=4.48 num2words`로 설치하세요.

### ACT 추론 (휴먼 오버라이드 포함)

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
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
    --teleop.type=humanaopen_teleop \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --num-episodes=5 \
    --duration=30 \
    --fps=30
```

### SmolVLA 추론 (언어 조건부, 오버라이드 없음)

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
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 25, "fourcc": "MJPG"}}' \
    --num-episodes=2 \
    --duration=10 \
    --fps=10
```

> **SmolVLA 성능 참고**: VLM 추론은 ~1s/frame (450M params). 10s 에피소드를
> 10fps = 100 frames로 실행하면 ≈ 100s 실제 대기 시간. 실시간 배포에는
> ACT(~50ms/frame)를 사용하세요. SmolVLA는 언어 조건부 작업에 가장 적합합니다.

### 추론 중 컨트롤

| 제어 | 키 | 참고 |
|---------|------|-------|
| Override (ACT 전용) | `e` (누르는 중) | 팔을 리더 제어로 전환 |
| 종료 | `q` | 모든 에피소드 중지 |

**휴먼 오버라이드** (ACT 전용):
- `e` 누르는 중: 팔이 리더를 따름, 헤드/리프트/베이스는 키보드, 정책 일시 중지
- `e` 놓기: 정책 제어로 복귀

## 라이선스

Apache 2.0
