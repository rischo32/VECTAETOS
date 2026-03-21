"""
VECTAETOS — TetraGlyph Projection Bridge

Maps distribution M → glyph sequence

NON-ONTOLOGICAL
DESCRIPTIVE ONLY
"""

GLYPH_LEVELS = [
    (0.0, 0.4, "◯"),
    (0.4, 0.6, "◇"),
    (0.6, 0.8, "△"),
    (0.8, 1.0, "⌓"),
]


AXIOM_PAIRS = [
    ("INT", "LEX"),
    ("VER", "LIB"),
    ("UNI", "REL"),
    ("WIS", "CRE"),
]


def value_to_glyph(v: float) -> str:
    for low, high, glyph in GLYPH_LEVELS:
        if low <= v < high:
            return glyph
    return "⌓"


def distribution_to_glyph(dist: dict) -> str:
    """
    Convert M → 4-glyph sequence
    """

    values = []

    for a, b in AXIOM_PAIRS:
        combined = (dist[a] + dist[b]) / 2.0
        values.append(value_to_glyph(combined))

    return "".join(values)


def multi_projection_to_glyphs(bundle: dict) -> dict:
    """
    Convert all projections → glyphs
    """

    projections = bundle["projections"]

    glyphs = {
        name: distribution_to_glyph(dist)
        for name, dist in projections.items()
    }

    return glyphs
