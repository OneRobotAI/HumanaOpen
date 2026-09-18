"""LightNav-0 navigation adapter for HumanaOpen.

Bridges the LightNav-0 VLM navigation server (running on a GPU machine) to
HumanaOpen's differential-drive base over ZMQ. This is the ONLY piece of code
that touches HumanaOpen for navigation — no changes to HumanaOpenHost itself.

Flow per control tick:
  1. capture one frame from the chest camera (RGB, forward-facing)
  2. JPEG-encode + send to lightnav-serve over WebSocket ("next")
  3. server returns 10 SE(2) waypoints; take the first ([forward_m, lat, yaw_rad])
  4. v = forward_m/dt, w = rad2deg(yaw_rad/dt)   (HumanaOpen theta.vel is deg/s)
  5. EMA-smooth + clamp + deadband (the RVQ action tokenizer is quantized, e.g.
     yaw often sits at exactly ±0.314rad; direct conversion produces violent
     ±72deg/s spins that are noise, not intent)
  6. publish {"x.vel": v, "theta.vel": w} over ZMQ PUSH to HumanaOpenHost:5555

Safety:
  - velocities are clamped to --max-vel / --max-omega
  - on "stop":true, empty waypoints, camera failure, or Ctrl+C we publish 0
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
import signal
import time

import cv2
import numpy as np
import zmq
import websockets

# Control period (s). Keep equal to the Host cycle so velocities are consistent.
DT = 0.25


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
    # Safety limits — clamp model output to these hardware-safe maxima.
    p.add_argument("--max-vel", type=float, default=0.35,
                   help="max linear velocity in m/s (clamped)")
    p.add_argument("--max-omega", type=float, default=25.0,
                   help="max angular velocity in deg/s (clamped)")
    # EMA smoothing factor. Alternating quantized noise (±0.314 rad yaw) averages
    # to ~0 while sustained intent (e.g. 0.15 m forward for many frames) survives.
    p.add_argument("--ema-alpha", type=float, default=0.35)
    # Deadbands: below these the output is treated as pure noise.
    p.add_argument("--fwd-deadband", type=float, default=0.03, help="m")
    p.add_argument("--yaw-deadband", type=float, default=6.0, help="deg/s")
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

    # ── Smoothing state (EMA) ────────────────────────────────────────────
    ema_v = 0.0
    ema_w = 0.0

    async def publish_smooth(raw_v: float, raw_w_deg: float) -> None:
        """EMA-smooth raw velocities, deadband the noise, clamp, and publish."""
        nonlocal ema_v, ema_w
        a = args.ema_alpha
        ema_v = a * raw_v + (1.0 - a) * ema_v
        ema_w = a * raw_w_deg + (1.0 - a) * ema_w

        # Deadband: pure quantizer noise sits right at ±0.314 rad/DT = ±72 deg/s.
        # If EMA shrinks it below the deadband it was alternating noise → zero it.
        if abs(ema_v) < args.fwd_deadband:
            ema_v = 0.0
        if abs(ema_w) < args.yaw_deadband:
            ema_w = 0.0

        # Clamp to hardware-safe maxima.
        v = float(np.clip(ema_v, -args.max_vel, args.max_vel))
        w = float(np.clip(ema_w, -args.max_omega, args.max_omega))
        send_vel(v, w)
        print(f"[nav] raw=({raw_v:+.3f} m/s,{raw_w_deg:+.1f} d/s) → "
              f"send=({v:+.3f} m/s,{w:+.1f} d/s)")

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
                ema_v = ema_w = 0.0
                send_vel(0.0, 0.0)
                await asyncio.sleep(DT)
                continue

            # First waypoint [forward_m, lateral_m, yaw_rad]
            fwd, _lat, yaw = acts[0][0], acts[0][1], acts[0][2]
            raw_v = fwd / DT
            raw_w = float(np.rad2deg(yaw / DT))
            await publish_smooth(raw_v, raw_w)
            await asyncio.sleep(DT - (time.time() - t0))  # keep loop at ~DT

        # Clean shutdown: zero the base.
        print("[nav] Ctrl+C — zeroing velocity, disconnecting")
        send_vel(0.0, 0.0)
        await asyncio.sleep(0.1)
        cap.release()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))