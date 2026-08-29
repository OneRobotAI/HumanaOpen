"""Unlock the head tilt (ID 13) servo's internal position limits + re-record the travel range.

Finding: the servo EPROM holds Min/Max_Position_Limit = [1430, 2096], only ~58°,
which prevents head pitch from reaching the lowest position. The calibration file
range is simply copied from here.

Fix:
1. Write Min_Position_Limit = 0, Max_Position_Limit = 4095 (STS3215 300° full travel)
2. Probe the real mechanical travel in small steps (stops automatically at the limit)
3. Return to the center position

Usage:
    python3 examples/unlock_head_tilt.py [--probe]

⚠️ Only touches the head tilt (ID 13). Torque_Enable=0 is required to modify the limit registers.
"""

import sys
import time
import builtins

sys.path.insert(0, "/home/zach/HumanaOpen")
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
    # 1. Disable torque -> unlock the limits
    print("[1] 关扭矩...")
    bus.write("Torque_Enable", name, 0)
    time.sleep(0.3)

    # 2. Read current limits
    for label, addr in [("Min_Position_Limit", 9), ("Max_Position_Limit", 11)]:
        val = bus._read(addr, 2, 13, raise_on_error=True)[0]
        print(f"    当前 {label} = {val}")

    # 3. Write 0 / 4095 (requires Lock=0 first)
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

    # 4. Verify
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

    # 5. Optional: probe the real travel
    if PROBE:
        print("\n[4] 试探真实行程 (小步, 撞限位停):")
        bus.write("Torque_Enable", name, 1)
        time.sleep(0.3)
        cur = int(bus.read("Present_Position", name, normalize=False))
        print(f"    起始 raw={cur}")
        # Probe downward
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
        # Probe upward (from the current lower-limit point)
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
        # Return to center
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
