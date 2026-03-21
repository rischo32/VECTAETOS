#!/usr/bin/env python3
"""
VECTAETOS — README Φ State Adapter

- číta posledný artifacts/run_*.jsonl
- extrahuje deterministický stav
- zapisuje do ROOT README medzi Φ markery
- CI-safe, deterministic, fail-fast
"""

from pathlib import Path
import json
import re
import sys


# === PATHS ===

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
ARTIFACTS_DIR = ROOT / "artifacts"


# === MARKERS ===

START = "<!-- Φ_STATE_START -->"
END = "<!-- Φ_STATE_END -->"


# === LOAD LAST ARTIFACT ===

def get_latest_artifact():
    files = sorted(ARTIFACTS_DIR.glob("run_*.jsonl"))
    if not files:
        raise FileNotFoundError("No artifacts/run_*.jsonl found")
    return files[-1]


def load_last_state(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        raise ValueError("Artifact file is empty")

    return json.loads(lines[-1])


# === EXTRACT STATE ===

def extract_metrics(state: dict):
    try:
        poles = state["poles"]
        qe = state["qe_aporia"]["aporia"]
        epistemic = state["epistemic"]

        # agregácia (deterministická)
        E = sum(p["E"] for p in poles) / len(poles)
        C = sum(p["C"] for p in poles) / len(poles)
        T = sum(p["T"] for p in poles) / len(poles)
        M = sum(p["M"] for p in poles) / len(poles)
        S = sum(p["S"] for p in poles) / len(poles)

        return {
            "E": E,
            "C": C,
            "T": T,
            "M": M,
            "S": S,
            "qe": qe,
            "h": epistemic.get("topological_humility", 0.0),
            "asym": epistemic.get("total_asymmetry", 0.0),
            "integrity": epistemic.get("integrity", 0.0),
            "triality": epistemic.get("triality_preserved", False),
        }

    except KeyError as e:
        raise RuntimeError(f"Missing key in state: {e}")


# === RENDER ===

def render_block(m: dict) -> str:
    return f"""
### Live Epistemic State

| Metric | Value |
|-------|------|
| E | {m["E"]:.4f} |
| C | {m["C"]:.4f} |
| T | {m["T"]:.4f} |
| M | {m["M"]:.4f} |
| S | {m["S"]:.4f} |
| QE | {"YES" if m["qe"] else "NO"} |
| h (humility) | {m["h"]:.4f} |
| Asymmetry | {m["asym"]:.4f} |
| Integrity | {m["integrity"]:.4f} |
| Triality | {"OK" if m["triality"] else "BROKEN"} |
""".strip()


# === UPDATE README ===

def update_readme(content: str, new_block: str) -> str:
    pattern = re.compile(
        rf"{START}.*?{END}",
        re.DOTALL
    )

    replacement = f"{START}\n{new_block}\n{END}"

    if not pattern.search(content):
        raise RuntimeError("Φ markers not found in README.md")

    return pattern.sub(replacement, content)


# === MAIN ===

def main():
    if not README_PATH.exists():
        print("ERROR: README.md not found", file=sys.stderr)
        sys.exit(1)

    artifact = get_latest_artifact()
    state = load_last_state(artifact)
    metrics = extract_metrics(state)
    block = render_block(metrics)

    original = README_PATH.read_text(encoding="utf-8")
    updated = update_readme(original, block)

    if original == updated:
        print("No changes in README")
        return

    README_PATH.write_text(updated, encoding="utf-8")
    print(f"README updated from {artifact.name}")


if __name__ == "__main__":
    main()
