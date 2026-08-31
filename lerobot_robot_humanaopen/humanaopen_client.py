"""ZMQ client robot — runs on the teleoperation laptop (dual-machine mode).

Receives observations from ``HumanaOpenHost`` over ZMQ and sends action
commands back.  Implements the full lerobot ``Robot`` contract so that
``make_robot_from_config`` can construct it directly: data collection
(``record_data.py``) and policy rollouts (``eval_data.py``) work in
dual-machine mode without any monkey-patching.

The feature surfaces (``observation_features`` / ``action_features``) mirror
``HumanaOpen`` exactly (same key names and order), so datasets recorded over
ZMQ are schema-identical to single-machine ones.

Transport (modeled on lerobot AlohaMini client):
- obs: PULL socket (host PUSH+SNDHWM=1), multipart
      [0] JSON state (`_image_encoding`, `_images`)
      [1..] alternating camera-name / JPEG-bytes frames
- cmd: PUSH socket, JSON single-frame (CONFLATE-safe)
"""

from __future__ import annotations

import json
import logging
import threading
import time
from functools import cached_property
from typing import Any

import numpy as np
import zmq

from lerobot.robots.robot import Robot

from .config_humanaopen import HumanaOpenClientConfig
from .humanaopen import _state_keys

logger = logging.getLogger(__name__)


