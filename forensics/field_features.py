from dataclasses import dataclass
from typing import Tuple


@dataclass
class FieldFeature:
    """
    Descriptive unit of epistemic structure.

    This is NOT a problem, error, or anomaly.
    It represents an observable structural feature of Φ.
    """

    type: str          # e.g. "low_coherence_zone"
    ltl: int           # time layer (LTL index)
    indices: Tuple     # affected poles or relations (i) or (i,j)
    metric: str        # "C", "E", "A_ij", ...
    value: float       # observed value
    threshold: float   # heuristic projection threshold (NOT κ)
    intensity: str     # "low", "medium", "high", "extreme"
