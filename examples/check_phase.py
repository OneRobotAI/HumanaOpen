"""读取升降舵机相位寄存器, 确认速度单位."""
import time

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="/dev/ttyACM1",
    motors={"lift_axis": Motor(9, "sts3250", MotorNormMode.DEGREES)},
)
bus.connect()

try:
    phase = int(bus.read("Phase", "lift_axis", normalize=False))
    bit2 = (phase >> 2) & 1
    print(f"Phase 寄存器 (地址18) = 0x{phase:X} = 0b{phase:08b}")
    print(f"BIT2 = {bit2}  →  速度单位 = {'0.0146 RPM/raw' if bit2 else '0.732 RPM/raw'}")

    if bit2:
        # 0.0146 单位: 需要 56.25rpm → v_max ≈ 3853
        print(f"  对应目标 7.5mm/s (300mm/40s): v_max ≈ 3853")
    else:
        # 0.732 单位: 需要 56.25rpm → v_max ≈ 77
        print(f"  对应目标 7.5mm/s (300mm/40s): v_max ≈ 77")

finally:
    try:
        bus.disconnect()
    except Exception:
        pass
