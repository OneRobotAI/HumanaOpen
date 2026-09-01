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

## [0.1.0] - 2026-09

Initial open-source release.
