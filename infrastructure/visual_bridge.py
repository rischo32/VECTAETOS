#!/usr/bin/env python3
"""
VECTAETOS :: VISUAL BRIDGE

Projection → Glyph → Render

- Non-agentic
- Non-interventional
- Descriptive only
"""

from typing import Dict, Any

from infrastructure.projection_adapter_v2 import generate_projection_bundle


# ============================================================
# GLYPH RENDER (simple textual)
# ============================================================

def format_glyphs(glyphs: Dict[str, str]) -> str:
    """
    Prevedie glyph dictionary na textový výstup.
    """
    lines = []
    lines.append("GLYPH PROJECTION")
    lines.append("=" * 40)

    for key, value in glyphs.items():
        lines.append(f"{key.upper():12s}: {value}")

    return "\n".join(lines)


# ============================================================
# BUNDLE RENDER
# ============================================================

def render_bundle(bundle: Dict[str, Any]) -> str:
    """
    Kompletný výstup projekcie.
    """
    lines = []

    glyphs = bundle.get("glyphs", {})
    entropy = bundle.get("entropy", 0.0)
    merkle = bundle.get("merkle", "")

    # glyphs
    lines.append(format_glyphs(glyphs))
    lines.append("")

    # metadata
    lines.append("METRICS")
    lines.append("=" * 40)
    lines.append(f"entropy : {entropy:.6f}")
    lines.append(f"merkle  : {merkle[:16]}...")

    return "\n".join(lines)


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def render_query(query: str) -> str:
    """
    Query → Projection → Glyph → Output
    """
    bundle = generate_projection_bundle(query)
    return render_bundle(bundle)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    try:
        while True:
            q = input("query > ")
            print()
            print(render_query(q))
            print()
    except KeyboardInterrupt:
        print("\nStopped.")
