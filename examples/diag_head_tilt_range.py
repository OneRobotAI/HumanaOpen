"""头部 tilt (ID 13) 真实行程诊断 — 小步试探, 撞限位即停.

为什么: 校准文件里 head_tilt range=[1430, 2096] 只有 666 ticks (~58°),
用户反馈俯仰无法降到最下面. 本脚本绕过校准限制直接驱动 ID 13,
从当前位置向"向下"方向小步移动, 每次检查位置是否变化 (不变=机械限位),
确定真实物理行程, 供重新校准或修正限位.

用法:
    python3 examples/diag_head_tilt_range.py [--step 50] [--max-steps 60]

安全:
- 小步 (默认 50 ticks ≈ 4.4°) + 位置变化检测, 撞限位自动停
- 只动头部 tilt, 不碰其他任何电机
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaLite")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

STEP = 50
MAX_STEPS = 60
if "--step" in sys.argv:
    STEP = int(sys.argv[sys.argv.index("--step") + 1])
if "--max-steps" in sys.argv:
    MAX_STEPS = int(sys.argv[sys.argv.index("--max-steps") + 1])

# 只注册头部 tilt (ID 13) — 在 port1 总线上
bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()

try:
    # 当前位置
    cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
    print(f"起始 raw 位置 = {cur}")
    print(f"校准范围: [1430, 2096] (当前 telop 上限)")

    # 从校准下限开始向"下"试探 (小步进 + 机械限位检测)
    target = cur
    print(f"\n向'下'试探 (STEP={STEP} ticks/步)...")
    for i in range(MAX_STEPS):
        target -= STEP
        bus.write("Goal_Position", "head_tilt", target, normalize=False)
        time.sleep(0.15)

        new_cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
        moved = new_cur != cur
        if not moved:
            print(f"  ⛔ 机械限位! 停在 raw={new_cur} (第 {i} 步)")
            break
        cur = new_cur
        if i % 5 == 0 or i == MAX_STEPS - 1:
            print(f"  步 {i:2d}: raw={cur:>5}")

    print(f"\n向下真实下限 ≈ raw {cur}")
    print(f"  = 归一化 {(cur-2048)*360/4096:+.1f}° (校准文件是 {(1430-2048)*360/4096:+.1f}°)")

    # 回到校准范围中间 (避免留在极限位置)
    print(f"\n回到校准范围中间 (raw 1763)...")
    bus.write("Goal_Position", "head_tilt", 1763, normalize=False)
    time.sleep(0.5)
    cur = int(bus.read("Present_Position", "head_tilt", normalize=False))
    print(f"  当前 raw = {cur}")

except KeyboardInterrupt:
    print("\n⛔ 中断")

finally:
    try:
        bus.disconnect()
    except Exception:
        pass
    print("已断开")
