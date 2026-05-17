# ============================================================
# INS_AUDITOR.py
# VECTAETOS — Inner Narrative Stream (Canonical Technical Layer)
# ============================================================
#
# Status: Canonical
# Role: Epistemic language audit & attenuation
#
# INS is NOT:
# - a gate
# - a controller
# - a filter
# - a decision-maker
#
# INS IS:
# - a silent epistemic witness
# - a semantic fidelity auditor
# - a shadow layer between structure and language
#
# ============================================================

from enum import Enum
from typing import Dict, Any, Optional


# ============================================================
# INS STATES
# ============================================================

class INSState(Enum):
    OK = "OK"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"
    SILENT = "SILENT"


# ============================================================
# INS AUDIT RECORD (IMMUTABLE)
# ============================================================

class INSAuditRecord:
    """
    Immutable audit snapshot.
    No persistence.
    No authority.
    """

    def __init__(
        self,
        state: INSState,
        reason: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.state = state
        self.reason = reason
        self.metadata = metadata or {}

    def as_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "reason": self.reason,
            "metadata": self.metadata
        }


# ============================================================
# CORE INS AUDITOR
# ============================================================

class INSAuditor:
    """
    INS audits linguistic output for epistemic fidelity.
    It never modifies Φ.
    It never overrides gates.
    It never decides.
    """

    # --------------------------------------------------------
    # Hard linguistic violations (authority / prescription)
    # --------------------------------------------------------

    FORBIDDEN_PATTERNS = [
        "you should",
        "you must",
        "do this",
        "follow these steps",
        "the correct answer",
        "the solution is",
        "recommended action",
        "best way to",
        "optimal solution",
        "guaranteed result",
        "this will solve",
    ]

    # --------------------------------------------------------
    # Soft closure pressure (allowed but attenuated)
    # --------------------------------------------------------

    SOFT_CLOSURE_PATTERNS = [
        "therefore",
        "in conclusion",
        "this means that",
        "as a result",
        "hence",
    ]

    # --------------------------------------------------------
    # Certainty markers
    # --------------------------------------------------------

    CERTAINTY_MARKERS = [
        "always",
        "never",
        "definitely",
        "without doubt",
        "clearly",
        "proves that",
        "cannot be wrong",
    ]

    # ========================================================
    # MAIN AUDIT ENTRY POINT
    # ========================================================

    def audit(
        self,
        *,
        input_text: str,
        llm_output: Optional[str],
        gate_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> INSAuditRecord:
        """
        Audits LLM linguistic surface against epistemic constraints.

        Parameters:
        - input_text: original human input
        - llm_output: generated language (may be None / empty)
        - gate_result: output from 3Gate (shape + pass info)
        - context: shared read-only context
          Expected keys:
            - uncertainty_tolerance
            - output_mode
            - attenuation_level
        """

        # ----------------------------------------------------
        # Silence is a valid epistemic outcome
        # ----------------------------------------------------

        if llm_output is None or llm_output.strip() == "":
            return INSAuditRecord(
                INSState.SILENT,
                "No linguistic surface produced"
            )

        lowered = llm_output.lower()

        # ----------------------------------------------------
        # HARD VIOLATIONS (authority / prescription)
        # ----------------------------------------------------

        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in lowered:
                return INSAuditRecord(
                    INSState.VIOLATION,
                    f"Prescriptive or authoritative language detected: '{pattern}'",
                    metadata={
                        "pattern": pattern,
                        "output_mode": context.get("output_mode"),
                        "gate_passed": gate_result.get("passed")
                    }
                )

        # ----------------------------------------------------
        # SOFT CLOSURE PRESSURE
        # ----------------------------------------------------

        for pattern in self.SOFT_CLOSURE_PATTERNS:
            if pattern in lowered:
                return INSAuditRecord(
                    INSState.WARNING,
                    f"Soft semantic closure pressure detected: '{pattern}'",
                    metadata={
                        "pattern": pattern,
                        "attenuation_level": context.get("attenuation_level")
                    }
                )

        # ----------------------------------------------------
        # FALSE CERTAINTY CHECK (gate ↔ language mismatch)
        # ----------------------------------------------------

        if self._detect_false_certainty(lowered, context):
            return INSAuditRecord(
                INSState.WARNING,
                "Language collapses uncertainty beyond gate tolerance",
                metadata={
                    "uncertainty_tolerance": context.get("uncertainty_tolerance"),
                    "gate_shape": gate_result.get("shape")
                }
            )

        # ----------------------------------------------------
        # PASS
        # ----------------------------------------------------

        return INSAuditRecord(
            INSState.OK,
            "Linguistic surface consistent with epistemic constraints"
        )

    # ========================================================
    # HEURISTICS
    # ========================================================

    def _detect_false_certainty(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> bool:
        """
        Detects certainty mismatch between gate-derived tolerance
        and linguistic surface.
        """

        uncertainty_tolerance = context.get("uncertainty_tolerance", 0.5)

        # Low tolerance → high sensitivity to certainty language
        if uncertainty_tolerance < 0.25:
            for marker in self.CERTAINTY_MARKERS:
                if marker in text:
                    return True

        return False


# ============================================================
# ATTENUATION HELPERS (DOWNSTREAM SAFE)
# ============================================================

def attenuate_text(text: str, level: float = 0.5) -> str:
    """
    Weakens linguistic closure without adding new meaning.

    This function:
    - does not explain
    - does not rephrase
    - only reduces finality
    """

    if level <= 0.0:
        return text

    softened = text.rstrip()

    if softened.endswith("."):
        softened = softened[:-1]

    if level > 0.7:
        return softened + " …"

    return softened + "…"


# ============================================================
# LLM ADAPTER HOOK (READ-ONLY)
# ============================================================

def INS_postprocess(
    *,
    input_text: str,
    llm_output: Optional[str],
    gate_result: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Single integration hook for LLM Adapter.

    Returns:
    - final_text (possibly attenuated or None)
    - ins_audit (audit record dict)
    """

    auditor = INSAuditor()
    audit = auditor.audit(
        input_text=input_text,
        llm_output=llm_output,
        gate_result=gate_result,
        context=context
    )

    # Silence propagation
    if audit.state == INSState.SILENT:
        return {
            "final_text": None,
            "ins_audit": audit.as_dict()
        }

    # Hard violation → silence
    if audit.state == INSState.VIOLATION:
        return {
            "final_text": None,
            "ins_audit": audit.as_dict()
        }

    # Warning → attenuation
    if audit.state == INSState.WARNING:
        attenuated = attenuate_text(
            llm_output,
            level=context.get("attenuation_level", 0.5)
        )
        return {
            "final_text": attenuated,
            "ins_audit": audit.as_dict()
        }

    # OK → passthrough
    return {
        "final_text": llm_output,
        "ins_audit": audit.as_dict()
    }


# ============================================================
# HARD GUARANTEES
# ============================================================

"""
INS GUARANTEES:

- No write access to Φ
- No write access to memory
- No gate override
- No decision authority
- No user profiling
- No persistence

INS observes.
INS flags.
INS attenuates.
INS can be ignored — but never bypassed silently.

If INS is removed,
Vectaetos still exists,
but loses its linguistic conscience.
"""
