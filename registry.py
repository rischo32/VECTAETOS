import hashlib
import json


def _read_field(value, name):
    if isinstance(value, dict):
        return value[name]
    return getattr(value, name)


def _serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_payload(payload):
    return hashlib.sha256(_serialize(payload).encode("utf-8")).hexdigest()


def _sha256_value(value):
    if isinstance(value, str):
        data = value.encode("utf-8")
    elif isinstance(value, (bytes, bytearray)):
        data = bytes(value)
    else:
        data = _serialize(value).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def compute_phi_id(phi):
    sigma = _read_field(phi, "Sigma")
    matrix = _read_field(phi, "R")
    return _sha256_payload({"Sigma": sigma, "R": matrix})


def compute_run_id(phi_id, states):
    return _sha256_payload({"phi_id": phi_id, "states": states})


def create_registry_entry(run_output):
    phi = _read_field(run_output, "phi")
    states = _read_field(run_output, "states")
    epistemic = _read_field(run_output, "epistemic")
    proof = _read_field(epistemic, "proof")

    phi_id = compute_phi_id(phi)
    run_id = compute_run_id(phi_id, states)

    return {
        "phi_id": phi_id,
        "run_id": run_id,
        "topology_hash": _read_field(run_output, "topology_hash"),
        "epistemic_hash": _sha256_value(proof),
        "steps": len(states),
    }


__all__ = ["compute_phi_id", "compute_run_id", "create_registry_entry"]
