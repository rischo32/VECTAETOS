"""
VECTAETOS — Production Core
Stateless Deterministic Field Configuration Engine
CORE_SPEC Compliant
"""

import time
import json
import hashlib
import random

from simulation_vortex import run_vortex
from relational_projection import project_relations
from epistemic_cryptography import encrypt_projection
from phi_audit import PhiAudit


# ---------------------------------------------------
# QE DETECTION (topological invariant only)
# ---------------------------------------------------

def detect_qe(R):
    """
    QE vzniká ak antisymetria nie je zachovaná.
    """
    n = len(R)
    for i in range(n):
        for j in range(n):
            if R[i][j] != -R[j][i]:
                return True
    return False


# ---------------------------------------------------
# ENTROPY SIGNATURE (deskriptívna, neoptimalizačná)
# ---------------------------------------------------

def compute_entropy_signature(R):
    flat = []
    for row in R:
        flat.extend(row)
    return hashlib.sha256(str(flat).encode()).hexdigest()


# ---------------------------------------------------
# PRODUCTION CORE PIPELINE
# ---------------------------------------------------

def run_pipeline(config: dict):

    # ---------------------------------------
    # 1. FORMÁLNY VSTUPNÝ MODEL
    # ---------------------------------------

    mode = config.get("mode", "simulation")
    steps = config.get("steps", 1000)
    seed = config.get("seed", None)
    meta = config.get("meta", {})

    if seed is not None:
        random.seed(seed)

    # ---------------------------------------
    # 2. VORTEX (Φ konfigurácia)
    # ---------------------------------------

    R = run_vortex(steps=steps)

    # ---------------------------------------
    # 3. QE DETEKCIA
    # ---------------------------------------

    qe_flag = detect_qe(R)

    # ---------------------------------------
    # 4. RELATIONAL PROJECTION
    # ---------------------------------------

    projection = project_relations(R)

    # ---------------------------------------
    # 5. EPISTEMICKÁ KRYPTOGRAFIA
    # ---------------------------------------

    encrypted_projection = encrypt_projection(projection)

    # ---------------------------------------
    # 6. ENTROPY SIGNATURE
    # ---------------------------------------

    entropy_signature = compute_entropy_signature(R)

    # ---------------------------------------
    # 7. AUDIT LOG (OBSERVAČNÝ)
    # ---------------------------------------

    audit = PhiAudit()  # Lokálny — bez globálneho stavu

    entry = {
        "timestamp": int(time.time()),
        "event_type": "FIELD_PROJECTION",
        "qe_emergence": qe_flag,
        "entropy_signature": entropy_signature,
        "projection_hash": hashlib.sha256(
            str(encrypted_projection).encode()
        ).hexdigest(),
        "vortex_step": steps
    }

    audit.append_entry(entry)

    # ---------------------------------------
    # 8. OUTPUT
    # ---------------------------------------

    return {
        "qe": qe_flag,
        "entropy": entropy_signature,
        "projection": encrypted_projection
    }


# ---------------------------------------------------
# CLI MODE
# ---------------------------------------------------

if __name__ == "__main__":

    config = {
        "mode": "simulation",
        "steps": 2000,
        "seed": None,
        "meta": {
            "silent": False,
            "log_level": "standard"
        }
    }

    result = run_pipeline(config)
    print(json.dumps(result, indent=2))
