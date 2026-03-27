# -------------------------------------------
# Φ LOGGER — Hash-chained structural log
# -------------------------------------------

import json
import hashlib
import time
from pathlib import Path

LOG_FILE = Path("phi_log.jsonl")

_previous_hash = None


def _compute_hash(data, prev_hash):
    raw = json.dumps(data, sort_keys=True).encode()
    base = raw + (prev_hash.encode() if prev_hash else b"")
    return hashlib.sha256(base).hexdigest()


def log_event(event_type, payload):
    global _previous_hash

    entry = {
        "timestamp": time.time(),
        "event": event_type,
        "payload": payload,
    }

    entry_hash = _compute_hash(entry, _previous_hash)

    entry["hash"] = entry_hash
    entry["prev_hash"] = _previous_hash

    _previous_hash = entry_hash

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
