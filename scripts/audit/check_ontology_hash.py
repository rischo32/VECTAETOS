import os
import json
import hashlib

# ============================================
# CONFIG
# ============================================

ONTOLOGY_PATHS = [
    "formal/",
    "core/",
    "vortex/"
]

HASH_FILE = "artifacts/ontology.hash"


# ============================================
# HELPERS
# ============================================

def collect_files(paths):
    files = []
    for base in paths:
        if not os.path.exists(base):
            continue
        for root, _, filenames in os.walk(base):
            for f in filenames:
                if f.endswith(".py") or f.endswith(".md"):
                    files.append(os.path.join(root, f))
    return sorted(files)


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def compute_hash(file_list):
    h = hashlib.sha256()

    for path in file_list:
        h.update(path.encode())
        h.update(read_file(path))

    return h.hexdigest()


# ============================================
# MAIN
# ============================================

def main():
    print("=== ONTOLOGY HASH CHECK ===")

    files = collect_files(ONTOLOGY_PATHS)

    if not files:
        print("No ontology files found.")
        exit(1)

    print(f"Files included: {len(files)}")

    current_hash = compute_hash(files)

    print(f"Current hash: {current_hash}")

    os.makedirs("artifacts", exist_ok=True)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            stored_hash = f.read().strip()

        print(f"Stored hash:  {stored_hash}")

        if current_hash != stored_hash:
            print("❌ ONTOLOGY DRIFT DETECTED")
            exit(1)
        else:
            print("✅ Ontology stable")

    else:
        print("No stored hash found. Creating baseline.")

    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

    print("Hash stored.")


if __name__ == "__main__":
    main()
