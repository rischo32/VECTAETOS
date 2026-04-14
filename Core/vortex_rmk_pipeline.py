# core/vortex_rmk_pipeline.py

import numpy as np
import hashlib


# =========================
# Σ — SINGULARITIES
# =========================

SIGMA = [
    "INT", "LEX", "VER", "LIB",
    "UNI", "REL", "WIS", "CRE"
]


# =========================
# Φ — FIELD
# =========================

class Phi:
    def __init__(self, R: np.ndarray):
        assert R.shape == (8, 8), "R must be 8x8"
        assert np.allclose(R, -R.T), "R must be antisymmetric"
        self.R = R


# =========================
# INIT
# =========================

def random_R():
    R = np.random.randn(8, 8)
    return R - R.T


def init_phi():
    return Phi(random_R())


# =========================
# COHERENCE (Δ-based)
# =========================

def coherence(phi: Phi) -> float:
    R = phi.R
    n = 8

    total = 0.0
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                delta = R[i, j] + R[j, k] + R[k, i]
                total += abs(delta)
                count += 1

    return 1.0 - (total / count)


# =========================
# PERTURBATION
# =========================

def perturb(phi: Phi, scale=0.1) -> Phi:
    noise = np.random.randn(8, 8) * scale
    noise = noise - noise.T  # antisymmetric

    new_R = phi.R + noise
    return Phi(new_R)


# =========================
# QE DETECTION (CORRECT)
# =========================

def detect_QE(phi: Phi, trials=50) -> bool:
    """
    QE = neexistuje realizovateľná deformácia
    """

    for _ in range(trials):
        new_phi = perturb(phi)

        if coherence(new_phi) > 0:
            return False

    return True


# =========================
# TOPOLOGY HASH
# =========================

def topology_hash(phi: Phi) -> str:
    return hashlib.sha256(phi.R.tobytes()).hexdigest()


# =========================
# TETRAGLYPH (MINIMAL)
# =========================

def to_glyph(phi: Phi, state: str) -> dict:
    return {
        "topology_hash": topology_hash(phi),
        "state": state  # "REALIZABLE" | "QE"
    }


# =========================
# VORTEX
# =========================

def vortex(phi: Phi, steps=20):
    results = []

    current = phi

    for _ in range(steps):

        new_phi = perturb(current)

        if detect_QE(new_phi):
            state = "QE"
        else:
            state = "REALIZABLE"

        results.append((new_phi, state))

        current = new_phi

    return results


# =========================
# RUN
# =========================

def run_demo():
    phi = init_phi()

    traj = vortex(phi, steps=10)

    glyphs = [to_glyph(p, s) for p, s in traj]

    for i, g in enumerate(glyphs):
        print(f"τ{i}: {g}")


if __name__ == "__main__":
    run_demo()
