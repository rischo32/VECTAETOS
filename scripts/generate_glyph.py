#!/usr/bin/env python3
"""
VECTAETOS :: Glyph Generator
Deterministic projection from multi_run.json → docs/glyphs/

NON-AGENTIC:
- no optimization
- no randomness
- pure projection

INPUT:
    artifacts/multi_run.json

OUTPUT:
    docs/glyphs/latest.json
    docs/glyphs/latest.md
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Any, List


# =========================
# CONFIG
# =========================

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "multi_run.json"
OUT_DIR = ROOT / "docs" / "glyphs"

OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


# =========================
# IO
# =========================

def load_state() -> Dict[str, Any]:
    if not ARTIFACT.exists():
        raise FileNotFoundError(f"Missing artifact: {ARTIFACT}")

    with open(ARTIFACT, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# EXTRACTION
# =========================

def extract_last_run(data: Dict[str, Any]) -> Dict[str, Any]:
    runs = data.get("runs") or data.get("trajectories") or []

    if not runs:
        raise ValueError("No runs found in multi_run.json")

    return runs[-1]


def extract_sigma(run: Dict[str, Any]) -> List[Dict[str, float]]:
    return run.get("sigma") or run.get("singularities") or []


def extract_state(run: Dict[str, Any]) -> Dict[str, float]:
    return run.get("state") or run.get("metrics") or {}


# =========================
# GLYPH PROJECTION
# =========================

def build_glyph(sigma: List[Dict[str, float]], state: Dict[str, float]) -> Dict[str, Any]:
    """
    Pure structural projection
    """

    return {
        "type": "vectaetos_glyph",
        "sigma_count": len(sigma),
        "state": state,
        "sigma": sigma,
    }


# =========================
# SERIALIZATION
# =========================

def save_json(glyph: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(glyph, f, indent=2)


def save_markdown(glyph: Dict[str, Any]) -> None:
    lines = []
    lines.append("# Φ Glyph Projection\n")

    state = glyph["state"]

    if state:
        lines.append("## State\n")
        for k, v in state.items():
            if isinstance(v, (int, float)):
                lines.append(f"- {k}: {v:.6f}")
            else:
                lines.append(f"- {k}: {v}")
        lines.append("")

    sigma = glyph["sigma"]

    if sigma:
        lines.append("## Σ Singularities\n")
        header = "| Σ | E | C | T | M | S |"
        sep = "|---|---|---|---|---|---|"
        lines.append(header)
        lines.append(sep)

        for i, s in enumerate(sigma, start=1):
            E = s.get("E", 0.0)
            C = s.get("C", 0.0)
            T = s.get("T", 0.0)
            M = s.get("M", 0.0)
            S = s.get("S", 0.0)

            lines.append(
                f"| Σ{i} | {E:.3f} | {C:.3f} | {T:.3f} | {M:.3f} | {S:.3f} |"
            )

        lines.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================
# MAIN
# =========================

def main() -> None:
    data = load_state()

    run = extract_last_run(data)
    sigma = extract_sigma(run)
    state = extract_state(run)

    glyph = build_glyph(sigma, state)

    save_json(glyph)
    save_markdown(glyph)

    print("✔ glyph generated")
    print(f"→ {OUT_JSON}")
    print(f"→ {OUT_MD}")


if __name__ == "__main__":
    main()
