#!/usr/bin/env python3
"""Validate skill structure and repository-local references."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path


BACKTICK_PATH_PATTERN = re.compile(
    r"`((?:(?:\.\./){1,3})?(?:references|scripts|assets|subskills)/[^`]+)`"
)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)#][^)]+)\)")
SKILL_FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
GENERATED_TRACKED_PATTERNS = (
    "data/",
    "slprj/",
)
GENERATED_TRACKED_SUFFIXES = (
    ".slxc",
    ".asv",
    ".autosave",
    ".m~",
)
OPENAI_YAML_REQUIRED_FIELDS = (
    "display_name",
    "short_description",
    "default_prompt",
)
OPENAI_SHORT_DESCRIPTION_MIN = 25
OPENAI_SHORT_DESCRIPTION_MAX = 64
REFERENCE_TOC_LINE_THRESHOLD = 100


def display(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def display_resolved(path: Path, root: Path) -> str:
    return display(path, root) if path.is_relative_to(root) else str(path)


def resolve_reference(root: Path, declaring_file: Path, raw_path: str) -> Path:
    """Resolve a backticked repository path from the file that declared it."""
    if raw_path.startswith("../"):
        return (declaring_file.parent / raw_path).resolve()

    if declaring_file == root / "SKILL.md":
        return root / raw_path

    if declaring_file.match("subskills/*/SKILL.md") and raw_path.startswith(
        ("references/", "scripts/")
    ):
        return declaring_file.parent / raw_path

    return root / raw_path


def glob_matches(root: Path, declaring_file: Path, raw_path: str, resolved_path: Path):
    if raw_path.startswith("../"):
        return declaring_file.parent.glob(raw_path)

    if declaring_file.match("subskills/*/SKILL.md") and raw_path.startswith(
        ("references/", "scripts/")
    ):
        return declaring_file.parent.glob(raw_path)
    return root.glob(raw_path)


def iter_skill_files(root: Path):
    yield root / "SKILL.md"
    yield from sorted((root / "subskills").glob("*/SKILL.md"))


def iter_markdown_files(root: Path):
    yield root / "README.md"
    yield from iter_skill_files(root)
    yield from sorted((root / "references").glob("*.md"))
    yield from sorted((root / "subskills").glob("*/*.md"))
    yield from sorted((root / "subskills").glob("*/references/*.md"))


def iter_declared_paths(root: Path):
    for md_file in iter_markdown_files(root):
        if not md_file.exists():
            if md_file.name == "SKILL.md":
                yield md_file, "", md_file
            continue

        text = md_file.read_text(encoding="utf-8")
        for raw_path in sorted(set(BACKTICK_PATH_PATTERN.findall(text))):
            yield md_file, raw_path, resolve_reference(root, md_file, raw_path)

        for raw_path in sorted(set(MARKDOWN_LINK_PATTERN.findall(text))):
            if is_local_markdown_path(raw_path):
                yield md_file, raw_path, resolve_reference(root, md_file, raw_path)

    for skill_file in sorted((root / "subskills").glob("*/SKILL.md")):
        yield root / "SKILL.md", skill_file.relative_to(root).as_posix(), skill_file


def validate_long_reference_toc(root: Path):
    failures = []
    candidates = list((root / "references").glob("*.md"))
    candidates.extend((root / "subskills").glob("*/references/*.md"))

    for md_file in sorted(candidates):
        text = md_file.read_text(encoding="utf-8")
        if text.count("\n") + 1 <= REFERENCE_TOC_LINE_THRESHOLD:
            continue
        if "\n## Contents\n" not in text[:500]:
            failures.append(
                (
                    md_file,
                    f"reference longer than {REFERENCE_TOC_LINE_THRESHOLD} lines should include ## Contents near the top",
                )
            )
    return failures


def is_local_markdown_path(raw_path: str) -> bool:
    if raw_path.startswith(("http://", "https://", "mailto:", "#")):
        return False
    if raw_path.startswith("<") and raw_path.endswith(">"):
        raw_path = raw_path[1:-1]
    return not raw_path.startswith("/")


def parse_frontmatter(text: str):
    match = SKILL_FRONTMATTER_PATTERN.match(text)
    if not match:
        return None
    values = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def validate_skill_frontmatter(root: Path):
    failures = []
    for skill_file in iter_skill_files(root):
        if not skill_file.exists():
            failures.append((skill_file, "missing SKILL.md"))
            continue
        metadata = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        if not metadata:
            failures.append((skill_file, "missing YAML frontmatter"))
            continue
        for key in ("name", "description"):
            if not metadata.get(key):
                failures.append((skill_file, f"missing frontmatter field: {key}"))
    return failures


def tracked_generated_artifacts(root: Path):
    try:
        output = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True, stderr=subprocess.DEVNULL
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    artifacts = []
    for path in output.splitlines():
        if path.startswith(GENERATED_TRACKED_PATTERNS) or path.endswith(
            GENERATED_TRACKED_SUFFIXES
        ):
            artifacts.append(path)
    return artifacts


def validate_openai_yaml(root: Path):
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        return [(path, "missing agents/openai.yaml")]

    text = path.read_text(encoding="utf-8")
    failures = []
    if "interface:" not in text:
        failures.append((path, "missing interface section"))
    short_description = None
    for field in OPENAI_YAML_REQUIRED_FIELDS:
        match = re.search(rf"^\s+{re.escape(field)}:\s+\"(.+)\"", text, re.MULTILINE)
        if not match:
            failures.append((path, f"missing or unquoted interface.{field}"))
            continue
        if field == "short_description":
            short_description = match.group(1)
    if short_description is not None:
        if not (OPENAI_SHORT_DESCRIPTION_MIN <= len(short_description) <= OPENAI_SHORT_DESCRIPTION_MAX):
            failures.append(
                (
                    path,
                    "interface.short_description should be 25-64 characters",
                )
            )
    if "$simulink-power-electronics" not in text:
        failures.append((path, "default_prompt should mention $simulink-power-electronics"))
    return failures


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print only failures and the final summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    skill_path = root / "SKILL.md"

    if not skill_path.exists():
        print(f"missing {skill_path}", file=sys.stderr)
        return 1

    missing = []
    frontmatter_failures = validate_skill_frontmatter(root)
    openai_yaml_failures = validate_openai_yaml(root)
    toc_failures = validate_long_reference_toc(root)
    generated_artifacts = tracked_generated_artifacts(root)

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
    if not args.quiet:
        for declaring_file, raw_path, resolved_path in unique_checks:
            status = "missing" if (declaring_file, raw_path, resolved_path) in missing_set else "ok"
            source = display(declaring_file, root)
            target = display_resolved(resolved_path, root)
            print(f"{status}: {source} -> {raw_path or target}")

    for skill_file, reason in frontmatter_failures:
        print(f"frontmatter missing: {display(skill_file, root)} -> {reason}", file=sys.stderr)

    for yaml_file, reason in openai_yaml_failures:
        print(f"openai.yaml invalid: {display(yaml_file, root)} -> {reason}", file=sys.stderr)

    for md_file, reason in toc_failures:
        print(f"reference invalid: {display(md_file, root)} -> {reason}", file=sys.stderr)

    for artifact in generated_artifacts:
        print(f"tracked generated artifact: {artifact}", file=sys.stderr)

    if missing:
        print("\nMissing paths declared in skill files:", file=sys.stderr)
        for declaring_file, raw_path, resolved_path in missing:
            source = display(declaring_file, root)
            target = display_resolved(resolved_path, root)
            print(f"- {source}: {raw_path or target} -> {target}", file=sys.stderr)

    failed = (
        missing
        or frontmatter_failures
        or openai_yaml_failures
        or toc_failures
        or generated_artifacts
    )
    if not failed:
        print(f"ok: validated {len(unique_checks)} repository-local references and skill metadata")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
