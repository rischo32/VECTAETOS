from pathlib import Path
import json

README_PATH = Path("README.md")
JSON_PATH = Path("artifacts/run_2.jsonl")  # uprav ak máš iný názov


# ---------- LOAD ----------

def load_latest_state():
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"{JSON_PATH} not found")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if not lines:
        raise ValueError("JSONL is empty")

    return json.loads(lines[-1])


# ---------- FORMAT ----------

def format_main_metrics(state):
    epistemic = state.get("epistemic", {})

    return f"""| Metric | Value |
|--------|------|
| E | {state["poles"][0]["E"]:.4f} |
| C | {state["poles"][0]["C"]:.4f} |
| T | {state["poles"][0]["T"]:.4f} |
| M | {state["poles"][0]["M"]:.4f} |
| S | {state["poles"][0]["S"]:.4f} |
| QE | {"YES" if state.get("qe_aporia", {}).get("aporia") else "NO"} |
| h (humility) | {epistemic.get("topological_humidity", 0):.4f} |
| Asymmetry | {epistemic.get("total_asymmetry", 0):.4f} |
| Integrity | {1.0 if epistemic.get("integrity", False) else 0.0:.4f} |
| Triality | {"OK" if epistemic.get("triality_preserved") else "FAIL"} |
"""


def format_singularities(poles):
    rows = []
    for i, p in enumerate(poles, start=1):
        rows.append(
            f"| Σ{i} | {p['E']:.3f} | {p['C']:.3f} | {p['T']:.3f} | {p['M']:.3f} | {p['S']:.3f} |"
        )

    return f"""| Σ | E | C | T | M | S |
|--|--|--|--|--|--|
{chr(10).join(rows)}
"""


# ---------- UPDATE BLOCK ----------

def replace_block(content, start_tag, end_tag, new_block):
    if start_tag not in content or end_tag not in content:
        raise ValueError(f"Missing markers: {start_tag} / {end_tag}")

    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]

    return f"{before}{start_tag}\n\n{new_block}\n{end_tag}{after}"


# ---------- MAIN ----------

def update_readme():
    state = load_latest_state()
    poles = state["poles"]

    readme = README_PATH.read_text(encoding="utf-8")

    # --- update main metrics ---
    metrics_block = format_main_metrics(state)
    readme = replace_block(
        readme,
        "<!-- Φ_STATE_START -->",
        "<!-- Φ_STATE_END -->",
        metrics_block
    )

    # --- update singularities table ---
    singularities_block = format_singularities(poles)
    readme = replace_block(
        readme,
        "<!-- Φ_SINGULARITIES_START -->",
        "<!-- Φ_SINGULARITIES_END -->",
        singularities_block
    )

    README_PATH.write_text(readme, encoding="utf-8")


# ---------- ENTRY ----------

if __name__ == "__main__":
    update_readme()
