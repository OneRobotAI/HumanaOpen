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

try:
    import cv2
except ImportError:  # pragma: no cover - host without opencv falls back to raw frames
    cv2 = None  # type: ignore[assignment]

from .config_humanaopen import HumanaOpenConfig, HumanaOpenHostConfig
from .humanaopen import HumanaOpen

logger = logging.getLogger(__name__)


def _serialize_obs(obs: dict[str, Any], jpeg_quality: int = 85) -> bytes:
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
        [1 byte]  fmt              1=JPEG, 0=raw
        [4 bytes] payload_len      length of the encoded frame data
        [payload_len bytes] image data (JPEG bytes if fmt=1, else raw H*W*C uint8)
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
        if jpeg_quality > 0 and cv2 is not None:
            # cv2.imencode expects BGR; HumanaOpen observation frames are RGB.
            ok, enc = cv2.imencode(
                ".jpg",
                cv2.cvtColor(v, cv2.COLOR_RGB2BGR),
                [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality],
            )
            payload = enc.tobytes() if ok else b""
            fmt = 1  # JPEG
        else:
            payload = v.astype(np.uint8).tobytes()
            fmt = 0  # raw
        buf.extend(struct.pack("<BI", fmt, len(payload)))
        buf.extend(payload)

    return bytes(buf)


def _deserialize_cmd(data: bytes) -> dict[str, Any]:
    """Unpack an action dict from bytes (mirror of above)."""
    action: dict[str, Any] = {}
    pos = 0
    # Client _serialize_cmd uses "<II" (magic, n_floats) — not "<III"
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

        # Shared image cache + thread-safe lock
        # Images are captured continuously by a dedicated thread; the main loop only
        # reads the latest cache, without blocking the action response
        import threading
        cam_lock = threading.Lock()
        cam_cache: dict[str, Any] = {}
        stop_cam = threading.Event()

        def _camera_thread():
            """Continuously capture images into the cache in the background.

            Each camera is read independently so that a single failing camera
            cannot blank the others. On a transient read error the previous
            good frame is kept (no clear()), so the obs stream keeps images.
            """
            cam_interval = 1.0 / self.host_cfg.image_fps if self.host_cfg.image_fps > 0 else 0.0
            while not stop_cam.is_set():
                frames: dict[str, Any] = {}
                for cam_key, cam in robot.cameras.items():
                    try:
                        frame = cam.async_read()
                        if frame is not None and getattr(frame, "ndim", 0) == 3:
                            frames[cam_key] = frame
                    except Exception as e:
                        # Log the failure once per camera; keep whatever the
                        # camera delivered last time (cache is not cleared).
                        logger.warning("camera '%s' read failed: %s", cam_key, e)
                if frames:
                    with cam_lock:
                        cam_cache.update(frames)
                elif not cam_cache:
                    logger.warning("no camera delivered any frame yet")
                if cam_interval > 0:
                    time.sleep(cam_interval)
                else:
                    time.sleep(0.05)

        cam_thread = threading.Thread(target=_camera_thread, daemon=True)
        cam_thread.start()

        try:
            frame_count = 0
            while time.monotonic() < deadline:
                t0 = time.perf_counter()

                # High frequency: read joint state (no cameras, millisecond-level)
                try:
                    obs = robot.get_observation_no_cameras()
                except Exception:
                    time.sleep(loop_dt)
                    continue

                # Attach the latest image cache (non-blocking; the background thread is already capturing)
                with cam_lock:
                    obs.update(cam_cache)

                pub.send_multipart([b"obs", _serialize_obs(obs, self.host_cfg.jpeg_quality)])

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
            stop_cam.set()
            cam_thread.join(timeout=1.0)
            robot.disconnect()
            pub.close()
            sub.close()
            ctx.term()
            logger.info("Host stopped.")
