#!/usr/bin/env python3
"""
VECTAETOS — README Glyph Updater (FINAL)

- Deterministic glyph generation (commit-based seed)
- SVG visualization
- Safe README patching
- CI-ready (GitHub Actions)

NON-ONTOLOGICAL
NO EPISTEMIC AUTHORITY
"""

import sys
from pathlib import Path
import subprocess
import hashlib
import random
import re

# ─────────────────────────────────────────────
# PATH FIX (CRITICAL)
# ─────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# local import (same folder)
from glyph_generator import generate_glyph_line

# repo imports
from infrastructure.projection_adapter_v2 import generate_projection_bundle
from TetraGlyph.glyph_svg import glyph_to_svg


README_PATH = ROOT / "README.md"


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
# GLYPH + SVG GENERATION
# ─────────────────────────────────────────────

def generate_visual_block():
    commit = get_git_hash()
    seed = seed_from_hash(commit)

    random.seed(seed)

    # minimalist input (no semantics)
    query = commit[:12]

    bundle = generate_projection_bundle(query)

    glyphs = bundle["glyphs"]
    entropy = bundle["entropy"]

    # text line
    glyph_line = " | ".join(glyphs.values())

    # SVG (first projection as representative)
    first_key = list(glyphs.keys())[0]
    svg = glyph_to_svg(glyphs[first_key])

    # entropy summary
    entropy_line = " | ".join(
        f"{k}:{round(v,3)}" for k, v in entropy.items()
    )

    return glyph_line, svg, entropy_line


# ─────────────────────────────────────────────
# README UPDATE
# ─────────────────────────────────────────────

def update_readme():
    if not README_PATH.exists():
        raise FileNotFoundError("README.md not found")

    content = README_PATH.read_text()

    glyph_line, svg, entropy_line = generate_visual_block()

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
