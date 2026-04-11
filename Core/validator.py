# core/validator.py

import json

from core.proof import CanonicalIdentityProof
from core.identity import VectaetosIdentity


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

    # =========================
    # MAIN VALIDATION
    # =========================
    @classmethod
    def validate(cls, output: dict) -> ValidationResult:
        """
        Validate full Vectaetos output
        """

        try:
            # -------------------------
            # BASIC STRUCTURE
            # -------------------------
            if "data" not in output:
                return ValidationResult(False, "missing data field")

            if "proof" not in output:
                return ValidationResult(False, "missing proof")

            if "identity" not in output:
                return ValidationResult(False, "missing identity")

            data = output["data"]
            proof_given = output["proof"]
            identity_given = output["identity"]

            # -------------------------
            # EXTRACT STATE
            # -------------------------
            epistemic = data.get("epistemic_cryptography", {})

            if "last_state" in data:
                state = data["last_state"]
            else:
                state = data.get("final_state", [])

            if not state:
                return ValidationResult(False, "missing state")

            # -------------------------
            # REBUILD MATRIX A
            # -------------------------
            try:
                A = cls._rebuild_A(state)
            except Exception as e:
                return ValidationResult(False, f"A reconstruction failed: {str(e)}")

            # -------------------------
            # REBUILD EPISTEMIC
            # -------------------------
            ep = cls._rebuild_epistemic(epistemic)

            # -------------------------
            # RECOMPUTE PROOF
            # -------------------------
            proof_expected = CanonicalIdentityProof.compute_proof(A, ep)

            if proof_expected != proof_given:
                return ValidationResult(False, "proof mismatch", {
                    "expected": proof_expected,
                    "given": proof_given
                })

            # -------------------------
            # VALIDATE IDENTITY
            # -------------------------
            identity_expected = VectaetosIdentity.validate(ep)

            if isinstance(identity_given, dict):
                identity_given_status = identity_given.get("status", identity_given)
            else:
                identity_given_status = identity_given

            if identity_expected != identity_given_status:
                return ValidationResult(False, "identity mismatch", {
                    "expected": identity_expected,
                    "given": identity_given_status
                })

            # -------------------------
            # SUCCESS
            # -------------------------
            return ValidationResult(True, "valid vectaetos output")

        except Exception as e:
            return ValidationResult(False, f"validation error: {str(e)}")

    # =========================
    # HELPERS
    # =========================

    @staticmethod
    def _rebuild_A(poles):
        """
        Reconstruct relational matrix A from poles
        """
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

    @staticmethod
    def _rebuild_epistemic(ep):
        """
        Extract minimal epistemic identity
        """
        return {
            "topological_humility": ep.get("topological_humility", 0.0),
            "integrity": ep.get("integrity", 1),
            "dominant_mode": ep.get("dominant_mode", False)
        }


# =========================
# CLI HELPER
# =========================

def validate_file(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    result = VectaetosValidator.validate(data)

    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python core/validator.py <file.json>")
        sys.exit(1)

    validate_file(sys.argv[1])
