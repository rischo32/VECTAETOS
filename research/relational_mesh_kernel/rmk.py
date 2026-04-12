from rmk_types import RelationalMesh, NodeState
from rmk_metrics import *

def build_test_mesh():
    mesh = RelationalMesh(8)

    # jednoduché seed relácie
    mesh.set(0, 1, 0.2)
    mesh.set(1, 2, -0.1)
    mesh.set(2, 3, 0.15)

    return mesh


def build_nodes():
    return [
        NodeState(0.7, 0.8, 0.2, 0.0, 0.1)
        for _ in range(8)
    ]


def run_rmk():
    mesh = build_test_mesh()
    nodes = build_nodes()

    coh = coherence(mesh)
    mu = local_uncertainty(nodes)
    mu_total = total_uncertainty(mu)
    A_total = asymmetry(mesh, nodes)
    h = humility(mu_total, A_total)

    return {
        "coherence": coh,
        "mu_total": mu_total,
        "A_total": A_total,
        "humility": h
    }


if __name__ == "__main__":
    result = run_rmk()
    print(result)
