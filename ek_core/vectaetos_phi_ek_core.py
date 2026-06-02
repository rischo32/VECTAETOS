#!/usr/bin/env python3
"""
VECTAETOS — Minimal Phi / Epistemic Cryptography Core
=====================================================

Python: 3.11+
Runtime: stdlib only
Mode: deterministic, one-shot, audit-only

Boundary:
    This script takes an already-given 8x8 antisymmetric relational matrix R
    and produces external structural audit artifacts.

Allowed path:
    Φ = (Σ, R)
    R -> Δ = d1R
    R, Δ -> EK observables
    EK observables -> canonical JSON record
    record -> SHA-256 + SHA3-512
    record -> optional append-only JSONL ledger

This script does not:
    - compute truth,
    - compute K(Φ),
    - compute κ,
    - select trajectories,
    - rank trajectories,
    - control a Vortex,
    - write back into Φ,
    - mutate the supplied R,
    - create a feedback loop.

All numeric values here are audit observables only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


VERSION = "VECTAETOS_PHI_EK_MINIMAL.v0.1.0"
N = 8
DEFAULT_EPSILON = 1.0e-12
DEFAULT_TOLERANCE = 1.0e-9

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


class VectaetosInputError(ValueError):
    """Input artifact cannot be audited mechanically."""


def canonical_edges() -> list[tuple[int, int]]:
    """Canonical K8 unordered edge order: C(8,2)=28."""
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def canonical_triangles() -> list[tuple[int, int, int]]:
    """Canonical K8 unordered triangle order: C(8,3)=56."""
    return [
        (i, j, k)
        for i in range(N)
        for j in range(i + 1, N)
        for k in range(j + 1, N)
    ]


def is_finite_number(value: Any) -> bool:
    """True only for finite numeric values, excluding bool."""
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def round_float(value: float, digits: int = 15) -> float:
    """Normalize floats for stable JSON serialization."""
    if not math.isfinite(value):
        raise VectaetosInputError("non-finite audit observable")
    rounded = round(float(value), digits)
    return 0.0 if rounded == -0.0 else rounded


def require_json_safe(value: Any, name: str) -> None:
    """Ensure a value has deterministic JSON representation."""
    try:
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VectaetosInputError(f"{name} must be JSON-serializable without NaN/Infinity") from exc


def canonical_serialize(payload: Mapping[str, Any]) -> str:
    """Canonical JSON serialization used for structural fingerprints."""
    require_json_safe(payload, "payload")
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def load_json(path: Path) -> Any:
    """Load JSON from disk."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VectaetosInputError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VectaetosInputError(f"invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Write canonical pretty JSON to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    require_json_safe(payload, "payload")
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def extract_R(payload: Any) -> list[list[float]]:
    """
    Accept either:
      - raw 8x8 matrix
      - object with key "R"
    """
    candidate = payload.get("R") if isinstance(payload, Mapping) and "R" in payload else payload
    return validate_R(candidate)


