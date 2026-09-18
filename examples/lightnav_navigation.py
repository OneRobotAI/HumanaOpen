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

# ── Trajectory-tracking controller ──────────────────────────────────────────
# Based on LightNav's official mujoco demo control law (mujoco_demo/vln_mujoco/
# control.py): angular = 1.8*bearing + 0.25*target_yaw, linear = 0.75*distance*
# cos(bearing), zero linear when |bearing| > 65 deg. The official thresholds are
# tuned for the demo (0.35 m min distance). On HumanaOpen the RVQ action
# tokenizer quantizes waypoints to coarse levels (yaw sits at exactly ±0.314 rad
# == ±π/10 for "no turn", and forward steps are ~0.15 m), so the noise gate must
# be tighter and both bearing and yaw need deadbands. Tune via CLI if needed.


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _valid_point(point) -> bool:
    return len(point) >= 3 and all(
        math.isfinite(float(value)) for value in point[:3]
    )


# Waypoint below this (forward,lateral) distance is pure quantizer noise — gone.
# The official demo uses 0.35 m; HumanaOpen real robot steps are ~0.15 m.
MIN_TARGET_DIST = 0.08
# Bearing smaller than this contributes nothing (quantizer noise on lateral).
# Official law uses raw bearing; here lateral steps are ~0.02 m — too noisy.
BEARING_DEADBAND_RAD = math.radians(8.0)
# Yaw smaller than this is the "no-turn" quantizer level (±π/10). Official law
# keeps 0.25*target_yaw; here yaw=±0.314 would sort as a real turn — it isn't.
YAW_DEADBAND_RAD = math.radians(30.0)


def waypoint_command(
    waypoints,
    *,
    max_linear: float = 0.35,
    max_angular_rad: float = 1.2,
) -> tuple[float, float]:
    """Turn a body-frame VLN path into a conservative differential-drive command.

    Returns (linear m/s, angular deg/s). Same control law as LightNav's official
    mujoco demo (target-point tracker) but with deadbands for the RVQ quantizer
    levels observed on the real robot:
      * a waypoint under MIN_TARGET_DIST is noise; if ALL are noise → (0, 0)
      * angular = 1.8*bearing + 0.25*target_yaw (rad/s), bearing/yaw deadbanded
      * linear  = 0.75*distance*cos(bearing), 0 when |bearing| > 65 deg
    """
    if not waypoints:
        return 0.0, 0.0
    first = waypoints[0]
    if not _valid_point(first):
        return 0.0, 0.0

    # The model's waypoint[0] is the action for the CURRENT frame; later
    # waypoints are its predicted future path. Acting on a later waypoint while
    # [0] is near-zero caused full-rate spins on real robot (a noisy far point
    # with huge bearing). Gate on waypoint[0] alone: near-zero → stand still.
    if math.hypot(float(first[0]), float(first[1])) < MIN_TARGET_DIST:
        return 0.0, 0.0

    target = first

    forward, lateral, target_yaw = (float(value) for value in target[:3])
    distance = math.hypot(forward, lateral)
    bearing = math.atan2(lateral, forward)

    # Deadband the noisy channels (quantizer levels) before applying gains.
    if abs(bearing) < BEARING_DEADBAND_RAD:
        bearing = 0.0
    if abs(target_yaw) < YAW_DEADBAND_RAD:
        target_yaw = 0.0

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