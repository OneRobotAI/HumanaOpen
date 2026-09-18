"""LightNav-0 navigation adapter for HumanaOpen.

Bridges the LightNav-0 VLM navigation server (running on a GPU machine) to
HumanaOpen's differential-drive base over ZMQ. This is the ONLY piece of code
that touches HumanaOpen for navigation — no changes to HumanaOpenHost itself.

Flow per control tick:
  1. capture one frame from the chest camera (RGB, forward-facing)
  2. JPEG-encode + send to lightnav-serve over WebSocket ("next")
  3. server returns 10 SE(2) waypoints ([forward_m, lateral_m, yaw_rad])
  4. convert waypoints → (v, w) with the SAME controller as LightNav's own
     mujoco demo (waypoint_command): trajectory-tracking with gains, skipping
     near-zero waypoints (<0.35 m) that are quantizer noise, and zeroing
     linear speed when the target bearing exceeds 65 deg (turn-then-go)
  5. publish {"x.vel": v m/s, "theta.vel": w deg/s} over ZMQ PUSH :5555

Safety:
  - velocities clamped to --max-linear / --max-angular (rad/s → deg/s inside)
  - on "stop":true, empty waypoints, camera failure, or Ctrl+C: zero velocity
  - the base watchdog stops wheels if no command within watchdog_timeout_ms

Usage (run on the JETSON — the robot side):
    python3 examples/lightnav_navigation.py \
        --lightnav ws://192.168.1.12:8050 \
        --zmq-host 127.0.0.1 \
        --camera /dev/video0 \
        --instruction "walk forward slowly"

Env vars for proxies: websockets reads http(s)/socks proxy variables. If the
robot machine has a proxy for the internet, ensure LAN connects bypass it:
    NO_PROXY=192.168.1.12 python3 examples/lightnav_navigation.py ...
"""
import argparse
import asyncio
import base64
import json
import math
import signal
import time

import cv2
import numpy as np
import zmq
import websockets

# Control period (s). Keep equal to the Host cycle so velocities are consistent.
DT = 0.25

# ── Trajectory-tracking controller (ported from LightNav's mujoco demo) ─────
# Gains and thresholds below are the official ones — do not tune blindly.


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _dist_ok(point) -> bool:
    """True if the waypoint is far enough to be a real intent, not quantizer noise."""
    return len(point) >= 3 and all(
        math.isfinite(float(value)) for value in point[:3]
    ) and math.hypot(float(point[0]), float(point[1])) >= 0.35


def waypoint_command(
    waypoints,
    *,
    max_linear: float = 0.35,
    max_angular_rad: float = 1.2,
) -> tuple[float, float]:
    """Turn a body-frame VLN path into a conservative differential-drive command.

    Returns (linear m/s, angular deg/s). Uses the same control law as LightNav's
    mujoco_demo/vln_mujoco/control.py — a target-point tracker that:
      * picks the first waypoint at least 0.35 m away (noise gate)
      * angular = 1.8*bearing + 0.25*target_yaw  (rad/s), clamped
      * linear  = 0.75*distance*cos(bearing)     (m/s), 0 when bearing > 65 deg
    """
    if not waypoints:
        return 0.0, 0.0
    valid = [
        point
        for point in waypoints
        if len(point) >= 3 and all(math.isfinite(float(value)) for value in point[:3])
    ]
    if not valid:
        return 0.0, 0.0

    target = next((p for p in valid if _dist_ok(p)), valid[-1])
    forward, lateral, target_yaw = (float(value) for value in target[:3])
    distance = math.hypot(forward, lateral)
    bearing = math.atan2(lateral, forward)
    angular_rad = _clamp(
        1.8 * bearing + 0.25 * target_yaw,
        -max_angular_rad,
        max_angular_rad,
    )
    alignment = max(0.0, math.cos(bearing))
    linear = _clamp(0.75 * distance * alignment, 0.0, max_linear)
    if abs(bearing) > math.radians(65):
        linear = 0.0
    return linear, float(np.rad2deg(angular_rad))


