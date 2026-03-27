"""
phi_audit.py
Φ Audit Layer — HMAC Signed Hash Chain (Mobile Stable Version)

No external dependencies.
Uses Python standard library only.
"""

import json
import os
import hashlib
import hmac
import secrets
import time


class PhiAudit:

    def __init__(self,
                 log_path="phi_log.jsonl",
                 audit_path="phi_audit.json",
                 key_path="phi_secret.key"):

        self.log_path = log_path
        self.audit_path = audit_path
        self.key_path = key_path

        self._ensure_secret_key()
        self.secret_key = self._load_secret_key()
        self.previous_chain_hash = self._load_last_chain_hash()

    # ---------------------------------------------------
    # Secret Key Management
    # ---------------------------------------------------

    def _ensure_secret_key(self):
        if not os.path.exists(self.key_path):
            key = secrets.token_bytes(32)
            with open(self.key_path, "wb") as f:
                f.write(key)
            print("[Φ-AUDIT] Secret key generated.")

    def _load_secret_key(self):
        with open(self.key_path, "rb") as f:
            return f.read()

    # ---------------------------------------------------
    # Hashing
    # ---------------------------------------------------

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def _hmac_sign(self, message: str) -> str:
        return hmac.new(
            self.secret_key,
            message.encode(),
            hashlib.sha256
        ).hexdigest()

    def _load_last_chain_hash(self):
        if not os.path.exists(self.audit_path):
            return "0" * 64

        with open(self.audit_path, "r") as f:
            data = json.load(f)
            return data.get("last_chain_hash", "0" * 64)

    # ---------------------------------------------------
    # Append Entry
    # ---------------------------------------------------

    def append_entry(self, entry: dict):

        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = self._hash(entry_json)

        chain_hash = self._hash(self.previous_chain_hash + entry_hash)
        signature = self._hmac_sign(chain_hash)

        audit_record = {
            "timestamp": int(time.time()),
            "entry_hash": entry_hash,
            "chain_hash": chain_hash,
            "signature": signature
        }

        # append log line
        with open(self.log_path, "a") as f:
            f.write(entry_json + "\n")

        # update audit state
        with open(self.audit_path, "w") as f:
            json.dump({
                "last_chain_hash": chain_hash,
                "last_signature": signature
            }, f, indent=2)

        self.previous_chain_hash = chain_hash

        return audit_record

    # ---------------------------------------------------
    # Verify Integrity
    # ---------------------------------------------------

    def verify_full_log(self):

        if not os.path.exists(self.log_path):
            return True

        previous_hash = "0" * 64

        with open(self.log_path, "r") as f:
            for line in f:
                entry = json.loads(line.strip())
                entry_json = json.dumps(entry, sort_keys=True)
                entry_hash = self._hash(entry_json)
                chain_hash = self._hash(previous_hash + entry_hash)
                previous_hash = chain_hash

        if not os.path.exists(self.audit_path):
            return False

        with open(self.audit_path, "r") as f:
            audit_data = json.load(f)

        final_chain_hash = audit_data["last_chain_hash"]
        final_signature = audit_data["last_signature"]

        expected_signature = self._hmac_sign(final_chain_hash)

        return (
            final_chain_hash == previous_hash and
            final_signature == expected_signature
        )
