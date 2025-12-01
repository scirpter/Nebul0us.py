# 2oh

Completely external, networked Nebulous.io bots.

## Quick Start

- Install deps: `python -m pip install -r requirements.txt`
- Tip: `orjson` is included for faster snapshots. If install fails on your platform, the code falls back to Python’s json.
- Run UI: `python src/main.py` (or `run.bat` on Windows)
- Train RL in simulator:
  - Windows: `train-sim.bat`
  - Any OS: `python src/cli.py train-sim --episodes 1000 --seed 0`
