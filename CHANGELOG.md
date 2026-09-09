# Changelog

All notable changes to **HumanaOpen** are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/); this project is
pre-1.0 so breaking changes may occur until a stable release.

## [Unreleased]

### Added
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

## [0.1.0] - 2026-09

Initial open-source release.
