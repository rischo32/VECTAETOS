# VECTAETOS™ - Security Policy

**Status:** Active repository security and architectural safety policy  
**Version:** 0.2-license-sentinel-aligned  
**Execution Power:** none  
**Feedback into Φ:** none  
**Legal note:** This is not legal advice. Security review, license integrity review, and architectural drift review do not create deployment authorization, safety proof, or truth authority.

---

## 1. Scope

VECTAETOS™ is a foundational, non-agentic, safety-oriented onto-epistemic field architecture.

This repository should be understood as:

- a research and formalization framework,
- a structural and ontological safety substrate,
- a non-authoritative, non-optimizing, non-decisional system root,
- a repository containing canonical materials, implementation-boundary documents, projection / trace governance, software/tooling guards, and a layered custom license stack.

This repository should **not** be understood as:

- a production autonomous agent,
- a deployment-ready decision engine,
- a self-authorizing operational intelligence layer,
- a safety guarantee,
- a regulatory authority,
- a truth authority,
- a certified deployment validator.

Security in this repository therefore includes both:

1. **technical security**  
   such as code integrity, workflow integrity, dependency risks, repository boundary violations, disclosure risks, token exposure, CI/CD trust boundaries, and supply-chain issues,

2. **architectural safety integrity**  
   such as violations of non-agentic constraints, reverse-flow violations, bypass of canonical anchors, invalid standalone higher-layer behavior, or unauthorized shifts toward operative authority,

3. **license-stack integrity**  
   such as unauthorized license-file mutation, DOI mismatch, badge drift, registry mismatch, missing boundary clauses, broken supersession statements, or tamper-evidence failure.

---

## 2. Supported Versions

The following support policy applies unless explicitly stated otherwise:

| Lineage / Branch / Artifact | Status |
|---|---|
| `main` | actively maintained research baseline |
| current frozen canonical anchors | supported for integrity review |
| current license stack | supported for integrity review |
| License Sentinel / license guard | supported for drift and tamper-evidence review |
| current DOI-published license records | supported for reference consistency review |
| archived branches / historical experiments | not supported except for provenance |
| unpublished local forks / mirrored copies | not supported |

Security review is prioritized for the current canonical branch, current canonical anchor set, and current license-stack perimeter.

---

## 3. Current DOI-Anchored License Stack

The current VECTAETOS™ license stack is published as separate DOI-anchored layers:

| Layer | Role | DOI |
|---|---|---|
| VCL-2.0 | canonical ontology / documentation | `10.5281/zenodo.20533697` |
| VTP-1.0 | identity / compatibility policy | `10.5281/zenodo.20534913` |
| VNAL-1.1 | implementation behavior | `10.5281/zenodo.20571153` |
| VPL-1.0 | projection / trace artifacts | `10.5281/zenodo.20574386` |
| AEPL-2.0-VECTAETOS | software / tooling / guards | `10.5281/zenodo.20574489` |

These DOI records are provenance and citation anchors.

They do **not** modify Φ.

```text
license DOI ≠ ontology mutation
license badge ≠ legal proof
license registry ≠ truth authority
hash manifest ≠ semantic validation
CI green ≠ deployment authorization
```

---

## 4. License Sentinel Boundary

The License Sentinel / license guard is a repository-integrity and drift-detection surface.

It may:

- check that declared license files exist,
- check that expected DOI strings are present,
- check that DOI badges match the registry,
- check that required boundary clauses are present,
- check hash / manifest integrity,
- detect unauthorized license-file mutation,
- report configured boundary violations,
- fail CI when repository integrity constraints are not satisfied.

It must not:

- define ontology,
- prove legal validity,
- prove truth,
- validate deployment,
- certify safety,
- rewrite canonical meaning,
- auto-fix ontology-facing text,
- silently mutate protected license or anchor files,
- become an authority over Φ.

A License Sentinel finding means:

```text
A configured repository or license-stack boundary appears to be violated.
```

It does not mean:

