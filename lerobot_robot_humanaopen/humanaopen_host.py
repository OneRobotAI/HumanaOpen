"""ZMQ host — runs on the robot side (Jetson / Raspberry Pi).

Connects to the real hardware and forwards observations / receives
action commands from a remote ``HumanaOpenClient`` over ZMQ.

Transport (modeled on lerobot AlohaMini host):
- cmd: PULL socket, JSON single-frame, CONFLATE-safe
- obs: PUSH socket with SNDHWM=1, multipart message:
      [0] JSON state (floats) with `_image_encoding` + `_images` metadata
      [1..] alternating camera-name / JPEG-bytes frames
  Sending is NOBLOCK: if the client is slower, the previous pending
  observation is dropped so the wire always carries the newest frame.
"""

from __future__ import annotations

import json
import logging
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


def _jsonable(value: Any) -> Any:
    """Convert numpy scalars to JSON-native values without touching plain values."""
    if hasattr(value, "item"):
        try:
            return value.item()
        except ValueError:
            pass
    return value


def build_observation_multipart(
    obs: dict[str, Any], camera_keys, jpeg_quality: int = 70
) -> list[bytes]:
    """Encode state as JSON and camera images as JPEG binary multipart frames.

    Layout: [json(state), cam_key, jpeg_bytes, cam_key, jpeg_bytes, ...]
    The JSON head carries ``_image_encoding`` and ``_images`` so the client
    knows the number/names of images that follow (multipart-safe).

    Images are normally pre-encoded by the camera thread (``bytes`` values in
    ``obs``); an ``ndarray`` fallback encodes synchronously here.
    """
    state_observation = {
        _jsonable(key): _jsonable(value) for key, value in obs.items() if key not in camera_keys
    }
    state_observation["_image_encoding"] = "jpeg"

    parts: list[bytes] = [json.dumps(state_observation).encode("utf-8")]
    image_names: list[str] = []
    for cam_key in camera_keys:
        frame = obs.get(cam_key)
        if frame is None:
            continue
        if isinstance(frame, bytes):
            # Pre-encoded by the camera thread (async path) — use as-is.
            jpeg_bytes = frame
        elif isinstance(frame, np.ndarray) and frame.ndim == 3:
            # Fallback: encode synchronously here.
            if cv2 is None:
                logger.warning("cv2 unavailable — skipping camera %s", cam_key)
                continue
            # observation frames are RGB; cv2.imencode expects BGR.
            ret, buffer = cv2.imencode(
                ".jpg",
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality],
            )
            if not ret:
                logger.warning("Failed to JPEG encode camera frame %s.", cam_key)
                continue
            jpeg_bytes = buffer.tobytes()
        else:
            continue
        image_names.append(cam_key)
        parts.extend([cam_key.encode("utf-8"), jpeg_bytes])

    state_observation["_images"] = image_names
    parts[0] = json.dumps(state_observation).encode("utf-8")
    return parts


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

        # Observation socket — PUSH, single pending frame: if the client is slow
        # the oldest observation is dropped so the wire always carries the
        # newest. (CONFLATE would be ideal but is unsafe with multipart frames.)
        pub = ctx.socket(zmq.PUSH)
        pub.setsockopt(zmq.SNDHWM, 1)
        pub.bind(f"tcp://*:{self.host_cfg.port_zmq_observations}")

        # Command socket — PULL, JSON single-frame (CONFLATE-safe)
        sub = ctx.socket(zmq.PULL)
        sub.setsockopt(zmq.CONFLATE, 1)
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
        # Wall-clock timestamp of the newest frame the camera thread produced;
        # the main loop stamps it into the obs head so the client can measure
        # capture->send->recv latency and attribute the image delay.
        cam_capture_ts: float = 0.0

        def _camera_thread():
            """Continuously capture + JPEG-encode images in the background.

            Each camera is read independently so that a single failing camera
            cannot blank the others. On a transient read error the previous
            good frame is kept (no clear()), so the obs stream keeps images.
            Capture rate = main loop Hz / image_fps_divider (default 30/3 = 10Hz),
            matching how often the main loop attaches the cache to obs.

            Frames are JPEG-encoded HERE, not in the 30Hz control loop: imencode
            is expensive (10-20ms per 640x480 frame), and doing it synchronously
            starved the image pipeline on low-power hosts, making streamed views
            lag seconds behind reality.
            """
            nonlocal cam_capture_ts
            cam_interval = loop_dt * self.host_cfg.image_fps_divider
            while not stop_cam.is_set():
                frames: dict[str, Any] = {}
                for cam_key, cam in robot.cameras.items():
                    try:
                        frame = cam.async_read(timeout_ms=max(200, int(cam_interval * 1000)))
                        if frame is not None and getattr(frame, "ndim", 0) == 3:
                            frames[cam_key] = frame
                    except Exception as e:
                        # Log the failure once per camera; keep whatever the
                        # camera delivered last time (cache is not cleared).
                        logger.warning("camera '%s' read failed: %s", cam_key, e)
                if frames:
                    encoded: dict[str, bytes] = {}
                    if cv2 is not None:
                        for cam_key, frame in frames.items():
                            try:
                                ret, buffer = cv2.imencode(
                                    ".jpg",
                                    cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                                    [int(cv2.IMWRITE_JPEG_QUALITY), self.host_cfg.jpeg_quality],
                                )
                                if ret:
                                    encoded[cam_key] = buffer.tobytes()
                            except Exception as e:
                                logger.warning("camera '%s' encode failed: %s", cam_key, e)
                    with cam_lock:
                        if encoded:
                            cam_cache.update(encoded)
                            cam_capture_ts = time.time()
                        elif not cam_cache:
                            logger.warning("no camera delivered any frame yet")
                time.sleep(cam_interval)

        cam_thread = threading.Thread(target=_camera_thread, daemon=True)
        cam_thread.start()

        try:
            frame_count = 0
            while time.monotonic() < deadline:
                t0 = time.perf_counter()

                # ── Receive + execute command FIRST (like lerobot LeKiwi/AlohaMini
                # hosts): the action channel must NOT wait behind observation/image
                # work. Non-blocking + CONFLATE keeps only the newest command, so a
                # slow obs/build below never delays the operator's action.
                try:
                    cmd_str = sub.recv_string(zmq.NOBLOCK)
                    action = dict(json.loads(cmd_str))
                except zmq.Again:
                    action = {}
                except (ValueError, TypeError) as e:
                    logger.warning("Bad command message: %s", e)
                    action = {}

                if action:
                    robot.send_action(action)

                # High frequency: read joint state (no cameras, millisecond-level)
                try:
                    obs = robot.get_observation_no_cameras()
                except Exception:
                    time.sleep(loop_dt)
                    continue

                # Attach the latest image cache only every few control frames:
                # images are large (even JPEG ~30KB each), and sending them on
                # every frame saturates the link and delays the action channel.
                # Image frames therefore run at max_loop_freq_hz/image_fps_divider.
                if frame_count % self.host_cfg.image_fps_divider == 0:
                    with cam_lock:
                        obs.update(cam_cache)
                    # Stamps for client-side latency measurement (capture -> recv).
                    obs["_cam_ts"] = cam_capture_ts if cam_capture_ts else time.time()

                # Send the newest observation; drop instead of blocking if the
                # client is slower than us (SNDHWM=1 keeps only one pending).
                parts = build_observation_multipart(obs, robot.cameras.keys(), self.host_cfg.jpeg_quality)
                try:
                    pub.send_multipart(parts, flags=zmq.NOBLOCK)
                except zmq.Again:
                    logger.info("Dropping observation — no client connected.")

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
            # Persist the lift position on ANY host exit (Ctrl+C / timeout / crash):
            # the PC-side save_zero is a no-op in dual-machine mode, so the Host is
            # the only place that can remember the last lift height — otherwise
            # every restart re-homes to zero.
            try:
                robot.lift_axis.save_zero()
            except Exception:
                pass
            robot.disconnect()
            pub.close()
            sub.close()
            ctx.term()
            logger.info("Host stopped.")
