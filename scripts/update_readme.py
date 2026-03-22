from pathlib import Path
import json

README_PATH = Path("README.md")
JSON_PATH = Path("artifacts/multi_run.json")


def load_state():
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"{JSON_PATH} not found")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_singularities(samples):
    rows = []
    for i, p in enumerate(samples, start=1):
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
    state = load_state()

    samples = state.get("samples", [])
    if not samples:
        raise ValueError("No samples in multi_run.json")

    readme = README_PATH.read_text(encoding="utf-8")

    singularities_block = format_singularities(samples)

    readme = replace_block(
        readme,
        "<!-- Φ_SINGULARITIES_START -->",
        "<!-- Φ_SINGULARITIES_END -->",
        singularities_block
    )

    README_PATH.write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
