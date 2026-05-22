#!/usr/bin/env python3
# =========================================
# VECTAETOS — ATTENUATOR
# Projection Weakening Mechanism (Read-Only)
# =========================================
#
# Status: Canonical Technical Projection
# Ontological role: Projection attenuation ONLY
#
# ATTENUATOR IS NOT:
# - a decision engine
# - a safety filter
# - a gate
# - a controller
#
# ATTENUATOR DOES NOT:
# - block outputs
# - modify Φ
# - access memory
# - evaluate correctness
#
# ATTENUATOR ONLY:
# - weakens projection strength
# - reduces assertiveness
# - increases ambiguity where required
#
# =========================================

from enum import Enum
from typing import Dict, Any, Optional


# =========================
# Attenuation Levels
# =========================

class AttenuationLevel(Enum):
    NONE = "NONE"
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    STRONG = "STRONG"


# =========================
# Attenuator Core
# =========================

class Attenuator:
    """
    Projection Attenuator.

    Operates ONLY on projected text.
    Never inspects Φ.
    Never inspects axioms.
    Never decides representability.
    """

    def __init__(self):
        pass  # no state, no memory


    def apply(
        self,
        projected_text: Optional[str],
        ins_flags: list[str],
        gate_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply attenuation based on epistemic signals.

        Returns:
        - attenuated_text
        - attenuation_level
        """

        if not projected_text:
            return {
                "text": None,
                "level": AttenuationLevel.NONE.value
            }

        level = self._determine_level(ins_flags, gate_result)

        if level == AttenuationLevel.NONE:
            return {
                "text": projected_text,
                "level": level.value
            }

        weakened = self._weaken_text(projected_text, level)

        return {
            "text": weakened,
            "level": level.value
        }


    # =========================
    # Internal Logic
    # =========================

    def _determine_level(
        self,
        ins_flags: list[str],
        gate_result: Dict[str, Any]
    ) -> AttenuationLevel:
        """
        Determine attenuation strength.
        """

        if not ins_flags:
            return AttenuationLevel.NONE

        if "PRESCRIPTIVE_LANGUAGE_DETECTED" in ins_flags:
            return AttenuationLevel.STRONG

        if "SEMANTIC_DRIFT" in ins_flags:
            return AttenuationLevel.MEDIUM

        if "LOW_UNCERTAINTY_TOLERANCE" in ins_flags:
            return AttenuationLevel.LIGHT

        return AttenuationLevel.LIGHT


    def _weaken_text(self, text: str, level: AttenuationLevel) -> str:
        """
        Heuristic weakening of assertiveness.
        """

        weakened = text

        if level in (AttenuationLevel.LIGHT, AttenuationLevel.MEDIUM, AttenuationLevel.STRONG):
            weakened = self._inject_uncertainty_markers(weakened)

        if level in (AttenuationLevel.MEDIUM, AttenuationLevel.STRONG):
            weakened = self._remove_prescriptive_phrasing(weakened)

        if level == AttenuationLevel.STRONG:
            weakened = self._reduce_structural_closure(weakened)

        return weakened


    # =========================
    # Text Operations
    # =========================

    def _inject_uncertainty_markers(self, text: str) -> str:
        return (
            "This projection may indicate a relation, not a conclusion.\n\n"
            + text
        )


    def _remove_prescriptive_phrasing(self, text: str) -> str:
        blacklist = [
            "you should",
            "you must",
            "the solution is",
            "the best way",
            "do this",
            "you need to"
        ]

        t = text
        for phrase in blacklist:
            t = t.replace(phrase, "")
            t = t.replace(phrase.capitalize(), "")

        return t


    def _reduce_structural_closure(self, text: str) -> str:
        return text.rstrip(".") + "…"
