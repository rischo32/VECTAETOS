# cli_guard.py

import json
import sys

from vnal_guard import validate_output, VNALViolation


def run_guard(raw_output):
    try:
        output = json.loads(raw_output)
    except Exception:
        raise Exception("Invalid JSON output")

    try:
        validate_output(output)
    except VNALViolation as e:
        print(f"[GUARD BLOCKED] {str(e)}")
        sys.exit(1)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    raw = sys.stdin.read()
    run_guard(raw)
