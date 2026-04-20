import hashlib
import json

from core.vortex_pipeline import Phi, compute_epistemic, sample_sigma, topology_hash, vortex


def _serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value):
    return hashlib.sha256(_serialize(value).encode("utf-8")).hexdigest()


def extract_replay_config(run_output: dict) -> dict:
    """
    Extract minimal deterministic replay config.
    Requires canonical run() output with:
    - seed
    - phi
    - states
    """
    if "seed" not in run_output:
        raise KeyError("run_output['seed'] is required for deterministic replay")

    return {
        "seed": int(run_output["seed"]),
        "steps": len(run_output["states"]),
        "phi": {
            "Sigma": tuple(run_output["phi"]["Sigma"]),
            "R": run_output["phi"]["R"],
        },
    }


def replay_run(config: dict) -> dict:
    """
    Deterministic replay using canonical core logic only.
    """
    seed = int(config["seed"])
    steps = int(config["steps"])
    phi_data = config["phi"]

    phi = Phi(
        Sigma=tuple(phi_data["Sigma"]),
        R=phi_data["R"],
    )

    sigma = sample_sigma(seed=seed)
    states = vortex(phi, sigma, steps, seed)
    epistemic = compute_epistemic(states, phi.R)

    return {
        "seed": seed,
        "phi": {
            "Sigma": phi.Sigma,
            "R": phi.R,
        },
        "states": states,
        "epistemic": epistemic,
        "topology_hash": topology_hash(phi.R),
    }


def verify_replay(original: dict, replayed: dict) -> bool:
    """
    Exact structural equality via canonical hash.
    """
    return _sha256(original) == _sha256(replayed)
