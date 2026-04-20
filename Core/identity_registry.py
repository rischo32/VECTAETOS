import json
import hashlib


def _serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value):
    return hashlib.sha256(_serialize(value).encode("utf-8")).hexdigest()


def compute_phi_id(phi: dict) -> str:
    """
    Identity of Φ (structure only).
    Note: current version is order-sensitive.
    S₈ canonicalization can be added later.
    """
    return _sha256({
        "Sigma": phi["Sigma"],
        "R": phi["R"],
    })


def compute_run_id(phi_id: str, states: list) -> str:
    """
    Identity of a simulation run.
    """
    return _sha256({
        "phi_id": phi_id,
        "states": states,
    })


def compute_epistemic_hash(epistemic: dict) -> str:
    """
    Hash of epistemic proof.
    """
    return _sha256(epistemic.get("proof", {}))


def create_identity_record(run_output: dict) -> dict:
    """
    Pure identity extraction (no side effects).
    """
    phi = run_output["phi"]
    states = run_output["states"]
    epistemic = run_output.get("epistemic", {})

    phi_id = compute_phi_id(phi)
    run_id = compute_run_id(phi_id, states)
    epistemic_hash = compute_epistemic_hash(epistemic)

    return {
        "phi_id": phi_id,
        "run_id": run_id,
        "topology_hash": run_output["topology_hash"],
        "epistemic_hash": epistemic_hash,
        "steps": len(states),
    }


__all__ = [
    "compute_phi_id",
    "compute_run_id",
    "compute_epistemic_hash",
    "create_identity_record",
]
