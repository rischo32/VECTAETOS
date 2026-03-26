# Security Policy — VECTAETOS™

VECTAETOS is a non-agentic epistemic field framework.
No operational AI system is deployed within this repository.

---

## Security Model

This repository operates on two distinct and non-overlapping layers:

### 1. Technical Security

Concerns:

* Source code integrity
* Dependency vulnerabilities
* Repository infrastructure
* Build and deployment surfaces (if applicable)

Handled via:

* GitHub Security (Dependabot, Code Scanning, Secret Scanning)
* Standard vulnerability reporting

---

### 2. Ontological Invariance (Non-Security Domain)

Concerns:

* Integrity of epistemic structure
* Preservation of axiomatic invariants
* Non-authoritative stance of the framework

Important:

> Ontological invariants are not subject to security patching.
> Any modification constitutes a lineage divergence, not a vulnerability fix.

This layer is **out of scope for traditional security processes**.

---

## Scope of Technical Security

This repository may contain:

* Python / JavaScript simulation code
* Documentation and formal specifications
* Web-related assets (vectaetos.eu)

Applicable security issues include:

* Code vulnerabilities
* Dependency risks (when exploitable in context)
* Exposure of secrets or credentials
* Infrastructure misconfiguration

---

## Non-Applicable / Low-Relevance Cases

The following may be considered **non-actionable**:

* Low-severity dependency vulnerabilities without external attack surface
* Issues requiring local-only access without privilege escalation
* Vulnerabilities in unused or non-executed code paths

Example:

> Regex-based ReDoS in local-only libraries (e.g., syntax highlighting tools)

---

## Reporting

Security issues related to **technical security** may be reported via:

* GitHub Issues
* GitHub Security Advisories (Security → Advisories)

Please include:

* Description of the issue
* Steps to reproduce
* Potential impact
* Suggested mitigation (if known)

---

## Ontological Integrity

The following files are considered canonical anchors:

* CANONICAL_ANCHORS.md
* FORMAL_*.md
* MECHANIZATION_OF_*.md

Properties:

* Immutable by definition
* Not patchable
* Not subject to incremental correction

Any modification:

> Creates a new lineage (fork), not a fix.

---

## Out of Scope

The following are explicitly excluded from security handling:

* Theoretical challenges to the framework
* Epistemic interpretation disputes
* Conceptual or philosophical critiques
* Feature requests or extensions

Use:

* Discussions → for epistemic exploration
* Issues → for technical defects only

---

## Guiding Principle

> Security protects systems from exploitation.
> VECTAETOS protects coherence from false certainty.

These domains must remain distinct.

____________________________________

VECTAETOS™ — Onto-Epistemic Field Framework of structure
© 2026 Richard Fonfára
All projections are non-prescriptive.
