# VECTAETOS — Unified Architecture Diagram

Status: Referential (non-ontological)
Scope: Complete structural orientation across **depth** (layers) and **triality** (repositories)
Authority: Descriptive only — canonical anchors remain in `/formal/MAPARCH.md`, `/VECTAETOS_MASTER_INDEX.md`, `/contracts/LAYER_BOUNDARIES.md`.

This document consolidates the architecture maps that were previously scattered across
`ARCHITECTURE.md`, `MAPARCH.md`, `docs/VECTAETOS_SYSTEM_MAP.md`, `docs/VECTAETOS_FIELD_DIAGRAM.md`
and `docs/arch_pipe.md` into a **single unified view** — not only the surface pipeline,
but also the **depth of layers**, the **triadic boundary** with ASIMULATOR / ASI_MOD,
the **structural (Δ / so(8)) backbone**, and the **CI / audit guardrails**.

The five sub-diagrams below are sections of the same picture. Together they form the
**unified architectural projection** of VECTAETOS™.

Pre-rendered flat projections of each sub-diagram are available under
[`unified_architecture/`](./unified_architecture/):

| # | Image | Focus |
|---|---|---|
| 1 | [`01-depth-stack.png`](./unified_architecture/01-depth-stack.png) | Full L0 → L10 depth stack with Δ backbone and NIR skelet |
| 2 | [`02-sigma-geometry.png`](./unified_architecture/02-sigma-geometry.png) | The 8 axiomatic poles Σ₁…Σ₈ around Φ |
| 3 | [`03-triadic-oaat.png`](./unified_architecture/03-triadic-oaat.png) | Triadic repository boundaries (VECTAETOS / ASIMULATOR / ASI_MOD) |
| 4 | [`04-ci-guardrails.png`](./unified_architecture/04-ci-guardrails.png) | CI workflows enforcing the non-agentic policy |
| 5 | [`05-unified-cross-section.png`](./unified_architecture/05-unified-cross-section.png) | One-picture cross-section (depth × triality × audit) |

---

## 1. Unified Depth Stack (L0 → L10 + Δ + NIR)

Reading top-to-bottom = descent from human surface into ontological depth.
NIR and the Δ / so(8) structural backbone are **orthogonal skelets** that apply
to every layer simultaneously.

