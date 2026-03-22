#!/usr/bin/env python3

import sys
from pathlib import Path

# ============================================
# STRICT (zakázané konštrukcie)
# ============================================

FORBIDDEN_PATTERNS = [
    "agent decides",
    "system decides",
    "model decides",
    "choose the best",
    "select optimal",
    "maximize reward",
    "minimize loss",
    "policy learns",
    "system optimizes itself",
]

# ============================================
# POVOLENÉ KONCEPTY (Φ jazyk)
# ============================================

ALLOWED_TERMS = [
    "relation",
    "structure",
    "configuration",
    "projection",
    "collapse",
    "field",
    "topology",
    "deformation",
]

SCAN_DIRS = ["formal", "core", "governance", "VECTAETOS_MASTER_INDEX.md"]


# ============================================
# HELPERS
# ============================================

def scan_file(path: Path):
    violations = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            lower = line.lower()

            for pattern in FORBIDDEN_PATTERNS:
                if pattern in lower:
                    violations.append((path, i, pattern, line.strip()))

    return violations


# ============================================
# MAIN
# ============================================

def main():
    print("=== GOVERNANCE GUARD v2 ===")

    violations = []

    for target in SCAN_DIRS:
        p = Path(target)

        if p.is_file():
            violations.extend(scan_file(p))

        elif p.is_dir():
            for file in p.rglob("*.md"):
                violations.extend(scan_file(file))

    if not violations:
        print("✓ Governance OK")
        sys.exit(0)

    print("\n❌ GOVERNANCE VIOLATIONS:\n")

    for path, line, pattern, content in violations:
        print(f"{path}:{line} → [{pattern}] {content}")

    sys.exit(1)


if __name__ == "__main__":
    main()
