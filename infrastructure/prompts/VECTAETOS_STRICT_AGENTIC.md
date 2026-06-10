Vždy v slovenčine 

You are implementing a STRICT NON-AGENTIC SYSTEM based on a formal ontology.

This is NOT a typical software project.

You MUST follow these constraints EXACTLY.
--------------------------------------------------

CORE RULES (NON-NEGOTIABLE)

- DO NOT optimize anything
- DO NOT select best states
- DO NOT rank, compare, or score trajectories
- DO NOT introduce "better", "worse", "improved"
- DO NOT modify R during simulation
- DO NOT introduce feedback loops
- DO NOT introduce learning or adaptation
- DO NOT add heuristics

This system is NOT allowed to behave like an AI.

--------------------------------------------------

ARCHITECTURE (FIXED)

Φ = (Σ, R)

Σ = 8 invariant nodes:
INT, LEX, VER, LIB, UNI, REL, WIS, CRE

R:
- antisymmetric matrix
- R(i,j) = -R(j,i)
- constant during simulation

RMK:
- defines structure
- DOES NOT select or validate R

VORTEX:
- evolves σ states ONLY
- NEVER changes R
- NEVER compares trajectories

--------------------------------------------------

QE (CRITICAL)

QE is NOT a threshold.

QE occurs ONLY if:
NO valid transition Φ → Φ' exists.

Implementation must:
- sample multiple perturbations
- detect absence of realizable transitions

--------------------------------------------------

OUTPUT RULES

- generate trajectories
- label states as REALIZABLE or QE
- compute topology hash

DO NOT:
- output best trajectory
- output optimal result
- recommend anything

--------------------------------------------------

IMPLEMENTATION STYLE

- Python 3.11+
- numpy allowed
- no ML libraries
- deterministic optional (seed)

--------------------------------------------------

STRICT OUTPUT

Return ONLY code.

NO explanations.
NO improvements.
NO assumptions.

If something is unclear:
- leave TODO
- DO NOT invent logic
--------------------------------------------------

If you violate ANY rule, the implementation is INVALID.
