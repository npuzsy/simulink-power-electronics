#!/usr/bin/env python3
"""Preflight checks for using this skill on Simulink PE projects."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()


@dataclass
class Check:
    name: str
    status: str
    detail: str


def run(command: list[str], cwd: Path = ROOT, timeout: int = 30) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return completed.returncode, completed.stdout.strip()


def check_file(path: Path, name: str) -> Check:
    if path.exists():
        return Check(name, "pass", str(path))
    return Check(name, "fail", f"missing: {path}")


def check_optional_file(path: Path, name: str) -> Check:
    if path.exists():
        return Check(name, "pass", str(path))
    return Check(name, "warn", f"not found: {path}")


def check_command(command: str, name: str, required: bool = False) -> Check:
    path = shutil.which(command)
    if path:
        return Check(name, "pass", path)
    return Check(name, "fail" if required else "warn", f"`{command}` not on PATH")


def check_matlab() -> Check:
    matlab_path = shutil.which("matlab")
    if not matlab_path:
        return Check("MATLAB CLI", "warn", "`matlab` not on PATH; GUI/MCP may still work")

    code, output = run(["matlab", "-batch", "disp(version)"], timeout=60)
    if code == 0:
        version = output.splitlines()[-1] if output else "version detected"
        return Check("MATLAB CLI", "pass", f"{matlab_path} ({version})")
    return Check("MATLAB CLI", "warn", f"{matlab_path}; version check failed: {output[:200]}")


def check_matlab_products() -> list[Check]:
    matlab_path = shutil.which("matlab")
    if not matlab_path:
        return [
            Check("MATLAB products", "warn", "skip product checks because MATLAB CLI is not on PATH")
        ]

    expression = (
        "p=string({ver.Name}); "
        "req=[\"MATLAB\",\"Simulink\"]; "
        "opt=[\"Simscape\",\"Simscape Electrical\",\"Simulink Test\"]; "
        "fprintf('installed=%s\\n', strjoin(p, '|')); "
        "fprintf('missing_required=%s\\n', strjoin(setdiff(req,p), '|')); "
        "fprintf('missing_optional=%s\\n', strjoin(setdiff(opt,p), '|'));"
    )
    code, output = run(["matlab", "-batch", expression], timeout=90)
    if code != 0:
        return [Check("MATLAB products", "warn", f"product query failed: {output[:240]}")]

    missing_required = ""
    missing_optional = ""
    for line in output.splitlines():
        if line.startswith("missing_required="):
            missing_required = line.partition("=")[2].strip()
        if line.startswith("missing_optional="):
            missing_optional = line.partition("=")[2].strip()

    checks = []
    if missing_required:
        checks.append(Check("Required MATLAB products", "fail", f"missing: {missing_required}"))
    else:
        checks.append(Check("Required MATLAB products", "pass", "MATLAB and Simulink detected"))

    if missing_optional:
        checks.append(
            Check("Optional MATLAB products", "warn", f"missing or not installed: {missing_optional}")
        )
    else:
        checks.append(Check("Optional MATLAB products", "pass", "Simscape, Simscape Electrical, Simulink Test detected"))
    return checks


def check_repository_validation() -> Check:
    code, output = run([sys.executable, "scripts/validate_skill_structure.py", "--quiet"])
    if code == 0:
        return Check("Skill structure validation", "pass", output)
    return Check("Skill structure validation", "fail", output)


def collect_checks() -> list[Check]:
    checks = [
        check_file(ROOT / "SKILL.md", "Root SKILL.md"),
        check_file(ROOT / "agents" / "openai.yaml", "OpenAI metadata"),
        check_repository_validation(),
        check_command("git", "Git CLI", required=True),
        check_matlab(),
        check_optional_file(
            HOME / ".matlab" / "agentic-toolkits" / "bin" / "matlab-mcp-core-server",
            "MATLAB MCP Core Server",
        ),
        check_optional_file(
            HOME / ".matlab" / "agentic-toolkits" / "simulink",
            "Simulink Agentic Toolkit files",
        ),
        check_optional_file(
            HOME / ".codex" / "skills" / "using-superpowers" / "SKILL.md",
            "using-superpowers companion skill",
        ),
    ]
    checks.extend(check_matlab_products())
    return checks


def main() -> int:
    checks = collect_checks()
    width = max(len(check.name) for check in checks)
    for check in checks:
        print(f"{check.status.upper():4}  {check.name:<{width}}  {check.detail}")

    if any(check.status == "fail" for check in checks):
        print("\nPreflight failed: fix FAIL items before claiming repository readiness.")
        return 1

    if any(check.status == "warn" for check in checks):
        print("\nPreflight completed with warnings. Model-level work may be limited.")
        return 0

    print("\nPreflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
