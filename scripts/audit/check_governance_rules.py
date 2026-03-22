import os
import sys

# ============================================
# LOAD GOVERNANCE RULES
# ============================================

GOVERNANCE_FILES = [
    "governance/ONTOLOGY_RULES.md",
    "governance/LANGUAGE_CONSTRAINTS.md",
    "governance/NON_AGENTIC_POLICY.md"
]

# fallback (ak by súbory neexistovali)
DEFAULT_FORBIDDEN = [
    "optimize",
    "optimization",
    "decision",
    "decide",
    "best",
    "correct",
    "incorrect",
    "valid",
    "invalid",
    "representable",
    "verify",
    "enforce",
    "should",
    "must",
    "goal",
    "reward"
]

# čo skenujeme
TARGET_DIRS = [
    "VECTAETOS_MASTER_INDEX.md",
    "formal/",
    "core/",
    "scripts/"
]


# ============================================
# EXTRACT FORBIDDEN WORDS
# ============================================

def extract_forbidden():
    words = set()

    for path in GOVERNANCE_FILES:
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()

            for line in content.splitlines():
                line = line.strip()
                if line.startswith("- "):
                    words.add(line[2:].strip())

    if not words:
        return set(DEFAULT_FORBIDDEN)

    return words


# ============================================
# COLLECT FILES
# ============================================

def collect_files():
    files = []

    for target in TARGET_DIRS:
        if os.path.isfile(target):
            files.append(target)

        elif os.path.isdir(target):
            for root, _, filenames in os.walk(target):
                for f in filenames:
                    if f.endswith(".md"):
                        files.append(os.path.join(root, f))

    return files


# ============================================
# SCAN
# ============================================

def scan(files, forbidden):
    violations = []

    for path in files:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()

            for word in forbidden:
                if word in content:
                    violations.append((path, word))

    return violations


# ============================================
# MAIN
# ============================================

def main():
    print("=== GOVERNANCE GUARD ===")

    forbidden = extract_forbidden()
    print(f"Loaded forbidden tokens: {len(forbidden)}")

    files = collect_files()
    print(f"Scanning files: {len(files)}")

    violations = scan(files, forbidden)

    if violations:
        print("\n❌ GOVERNANCE VIOLATION:\n")

        for path, word in violations:
            print(f"{path} → '{word}'")

        sys.exit(1)

    print("\n✅ GOVERNANCE OK")


if __name__ == "__main__":
    main()
