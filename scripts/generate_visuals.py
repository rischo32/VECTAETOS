from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# forensics
from forensics.feature_extractors import extract_features
from forensics.forensic_reader import load_latest


# =========================
# PATHS
# =========================

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "observatory"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# LAYOUT (DETERMINISTICKÝ)
# =========================

def fixed_layout(n: int = 8):
    """
    Fixné pozície uzlov (kruh) → stabilný vizuál medzi runmi
    """
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)
    return x, y


# =========================
# LOAD DATA
# =========================

def load_matrix(run: dict):
    """
    Očakáva:
    run["A"] → antisymetrická matica (8x8)
    """
    A = np.array(run.get("A", []))
    if A.size == 0:
        raise ValueError("Missing matrix A in run")
    return A


# =========================
# MAIN VISUAL
# =========================

def generate_graph():
    run = load_latest()
    if not run:
        print("No run data available")
        return

    A = load_matrix(run)
    n = A.shape[0]

    # layout
    x, y = fixed_layout(n)

    # forensics
    features = extract_features(run)

    highlight_nodes = set()
    highlight_edges = set()

    for f in features:
        if f.type == "low_coherence_zone":
            highlight_nodes.add(f.indices[0])

        elif f.type == "high_asymmetry_edge":
            highlight_edges.add(tuple(f.indices))

    # =========================
    # PLOT
    # =========================

    plt.figure(figsize=(6, 6))

    # --- edges ---
    for i in range(n):
        for j in range(i + 1, n):
            val = A[i, j]

            if abs(val) < 0.05:
                continue

            if (i, j) in highlight_edges:
                color = "orange"
                lw = 2.5
                alpha = 0.9
            else:
                color = "gray"
                lw = 0.8
                alpha = 0.4

            plt.plot(
                [x[i], x[j]],
                [y[i], y[j]],
                color=color,
                linewidth=lw,
                alpha=alpha,
            )

    # --- nodes ---
    for i in range(n):
        if i in highlight_nodes:
            color = "red"
            size = 180
        else:
            color = "blue"
            size = 80

        plt.scatter(x[i], y[i], s=size, c=color)

        # label
        plt.text(x[i] * 1.1, y[i] * 1.1, f"{i}", ha="center", va="center")

    plt.title("Φ Relational Field (Highlighted)")
    plt.axis("off")

    out = OUT_DIR / "runic_graph_latest.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# =========================
# ENTRY
# =========================

def main():
    generate_graph()


if __name__ == "__main__":
    main()
