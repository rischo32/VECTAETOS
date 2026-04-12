from typing import List
from rmk_types import RelationalMesh, NodeState


def compute_cycles(mesh: RelationalMesh) -> List[float]:
    n = mesh.size
    cycles = []

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                delta = (
                    mesh.get(i, j) +
                    mesh.get(j, k) +
                    mesh.get(k, i)
                )
                cycles.append(delta)

    return cycles


def coherence(mesh: RelationalMesh) -> float:
    cycles = compute_cycles(mesh)
    if not cycles:
        return 1.0
    return 1.0 - (sum(abs(c) for c in cycles) / len(cycles))


def local_uncertainty(nodes: List[NodeState]) -> List[float]:
    T_vals = [n.T for n in nodes]
    mean_T = sum(T_vals) / len(T_vals)

    mu = []
    for n in nodes:
        val = abs(n.T - mean_T) + (1 - n.C)
        mu.append(val)

    return mu


def total_uncertainty(mu: List[float]) -> float:
    return sum(mu)


def asymmetry(mesh: RelationalMesh, nodes: List[NodeState]) -> float:
    total = 0.0
    n = mesh.size

    for i in range(n):
        for j in range(i+1, n):
            Tij = abs(mesh.get(i, j))
            Ci = nodes[i].C
            Cj = nodes[j].C

            Aij = Tij * ((Ci + Cj) / 2)
            total += Aij

    return total

def humility(mu_total: float, A_total: float) -> float:
    if (mu_total + A_total) == 0:
        return 1.0
    return mu_total / (mu_total + A_total)
