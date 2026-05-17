#!/usr/bin/env python3
"""
VECTAETOS — Epistemic Cryptography Pipeline

EK step for deterministic structural trace generation.

Canonical chain:

    outputs
    -> deterministic canonical serialization
    -> R ∈ so(8)
    -> Δ = d1R
    -> representability check
    -> kappa_trace as trace-only observable
    -> structural fingerprint

This module does NOT:
    - compute K(Φ)
    - compute κ
    - compute truth
    - compute safety
    - interpret meaning
    - select trajectories
    - optimize anything
    - mutate Φ or R
    - feed audit/projection output back into Φ

EK here is trace-only and non-authoritative.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from typing import Any, Final

import numpy as np

try:
    from .representability import is_representable
except ImportError:  # pragma: no cover - compatibility for direct execution
    from representability import is_representable  # type: ignore


N_NODES: Final[int] = 8
DELTA_DIM: Final[int] = 56


TRIPLES: Final[tuple[tuple[int, int, int], ...]] = tuple(
    (i, j, k)
    for i in range(N_NODES)
    for j in range(i + 1, N_NODES)
    for k in range(j + 1, N_NODES)
)


def _json_default(value: Any) -> str:
    """
    Deterministic fallback for values that are not JSON-native.

    This does not interpret the value.
    It only stabilizes serialization for trace generation.
    """
    return repr(value)


def canonical_serialize_outputs(outputs: Iterable[Any]) -> bytes:
    """
    Canonically serialize observed outputs.

    This serialization is used only to derive a deterministic structural trace.
    It is not a semantic interpretation of the outputs.
    """
    material = list(outputs)

    payload = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=_json_default,
    )

    return payload.encode("utf-8")


def reconstruct_R(outputs: Iterable[Any]) -> np.ndarray:
    """
    Deterministically reconstruct an antisymmetric R ∈ so(8) from outputs.

    This is an EK reconstruction artifact, not Φ itself.

    The reconstructed R:
        - is 8x8
        - is antisymmetric
        - has zero diagonal
        - is deterministic for the same outputs
    """
    canonical = canonical_serialize_outputs(outputs)
    digest = hashlib.sha3_512(canonical).digest()

    r = np.zeros((N_NODES, N_NODES), dtype=float)
    cursor = 0

    for i in range(N_NODES):
        for j in range(i + 1, N_NODES):
            b1 = digest[cursor % len(digest)]
            b2 = digest[(cursor + 1) % len(digest)]
            cursor += 2

            raw = (b1 << 8) | b2

            # Map [0, 65535] -> [-1, 1]
            value = (raw / 32767.5) - 1.0

            r[i, j] = value
            r[j, i] = -value

    return r


def delta_from_R(r: np.ndarray) -> np.ndarray:
    """
    Compute Δ = d1R.

    For i < j < k:

        Δ(i,j,k) = R_ij + R_jk + R_ki

    The output is a 56-dimensional vector ordered lexicographically over triples.
    """
    if r.shape != (N_NODES, N_NODES):
        raise ValueError(f"Expected R shape {(N_NODES, N_NODES)}, got {r.shape}")

    if not np.isfinite(r).all():
        raise ValueError("R contains non-finite values")

    if not np.allclose(r + r.T, np.zeros_like(r), rtol=0.0, atol=1e-12):
        raise ValueError("R is not antisymmetric")

    if not np.allclose(np.diag(r), np.zeros(N_NODES), rtol=0.0, atol=1e-12):
        raise ValueError("R diagonal must be zero")

    delta = np.zeros(DELTA_DIM, dtype=float)

    for index, (i, j, k) in enumerate(TRIPLES):
        delta[index] = r[i, j] + r[j, k] + r[k, i]

    return delta


def reconstruct_delta(outputs: Iterable[Any]) -> np.ndarray:
    """
    Deterministically reconstruct representable Δ from outputs.

    Correct structural chain:

        outputs -> R ∈ so(8) -> Δ = d1R

    Therefore Δ is representable by construction unless implementation invariants fail.

    This function does not construct arbitrary 56D curvature directly.
    """
    r = reconstruct_R(outputs)
    return delta_from_R(r)


def _kappa_numeric_trace(delta: Iterable[float] | np.ndarray) -> list[float]:
    """
    Produce a numeric trace-only structural observable from Δ.

    Important:
        This is not κ.
        This is not K(Φ).
        This is not a safety score.
        This is not a validity score.

    This exists only as a legacy numeric audit alias for deterministic tests.
    """
    arr = np.asarray(delta, dtype=float)

    if arr.shape != (DELTA_DIM,):
        raise ValueError(f"Expected Δ shape {(DELTA_DIM,)}, got {arr.shape}")

    if not np.isfinite(arr).all():
        raise ValueError("Δ contains non-finite values")

    mean = float(np.mean(arr))
    centered = arr - mean

    abs_centered = np.abs(centered)
    total = float(np.sum(abs_centered))

    if total == 0.0:
        return [0.0 for _ in range(DELTA_DIM)]

    trace = abs_centered / total

    return [float(value) for value in trace]


def kappa_trace(delta: Iterable[float] | np.ndarray) -> list[str]:
    """
    Produce a symbolic trace-only structural observable from Δ.

    Important:
        This is not κ.
        This is not K(Φ).
        This is not a safety score.
        This is not a validity score.

    The string representation prevents accidental treatment as numeric κ.
    """
    numeric = _kappa_numeric_trace(delta)
    return [format(value, ".12g") for value in numeric]


def structural_hash(delta: Iterable[float] | np.ndarray) -> str:
    """
    Compute deterministic structural fingerprint over Δ.

    The hash is an identity/fingerprint trace only.
    It is not proof of truth, correctness, safety, or validity.
    """
    arr = np.asarray(delta, dtype=float)

    if arr.shape != (DELTA_DIM,):
        raise ValueError(f"Expected Δ shape {(DELTA_DIM,)}, got {arr.shape}")

    if not np.isfinite(arr).all():
        raise ValueError("Δ contains non-finite values")

    canonical_values = [round(float(value), 12) for value in arr.tolist()]

    payload = json.dumps(
        {
            "type": "VECTAETOS_EK_DELTA_TRACE",
            "delta": canonical_values,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha3_512(payload).hexdigest()


def ek_step(outputs: Iterable[Any]) -> dict[str, Any]:
    """
    Single EK step.

    Returns a deterministic structural trace.

    The returned dictionary intentionally avoids:
        - interpretation
        - recommendation
        - decision
        - truth
        - validity authority
        - safety authority
        - K(Φ)
        - κ as numeric boundary
    """
    material = list(outputs)

    # 1. reconstruct representable curvature
    delta_hat = reconstruct_delta(material)

    # 2. representability constraint
    #
    # This is a structural check only:
    # Δ ∈ Im(d1)
    #
    # It is not K(Φ), not κ, not truth, not safety.
    if not is_representable(delta_hat):
        raise ValueError("DELTA_NOT_REPRESENTABLE")

    # 3. trace-only observables
    numeric_trace = _kappa_numeric_trace(delta_hat)
    trace = kappa_trace(delta_hat)
    fingerprint = structural_hash(delta_hat)
    delta_values = [float(value) for value in delta_hat.tolist()]

    return {
        "delta": delta_values,
        "delta_hat": delta_values,
        "kappa": numeric_trace,
        "kappa_trace": trace,
        "hash": fingerprint,
    }


def _hash_merkle_pair(left: str, right: str) -> str:
    """
    Deterministically hash a Merkle pair.

    This is structural identity only.
    It is not truth, validity, safety, selection, or interpretation.
    """
    payload = json.dumps(
        {
            "left": left,
            "right": right,
            "type": "VECTAETOS_EK_MERKLE_PAIR",
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha3_512(payload).hexdigest()


def _merkle_root(hashes: Iterable[str]) -> str:
    """
    Build a deterministic SHA3-512 Merkle root over EK step hashes.

    Empty trajectory is represented by a fixed structural empty-root hash.
    Odd levels duplicate the final item deterministically.
    """
    level = list(hashes)

    if not level:
        return hashlib.sha3_512(b"VECTAETOS_EK_EMPTY_TRAJECTORY").hexdigest()

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        level = [
            _hash_merkle_pair(level[index], level[index + 1])
            for index in range(0, len(level), 2)
        ]

    return level[0]


def ek_trajectory(stream: Iterable[Iterable[Any]]) -> dict[str, Any]:
    """
    Build a deterministic EK trajectory artifact from a stream of output batches.

    This function:
        - calls ek_step for each batch
        - preserves per-step structural hashes
        - computes a deterministic Merkle root
        - does not interpret outputs
        - does not select trajectories
        - does not optimize
        - does not mutate Φ, R, K(Φ), κ, QE, Vortex, projection, or human judgment
    """
    steps: list[dict[str, Any]] = []

    for index, outputs in enumerate(stream):
        step = ek_step(outputs)

        steps.append(
            {
                "index": index,
                "delta": step["delta"],
                "delta_hat": step["delta_hat"],
                "kappa": step["kappa"],
                "kappa_trace": step["kappa_trace"],
                "hash": step["hash"],
            }
        )

    step_hashes = [step["hash"] for step in steps]
    merkle_root = _merkle_root(step_hashes)

    artifact = {
        "type": "VECTAETOS_EK_TRAJECTORY_TRACE",
        "version": 1,
        "step_count": len(steps),
        "step_hashes": step_hashes,
        "merkle_root": merkle_root,
    }

    return {
        "steps": steps,
        "artifact": artifact,
    }


__all__ = [
    "DELTA_DIM",
    "N_NODES",
    "TRIPLES",
    "canonical_serialize_outputs",
    "delta_from_R",
    "ek_step",
    "ek_trajectory",
    "kappa_trace",
    "reconstruct_R",
    "reconstruct_delta",
    "structural_hash",
]
