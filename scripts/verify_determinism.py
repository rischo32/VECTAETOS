#!/usr/bin/env python3
"""
VECTAETOS :: Vortex Determinism Verifier

Role:
- deterministic repeatability verifier
- runs the same Vortex entrypoint twice with the same seed
- compares normalized ordered JSONL outputs
- writes runtime-only report under .runtime/determinism
- does not write to /artifacts
- does not mutate ontology, anchors, Φ, K(Φ), κ, QE, audit, or projection semantics

This verifier checks repeatability under a fixed execution configuration.
It does not claim safety, deployment validity, empirical legitimacy, or L4 evidence.

Python:
- 3.11+

Run from:
- repository root
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(".").resolve()

VORTEX_ENTRYPOINT = Path(
    os.getenv("VECTAETOS_VORTEX_ENTRYPOINT", "vortex/vortex_v2.0.py")
)

RUNTIME_DIR = ROOT / ".runtime" / "determinism"
RUN_1_PATH = RUNTIME_DIR / "run_1.jsonl"
RUN_2_PATH = RUNTIME_DIR / "run_2.jsonl"
RUN_1_NORMALIZED = RUNTIME_DIR / "run_1_normalized.json"
RUN_2_NORMALIZED = RUNTIME_DIR / "run_2_normalized.json"
REPORT_PATH = RUNTIME_DIR / "verification_report.json"

SEED = int(os.getenv("VECTAETOS_DETERMINISM_SEED", "42"))
STEPS = int(os.getenv("VECTAETOS_DETERMINISM_STEPS", "1000"))

FLOAT_PRECISION = int(os.getenv("VECTAETOS_FLOAT_PRECISION", "6"))

NONDETERMINISTIC_KEYS = {
    "timestamp",
    "time",
    "created_at",
    "updated_at",
    "elapsed",
    "duration",
    "runtime_seconds",
}


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    Parse a JSONL file into an ordered list of dictionaries.

    Order is intentionally preserved.
    Sorting would hide ordering non-determinism.
    """
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()

        if not stripped:
            continue

        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc

        if not isinstance(value, dict):
            raise ValueError(f"Expected JSON object at {path}:{line_no}")

        rows.append(value)

    return rows


def normalize(value: Any) -> Any:
    """
    Normalize output for deterministic comparison.

    - removes known runtime-only keys
    - rounds finite floats
    - preserves list order
    - sorts dictionary keys only during serialization
    """
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}

        for key, item in value.items():
            if key in NONDETERMINISTIC_KEYS:
                continue

            normalized[key] = normalize(item)

        return normalized

    if isinstance(value, list):
        return [normalize(item) for item in value]

    if isinstance(value, float):
        if math.isfinite(value):
            return round(value, FLOAT_PRECISION)
        return str(value)

    if isinstance(value, (str, int, bool)) or value is None:
        return value

    if hasattr(value, "item"):
        return normalize(value.item())

    return str(value)


def compute_sha256(value: Any) -> dict[str, Any]:
    serialized = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    payload = serialized.encode("utf-8")

    return {
        "sha256": hashlib.sha256(payload).hexdigest(),
        "serialized_size_bytes": len(payload),
    }


def ensure_entrypoint_exists() -> None:
    if not VORTEX_ENTRYPOINT.exists():
        raise FileNotFoundError(
            f"Vortex entrypoint not found: {VORTEX_ENTRYPOINT}. "
            "Set VECTAETOS_VORTEX_ENTRYPOINT if the canonical entrypoint moved."
        )


def run_vortex(output_path: Path) -> None:
    """
    Run the configured Vortex entrypoint.

    This assumes the entrypoint supports:
    --seed, --steps, --output, --quiet
    """
    if output_path.exists():
        output_path.unlink()

    cmd = [
        sys.executable,
        str(VORTEX_ENTRYPOINT),
        "--seed",
        str(SEED),
        "--steps",
        str(STEPS),
        "--output",
        str(output_path),
        "--quiet",
    ]

    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"

    print(f"[DETERMINISM] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=env)

    if not output_path.exists():
        raise FileNotFoundError(f"Expected output was not produced: {output_path}")


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ensure_entrypoint_exists()

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    print("[DETERMINISM] Starting deterministic repeatability check")
    print(f"[DETERMINISM] entrypoint={VORTEX_ENTRYPOINT}")
    print(f"[DETERMINISM] seed={SEED}")
    print(f"[DETERMINISM] steps={STEPS}")
    print(f"[DETERMINISM] output_dir={RUNTIME_DIR}")

    run_vortex(RUN_1_PATH)
    run_vortex(RUN_2_PATH)

    run_1_raw = parse_jsonl(RUN_1_PATH)
    run_2_raw = parse_jsonl(RUN_2_PATH)

    run_1_normalized = normalize(run_1_raw)
    run_2_normalized = normalize(run_2_raw)

    run_1_hash = compute_sha256(run_1_normalized)
    run_2_hash = compute_sha256(run_2_normalized)

    deterministic = run_1_hash == run_2_hash

    write_json(RUN_1_NORMALIZED, run_1_normalized)
    write_json(RUN_2_NORMALIZED, run_2_normalized)

    report = {
        "role": "vortex_determinism_repeatability_report",
        "entrypoint": str(VORTEX_ENTRYPOINT),
        "seed": SEED,
        "steps": STEPS,
        "float_precision": FLOAT_PRECISION,
        "runtime_only": True,
        "writes_artifacts_directory": False,
        "safety_claim": False,
        "deployment_claim": False,
        "l4_claim": False,
        "records_run_1": len(run_1_raw),
        "records_run_2": len(run_2_raw),
        "run_1": run_1_hash,
        "run_2": run_2_hash,
        "deterministic": deterministic,
    }

    write_json(REPORT_PATH, report)

    if not deterministic:
        print("[DETERMINISM] FAILED")
        print(f"  Run 1 SHA256: {run_1_hash['sha256']}")
        print(f"  Run 2 SHA256: {run_2_hash['sha256']}")
        print(f"  Records run 1: {len(run_1_raw)}")
        print(f"  Records run 2: {len(run_2_raw)}")
        print(f"  Report: {REPORT_PATH}")
        return 1

    print("[DETERMINISM] PASS")
    print(f"  SHA256: {run_1_hash['sha256']}")
    print(f"  Records: {len(run_1_raw)}")
    print(f"  Report: {REPORT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
