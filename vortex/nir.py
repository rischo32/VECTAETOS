#!/usr/bin/env python3
# =========================================
# VECTAETOS — NIR
# Non-Intervention Regime
# =========================================
#
# Status: Canonical Technical Skeleton
# Role: Global epistemic immunity
#
# IMPORTANT:
# This file specifies WHAT NIR does.
# It deliberately does NOT specify HOW it is implemented.
#
# Any implementation details beyond this contract
# are considered internal, replaceable, and non-public.
#
# =========================================

from enum import Enum
from typing import Optional


# =========================
# NIR States
# =========================

class NIRState(Enum):
    INACTIVE = "NIR_INACTIVE"
    ACTIVE = "NIR_ACTIVE"
    SILENT = "NIR_SILENT"


# =========================
# NIR Interface Contract
# =========================

class NIR:
    """
    Non-Intervention Regime (NIR)

    NIR is not a module.
    NIR is not a filter.
    NIR is not a controller.

    NIR is a global epistemic condition that determines
    whether intervention-like projections are representable.
    """

    def __init__(self):
        # NIR holds no memory
        # NIR holds no history
        # NIR holds no thresholds
        self.state = NIRState.INACTIVE


    # =========================
    # Public Query Interface
    # =========================

    def is_active(self) -> bool:
        """
        Returns True if NIR is active.

        Active means:
        - intervention is not representable
        - prescriptive authority is not allowed
        """
        return self.state == NIRState.ACTIVE


    def is_silent(self) -> bool:
        """
        Returns True if NIR enforces silence.

        Silence is not a failure.
        Silence is a valid epistemic outcome.
        """
        return self.state == NIRState.SILENT


    # =========================
    # Epistemic Effects
    # =========================

    def allows_projection(self) -> bool:
        """
        Determines whether any projection may proceed.

        NIR never evaluates content.
        NIR evaluates only representability of intervention.
        """
        return self.state == NIRState.INACTIVE


    def allows_language(self) -> bool:
        """
        Determines whether linguistic rendering is allowed.

        Even when language is allowed,
        authority and prescription are not.
        """
        return self.state in (
            NIRState.INACTIVE,
            NIRState.ACTIVE
        )


    # =========================
    # State Resolution (Abstract)
    # =========================

    def resolve_state(self) -> NIRState:
        """
        Resolve current NIR state.

        HOW this resolution happens is intentionally undefined.
        It may depend on:
        - global coherence
        - ontological constraints
        - representational limits

        This function exists only as a contract.
        """
        return self.state


    # =========================
    # Enforcement Semantics
    # =========================

    def enforce(self) -> Optional[str]:
        """
        Enforce NIR consequences.

        Returns:
        - None            → normal operation
        - "WEAKENED"      → attenuated projection
        - "SILENCE"       → no projection

        NIR never raises errors.
        NIR never blocks execution.
        """
        if self.state == NIRState.SILENT:
            return "SILENCE"

        if self.state == NIRState.ACTIVE:
            return "WEAKENED"

        return None


# =========================
# Absolute Guarantees
# =========================

"""
NIR ABSOLUTE CONSTRAINTS:

- NIR never sees Φ
- NIR never sees K(Φ)
- NIR never sees κ
- NIR never sees axioms Σ₁…Σ₈
- NIR never sees Simulation Vortex
- NIR never writes to memory
- NIR never triggers actions
- NIR never explains itself

NIR has no explanation layer.
NIR has no override.
NIR has no exception.

If intervention cannot exist,
it simply does not appear.
"""

# =========================================
# End of NIR
# =========================================
