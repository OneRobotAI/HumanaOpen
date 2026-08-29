"""Read the lift servo phase register to confirm the speed unit."""
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
        # 0.0146 unit: needs 56.25rpm → v_max ≈ 3853
        print(f"  对应目标 7.5mm/s (300mm/40s): v_max ≈ 3853")
    else:
        # 0.732 unit: needs 56.25rpm → v_max ≈ 77
        print(f"  对应目标 7.5mm/s (300mm/40s): v_max ≈ 77")

finally:
    try:
        bus.disconnect()
    except Exception:
        pass
