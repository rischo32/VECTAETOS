# core/ontology_binding.py

import json
import hashlib
import base64


class OntologyBinding:

    def __init__(self, ontology_file="ontology_hash.json"):
        with open(ontology_file, "r") as f:
            self.ontology = json.load(f)

    # =========================
    # EXTRACT ROOT
    # =========================
    def root_hash(self):
        return self.ontology["root_hash"]

    # =========================
    # BIND PROOF
    # =========================
    def bind(self, proof: str) -> dict:
        """
        Combine proof with ontology root
        """

        root = self.root_hash()

        payload = {
            "proof": proof,
            "ontology_root": root
        }

        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

        return {
            "sha256": base64.b64encode(hashlib.sha256(serialized).digest()).decode(),
            "sha3_256": base64.b64encode(hashlib.sha3_256(serialized).digest()).decode()
        }

    # =========================
    # VERIFY BINDING
    # =========================
    def verify(self, proof: str, binding: dict) -> bool:
        expected = self.bind(proof)

        return (
            expected["sha256"] == binding.get("sha256") and
            expected["sha3_256"] == binding.get("sha3_256")
        )
