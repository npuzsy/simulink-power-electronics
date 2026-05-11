#!/usr/bin/env python3
"""Validate repository-local references declared by root and subskill files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


PATH_PATTERN = re.compile(r"`((?:references|scripts|assets|subskills)/[^`]+)`")


def display(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve_reference(root: Path, declaring_file: Path, raw_path: str) -> Path:
    """Resolve a backticked repository path from the file that declared it."""
    if declaring_file == root / "SKILL.md":
        return root / raw_path

    if declaring_file.match("subskills/*/SKILL.md") and raw_path.startswith(
        ("references/", "scripts/")
    ):
        return declaring_file.parent / raw_path

    return root / raw_path


def glob_matches(root: Path, declaring_file: Path, raw_path: str, resolved_path: Path):
    if declaring_file.match("subskills/*/SKILL.md") and raw_path.startswith(
        ("references/", "scripts/")
    ):
        return declaring_file.parent.glob(raw_path)
    return root.glob(raw_path)


def iter_declared_paths(root: Path):
    skill_files = [root / "SKILL.md"]
    skill_files.extend(sorted((root / "subskills").glob("*/SKILL.md")))

    for skill_file in skill_files:
        if not skill_file.exists():
            yield skill_file, "", skill_file
            continue

        text = skill_file.read_text(encoding="utf-8")
        for raw_path in sorted(set(PATH_PATTERN.findall(text))):
            yield skill_file, raw_path, resolve_reference(root, skill_file, raw_path)

    for skill_file in sorted((root / "subskills").glob("*/SKILL.md")):
        yield root / "SKILL.md", skill_file.relative_to(root).as_posix(), skill_file


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_path = root / "SKILL.md"

    if not skill_path.exists():
        print(f"missing {skill_path}", file=sys.stderr)
        return 1

    missing = []

    checks = list(iter_declared_paths(root))
    seen = set()
    unique_checks = []
    for declaring_file, raw_path, resolved_path in checks:
        key = (declaring_file, raw_path, resolved_path)
        if key not in seen:
            seen.add(key)
            unique_checks.append((declaring_file, raw_path, resolved_path))

    for declaring_file, raw_path, resolved_path in unique_checks:
        if not raw_path:
            missing.append((declaring_file, raw_path, resolved_path))
            continue
        if any(char in raw_path for char in "*?["):
            if not list(glob_matches(root, declaring_file, raw_path, resolved_path)):
                missing.append((declaring_file, raw_path, resolved_path))
            continue
        if not resolved_path.exists():
            missing.append((declaring_file, raw_path, resolved_path))

    missing_set = set(missing)
    for declaring_file, raw_path, resolved_path in unique_checks:
        status = "missing" if (declaring_file, raw_path, resolved_path) in missing_set else "ok"
        source = display(declaring_file, root)
        target = display(resolved_path, root)
        print(f"{status}: {source} -> {raw_path or target}")

    if missing:
        print("\nMissing paths declared in skill files:", file=sys.stderr)
        for declaring_file, raw_path, resolved_path in missing:
            source = display(declaring_file, root)
            target = display(resolved_path, root)
            print(f"- {source}: {raw_path or target} -> {target}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
