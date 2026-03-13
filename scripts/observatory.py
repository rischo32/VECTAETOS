import json
from datetime import datetime
from pathlib import Path

status_file = Path("field_status.json")
history_file = Path("observatory_history.json")

if not status_file.exists():
    print("No field_status.json")
    exit()

status = json.load(open(status_file))

entry = {
    "time": datetime.utcnow().isoformat(),
    "h_topo": status["h_topo_mean"],
    "qe": status["qe_total"],
    "triality": status["triality_ok"]
}

if history_file.exists():
    history = json.load(open(history_file))
else:
    history = []

history.append(entry)

with open(history_file,"w") as f:
    json.dump(history,f,indent=2)

print("Observatory updated")
