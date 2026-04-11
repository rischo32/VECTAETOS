# core/signature.py

import json
import hashlib
import base64


class VectaetosSignature:

    @staticmethod
    def _canonical_payload(output: dict) -> bytes:
        payload = dict(output)
        payload.pop("signature", None)

        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        return serialized

    @staticmethod
    def sign_output(output: dict) -> dict:
        """
        Hash-based signature (dual hash)
        """

        message = VectaetosSignature._canonical_payload(output)

        sha256 = hashlib.sha256(message).digest()
        sha3 = hashlib.sha3_256(message).digest()

        return {
            "sha256": base64.b64encode(sha256).decode(),
            "sha3_256": base64.b64encode(sha3).decode()
        }

    @staticmethod
    def verify_output(output: dict, signature: dict) -> bool:

        expected = VectaetosSignature.sign_output(output)

        return (
            expected["sha256"] == signature.get("sha256") and
            expected["sha3_256"] == signature.get("sha3_256")
        )
