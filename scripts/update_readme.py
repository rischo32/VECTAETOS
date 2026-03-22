import json
from pathlib import Path

ARTIFACT = Path("artifacts/multi_run.json")
README = Path("README.md")


# ---------- LOAD ----------

def load_state():
    if not ARTIFACT.exists():
        return {}
    with open(ARTIFACT, "r") as f:
        return json.load(f)


# ---------- FORMATTERS ----------

def format_singularities(state):
    runs = state.get("runs", [])

    if not runs:
        return "_No data available_"

    rows = ""
    for i, r in enumerate(runs, start=1):
        rows += (
            f"| Σ{i} | {r['E']:.3f} | {r['C']:.3f} | "
            f"{r['T']:.3f} | {r['M']:.3f} | {r['S']:.3f} |\n"
        )

    return f"""
| Σ | E | C | T | M | S |
|---|---|---|---|---|---|
{rows}
"""


def format_delta(state):
    runs = state.get("runs", [])

    if len(runs) < 2:
        return "_Not enough data for Δ_"

    prev = runs[-2]
    curr = runs[-1]

    def d(k):
        return curr[k] - prev[k]

    return f"""
| Δ Metric | Value |
|----------|-------|
| ΔE | {d('E'):.4f} |
| ΔC | {d('C'):.4f} |
| ΔT | {d('T'):.4f} |
| ΔM | {d('M'):.4f} |
| ΔS | {d('S'):.4f} |
"""


def format_main_metrics(state):
    agg = state.get("aggregated", {})

    return f"""
| Metric | Value |
|--------|-------|
| QE | N/A |
| h (humility) | {agg.get("h", 0.0):.4f} |
| Asymmetry | {agg.get("asymmetry", 0.0):.4f} |
| Integrity | {agg.get("integrity", 0.0):.4f} |
| Triality | N/A |
"""


# ---------- UPDATE README ----------

def replace_section(content, marker, new_block):
    start = content.find(marker)
    if start == -1:
        return content

    end = content.find("<!-- END -->", start)
    if end == -1:
        return content

    end += len("<!-- END -->")

    return content[:start] + new_block + content[end:]


def main():
    state = load_state()

    singularities = format_singularities(state)
    metrics = format_main_metrics(state)
    delta = format_delta(state)

    with open(README, "r") as f:
        content = f.read()

    content = replace_section(
        content,
        "<!-- SINGULARITIES_START -->",
        f"<!-- SINGULARITIES_START -->\n{singularities}\n<!-- END -->",
    )

    content = replace_section(
        content,
        "<!-- METRICS_START -->",
        f"<!-- METRICS_START -->\n{metrics}\n<!-- END -->",
    )

    content = replace_section(
        content,
        "<!-- DELTA_START -->",
        f"<!-- DELTA_START -->\n{delta}\n<!-- END -->",
    )

    with open(README, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
