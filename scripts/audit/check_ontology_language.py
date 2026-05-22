#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path

# ============================================
# CONFIG
# ============================================

FORBIDDEN_STRICT = [
    "reward function",
    "maximize reward",
    "minimize loss",
    "policy network",
    "agent learns",
]

# slová ktoré sú OK v matematike
ALLOWED_CONTEXT = [
    "representable",
    "non-representable",
    "valid",
    "invalid",
    "decision boundary",
    "formal decision",
]

# podozrivé – ale treba kontext
SUSPECT_WORDS = [
    "optimize",
    "optimization",
    "decision",
    "decide",
    "goal",
    "reward",
    "must",
    "enforce",
    "correct",
]

SCAN_DIRS = ["formal", "Core", "VECTAETOS_MASTER_INDEX.md"]


# ============================================
# HELPERS
# ============================================

def is_allowed_context(line: str) -> bool:
    return any(ctx in line.lower() for ctx in ALLOWED_CONTEXT)


def is_strict_violation(line: str) -> bool:
    return any(bad in line.lower() for bad in FORBIDDEN_STRICT)


def is_suspect_violation(line: str) -> bool:
    if is_allowed_context(line):
        return False
    return any(word in line.lower() for word in SUSPECT_WORDS)


def scan_file(path: Path):
    violations = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):

            if is_strict_violation(line):
                violations.append((path, i, "STRICT", line.strip()))

            elif is_suspect_violation(line):
                violations.append((path, i, "SUSPECT", line.strip()))

    return violations


# ============================================
# MAIN
# ============================================

def main():
    print("=== ONTOLOGY LANGUAGE GUARD v2 ===")

    all_violations = []

    for target in SCAN_DIRS:
        p = Path(target)

        if p.is_file():
            all_violations.extend(scan_file(p))

        elif p.is_dir():
            for file in p.rglob("*.md"):
                all_violations.extend(scan_file(file))

    if not all_violations:
        print("✓ No violations detected")
        sys.exit(0)

    strict = [v for v in all_violations if v[2] == "STRICT"]
    suspect = [v for v in all_violations if v[2] == "SUSPECT"]

    if strict:
        print("\n❌ STRICT VIOLATIONS:\n")
        for path, line, _, content in strict:
            print(f"{path}:{line} → {content}")
        sys.exit(1)

    print("\n⚠ SUSPECT LANGUAGE (allowed for now):\n")
    for path, line, _, content in suspect[:20]:
        print(f"{path}:{line} → {content}")

    print("\n✓ Passed (no strict violations)")
    sys.exit(0)


if __name__ == "__main__":
    main()
