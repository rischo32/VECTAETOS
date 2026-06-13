# VECTAETOS CLI

## Status

```text
candidate / execution-projection adapter
```

The `/cli/` layer is a terminal-facing adapter for running a bounded VECTAETOS projection pipeline.

It is not an agent.

It is not an optimizer.

It is not a truth engine.

It is not a deployment validator.

It is not an ontological authority.

---

## Purpose

The CLI exists to provide a minimal command-line entry point for the current VECTAETOS runtime/projection path.

Its role is to:

```text
run simulation/projection
normalize output shape
attach ontology binding as provenance
validate output boundary through VNAL
attach integrity signature
append local registry record
optionally attempt remote sync
emit final JSON
```

The CLI must remain downstream of the ontology.

It must not redefine:

```text
Φ
K(Φ)
κ
QE
Σ₁...Σ₈
Vortex role
EK / audit role
projection role
LLM role
```

---

## Entry Point

```text
cli/run.py
```

Run from repository root:

```bash
python3 cli/run.py
```

Recommended controlled form:

```bash
export PYTHONNOUSERSITE=1
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

python3 cli/run.py
```

Minimal syntax check:

```bash
python3 -m py_compile cli/run.py
```

---

## Current Pipeline

The current `cli/run.py` flow is:

```text
VortexConfig()
    ↓
VectaetosSimulation(config)
    ↓
sim.run()
    ↓
ensure_identity(raw)
    ↓
project_output(raw)
    ↓
attach_ontology_binding(output)
    ↓
validate_output(output)
    ↓
VectaetosSignature.sign_output(output)
    ↓
VectaetosRegistry.append(output)
    ↓
sync_to_nodes(output)
    ↓
emit_json(output)
```

The ordering matters.

Validation must happen before registry write or remote sync.

Registry and sync are side effects after validation.

If a runtime boundary is hit, the CLI emits a QE-shaped JSON report instead of partial authoritative output.

---

## Output Shape

The normal projected output has the form:

```json
{
  "type": "trajectory",
  "uncertainty": {
    "level": "derived",
    "aporia_events": 0
  },
  "identity": "...",
  "proof": "...",
  "data": {},
  "ontology_binding": {},
  "signature": {},
  "registry": {
    "entry_hash": "..."
  },
  "sync": []
}
```

The QE/fail-closed output has the form:

```json
{
  "type": "QE",
  "stage": "runtime",
  "reason": "...",
  "uncertainty": {
    "level": "max"
  },
  "identity": "UNKNOWN"
}
```

QE here is a boundary exposure.

It is not an exception-as-truth.

It is not a fallback answer.

---

## Runtime Files

Current defaults:

```text
outputs/registry.jsonl
ontology_hash.json
```

The registry is a provenance chain.

It is not truth.

It is not empirical validation.

It is not deployment admissibility.

Recommended `.gitignore` policy:

```gitignore
# CLI runtime outputs
outputs/*.jsonl
outputs/*.json
```

If curated fixtures are needed, store them under a dedicated sample directory, for example:

```text
outputs/samples/
```

and mark them explicitly as examples.

---

## Remote Sync

Current default nodes:

```text
http://localhost:8001/append
http://localhost:8002/append
```

Remote sync is best-effort.

Sync failure must remain inside the report.

Sync failure must not:

```text
feed back into Φ
alter the projected trajectory
change registry history
force a retry loop
create authority
```

If the optional `requests` package is missing, sync should be reported as skipped.

---

## Boundary Rules

The CLI may:

```text
emit JSON
normalize projected output
attach provenance binding
attach integrity signature
append registry record after validation
attempt best-effort remote sync
emit QE-shaped boundary reports
```

The CLI must not:

```text
optimize trajectories
select the best trajectory
recommend an action
maximize coherence
treat signatures as truth
treat registry hashes as truth
treat ontology binding as authority
treat h_topo or EK observables as scores
write back into Φ
create a feedback loop
turn audit into command
turn projection into interpretation
```

---

## Current Implementation Note

The current `cli/run.py` imports packages using lowercase paths such as:

```python
from core.vortex import VectaetosSimulation, VortexConfig
from core.identity import VectaetosIdentity
from core.ontology_binding import OntologyBinding
from core.signature import VectaetosSignature
from core.registry import VectaetosRegistry
from vnal.vnal_guard import validate_output, VNALViolation
```

On Linux, path casing matters.

If repository modules exist as `Core/` or `VNAL/`, this CLI may require an import-path patch before canonical CI use.

Recommended future fix:

```text
either normalize package directories to lowercase core/ and vnal/
or update cli/run.py imports to match repository paths
or add a compatibility adapter with explicit tests
```

Do not hide this behind `PYTHONPATH`.

The import boundary should be explicit and deterministic.

---

## Local Troubleshooting

### 1. ModuleNotFoundError: core

Likely cause:

```text
package path mismatch or missing PYTHONPATH
```

Check:

```bash
ls core Core
```

Then either run with:

```bash
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
```

or patch imports/directories consistently.

### 2. Missing ontology_hash.json

The ontology binding step expects:

```text
ontology_hash.json
```

If this file is absent, the CLI should fail closed into QE-shaped output.

### 3. requests is not installed

Remote sync is optional.

The CLI should still produce a local report with sync marked as skipped.

### 4. Registry path missing

The CLI creates:

```text
outputs/
```

before appending to:

```text
outputs/registry.jsonl
```

---

## Minimal Local Check

```bash
python3 -m py_compile cli/run.py

export PYTHONNOUSERSITE=1
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

python3 cli/run.py
```

Expected result:

```text
JSON output to stdout
```

Failure mode:

```text
QE-shaped JSON output
```

---

## Recommended Future Tests

Add central tests under:

```text
tests/test_cli_run.py
```

Minimum test targets:

```text
emit_qe returns stable QE-shaped output
project_output preserves raw data under data
ensure_identity adds fallback identity only when epistemic_cryptography exists
attach_ontology_binding fails if proof missing
sync_to_nodes skips cleanly when requests is absent
main emits QE-shaped output on runtime failure
```

These tests belong in `/tests/`, not in `/cli/tests/`.

---

## Canonical Sentence

The VECTAETOS CLI is an execution/projection adapter: it may emit bounded reports and append provenance records, but it must never become an agent, optimizer, truth authority, or feedback path into Φ.
