# VECTAETOS™ License Stack

**Directory:** `/LICENSES/`  
**Status:** Draft / Review Layer  
**Purpose:** Human-readable map of the VECTAETOS™ licensing, projection, implementation, and identity boundary stack  
**Legal note:** This directory is not legal advice. Custom license enforceability depends on jurisdiction, registration status, actual use, and applicable law.

---
→ VCL-2.0 : [![VCL-2.0 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20533697.svg)](https://doi.org/10.5281/zenodo.20533697)
___
→ AEPL-2.0 : 
___
→ VNAL-1.1 : [![VNAL-1.1 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20571153.svg)](https://doi.org/10.5281/zenodo.20571153) 
___
→ VPL-1.0 : [![VPL-1.0 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20574386.svg)](https://doi.org/10.5281/zenodo.20574386)
___
→ VTP-1.0 : [![VTP-1.0 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20534913.svg)](https://doi.org/10.5281/zenodo.20534913)
___
## Perimeter Level Mapping

This license stack is guarded under the VECTAETOS Level model:

- Level 0 — repository identity, canonical file presence, license stack placement
- Level 5 — release wording, evidence claims, DOI wording, CI execution checks

The license stack must not use older P0–P4 perimeter labels.
___
## 0. Core Boundary

This directory contains the licensing and identity-use layer for VECTAETOS™.

The license stack protects:

```text
canonical ontology
repository use
implementation behavior
projection artifacts
public identity
compatibility claims
```

It does **not** define ontology.

It does **not** decide truth.

It does **not** authorize deployment.

It does **not** make any artifact, projection, guard, DOI, hash, signature, or report an authority over Φ.

```text
license ≠ ontology
policy ≠ truth
trademark ≠ Φ
guard ≠ authority
hash ≠ semantic truth
projection ≠ interpretation
EK ≠ decision
```

---

## 1. License Stack Overview

The VECTAETOS™ license stack is layered.

Each layer governs a different type of material.

```text
ontology / anchors / doctrine     → VCL-2.0
software / guards / tooling       → AEPL-2.0-VECTAETOS
implementation systems            → VNAL-1.1
projection / glyph / EK traces    → VPL-1.0
marks / identity / compatibility  → VTP-1.0
```

This separation prevents one license from collapsing every layer into one authority.

---

## 2. Files in This Directory

```text
LICENSE_STACK.md
VCL-2.0.md
AEPL-2.0-VECTAETOS.md
VNAL-1.1.md
VPL-1.0.md
VTP-1.0.md
LICENSE_LINEAGE_AND_SUPERSESSION.md
ZENODO_RELEASE_MINIGUIDE.md
README.md
```

---

## 3. Layer Map

### `LICENSE_STACK.md`

Human-readable overview of the full licensing structure.

Use this file to understand:

```text
which license applies to which repository layer
how the layers relate
which documents are historical
which documents are proposed successors
```

### `VCL-2.0.md`

**VECTAETOS™ Canonical License**

Applies to:

```text
canonical anchors
frozen ontology
canonical operating doctrine
formal vocabulary
Φ = (Σ, R)
ZMYSEL / Ξ boundary language
K(Φ), κ, QE
Vortex boundary language
Epistemic Cryptography boundary language
TetraGlyph canonical descriptions
```

Purpose:

```text
protect canonical lineage
prevent ontology laundering
prevent false official status
preserve non-agentic identity
preserve non-authoritative framing
```

Short rule:

```text
You may study, cite, discuss, and create compatible derivatives.
You may not present modified, agentic, optimizing, decisional, or authority-claiming systems as canonical VECTAETOS™.
```

### `AEPL-2.0-VECTAETOS.md`

**Axiomatic Epistemic Public License**

Applies to:

```text
source code
guards
CLI audit tools
LSP diagnostics
contracts
test fixtures
adapter code
parser code
projection tooling
repository automation
CI helper scripts
```

Purpose:

```text
permit research and implementation
preserve non-authoritative output language
protect deterministic audit behavior
prevent software from becoming ontology
prevent guards from becoming truth authorities
```

Short rule:

```text
Code may expose drift.
Code may not define truth.
```

### `VNAL-1.1.md`

**VECTAETOS™ Non-Agentic License**

Applies to:

```text
ASIMULATOR-like systems
simulation engines
runtime structures
dialogue prototypes
output-producing implementations
trajectory exploration tools
adapter-integrated prototypes
```

Purpose:

```text
preserve non-agentic behavior
preserve uncertainty disclosure
preserve QE / aporia / silence where structurally valid
prevent single-answer collapse
prevent reward-loop collapse
```

Short rule:

```text
Implementation may explore.
Implementation may not decide.
```

### `VPL-1.0.md`

**VECTAETOS™ Projection License**

Applies to:

```text
TetraGlyph
glyphs
runes
projection diagrams
symbolic renderings
EK observables
audit traces
structural fingerprints
hash reports
Merkle roots
ledger-like records
trace bundles
```

Purpose:

```text
preserve projection ≠ interpretation
preserve glyph ≠ verdict
preserve hash ≠ truth
preserve EK trace ≠ deployment validation
```

Short rule:

```text
Projection may reveal form.
Projection may not claim authority over meaning.
```

### `VTP-1.0.md`

**VECTAETOS™ Trademark and Compatibility Policy**

Applies to:

```text
VECTAETOS™
VECTAETΦS™
VECTAETOS FOUNDATIONS
VECTLAB™
VECTLAB Research Node
VECTLAB Epistemic Shield
badges
logos
domains
package names
repository names
compatibility claims
certification claims
confusingly similar identifiers
```

Purpose:

```text
protect public identity
prevent false official status
prevent misleading compatibility claims
prevent productized authority claims
prevent weaponized or operational claims
```

Short rule:

```text
You may reference VECTAETOS™ truthfully.
You may not manufacture official authority from the name.
```

### `LICENSE_LINEAGE_AND_SUPERSESSION.md`

Explains the historical relationship between older and newer licenses.

Covers:

```text
AEPL-1.2-VECTAETOS
VCL-1.0
VNAL-1.0
VCL-2.0
AEPL-2.0-VECTAETOS
VNAL-1.1
VPL-1.0
VTP-1.0
```

Important rule:

```text
license version ≠ ontology version
legal supersession ≠ semantic supersession
DOI update ≠ Φ mutation
```

### `ZENODO_RELEASE_MINIGUIDE.md`

Minimal operational guide for DOI anchoring.

Recommended sequence:

```text
repo first
review second
Zenodo after review
DOI back-reference after publication
```

Safe DOI wording:

```text
This DOI archives the license text as published on the release date.
```

Forbidden DOI wording:

```text
This DOI proves ontology.
This DOI validates VECTAETOS™.
This DOI authorizes deployment.
```

---

## 4. Recommended Repository Root Links

The root `LICENSE.md` should link back here:

```md
## Licensing

This repository uses the VECTAETOS™ License Stack.

- Canonical ontology and anchors: `LICENSES/VCL-2.0.md`
- Software and tooling: `LICENSES/AEPL-2.0-VECTAETOS.md`
- Implementation systems: `LICENSES/VNAL-1.1.md`
- Projection artifacts and EK traces: `LICENSES/VPL-1.0.md`
- Marks and compatibility claims: `LICENSES/VTP-1.0.md`

See `LICENSES/README.md` for the full layer map.
```

---

## 5. Minimal Decision Guide

```text
Is it a canonical anchor, doctrine, or ontology term?
  → VCL-2.0

Is it code, guard logic, contract logic, parser, adapter, or CI tooling?
  → AEPL-2.0-VECTAETOS

Is it an implementation system that produces behavior, outputs, traces, or simulations?
  → VNAL-1.1

Is it a glyph, rune, projection, EK trace, hash, Merkle root, fingerprint, or symbolic artifact?
  → VPL-1.0

Is it a name, logo, badge, domain, package name, compatibility claim, or certification claim?
  → VTP-1.0
```

---

## 6. Safe Attribution

Suggested attribution for derivative or research materials:

> VECTAETOS™, VECTAETΦS™, VECTAETOS FOUNDATIONS, VECTLAB™, and related marks are associated with the VECTAETOS project by Richard Fonfára. This work is independent unless explicitly marked as official. Use of the marks does not imply endorsement, certification, deployment validity, safety guarantee, or decision authority.

---

## 7. Safe Compatibility Statement

Allowed:

```text
This project is inspired by VECTAETOS™ and is not an official implementation.
```

Allowed:

```text
Compatible with selected VECTAETOS™ concepts; not endorsed, certified, or canonical.
```

Forbidden without explicit authorization:

```text
Official VECTAETOS™ implementation.
VECTAETOS™ certified.
VECTAETOS™ validated.
VECTAETOS™ deployment-ready.
VECTAETOS™ safety-approved.
```

---

## 8. Non-Goals

This license directory does not:

```text
define Φ
modify Φ
define K(Φ)
define κ
define QE
validate deployment
prove empirical safety
replace human review
replace canonical anchors
make EK an enforcement authority
make cryptographic integrity semantic truth
make CI a metaphysical verifier
```
---

## 9. Final Boundary

```text
The license stack protects use, lineage, identity, and representation.
It does not own truth.
It does not own Φ.
It does not make VECTAETOS™ an authority.
```

Slovensky:

```text
Licenčný stack chráni použitie, líniu, identitu a reprezentáciu.
Nevlastní pravdu.
Nevlastní Φ.
Nerobí z VECTAETOS™ autoritu.
```

End of `/LICENSES/README.md`.
