import json
from vortex.vortex_unified_v3 import VectaetosSimulation, VortexConfig
from vnal.vnal_guard import validate_output, VNALViolation


def project_output(raw_result):
    # transformácia na VNAL formát
    return {
        "type": "trajectory",
        "uncertainty": {
            "level": "derived",
            "aporia_events": len(raw_result.get("aporia_events", []))
        },
        "data": raw_result
    }


def main():
    config = VortexConfig()
    sim = VectaetosSimulation(config)

    raw = sim.run()
    output = project_output(raw)

    try:
        validate_output(output)
    except VNALViolation as e:
        print(json.dumps({
            "type": "QE",
            "reason": str(e),
            "uncertainty": {"level": "max"}
        }, indent=2))
        return

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
