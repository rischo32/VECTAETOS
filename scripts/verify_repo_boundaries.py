#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
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

FORBIDDEN_PATTERNS = [
    re.compile(r"\bimport\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bimport\s+asi_mod\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asi_mod\b", re.IGNORECASE),
    re.compile(r"\bimport\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asimulator\b", re.IGNORECASE),
    re.compile(r"\bimport\s+asi[-_]?mod\b", re.IGNORECASE),
    re.compile(r"\bfrom\s+asi[-_]?mod\b", re.IGNORECASE),
]

FORBIDDEN_TOKENS = [
    "ASIMULATOR/",
    "ASI_MOD/",
]


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_EXTENSIONS


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
        for token in FORBIDDEN_TOKENS:
            if token in line:
                violations.append(
                    f"{path}:{idx}: forbidden downstream repository reference -> {line.strip()}"
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

    print("[OK] No reverse imports or forbidden downstream references detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
