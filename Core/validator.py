# core/validator.py

import json

from core.proof import CanonicalIdentityProof
from core.identity import VectaetosIdentity
from core.signature import VectaetosSignature


class ValidationResult:
    def __init__(self, valid: bool, reason: str, details: dict = None):
        self.valid = valid
        self.reason = reason
        self.details = details or {}

    def to_dict(self):
        return {
            "valid": self.valid,
            "reason": self.reason,
            "details": self.details
        }


class VectaetosValidator:

    @classmethod
    def validate(cls, output: dict) -> ValidationResult:

        try:
            if "data" not in output:
                return ValidationResult(False, "missing data")

            if "proof" not in output:
                return ValidationResult(False, "missing proof")

            if "identity" not in output:
                return ValidationResult(False, "missing identity")

            data = output["data"]
            proof_given = output["proof"]
            identity_given = output["identity"]

            # -------------------------
            # STATE
            # -------------------------
            state = data.get("final_state", [])
            if not state:
                return ValidationResult(False, "missing state")

            # -------------------------
            # REBUILD A
            # -------------------------
            A = cls._rebuild_A(state)

            # -------------------------
            # EPISTEMIC
            # -------------------------
            ep = {
                "topological_humility": data.get("epistemic_cryptography", {}).get("topological_humility", 0.0),
                "integrity": 1,
                "dominant_mode": False
            }

            # -------------------------
            # PROOF CHECK
            # -------------------------
            proof_expected = CanonicalIdentityProof.compute_proof(A, ep)

            if proof_expected != proof_given:
                return ValidationResult(False, "proof mismatch")

            # -------------------------
            # IDENTITY CHECK
            # -------------------------
            identity_expected = VectaetosIdentity.validate(ep)

            if identity_expected != identity_given:
                return ValidationResult(False, "identity mismatch")

            # -------------------------
            # SIGNATURE CHECK
            # -------------------------
            if "signature" in output:
                if not VectaetosSignature.verify_output(output, output["signature"]):
                    return ValidationResult(False, "invalid hash signature")

            return ValidationResult(True, "valid")

        except Exception as e:
            return ValidationResult(False, str(e))

    @staticmethod
    def _rebuild_A(poles):
        n = len(poles)
        A = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                Ti = poles[i].get("T", 0.0)
                Tj = poles[j].get("T", 0.0)
                Ci = poles[i].get("C", 0.0)
                Cj = poles[j].get("C", 0.0)

                val = abs(Ti - Tj) * ((Ci + Cj) / 2.0)

                A[i][j] = val
                A[j][i] = -val

        return A


def validate_file(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    result = VectaetosValidator.validate(data)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python core/validator.py file.json")
        exit(1)

    validate_file(sys.argv[1])
