"""解锁头部 tilt (ID 13) 舵机内部位置限制 + 重录行程.

发现: 舵机 EPROM 里 Min/Max_Position_Limit = [1430, 2096], 只有 ~58°,
导致头部俯仰无法降到最下面. 校准文件的范围就是复制自这里.

修复:
1. 写 Min_Position_Limit = 0, Max_Position_Limit = 4095 (STS3215 300° 全行程)
2. 小步试探真实机械行程 (撞限位自动停)
3. 回到中间位置

用法:
    python3 examples/unlock_head_tilt.py [--probe]

⚠️ 只动头部 tilt (ID 13). 需要 Torque_Enable=0 才能改限制寄存器.
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaLite")
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

PROBE = "--probe" in sys.argv

bus = FeetechMotorsBus(
    port="/dev/ttyACM0",
    motors={"head_tilt": Motor(13, "sts3215", MotorNormMode.DEGREES)},
)
bus.connect()

name = "head_tilt"
try:
    # 1. 关扭矩 → 解锁限制
    print("[1] 关扭矩...")
    bus.write("Torque_Enable", name, 0)
    time.sleep(0.3)

    # 2. 读当前限制
    for label, addr in [("Min_Position_Limit", 9), ("Max_Position_Limit", 11)]:
        val = bus._read(addr, 2, 13, raise_on_error=True)[0]
        print(f"    当前 {label} = {val}")

    # 3. 写入 0 / 4095 (需先 Lock=0)
    print("[2] 写全行程限制 [0, 4095]...")
    try:
        bus.write("Lock", name, 0)
    except Exception:
        pass
    time.sleep(0.2)
    bus._write(9, 2, 13, 0)        # Min = 0
    bus._write(11, 2, 13, 4095)    # Max = 4095
    time.sleep(0.3)
    try:
        bus.write("Lock", name, 1)
    except Exception:
        pass

    # 4. 验证
    print("[3] 验证:")
    ok = True
    for label, addr in [("Min_Position_Limit", 9), ("Max_Position_Limit", 11)]:
        val = bus._read(addr, 2, 13, raise_on_error=True)[0]
        print(f"    {label} = {val}")
        if label.startswith("Min") and val != 0:
            ok = False
        if label.startswith("Max") and val != 4095:
            ok = False
    print(f"    {'✅ 限制已解锁!' if ok else '⚠️ 写入未生效'}")

    # 5. 可选: 试探真实行程
    if PROBE:
        print("\n[4] 试探真实行程 (小步, 撞限位停):")
        bus.write("Torque_Enable", name, 1)
        time.sleep(0.3)
        cur = int(bus.read("Present_Position", name, normalize=False))
        print(f"    起始 raw={cur}")
        # 向下试探
        target = cur
        for i in range(80):
            target -= 50
            bus.write("Goal_Position", name, target, normalize=False)
            time.sleep(0.15)
            new_cur = int(bus.read("Present_Position", name, normalize=False))
            if new_cur == cur:
                print(f"    ⛔ 向下限位 raw={new_cur} ({(new_cur-2048)*360/4096:+.1f}°)")
                break
            cur = new_cur
        # 向上试探 (从当前向下限位点)
        print("    向上试探:")
        target = cur
        for i in range(120):
            target += 50
            bus.write("Goal_Position", name, target, normalize=False)
            time.sleep(0.15)
            new_cur = int(bus.read("Present_Position", name, normalize=False))
            if new_cur == cur:
                print(f"    ⛔ 向上限位 raw={new_cur} ({(new_cur-2048)*360/4096:+.1f}°)")
                break
            cur = new_cur
        # 回到中间
        bus.write("Goal_Position", name, 2048, normalize=False)
        time.sleep(0.5)
        print(f"    回到中间 raw={int(bus.read('Present_Position', name, normalize=False))}")

except KeyboardInterrupt:
    print("\n⛔ 中断")

finally:
    try:
        bus.write("Goal_Position", name, 2048, normalize=False)
        time.sleep(0.3)
        bus.write("Torque_Enable", name, 0)
    except Exception:
        pass
    try:
        bus.disconnect()
    except Exception:
        pass
    print("已断开")