def _parse_observation_multipart(
    message_parts: list[bytes], camera_names: set[str]
) -> tuple[dict[str, Any], float]:
    """Parse a multipart observation: JSON state head + cam/JPEG frame pairs.

    The JSON head (part 0) holds the float state plus the ``_images`` name
    list.  Frames follow as alternating [cam_name, jpeg_bytes] frames.

    Returns (obs, cam_ts) where cam_ts is the host-side capture timestamp
    (0.0 when the frame carries no camera data), used for latency measurement.
    """
    if not message_parts:
        return {}, 0.0

    try:
        state = json.loads(message_parts[0].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logger.error("Error decoding observation JSON: %s", e)
        return {}, 0.0

    cam_ts = float(state.get("_cam_ts", 0.0) or 0.0)
    obs: dict[str, Any] = {k: v for k, v in state.items() if not k.startswith("_")}

    if len(message_parts) > 1:
        import cv2

        if (len(message_parts) - 1) % 2 != 0:
            logger.warning("Invalid multipart observation: expected camera/JPEG pairs.")
        for index in range(1, len(message_parts) - 1, 2):
            try:
                cam_name = message_parts[index].decode("utf-8")
            except UnicodeDecodeError:
                logger.warning("Invalid camera name in multipart observation.")
                continue
            if cam_name not in camera_names:
                continue
            frame = cv2.imdecode(np.frombuffer(message_parts[index + 1], np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                logger.warning("cv2.imdecode returned None for camera %s.", cam_name)
                continue
            obs[cam_name] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return obs, cam_ts


def _serialize_cmd(action: dict[str, Any]) -> str:
    """Pack an action dict as a JSON string (host side uses json.loads)."""
    return json.dumps({k: float(v) for k, v in action.items() if isinstance(v, (int, float, np.floating))})


class HumanaOpenClient(Robot):
    """Teleop-side ZMQ robot implementing the lerobot Robot contract.

    ::

        config = HumanaOpenClientConfig(remote_ip="192.168.1.9")
        robot = HumanaOpenClient(config)
        robot.connect()

        while running:
            obs = robot.get_observation()
            action = my_teleop(obs)
            robot.send_action(action)

        robot.disconnect()
    """

    config_class = HumanaOpenClientConfig
    name = "humanaopen_client"

    def __init__(self, config: HumanaOpenClientConfig):
        super().__init__(config)
        self.config = config
        self._ctx: zmq.Context | None = None
        self._sub: zmq.Socket | None = None
        self._pub: zmq.Socket | None = None
        self._last_obs: dict[str, Any] = {}
        self._last_obs_time = 0.0
        # Image frames arrive at a lower rate than joint state (host divider);
        # cache them so fresh non-image obs frames can re-attach them.
        self._img_cache: dict[str, Any] = {}
        self._img_lock = threading.Lock()

    # ── Feature descriptors (mirror HumanaOpen so the dataset schema matches) ──
    # Cameras are a *schema* only: images arrive over ZMQ, so no local camera is
    # opened. ``config.cameras`` must list the cameras the Host actually streams.

    @property
    def _state_ft(self) -> dict[str, type]:
        return dict.fromkeys(_state_keys(), float)

    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        return {
            cam: (cfg.height, cfg.width, 3)
            for cam, cfg in self.config.cameras.items()
        }

    @property
    def cameras(self) -> dict:
        """Camera schema (name -> config). No camera is opened locally."""
        return self.config.cameras

    @cached_property
    def observation_features(self) -> dict[str, type | tuple]:
        return {**self._state_ft, **self._cameras_ft}

    @cached_property
    def action_features(self) -> dict[str, type]:
        return self._state_ft

    # ── Connection ────────────────────────────────────────────────────────

    def connect(self, calibrate: bool = True) -> None:
        self._ctx = zmq.Context()

        # Receive observations — PULL (host PUSH with SNDHWM=1 keeps only one
        # pending frame; we additionally drain below).
        self._sub = self._ctx.socket(zmq.PULL)
        self._sub.setsockopt(zmq.RCVHWM, 1)
        self._sub.connect(f"tcp://{self.config.remote_ip}:{self.config.port_zmq_observations}")

        # Send action commands — PUSH to host PULL (JSON single-frame).
        # CONFLATE=1 keeps only the newest command in-flight (same as lerobot
        # AlohaMini): a stale backlog must never make the operator's latest
        # action wait behind already-obsolete ones.
        self._pub = self._ctx.socket(zmq.PUSH)
        self._pub.setsockopt(zmq.CONFLATE, 1)
        self._pub.connect(f"tcp://{self.config.remote_ip}:{self.config.port_zmq_cmd}")

        # Verify the connection: wait until the host actually streams an
        # observation, otherwise fail fast instead of faking success.
        poller = zmq.Poller()
        poller.register(self._sub, zmq.POLLIN)
        if dict(poller.poll(self.config.connect_timeout_s * 1000)).get(self._sub) != zmq.POLLIN:
            raise RuntimeError(
                f"Timeout waiting for HumanaOpen Host at {self.config.remote_ip} to connect "
                f"(obs port {self.config.port_zmq_observations}). Is HumanaOpenHost running?"
            )

        logger.info("Client connected to %s", self.config.remote_ip)

    def disconnect(self) -> None:
        if self._sub:
            self._sub.close()
        if self._pub:
            self._pub.close()
        if self._ctx:
            self._ctx.term()
        logger.info("Client disconnected.")

    @property
    def is_connected(self) -> bool:
        return self._sub is not None and self._pub is not None

    @property
    def is_calibrated(self) -> bool:
        # Calibration is handled on the Host side (HumanaOpenHost homes/calibrates
        # the real motors). The ZMQ client is always considered "calibrated".
        return True

    def calibrate(self) -> None:
        # No-op: calibration runs where the hardware lives (the Host).
        pass

    def configure(self) -> None:
        # No-op: all motor configuration is applied by the Host.
        pass

    def get_observation(self) -> dict[str, Any]:
        """Return the latest observation from the robot host.

        Drains the PULL socket in non-blocking mode so only the freshest
        queued observation is kept (host PUSH keeps SNDHWM=1 anyway).
        Images arrive on a subset of frames (host image_fps_divider), so a
        frame carrying no image keeps the previously received one: joint/
        action state is always freshest, image stream stays at its own rate.
        """
        if not self.is_connected:
            raise RuntimeError("Client is not connected")

        camera_names = set(self._cameras_ft.keys())
        pending = self._sub.poll(0)
        now = time.time()
        while pending:
            try:
                message_parts = self._sub.recv_multipart(flags=zmq.NOBLOCK)
                obs, cam_ts = _parse_observation_multipart(message_parts, camera_names)
                # Persist image frames separately: they arrive less often than
                # joint state (host divider), so retain them across calls.
                for k, v in obs.items():
                    if isinstance(v, np.ndarray) and v.ndim == 3:
                        with self._img_lock:
                            self._img_cache[k] = v
                self._last_obs = obs
                self._last_obs_time = time.time()
                # Latency diagnostic: host-capture -> here, printed throttled.
                if cam_ts > 0:
                    lat_ms = int((time.time() - cam_ts) * 1000)
                    if lat_ms > 50 and time.time() - getattr(self, "_last_lat_print", 0.0) > 2.0:
                        self._last_lat_print = time.time()
                        print(f"  ⏱️ obs latency: {lat_ms}ms (host capture -> PC recv)")
            except zmq.Again:
                break
            pending = self._sub.poll(0)

        # Re-attach the most recent images to the freshest joint frame.
        with self._img_lock:
            if self._img_cache:
                self._last_obs.update(self._img_cache)

        return dict(self._last_obs)

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """Send an action command to the robot host (JSON single-frame)."""
        if not self.is_connected:
            raise RuntimeError("Client is not connected")
        self._pub.send_string(_serialize_cmd(action))
        return action

    @property
    def lift_axis(self):
        """Minimal lift accessor backed by the latest ZMQ observation.

        ``get_height_mm`` reads ``lift_axis.height_mm`` from the streamed obs;
        ``save_zero`` is a no-op because zero persistence is handled by the Host
        (which owns the physical motor and its calibration file).
        """
        _client = self

        class _LiftAxis:
            def get_height_mm(self) -> float:
                return _client._last_obs.get("lift_axis.height_mm", 0.0)

            def save_zero(self) -> None:
                # Zero is persisted on the Host side; nothing to do here.
                pass

        return _LiftAxis()

    def run_keyboard_teleop(self) -> None:
        """Simple keyboard teleoperation loop (WASD + IJKL for lift).

        A minimal demo — swap with your actual teleoperator.
        """
        try:
            import keyboard
        except ImportError:
            logger.error(
                "run_keyboard_teleop needs the 'keyboard' package:\n"
                "  pip install keyboard\n"
                "(Linux: run as root or use 'pynput' instead.)"
            )
            return

        self.connect()
        logger.info("Keyboard teleop started.  Keys: i/k fwd/bwd, j/l turn, u/d lift")

        try:
            while True:
                obs = self.get_observation()

                action: dict[str, Any] = {}
                # Arms: copy current position (hold still)
                for k, v in obs.items():
                    if k.endswith(".pos"):
                        action[k] = v

                # Base
                action["x.vel"] = 0.0
                action["theta.vel"] = 0.0
                if keyboard.is_pressed("i"):
                    action["x.vel"] = 0.2
                if keyboard.is_pressed("k"):
                    action["x.vel"] = -0.2
                if keyboard.is_pressed("j"):
                    action["theta.vel"] = 30.0
                if keyboard.is_pressed("l"):
                    action["theta.vel"] = -30.0

                # Lift
                if keyboard.is_pressed("u"):
                    action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0) + 2
                if keyboard.is_pressed("h"):
                    action["lift_axis.height_mm"] = obs.get("lift_axis.height_mm", 0) - 2

                self.send_action(action)
                time.sleep(0.02)

        except KeyboardInterrupt:
            pass
        finally:
            self.disconnect()
