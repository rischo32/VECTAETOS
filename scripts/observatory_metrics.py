import json

INPUT_FILE = "observatory_output.json"
OUTPUT_FILE = "observatory_metrics.json"

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

        poles = data.get("poles", [])
        epistemic = data.get("epistemic", {})

        metrics = {
            "num_poles": len(poles),
            "topological_humility": epistemic.get("topological_humility", 0),
            "dominant_mode": epistemic.get("dominant_mode", False),
            "triality_preserved": epistemic.get("triality_preserved", None),
            "total_asymmetry": epistemic.get("total_asymmetry", 0)
        }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(metrics, f, indent=2)

        print("Observatory metrics generated")

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
