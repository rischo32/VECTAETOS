import os
import sys

# ❌ zakázané slová (ontologický drift)
FORBIDDEN = [
    "optimize",
    "optimization",
    "decision",
    "decide",
    "best",
    "choose",
    "correct",
    "incorrect",
    "valid",
    "invalid",
    "representable",
    "non-representable",
    "verify",
    "enforce",
    "should",
    "must",
    "goal",
    "reward"
]

# kde hľadať (pridaj podľa potreby)
TARGET_FILES = [
    "VECTAETOS_MASTER_INDEX.md",
    "formal/",
    "core/"
]


def scan_file(path):
    violations = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()

        for word in FORBIDDEN:
            if word in content:
                violations.append((path, word))

    return violations


def collect_files():
    files = []

    for target in TARGET_FILES:
        if os.path.isfile(target):
            files.append(target)
        elif os.path.isdir(target):
            for root, _, filenames in os.walk(target):
                for f in filenames:
                    if f.endswith(".md"):
                        files.append(os.path.join(root, f))

    return files


def main():
    print("=== ONTOLOGY LANGUAGE GUARD ===")

    files = collect_files()
    all_violations = []

    for f in files:
        all_violations.extend(scan_file(f))

    if all_violations:
        print("❌ FORBIDDEN LANGUAGE DETECTED:\n")
        for path, word in all_violations:
            print(f"{path} → '{word}'")

        sys.exit(1)

    print("✅ LANGUAGE OK")


if __name__ == "__main__":
    main()