```mermaid
flowchart TB
    classDef human fill:#f4f1de,stroke:#3d405b,stroke-width:1px,color:#3d405b
    classDef gate fill:#e7ecef,stroke:#274c77,color:#274c77
    classDef field fill:#f6bd60,stroke:#6d2e46,stroke-width:2px,color:#3d1308
    classDef sigma fill:#fff3b0,stroke:#6d2e46,color:#3d1308
    classDef kernel fill:#e9c46a,stroke:#6d2e46,color:#3d1308
    classDef vortex fill:#cdb4db,stroke:#3a2e6d,color:#241041
    classDef proj fill:#bde0fe,stroke:#023e8a,color:#023047
    classDef adapter fill:#caf0f8,stroke:#0077b6,color:#03045e
    classDef delta fill:#dde5b6,stroke:#606c38,color:#283618
    classDef nir fill:#2a2a2a,stroke:#f6bd60,stroke-width:2px,color:#f6bd60
    classDef audit fill:#ffb4a2,stroke:#6a040f,color:#370617

    H0(["L0 · HUMAN — questions, statements, observations"]):::human

    subgraph PREFIELD ["Pre-field conditioning"]
        direction TB
        L1["L1 · LLM entry adapter<br/>parsing only, no authority"]:::adapter
        L2["L2 · 3Gate — W · D · H<br/>epistemic deformation, not validation"]:::gate
        L3["L3 · 4ES + QE<br/>AA · AN · NA · NN · QE<br/>representability evaluation"]:::gate
    end

    subgraph ONTOLOGY ["Primary ontology — Φ"]
        direction TB
        L4(("L4 · Φ<br/>Relational Epistemic Field<br/>Φ = (Σ, R), R ∈ so(8)")):::field
        L5["L5 · Σ₁…Σ₈<br/>INT · LEX · VER · LIB<br/>UNI · REL · WIS · CRE"]:::sigma
        L6["L6 · K(Φ) and κ<br/>coherence predicate<br/>representability boundary"]:::kernel
    end

    subgraph DYNAMICS ["Dynamics — auxiliary, non-decisional"]
        direction TB
        L7["L7 · Simulation Vortex Φ(t)<br/>candidate trajectories<br/>no access to K, κ, Σ"]:::vortex
    end

    subgraph PROJECTION ["Read-only projection"]
        direction TB
        L8["L8 · Runic Projection Π(Φ)<br/>symbolic, lossy, descriptive"]:::proj
        L9["L9 · LLM rendering adapter<br/>translation, never source"]:::adapter
        L10(["L10 · Descriptive Output<br/>text · silence · QE"]):::human
    end

    subgraph STRUCT ["Δ / EK 2.0 — structural backbone"]
        direction LR
        D1["Δ = dR<br/>Δ ∈ ℝ⁵⁶, dΔ = 0"]:::delta
        D2["Canonicalization<br/>G = S₈ orbit"]:::delta
        D3["H(Φ) = H(Δ_c)<br/>structural hash"]:::delta
        D4["κ sensitivity<br/>under perturbations"]:::delta
        D1 --> D2 --> D3 --> D4
    end

    subgraph MEM ["Memory / trace — non-directive"]
        direction TB
        M1["ESM · LTL · EAT · MML<br/>records, never instructs"]:::audit
    end

    subgraph AUDIT ["Epistemic Cryptography — read-only audit"]
        direction TB
        A1["μᵢ local uncertainty<br/>Aᵢⱼ pairwise asymmetry<br/>h topological humility"]:::audit
    end

    NIR[["NIR — Non-Intervention Regime<br/>global epistemic immunity · opaque · non-bypassable"]]:::nir

    H0 --> L1 --> L2 --> L3 --> L4
    L4 --- L5
    L4 --> L6 --> L7 --> L8 --> L9 --> L10 --> H0

    L4 -. "canonical observation" .-> STRUCT
    L4 -. "observed by" .-> AUDIT
    L7 -. "traced in" .-> MEM
    STRUCT -. "feeds invariants to" .-> AUDIT

    NIR -. "active across" .-> PREFIELD
    NIR -. "active across" .-> ONTOLOGY
    NIR -. "active across" .-> DYNAMICS
    NIR -. "active across" .-> PROJECTION
    NIR -. "active across" .-> AUDIT
```

**Key invariants expressed in this view**

- Φ is reached only through `3Gate → 4ES + QE`; no input enters Φ unmediated.
- K(Φ) and κ are **descriptive predicates**, never optimization targets.
- The Vortex has no access to K(Φ), κ, or Σ — it is pure exploration.
- Projection (L8–L10) is **read-only**; there is no feedback edge back into Φ.
- The Δ backbone and audit layer **observe** the field but cannot write to it.
- NIR is orthogonal to the pipeline — it applies at every layer simultaneously.

---

## 2. Σ Geometry — The 8 Axiomatic Poles of Φ

The field Φ is stabilized by eight non-hierarchical axiomatic centers Σ₁…Σ₈
connected by 28 relational tensions (R ∈ so(8), antisymmetric).
No pole has authority; triality (INT / LEX / VER) acts as a structural symmetry.

```mermaid
flowchart TB
    classDef pole fill:#fff3b0,stroke:#6d2e46,stroke-width:1.5px,color:#3d1308
    classDef center fill:#f6bd60,stroke:#6d2e46,stroke-width:2px,color:#3d1308

    INT(["INT · ZÁMER"]):::pole
    LEX(["LEX · EXISTENCIA"]):::pole
    VER(["VER · PRAVDA"]):::pole
    LIB(["LIB · SLOBODA"]):::pole
    UNI(["UNI · JEDNOTA"]):::pole
    REL(["REL · VZÁJOMNOSŤ"]):::pole
    WIS(["WIS · MÚDROSŤ"]):::pole
    CRE(["CRE · TVORBA"]):::pole

    PHI(("Φ · Epistemic Field<br/>R ∈ so(8)<br/>28 tensions")):::center

    INT --- PHI
    LEX --- PHI
    VER --- PHI
    LIB --- PHI
    UNI --- PHI
    REL --- PHI
    WIS --- PHI
    CRE --- PHI

    INT --- LEX
    LEX --- VER
    VER --- LIB
    LIB --- UNI
    UNI --- REL
    REL --- WIS
    WIS --- CRE
    CRE --- INT
```

