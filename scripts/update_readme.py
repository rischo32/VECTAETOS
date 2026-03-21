#!/usr/bin/env python3
"""
VECTAETOS :: README STATE UPDATER

- Root-safe
- CI-safe
- Non-interventional
- Descriptive only
"""

import json
import re
from pathlib import Path

# ============================================================
# ROOT DETECTION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
STATE_FILE = ROOT / "vortex_state.jsonl"

# imports (lazy-safe)
try:
    from infrastructure.projection_adapter_v2 import generate_projection_bundle
except Exception:
    generate_projection_bundle = None

try:
    from infrastructure.svg_renderer import generate_svg
except Exception:
    generate_svg = None

try:
    from audit.forensic_diagnostics_v2 import VortexDiagnostics
except Exception:
    VortexDiagnostics = None


# ============================================================
# LOAD STATE
# ============================================================

def load_last_state():
    if not STATE_FILE.exists():
        return {}

    try:
        lines = STATE_FILE.read_text().splitlines()
        return json.loads(lines[-1]) if lines else {}
    except Exception:
        return {}


# ============================================================
# SAFE DEFAULTS
# ============================================================

def fallback_bundle():
    return {
        "glyphs": {
            "field": "◯",
            "tension": "△",
            "structure": "◇",
            "qe": "⊘"
        },
        "entropy": 0.0,
        "merkle": "0"*64
    }


def fallback_svg():
    return "<!-- no data -->"


# ============================================================
# MAIN
# ============================================================

def main():
    if not README.exists():
        raise FileNotFoundError(f"README not found at {README}")

    state = load_last_state()

    # --------------------------------------------------------
    # PROJECTION
    # --------------------------------------------------------
    if generate_projection_bundle:
        try:
            bundle = generate_projection_bundle("auto")
        except Exception:
            bundle = fallback_bundle()
    else:
        bundle = fallback_bundle()

    # --------------------------------------------------------
    # DIAGNOSTICS
    # --------------------------------------------------------
    if VortexDiagnostics:
        try:
            diag = VortexDiagnostics(str(STATE_FILE))
            report = diag.full_diagnostic(state)
        except Exception:
            report = {"problems": []}
    else:
        report = {"problems": []}

    # --------------------------------------------------------
    # QE STATE
    # --------------------------------------------------------
    qe = state.get("qe_aporia", {}).get("aporia", False)

    # --------------------------------------------------------
    # SVG
    # --------------------------------------------------------
    if generate_svg:
        try:
            svg = generate_svg(
                report={
                    "entropy": bundle.get("entropy", 0.0),
                    "singularity": 0,
                    "qe": qe
                },
                glyphs=bundle.get("glyphs", {}),
                diagnostics=report
            )
        except Exception:
            svg = fallback_svg()
    else:
        svg = fallback_svg()

    # --------------------------------------------------------
    # README UPDATE
    # --------------------------------------------------------
    content = README.read_text()

    block = f"""<!-- Φ_STATE_START -->
{svg}
<!-- Φ_STATE_END -->"""

    if "<!-- Φ_STATE_START -->" not in content:
        # ak tam ešte nie je blok → pridaj ho na koniec
        content += "\n\n## Live Epistemic State\n\n" + block
    else:
        content = re.sub(
            r"<!-- Φ_STATE_START -->.*<!-- Φ_STATE_END -->",
            block,
            content,
            flags=re.S
        )

    README.write_text(content)


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()