```text
Truth failed.
Ontology failed.
The system is unsafe.
Deployment is invalid.
The license is legally invalid.
```

---

## 5. What Should Be Reported

Please report any issue that may affect:

- repository integrity,
- canonical anchor integrity,
- license-stack integrity,
- DOI / badge / registry consistency,
- hash-lock or manifest integrity,
- License Sentinel bypass,
- workflow trust boundaries,
- CI/CD safety controls,
- dependency trust or supply-chain safety,
- unauthorized reverse dependency flow,
- invalid standalone operability of higher layers,
- bypass of fail-closed mechanisms,
- disclosure of secrets, credentials, or sensitive tokens,
- architectural drift that creates hidden authority, hidden optimization, hidden execution paths, or hidden deployment claims.

Examples include:

- a way for a downstream layer to operate as valid without VECTAETOS™,
- a way to bypass canonical anchor verification,
- a way to bypass License Sentinel checks,
- a workflow or token that grants more power than intended,
- a route by which audit becomes executive,
- a route by which interpretation becomes ontology,
- a route by which a non-agentic layer becomes decision-bearing,
- a route by which CI success is represented as deployment authorization,
- a route by which a hash, signature, DOI, badge, or registry entry is represented as truth.

---

## 6. License-Stack Issues That Should Be Reported

Please report license-stack problems such as:

- a license file missing from `LICENSES/`,
- a DOI mismatch between README, `LICENSE.md`, `LICENSE_REGISTRY.json`, and the license file,
- a DOI badge pointing to the wrong Zenodo record,
- unauthorized modification of a DOI-published license file,
- removal of non-authority clauses,
- removal of `Execution Power: none`,
- removal of `Feedback into Φ: none`,
- collapse of VCL, VTP, VNAL, VPL, or AEPL into a single authority layer,
- treating VTP as a software license,
- treating AEPL tooling permission as ontology permission,
- treating VPL projection output as interpretation authority,
- treating VNAL implementation behavior as canonical ontology,
- treating VCL citation as deployment validation,
- registry or manifest drift not explained by an explicit release.

---

## 7. Out of Scope

The following are generally out of scope for vulnerability handling unless they directly create a concrete security, integrity, or safety risk:

- purely stylistic disagreements,
- documentation wording preferences,
- speculative claims without a reproducible path,
- philosophical disagreement without a structural exploit path,
- hypothetical misuse scenarios with no actionable mechanism,
- unsupported forks, mirrors, or modified third-party deployments,
- disagreement with the license stack without a concrete integrity, confusion, or misrepresentation path.

That said, architecture-level safety concerns are welcome when they are concrete, reproducible, and tied to an actual integrity or control failure.

---

## 8. Reporting a Vulnerability

Please **do not** open a public GitHub issue for undisclosed vulnerabilities.

Instead, report privately using one of the following channels:

- project contact email: `<fonfararichard@gmail.com>`

Please include as much of the following as possible:

- affected repository,
- affected branch or commit,
- affected file or license layer,
- affected DOI or badge, if relevant,
- clear description of the issue,
- reproduction steps,
- impact assessment,
- whether the issue is technical, architectural, license-stack related, or mixed,
- logs, screenshots, proof-of-concept, or minimal reproducer if available,
- whether you believe disclosure should be coordinated.

A good report is precise, minimal, reproducible, and avoids unnecessary speculation.

---

## 9. Disclosure Expectations

We aim to handle reports in good faith.

Target process:

- acknowledgement of receipt: as soon as reasonably possible,
- initial triage: as soon as reasonably possible,
- coordinated remediation discussion: when the report is validated,
- public disclosure: only after remediation, mitigation, or explicit agreement.

Please avoid:

- public disclosure before initial review,
- social engineering,
- destructive testing,
- denial-of-service,
- mass automated probing,
- credential harvesting,
- exfiltration of private data,
- attempts to bypass legal or platform boundaries,
- attempts to force an ontological or deployment conclusion through a vulnerability report.

Good-faith reporting intended to improve the safety and integrity of the architecture will be treated seriously and respectfully.

