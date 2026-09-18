"""LightNav-0 navigation adapter for HumanaOpen.

Bridges the LightNav-0 VLM navigation server (running on a GPU machine) to
HumanaOpen's differential-drive base over ZMQ. This is the ONLY piece of code
that touches HumanaOpen for navigation — no changes to HumanaOpenHost itself.

Flow per control tick:
  1. capture one frame from the chest camera (RGB, forward-facing)
  2. JPEG-encode + send to lightnav-serve over WebSocket ("next")
  3. server returns 10 SE(2) waypoints; take the first ([forward_m, lat, yaw_rad])
  4. v = forward_m/dt, w = rad2deg(yaw_rad/dt)   (HumanaOpen theta.vel is deg/s)
  5. publish {"x.vel": v, "theta.vel": w} over ZMQ PUSH to HumanaOpenHost:5555

Safety: on "stop":true (goal reached) or any error we publish zero velocity.
Manual control remains available on the Host (the base has a watchdog that
stops the wheels if no new command arrives within watchdog_timeout_ms).

Usage (run on the JETSON — the robot side):
    python3 examples/lightnav_navigation.py \
        --lightnav ws://192.168.1.12:8050 \
        --zmq-host 127.0.0.1 \
        --camera /dev/video6 \
        --instruction "walk forward slowly"

Env vars for proxies: websockets reads http(s)/socks proxy variables. If the
robot machine has a proxy for the internet, ensure LAN connects bypass it:
    NO_PROXY=192.168.1.12 python3 examples/lightnav_navigation.py ...
"""
import argparse
import asyncio
import base64
import json
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
    p.add_argument("--camera", default="/dev/video6", help="chest (forward) camera device")
    p.add_argument("--instruction", default="walk forward slowly",
                   help="language instruction sent to the model")
    p.add_argument("--frame-width", type=int, default=640)
    p.add_argument("--frame-height", type=int, default=360)
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

        seq = 0
        while True:
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

            # First waypoint [forward_m, lateral_m, yaw_rad]
            fwd, _lat, yaw = acts[0][0], acts[0][1], acts[0][2]
            v = fwd / DT
            w_deg = float(np.rad2deg(yaw / DT))
            latency_ms = (time.time() - t0) * 1e3
            print(f"[nav] fwd={fwd:+.3f}m yaw={yaw:+.3f}rad → "
                  f"x.vel={v:+.3f} theta.vel={w_deg:+.1f} ({latency_ms:.0f}ms)")
            send_vel(v, w_deg)
            await asyncio.sleep(DT - (time.time() - t0))  # keep loop at ~DT


if __name__ == "__main__":
    asyncio.run(run(parse_args()))