import json
import hashlib


def _hash(data: dict) -> str:
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


def compute_phi_id(phi: dict) -> str:
    """
    Identity of Φ (structure only)
    """
    payload = {
        "Sigma": phi["Sigma"],
        "R": phi["R"]
    }
    return _hash(payload)


def compute_run_id(phi_id: str, states: list) -> str:
    """
    Identity of a simulation run
    """
    payload = {
        "phi_id": phi_id,
        "states": states
    }
    return _hash(payload)


def compute_epistemic_hash(epistemic: dict) -> str:
    """
    Hash of epistemic proof
    """
    proof = epistemic.get("proof", {})
    return _hash(proof)


def create_identity_record(run_output: dict) -> dict:
    """
    Pure identity extraction (no side effects)
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
        "topology_hash": run_output.get("topology_hash"),
        "epistemic_hash": epistemic_hash,
        "steps": len(states)
    }
