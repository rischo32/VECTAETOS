# cli/run.py

import json

# CORE (FINAL)
from core.vortex import VectaetosSimulation, VortexConfig
from core.identity import VectaetosIdentity
from core.proof import CanonicalIdentityProof

# VNAL
from vnal.vnal_guard import validate_output, VNALViolation


# =========================
# PROJECTION
# =========================

def project_output(raw_result):
    """
    VNAL projection layer
    """

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
# MAIN
# =========================

def main():

    # CONFIG
    config = VortexConfig()

    # SIMULATION
    sim = VectaetosSimulation(config)
    raw = sim.run()

    # =========================
    # EXTRA SAFETY (RE-CHECK)
    # =========================

    # ak nie je identity vrátená z core (fallback)
    if "identity" not in raw and "epistemic_cryptography" in raw:
        ep = raw["epistemic_cryptography"]

        identity = VectaetosIdentity.validate({
            "topological_humility": ep.get("topological_humility", 0.0),
            "integrity": 1,
            "dominant_mode": False
        })

        raw["identity"] = identity

    # =========================
    # PROJECTION
    # =========================

    output = project_output(raw)

    # =========================
    # VNAL VALIDATION
    # =========================

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

    # =========================
    # FINAL OUTPUT
    # =========================

    print(json.dumps(output, indent=2))


# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    main()
