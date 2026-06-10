#!/usr/bin/env python3
"""
VECTAETOS :: Vortex Runner

Role:
- deterministic single-run producer
- non-authoritative projection support
- no trajectory ranking
- no best-path selection
- no optimization
- no feedback into Φ
- no /artifacts dependency

Outputs:
- vortex_state.jsonl                    runtime trace emitted by VectaetosSimulation
- docs/observatory/vortex_latest.json   latest descriptive projection snapshot

Python:
- 3.11+

Run from:
- repository root
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from vortex.vortex_v1_2_3 import VectaetosSimulation, VortexConfig


ROOT = Path(__file__).resolve().parents[1]

RUNTIME_TRACE = ROOT / "vortex_state.jsonl"
OUT_DIR = ROOT / "docs" / "observatory"
LATEST_SNAPSHOT = OUT_DIR / "vortex_latest.json"


DEFAULT_SEED = 42
DEFAULT_STEPS = 500


def remove_previous_runtime_trace() -> None:
    """
    Remove only the local runtime trace from the previous run.

    This does not mutate ontology, anchors, Φ, K(Φ), κ, QE,
    audit layers, or projection semantics.
    """
    if RUNTIME_TRACE.exists():
        RUNTIME_TRACE.unlink()


def load_latest_runtime_state() -> dict[str, Any]:
    """
    Read the last JSONL entry emitted by the simulation.

    The last entry is treated as a descriptive snapshot only.
    """
    if not RUNTIME_TRACE.exists():
        raise FileNotFoundError(f"{RUNTIME_TRACE} not found after Vortex run")

    lines = RUNTIME_TRACE.read_text(encoding="utf-8").splitlines()

    if not lines:
        raise ValueError(f"{RUNTIME_TRACE} is empty")

    return json.loads(lines[-1])


def write_latest_snapshot(snapshot: dict[str, Any]) -> None:
    """
    Write a deterministic observatory-side snapshot.

    This replaces the old artifacts/multi_run.json output.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "role": "vortex_latest_descriptive_projection",
        "non_authoritative": True,
        "ranking": False,
        "optimization": False,
        "selection": False,
        "seed": DEFAULT_SEED,
        "steps": DEFAULT_STEPS,
        "snapshot": snapshot,
    }

    LATEST_SNAPSHOT.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def run_single(seed: int = DEFAULT_SEED, steps: int = DEFAULT_STEPS) -> dict[str, Any]:
    """
    Run one deterministic Vortex projection sample.

    The seed is a deterministic execution seed only.
    It is not a Σ mapping and has no ontological status.
    """
    remove_previous_runtime_trace()

    config = VortexConfig(
        steps=steps,
        seed=seed,
    )

    sim = VectaetosSimulation(config)
    sim.run()

    return load_latest_runtime_state()


def main() -> int:
    snapshot = run_single()
    write_latest_snapshot(snapshot)

    print("[VORTEX-RUNNER] single deterministic run complete")
    print(f"[VORTEX-RUNNER] runtime trace: {RUNTIME_TRACE}")
    print(f"[VORTEX-RUNNER] latest snapshot: {LATEST_SNAPSHOT}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
