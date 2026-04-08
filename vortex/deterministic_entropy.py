#!/usr/bin/env python3
# =========================================
# VECTAETOS :: DETERMINISTIC ENTROPY ENGINE
# VORTEX v2 + EK PIPELINE (Φ-CLEAN)
# =========================================

import math
import json
import hashlib
from dataclasses import dataclass
from typing import List, Dict
from itertools import permutations


# =========================================
# CONFIG
# =========================================

@dataclass
class Config:
    poles: int = 8
    steps: int = 500
    dt: float = 0.05


# =========================================
# SIGMA
# =========================================

@dataclass
class Sigma:
    E: float
    C: float
    T: float
    M: float
    S: float

    def clamp(self):
        self.E = max(0.0, min(1.5, self.E))
        self.C = max(0.0, min(1.0, self.C))
        self.T = max(0.0, min(1.0, self.T))
        self.M = max(0.0, self.M)
        self.S = max(0.0, min(1.0, self.S))


def init_poles(n: int) -> List[Sigma]:
    return [
        Sigma(E=0.5 + i * 0.01, C=0.6, T=0.2, M=0.0, S=0.05)
        for i in range(n)
    ]


# =========================================
# DETERMINISTIC FIELD
# =========================================

def deterministic_field(i: int, j: int, t: int) -> float:
    return math.sin((i+1)*12.9898 + (j+1)*78.233 + t*0.1) * 0.01


# =========================================
# CORE DYNAMICS
# =========================================

class Vortex:
    def __init__(self, config: Config):
        self.config = config
        self.poles = init_poles(config.poles)
        self.step = 0

    def step_dynamics(self):
        n = len(self.poles)

        for i in range(n):
            for j in range(i+1, n):
                si, sj = self.poles[i], self.poles[j]

                grad_T = sj.T - si.T
                grad_C = sj.C - si.C

                field = deterministic_field(i, j, self.step)

                flow = grad_T * grad_C
                flow *= (1.0 + si.M)
                flow += field

                si.E += flow * self.config.dt
                sj.E -= flow * self.config.dt

                si.M += abs(flow) * 0.01
                sj.M += abs(flow) * 0.01

        for s in self.poles:
            s.T += (1.0 - s.C) * 0.04 * self.config.dt
            s.C -= s.T * 0.015 * self.config.dt
            s.S += s.T * 0.01
            s.M *= 0.995

        for s in self.poles:
            s.clamp()

        self.step += 1


# =========================================
# EK CORE
# =========================================

def build_A(poles: List[Sigma]) -> List[List[float]]:
    n = len(poles)
    A = [[0.0]*n for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            val = abs(poles[i].T - poles[j].T) * ((poles[i].C + poles[j].C)/2)
            A[i][j] = val
            A[j][i] = -val

    return A


def compute_mu(poles: List[Sigma]) -> List[float]:
    n = len(poles)
    mean_T = sum(p.T for p in poles)/n
    return [abs(p.T - mean_T) + 0.5*(1.0 - p.C) for p in poles]


# =========================================
# CANONICAL Δ̂ (S₈ INVARIANT)
# =========================================

def apply_permutation(A, perm):
    n = len(A)
    B = [[0.0]*n for _ in range(n)]

    inv = {perm[i]: i for i in range(n)}

    for i in range(n):
        for j in range(n):
            B[i][j] = A[inv[i]][inv[j]]

    return B


def canonical_key(A):
    return tuple(tuple(round(v, 6) for v in row) for row in A)


def canonicalize(A):
    n = len(A)
    best = None
    best_key = None

    for perm in permutations(range(n)):
        candidate = apply_permutation(A, perm)
        key = canonical_key(candidate)

        if best_key is None or key < best_key:
            best = candidate
            best_key = key

    return best


# =========================================
# FINGERPRINT
# =========================================

def fingerprint(mu: List[float], A: List[List[float]], step: int) -> str:
    A_canon = canonicalize(A)

    payload = {
        "step": step,
        "mu": [round(x, 6) for x in mu],
        "A": [[round(v, 6) for v in row] for row in A_canon]
    }

    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()


# =========================================
# RUN SINGLE
# =========================================

def run_single(config: Config) -> Dict:
    vortex = Vortex(config)

    trajectory = []

    for _ in range(config.steps):
        vortex.step_dynamics()

        A = build_A(vortex.poles)
        mu = compute_mu(vortex.poles)
        fp = fingerprint(mu, A, vortex.step)

        trajectory.append(fp)

    return {
        "trajectory_length": len(trajectory),
        "final_fingerprint": trajectory[-1]
    }


# =========================================
# ENSEMBLE
# =========================================

def run_ensemble(config: Config, runs: int = 8) -> List[Dict]:
    results = []

    for i in range(runs):
        res = run_single(config)

        results.append({
            "id": i,
            "fingerprint": res["final_fingerprint"]
        })

    return results


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    cfg = Config()
    out = run_ensemble(cfg, runs=8)
    print(json.dumps(out, indent=2))
