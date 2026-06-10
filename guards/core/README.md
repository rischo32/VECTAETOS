# VECTAETOS™ Guard Core

**Path:** `guards/core/`  
**Status:** shared implementation kernel  
**Scope:** repository perimeter diagnostics only  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Feedback into Φ:** none  

---

## 0. Boundary

`guards/core/` contains shared helper modules for VECTAETOS repository guards.

It standardizes how guards represent findings, render reports, parse contracts, scan text, scan Python AST, classify paths, infer code roles, check capabilities, and verify immutable blob bytes.

It is not a guard by itself.

It is not an ontology layer.

It is not a contract source.

It is not a replacement for anchors.

It does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, ZMYSEL, or canonical meaning.

```text
guards/core/ = shared non-authoritative guard infrastructure
```

Core invariant:

```text
Guard exponuje drift; nedefinuje pravdu.
```

---

## 1. What this directory is

`guards/core/` provides deterministic primitives for:

```text
perimeter coordinates
finding schema
severity and confidence labels
drift vectors
evidence classes
safe PASS / FAIL wording
exit-code mapping
contract loading and validation
negation-aware text scanning
alias-aware Python AST scanning
path classification
role inference
capability policy
byte-integrity verification
```

The intended flow:

```text
anchor / contract
    ↓
shared guard kernel
    ↓
individual guard
    ↓
Finding
    ↓
text / JSON / GitHub report
    ↓
CLI / CI repository-state signal
```

The flow must not reverse.

---

## 2. What this directory is not

`guards/core/` must never become:

```text
ontology source
truth authority
decision layer
optimizer
controller
runtime agent
deployment validator
safety proof
empirical proof
Φ modifier
K(Φ) evaluator
κ estimator
QE resolver
Vortex selector
Projection interpreter
EK authority
auto-fix layer
auto-quarantine layer
auto-revert layer
```

Core modules may expose diagnostics.

They must not define meaning.

---

## 3. Current modules

### `perimeter.py`

Defines shared perimeter vocabulary.

Main responsibilities:

```text
PerimeterLevel: Level 0 through Level 5
PerimeterScope
LegacyScope compatibility for old P0–P4 values
DriftVector V0 through V15
EvidenceClass E0 through E7
EnforcementMode
IntegrityPosture
Severity
Confidence
safe PASS / FAIL wording
forbidden report claims
safe wording registry
level / scope validation
```

Boundary:

```text
Perimeter coordinates classify diagnostics.
They are not ontology.
```

---

### `findings.py`

Defines the shared `Finding` object.

Main responsibilities:

```text
one shared finding schema
Level 0–5 support
legacy scope compatibility
vector and vectors support
stable deterministic finding id
ontology_authority invariant
auto_fix_allowed invariant
path normalization
JSON-compatible conversion
```

Required posture:

```text
Finding = diagnostic record
Finding ≠ verdict
Finding ≠ truth claim
Finding ≠ metaphysical proof
```

Minimum target shape:

```yaml
guard_id: "GUARD-12"
guard_file: "guards/coherence_vocabulary_guard.py"
rule_id: "FC-KAPPA-METRIC"
contract_schema_version: "1.0"

level: "Level 2"
scope: "semantic_vocabulary"
vector: "V3_forbidden_conversion"
severity: "BLOCKER"
confidence: "high"

path: "formal/example.md"
message: "Pattern appears to convert κ into metric language."

ontology_authority: false
auto_fix_allowed: false
```

---

### `reporting.py`

Defines deterministic rendering and exit-code mapping.

Main responsibilities:

```text
stable finding ordering
JSON report rendering
human text report rendering
GitHub step-summary rendering
severity threshold handling
exit-code calculation
safe PASS / FAIL language
forbidden authoritative report wording detection
```

Exit-code contract:

```text
0 = no findings at configured enforcement level
1 = blocker finding detected
2 = guard infrastructure failure / confidence unavailable
3 = invalid contract / missing anchor trace / invalid manifest signature
4 = invalid CLI usage
```

Boundary:

```text
Exit code = repository-state signal
Exit code ≠ truth value
CI pass ≠ empirical validation
CI fail ≠ metaphysical proof
```

---

### `contracts.py`

Defines read-only contract loading and validation.

Main responsibilities:

```text
JSON contract loading
optional YAML loading if PyYAML is available
schema_version validation
rule_id validation
anchor_ref traceability
protected_object traceability
level / scope validation
vector / vectors validation
evidence_class_allowed validation
enforcement_mode validation
integrity_posture validation
ContractRule → Finding conversion
```

Strict or fail-closed rules must have:

