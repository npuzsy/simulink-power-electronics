#!/usr/bin/env python3
"""Validate repository-local references declared by the skill entry point."""

from __future__ import annotations

import re
import sys
from pathlib import Path


PATH_PATTERN = re.compile(r"`((?:references|scripts|assets|subskills)/[^`]+)`")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_path = root / "SKILL.md"

    if not skill_path.exists():
        print(f"missing {skill_path}", file=sys.stderr)
        return 1

    text = skill_path.read_text(encoding="utf-8")
    referenced_paths = sorted(set(PATH_PATTERN.findall(text)))
    for skill_md in sorted((root / "subskills").glob("*/SKILL.md")):
        referenced_paths.append(skill_md.relative_to(root).as_posix())
    referenced_paths = sorted(set(referenced_paths))
    missing = []
    for path in referenced_paths:
        if any(char in path for char in "*?["):
            if not list(root.glob(path)):
                missing.append(path)
            continue
        if not (root / path).exists():
            missing.append(path)

    for path in referenced_paths:
        status = "ok" if path not in missing else "missing"
        print(f"{status}: {path}")

    if missing:
        print("\nMissing paths declared in SKILL.md:", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
