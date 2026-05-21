# VECTAETOS — Layer 6: Runic Projection Design

## 1. Overview
The **Runic Projection Layer** (Layer 6) serves as the bridge between the mathematical formalism of the Ontological Field (Φ) and the linguistic interpretation of the LLM Adapter (Layer 7). It reduces the high-dimensional relational state of so(8) into a symbolic set of "Runes" that convey the structural "mood" or "health" of the architecture.

## 2. Runic Symbology
The projection uses four primary symbols, representing the four cardinal states of an axiomatic structure:

| Rune | Name | Ontological State | Interpretation |
| :--- | :--- | :--- | :--- |
| **◯** | **Stability** | Coherent ($K=1$), Low Curvature | The architecture is grounded and consistent. The relations are balanced. |
| **△** | **Tension** | Coherent ($K=1$), High Curvature | Structural stress is present. The logic is "strained" but holding. |
| **◇** | **Transition** | Coherent ($K=1$), High Uncertainty | The state is in flux. The Simulation Vortex is generating high variance. |
| **⊘** | **Aporia** | Incoherent ($K=0$) or QE | A logical dead-end. The configuration is unrealizable or "void". |

## 3. Mathematical Mapping (Φ → Runes)

### 3.1. Global System Projection (The Primary Rune)
The global state of Φ is projected into a single **Dominant Rune** using telemetry from `Ψ_EK(Φ)` (deprecated alias `Q_EK` accepted only for legacy input) and the following heuristic:

1.  **If $K_D(\Phi) = 0$ or representability closure fails ($d^2\Delta \neq 0$ within tolerance)**: Global state is **⊘ (Aporia)**.
2.  **Else if $\mu_{tot} > A_{tot}$**: Global state is **◇ (Transition)**.
3.  **Else if $\|\Delta\|_F > \frac{\theta_G}{2}$**: Global state is **△ (Tension)**.
4.  **Else**: Global state is **◯ (Stability)**.

### 3.2. Singularity-Specific Projection
Each of the 8 axiomatic singularities ($\Sigma_i$) is assigned a rune based on its local neighborhood in so(8):

Let the Local Tension $T_i = \sum_{j,k} |\Delta(i, j, k)|$ be the sum of curvatures involving $\Sigma_i$.

- **Σᵢ = ⊘** if $K_D(\Phi) = 0$ (The whole field is collapsed).
- **Σᵢ = ◇** if local uncertainty $\mu_i$ exceeds a local threshold.
- **Σᵢ = △** if $T_i$ exceeds a threshold (e.g., $T_i > 2.0$).
- **Σᵢ = ◯** otherwise.

## 4. Output Format (Runic Stream)
The Projection Layer outputs a "Runic Stream" to the LLM Adapter. This stream is formatted as a structured metadata block to be included in the context.

### 4.1. Formal Schema
```runic
[VECTAETOS:RUNIC_PROJECTION_v1]
FIELD_STATE: <GLOBAL_RUNE>
SYSTEM_K: <1/0>
h_topo: <0.xxxx>

[AXIOM_SINGULARITIES]
INT: <RUNE> | LEX: <RUNE> | VER: <RUNE> | LIB: <RUNE>
UNI: <RUNE> | REL: <RUNE> | WIS: <RUNE> | CRE: <RUNE>

[VORTEX_DENSITY]
TRAJECTORIES: <n>
COHERENCE_YIELD: <percentage>%
```

### 4.2. Example Projection (High Tension State)
```runic
[VECTAETOS:RUNIC_PROJECTION_v1]
FIELD_STATE: △
SYSTEM_K: 1
h_topo: 0.7241

[AXIOM_SINGULARITIES]
INT: ◯ | LEX: △ | VER: ◯ | LIB: ◯
UNI: ◯ | REL: △ | WIS: ◯ | CRE: ◇

[VORTEX_DENSITY]
TRAJECTORIES: 12
COHERENCE_YIELD: 8.3%
```

## 5. Interpretation for LLM Adapter
The LLM Adapter (Layer 7) uses this projection to guide its descriptive output:
- **◯ (Stability)** → Use calm, declarative, and grounded language.
- **△ (Tension)** → Highlight contradictions, trade-offs, and "logical weight".
- **◇ (Transition)** → Emphasize possibility, potentiality, and the "unfolding" of the system.
- **⊘ (Aporia)** → Describe the silence, the void, or the breakdown of the model's ability to represent the request.
