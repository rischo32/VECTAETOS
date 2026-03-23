from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

from .feature_extractors import extract_features
from .field_features import FieldFeature


# =========================
# PATHS (CI + LOCAL SAFE)
# =========================

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "multi_run.json"


# =========================
# LOAD
# =========================

def load_latest() -> Dict:
    if not ARTIFACT.exists():
        return {}

    with open(ARTIFACT, "r", encoding="utf-8") as f:
        data = json.load(f)

    runs = data.get("runs", [])
    return runs[-1] if runs else {}


# =========================
# SUMMARY
# =========================

def summarize(features: List[FieldFeature]) -> Dict[str, int]:
    summary: Dict[str, int] = {}

    for f in features:
        summary[f.type] = summary.get(f.type, 0) + 1

    return summary


# =========================
# RENDER (TEXT REPORT)
# =========================

def render_report(features: List[FieldFeature]) -> str:
    lines: List[str] = []

    lines.append("Φ FORENSIC REPORT")
    lines.append("=" * 32)
    lines.append("")

    if not features:
        lines.append("No observable structural features.")
        return "\n".join(lines)

    # --- summary ---
    summary = summarize(features)

    lines.append("SUMMARY")
    lines.append("-" * 16)

    for k, v in sorted(summary.items()):
        lines.append(f"{k}: {v}")

    lines.append("")

    # --- details ---
    lines.append("DETAILS")
    lines.append("-" * 16)

    for f in features:
        idx = ",".join(map(str, f.indices))

        lines.append(
            f"[{f.type}] "
            f"(Σ:{idx}) "
            f"{f.metric}={f.value:.4f} "
            f"intensity={f.intensity}"
        )

    return "\n".join(lines)


# =========================
# OPTIONAL MARKDOWN OUTPUT
# =========================

def render_markdown(features: List[FieldFeature]) -> str:
    lines: List[str] = []

    lines.append("# Φ Forensic Report\n")

    if not features:
        lines.append("_No observable structural features._\n")
        return "\n".join(lines)

    summary = summarize(features)

    lines.append("## Summary\n")

    for k, v in sorted(summary.items()):
        lines.append(f"- **{k}**: {v}")

    lines.append("\n## Details\n")

    for f in features:
        idx = ",".join(map(str, f.indices))

        lines.append(
            f"- `{f.type}` | Σ[{idx}] | "
            f"{f.metric}={f.value:.4f} | "
            f"{f.intensity}"
        )

    return "\n".join(lines)


# =========================
# PIPELINE ENTRY
# =========================

def run_text_report() -> str:
    run = load_latest()
    if not run:
        return "No data available."

    features = extract_features(run)
    return render_report(features)


def run_markdown_report(output_path: Path | None = None) -> Path | None:
    run = load_latest()
    if not run:
        return None

    features = extract_features(run)
    md = render_markdown(features)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)

        return output_path

    return None


# =========================
# MAIN
# =========================

def main():
    report = run_text_report()
    print(report)


if __name__ == "__main__":
    main()
