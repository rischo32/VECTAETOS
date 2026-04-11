# core/registry.py

import json
import hashlib
import time
from pathlib import Path


class VectaetosRegistry:

    def __init__(self, path="registry.jsonl"):
        self.path = Path(path)

        if not self.path.exists():
            self.path.touch()

    # =========================
    # HASH
    # =========================
    @staticmethod
    def _hash(data: dict) -> str:
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode()).hexdigest()

    # =========================
    # GET LAST HASH
    # =========================
    def _last_hash(self) -> str:
        try:
            with open(self.path, "r") as f:
                lines = f.readlines()
                if not lines:
                    return "GENESIS"
                last = json.loads(lines[-1])
                return last.get("entry_hash", "GENESIS")
        except Exception:
            return "GENESIS"

    # =========================
    # APPEND
    # =========================
    def append(self, output: dict) -> dict:
        """
        Append new entry to registry
        """

        prev_hash = self._last_hash()

        entry = {
            "timestamp": time.time(),
            "proof": output.get("proof"),
            "identity": output.get("identity"),
            "signature": output.get("signature"),
            "prev_hash": prev_hash
        }

        entry_hash = self._hash(entry)

        record = {
            "entry": entry,
            "entry_hash": entry_hash
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")

        return record

    # =========================
    # VERIFY CHAIN
    # =========================
    def verify(self) -> bool:
        """
        Verify entire chain integrity
        """

        prev_hash = "GENESIS"

        with open(self.path, "r") as f:
            for line in f:
                record = json.loads(line)

                entry = record["entry"]
                entry_hash = record["entry_hash"]

                # check linkage
                if entry["prev_hash"] != prev_hash:
                    return False

                # recompute hash
                expected_hash = self._hash(entry)

                if expected_hash != entry_hash:
                    return False

                prev_hash = entry_hash

        return True

    # =========================
    # SUMMARY
    # =========================
    def summary(self) -> dict:
        count = 0
        last_hash = "GENESIS"

        with open(self.path, "r") as f:
            for line in f:
                record = json.loads(line)
                last_hash = record["entry_hash"]
                count += 1

        return {
            "entries": count,
            "last_hash": last_hash
        }
