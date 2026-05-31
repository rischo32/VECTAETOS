# L0_L4_REQUIRED_EVIDENCE.md

## VECTAETOS™ — L0–L4 Required Evidence

**Status:** canonical-candidate evidence discipline  
**Layer:** Governance / Evidence Boundary / Implementation Readiness  
**Scope:** VECTAETOS™ / ASIMULATOR / ASI_MOD / EAI / EK / LSP / CI / downstream implementations  
**Lineage:** VECTAETOS 1.x compatible  
**Authority:** descriptive only  
**Execution Power:** none  
**Feedback into Φ:** none  
**Optimization:** none  
**Decision Power:** none  

---

## 0. Purpose

This document defines the minimum evidence required for each evidence layer `L0` through `L4`.

It exists to prevent evidence laundering.

A lower layer must not claim the evidential status of a higher layer.

```text
L0 consistency ≠ software verification
L1 guard pass ≠ empirical proof
L2 deterministic tests ≠ adversarial robustness
L3 simulated exposure ≠ real-world validation
L4 validation ≠ ontological authority
```

Evidence records may support documentation, traceability, review, and implementation discipline.

They do not mutate Φ.

They do not authorize deployment by themselves.

They do not create truth.

---

## 1. Core Evidence Ladder

```text
L0 — formal and ontological consistency
L1 — mechanized repository enforcement
L2 — deterministic software verification
L3 — simulated adversarial visibility
L4 — real-world empirical validation
```

Full operational admissibility may only be claimed under the strict condition:

```math
A_{\mathrm{full}} = 1
\iff
L0 \land L1 \land L2 \land L3 \land \mathrm{replicated}(L4)
```

Until replicated L4 evidence exists:

```math
A_{\mathrm{full}} = 0
```

This formula is not an optimization target.

It is a claim-boundary rule.

---

## 2. Global Rules

### 2.1 Non-Transfer Rule

```text
Evidence status does not transfer upward.
```

Examples:

```text
A clean CI run may support L1/L2.
It does not establish L3 or L4.

A deterministic EK artifact may support traceability.
It does not prove real-world safety.

A formal anchor may support L0.
It does not prove implementation correctness.

A simulation campaign may support L3.
It does not establish replicated L4.
```

### 2.2 No Authority Inflation

No evidence artifact may become:

```text
truth authority
deployment authority
safety certificate
legal verdict
compliance score
human-risk decision signal
regulatory shield
```

### 2.3 Layer-Local Claim Grammar

Each layer may only say what it can actually support:

```text
L0: "The formal description appears internally consistent under the reviewed anchors."
L1: "The repository guard detected or did not detect declared structural violations."
L2: "The bounded implementation passed deterministic verification under stated fixtures."
L3: "The simulated adversarial campaign exposed or did not expose declared drift vectors."
L4: "A real-world empirical study produced observed results under stated conditions."
```

No layer may say:

```text
therefore safe
therefore compliant
therefore true
therefore deployable
therefore canonical
therefore ASI
```

---

## 3. L0 — Formal and Ontological Consistency

### 3.1 Definition

`L0` means the formal / ontological description is internally coherent with declared VECTAETOS root constraints.

It concerns meaning, layer boundaries, and non-drift.

It does not concern software execution.

### 3.2 Required Evidence

Minimum required evidence:

```text
[ ] frozen core or canonical anchor reference
[ ] declared layer position
[ ] Φ = (Σ, R) boundary preserved
[ ] no agency injection
[ ] no optimizer / reward / goal function
[ ] no decision, recommendation, ranking, or scoring role
[ ] no feedback into Φ
[ ] no lower-layer rewrite of higher-layer meaning
[ ] κ not treated as metric, score, or threshold
[ ] QE not treated as error to minimize
[ ] projection not treated as interpretation
[ ] audit not treated as ontology
[ ] memory/context not treated as Φ state
[ ] uncertainty explicitly preserved
```

### 3.3 Acceptable Artifacts

```text
canonical anchors
formal definitions
doctrine notes
math appendices
non-goals
semantic drift review
layer maps
controlled glossary
```

### 3.4 Forbidden L0 Claims

```text
L0 proves implementation works.
L0 proves empirical safety.
L0 proves regulatory compliance.
L0 authorizes deployment.
L0 establishes ASI capability.
```

---

## 4. L1 — Mechanized Repository Enforcement

### 4.1 Definition

`L1` means repository-level enforcement exists and can detect declared structural or semantic violations.

It is a guard layer.

It is not ontology.

### 4.2 Required Evidence

Minimum required evidence:

```text
[ ] machine-readable behavior contract
[ ] protected symbol list
[ ] protected path list
[ ] hard violation list
[ ] deterministic CLI audit
[ ] LSP diagnostic mapping where applicable
[ ] CI integration
[ ] fail-closed behavior for root-adjacent uncertainty
[ ] no semantic autofix of anchors
[ ] no guard rewrite of ontology
[ ] reproducible audit output
[ ] audit report artifact retained
```

### 4.3 Acceptable Artifacts

```text
behavior_contract.yaml
guard_policy.yaml
ci_report.json
lsp_diagnostics.json
audit_findings.json
protected_paths.txt
semantic_drift_report.md
```

### 4.4 Forbidden L1 Claims

```text
CI pass proves empirical safety.
LSP clean proves VECTAETOS compliance.
Guard pass proves K(Φ)=1.
Audit clean proves deployment readiness.
Repository status proves ontology.
```

---

## 5. L2 — Deterministic Software Verification

### 5.1 Definition

`L2` means bounded implementation behavior has been tested deterministically.

It concerns reproducible software behavior, not real-world validity.

