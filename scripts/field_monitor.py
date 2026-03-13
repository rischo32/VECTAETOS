import json
import glob
from statistics import mean

files = glob.glob("vortex_*.json")

if not files:
    print("No vortex outputs found")
    exit()

h_values = []
qe_events = []
triality = []

for f in files:
    data = json.load(open(f))

    h_values.append(data["epistemic"]["topological_humility"])
    qe_events.append(data["events"]["qe_aporia"])
    triality.append(data["epistemic"]["triality_preserved"])

report = {
    "runs": len(files),
    "h_topo_mean": mean(h_values),
    "qe_total": sum(qe_events),
    "triality_ok": all(triality)
}

with open("field_status.json","w") as f:
    json.dump(report,f,indent=2)

print("Field status written")
print(report)
