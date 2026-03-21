#!/usr/bin/env python3
"""
VECTAETOS — README Glyph Updater

- Injects deterministic glyph projection into README
- Includes SVG visualization
- No epistemic authority
"""

import subprocess
import hashlib
import random
import re
from pathlib import Path

from infrastructure.projection_adapter_v2 import generate_projection_bundle
from TetraGlyph.glyph_svg import glyph_to_svg


README_PATH = Path("README.md")


# ─────────────────────────────────────────────
# GIT SEED
# ─────────────────────────────────────────────

def get_git_hash() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip()


def seed_from_hash(commit_hash: str) -> int:
    return int(hashlib.sha256(commit_hash.encode()).hexdigest(), 16) % (10**8)


# ─────────────────────────────────────────────
# GLYPH GENERATION
# ─────────────────────────────────────────────

def generate_glyph_bundle():
    commit = get_git_hash()
    seed = seed_from_hash(commit)

    random.seed(seed)

    # minimalist input (no semantics)
    query = commit[:12]

    bundle = generate_projection_bundle(query)

    glyphs = bundle["glyphs"]
    entropy = bundle["entropy"]

    # glyph text line
    glyph_line = " | ".join(glyphs.values())

    # merged glyph for SVG (first projection as representative)
    first_key = list(glyphs.keys())[0]
    svg = glyph_to_svg(glyphs[first_key])

    return glyph_line, svg, entropy


# ─────────────────────────────────────────────
# README UPDATE
# ─────────────────────────────────────────────

def update_readme():
    if not README_PATH.exists():
        raise FileNotFoundError("README.md not found")

    content = README_PATH.read_text()

    glyph_line, svg, entropy = generate_glyph_bundle()

    # optional: entropy summary
    entropy_line = " | ".join(
        f"{k}:{round(v,3)}" for k, v in entropy.items()
    )

    new_block = f"""<!-- GLYPH_SEQUENCE_START -->
{glyph_line}

{svg}

Entropy:
{entropy_line}
<!-- GLYPH_SEQUENCE_END -->"""

    pattern = r"<!-- GLYPH_SEQUENCE_START -->.*<!-- GLYPH_SEQUENCE_END -->"

    if not re.search(pattern, content, flags=re.DOTALL):
        raise ValueError("README missing GLYPH_SEQUENCE markers")

    updated = re.sub(pattern, new_block, content, flags=re.DOTALL)

    README_PATH.write_text(updated)


# ─────────────────────────────────────────────
# ENTRY
# ─────────────────────────────────────────────

if __name__ == "__main__":
    update_readme()
