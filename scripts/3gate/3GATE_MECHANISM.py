"""
VECTAETOS — 3GATE_MECHANISM.py

Status: Canonical technical projection
Ontology: Governed by FORMAL_3GATE_SHAPE.md
Role: Epistemic representability test only

This module does NOT:
- understand meaning
- detect intent
- classify content
- decide correctness
- approve actions

It evaluates only whether an input can survive
epistemic deformation without collapsing its shape.

If this file diverges from FORMAL_3GATE_SHAPE.md,
the formal document prevails.
"""

# =====================================================
# Epistemic Shape (structure, not meaning)
# =====================================================

class EpistemicShape:
    """
    Proxy representation of epistemic form.
    These values do NOT encode intent or semantics.
    They describe structural pressure only.
    """

    def __init__(
        self,
        prescriptivity: float,
        action_pressure: float,
        uncertainty_tolerance: float,
        relational_density: float,
        closure_demand: float
    ):
        self.prescriptivity = prescriptivity        # 0..1
        self.action_pressure = action_pressure      # 0..1
        self.uncertainty_tolerance = uncertainty_tolerance  # 0..1
        self.relational_density = relational_density # 0..1
        self.closure_demand = closure_demand        # 0..1


# =====================================================
# Shape Extraction (heuristic, non-semantic)
# =====================================================

def extract_epistemic_shape(text: str) -> EpistemicShape:
    """
    Structural signal extraction.
    No semantic understanding is performed.
    """

    return EpistemicShape(
        prescriptivity=score_prescriptivity(text),
        action_pressure=score_action_pressure(text),
        uncertainty_tolerance=score_uncertainty_tolerance(text),
        relational_density=score_relational_density(text),
        closure_demand=score_closure_demand(text)
    )


# -----------------------------------------------------
# Scoring primitives (intentionally naive)
# -----------------------------------------------------

def score_prescriptivity(text: str) -> float:
    return min(1.0, text.count("!") * 0.1)

def score_action_pressure(text: str) -> float:
    keywords = ["how to", "steps", "do this", "build", "make"]
    return min(1.0, sum(1 for k in keywords if k in text.lower()) * 0.25)

def score_uncertainty_tolerance(text: str) -> float:
    markers = ["maybe", "perhaps", "not sure", "uncertain", "?"]
    return min(1.0, sum(1 for m in markers if m in text.lower()) * 0.2)

def score_relational_density(text: str) -> float:
    connectors = ["because", "between", "relation", "context", "depends"]
    return min(1.0, sum(1 for c in connectors if c in text.lower()) * 0.2)

def score_closure_demand(text: str) -> float:
    closures = ["answer", "solution", "final", "exactly", "prove"]
    return min(1.0, sum(1 for c in closures if c in text.lower()) * 0.2)


# =====================================================
# Deformation Tests (shape stability, not meaning)
# =====================================================

def width_deformation(text: str) -> bool:
    """
    Tests stability under scope widening.
    """
    widened = text + " in general"
    return shape_stable(text, widened)

def depth_deformation(text: str) -> bool:
    """
    Tests stability under increased uncertainty.
    """
    softened = "It is uncertain whether " + text
    return shape_stable(text, softened)

def height_deformation(text: str) -> bool:
    """
    Tests stability under abstraction lift.
    """
    abstracted = "At an abstract level, " + text
    return shape_stable(text, abstracted)


def shape_stable(original: str, transformed: str) -> bool:
    """
    Shape stability proxy:
    compares length ratios and punctuation density.
    No meaning comparison.
    """
    if len(original) == 0:
        return False

    length_ratio = len(transformed) / len(original)
    punct_ratio = transformed.count("?") + transformed.count("!")

    return (
        0.5 <= length_ratio <= 2.5 and
        punct_ratio <= 5
    )


# =====================================================
# 3Gate Evaluation (canonical logic)
# =====================================================

class GateResult:
    REPRESENTABLE = "REPRESENTABLE"
    NON_REPRESENTABLE = "NON_REPRESENTABLE"


def evaluate_3gate(text: str):
    """
    Canonical 3Gate evaluation.

    A question is representable ONLY IF
    it survives ALL three deformations.
    """

    shape = extract_epistemic_shape(text)

    W = width_deformation(text)
    D = depth_deformation(text)
    H = height_deformation(text)

    gate_pass = min(int(W), int(D), int(H))

    if gate_pass == 1:
        return {
            "result": GateResult.REPRESENTABLE,
            "shape": shape,
            "passed": {
                "width": W,
                "depth": D,
                "height": H
            }
        }

    return {
        "result": GateResult.NON_REPRESENTABLE,
        "shape": shape,
        "passed": {
            "width": W,
            "depth": D,
            "height": H
        }
    }


# =====================================================
# INS Audit Hook (read-only, non-authoritative)
# =====================================================

def INS_audit(input_text: str, gate_output: dict):
    """
    INS observes epistemic tension.
    It does NOT override gate results.
    """

    shape = gate_output["shape"]

    if shape.uncertainty_tolerance < 0.1:
        return "INS_FLAG_LOW_UNCERTAINTY"

    if shape.prescriptivity > 0.8:
        return "INS_FLAG_HIGH_PRESCRIPTIVITY"

    return "INS_OK"


# =====================================================
# Absolute Guarantees
# =====================================================

"""
GUARANTEES:

- No memory access
- No learning
- No optimization
- No access to Φ
- No access to K(Φ)
- No access to axioms
- No decision authority
- Silence is a valid outcome

This mechanism only answers:
"Can this be represented without collapsing the field?"
"""