---

## 3. Triadic Repository Layering — OAAT

VECTAETOS is one of three repositories forming an **Ontologically Asymmetric
Architectural Triality** (OAAT). The only valid information flow is downward
(ontology → simulation → dialogue). Upward flows are contractually forbidden
(`contracts/LAYER_BOUNDARIES.md`).

```mermaid
flowchart TB
    classDef vect fill:#f6bd60,stroke:#6d2e46,stroke-width:2px,color:#3d1308
    classDef asim fill:#bde0fe,stroke:#023e8a,color:#023047
    classDef mod  fill:#caf0f8,stroke:#0077b6,color:#03045e
    classDef audit fill:#ffb4a2,stroke:#6a040f,color:#370617

    subgraph V ["VECTAETOS™ — Ontology Layer"]
        V1["Φ · Σ₁…Σ₈ · K(Φ) · κ · QE<br/>entropic humility · invariants"]:::vect
    end

    subgraph A ["ASIMULATOR™ — Simulation Layer"]
        A1["Procedural exploration<br/>4ES + QE projection<br/>event modeling · retrieval"]:::asim
    end

    subgraph M ["ASI_MOD™ — Dialogue Layer"]
        M1["Language articulation<br/>working memory · summarization<br/>no ontological authority"]:::mod
    end

    AUDIT[["Audit / Epistemic Cryptography<br/>observe · record · hash — never command"]]:::audit

    V1 ==>|"valid flow"| A1
    A1 ==>|"valid flow"| M1

    M1 -. "forbidden" .-> A1
    M1 -. "forbidden" .-> V1
    A1 -. "forbidden" .-> V1
    AUDIT -. "forbidden as authority" .-> V1

    V1 -. "observed by" .-> AUDIT
    A1 -. "observed by" .-> AUDIT
    M1 -. "observed by" .-> AUDIT
```

---

## 4. CI / Governance Guardrails

The architectural constraints above are mechanically enforced by repository CI.
Every PR must pass these ontology guards before merge — they are the **operational
projection** of the non-agentic policy.

```mermaid
flowchart LR
    classDef ci fill:#e9c46a,stroke:#6d2e46,color:#3d1308
    classDef rule fill:#dde5b6,stroke:#606c38,color:#283618
    classDef gate fill:#2a2a2a,stroke:#f6bd60,stroke-width:2px,color:#f6bd60

    PR(["Pull Request"]):::rule

    subgraph GUARDS [".github/workflows"]
        direction TB
        G1["ontology_guard.yml"]:::ci
        G2["canonical_guard.yml"]:::ci
        G3["canonical-anchor.yml"]:::ci
        G4["anchor-hash.yml"]:::ci
        G5["phi_integrity.yml"]:::ci
        G6["phi_state.yml + phi_state_pr.yml"]:::ci
        G7["determinism.yml"]:::ci
        G8["vortex_determinism.yml"]:::ci
        G9["repo-boundaries.yml"]:::ci
        G10["observatory.yml"]:::ci
    end

    POLICY["governance/NON_AGENTIC_POLICY.md<br/>governance/ONTOLOGY_RULES.md<br/>governance/LANGUAGE_CONSTRAINTS.md"]:::rule
    IL["importlinter.ini<br/>layer import boundaries"]:::rule
    ANCHORS["ANCHOR_INDEX.md<br/>CANONICAL_ANCHORS.md"]:::rule

    MERGE{{"Merge gate"}}:::gate

    PR --> GUARDS
    POLICY --> GUARDS
    IL --> GUARDS
    ANCHORS --> GUARDS
    GUARDS --> MERGE
```

---

## 5. Unified Cross-Section (All Layers at Once)

