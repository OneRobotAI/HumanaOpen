# Changelog

All notable changes to **HumanaOpen** are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/); this project is
pre-1.0 so breaking changes may occur until a stable release.

## [Unreleased]

### Added
- **Arm/head tremor suppression (leader + follower jitter lock)**:
  - `leader.py`: speed-adaptive EMA (`alpha_min`, `alpha_speed_ref`) replaces
    the fixed 0.35 alpha — the arm freezes at rest and stays responsive during
    fast moves.
  - `leader.py`: output deadband (`deadband=0.1` ≈ 2 encoder ticks): the
    emitted action holds its last value until the smoothed signal actually
    moves, so stationary encoder self-noise (±0.1) never reaches the follower.
    Gripper gets the same deadband (no EMA).
  - `humanaopen.py`: follower write deadband (`goal_deadband=0.1`): targets
    whose delta from the last written value is below the band are skipped
    (existing wheel-dedup pattern), so a still arm issues zero servo writes —
    no re-planning, no bus traffic, no micro-motion.
  - New tunables in `leader.py` / `config_humanaopen.py`:
    `alpha_min=0.15`, `alpha_speed_ref=1.0`, `deadband=0.1`,
    `goal_deadband=0.1` — all optional, values above are the backward-
    compatible defaults.
  - Mock-verified: `tests/test_leader_jitter.py` (run without hardware) proves
    stationary output stays bit-identical under ±0.1 noise over 2000 frames,
    fast steps are tracked in ~0.3s, and slow ramps never drift.
- **`teleop_leader_to_follower.py`: command-line bus-topology switch**
  (`--robot.port1/port2/port3`). `--robot.port3 None` (default) keeps the
  2-bus layout (wheels+lift on port2); passing a device name (e.g.
  `--robot.port3 /dev/ttyACM2`) moves lift+wheels to a dedicated third bus —
  right arm gets an uncontended bus2 (cleaner 60Hz frame timing, less
  move-start latency). Same `None` string parsing as `record_data.py` /
  `eval_data.py`.
- **`humanaopen_host_launcher.py`: command-line Host startup** for
  dual-machine (ZMQ) mode. Same flag style as the other scripts:
  `--robot.port1/port2/port3` (`None` = 2-bus, any device name = 3-bus),
  `--no-cameras` (pure control, no video), and per-camera overrides
  (`--head-camera`, `--left-wrist-camera`, `--right-wrist-camera`,
  `--chest-camera`). Covers all four 2-bus/3-bus × cameras on/off
  combinations without editing a `python3 -c` one-liner. All four READMEs
  updated to recommend it (inline form kept as equivalent alternative).
- Dual-machine (ZMQ) data collection and inference examples in all four READMEs.
- Unified `--display=rerun|foxglove` display flag across teleop / record / eval
  (omit `--display` for headless; `--display=foxglove` auto-opens the web viewer).
- `--enable-base` and `--enable-lift` switches for policy inference
  (`--enable-lift` holds the lift at its current height by default).
- Base auto-stop on inference exit: ZMQ CONFLATE-safe stop ordering + a Host
  watchdog that zeroes the wheels after `watchdog_timeout_ms` with no command.
- Foxglove visualization backend for teleop / record / eval.
- `hardware/` directory: BOM, assembly, CAD (Fusion 360 + STEP), STL, URDF,
  electronics wiring.
- CAD STEP exports (36 files): `hardware/cad/step/HumanaOpen_step/` (16 parts:
  chassis, torso, head, lift) and `hardware/cad/step/Open-arms-mini_step/`
  (20 parts: J1-J8 arm joints, holders, trigger, WaveShare plate).
- 3D-print STL files (38 files): `hardware/stl/HumanaOpen_stl/` (17 parts) and
  `hardware/stl/Open-arms-mini-stl/` (21 parts), in mm, revision-named.
- Complete robot URDF: `hardware/urdf/humanaopen.urdf` — full kinematic tree
  (base wheels, lift, torso, head pan/tilt, 2× 7-DOF arm + gripper) with 26
  STL meshes in `hardware/urdf/meshes/`, collision boxes, and estimated
  inertial. Joint names mirror `lerobot_robot_humanaopen/humanaopen.py`.
- **Language-driven navigation** (`examples/lightnav_navigation.py`): LightNav-0
  vision-language-action model on a GPU PC drives the base through a lightweight
  ZMQ adapter — no LightNav install / ROS / lidar / map on the robot. Uses the
  official `waypoint_command` control law + RVQ-quantization deadbands
  (fail-safe zero on stop/disconnect). Real-robot verified: straight walk
  0.113 m/s, left-turn arc, exact idle zero. English instructions only.
  Docs: `docs/navigation/lightnav_integration.md`.

### Fixed
- Teleop native Rerun (`--display`) now logs on the main control thread to avoid
  gRPC backpressure / frozen viewer.
- `--display` no longer prefix-matched to `--display-foxglove` (added explicit
  `--display` argument).
- Lift would appear to "not move": `Acceleration` (SRAM) resets to 0 on every
  power cycle, capping commanded speed at ~10-20% of target; lift
  `configure()` now writes `Acceleration=254` (fastest ramp) on every connect.
- Lift would silently run 50x slower than commanded when the servo `Phase`
  register BIT2 was 1 (1 step/s/raw) while all speed constants assume BIT2=0
  (50 step/s/raw). `configure()` now reads `Phase` and switches BIT2 to 0
  (EPROM write, survives reboot) automatically — no manual
  `examples/switch_phase_bit2.py` needed after firmware re-flash.
- Stale lift zero file after a servo replacement: `restore_zero()` now checks
  `Model_Number` (different-motor detection) and a triangle-consistency check
  (`(cur - abs_tick_at_home) mod rev == extended_ticks mod rev`) that catches
  same-model swaps even when the raw encoder tick coincidentally matches.
  A stale zero file now invalidates automatically → re-home, no manual
  `rm lift_zero.json` needed.
- Dual-machine teleop latency overhaul: host control loop 30→60Hz
  (`max_loop_freq_hz=60`) and teleop `--fps` option (halves the 2-frame
  pipeline delay ~66ms→~33ms); host drains the command queue each frame and
  applies only the newest so stale commands never replay after a stall; teleop
  reads both leader arms concurrently (two serial buses in parallel); serial
  retries removed from the hot path (a flaky sync_read no longer stalls the
  whole 30/60Hz loop up to 140ms); client PUSH `SNDTIMEO=10ms` + send
  fault-tolerance so a stalled peer never freezes the loop; lift bus-write
  failures no longer crash the host. Latency display rewritten as a **skew-free
  command→obs RTT**: every command carries the client's `perf_counter_ns`, the
  host echoes it in the next observation, and the client computes RTT on its
  own monotonic clock — immune to cross-machine wall-clock skew (the old
  `net:` reading was meaningless, often negative).

## [0.1.0] - 2026-09

Initial open-source release.
