#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Deterministic stdlib-only smoke mode.
# -S disables automatic import of the site module.
# PYTHONPATH is cleared so local/system path leakage is not silently accepted.
PYTHON_BIN="${PYTHON_BIN:-python3}"
PY=("$PYTHON_BIN" "-S")

export PYTHONNOUSERSITE=1
unset PYTHONPATH

mkdir -p examples audit

"${PY[@]}" vectaetos_phi_ek_core.py selftest

"${PY[@]}" vectaetos_phi_ek_core.py sample \
  --out examples/R_sample.json

"${PY[@]}" vectaetos_phi_ek_core.py audit \
  --input examples/R_sample.json \
  --out audit/latest_record.json \
  --ledger audit/ledger.jsonl \
  --field-state-id local-phi-001 \
  --run-id local-smoke-001 \
  --ledger-index 0

"${PY[@]}" vectaetos_phi_ek_core.py verify \
  --input audit/latest_record.json

"${PY[@]}" vectaetos_phi_ek_core.py ledger \
  --input audit/ledger.jsonl \
  --out audit/ledger_summary.json
