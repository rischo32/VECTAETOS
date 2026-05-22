import json
import hashlib

from core.vortex_pipeline import construct_phi, sample_sigma, vortex


def _serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value):
    return hashlib.sha256(_serialize(value).encode("utf-8")).hexdigest()


def extract_replay_config(run_output: dict) -> dict:
    """
    Deterministic config extraction
    """

    return {
        "seed": run_output["seed"],
        "steps": len(run_output["states"]),
        "phi": run_output["phi"]
    }


def replay_run(config: dict) -> dict:
    """
    Deterministic replay using core logic
    """

    seed = config["seed"]
    steps = config["steps"]
    phi_data = config["phi"]

    # reconstruct Phi
    phi = construct_phi(seed=seed)

    # enforce exact R
    phi.R = phi_data["R"]

    # initial state
    sigma = sample_sigma(seed=seed)

    # run vortex (NO custom logic!)
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
    Exact hash match
    """

    return _sha256(original["states"]) == _sha256(replayed["states"])
