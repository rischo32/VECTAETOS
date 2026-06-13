#!/usr/bin/env bash
set -euo pipefail

GUARD_ID="${1:?Usage: $0 <guard_id> [target_file]}"
TARGET_FILE="${2:-}"

export PYTHONPATH="${PWD}/guards"

python3 -c "
from core.sealed_loader import execute_guard_sealed
import sys

PUBLIC_KEY_HEX = '$(cat guards/config/public_key.hex)'  # 64 hex chars

result = execute_guard_sealed(
    guard_id='${GUARD_ID}',
    target_file='${TARGET_FILE}',
    repo_root='${PWD}',
    public_key_hex=PUBLIC_KEY_HEX,
)

print(result.output)

if not result.success:
    print(f'\nSECURITY VIOLATIONS:', file=sys.stderr)
    for v in result.security_violations:
        print(f'  [{v.layer}] {v.violation_type}: {v}', file=sys.stderr)
    
    sys.exit(result.exit_code)
else:
    sys.exit(result.exit_code)
"
