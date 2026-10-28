#!/usr/bin/env -S uv run
"""Run a quest: `./run.py 2025 3` or `./run.py 4 2` (story 4, quest 2).
Start a quest from template.py: `./run.py new 2026 1`."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def quest_dir(event: int, quest: int) -> Path:
    if event >= 2024:
        return ROOT / f"{event}/{quest:02}"
    return ROOT / f"stories/{event}/{quest}"


def run(event: int, quest: int):
    day = quest_dir(event, quest)
    if not (day / "main.py").exists():
        sys.exit(f"no main.py in {day}")

    # cwd = quest dir, since main.py writes correct_part_N / images relative to it
    sys.exit(subprocess.call([sys.executable, "main.py"], cwd=day))


def new(event: int, quest: int):
    target = quest_dir(event, quest) / "main.py"
    if target.exists():
        sys.exit(f"{target} already exists")

    src = (ROOT / "template.py").read_text()
    src = re.sub(r"^EVENT = .*$", f"EVENT = {event}", src, count=1, flags=re.MULTILINE)
    src = re.sub(r"^QUEST = .*$", f"QUEST = {quest}", src, count=1, flags=re.MULTILINE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(src)
    print(f"created {target}")


def main():
    args = sys.argv[1:]
    cmd = new if args[:1] == ["new"] else run
    args = args[1:] if cmd is new else args
    if len(args) != 2:
        sys.exit(f"usage: {sys.argv[0]} [new] <event|story> <quest>")
    cmd(int(args[0]), int(args[1]))


if __name__ == "__main__":
    main()
