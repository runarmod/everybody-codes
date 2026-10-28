#!/usr/bin/env -S uv run
"""Run a quest: `./run.py 2025 3` or `./run.py 4 2` (story 4, quest 2)."""

import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <event|story> <quest>")

    event, quest = int(sys.argv[1]), int(sys.argv[2])
    root = Path(__file__).parent
    day = (
        root / f"{event}/{quest:02}"
        if event >= 2024
        else root / f"stories/{event}/{quest}"
    )

    if not (day / "main.py").exists():
        sys.exit(f"no main.py in {day}")

    # cwd = quest dir, since main.py writes correct_part_N / images relative to it
    sys.exit(subprocess.call([sys.executable, "main.py"], cwd=day))


if __name__ == "__main__":
    main()
