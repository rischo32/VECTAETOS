import json
import os

README_PATH = "README.md"
JSON_PATH = "artifacts/multi_run.json"
JSONL_PATH = "artifacts/multi_run.jsonl"

START_TAG = "<!-- Φ_STATE_START -->"
END_TAG = "<!-- Φ_STATE_END -->"


# ------------------------
# LOAD STATE (SAFE)
# ------------------------
def load_state():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH) as f:
            return json.load(f)

    elif os.path.exists(JSONL_PATH):
        with open(JSONL_PATH) as f:
            lines = f.readlines()
            if not lines:
                return None
            return json.loads(lines[-1])

    else:
        print("⚠ No artifacts found")
        return None


# ------------------------
# FORMAT TABLES
# ------------------------
def format_main_metrics(state):
    e = state.get("epistemic", {})

    return f"""
| Metric | Value |
|--------|-------|
| QE | {"YES" if e.get("qe") else "NO"} |
| h (humility) | {e.get("h", 0.0):.4f} |
| Asymmetry | {e.get("asymmetry", 0.0):.4f} |
| Integrity | {e.get("integrity", 0.0):.4f} |
| Triality | {e.get("triality", "N/A")} |
"""


def format_singularities(state):
    rows = ""
    for s in state.get("singularities", []):
        rows += f"| Σ{s['Σ']} | {s['E']} | {s['C']} | {s['T']} | {s['M']} | {s['S']} |\n"

    return f"""
| Σ | E | C | T | M | S |
|---|---|---|---|---|---|
{rows}
"""


def build_block(state):
    main = format_main_metrics(state)
    sigmas = format_singularities(state)

    return f"""
## 🧠 Live Epistemic State

{main}

## 🔷 Φ Singularities (Live)

{sigmas}
"""


# ------------------------
# REPLACE BLOCK
# ------------------------
def replace_block(readme, new_block):
    if START_TAG not in readme or END_TAG not in readme:
        raise ValueError(f"Missing markers: {START_TAG} / {END_TAG}")

    before = readme.split(START_TAG)[0]
    after = readme.split(END_TAG)[1]

    return f"{before}{START_TAG}\n{new_block}\n{END_TAG}{after}"


# ------------------------
# MAIN
# ------------------------
def update_readme():
    state = load_state()

    if state is None:
        print("⚠ Skipping README update (no state)")
        return

    if not os.path.exists(README_PATH):
        raise FileNotFoundError("README.md not found")

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    new_block = build_block(state)
    updated = replace_block(readme, new_block)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    print("✔ README updated")


if __name__ == "__main__":
    update_readme()
