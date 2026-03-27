# ============================================================
# VECTAETOS :: Simulation Vortex Φ (v0.4 CANONICAL — FIXED)
# ------------------------------------------------------------
# - deterministic
# - no noise
# - no break (no implicit goal)
# - antisymmetric relational field
# - QE = topological fragmentation
# - no optimization
# - no objective
# - no agent
# ============================================================

import random
import math
from typing import List, Tuple

# ------------------------------------------------------------
# DETERMINISM
# ------------------------------------------------------------

random.seed(42)

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

N = 8
INTERACTION_STRENGTH = 0.03
QE_EDGE_THRESHOLD = 0.15


# ------------------------------------------------------------
# INITIAL RELATIONAL MATRIX
# ------------------------------------------------------------

def generate_initial_relations(n: int = N) -> List[List[float]]:
    R = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            val = random.uniform(-0.2, 0.2)
            R[i][j] = val
            R[j][i] = -val  # antisymmetry

    return R


# ------------------------------------------------------------
# PAIRWISE INTERACTION FIELD
# ------------------------------------------------------------

def pairwise_interaction(R: List[List[float]]) -> List[List[float]]:
    new_R = [[0.0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(i + 1, N):

            tension = R[i][j]

            # deterministic interaction (no noise)
            coupling = 0.0
            for k in range(N):
                if k != i and k != j:
                    coupling += (R[i][k] - R[j][k])

            coupling *= INTERACTION_STRENGTH

            updated = tension + coupling

            # bounded stabilization
            stabilized = math.tanh(updated)

            new_R[i][j] = stabilized
            new_R[j][i] = -stabilized

    return new_R


# ------------------------------------------------------------
# QE DETECTOR (GRAPH FRAGMENTATION)
# ------------------------------------------------------------

def detect_qe(R: List[List[float]]) -> bool:
    """
    QE occurs when relational graph becomes disconnected.
    """

    visited = set()

    def dfs(node: int):
        for j in range(N):
            if abs(R[node][j]) > QE_EDGE_THRESHOLD and j not in visited:
                visited.add(j)
                dfs(j)

    visited.add(0)
    dfs(0)

    return len(visited) < N


# ------------------------------------------------------------
# RUN SIMULATION (TRAJECTORY GENERATION)
# ------------------------------------------------------------

def run_simulation(steps: int = 2000) -> Tuple[List[List[float]], bool]:

    R = generate_initial_relations()
    qe_state = False

    for _ in range(steps):

        R = pairwise_interaction(R)

        # no break — no objective
        if detect_qe(R):
            qe_state = True

    return R, qe_state


# ------------------------------------------------------------
# LOCAL TEST (NON-AUTHORITATIVE)
# ------------------------------------------------------------

if __name__ == "__main__":
    R_final, qe = run_simulation()
    print("QE state:", qe)