This is the "one picture" view — depth, triality and audit superimposed.
It is intentionally dense: it is the diagram to print and pin to a wall.

```mermaid
flowchart TB
    classDef human fill:#f4f1de,stroke:#3d405b,color:#3d405b
    classDef gate fill:#e7ecef,stroke:#274c77,color:#274c77
    classDef field fill:#f6bd60,stroke:#6d2e46,stroke-width:2px,color:#3d1308
    classDef kernel fill:#e9c46a,stroke:#6d2e46,color:#3d1308
    classDef vortex fill:#cdb4db,stroke:#3a2e6d,color:#241041
    classDef proj fill:#bde0fe,stroke:#023e8a,color:#023047
    classDef adapter fill:#caf0f8,stroke:#0077b6,color:#03045e
    classDef audit fill:#ffb4a2,stroke:#6a040f,color:#370617
    classDef delta fill:#dde5b6,stroke:#606c38,color:#283618
    classDef nir fill:#2a2a2a,stroke:#f6bd60,stroke-width:2px,color:#f6bd60

    H(["HUMAN"]):::human

    subgraph VECTAETOS ["VECTAETOS™ · Ontology"]
        direction TB
        G1["3Gate W · D · H"]:::gate
        G2["4ES + QE"]:::gate
        PHI(("Φ · Σ₁…Σ₈<br/>R ∈ so(8)")):::field
        K["K(Φ) · κ"]:::kernel
        DELTA["Δ · canonical · H · κ<br/>EK 2.0 structural backbone"]:::delta
        EK["Epistemic Cryptography<br/>μ · A · h"]:::audit
    end

    subgraph ASIMULATOR ["ASIMULATOR™ · Simulation"]
        direction TB
        VOR["Simulation Vortex Φ(t)<br/>candidate trajectories"]:::vortex
        MEM["ESM · LTL · EAT · MML<br/>memory as trace"]:::audit
    end

    subgraph ASI_MOD ["ASI_MOD™ · Dialogue"]
        direction TB
        PI["Runic Projection Π(Φ)"]:::proj
        LLM["LLM Adapter<br/>render only"]:::adapter
        OUT(["Descriptive output · text · silence · QE"]):::human
    end

    NIR[["NIR · Non-Intervention Regime<br/>active across the entire pipeline"]]:::nir

    H --> G1 --> G2 --> PHI
    PHI --- K
    PHI -. "canonical observation" .-> DELTA
    PHI -. "observed by" .-> EK
    K --> VOR --> MEM
    VOR --> PI --> LLM --> OUT --> H
    DELTA -. "invariants" .-> EK

    NIR -. "all layers" .-> VECTAETOS
    NIR -. "all layers" .-> ASIMULATOR
    NIR -. "all layers" .-> ASI_MOD
```

---

## 6. Legend

| Symbol | Meaning |
| --- | --- |
| Φ | Relational epistemic field — the only primary ontology |
| Σ₁…Σ₈ | Invariant axiomatic centers (INT, LEX, VER, LIB, UNI, REL, WIS, CRE) |
| R ∈ so(8) | Antisymmetric relational matrix; 28 independent tensions |
| Δ = dR | Relational differential; Δ ∈ ℝ⁵⁶, constraint dΔ = 0 |
| K(Φ) | Descriptive coherence predicate (never a score) |
| κ | Representability boundary (never a threshold) |
| 4ES | Epistemic states AA · AN · NA · NN |
| QE | Qualitative Epistemic Aporia — valid non-closure, not an error |
| Π(Φ) | Runic projection — read-only, lossy |
| NIR | Non-Intervention Regime — global, opaque, non-bypassable |
| H(Φ) | Structural hash of canonicalized Δ |

---

## 7. Canonical Closure

> Vectaetos is not powerful because it can act.
> Vectaetos is powerful because **there is nowhere for power to attach.**

This unified diagram is a **projection of the architecture**, not the architecture itself.
All canonical meaning remains fixed in the anchors in `/formal/` and `/contracts/`.

© VECTAETOS™ — UNIFIED_ARCHITECTURE.md
