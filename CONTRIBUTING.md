# Contributing

Thanks for considering contributing to **HumanaOpen**! This is an open-source
semi-humanoid robot built on [LeRobot](https://github.com/huggingface/lerobot)
and [open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini).

## Code of conduct

Be respectful and constructive. This project is maintained free in spare time.

## How to contribute

1. **Report a bug** — open an issue with your setup, commands, and logs.
2. **Suggest a feature** — open an issue describing the use case.
3. **Submit code/design** — open a pull request (see below).

## Development workflow

- Branch from `main`; keep changes focused and atomic.
- Keep the four-language READMEs (`README.md`, `README_zh.md`, `README_fr.md`,
  `README_ko.md`) in sync when you change user-facing behaviour.
- Preserve comment styles: no external-project attributions, self-documenting
  comments that explain *why*.
- For hardware changes, re-export the STL/STEP from the Fusion 360 source and
  update the `hardware/` docs + BOM.

## One-time setup

```bash
git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen
pip install -e . --no-deps
```

## Running the pipeline

See the README and `docs/manual_*.md` for teleoperation, data collection,
training, and inference.
