# cli/run.py
"""
VECTAETOS CLI runner.

Boundary:
- This module is an execution/projection adapter.
- It must not redefine Φ, mutate ontology, optimize trajectories, or treat signatures,
  registry hashes, or ontology bindings as truth.
- Side effects are ordered after VNAL validation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - only used in minimal deployments
    requests = None  # type: ignore[assignment]

# CORE
from core.vortex import VectaetosSimulation, VortexConfig
from core.identity import VectaetosIdentity
from core.ontology_binding import OntologyBinding

# SECURITY
from core.signature import VectaetosSignature
from core.registry import VectaetosRegistry

# VNAL
from vnal.vnal_guard import validate_output, VNALViolation


# =========================
# CONFIG
# =========================

REGISTRY_PATH = "outputs/registry.jsonl"
ONTOLOGY_HASH_PATH = "ontology_hash.json"

REGISTRY_NODES = [
    "http://localhost:8001/append",
    "http://localhost:8002/append",
]


# =========================
# JSON OUTPUT
# =========================

def emit_json(payload: dict[str, Any]) -> None:
    """Emit deterministic human-readable JSON."""
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def emit_qe(reason: str, *, stage: str) -> None:
    """Emit a non-authoritative QE report and stop the run."""
    emit_json({
        "type": "QE",
        "stage": stage,
        "reason": reason,
        "uncertainty": {"level": "max"},
        "identity": "UNKNOWN",
    })


# =========================
# PROJECTION
# =========================

def project_output(raw_result: dict[str, Any]) -> dict[str, Any]:
    """Project raw Vortex output into a serializable report structure."""
    epistemic = raw_result.get("epistemic_cryptography", {})
    proof = epistemic.get("proof", "")
    identity = raw_result.get("identity", {})

    return {
        "type": "trajectory",
        "uncertainty": {
            "level": "derived",
            "aporia_events": len(raw_result.get("aporia_events", [])),
        },
        "identity": identity,
        "proof": proof,
        "data": raw_result,
    }


def ensure_identity(raw_result: dict[str, Any]) -> dict[str, Any]:
    """
    Add fallback identity only when the simulation returned epistemic data
    but no identity block.

    This is descriptive normalization, not identity authority.
    """
    if "identity" not in raw_result and "epistemic_cryptography" in raw_result:
        ep = raw_result["epistemic_cryptography"]

        raw_result["identity"] = VectaetosIdentity.validate({
            "topological_humility": ep.get("topological_humility", 0.0),
            "integrity": 1,
            "dominant_mode": False,
        })

    return raw_result


def attach_ontology_binding(
    output: dict[str, Any],
    *,
    ontology_hash_path: str = ONTOLOGY_HASH_PATH,
) -> dict[str, Any]:
    """
    Attach ontology binding after projection, when output["proof"] exists.

    The binding is provenance / integrity evidence only. It is not truth,
    interpretation, or authority.
    """
    proof = output.get("proof")
    if not proof:
        raise ValueError("Cannot bind ontology: output proof is missing.")

    binder = OntologyBinding(ontology_hash_path)
    output["ontology_binding"] = binder.bind(proof)
    return output


# =========================
# REMOTE SYNC
# =========================

def sync_to_nodes(output: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Best-effort remote sync.

    Sync errors are represented in the report. They must not feed back into Φ
    or retroactively alter the projected trajectory.
    """
    results: list[dict[str, Any]] = []

    if requests is None:
        return [
            {
                "node": node,
                "status": "SKIPPED",
                "error": "requests is not installed",
            }
            for node in REGISTRY_NODES
        ]

    for node in REGISTRY_NODES:
        try:
            response = requests.post(node, json=output, timeout=2)
            results.append({
                "node": node,
                "status": response.status_code,
            })
        except requests.RequestException as exc:
            results.append({
                "node": node,
                "status": "ERROR",
                "error": str(exc),
            })

    return results


# =========================
# MAIN
# =========================

def main() -> None:
    try:
        config = VortexConfig()
        sim = VectaetosSimulation(config)

        raw = sim.run()
        if not isinstance(raw, dict):
            emit_qe("Simulation returned non-dict output.", stage="simulation")
            return

        # -------------------------
        # NORMALIZATION
        # -------------------------
        raw = ensure_identity(raw)

        # -------------------------
        # PROJECTION
        # -------------------------
        output = project_output(raw)

        # -------------------------
        # ONTOLOGY BINDING
        # -------------------------
        output = attach_ontology_binding(output)

        # -------------------------
        # VNAL VALIDATION
        # Must happen before registry writes or remote sync.
        # -------------------------
        validate_output(output)

        # -------------------------
        # HASH SIGNATURE
        # Signature is integrity/provenance evidence, not truth.
        # -------------------------
        output["signature"] = VectaetosSignature.sign_output(output)

        # -------------------------
        # LOCAL REGISTRY
        # Logging happens only after successful validation.
        # -------------------------
        Path(REGISTRY_PATH).parent.mkdir(parents=True, exist_ok=True)
        registry = VectaetosRegistry(REGISTRY_PATH)
        record = registry.append(output)

        output["registry"] = {
            "entry_hash": record["entry_hash"],
        }

        # -------------------------
        # REMOTE SYNC
        # Best-effort side effect after validation and local registry.
        # -------------------------
        output["sync"] = sync_to_nodes(output)

        # -------------------------
        # FINAL OUTPUT
        # -------------------------
        emit_json(output)

    except VNALViolation as exc:
        emit_qe(str(exc), stage="vnal_validation")
    except Exception as exc:
        # Fail closed: expose boundary instead of emitting a partial authoritative result.
        emit_qe(str(exc), stage="runtime")


# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    main()
    
