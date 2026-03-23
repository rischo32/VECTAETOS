from typing import List, Dict

from .field_features import FieldFeature


# =========================
# HEURISTIC PROXIES
# =========================
# IMPORTANT:
# These are NOT κ.
# These are observational thresholds only.

COHERENCE_PROXY = 0.25
UNCERTAINTY_THRESHOLD = 0.7
ASYMMETRY_THRESHOLD = 0.8


# =========================
# INTENSITY LABEL
# =========================

def intensity_label(v: float) -> str:
    if v > 0.9:
        return "extreme"
    if v > 0.7:
        return "high"
    if v > 0.4:
        return "medium"
    return "low"


# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(run: Dict) -> List[FieldFeature]:
    """
    Extract structural features from a single vortex run.

    This function does NOT:
    - evaluate correctness
    - detect errors
    - perform decisions

    It only maps observable structure.
    """

    features: List[FieldFeature] = []

    ltl = run.get("ltl", 0)
    poles = run.get("poles", [])

    # -------------------------
    # POLE-LEVEL FEATURES
    # -------------------------
    for i, p in enumerate(poles):
        C = p.get("C", 1.0)
        E = p.get("E", 0.0)

        # Low coherence region
        if C < COHERENCE_PROXY:
            features.append(FieldFeature(
                type="low_coherence_zone",
                ltl=ltl,
                indices=(i,),
                metric="C",
                value=C,
                threshold=COHERENCE_PROXY,
                intensity=intensity_label(1 - C)
            ))

        # High uncertainty region
        if E > UNCERTAINTY_THRESHOLD:
            features.append(FieldFeature(
                type="high_uncertainty_zone",
                ltl=ltl,
                indices=(i,),
                metric="E",
                value=E,
                threshold=UNCERTAINTY_THRESHOLD,
                intensity=intensity_label(E)
            ))

    # -------------------------
    # RELATIONAL FEATURES
    # -------------------------
    A = run.get("A", [])

    for i, row in enumerate(A):
        for j, val in enumerate(row):
            if i < j:
                abs_val = abs(val)

                if abs_val > ASYMMETRY_THRESHOLD:
                    features.append(FieldFeature(
                        type="high_asymmetry_edge",
                        ltl=ltl,
                        indices=(i, j),
                        metric="A_ij",
                        value=val,
                        threshold=ASYMMETRY_THRESHOLD,
                        intensity=intensity_label(abs_val)
                    ))

    return features