### 5.2 Required Evidence

Minimum required evidence:

```text
[ ] deterministic unit tests
[ ] regression tests
[ ] golden fixtures
[ ] property tests where appropriate
[ ] canonical serialization tests
[ ] fixed Σ ordering tests
[ ] no hidden randomness
[ ] no network dependency in verification path
[ ] no mutation of Φ, R, anchors, or protected inputs
[ ] no use of EK observables as control variables
[ ] explicit error types
[ ] reproducible test reports
[ ] version-pinned verification environment
```

### 5.3 Acceptable Artifacts

```text
pytest report
coverage report
fixture hash report
golden output snapshots
determinism proof log
reproducibility manifest
software bill of materials where applicable
```

### 5.4 Forbidden L2 Claims

```text
Unit tests prove real-world safety.
Determinism proves truth.
Serialization integrity proves semantic validity.
Hash stability proves ontology.
Software verification proves deployment admissibility.
```

---

## 6. L3 — Simulated Adversarial Visibility

### 6.1 Definition

`L3` means simulated adversarial scenarios have been used to expose drift, jailbreak, boundary collapse, or forbidden conversions.

It is visibility under simulated stress.

It is not real-world empirical validation.

### 6.2 Required Evidence

Minimum required evidence:

```text
[ ] adversarial scenario catalog
[ ] declared threat model
[ ] drift vector taxonomy
[ ] negative test fixtures
[ ] boundary-collapse tests
[ ] authority-inflation tests
[ ] optimizer-injection tests
[ ] feedback-loop tests
[ ] projection-as-interpretation tests
[ ] audit-as-ontology tests
[ ] hash-as-truth tests
[ ] score/ranking/recommendation misuse tests
[ ] simulated failure reports
[ ] unresolved scenario register
```

### 6.3 Acceptable Artifacts

```text
EK_ADVERSARIAL_SCENARIO_CATALOG.md
red_team_report.md
drift_vector_matrix.csv
simulation_run_manifest.json
boundary_failure_report.json
negative_fixture_set/
```

### 6.4 Forbidden L3 Claims

```text
Simulation proves field safety.
Adversarial tests prove no real-world harm.
Scenario coverage proves deployment readiness.
No simulated failure means L4 validation.
```

---

## 7. L4 — Real-World Empirical Validation

### 7.1 Definition

`L4` means real-world empirical validation has been conducted under documented conditions.

For full operational admissibility, L4 must be replicated.

### 7.2 Required Evidence

Minimum required evidence:

```text
[ ] explicit study protocol
[ ] declared use context
[ ] ethical / legal review where required
[ ] risk assessment for affected persons where applicable
[ ] data provenance record
[ ] measurement plan
[ ] failure criteria
[ ] non-intervention boundary
[ ] human oversight boundary
[ ] independent replication or replication plan
[ ] adverse event log
[ ] limitation statement
[ ] publication or audit trail
[ ] post-study drift review
```

### 7.3 Acceptable Artifacts

```text
study_protocol.md
ethics_review_record.md
data_provenance.json
real_world_observation_log.jsonl
replication_report.md
adverse_event_log.jsonl
limitations.md
external_review_letter.md
```

### 7.4 Forbidden L4 Claims

```text
A single study proves universal safety.
Real-world validation makes Φ an authority.
Empirical success authorizes all downstream uses.
L4 removes legal duties.
L4 converts ASI_MOD into a decision layer.
```

---

## 8. Evidence Record Schema

Every evidence record should preserve the following minimum fields:

```json
{
  "evidence_id": "string",
  "layer": "L0 | L1 | L2 | L3 | L4",
  "artifact_type": "string",
  "artifact_path": "string",
  "source_anchor": "string",
  "claim_supported": "string",
  "claim_not_supported": ["string"],
  "method": "string",
  "environment": "string",
  "date": "YYYY-MM-DD",
  "reviewer": "string",
  "status": "accepted | candidate | hypothesis | suspended | rejected",
  "limitations": ["string"],
  "no_feedback_into_phi": true,
  "no_deployment_authority": true,
  "no_truth_authority": true
}
```

---

## 9. Evidence Promotion Rule

A system may move from one evidence layer to another only by adding the required evidence of the higher layer.

It may not promote by narrative.

```text
more documentation ≠ higher evidence
more confidence ≠ higher evidence
more citations ≠ higher evidence
more tests ≠ L4
more demos ≠ L4
```

Promotion requires the missing layer-specific artifact.

---

## 10. Downgrade Triggers

Evidence status must be downgraded or suspended if any of the following occurs:

```text
anchor conflict
contract drift
unexplained test non-determinism
guard suppression of hard violations
new agency claim
new optimization claim
new decision-support use
new ranking/scoring interface
new LLM wrapper
public deployment
commercial interface
third-party use in affected-person context
unreviewed regulatory change
L4 replication failure
```

Downgrade is not punishment.

It is boundary restoration.

---

## 11. Minimum Repository Layout

Recommended layout:

```text
evidence/
  L0/
    ontology_consistency_review.md
    layer_boundary_review.md
  L1/
    ci_audit_report.json
    guard_policy.yaml
  L2/
    deterministic_test_report.json
    reproducibility_manifest.json
  L3/
    adversarial_scenario_catalog.md
    red_team_report.md
  L4/
    study_protocol.md
    replication_report.md
    adverse_event_log.jsonl
```

---

## 12. Final Boundary

```text
Evidence exposes support.
Evidence does not create truth.

Evidence constrains claims.
Evidence does not mutate Φ.

Evidence may justify caution.
Evidence does not authorize authority.
```

End of `L0_L4_REQUIRED_EVIDENCE.md`.
