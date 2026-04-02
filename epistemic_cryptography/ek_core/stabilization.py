from typing import Dict, Tuple
import math

Index = int
Triple = Tuple[Index, Index, Index]


def l2_norm(delta: Dict[Triple, float]) -> float:
    return math.sqrt(sum(v * v for v in delta.values()))


def stabilize_delta(
    delta: Dict[Triple, float],
    epsilon: float = 1e-9,
    precision: int = 12,
) -> Dict[Triple, float]:
    """
    Stabilization layer for Delta_hat.

    Operations:
    1. Remove numerical noise (epsilon cutoff)
    2. Normalize scale (L2)
    3. Quantize values (round)

    NO:
    - optimization
    - smoothing
    - structural changes
    """

    # --- STEP 1: epsilon cutoff ---
    filtered = {}

    for k, v in delta.items():
        if abs(v) >= epsilon:
            filtered[k] = v
        else:
            filtered[k] = 0.0

    # --- STEP 2: normalization ---
    norm = l2_norm(filtered)

    if norm > 0:
        normalized = {k: v / norm for k, v in filtered.items()}
    else:
        normalized = filtered

    # --- STEP 3: quantization ---
    stabilized = {}

    for k, v in normalized.items():
        stabilized[k] = round(v, precision)

    return stabilized