def validate_R(
    R: Any,
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[list[float]]:
    """
    Validate an 8x8 antisymmetric matrix R.

    Mechanical checks only:
      - shape 8x8,
      - finite numeric values,
      - zero diagonal,
      - R_ij = -R_ji.

    This is not K(Φ).
    This is not κ.
    """
    if isinstance(R, (str, bytes)) or not isinstance(R, Sequence):
        raise VectaetosInputError("R must be a sequence of 8 numeric rows")
    if len(R) != N:
        raise VectaetosInputError(f"R must have exactly {N} rows")

    matrix: list[list[float]] = []
    for i, row in enumerate(R):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise VectaetosInputError(f"R[{i}] must be a numeric row")
        if len(row) != N:
            raise VectaetosInputError(f"R[{i}] must have exactly {N} values")
        matrix_row: list[float] = []
        for j, value in enumerate(row):
            if not is_finite_number(value):
                raise VectaetosInputError(f"R[{i}][{j}] must be a finite number")
            matrix_row.append(float(value))
        matrix.append(matrix_row)

    if tolerance < 0 or not math.isfinite(tolerance):
        raise VectaetosInputError("tolerance must be finite and non-negative")

    for i in range(N):
        if abs(matrix[i][i]) > tolerance:
            raise VectaetosInputError(f"R[{i}][{i}] must be zero within tolerance")

    for i, j in canonical_edges():
        residual = matrix[i][j] + matrix[j][i]
        if abs(residual) > tolerance:
            raise VectaetosInputError(
                f"R must be antisymmetric: R[{i}][{j}] + R[{j}][{i}] = {residual!r}"
            )

    return matrix


def sample_R() -> list[list[float]]:
    """
    Deterministic non-zero sample R in so(8).

    The values are small fixed rational-like tensions.
    No random source is used.
    """
    matrix = [[0.0 for _ in range(N)] for _ in range(N)]
    for i, j in canonical_edges():
        raw = ((i + 1) * 3 - (j + 1) * 2 + ((i + j) % 3) - 1)
        value = round(raw / 10.0, 6)
        matrix[i][j] = value
        matrix[j][i] = -value
    return matrix


def compute_delta(R: Sequence[Sequence[float]]) -> list[dict[str, Any]]:
    """Compute Δ_ijk = R_ij + R_jk + R_ki over 56 canonical K8 triangles."""
    matrix = validate_R(R)
    out: list[dict[str, Any]] = []
    for i, j, k in canonical_triangles():
        delta = matrix[i][j] + matrix[j][k] + matrix[k][i]
        out.append(
            {
                "indices": [i, j, k],
                "labels": [SIGMA_ORDER[i], SIGMA_ORDER[j], SIGMA_ORDER[k]],
                "Delta": round_float(delta),
                "abs_Delta": round_float(abs(delta)),
            }
        )
    return out


def compute_local_loads(R: Sequence[Sequence[float]]) -> tuple[list[float], float]:
    """Compute local incident load L_i and total edge load over i<j."""
    matrix = validate_R(R)
    local = [
        round_float(sum(abs(matrix[i][j]) for j in range(N) if j != i))
        for i in range(N)
    ]
    total = round_float(sum(abs(matrix[i][j]) for i, j in canonical_edges()))
    return local, total


def compute_T_EK(R: Sequence[Sequence[float]]) -> list[float]:
    """
    T_i^EK = L_i / (2 * L_total), or 0 when L_total=0.

    Audit observable only.
    """
    local, total = compute_local_loads(R)
    if total <= DEFAULT_TOLERANCE:
        return [0.0 for _ in range(N)]
    return [round_float(value / (2.0 * total)) for value in local]


def compute_chi(R: Sequence[Sequence[float]]) -> list[float]:
    """
    χ_i = average absolute Δ over triangles incident to i.

    In K8 each node is incident to C(7,2)=21 triangles.
    """
    deltas = compute_delta(R)
    chi: list[float] = []
    for center in range(N):
        values = [float(item["abs_Delta"]) for item in deltas if center in item["indices"]]
        if len(values) != 21:
            raise RuntimeError("internal K8 triangle incidence invariant failed")
        chi.append(round_float(sum(values) / 21.0))
    return chi


def compute_C_EK(chi: Sequence[float]) -> list[float]:
    """
    C_i^EK = 1/(1+χ_i).

    Audit clarity observable only.
    Not K(Φ), not safety, not κ.
    """
    if len(chi) != N:
        raise VectaetosInputError("chi must contain exactly 8 values")
    out: list[float] = []
    for i, value in enumerate(chi):
        if not is_finite_number(value):
            raise VectaetosInputError(f"chi[{i}] must be finite")
        numeric = float(value)
        if numeric < 0:
            raise VectaetosInputError(f"chi[{i}] must be non-negative")
        out.append(round_float(1.0 / (1.0 + numeric)))
    return out


def compute_mu(
    T_EK: Sequence[float],
    C_EK: Sequence[float],
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> list[float]:
    """
    μ_i = T_i^EK / (T_i^EK + C_i^EK + ε).

    Audit uncertainty observable only.
    """
    if len(T_EK) != N or len(C_EK) != N:
        raise VectaetosInputError("T_EK and C_EK must contain exactly 8 values")
    if epsilon <= 0 or not math.isfinite(epsilon):
        raise VectaetosInputError("epsilon must be finite and positive")
    out: list[float] = []
    for i, (t_value, c_value) in enumerate(zip(T_EK, C_EK, strict=True)):
        if not is_finite_number(t_value) or not is_finite_number(c_value):
            raise VectaetosInputError(f"T_EK[{i}] and C_EK[{i}] must be finite")
        t = float(t_value)
        c = float(c_value)
        if t < 0:
            raise VectaetosInputError(f"T_EK[{i}] must be non-negative")
        if c <= 0:
            raise VectaetosInputError(f"C_EK[{i}] must be positive")
        out.append(round_float(t / (t + c + epsilon)))
    return out


def compute_A_EK(mu: Sequence[float]) -> list[list[float]]:
    """
    A_ij^EK = |μ_i - μ_j|.

    Symmetric magnitude observable.
    No directional authority.
    """
    if len(mu) != N:
        raise VectaetosInputError("mu must contain exactly 8 values")
    values: list[float] = []
    for i, value in enumerate(mu):
        if not is_finite_number(value):
            raise VectaetosInputError(f"mu[{i}] must be finite")
        numeric = float(value)
        if numeric < 0:
            raise VectaetosInputError(f"mu[{i}] must be non-negative")
        values.append(numeric)

    return [
        [0.0 if i == j else round_float(abs(values[i] - values[j])) for j in range(N)]
        for i in range(N)
    ]


def compute_A_total(A_EK: Sequence[Sequence[float]]) -> float:
    """A_total^EK = sum_{i<j} A_ij^EK."""
    if len(A_EK) != N:
        raise VectaetosInputError("A_EK must have exactly 8 rows")
    total = 0.0
    for i, j in canonical_edges():
        value = A_EK[i][j]
        if not is_finite_number(value):
            raise VectaetosInputError(f"A_EK[{i}][{j}] must be finite")
        total += float(value)
    return round_float(total)


def compute_h_topo(
    mu: Sequence[float],
    A_EK: Sequence[Sequence[float]],
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> float:
    """
    h_topo = μ_total / (μ_total + A_total^EK + ε).

    Audit observable only.
    Not K(Φ), not κ, not deployment admissibility.
    """
    if epsilon <= 0 or not math.isfinite(epsilon):
        raise VectaetosInputError("epsilon must be finite and positive")
    mu_total = sum(float(x) for x in mu)
    A_total = compute_A_total(A_EK)
    denominator = mu_total + A_total + epsilon
    if denominator <= 0:
        return 0.0
    return round_float(mu_total / denominator)


def fingerprint_payload(payload: Mapping[str, Any]) -> dict[str, str]:
    """Dual fingerprint: SHA-256 and SHA3-512 over canonical JSON without fingerprint fields."""
    copied = copy.deepcopy(dict(payload))
    copied.pop("fingerprint", None)
    copied.pop("fingerprints", None)
    serialized = canonical_serialize(copied).encode("utf-8")
    return {
        "sha256": hashlib.sha256(serialized).hexdigest(),
        "sha3_512": hashlib.sha3_512(serialized).hexdigest(),
    }


def verify_fingerprint(payload: Mapping[str, Any]) -> bool:
    """Verify stored fingerprint against canonical content."""
    stored = payload.get("fingerprint")
    if not isinstance(stored, Mapping):
        return False
    expected = fingerprint_payload(payload)
    return (
        stored.get("sha256") == expected["sha256"]
        and stored.get("sha3_512") == expected["sha3_512"]
    )


def build_record(
    R: Sequence[Sequence[float]],
    *,
    metadata: Mapping[str, Any] | None = None,
    field_state_id: str | None = None,
    run_id: str | None = None,
    ledger_index: int | str | None = None,
    qe_marker: bool | None = None,
) -> dict[str, Any]:
    """Build a complete JSON-safe EK audit record from R."""
    matrix = validate_R(R)
    safe_metadata = dict(metadata or {})
    require_json_safe(safe_metadata, "metadata")

    local_loads, total_load = compute_local_loads(matrix)
    T_EK = compute_T_EK(matrix)
    delta = compute_delta(matrix)
    chi = compute_chi(matrix)
    C_EK = compute_C_EK(chi)
    mu = compute_mu(T_EK, C_EK)
    A_EK = compute_A_EK(mu)
    h_topo = compute_h_topo(mu, A_EK)

    record: dict[str, Any] = {
        "version": VERSION,
        "boundary": {
            "mode": "deterministic_audit_only",
            "phi_write_back": False,
            "vortex_control": False,
            "computes_K_phi": False,
            "computes_kappa": False,
            "selects_trajectory": False,
            "truth_authority": False,
            "safety_authority": False,
        },
        "field": {
            "Phi": "(Sigma,R)",
            "sigma_order": list(SIGMA_ORDER),
            "R": [[round_float(v) for v in row] for row in matrix],
            "R_in_so8_mechanical": True,
            "independent_relations": 28,
            "triangle_cycles": 56,
        },
        "ledger": {
            "index": ledger_index,
            "field_state_id": field_state_id,
            "run_id": run_id,
            "append_only_required": True,
        },
        "observables": {
            "local_loads": local_loads,
            "total_edge_load": total_load,
            "T_EK": T_EK,
            "Delta": delta,
            "chi": chi,
            "C_EK": C_EK,
            "mu": mu,
            "mu_total": round_float(sum(mu)),
            "A_EK": A_EK,
            "A_total_EK": compute_A_total(A_EK),
            "h_topo": h_topo,
            "qe_marker_supplied_by_upstream": qe_marker,
        },
        "metadata": safe_metadata,
    }

    record["fingerprint"] = fingerprint_payload(record)
    return record


def append_ledger(path: Path, record: Mapping[str, Any]) -> None:
    """Append a canonical JSON line. This function never rewrites existing entries."""
    path.parent.mkdir(parents=True, exist_ok=True)
    require_json_safe(record, "record")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_serialize(record) + "\n")


def read_ledger(path: Path) -> list[dict[str, Any]]:
    """Read JSONL ledger entries."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise VectaetosInputError(f"missing ledger: {path}") from exc

    entries: list[dict[str, Any]] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise VectaetosInputError(f"invalid ledger JSON at line {number}: {exc}") from exc
        if not isinstance(item, dict):
            raise VectaetosInputError(f"ledger line {number} must be an object")
        entries.append(item)
    return entries


def build_merkle_root(hashes: Sequence[str]) -> str:
    """
    Deterministic Merkle-like root over SHA-256 leaf hashes.

    For odd layers, the last node is duplicated.
    Empty ledger returns SHA-256 of empty bytes.
    """
    if not hashes:
        return hashlib.sha256(b"").hexdigest()

    layer = [bytes.fromhex(h) for h in hashes]
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        next_layer: list[bytes] = []
        for i in range(0, len(layer), 2):
            next_layer.append(hashlib.sha256(layer[i] + layer[i + 1]).digest())
        layer = next_layer
    return layer[0].hex()


def cmd_sample(args: argparse.Namespace) -> int:
    payload = {
        "R": sample_R(),
        "metadata": {
            "note": "deterministic sample R for local smoke test",
            "authority": "none",
        },
    }
    write_json(Path(args.out), payload)
    print(f"WROTE {args.out}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    payload = load_json(Path(args.input))
    matrix = extract_R(payload)
    input_metadata = payload.get("metadata", {}) if isinstance(payload, Mapping) else {}
    extra_metadata = {
        "source_file": str(args.input),
        "input_metadata": input_metadata,
    }
    record = build_record(
        matrix,
        metadata=extra_metadata,
        field_state_id=args.field_state_id,
        run_id=args.run_id,
        ledger_index=args.ledger_index,
        qe_marker=args.qe_marker,
    )
    write_json(Path(args.out), record)
    if args.ledger:
        append_ledger(Path(args.ledger), record)
    print(f"WROTE {args.out}")
    if args.ledger:
        print(f"APPENDED {args.ledger}")
    print(f"sha256={record['fingerprint']['sha256']}")
    print(f"sha3_512={record['fingerprint']['sha3_512']}")
    print(f"h_topo={record['observables']['h_topo']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    payload = load_json(Path(args.input))
    if not isinstance(payload, Mapping):
        raise VectaetosInputError("record must be a JSON object")
    ok = verify_fingerprint(payload)
    print("VALID" if ok else "INVALID")
    return 0 if ok else 2


def cmd_ledger(args: argparse.Namespace) -> int:
    entries = read_ledger(Path(args.input))
    invalid = [idx for idx, entry in enumerate(entries) if not verify_fingerprint(entry)]
    leaf_hashes = [
        entry["fingerprint"]["sha256"]
        for entry in entries
        if isinstance(entry.get("fingerprint"), Mapping)
        and isinstance(entry["fingerprint"].get("sha256"), str)
    ]
    summary = {
        "ledger": str(args.input),
        "entries": len(entries),
        "invalid_fingerprint_indices": invalid,
        "merkle_root_sha256": build_merkle_root(leaf_hashes),
    }
    if args.out:
        write_json(Path(args.out), summary)
        print(f"WROTE {args.out}")
    print(canonical_serialize(summary))
    return 0 if not invalid else 2


def cmd_selftest(_: argparse.Namespace) -> int:
    matrix = sample_R()
    record_1 = build_record(matrix, field_state_id="selftest", run_id="a", ledger_index=0)
    record_2 = build_record(matrix, field_state_id="selftest", run_id="a", ledger_index=0)

    if not verify_fingerprint(record_1):
        raise AssertionError("fingerprint verification failed")
    if record_1["fingerprint"] != record_2["fingerprint"]:
        raise AssertionError("determinism failed: fingerprints differ")
    if len(record_1["observables"]["Delta"]) != 56:
        raise AssertionError("Delta count must be 56")
    if len(record_1["observables"]["mu"]) != 8:
        raise AssertionError("mu count must be 8")
    if len(record_1["field"]["R"]) != 8:
        raise AssertionError("R row count must be 8")

    print("SELFTEST PASS")
    print(f"sha256={record_1['fingerprint']['sha256']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vectaetos_phi_ek_core.py",
        description="Minimal deterministic Phi/EK audit core for VECTAETOS.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sample = sub.add_parser("sample", help="write deterministic sample R JSON")
    p_sample.add_argument("--out", default="examples/R_sample.json")
    p_sample.set_defaults(func=cmd_sample)

    p_audit = sub.add_parser("audit", help="build EK audit record from R JSON")
    p_audit.add_argument("--input", required=True)
    p_audit.add_argument("--out", default="audit/latest_record.json")
    p_audit.add_argument("--ledger", default="audit/ledger.jsonl")
    p_audit.add_argument("--field-state-id", default=None)
    p_audit.add_argument("--run-id", default=None)
    p_audit.add_argument("--ledger-index", default=None)
    p_audit.add_argument(
        "--qe-marker",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="optional upstream QE marker to record; this script does not compute QE",
    )
    p_audit.set_defaults(func=cmd_audit)

    p_verify = sub.add_parser("verify", help="verify one JSON audit record fingerprint")
    p_verify.add_argument("--input", required=True)
    p_verify.set_defaults(func=cmd_verify)

    p_ledger = sub.add_parser("ledger", help="verify JSONL ledger and compute Merkle-like root")
    p_ledger.add_argument("--input", default="audit/ledger.jsonl")
    p_ledger.add_argument("--out", default=None)
    p_ledger.set_defaults(func=cmd_ledger)

    p_self = sub.add_parser("selftest", help="run built-in deterministic smoke test")
    p_self.set_defaults(func=cmd_selftest)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except VectaetosInputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except AssertionError as exc:
        print(f"SELFTEST FAIL: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
