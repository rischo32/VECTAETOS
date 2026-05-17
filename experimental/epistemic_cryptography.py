#!/usr/bin/env python3
"""
VECTAETOS — Epistemic Cryptography Core
=======================================

File: ek_core/epistemic_cryptography.py
Python: 3.11+

Status:
    Deterministic audit-only implementation of
    EPISTEMIC_CRYPTOGRAPHY_FORMALISM.md v0.2.

Boundary:
    This module translates an already-given antisymmetric relational matrix R
    into external EK audit observables and structural fingerprints.

This module does NOT:
    - decide,
    - recommend,
    - optimize,
    - validate truth,
    - validate deployment,
    - compute K(Phi),
    - estimate kappa,
    - control Vortex,
    - select trajectories,
    - write back into Phi,
    - mutate R,
    - create a feedback loop.

Allowed transformation:
    R -> T_EK
    R -> Delta -> chi -> C_EK
    T_EK, C_EK -> mu
    mu -> A_EK
    mu, A_EK -> h_topo
    record -> SHA-256 + SHA3-512

The numeric observables generated here are audit observables only.
They are not K(Phi), not kappa, not safety, not truth, not authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


VERSION = "EPISTEMIC_CRYPTOGRAPHY_FORMALISM.v0.2"

SIGMA_ORDER: tuple[str, ...] = (
    "INT",
    "LEX",
    "VER",
    "LIB",
    "UNI",
    "REL",
    "WIS",
    "CRE",
)

N = 8
DEFAULT_EPSILON = 1.0e-12
DEFAULT_TOLERANCE = 1.0e-9


class EKInputError(ValueError):
    """Raised when the supplied relational matrix cannot be audited."""


def canonical_edges() -> list[tuple[int, int]]:
    """
    Return the canonical K8 edge ordering.

    There are C(8, 2) = 28 unordered edges.
    """
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def canonical_triangles() -> list[tuple[int, int, int]]:
    """
    Return the canonical K8 triangle ordering.

    There are C(8, 3) = 56 unordered triangles.
    """
    return [
        (i, j, k)
        for i in range(N)
        for j in range(i + 1, N)
        for k in range(j + 1, N)
    ]


def _is_number(value: Any) -> bool:
    """Return True only for finite int/float values excluding bool."""
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def _require_json_safe(value: Any, *, name: str) -> None:
    """
    Ensure a value can be serialized canonically to JSON.

    This prevents hidden non-deterministic objects from entering fingerprints.
    """
    try:
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise EKInputError(f"{name} must be JSON-serializable without NaN/Infinity") from exc


def _round_float(value: float, *, digits: int = 15) -> float:
    """
    Normalize float representation for stable JSON records.

    This is not an ontological operation.
    It only limits serialization noise in audit traces.
    """
    if not math.isfinite(value):
        raise EKInputError("EK observable became non-finite")
    rounded = round(float(value), digits)
    if rounded == -0.0:
        return 0.0
    return rounded


def _round_matrix(matrix: Sequence[Sequence[float]], *, digits: int = 15) -> list[list[float]]:
    """Return a rounded JSON-safe copy of a numeric matrix."""
    return [[_round_float(value, digits=digits) for value in row] for row in matrix]


def validate_R_shape(
    R: Sequence[Sequence[float]],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[list[float]]:
    """
    Validate and return a copied 8x8 antisymmetric real matrix.

    This function checks only mechanical representability for EK audit:
        - matrix shape is 8x8,
        - all values are finite numbers,
        - diagonal is zero within tolerance,
        - R_ij = -R_ji within tolerance.

    It does NOT validate K(Phi).
    It does NOT evaluate kappa.
    It does NOT authorize the field.
    """
    if isinstance(R, (str, bytes)) or not isinstance(R, Sequence):
        raise EKInputError("R must be a sequence of 8 numeric rows")

    if len(R) != N:
        raise EKInputError(f"R must have exactly {N} rows")

    copied: list[list[float]] = []

    for row_index, row in enumerate(R):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise EKInputError(f"R[{row_index}] must be a numeric row")
        if len(row) != N:
            raise EKInputError(f"R[{row_index}] must have exactly {N} values")

        copied_row: list[float] = []
        for col_index, value in enumerate(row):
            if not _is_number(value):
                raise EKInputError(f"R[{row_index}][{col_index}] must be a finite number")
            copied_row.append(float(value))
        copied.append(copied_row)

    if tolerance < 0 or not math.isfinite(tolerance):
        raise EKInputError("tolerance must be a finite non-negative number")

    for i in range(N):
        if abs(copied[i][i]) > tolerance:
            raise EKInputError(f"R[{i}][{i}] must be zero within tolerance")

    for i in range(N):
        for j in range(i + 1, N):
            residual = copied[i][j] + copied[j][i]
            if abs(residual) > tolerance:
                raise EKInputError(
                    f"R must be antisymmetric: R[{i}][{j}] + R[{j}][{i}] = {residual!r}"
                )

    return copied


def compute_relational_loads(
    R: Sequence[Sequence[float]],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> tuple[list[float], float]:
    """
    Compute local incident relational loads L_i and global edge load L_tot.

    L_i     = sum_{j != i} |R_ij|
    L_tot   = sum_{i < j} |R_ij|
    """
    matrix = validate_R_shape(R, tolerance=tolerance)

    local_loads = []
    for i in range(N):
        load = sum(abs(matrix[i][j]) for j in range(N) if j != i)
        local_loads.append(_round_float(load))

    total_load = sum(abs(matrix[i][j]) for i, j in canonical_edges())

    return local_loads, _round_float(total_load)


def compute_T_EK(
    R: Sequence[Sequence[float]],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[float]:
    """
    Compute normalized local relational tension observables T_i^EK.

    T_i^EK = L_i / (2 * L_tot), if L_tot > 0
    T_i^EK = 0,                  if L_tot = 0

    T_i^EK is an audit observable only.
    """
    local_loads, total_load = compute_relational_loads(R, tolerance=tolerance)

    if total_load <= tolerance:
        return [0.0 for _ in range(N)]

    denominator = 2.0 * total_load
    return [_round_float(load / denominator) for load in local_loads]


def compute_triangle_curvatures(
    R: Sequence[Sequence[float]],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[dict[str, Any]]:
    """
    Compute canonical triangle curvature observables.

    Delta_ijk = R_ij + R_jk + R_ki

    The result is JSON-ready and ordered by canonical K8 triangle order.
    """
    matrix = validate_R_shape(R, tolerance=tolerance)
    result: list[dict[str, Any]] = []

    for i, j, k in canonical_triangles():
        delta = matrix[i][j] + matrix[j][k] + matrix[k][i]
        result.append(
            {
                "indices": [i, j, k],
                "labels": [SIGMA_ORDER[i], SIGMA_ORDER[j], SIGMA_ORDER[k]],
                "Delta": _round_float(delta),
                "abs_Delta": _round_float(abs(delta)),
            }
        )

    return result


def compute_chi(
    R: Sequence[Sequence[float]],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[float]:
    """
    Compute local curvature load chi_i.

    chi_i = (1 / 21) * sum |Delta_abc| over triangles incident to i.

    K8 has C(7, 2) = 21 triangles incident to every center.
    """
    triangle_curvatures = compute_triangle_curvatures(R, tolerance=tolerance)
    chi: list[float] = []

    for center in range(N):
        incident_abs = [
            float(item["abs_Delta"])
            for item in triangle_curvatures
            if center in item["indices"]
        ]

        if len(incident_abs) != 21:
            raise RuntimeError("Internal K8 triangle incidence invariant failed")

        chi.append(_round_float(sum(incident_abs) / 21.0))

    return chi


def compute_C_EK(chi: Sequence[float]) -> list[float]:
    """
    Compute external curvature clarity observables C_i^EK.

    C_i^EK = 1 / (1 + chi_i)

    C_i^EK is not K(Phi).
    C_i^EK is not coherence.
    C_i^EK is not safety.
    """
    if len(chi) != N:
        raise EKInputError(f"chi must contain exactly {N} values")

    result: list[float] = []
    for index, value in enumerate(chi):
        if not _is_number(value):
            raise EKInputError(f"chi[{index}] must be a finite number")
        numeric = float(value)
        if numeric < 0:
            raise EKInputError(f"chi[{index}] must be non-negative")
        result.append(_round_float(1.0 / (1.0 + numeric)))

    return result


def compute_mu(
    T_EK: Sequence[float],
    C_EK: Sequence[float],
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> list[float]:
    """
    Compute local EK uncertainty observables.

    mu_i = T_i^EK / (T_i^EK + C_i^EK + epsilon)

    mu_i is an audit-visible observable.
    It is not a belief state.
    It is not epistemic authority.
    """
    if len(T_EK) != N:
        raise EKInputError(f"T_EK must contain exactly {N} values")
    if len(C_EK) != N:
        raise EKInputError(f"C_EK must contain exactly {N} values")
    if epsilon <= 0 or not math.isfinite(epsilon):
        raise EKInputError("epsilon must be a finite positive number")

    mu: list[float] = []
    for i, (t_value, c_value) in enumerate(zip(T_EK, C_EK, strict=True)):
        if not _is_number(t_value):
            raise EKInputError(f"T_EK[{i}] must be a finite number")
        if not _is_number(c_value):
            raise EKInputError(f"C_EK[{i}] must be a finite number")

        t_float = float(t_value)
        c_float = float(c_value)

        if t_float < 0:
            raise EKInputError(f"T_EK[{i}] must be non-negative")
        if c_float <= 0:
            raise EKInputError(f"C_EK[{i}] must be positive")

        mu.append(_round_float(t_float / (t_float + c_float + epsilon)))

    return mu


def compute_A_EK(mu: Sequence[float]) -> list[list[float]]:
    """
    Compute pairwise EK asymmetry matrix.

    A_ij^EK = |mu_i - mu_j|

    A_EK is descriptive only.
    It prescribes no correction.
    """
    if len(mu) != N:
        raise EKInputError(f"mu must contain exactly {N} values")

    values: list[float] = []
    for index, value in enumerate(mu):
        if not _is_number(value):
            raise EKInputError(f"mu[{index}] must be a finite number")
        numeric = float(value)
        if numeric < 0:
            raise EKInputError(f"mu[{index}] must be non-negative")
        values.append(numeric)

    matrix: list[list[float]] = []
    for i in range(N):
        row: list[float] = []
        for j in range(N):
            if i == j:
                row.append(0.0)
            else:
                row.append(_round_float(abs(values[i] - values[j])))
        matrix.append(row)

    return matrix


def compute_total_asymmetry(A_EK: Sequence[Sequence[float]]) -> float:
    """
    Compute total pairwise asymmetry over canonical unordered pairs.

    A_tot^EK = sum_{i < j} A_ij^EK
    """
    if len(A_EK) != N:
        raise EKInputError(f"A_EK must have exactly {N} rows")

    copied: list[list[float]] = []
    for row_index, row in enumerate(A_EK):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise EKInputError(f"A_EK[{row_index}] must be a numeric row")
        if len(row) != N:
            raise EKInputError(f"A_EK[{row_index}] must have exactly {N} values")

        copied_row: list[float] = []
        for col_index, value in enumerate(row):
            if not _is_number(value):
                raise EKInputError(f"A_EK[{row_index}][{col_index}] must be finite")
            numeric = float(value)
            if numeric < 0:
                raise EKInputError(f"A_EK[{row_index}][{col_index}] must be non-negative")
            copied_row.append(numeric)
        copied.append(copied_row)

    total = sum(copied[i][j] for i, j in canonical_edges())
    return _round_float(total)


def compute_h_topo(
    mu: Sequence[float],
    A_EK: Sequence[Sequence[float]],
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> float:
    """
    Compute topological humility observable.

    h_topo = mu_tot / (mu_tot + A_tot^EK + epsilon)

    h_topo is not a reward.
    h_topo is not a target.
    h_topo is not K(Phi).
    h_topo is not kappa.
    h_topo is not deployment admissibility.
    """
    if epsilon <= 0 or not math.isfinite(epsilon):
        raise EKInputError("epsilon must be a finite positive number")

    if len(mu) != N:
        raise EKInputError(f"mu must contain exactly {N} values")

    mu_values: list[float] = []
    for index, value in enumerate(mu):
        if not _is_number(value):
            raise EKInputError(f"mu[{index}] must be a finite number")
        numeric = float(value)
        if numeric < 0:
            raise EKInputError(f"mu[{index}] must be non-negative")
        mu_values.append(numeric)

    mu_total = sum(mu_values)
    asymmetry_total = compute_total_asymmetry(A_EK)
    denominator = mu_total + asymmetry_total + epsilon

    if denominator <= 0:
        return 0.0

    return _round_float(mu_total / denominator)


def _strip_fingerprints(payload: Mapping[str, Any]) -> dict[str, Any]:
    """
    Return a deep-copied payload without fingerprint fields.

    Fingerprints must not hash themselves.
    """
    copied = copy.deepcopy(dict(payload))
    copied.pop("fingerprint", None)
    copied.pop("fingerprints", None)
    return copied


def canonical_serialize(payload: Mapping[str, Any]) -> str:
    """
    Deterministically serialize a JSON-safe payload.

    This function is used as the canonical input for structural fingerprints.
    """
    _require_json_safe(payload, name="payload")
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def fingerprint_record(payload: Mapping[str, Any]) -> dict[str, str]:
    """
    Compute dual structural fingerprints for a payload.

    The top-level fingerprint/fingerprints fields are excluded to avoid
    self-referential hashing.
    """
    payload_without_fingerprints = _strip_fingerprints(payload)
    serialized = canonical_serialize(payload_without_fingerprints).encode("utf-8")

    return {
        "sha256": hashlib.sha256(serialized).hexdigest(),
        "sha3_512": hashlib.sha3_512(serialized).hexdigest(),
    }


def verify_fingerprint(payload: Mapping[str, Any]) -> bool:
    """
    Verify that a record's stored fingerprints match its canonical content.

    This verifies only structural equality of serialized audit content.
    It does not verify truth, safety, K(Phi), kappa, or deployment validity.
    """
    stored = payload.get("fingerprint")
    if not isinstance(stored, Mapping):
        return False

    expected = fingerprint_record(payload)

    return (
        stored.get("sha256") == expected["sha256"]
        and stored.get("sha3_512") == expected["sha3_512"]
    )


def build_ek_record(
    R: Sequence[Sequence[float]],
    *,
    metadata: Mapping[str, Any] | None = None,
    field_state_id: str | None = None,
    run_id: str | None = None,
    ledger_index: int | str | None = None,
    epsilon: float = DEFAULT_EPSILON,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, Any]:
    """
    Build a complete EK audit record from an already-given R matrix.

    This function does not mutate R.

    It returns a JSON-ready dict containing:
        - canonical sigma order,
        - copied relation matrix,
        - T_EK,
        - Delta triangle curvature records,
        - chi,
        - C_EK,
        - mu,
        - A_EK,
        - h_topo,
        - dual fingerprints,
        - explicit non-authority boundary.

    Important:
        The returned observables are external audit observables only.
    """
    matrix = validate_R_shape(R, tolerance=tolerance)

    if metadata is None:
        safe_metadata: dict[str, Any] = {}
    else:
        _require_json_safe(metadata, name="metadata")
        safe_metadata = copy.deepcopy(dict(metadata))

    if ledger_index is not None:
        _require_json_safe(ledger_index, name="ledger_index")
    if field_state_id is not None:
        _require_json_safe(field_state_id, name="field_state_id")
    if run_id is not None:
        _require_json_safe(run_id, name="run_id")

    local_loads, total_load = compute_relational_loads(matrix, tolerance=tolerance)
    T_EK = compute_T_EK(matrix, tolerance=tolerance)
    triangle_curvatures = compute_triangle_curvatures(matrix, tolerance=tolerance)
    chi = compute_chi(matrix, tolerance=tolerance)
    C_EK = compute_C_EK(chi)
    mu = compute_mu(T_EK, C_EK, epsilon=epsilon)
    A_EK = compute_A_EK(mu)
    A_total_EK = compute_total_asymmetry(A_EK)
    h_topo = compute_h_topo(mu, A_EK, epsilon=epsilon)

    record: dict[str, Any] = {
        "version": VERSION,
        "sigma_order": list(SIGMA_ORDER),
        "ledger": {
            "index": ledger_index,
            "field_state_id": field_state_id,
            "run_id": run_id,
            "append_only_required": True,
        },
        "graph_domain": {
            "vertices": N,
            "edges": len(canonical_edges()),
            "triangles": len(canonical_triangles()),
        },
        "relation_matrix": _round_matrix(matrix),
        "tension": {
            "local_loads": local_loads,
            "total_load": total_load,
            "T_EK": T_EK,
        },
        "curvature": {
            "triangle_curvatures": triangle_curvatures,
            "chi": chi,
            "C_EK": C_EK,
        },
        "uncertainty": {
            "mu": mu,
            "mu_total": _round_float(sum(mu)),
        },
        "asymmetry": {
            "A_EK": A_EK,
            "A_total_EK": A_total_EK,
        },
        "humility": {
            "h_topo": h_topo,
            "interpretation": "audit_observable_only",
        },
        "metadata": safe_metadata,
        "boundary": {
            "authority": "none",
            "agency": "none",
            "optimization": "none",
            "decision_power": "none",
            "runtime_control": "none",
            "feedback_into_phi": False,
            "writes_into_phi": False,
            "mutates_R": False,
            "computes_K_phi": False,
            "estimates_kappa": False,
            "controls_vortex": False,
            "selects_trajectories": False,
        },
    }

    record["fingerprint"] = fingerprint_record(record)
    return record


def build_zero_record(
    *,
    metadata: Mapping[str, Any] | None = None,
    field_state_id: str | None = None,
    run_id: str | None = None,
    ledger_index: int | str | None = None,
) -> dict[str, Any]:
    """
    Build an EK record from the zero antisymmetric relation matrix.

    This is useful as a deterministic fixture.
    """
    zero = [[0.0 for _ in range(N)] for _ in range(N)]
    return build_ek_record(
        zero,
        metadata=metadata,
        field_state_id=field_state_id,
        run_id=run_id,
        ledger_index=ledger_index,
    )


def load_R_from_json(path: str | Path) -> list[list[float]]:
    """
    Load R from a JSON file.

    Accepted shapes:
        1. [[...], ...]
        2. {"R": [[...], ...]}
        3. {"relation_matrix": [[...], ...]}

    This function only reads the input file.
    It does not write outputs.
    """
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EKInputError(f"Input file not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise EKInputError(f"Invalid JSON input: {source}") from exc

    if isinstance(raw, Mapping):
        if "R" in raw:
            raw_R = raw["R"]
        elif "relation_matrix" in raw:
            raw_R = raw["relation_matrix"]
        else:
            raise EKInputError("JSON object must contain 'R' or 'relation_matrix'")
    else:
        raw_R = raw

    return validate_R_shape(raw_R)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic VECTAETOS Epistemic Cryptography audit record "
            "from an already-given 8x8 antisymmetric R matrix. Prints JSON to stdout."
        )
    )
    parser.add_argument(
        "input_json",
        help="Path to JSON containing either an 8x8 matrix, {'R': matrix}, or {'relation_matrix': matrix}.",
    )
    parser.add_argument("--field-state-id", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--ledger-index", default=None)
    parser.add_argument(
        "--metadata-json",
        default=None,
        help="Optional JSON object string for non-authoritative metadata.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    """
    CLI entry point.

    The CLI prints the EK audit record to stdout.
    It does not write files and does not mutate the source JSON.
    """
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        metadata = None
        if args.metadata_json is not None:
            parsed_metadata = json.loads(args.metadata_json)
            if not isinstance(parsed_metadata, Mapping):
                raise EKInputError("--metadata-json must decode to a JSON object")
            metadata = parsed_metadata

        R = load_R_from_json(args.input_json)
        record = build_ek_record(
            R,
            metadata=metadata,
            field_state_id=args.field_state_id,
            run_id=args.run_id,
            ledger_index=args.ledger_index,
        )

        print(canonical_serialize(record))
        return 0

    except EKInputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
