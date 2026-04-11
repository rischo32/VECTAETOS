# Core/epistemic.py

import math
from typing import List, Dict

from core.proof import CanonicalIdentityProof


class EpistemicMetrics:

    def __init__(self):
        self.mu = []
        self.A = []
        self.total_asymmetry = 0.0
        self.topological_humility = 0.0
        self.integrity = 1
        self.dominant_mode = False
        self.proof = ""

    def to_dict(self):
        return {
            "mu": self.mu,
            "A": self.A,
            "total_asymmetry": self.total_asymmetry,
            "topological_humility": self.topological_humility,
            "integrity": self.integrity,
            "dominant_mode": self.dominant_mode,
            "proof": self.proof
        }


class EpistemicCryptography:

    # =========================
    # BUILD A
    # =========================
    @staticmethod
    def build_relational_matrix(poles: List[Dict]) -> List[List[float]]:
        n = len(poles)
        A = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                Ti = poles[i]["T"]
                Tj = poles[j]["T"]
                Ci = poles[i]["C"]
                Cj = poles[j]["C"]

                val = abs(Ti - Tj) * ((Ci + Cj) / 2.0)

                A[i][j] = val
                A[j][i] = -val

        return A

    # =========================
    # MU
    # =========================
    @staticmethod
    def compute_mu(poles: List[Dict]) -> List[float]:
        n = len(poles)
        mean_T = sum(p["T"] for p in poles) / n

        mu = []
        for p in poles:
            mu_i = abs(p["T"] - mean_T) + (1.0 - p["C"])
            mu.append(mu_i)

        return mu

    # =========================
    # ASYMMETRY
    # =========================
    @staticmethod
    def total_asymmetry(A: List[List[float]]) -> float:
        n = len(A)
        total = 0.0

        for i in range(n):
            for j in range(i + 1, n):
                total += abs(A[i][j])

        return total

    # =========================
    # HUMILITY
    # =========================
    @staticmethod
    def topological_humility(mu: List[float], A_total: float) -> float:
        mu_tot = sum(mu)
        denom = mu_tot + A_total

        return mu_tot / denom if denom > 0 else 1.0

    # =========================
    # MAIN
    # =========================
    def compute(self, poles: List[Dict]) -> EpistemicMetrics:

        metrics = EpistemicMetrics()

        A = self.build_relational_matrix(poles)
        mu = self.compute_mu(poles)
        A_tot = self.total_asymmetry(A)
        h = self.topological_humility(mu, A_tot)

        metrics.A = A
        metrics.mu = mu
        metrics.total_asymmetry = A_tot
        metrics.topological_humility = h

        # integrity (basic)
        metrics.integrity = 1 if all(math.isfinite(x) for x in mu) else 0

        # dominant mode (simple placeholder)
        metrics.dominant_mode = False

        # PROOF
        metrics.proof = CanonicalIdentityProof.compute_proof(
            A,
            {
                "topological_humility": h,
                "integrity": metrics.integrity,
                "dominant_mode": metrics.dominant_mode
            }
        )

        return metrics
