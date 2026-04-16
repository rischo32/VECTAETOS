import json
import hashlib

from core.vortex_pipeline import construct_phi, sample_sigma, vortex


def _serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value):
    return hashlib.sha256(_serialize(value).encode("utf-8")).hexdigest()


def extract_replay_config(run_output: dict) -> dict:
    """
    Extract minimal deterministic config
    """

    return {
        "seed": run_output.get("seed"),
        "steps": len(run_output.get("states", [])),
        "phi": run_output.get("phi")
    }


def replay_run(config: dict) -> dict:
    """
    Deterministic replay
    """

    seed = config["seed"]
    steps = config["steps"]
    phi_data = config["phi"]

    # reconstruct Phi exactly
    phi = construct_phi(seed=seed)
    phi.R = phi_data["R"]  # enforce identical structure

    sigma = sample_sigma(seed=seed)
    states = vortex(phi, sigma, steps)

    return {
        "phi": {
            "Sigma": phi.Sigma,
            "R": phi.R
        },
        "states": states
    }


def verify_replay(original: dict, replayed: dict) -> bool:
    """
    Verify exact match
    """

    return _sha256(original["states"]) == _sha256(replayed["states"])
