# cli/run.py

import json
import requests

# CORE
from core.vortex import VectaetosSimulation, VortexConfig
from core.identity import VectaetosIdentity

# SECURITY
from core.signature import VectaetosSignature
from core.registry import VectaetosRegistry

# VNAL
from vnal.vnal_guard import validate_output, VNALViolation


# =========================
# CONFIG
# =========================

REGISTRY_PATH = "outputs/registry.jsonl"

REGISTRY_NODES = [
    "http://localhost:8001/append",
    "http://localhost:8002/append"
]


# =========================
# PROJECTION
# =========================

def project_output(raw_result):

    epistemic = raw_result.get("epistemic_cryptography", {})
    proof = epistemic.get("proof", "")
    identity = raw_result.get("identity", {})

    return {
        "type": "trajectory",
        "uncertainty": {
            "level": "derived",
            "aporia_events": len(raw_result.get("aporia_events", []))
        },
        "identity": identity,
        "proof": proof,
        "data": raw_result
    }


# =========================
# REMOTE SYNC
# =========================

def sync_to_nodes(output):

    results = []

    for node in REGISTRY_NODES:
        try:
            r = requests.post(node, json=output, timeout=2)

            results.append({
                "node": node,
                "status": r.status_code
            })

        except Exception as e:
            results.append({
                "node": node,
                "status": "ERROR",
                "error": str(e)
            })

    return results


# =========================
# MAIN
# =========================

def main():

    config = VortexConfig()
    sim = VectaetosSimulation(config)

    raw = sim.run()

    # -------------------------
    # FALLBACK IDENTITY
    # -------------------------
    if "identity" not in raw and "epistemic_cryptography" in raw:
        ep = raw["epistemic_cryptography"]

        raw["identity"] = VectaetosIdentity.validate({
            "topological_humility": ep.get("topological_humility", 0.0),
            "integrity": 1,
            "dominant_mode": False
        })

    # -------------------------
    # PROJECTION
    # -------------------------
    output = project_output(raw)

    # -------------------------
    # HASH SIGNATURE (dual)
    # -------------------------
    signature = VectaetosSignature.sign_output(output)
    output["signature"] = signature

    # -------------------------
    # LOCAL REGISTRY
    # -------------------------
    registry = VectaetosRegistry(REGISTRY_PATH)
    record = registry.append(output)

    output["registry"] = {
        "entry_hash": record["entry_hash"]
    }

    # -------------------------
    # REMOTE SYNC
    # -------------------------
    output["sync"] = sync_to_nodes(output)

    # -------------------------
    # VNAL VALIDATION
    # -------------------------
    try:
        validate_output(output)

    except VNALViolation as e:
        print(json.dumps({
            "type": "QE",
            "reason": str(e),
            "uncertainty": {"level": "max"},
            "identity": "UNKNOWN"
        }, indent=2))
        return

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    print(json.dumps(output, indent=2))


# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    main()
