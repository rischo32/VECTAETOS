import json
from pathlib import Path


ARTIFACT_PATH = Path("artifacts/multi_run.json")
README_PATH = Path("README.md")


def load_data():
    if not ARTIFACT_PATH.exists():
        return None
    with open(ARTIFACT_PATH) as f:
        return json.load(f)


# =========================
# Φ SINGULARITIES
# =========================
def format_singularities(data):
    runs = data.get("runs", [])
    if not runs:
        return "_No data_"

    last = runs[-1]
    poles = last.get("poles", [])

    if not poles:
        return "_No poles_"

    rows = ""
    for i, p in enumerate(poles, start=1):
        rows += (
            f"| Σ{i} | "
            f"{p.get('E',0):.3f} | "
            f"{p.get('C',0):.3f} | "
            f"{p.get('T',0):.3f} | "
            f"{p.get('M',0):.3f} | "
            f"{p.get('S',0):.3f} |\n"
        )

    return f"""
| Σ | E | C | T | M | S |
|---|---|---|---|---|---|
{rows}
"""


# =========================
# LIVE STATE
# =========================
def format_live_state(data):
    agg = data.get("aggregated", {})

    if not agg:
        return "_No aggregated state_"

    return f"""
| Metric | Value |
|--------|------|
| E | {agg.get('E',0):.4f} |
| C | {agg.get('C',0):.4f} |
| T | {agg.get('T',0):.4f} |
| M | {agg.get('M',0):.4f} |
| S | {agg.get('S',0):.4f} |
"""


# =========================
# Δ DRIFT
# =========================
def avg_poles(run):
    poles = run.get("poles", [])
    if not poles:
        return {}

    keys = ["E", "C", "T", "M", "S"]
    avg = {}

    for k in keys:
        avg[k] = sum(p.get(k, 0) for p in poles) / len(poles)

    return avg


def format_delta(data):
    runs = data.get("runs", [])

    if len(runs) < 2:
        return "_Not enough data_"

    prev = avg_poles(runs[-2])
    curr = avg_poles(runs[-1])

    def d(k):
        return curr.get(k, 0) - prev.get(k, 0)

    return f"""
| Δ Metric | Value |
|----------|-------|
| ΔE | {d('E'):.5f} |
| ΔC | {d('C'):.5f} |
| ΔT | {d('T'):.5f} |
| ΔM | {d('M'):.5f} |
| ΔS | {d('S'):.5f} |
"""


# =========================
# Φ FORENSIC PROJECTION
# =========================
def format_forensic_projection():
    path = Path("docs/observatory/runic_graph_latest.png")

    if not path.exists():
        return "_No projection available_"

    return f"![Φ Projection]({path})"


# =========================
# REPLACE SECTION
# =========================
def replace_section(content, marker, new_block):
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"

    if start not in content or end not in content:
        return content

    before = content.split(start)[0]
    after = content.split(end)[1]

    return f"{before}{start}\n{new_block}\n{end}{after}"


# =========================
# MAIN
# =========================
def main():
    data = load_data()

    if data is None:
        print("No artifact found")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_section(
        content,
        "SINGULARITIES",
        format_singularities(data)
    )

    content = replace_section(
        content,
        "LIVE_STATE",
        format_live_state(data)
    )

    content = replace_section(
        content,
        "DELTA",
        format_delta(data)
    )

    content = replace_section(
        content,
        "FORENSIC",
        format_forensic_projection()
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated.")


if __name__ == "__main__":
    main()
