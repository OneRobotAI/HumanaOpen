"""ZMQ host — runs on the robot side (Jetson / Raspberry Pi).

Connects to the real hardware and forwards observations / receives
action commands from a remote ``HumanaOpenClient`` over ZMQ.
"""

from __future__ import annotations

import logging
import struct
import time
import traceback
from typing import Any

import numpy as np
import zmq

from .config_humanaopen import HumanaOpenConfig, HumanaOpenHostConfig
from .humanaopen import HumanaOpen

logger = logging.getLogger(__name__)


def _serialize_obs(obs: dict[str, Any]) -> bytes:
    """Pack an observation dict into a flat byte buffer.

    Layout (little-endian):
      [4 bytes]  magic           0x4F4253
      [4 bytes]  n_floats         number of float32 values
      [4 bytes]  n_images         number of images
      For each float:
        [4 bytes] key_len + key_utf8 + [4 bytes] float32 value
      For each image:
        [4 bytes] key_len + key_utf8
        [4 bytes] H, [4 bytes] W, [4 bytes] C
        [H*W*C bytes] np.uint8 data
    """
    floats = {k: v for k, v in obs.items() if isinstance(v, (int, float, np.floating))}
    images = {k: v for k, v in obs.items() if isinstance(v, np.ndarray) and v.ndim == 3}

    buf = bytearray()
    buf.extend(struct.pack("<III", 0x4F4253, len(floats), len(images)))

    for k, v in floats.items():
        k_bytes = k.encode()
        buf.extend(struct.pack("<I", len(k_bytes)))
        buf.extend(k_bytes)
        buf.extend(struct.pack("<f", float(v)))

    for k, v in images.items():
        k_bytes = k.encode()
        buf.extend(struct.pack("<I", len(k_bytes)))
        buf.extend(k_bytes)
        H, W, C = v.shape
        buf.extend(struct.pack("<III", H, W, C))
        buf.extend(v.astype(np.uint8).tobytes())

    return bytes(buf)


def _deserialize_cmd(data: bytes) -> dict[str, Any]:
    """Unpack an action dict from bytes (mirror of above)."""
    action: dict[str, Any] = {}
    pos = 0
    # Client _serialize_cmd 用 "<II" (magic, n_floats) — 不是 "<III"
    magic, n_floats = struct.unpack_from("<II", data, pos)
    pos += 8
    if magic != 0x4F4253:
        raise ValueError(f"Bad magic: {magic:#x}")

    for _ in range(n_floats):
        klen = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        key = data[pos : pos + klen].decode()
        pos += klen
        val = struct.unpack_from("<f", data, pos)[0]
        pos += 4
        action[key] = val

    return action


class HumanaOpenHost:
    """Robot-side ZMQ host that serves observations and accepts commands.

    Usage
    -----
    .. code-block:: python

        host = HumanaOpenHost(robot_config, host_config)
        host.run()  # blocks until interrupted
    """

    def __init__(
        self,
        robot_cfg: HumanaOpenConfig,
        host_cfg: HumanaOpenHostConfig | None = None,
    ):
        self.robot_cfg = robot_cfg
        self.host_cfg = host_cfg or HumanaOpenHostConfig()
        self._robot: HumanaOpen | None = None
        self._ctx: zmq.Context | None = None

    def run(self) -> None:
        robot = HumanaOpen(self.robot_cfg)
        robot.connect(calibrate=True)
        self._robot = robot

        ctx = zmq.Context()
        self._ctx = ctx

        # Publisher socket — observations (streaming, topic="obs")
        pub = ctx.socket(zmq.PUB)
        pub.bind(f"tcp://*:{self.host_cfg.port_zmq_observations}")

        # Subscriber socket — action commands (topic="cmd")
        sub = ctx.socket(zmq.SUB)
        sub.setsockopt_string(zmq.SUBSCRIBE, "cmd")
        sub.bind(f"tcp://*:{self.host_cfg.port_zmq_cmd}")
        sub.RCVTIMEO = self.host_cfg.watchdog_timeout_ms

        print(f"✅ Host ready — obs port: {self.host_cfg.port_zmq_observations}, cmd port: {self.host_cfg.port_zmq_cmd}")
        print(f"   Running at {self.host_cfg.max_loop_freq_hz}Hz, auto-stop after {self.host_cfg.connection_time_s}s")
        print(f"   Waiting for client connections... (Ctrl+C to stop)")

        loop_dt = 1.0 / self.host_cfg.max_loop_freq_hz
        deadline = time.monotonic() + self.host_cfg.connection_time_s

        try:
            frame_count = 0
            while time.monotonic() < deadline:
                t0 = time.perf_counter()

                # ── Read sensors ────────────────────────────────────────
                obs = robot.get_observation()
                pub.send_multipart([b"obs", _serialize_obs(obs)])

                # ── Receive command (non-blocking, with timeout) ────────
                try:
                    _, cmd_data = sub.recv_multipart()
                    action = _deserialize_cmd(cmd_data)
                except zmq.Again:
                    action = {}

                if action:
                    robot.send_action(action)

                frame_count += 1
                if frame_count % 150 == 0:  # every ~5s at 30Hz
                    print(f"  Host running... frame {frame_count}")

                # ── Rate-limit ──────────────────────────────────────────
                elapsed = time.perf_counter() - t0
                if elapsed < loop_dt:
                    time.sleep(loop_dt - elapsed)

        except KeyboardInterrupt:
            logger.info("Interrupted, shutting down...")
        except Exception:
            logger.error("Host crashed:\n%s", traceback.format_exc())
        finally:
            robot.disconnect()
            pub.close()
            sub.close()
            ctx.term()
            logger.info("Host stopped.")