def parse_args():
    p = argparse.ArgumentParser(description="LightNav-0 → HumanaOpen navigation bridge")
    p.add_argument("--lightnav", default="ws://192.168.1.12:8050",
                   help="LightNav-0 websocket server URL")
    p.add_argument("--zmq-host", default="127.0.0.1",
                   help="HumanaOpenHost IP (usually this Jetson itself)")
    p.add_argument("--zmq-port", type=int, default=5555,
                   help="HumanaOpenHost command port")
    p.add_argument("--camera", default="/dev/video0", help="chest (forward) camera device")
    p.add_argument("--instruction", default="walk forward slowly",
                   help="language instruction sent to the model")
    p.add_argument("--frame-width", type=int, default=640)
    p.add_argument("--frame-height", type=int, default=360)
    # Safety limits — clamp the controller output to these hardware-safe maxima.
    p.add_argument("--max-linear", type=float, default=0.35,
                   help="max linear velocity in m/s (official LightNav default)")
    p.add_argument("--max-angular", type=float, default=45.0,
                   help="max angular velocity in deg/s (~0.8 rad/s; official is 1.2)")
    return p.parse_args()


async def run(args):
    # ── ZMQ: publish velocity to HumanaOpenHost ──────────────────────────
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUSH)
    pub.connect(f"tcp://{args.zmq_host}:{args.zmq_port}")
    print(f"[nav] ZMQ → {args.zmq_host}:{args.zmq_port}")

    # ── Camera ───────────────────────────────────────────────────────────
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"[nav] ❌ cannot open camera {args.camera}")
        return
    print(f"[nav] camera {args.camera} ok")

    def send_vel(v: float, w_deg: float):
        action = {"x.vel": float(v), "theta.vel": float(w_deg)}
        pub.send_string(json.dumps(action))

    # ── WebSocket to lightnav-serve ───────────────────────────────────────
    print(f"[nav] connecting {args.lightnav} ...")
    async with websockets.connect(args.lightnav, ping_interval=None) as ws:
        await ws.send(json.dumps({"action": "login", "data": {"clientId": "humanaopen"}}))
        await ws.recv()
        await ws.send(json.dumps({"action": "reset", "data": {}}))
        await ws.recv()
        print("[nav] connected to LightNav server")

        # Stop the base cleanly on Ctrl+C instead of leaving it to the watchdog.
        loop = asyncio.get_running_loop()
        stopped = False

        def _stop(*_):
            nonlocal stopped
            stopped = True

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _stop)
            except NotImplementedError:
                pass  # non-UNIX platforms

        seq = 0
        while not stopped:
            ok, frame = cap.read()
            if not ok:
                print("[nav] ⚠️ frame read failed — zero vel")
                send_vel(0.0, 0.0)
                await asyncio.sleep(DT)
                continue

            frame = cv2.resize(frame, (args.frame_width, args.frame_height))
            ok_jpg, jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not ok_jpg:
                continue

            payload = {
                "action": "next",
                "data": {
                    "seq": seq,
                    "image": base64.b64encode(jpg.tobytes()).decode(),
                    "instruction": args.instruction,
                },
            }
            t0 = time.time()
            await ws.send(json.dumps(payload))
            raw = await ws.recv()
            resp = json.loads(raw)
            seq += 1

            data = resp.get("data", {})
            acts = data.get("actions", {}).get("actions")
            stop = bool(data.get("stop", False))

            if stop or not acts:
                print("[nav] 🛑 stop reached (or empty waypoints) — zero vel")
                send_vel(0.0, 0.0)
                await asyncio.sleep(DT)
                continue

            v, w_deg = waypoint_command(
                acts,
                max_linear=args.max_linear,
                max_angular_rad=math.radians(args.max_angular),
            )
            latency_ms = (time.time() - t0) * 1e3
            print(f"[nav] n_waypoints={len(acts)} first={acts[0]} → "
                  f"send=({v:+.3f} m/s,{w_deg:+.1f} d/s) ({latency_ms:.0f}ms)")
            send_vel(v, w_deg)
            await asyncio.sleep(DT - (time.time() - t0))  # keep loop at ~DT

        # Clean shutdown: zero the base.
        print("[nav] Ctrl+C — zeroing velocity, disconnecting")
        send_vel(0.0, 0.0)
        await asyncio.sleep(0.1)
        cap.release()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))