#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()

CODE_EXTENSIONS = {
    ".py",
}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
}

SELF_PATH = Path("scripts/verify_repo_boundaries.py").resolve()

FORBIDDEN_PATTERNS = [
    re.compile(r"\bimport\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bimport\s+asi_mod\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asi_mod\b", re.IGNORECASE),
    re.compile(r"\bimport\s+asi[-_]mod\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asi[-_]mod\b", re.IGNORECASE),
]


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    if path.resolve() == SELF_PATH:
        return False
    return path.suffix.lower() in CODE_EXTENSIONS


def scan_file(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    violations: list[str] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                violations.append(
                    f"{path}:{idx}: forbidden downstream import detected -> {line.strip()}"
                )

    return violations


def main() -> int:
    violations: list[str] = []

    for path in ROOT.rglob("*"):
        if path.is_file() and should_scan(path):
            violations.extend(scan_file(path))

    if violations:
        print("[ERROR] Repository boundary violations detected:", file=sys.stderr)
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1

    print("[OK] No reverse imports detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