---

## 10. Coordinated Disclosure

Where a report affects multiple repositories in the triad, disclosure may need to be coordinated across:

- `Vectaetos`
- `ASIMULATOR`
- `ASI_MOD`

This is especially important for:

- anchor integrity,
- license-stack integrity,
- assembly manifest integrity,
- component identity consistency,
- boot guard behavior,
- license guard behavior,
- repo boundary enforcement,
- workflow trust and token permissions.

A vulnerability in one layer may have architectural consequences for the others.

---

## 11. Architectural Security Constraints

The following are considered core security-and-safety constraints of the architecture:

1. **VECTAETOS™ is the ontological root.**  
   Higher layers may not redefine it.

2. **Execution must remain downstream of ontology.**  
   No reverse-flow authority is permitted.

3. **Interpretation must remain downstream of execution.**  
   Dialogic output must not become ontological source authority.

4. **Audit is non-executive.**  
   Audit may observe, record, hash, and verify structural integrity.  
   Audit may not command, optimize, redefine, or override ontology.

5. **License Sentinel is non-authoritative.**  
   It detects license-stack drift and tamper-evidence failure.  
   It does not validate law, ontology, safety, deployment, or truth.

6. **Higher layers are non-self-sufficient.**  
   `ASIMULATOR` and `ASI_MOD` must not become valid standalone systems.

7. **Fail-closed behavior is preferred.**  
   Invalid assembly states must not silently degrade into false legitimacy.

8. **Canonical anchor ownership remains in VECTAETOS™.**  
   Downstream repositories must not silently fork semantic authority.

9. **License stack separation must be preserved.**  
   VCL, VTP, VNAL, VPL, and AEPL must not collapse into a single authority layer.

Any vulnerability that breaks one of these constraints should be treated as high-priority.

---

## 12. Safety-Critical Transition Governance

VECTAETOS™ is published as a foundational, non-agentic, safety-oriented epistemic architecture.

Any transition of this architecture beyond foundational research toward materially relevant ASI-like capability must not become the unilateral decision of its author, but requires explicit multi-party safety deliberation with all competent and materially affected stakeholders invited to a common round table.

Until such conditions exist:

- no claim of deployment readiness is made,
- no claim of higher-layer legitimacy is made,
- no claim of ASI-like operational admissibility is made,
- no single individual is treated as solely authorized to legitimize such a transition.

This clause is not a product launch rule.

It is a responsibility constraint tied to the safety posture of the architecture itself.

---

## 13. Current Safety Posture

At the present stage:

- foundational ontology work may continue,
- formalization may continue,
- documentation may continue,
- license-stack integrity enforcement may continue,
- repository integrity enforcement may continue,
- empirical safety work may continue.

However:

- higher operative legitimization remains suspended,
- premature deployment claims are rejected,
- structurally complete architecture is not treated as empirically validated architecture,
- license publication is not treated as legal certainty,
- CI success is not treated as deployment validation.

Structural completeness is not the same as safety proof.

License-stack consistency is not the same as legal enforceability.

---

## 14. Safe Use Note

This repository does not authorize:

- autonomous harmful use,
- coercive use,
- manipulative use,
- surveillance use,
- weaponization,
- operational claims of authority,
- deployment claims that exceed empirical evidence,
- claims that license, DOI, badge, hash, or CI output proves truth, safety, or deployment validity.

Any use, implementation, or extension that claims authority, completeness, or exclusive correctness ceases to be consistent with the ontological posture of VECTAETOS™.

---

## 15. Final Note

Security here is not only about protecting code.

It is also about protecting:

- non-agentic constraints,
- architectural asymmetry,
- anchor integrity,
- license-stack integrity,
- semantic integrity,
- fail-closed dependency rules,
- DOI and provenance consistency,
- and the boundary between foundational research and unsafe premature operationalization.

```text
guard ≠ authority
hash ≠ truth
badge ≠ validity
DOI ≠ Φ mutation
CI green ≠ deployment authorization
security policy ≠ ontology
```
