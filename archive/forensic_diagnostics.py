#!/usr/bin/env python3
"""
VECTAETOS :: FORENSIC DIAGNOSTICS v1

Rozšírenie:
- Π_forensic operátory
- JSONL audit log
- export pre projekcie (glyph / adapter)
- bez intervencie do Φ

Status: NON-INTERVENTION COMPLIANT
"""

import json
import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


# ============================================================
# PROBLEM STRUCTURE
# ============================================================

@dataclass
class ProblemLocation:
    type: str
    ltl: int
    indices: Tuple
    metric: str
    value: float
    threshold: float
    severity: str


# ============================================================
# Π OPERÁTORY (FORENSIC PROJECTION)
# ============================================================

class PiForensicOperators:
    """
    Π_forensic : Φ → 𝒫(Ω)

    Ω = množina lokalizovaných problémov
    """

    @staticmethod
    def density(problems: List[ProblemLocation]) -> Dict[int, int]:
        """ρ_problem(i)"""
        density = {}

        for p in problems:
            if p.indices:
                for idx in p.indices:
                    density[idx] = density.get(idx, 0) + 1

        return density

    @staticmethod
    def entropy(problems: List[ProblemLocation]) -> float:
        """H_problem"""
        if not problems:
            return 0.0

        counts = {}
        for p in problems:
            counts[p.type] = counts.get(p.type, 0) + 1

        total = len(problems)
        H = 0.0

        for c in counts.values():
            p = c / total
            H -= p * math.log(p + 1e-12)

        return H

    @staticmethod
    def severity_vector(problems: List[ProblemLocation]) -> Dict[str, int]:
        vec = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for p in problems:
            vec[p.severity] += 1
        return vec


# ============================================================
# DIAGNOSTICS ENGINE
# ============================================================

class VortexDiagnostics:

    KAPPA = 0.25
    LAMBDA = 1.0
    DELTA_MAX = 2.6

    def __init__(
        self,
        ledger_file: str = "vortex_state.jsonl",
        log_file: str = "forensic_log.jsonl"
    ):
        self.ledger_file = ledger_file
        self.log_file = log_file
        self.history: List[Dict] = []
        self._load_history()

    def _load_history(self):
        if not Path(self.ledger_file).exists():
            return

        with open(self.ledger_file, 'r') as f:
            for line in f:
                try:
                    self.history.append(json.loads(line))
                except:
                    continue

    # ============================================================
    # LOCAL
    # ============================================================

    def find_incoherent_poles(self, state: Dict) -> List[ProblemLocation]:
        poles = state.get("poles", [])
        mu = state.get("epistemic", {}).get("mu", [])
        ltl = state.get("epistemic", {}).get("LTL", 0)

        if not mu or len(mu) != len(poles):
            return []

        mean = sum(mu) / len(mu)
        sigma = math.sqrt(sum((m - mean) ** 2 for m in mu) / len(mu))

        problems = []

        for i, (pole, m) in enumerate(zip(poles, mu)):
            if m > mean + 2 * sigma:
                problems.append(ProblemLocation(
                    "pole", ltl, (i,),
                    "local_uncertainty", m,
                    mean + 2 * sigma,
                    "high"
                ))

            if pole.get("C", 1.0) < self.KAPPA:
                problems.append(ProblemLocation(
                    "pole", ltl, (i,),
                    "coherence_below_kappa",
                    pole.get("C", 0),
                    self.KAPPA,
                    "critical"
                ))

        return problems

    def find_edges(self, state: Dict) -> List[ProblemLocation]:
        A = state.get("epistemic", {}).get("A_matrix", [])
        ltl = state.get("epistemic", {}).get("LTL", 0)

        problems = []
        n = len(A)

        for i in range(n):
            for j in range(i+1, n):
                val = abs(A[i][j])
                if val > self.LAMBDA * 0.9:
                    problems.append(ProblemLocation(
                        "edge", ltl, (i, j),
                        "relational_tension",
                        val,
                        self.LAMBDA,
                        "high"
                    ))

        return problems

    def find_triangles(self, state: Dict) -> List[ProblemLocation]:
        A = state.get("epistemic", {}).get("A_matrix", [])
        ltl = state.get("epistemic", {}).get("LTL", 0)

        problems = []
        n = len(A)

        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    delta = A[i][j] + A[j][k] + A[k][i]
                    if abs(delta) > self.DELTA_MAX * 0.5:
                        problems.append(ProblemLocation(
                            "triangle", ltl, (i, j, k),
                            "cycle_curvature",
                            abs(delta),
                            self.DELTA_MAX,
                            "medium"
                        ))

        return problems

    # ============================================================
    # QE
    # ============================================================

    def find_qe(self) -> List[ProblemLocation]:
        problems = []

        for s in self.history:
            qe = s.get("qe_aporia", {})
            if qe.get("aporia", False):
                problems.append(ProblemLocation(
                    "qe",
                    s.get("epistemic", {}).get("LTL", 0),
                    (),
                    "fragmentation",
                    qe.get("fragmentation_degree", 1.0),
                    0.0,
                    "critical"
                ))

        return problems

    # ============================================================
    # MAIN
    # ============================================================

    def full_diagnostic(self, current_state: Optional[Dict] = None) -> Dict:

        if current_state is None and self.history:
            current_state = self.history[-1]

        problems: List[ProblemLocation] = []

        if current_state:
            problems += self.find_incoherent_poles(current_state)
            problems += self.find_edges(current_state)
            problems += self.find_triangles(current_state)

        problems += self.find_qe()

        # Π OPERÁTORY
        density = PiForensicOperators.density(problems)
        entropy = PiForensicOperators.entropy(problems)
        severity_vec = PiForensicOperators.severity_vector(problems)

        report = {
            "timestamp": time.time(),
            "ltl": current_state.get("epistemic", {}).get("LTL", 0) if current_state else 0,
            "problems": [asdict(p) for p in problems],
            "pi": {
                "density": density,
                "entropy": entropy,
                "severity_vector": severity_vec
            }
        }

        self._log(report)

        return report

    # ============================================================
    # LOG
    # ============================================================

    def _log(self, report: Dict):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(report) + "\n")

    # ============================================================
    # EXPORT
    # ============================================================

    def to_projection_bundle(self, report: Dict) -> Dict:
        """
        Napojenie na projection_adapter_v2
        """
        return {
            "glyphs": {
                "entropy": report["pi"]["entropy"],
                "critical": report["pi"]["severity_vector"]["critical"],
                "density_max": max(report["pi"]["density"].values(), default=0)
            },
            "meta": {
                "ltl": report["ltl"]
            }
        }


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    diag = VortexDiagnostics()

    report = diag.full_diagnostic()

    print("\nFORENSIC SUMMARY")
    print("----------------")
    print("LTL:", report["ltl"])
    print("Problems:", len(report["problems"]))
    print("Entropy:", round(report["pi"]["entropy"], 4))
    print("Severity:", report["pi"]["severity_vector"])
