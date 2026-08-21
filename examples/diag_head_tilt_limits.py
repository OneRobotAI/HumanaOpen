"""头部 tilt 极限精测 — 确认机械硬限位 + 定位干涉点.

目的: 解锁舵机限制后, 确认向下 1347 / 向上 2242 是否机械硬限位,
以及极限附近电流变化 (堵转特征), 判断是否还有机械改造空间.

用法:
    python3 examples/diag_head_tilt_limits.py
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()
name = "head_tilt"


def probe(target, wait=0.6):
    """写目标位置, 等待, 返回 (最终位置, 电流)."""
    bus.write("Goal_Position", name, target, normalize=False)
    time.sleep(wait)
    pos = int(bus.read("Present_Position", name, normalize=False))
    cur = 0
    try:
        cur = int(bus.read("Present_Current", name, normalize=False))
    except Exception:
        pass
    return pos, cur


try:
    bus.write("Torque_Enable", name, 1)
    time.sleep(0.5)

    # 从已知边界外 100 ticks 开始, 每 10 ticks 逼近, 观察电流爬升
    print("向下极限精测 (从 1247 开始):")
    for raw in range(1247, 1367, 10):
        pos, cur = probe(raw)
        deg = (pos - 2048) * 360 / 4096
        print(f"  target={raw:>4} → pos={pos:>4} ({deg:+.1f}°)  I={cur}mA")
        if pos < raw - 30:  # 舵机拒绝接近目标 (硬限位)
            print(f"  ⛔ 硬限位确认在 pos={pos} 附近")
            break

    # 回到中位
    probe(2048)
    print()

    print("向上极限精测 (从 2342 开始):")
    for raw in range(2342, 2222, -10):
        pos, cur = probe(raw)
        deg = (pos - 2048) * 360 / 4096
        print(f"  target={raw:>4} → pos={pos:>4} ({deg:+.1f}°)  I={cur}mA")
        if pos > raw + 30:
            print(f"  ⛔ 硬限位确认在 pos={pos} 附近")
            break

    probe(2048)

except KeyboardInterrupt:
    print("\n⛔ 中断")

finally:
    try:
        bus.write("Goal_Position", name, 2048, normalize=False)
        time.sleep(0.5)
        bus.write("Torque_Enable", name, 0)
    except Exception:
        pass
    try:
        bus.disconnect()
    except Exception:
        pass
    print("已断开")