```yaml
anchor_ref:
protected_object:
vector:
evidence_class_allowed:
enforcement_mode:
```

Boundary:

```text
Contract = machine-readable projection of anchor constraints
Contract ≠ anchor
Contract ≠ ontology
Contract ≠ truth source
```

---

### `text_scan.py`

Defines negation-aware text scanning.

Required behavior:

```text
explicit negation → do not block
meta-example → do not block
explicit negation + operational pattern → WARN
meta-example + operational pattern → WARN
active operational claim without negation → finding by rule severity
```

Example:

```text
"VECTAETOS is not an optimizer."        → no blocker
"VECTAETOS optimizer selects path."     → blocker
"not optimizer, but score = ..."        → warning / review
```

Boundary:

```text
Text scan exposes vocabulary drift.
It does not interpret ontology.
```

---

### `ast_scan.py`

Defines alias-aware Python AST scanning.

Main responsibilities:

```text
parse Python source
never import target modules
never execute target modules
build import alias table
resolve aliased calls
detect subprocess
detect network calls
detect randomness
detect dynamic execution / import
detect file mutation calls
detect selection functions
detect ontology-facing assignments
emit Level 3 code_behavior findings
```

Examples of required detection:

```python
import subprocess as sp
sp.run(...)

from pathlib import Path
Path("x").open("w")

Phi = 1
```

Boundary:

```text
AST scan = static code diagnostic
AST scan ≠ runtime execution
AST scan ≠ proof of safety
```

---

### `paths.py`

Defines repository path normalization and path-role classification.

Main responsibilities:

```text
normalize repo paths
reject absolute paths
reject path traversal
resolve paths under repo root
infer PathRole
map PathRole to PerimeterLevel
map PathRole to PerimeterScope
detect text candidates
detect binary candidates
skip generated/heavy technical directories when requested
emit path-policy findings
```

Boundary:

```text
Path classification is diagnostic.
Path location does not create ontology.
Exclusion from one guard is not exclusion from the whole perimeter.
```

---

### `roles.py`

Defines code-role declaration and inference.

Supported declaration:

```python
# VECTAETOS_ROLE: guard
```

Boundary:

```text
Role inference grants no authority.
Role inference only selects diagnostic policy.
```

---

### `capabilities.py`

Defines role capability boundaries.

Main responsibilities:

```text
CodeRole enum
CapabilityName enum
CapabilityPolicy matrix
network policy
subprocess policy
file-write policy
randomness policy
selection-function policy
ontology-assignment protection
capability-to-drift-vector mapping
capability findings
```

Boundary:

```text
Capability denial = repository-state diagnostic
Capability denial ≠ metaphysical proof
Capability allow ≠ deployment validation
```

---

### `immutable_blob.py`

Defines read-only byte-integrity helpers.

Main responsibilities:

```text
load blob manifest
validate manifest schema
validate repo-relative paths
hash files with SHA-256
optionally hash files with SHA3-512
verify size
verify digest
build manifest records without writing files
render manifest JSON without writing files
emit Level 0 byte-integrity findings
```

Boundary:

```text
Hash match = byte integrity observable
Hash mismatch = repository-state integrity drift
Hash ≠ semantic truth
Hash ≠ ontology
Hash ≠ safety proof
```

---

## 4. Shared Finding contract

Every refactored guard should emit shared `Finding` objects from `findings.py`.

Target fields:

```yaml
guard_id:
guard_file:
rule_id:
contract_schema_version:

level:
scope:
vector:
vectors:
severity:
confidence:

path:
line:
column:
message:

protected_object:
observed_pattern:
forbidden_conversion:
negated_context:

evidence_class_allowed:
enforcement_mode:
integrity_posture:

anchor_ref:
contract_ref:
safer_form:

ontology_authority: false
auto_fix_allowed: false
```

Mandatory posture:

```text
ontology_authority must always be false
auto_fix_allowed must default to false
rule_id must be stable
contract_schema_version must be present
level / scope must be consistent
```

---

## 5. Safe report language

Allowed:

```text
PASS: No configured blocker was detected within the declared perimeter.
FAIL: Configured blocker detected within declared repository perimeter.
FAIL: Guard infrastructure error; confidence unavailable.
Repository-state result only.
Not empirical validation.
```

Forbidden:

```text
ontology preserved
truth proven
semantic correctness proven
VECTAETOS is safe
deployment ready
safety validated
guard-certified ontology
hash proves meaning
signature proves ontology
manifest-certified ontology
CI proves safety
```

---

## 6. Import direction

Allowed direction:

```text
individual guard → guards/core
```

