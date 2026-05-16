# ============================================================
# VECTAETOS :: Epistemic Cryptography (v0.3)
# ------------------------------------------------------------
# Passive structural audit layer.
#
# - Does NOT modify Φ
# - Does NOT modify Vortex
# - Does NOT intervene
# - Numerically bounded
# - Topology-descriptive only
# ============================================================

import hashlib
import time
from typing import List, Dict

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

DELTA = 0.3  # humility signal threshold (descriptive only)


# ------------------------------------------------------------
# LOCAL UNCERTAINTY μᵢ
# ------------------------------------------------------------

def compute_mu_i(poles: List[Dict]) -> List[float]:

    tensions = [p["T"] for p in poles]
    n = len(tensions)

    if n == 0:
        return []

    mean_t = sum(tensions) / n

    mu_values = []

    for p in poles:
        local_variation = abs(p["T"] - mean_t)

        # Coherence already in [0,1]
        coherence_term = 1.0 - p["C"]

        mu = local_variation + coherence_term

        # Clamp for safety
        mu = max(0.0, min(mu, 2.0))

        mu_values.append(mu)

    return mu_values


# ------------------------------------------------------------
# STRUCTURAL ASYMMETRY Aᵢⱼ
# ------------------------------------------------------------

def compute_asymmetry(poles: List[Dict]) -> float:

    A_total = 0.0
    n = len(poles)

    for i in range(n):
        for j in range(i + 1, n):

            Ti = poles[i]["T"]
            Tj = poles[j]["T"]

            Ci = poles[i]["C"]
            Cj = poles[j]["C"]

            # symmetric magnitude
            A_ij = abs(Ti - Tj) * ((Ci + Cj) / 2.0)

            # clamp
            A_ij = max(0.0, min(A_ij, 2.0))

            A_total += A_ij

    return A_total


# ------------------------------------------------------------
# TOPOLOGICAL HUMILITY h
# ------------------------------------------------------------

def compute_h(mu_total: float, A_total: float) -> float:

    denom = mu_total + A_total

    if denom == 0.0:
        return 1.0

    h = mu_total / denom

    # bounded
    return max(0.0, min(h, 1.0))


# ------------------------------------------------------------
# EPISTEMIC SIGNATURE
# ------------------------------------------------------------

def epistemic_signature(poles: List[Dict], qe_state: bool) -> Dict:

    mu_values = compute_mu_i(poles)
    mu_total = sum(mu_values)

    A_total = compute_asymmetry(poles)

    h_topo = compute_h(mu_total, A_total)

    signature = {
        "trajectories": len(poles),
        "dimensions": len(poles[0]) if poles else 0,
        "qe_state": qe_state,
        "mu_total": mu_total,
        "asymmetry_total": A_total,
        "h_topo": h_topo,
        "time_layer": int(time.time())
    }

    # structural checksum (NOT data hash)
    struct_repr = f"{len(poles)}|{qe_state}|{round(h_topo,6)}"
    checksum = hashlib.sha256(struct_repr.encode()).hexdigest()

    h_flag = "ABOVE_DELTA" if h_topo >= DELTA else "BELOW_DELTA"

    return {
        "epistemic_signature": signature,
        "coherence_checksum": checksum,
        "h_flag": h_flag
    }
