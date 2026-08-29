"""ZMQ client robot — runs on the teleoperation laptop (dual-machine mode).

Receives observations from ``HumanaOpenHost`` over ZMQ and sends action
commands back.  Implements the full lerobot ``Robot`` contract so that
``make_robot_from_config`` can construct it directly: data collection
(``record_data.py``) and policy rollouts (``eval_data.py``) work in
dual-machine mode without any monkey-patching.

The feature surfaces (``observation_features`` / ``action_features``) mirror
``HumanaOpen`` exactly (same key names and order), so datasets recorded over
ZMQ are schema-identical to single-machine ones.
"""

from __future__ import annotations

import logging
import struct
import time
from functools import cached_property
from typing import Any

import numpy as np
import zmq

from lerobot.robots.robot import Robot

from .config_humanaopen import HumanaOpenClientConfig
from .humanaopen import _state_keys

logger = logging.getLogger(__name__)


def _deserialize_obs(data: bytes) -> dict[str, Any]:
    """Unpack observation dict (mirror of host's _serialize_obs)."""
    obs: dict[str, Any] = {}
    pos = 0
    magic, n_floats, n_images = struct.unpack_from("<III", data, pos)
    pos += 12
    if magic != 0x4F4253:
        raise ValueError(f"Bad magic: {magic:#x}")

    for _ in range(n_floats):
        klen = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        key = data[pos : pos + klen].decode()
        pos += klen
        val = struct.unpack_from("<f", data, pos)[0]
        pos += 4
        obs[key] = val

    for _ in range(n_images):
        klen = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        key = data[pos : pos + klen].decode()
        pos += klen
        H, W, C = struct.unpack_from("<III", data, pos)
        pos += 12
        npx = H * W * C
        obs[key] = np.frombuffer(data[pos : pos + npx], dtype=np.uint8).reshape(H, W, C)
        pos += npx

    return obs


def _serialize_cmd(action: dict[str, Any]) -> bytes:
    """Pack action dict (mirror of host's _deserialize_cmd)."""
    buf = bytearray()
    floats = {k: v for k, v in action.items() if isinstance(v, (int, float, np.floating))}
    buf.extend(struct.pack("<II", 0x4F4253, len(floats)))
    for k, v in floats.items():
        k_bytes = k.encode()
        buf.extend(struct.pack("<I", len(k_bytes)))
        buf.extend(k_bytes)
        buf.extend(struct.pack("<f", float(v)))
    return bytes(buf)


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

        # Subscribe to observations
        self._sub = self._ctx.socket(zmq.SUB)
        self._sub.setsockopt_string(zmq.SUBSCRIBE, "obs")
        self._sub.connect(f"tcp://{self.config.remote_ip}:{self.config.port_zmq_observations}")
        self._sub.RCVTIMEO = self.config.polling_timeout_ms

        # Publish action commands
        self._pub = self._ctx.socket(zmq.PUB)
        self._pub.connect(f"tcp://{self.config.remote_ip}:{self.config.port_zmq_cmd}")

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
        """Return the latest observation from the robot host."""
        if not self.is_connected:
            raise RuntimeError("Client is not connected")

        try:
            _, obs_data = self._sub.recv_multipart()
            self._last_obs = _deserialize_obs(obs_data)
            self._last_obs_time = time.time()
        except zmq.Again:
            # No new data — return cached
            pass

        return dict(self._last_obs)

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """Send an action command to the robot host."""
        if not self.is_connected:
            raise RuntimeError("Client is not connected")
        self._pub.send_multipart([b"cmd", _serialize_cmd(action)])
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
