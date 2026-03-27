# -------------------------------------------------
# Relational Projection Layer
# R_ij → pole-style projection for EK
# -------------------------------------------------
# This layer:
# - does NOT modify relations
# - does NOT interpret
# - does NOT optimize
# - only derives local scalars from relational structure
# -------------------------------------------------

from typing import List, Dict


def relations_to_poles(R: List[List[float]]) -> List[Dict]:
    """
    Projects antisymmetric relational matrix R_ij
    into pole-style representation required by
    Epistemic Cryptography layer.
    """

    n = len(R)
    poles = []

    for i in range(n):

        # Average absolute relational tension
        avg_tension = (
            sum(abs(R[i][j]) for j in range(n) if j != i)
            / (n - 1)
        )

        # Coherence proxy:
        # higher tension → lower local coherence
        coherence = max(0.0, 1.0 - avg_tension)

        pole = {
            "E": 0.0,              # not used (placeholder)
            "C": coherence,
            "T": avg_tension,
            "M": 0.0,              # not used
            "S": 0.0               # not used
        }

        poles.append(pole)

    return poles
