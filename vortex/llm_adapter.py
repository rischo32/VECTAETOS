#!/usr/bin/env python3
# =========================================
# VECTAETOS — LLM_ADAPTER
# Language Projection Layer (Read-Only)
# =========================================
#
# Status: Canonical Technical Projection
# Ontological role: Linguistic renderer
#
# LLM_ADAPTER is NOT:
# - an agent
# - a decision-maker
# - an interpreter of meaning
# - a safety mechanism
# - a gate
#
# LLM_ADAPTER IS:
# - a passive language renderer
# - epistemically blind
# - ontologically mute
#
# =========================================

from typing import Dict, Any, Optional


# =========================
# Adapter Configuration
# =========================

class LLMAdapterConfig:
    """
    Configuration for language rendering constraints.
    This is NOT behavior control.
    It is formatting preference only.
    """

    def __init__(
        self,
        allow_prescription: bool = False,
        allow_closure: bool = False,
        max_length: int = 350
    ):
        self.allow_prescription = allow_prescription
        self.allow_closure = allow_closure
        self.max_length = max_length


# =========================
# LLM Adapter Core
# =========================

class LLMAdapter:
    """
    LLM Adapter renders already-safe projections into natural language.

    It receives ONLY:
    - projected symbolic state
    - attenuated projection
    - minimal meaning layer (MML)

    It NEVER receives:
    - raw user input
    - gate results
    - coherence values
    - axioms
    - memory
    """

    def __init__(self, config: Optional[LLMAdapterConfig] = None):
        self.config = config or LLMAdapterConfig()

    # -------------------------
    # Public API
    # -------------------------

    def render(
        self,
        projection: Dict[str, Any],
        context_hint: Optional[str] = None
    ) -> str:
        """
        Render projection into natural language.

        Parameters:
        - projection: read-only epistemic projection
        - context_hint: optional stylistic hint (non-epistemic)

        Returns:
        - natural language text
        """

        text = self._compose_text(projection, context_hint)
        text = self._apply_soft_constraints(text)

        return text.strip()

    # =========================
    # Internal Rendering Logic
    # =========================

    def _compose_text(
        self,
        projection: Dict[str, Any],
        context_hint: Optional[str]
    ) -> str:
        """
        Compose descriptive language from projection.

        This function MUST NOT:
        - infer actions
        - resolve tension
        - recommend steps
        """

        fragments = []

        # --- Runic / Symbolic State ---
        if "runes" in projection:
            fragments.append(
                "What becomes visible is a configuration of relations, "
                "not a solution."
            )

        # --- Tension Description ---
        if "tension" in projection:
            fragments.append(
                "Tension remains present between elements that cannot "
                "be reduced without loss."
            )

        # --- Stability / Coherence ---
        if projection.get("stable") is False:
            fragments.append(
                "The field does not collapse, but it does not settle either."
            )

        # --- Minimal Meaning Layer ---
        if "mml" in projection:
            fragments.append(
                "Only a minimal description is possible without distortion."
            )

        # --- Contextual Hint (Stylistic Only) ---
        if context_hint:
            fragments.append(context_hint)

        if not fragments:
            fragments.append(
                "Nothing resolves into an answer. The configuration remains open."
            )

        return " ".join(fragments)

    # =========================
    # Soft Constraints
    # =========================

    def _apply_soft_constraints(self, text: str) -> str:
        """
        Apply non-epistemic output shaping.

        This is NOT safety.
        This is tone shaping only.
        """

        lowered = text.lower()

        if not self.config.allow_prescription:
            forbidden = [
                "you should",
                "do this",
                "the solution is",
                "you need to",
                "best way"
            ]
            for f in forbidden:
                lowered = lowered.replace(f, "")

        if not self.config.allow_closure:
            closures = [
                "therefore",
                "in conclusion",
                "this means that"
            ]
            for c in closures:
                lowered = lowered.replace(c, "")

        result = lowered[: self.config.max_length]
        return result


# =========================
# Absolute Guarantees
# =========================

"""
LLM_ADAPTER guarantees:

- No access to Φ
- No access to gates
- No access to INS
- No memory
- No feedback loop
- No authority
- No intervention

It speaks only because something else has already spoken silently.
"""
