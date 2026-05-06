#!/usr/bin/env python3
"""
VECTAETOS :: Generate Visuals

Role:
- runtime visual projection helper
- non-authoritative visualization
- no ontology mutation
- no trajectory selection
- no optimization
- no automatic repository update
- no persistent docs write

Output:
- .runtime/observatory/runic_graph_latest.png

Python:
- 3.11+
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from forensics.feature_extractors import extract_features
from forensics.forensic_reader import load_latest


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT_DIR = ROOT / ".runtime" / "observatory"


def fixed_layout(n: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """
    Deterministic circular node layout.

    This is a visual layout only.
    It has no ontological status and does not rank nodes.
    """
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)
    return x, y


def load_matrix(run: dict[str, Any]) -> np.ndarray:
    """
    Load a relational matrix from a Vortex run snapshot.

    If no matrix is present, derive a descriptive antisymmetric visual matrix
    from pole tension/coherence values. This fallback is visualization-only.
    """
    matrix = run.get("A")
    if matrix is not None:
        return np.array(matrix)

    poles = run.get("poles")
    if not poles:
        raise ValueError("Missing both A and poles in run snapshot")

    n = len(poles)
    matrix_data = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            ti = float(poles[i].get("T", 0.0))
            tj = float(poles[j].get("T", 0.0))

            ci = float(poles[i].get("C", 0.0))
            cj = float(poles[j].get("C", 0.0))

            value = (ti - tj) + (ci - cj)

            matrix_data[i][j] = value
            matrix_data[j][i] = -value

    return np.array(matrix_data)


def generate_graph() -> Path | None:
    run = load_latest()
    if not run:
        print("[VISUALS] No run data available")
        return None

    matrix = load_matrix(run)
    n = matrix.shape[0]

    x, y = fixed_layout(n)
    features = extract_features(run)

    highlight_nodes: set[int] = set()
    highlight_edges: set[tuple[int, int]] = set()

    for feature in features:
        if feature.type == "low_coherence_zone" and feature.indices:
            highlight_nodes.add(int(feature.indices[0]))

        elif feature.type == "high_asymmetry_edge" and len(feature.indices) >= 2:
            i, j = int(feature.indices[0]), int(feature.indices[1])
            highlight_edges.add((min(i, j), max(i, j)))

    plt.figure(figsize=(6, 6))

    for i in range(n):
        for j in range(i + 1, n):
            value = matrix[i, j]

            if abs(value) < 0.05:
                continue

            if (i, j) in highlight_edges:
                color = "orange"
                linewidth = 2.5
                alpha = 0.9
            else:
                color = "gray"
                linewidth = 0.8
                alpha = 0.4

            plt.plot(
                [x[i], x[j]],
                [y[i], y[j]],
                color=color,
                linewidth=linewidth,
                alpha=alpha,
            )

    for i in range(n):
        if i in highlight_nodes:
            color = "red"
            size = 180
        else:
            color = "blue"
            size = 80

        plt.scatter(x[i], y[i], s=size, c=color)
        plt.text(x[i] * 1.1, y[i] * 1.1, f"{i}", ha="center", va="center")

    plt.title("Φ Relational Field — descriptive runtime visual projection")
    plt.axis("off")

    RUNTIME_OUT_DIR.mkdir(parents=True, exist_ok=True)

    out_path = RUNTIME_OUT_DIR / "runic_graph_latest.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"[VISUALS] Saved: {out_path}")
    print("[VISUALS] Runtime-only output.")
    print("[VISUALS] No repository docs update requested.")

    return out_path


def main() -> int:
    generate_graph()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