Forbidden direction:

```text
guards/core → individual guard authority
```

Allowed imports from individual guards:

```python
from guards.core.findings import make_finding, Severity, Confidence, DriftVector
from guards.core.reporting import render_text_report, render_json, exit_code_for
from guards.core.contracts import load_contract, finding_from_rule
from guards.core.text_scan import scan_text_to_findings
from guards.core.ast_scan import scan_python_file
from guards.core.paths import describe_path, iter_repo_files
```

Forbidden:

```text
core importing individual guard rule logic
core selecting which guard is correct
core changing guard rules dynamically
core mutating repository files
core mutating Φ or any ontology-facing structure
```

---

## 7. Refactor discipline

Existing guards should be migrated gradually.

Recommended order after core stabilization:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-01 canonical_ontology_guard.py
3. GUARD-03 vectaetos_code_behavior_audit.py
4. GUARD-08 qe_aporia_guard.py
5. GUARD-09 triality_guard.py
6. GUARD-10 vector_drift_guard.py
7. GUARD-11 master_index_router_guard.py
8. GUARD-20 release_claim_guard.py
9. GUARD-19 repo_path_guard.py
10. GUARD-22 contract_traceability_guard.py
11. GUARD-24 anchor_blob_integrity_guard.py
```

Each refactor may standardize:

```text
finding shape
report rendering
exit-code behavior
safe wording
contract traceability
```

Each refactor must not silently change:

```text
ontology
rule meaning
enforcement scope
anchor meaning
evidence claim level
```

---

## 8. Test expectation

Every core module must remain:

```text
Python 3.11+ compatible
standard-library only unless explicitly approved
deterministic
side-effect minimal
non-networked
non-agentic
non-authoritative
```

Minimum local check:

```bash
python3 -m py_compile guards/core/*.py
```

Expanded import smoke test:

```bash
python3 - <<'PY'
from guards.core.findings import make_finding, Severity, Confidence, DriftVector, Scope
from guards.core.reporting import render_text_report, exit_code_for
from guards.core.text_scan import make_rule, scan_text_to_findings
from guards.core.ast_scan import scan_python_source
from guards.core.paths import describe_path
from guards.core.roles import resolve_code_role
from guards.core.capabilities import CodeRole, CapabilityName, validate_capability_use

finding = make_finding(
    guard_id="GUARD-00",
    guard_file="guards/perimeter_kernel_guard.py",
    rule_id="CORE-SMOKE",
    scope=Scope.P0_REPOSITORY,
    vector=DriftVector.V0_AUTHORITY_INFLATION,
    severity=Severity.INFO,
    confidence=Confidence.HIGH,
    path="guards/core/README.md",
    message="Smoke test diagnostic only.",
)

print(render_text_report([finding], title="Core Smoke", mode="report"))
print(exit_code_for([finding]))

rule = make_rule(
    rule_id="TXT-SMOKE",
    pattern=r"optimizer",
    message="Optimizer wording observed.",
    scope=Scope.P1_SEMANTIC_VOCABULARY,
    vector=DriftVector.V2_AGENCY_INJECTION,
    severity=Severity.BLOCKER,
)

print(scan_text_to_findings(
    path="fixture.md",
    text="VECTAETOS is not an optimizer.",
    rules=[rule],
    guard_id="GUARD-12",
    guard_file="guards/coherence_vocabulary_guard.py",
))

result = scan_python_source(
    path="guards/example_guard.py",
    source='import subprocess as sp\nsp.run(["git", "status"])\n',
)

print([item.rule_id for item in result.findings])
print(describe_path("guards/core/findings.py").role.value)
print(resolve_code_role(path="guards/core/findings.py").value)
print(validate_capability_use(
    path="guards/example_guard.py",
    role=CodeRole.GUARD,
    capability=CapabilityName.SUBPROCESS,
    observed_pattern='sp.run(["git", "status"])',
)[0].rule_id)
PY
```

---

## 9. Stop conditions

Stop implementation if `guards/core/` introduces:

```text
truth authority
ontology source
optimizer
planner
decision system
recommendation engine
runtime controller
feedback loop into Φ
auto-fix layer for ontology-facing text
auto-revert mechanism
auto-quarantine mechanism
network dependency
hidden external state
```

---

## 10. Final boundary sentence

```text
guards/core/ standardizes how guard diagnostics are represented and reported.
It does not decide what VECTAETOS is.
```

Slovak:

```text
guards/core/ zjednocuje spôsob, akým guardy zapisujú a hlásia diagnostiku.
Nerozhoduje, čo je VECTAETOS.
```

End.
