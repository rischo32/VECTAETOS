from pathlib import Path
import json

README_PATH = Path("README.md")
JSON_PATH = Path("artifacts/run_2.jsonl")


def load_latest_state():
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"{JSON_PATH} not found")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if not lines:
        raise ValueError("JSONL is empty")

    return json.loads(lines[-1])


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


def replace_block(content, start_tag, end_tag, new_block):
    if start_tag not in content or end_tag not in content:
        raise ValueError(f"Missing markers: {start_tag} / {end_tag}")

    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]

    return f"{before}{start_tag}\n\n{new_block}\n{end_tag}{after}"


def update_readme():
    state = load_latest_state()
    poles = state["poles"]

    readme = README_PATH.read_text(encoding="utf-8")

    singularities_block = format_singularities(poles)

    readme = replace_block(
        readme,
        "<!-- Φ_SINGULARITIES_START -->",
        "<!-- Φ_SINGULARITIES_END -->",
        singularities_block
    )

    README_PATH.write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
