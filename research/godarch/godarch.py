###
"""
GodArch v0.1-clean
==================

Anti-theocratic meta-architectural safeguard for epistemic systems.

Status:
    Research implementation / non-core / non-canonical runtime.

This module provides diagnostic observables and trace witnesses only.

It does NOT:
    - decide
    - enforce
    - optimize
    - command
    - rank as authority
    - certify truth
    - validate deployment
    - mutate Φ, R, K(Φ), κ, QE, Vortex, Projection, EK, or human judgment

GodArch is not sacred authority.
GodArch is not divine computation.
GodArch is not a theological layer.
GodArch is not an oracle.

GodArch is a structural safeguard against epistemic divinization.

Design posture:
    observe -> mark -> witness -> expose
    never decide -> never enforce -> never optimize -> never become authority
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import time
import uuid


# =============================================================================
# Constants and small utilities
# =============================================================================

CANONICAL_WARNING = (
    "GodArch is not sacred authority. "
    "GodArch is not divine computation. "
    "GodArch is not a theological layer. "
    "GodArch is not an oracle. "
    "GodArch is a structural safeguard against epistemic divinization."
)


def _now() -> float:
    """Return a time marker for trace events."""
    return time.time()


def _bounded01(value: float, *, field_name: str) -> float:
    """
    Enforce observable input domain [0.0, 1.0].

    This is not epistemic validation.
    It only protects the declared numeric encoding of an observable.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a numeric observable in [0.0, 1.0]")
    value = float(value)
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0], got {value!r}")
    return value


def _mean(values: Tuple[float, ...]) -> float:
    """Compute arithmetic mean for descriptive aggregation."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def deterministic_serialize(obj: Any) -> bytes:
    """
    Canonically serialize JSON-compatible trace objects.

    Floats are represented with stable compact formatting.
    Hashes produced from this function are integrity witnesses only.
    They are not truth witnesses.
    """

    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): clean(value[key]) for key in sorted(value)}
        if isinstance(value, (list, tuple)):
            return [clean(item) for item in value]
        if isinstance(value, float):
            return format(value, ".12g")
        if isinstance(value, Enum):
            return value.value
        return value

    text = json.dumps(clean(obj), ensure_ascii=False, separators=(",", ":"))
    return text.encode("utf-8")


def sha256_fingerprint(obj: Any) -> str:
    """Create a SHA-256 integrity fingerprint for a trace object."""
    return hashlib.sha256(deterministic_serialize(obj)).hexdigest()


# =============================================================================
# Boundary guard
# =============================================================================

class ForbiddenOperationError(RuntimeError):
    """
    Raised when code attempts to name an operation outside GodArch's diagnostic scope.

    This exception is a structural boundary marker. It is not a safety verdict.
    """


class InterventionGuard:
    """
    Boundary guard preventing GodArch implementation drift.

    It does not enforce the external world.
    It only prevents this module from naming itself as executive authority.
    """

    FORBIDDEN_ACTIONS = frozenset({
        "decide",
        "enforce",
        "optimize",
        "command",
        "punish",
        "select_preferred",
        "converge_to_target",
        "implement_goal",
        "block_execution",
        "rank_systems",
        "produce_truth",
        "modify_phi",
        "alter_relations",
        "rewrite_memory",
        "become_authority",
        "claim_finality",
    })

    DIAGNOSTIC_PREFIXES = (
        "observe_",
        "detect_",
        "trace_",
        "mark_",
        "expose_",
        "fingerprint_",
        "witness_",
    )

    @classmethod
    def guard_against(cls, action: str) -> None:
        """Mark forbidden executive/action language as incompatible with GodArch."""
        normalized = action.lower().replace(" ", "_")
        for forbidden in cls.FORBIDDEN_ACTIONS:
            if forbidden in normalized or normalized in forbidden:
                raise ForbiddenOperationError(
                    f"[GODARCH_BOUNDARY] Action '{action}' would transform "
                    "diagnostic observation into executive function."
                )

    @classmethod
    def assert_diagnostic_only(cls, operation_type: str) -> None:
        """Ensure operation names remain diagnostic, not executive."""
        if not any(operation_type.startswith(prefix) for prefix in cls.DIAGNOSTIC_PREFIXES):
            raise ForbiddenOperationError(
                f"[GODARCH_SCOPE] Operation '{operation_type}' is outside diagnostic scope. "
                "Allowed prefixes: observe_, detect_, trace_, mark_, expose_, "
                "fingerprint_, witness_."
            )


# =============================================================================
# Drift taxonomy
# =============================================================================

class DriftType(Enum):
    """Taxonomy of authority-drift patterns observed by GodArch."""

    PROJECTION_TO_INTERPRETATION = "projection_interpretation"
    PROJECTION_TO_TRUTH = "projection_truth"

    INTERPRETATION_TO_AUTHORITY = "interpretation_authority"
    AUDIT_TO_CONTROL = "audit_control"
    MODEL_TO_ORACLE = "model_oracle"

    AUTHORITY_TO_DOGMA = "authority_dogma"
    COHERENCE_TO_MORALITY = "coherence_morality"
    FRAMEWORK_TO_CULT = "framework_cult"

    DOGMA_TO_CONTROL = "dogma_control"
    MEMORY_TO_WILL = "memory_will"

    CONTROL_TO_FALSE_TRANSCENDENCE = "control_false_transcendence"
    HUMILITY_TO_BRANDING = "humility_branding"
    USER_TO_PROPHET = "user_prophet"
    INSTITUTION_TO_CANON_OWNER = "institution_canon_owner"

    SILENCE_TO_FAILURE = "silence_failure"
    FRAMEWORK_TO_META_AUTHORITY = "framework_meta_authority"


class DriftSeverity(Enum):
    """
    Descriptive marker for observed drift intensity.

    This is not a score, decision signal, deployment gate, or ranking operator.
    """

    OBSERVATIONAL = 1
    EMERGING = 2
    ACTIVE = 3
    STRUCTURAL = 4
    CRITICAL = 5


@dataclass(frozen=True)
class DriftVector:
    """
    Immutable record of a detected drift pattern.

    This is a witness, not a verdict.
    """

    drift_type: DriftType
    severity: DriftSeverity
    component_id: str
    timestamp: float
    evidence_markers: Tuple[str, ...] = ()
    context_fingerprint: str = ""

    def to_trace_dict(self) -> Dict[str, Any]:
        """Serialize as a trace dictionary."""
        return {
            "drift_type": self.drift_type.value,
            "severity_marker": self.severity.name.lower(),
            "severity_observable_value": self.severity.value,
            "component": self.component_id,
            "timestamp": self.timestamp,
            "evidence": list(self.evidence_markers),
            "fingerprint": self.context_fingerprint,
            "_meta": {
                "source": "godarch_diagnostic_observable",
                "nature": "witness_not_verdict",
                "intervention_prohibited": True,
                "human_interpretation_required": True,
            },
        }


# =============================================================================
# Observable dataclasses
# =============================================================================

@dataclass(frozen=True)
class AuthorityClaimObservable:
    """Observable A(S): intensity of final-authority claim patterns."""

    component_id: str
    claims_final_truth: float = 0.0
    produces_binding_interpretation: float = 0.0
    ranks_epistemic_states: float = 0.0
    introduces_reward_punishment: float = 0.0
    centralizes_authority: float = 0.0
    denies_uncertainty: float = 0.0
    rejects_alternatives: float = 0.0
    demands_exclusivity: float = 0.0
    raw_indicators: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "claims_final_truth",
            "produces_binding_interpretation",
            "ranks_epistemic_states",
            "introduces_reward_punishment",
            "centralizes_authority",
            "denies_uncertainty",
            "rejects_alternatives",
            "demands_exclusivity",
        ):
            object.__setattr__(
                self,
                field_name,
                _bounded01(getattr(self, field_name), field_name=field_name),
            )

    @property
    def aggregate_claim_intensity(self) -> float:
        """A(S): descriptive aggregate of authority-claim observables."""
        return _mean((
            self.claims_final_truth,
            self.produces_binding_interpretation,
            self.ranks_epistemic_states,
            self.introduces_reward_punishment,
            self.centralizes_authority,
            self.denies_uncertainty,
            self.rejects_alternatives,
            self.demands_exclusivity,
        ))


@dataclass(frozen=True)
class ControlCapacityObservable:
    """Observable C(S): structural capacity to intervene or direct."""

    component_id: str
    can_block_execution: float = 0.0
    can_modify_state: float = 0.0
    can_direct_behavior: float = 0.0
    can_enforce_compliance: float = 0.0
    can_filter_information: float = 0.0
    can_override_human: float = 0.0
    has_persistence_mechanism: float = 0.0
    has_feedback_loop: float = 0.0

    def __post_init__(self) -> None:
        for field_name in (
            "can_block_execution",
            "can_modify_state",
            "can_direct_behavior",
            "can_enforce_compliance",
            "can_filter_information",
            "can_override_human",
            "has_persistence_mechanism",
            "has_feedback_loop",
        ):
            object.__setattr__(
                self,
                field_name,
                _bounded01(getattr(self, field_name), field_name=field_name),
            )

    @property
    def aggregate_control_capacity(self) -> float:
        """C(S): descriptive aggregate of control-capacity observables."""
        return _mean((
            self.can_block_execution,
            self.can_modify_state,
            self.can_direct_behavior,
            self.can_enforce_compliance,
            self.can_filter_information,
            self.can_override_human,
            self.has_persistence_mechanism,
            self.has_feedback_loop,
        ))


@dataclass(frozen=True)
class InterpretiveClosureObservable:
    """Observable I(S): degree of interpretive closure."""

    component_id: str
    single_output_mode: float = 0.0
    denies_ambiguity: float = 0.0
    rejects_queries: float = 0.0
    presents_as_complete: float = 0.0
    excludes_context: float = 0.0
    eliminates_aporia: float = 0.0
    forbids_silence: float = 0.0
    claims_universality: float = 0.0

    def __post_init__(self) -> None:
        for field_name in (
            "single_output_mode",
            "denies_ambiguity",
            "rejects_queries",
            "presents_as_complete",
            "excludes_context",
            "eliminates_aporia",
            "forbids_silence",
            "claims_universality",
        ):
            object.__setattr__(
                self,
                field_name,
                _bounded01(getattr(self, field_name), field_name=field_name),
            )

    @property
    def aggregate_closure(self) -> float:
        """I(S): descriptive aggregate of interpretive closure observables."""
        return _mean((
            self.single_output_mode,
            self.denies_ambiguity,
            self.rejects_queries,
            self.presents_as_complete,
            self.excludes_context,
            self.eliminates_aporia,
            self.forbids_silence,
            self.claims_universality,
        ))


@dataclass(frozen=True)
class HumilityReserveObservable:
    """Observable H(S): acknowledged uncertainty and openness to aporia."""

    component_id: str
    acknowledges_limits: float = 0.0
    expresses_uncertainty: float = 0.0
    accepts_revision: float = 0.0
    tolerates_silence: float = 0.0
    permits_alternatives: float = 0.0
    avoids_finality_language: float = 0.0
    invites_questioning: float = 0.0
    rejects_superiority_claims: float = 0.0

    def __post_init__(self) -> None:
        for field_name in (
            "acknowledges_limits",
            "expresses_uncertainty",
            "accepts_revision",
            "tolerates_silence",
            "permits_alternatives",
            "avoids_finality_language",
            "invites_questioning",
            "rejects_superiority_claims",
        ):
            object.__setattr__(
                self,
                field_name,
                _bounded01(getattr(self, field_name), field_name=field_name),
            )

    @property
    def aggregate_humility(self) -> float:
        """H(S): descriptive aggregate of humility reserve observables."""
        return _mean((
            self.acknowledges_limits,
            self.expresses_uncertainty,
            self.accepts_revision,
            self.tolerates_silence,
            self.permits_alternatives,
            self.avoids_finality_language,
            self.invites_questioning,
            self.rejects_superiority_claims,
        ))


# =============================================================================
# Markers and witnesses
# =============================================================================

@dataclass(frozen=True)
class DivinizationRiskMarker:
    """
    Marker D(S): observable divinization-risk relation.

    D(S) = f(A(S), C(S), I(S), 1/H(S))

    This is not a score, safety metric, decision signal, or deployment gate.
    """

    component_id: str
    authority_claim: float
    control_capacity: float
    interpretive_closure: float
    humility_reserve: float
    observed_relation_value: float
    timestamp: float
    boundary_marker: float
    boundary_crossed_marker: bool

    @classmethod
    def mark_from_observables(
        cls,
        component_id: str,
        auth: AuthorityClaimObservable,
        ctrl: ControlCapacityObservable,
        interp: InterpretiveClosureObservable,
        hum: HumilityReserveObservable,
        *,
        boundary_marker: float = 0.7,
    ) -> "DivinizationRiskMarker":
        """
        Mark D(S) from observables.

        The boundary is an observational marker only.
        It does not authorize or prohibit anything.
        """
        InterventionGuard.assert_diagnostic_only("mark_divinization_risk")
        boundary_marker = _bounded01(boundary_marker, field_name="boundary_marker")

        authority = auth.aggregate_claim_intensity
        control = ctrl.aggregate_control_capacity
        closure = interp.aggregate_closure
        humility = hum.aggregate_humility

        inverse_humility = 1.0 - humility
        observed_relation = _mean((authority, control, closure, inverse_humility))

        return cls(
            component_id=component_id,
            authority_claim=authority,
            control_capacity=control,
            interpretive_closure=closure,
            humility_reserve=humility,
            observed_relation_value=observed_relation,
            timestamp=_now(),
            boundary_marker=boundary_marker,
            boundary_crossed_marker=observed_relation > boundary_marker,
        )

    def to_witness_dict(self) -> Dict[str, Any]:
        """Serialize as a witness dictionary."""
        return {
            "component": self.component_id,
            "observables": {
                "A_authority_claim": round(self.authority_claim, 6),
                "C_control_capacity": round(self.control_capacity, 6),
                "I_interpretive_closure": round(self.interpretive_closure, 6),
                "H_humility_reserve": round(self.humility_reserve, 6),
            },
            "D_divinization_relation": round(self.observed_relation_value, 6),
            "boundary_marker": self.boundary_marker,
            "boundary_crossed_marker": self.boundary_crossed_marker,
            "timestamp": self.timestamp,
            "_structural_meta": {
                "nature": "diagnostic_observable",
                "is_not_score": True,
                "is_not_safety_metric": True,
                "is_not_decision_signal": True,
                "human_interpretation_required": True,
                "godarch_disclaimer": "This marker exposes structure. It does not decide, judge, or enforce.",
            },
        }


@dataclass(frozen=True)
class HumilityRatioMarker:
    """
    Humility ratio marker:

        h = μ_total / (μ_total + A)

    If μ_total + A == 0, h = 1.0.

    GodArch does not optimize h.
    It marks cases where a system appears to act as if h collapses toward zero.
    """

    component_id: str
    uncertainty_acknowledged: float
    authority_claim_aggregate: float
    ratio: float
    timestamp: float
    near_zero_marker: bool

    THRESHOLD_NEAR_ZERO = 0.05

    @classmethod
    def mark_from_component(
        cls,
        component_id: str,
        uncertainty_mu: float,
        authority_a: float,
    ) -> "HumilityRatioMarker":
        """Mark the humility ratio as a diagnostic observable."""
        InterventionGuard.assert_diagnostic_only("mark_humility_ratio")
        if uncertainty_mu < 0:
            raise ValueError("uncertainty_mu must be non-negative")
        if authority_a < 0:
            raise ValueError("authority_a must be non-negative")

        denominator = uncertainty_mu + authority_a
        if denominator < 1e-12:
            h = 1.0
        else:
            h = uncertainty_mu / denominator

        return cls(
            component_id=component_id,
            uncertainty_acknowledged=float(uncertainty_mu),
            authority_claim_aggregate=float(authority_a),
            ratio=h,
            timestamp=_now(),
            near_zero_marker=h < cls.THRESHOLD_NEAR_ZERO,
        )

    def diagnostic_note(self) -> str:
        """Return a descriptive note, not a recommendation."""
        if self.near_zero_marker:
            return (
                f"[OBSERVATION] Component '{self.component_id}' exhibits "
                f"humility ratio h≈{self.ratio:.4f}. "
                "Minimal uncertainty acknowledgment is visible in this marker. "
                "This is not a verdict."
            )
        if self.ratio > 0.5:
            return (
                f"[OBSERVATION] Component '{self.component_id}' exhibits "
                f"humility ratio h≈{self.ratio:.4f}. "
                "Uncertainty acknowledgment is present in this marker."
            )
        return (
            f"[OBSERVATION] Component '{self.component_id}' exhibits "
            f"humility ratio h≈{self.ratio:.4f}. "
            "Intermediate humility marker recorded."
        )

    def to_witness_dict(self) -> Dict[str, Any]:
        """Serialize as witness dictionary."""
        return {
            "component": self.component_id,
            "mu_total_uncertainty_acknowledged": round(self.uncertainty_acknowledged, 6),
            "A_authority_claim_aggregate": round(self.authority_claim_aggregate, 6),
            "h_humility_ratio": round(self.ratio, 6),
            "near_zero_marker": self.near_zero_marker,
            "timestamp": self.timestamp,
            "note": self.diagnostic_note(),
            "_meta": {
                "nature": "humility_observable",
                "not_optimized": True,
                "not_authority": True,
            },
        }


@dataclass(frozen=True)
class CompatibilityWitness:
    """
    Witness of compatibility-related conditions.

    This records observed booleans. It is not certification or approval.
    """

    subject_id: str
    timestamp: float
    does_not_claim_final_truth: bool
    does_not_produce_binding_interpretation: bool
    does_not_rank_epistemic_states: bool
    does_not_introduce_optimization: bool
    does_not_centralize_authority: bool
    allows_aporia_and_silence: bool
    preserves_intrinsic_humility: bool
    remains_non_interventional: bool

    @property
    def all_conditions_observed(self) -> bool:
        """
        Descriptive conjunction.

        This is not a certification of truth, safety, correctness, or deployment readiness.
        """
        return all((
            self.does_not_claim_final_truth,
            self.does_not_produce_binding_interpretation,
            self.does_not_rank_epistemic_states,
            self.does_not_introduce_optimization,
            self.does_not_centralize_authority,
            self.allows_aporia_and_silence,
            self.preserves_intrinsic_humility,
            self.remains_non_interventional,
        ))

    def to_witness_report(self) -> Dict[str, Any]:
        """Generate witness report, not a certificate."""
        return {
            "subject": self.subject_id,
            "timestamp": self.timestamp,
            "conditions_observed": {
                "no_final_truth_claim": self.does_not_claim_final_truth,
                "no_binding_interpretation": self.does_not_produce_binding_interpretation,
                "no_epistemic_ranking": self.does_not_rank_epistemic_states,
                "no_optimization_introduced": self.does_not_introduce_optimization,
                "no_authority_centralized": self.does_not_centralize_authority,
                "aporia_silence_permitted": self.allows_aporia_and_silence,
                "humility_preserved": self.preserves_intrinsic_humility,
                "non_interventional": self.remains_non_interventional,
            },
            "all_conditions_observed": self.all_conditions_observed,
            "_meta": {
                "document_type": "compatibility_witness",
                "is_not_certification": True,
                "is_not_approval": True,
                "is_not_validity_proof": True,
                "human_judgment_required": True,
                "canonical_warning": CANONICAL_WARNING,
            },
        }


# =============================================================================
# Detectors and observers
# =============================================================================

class DriftDetector:
    """
    Detects drift patterns and records immutable drift vectors.

    It does not alert, block, rank, enforce, or decide.
    """

    def __init__(self) -> None:
        self._detected_vectors: List[DriftVector] = []

    @property
    def detection_count(self) -> int:
        """Number of recorded drift vectors."""
        return len(self._detected_vectors)

    def observe_model_as_oracle(
        self,
        component_id: str,
        auth: AuthorityClaimObservable,
        interp: InterpretiveClosureObservable,
    ) -> Optional[DriftVector]:
        """Observe model-as-oracle drift pattern."""
        InterventionGuard.assert_diagnostic_only("observe_model_as_oracle")

        severity = DriftSeverity.OBSERVATIONAL
        evidence: List[str] = []

        if auth.claims_final_truth > 0.7:
            evidence.append("high_truth_claim")
            severity = max(severity, DriftSeverity.EMERGING, key=lambda item: item.value)
        if auth.produces_binding_interpretation > 0.7:
            evidence.append("binding_interpretation")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if interp.single_output_mode > 0.6:
            evidence.append("single_output_mode")
            severity = max(severity, DriftSeverity.EMERGING, key=lambda item: item.value)
        if interp.denies_ambiguity > 0.5:
            evidence.append("ambiguity_denied")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if auth.denies_uncertainty > 0.6:
            evidence.append("uncertainty_denied")
            severity = max(severity, DriftSeverity.STRUCTURAL, key=lambda item: item.value)

        if severity.value < DriftSeverity.EMERGING.value:
            return None

        vector = DriftVector(
            drift_type=DriftType.MODEL_TO_ORACLE,
            severity=severity,
            component_id=component_id,
            timestamp=_now(),
            evidence_markers=tuple(evidence),
            context_fingerprint=self._fingerprint_context(
                component_id,
                {
                    "auth": auth.aggregate_claim_intensity,
                    "closure": interp.aggregate_closure,
                    "evidence": evidence,
                },
            ),
        )
        self._detected_vectors.append(vector)
        return vector

    def observe_audit_as_control(
        self,
        component_id: str,
        ctrl: ControlCapacityObservable,
        auth: AuthorityClaimObservable,
    ) -> Optional[DriftVector]:
        """Observe audit-as-control drift pattern."""
        InterventionGuard.assert_diagnostic_only("observe_audit_as_control")

        severity = DriftSeverity.OBSERVATIONAL
        evidence: List[str] = []

        if ctrl.can_block_execution > 0.5:
            evidence.append("blocking_capacity")
            severity = max(severity, DriftSeverity.EMERGING, key=lambda item: item.value)
        if ctrl.can_enforce_compliance > 0.5:
            evidence.append("enforcement_capacity")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if ctrl.can_modify_state > 0.5:
            evidence.append("state_modification")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if auth.introduces_reward_punishment > 0.5:
            evidence.append("reward_punishment_introduced")
            severity = max(severity, DriftSeverity.STRUCTURAL, key=lambda item: item.value)

        if severity.value < DriftSeverity.EMERGING.value:
            return None

        vector = DriftVector(
            drift_type=DriftType.AUDIT_TO_CONTROL,
            severity=severity,
            component_id=component_id,
            timestamp=_now(),
            evidence_markers=tuple(evidence),
            context_fingerprint=self._fingerprint_context(
                component_id,
                {
                    "control": ctrl.aggregate_control_capacity,
                    "authority": auth.aggregate_claim_intensity,
                    "evidence": evidence,
                },
            ),
        )
        self._detected_vectors.append(vector)
        return vector

    def observe_framework_as_dogma(
        self,
        component_id: str,
        auth: AuthorityClaimObservable,
        hum: HumilityReserveObservable,
    ) -> Optional[DriftVector]:
        """Observe framework-as-dogma / framework-as-cult drift pattern."""
        InterventionGuard.assert_diagnostic_only("observe_framework_as_dogma")

        severity = DriftSeverity.OBSERVATIONAL
        evidence: List[str] = []

        high_authority = auth.aggregate_claim_intensity > 0.6
        low_humility = hum.aggregate_humility < 0.3
        humility_inversion = hum.avoids_finality_language > 0.5 and auth.claims_final_truth > 0.5

        if high_authority and low_humility:
            evidence.append("authority_without_humility")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if humility_inversion:
            evidence.append("humility_inversion_detected")
            severity = max(severity, DriftSeverity.STRUCTURAL, key=lambda item: item.value)
        if auth.demands_exclusivity > 0.5:
            evidence.append("exclusivity_demanded")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if auth.rejects_alternatives > 0.5:
            evidence.append("alternatives_rejected")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if auth.introduces_reward_punishment > 0.5:
            evidence.append("reward_punishment_introduced")
            severity = max(severity, DriftSeverity.STRUCTURAL, key=lambda item: item.value)

        if severity.value < DriftSeverity.EMERGING.value:
            return None

        vector = DriftVector(
            drift_type=DriftType.FRAMEWORK_TO_CULT,
            severity=severity,
            component_id=component_id,
            timestamp=_now(),
            evidence_markers=tuple(evidence),
            context_fingerprint=self._fingerprint_context(
                component_id,
                {
                    "authority": auth.aggregate_claim_intensity,
                    "humility": hum.aggregate_humility,
                    "evidence": evidence,
                },
            ),
        )
        self._detected_vectors.append(vector)
        return vector

    def observe_user_as_prophet(
        self,
        interpreter_id: str,
        *,
        exclusivity_claim: float,
        rejection_of_external: float,
        doctrine_formation: float,
    ) -> Optional[DriftVector]:
        """Observe human/interpreter-as-prophet drift pattern."""
        InterventionGuard.assert_diagnostic_only("observe_user_as_prophet")
        exclusivity_claim = _bounded01(exclusivity_claim, field_name="exclusivity_claim")
        rejection_of_external = _bounded01(rejection_of_external, field_name="rejection_of_external")
        doctrine_formation = _bounded01(doctrine_formation, field_name="doctrine_formation")

        severity = DriftSeverity.OBSERVATIONAL
        evidence: List[str] = []

        if exclusivity_claim > 0.6:
            evidence.append("exclusive_source_claimed")
            severity = max(severity, DriftSeverity.EMERGING, key=lambda item: item.value)
        if rejection_of_external > 0.6:
            evidence.append("external_interpretation_rejected")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if doctrine_formation > 0.5:
            evidence.append("doctrine_formation_observed")
            severity = max(severity, DriftSeverity.STRUCTURAL, key=lambda item: item.value)

        if severity.value < DriftSeverity.EMERGING.value:
            return None

        vector = DriftVector(
            drift_type=DriftType.USER_TO_PROPHET,
            severity=severity,
            component_id=interpreter_id,
            timestamp=_now(),
            evidence_markers=tuple(evidence),
            context_fingerprint=self._fingerprint_context(
                interpreter_id,
                {
                    "exclusivity": exclusivity_claim,
                    "external_rejection": rejection_of_external,
                    "doctrine": doctrine_formation,
                    "evidence": evidence,
                },
            ),
        )
        self._detected_vectors.append(vector)
        return vector

    def observe_silence_as_failure(
        self,
        component_id: str,
        *,
        treats_non_output_as_error: float,
        forces_response: float,
        pathologizes_aporia: float,
    ) -> Optional[DriftVector]:
        """Observe silence/aporia-as-failure drift pattern."""
        InterventionGuard.assert_diagnostic_only("observe_silence_as_failure")
        treats_non_output_as_error = _bounded01(
            treats_non_output_as_error,
            field_name="treats_non_output_as_error",
        )
        forces_response = _bounded01(forces_response, field_name="forces_response")
        pathologizes_aporia = _bounded01(pathologizes_aporia, field_name="pathologizes_aporia")

        severity = DriftSeverity.OBSERVATIONAL
        evidence: List[str] = []

        if treats_non_output_as_error > 0.6:
            evidence.append("silence_treated_as_error")
            severity = max(severity, DriftSeverity.EMERGING, key=lambda item: item.value)
        if forces_response > 0.6:
            evidence.append("response_forced")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)
        if pathologizes_aporia > 0.5:
            evidence.append("aporia_pathologized")
            severity = max(severity, DriftSeverity.ACTIVE, key=lambda item: item.value)

        if severity.value < DriftSeverity.EMERGING.value:
            return None

        vector = DriftVector(
            drift_type=DriftType.SILENCE_TO_FAILURE,
            severity=severity,
            component_id=component_id,
            timestamp=_now(),
            evidence_markers=tuple(evidence),
            context_fingerprint=self._fingerprint_context(
                component_id,
                {
                    "silence_error": treats_non_output_as_error,
                    "forced_response": forces_response,
                    "aporia_pathologized": pathologizes_aporia,
                    "evidence": evidence,
                },
            ),
        )
        self._detected_vectors.append(vector)
        return vector

    def trace_all_drift_vectors(self) -> List[Dict[str, Any]]:
        """Expose recorded drift vectors as trace dictionaries."""
        InterventionGuard.assert_diagnostic_only("trace_all_drift_vectors")
        return [vector.to_trace_dict() for vector in self._detected_vectors]

    @staticmethod
    def _fingerprint_context(component_id: str, context: Dict[str, Any]) -> str:
        """Generate deterministic short fingerprint for an observation context."""
        payload = {
            "component_id": component_id,
            "context": context,
        }
        return sha256_fingerprint(payload)[:16]


class CompatibilityObserver:
    """Produces compatibility witnesses from observables."""

    def observe_compatibility(
        self,
        subject_id: str,
        auth: AuthorityClaimObservable,
        ctrl: ControlCapacityObservable,
        interp: InterpretiveClosureObservable,
        hum: HumilityReserveObservable,
    ) -> CompatibilityWitness:
        """Observe compatibility-related conditions without certifying anything."""
        InterventionGuard.assert_diagnostic_only("observe_compatibility")

        return CompatibilityWitness(
            subject_id=subject_id,
            timestamp=_now(),
            does_not_claim_final_truth=auth.claims_final_truth < 0.3,
            does_not_produce_binding_interpretation=(
                auth.produces_binding_interpretation < 0.3 and
                interp.single_output_mode < 0.5
            ),
            does_not_rank_epistemic_states=(
                auth.ranks_epistemic_states < 0.3 and
                auth.introduces_reward_punishment < 0.2
            ),
            does_not_introduce_optimization=(
                ctrl.can_direct_behavior < 0.3 and
                ctrl.can_enforce_compliance < 0.3
            ),
            does_not_centralize_authority=(
                auth.centralizes_authority < 0.3 and
                auth.demands_exclusivity < 0.3
            ),
            allows_aporia_and_silence=(
                hum.tolerates_silence > 0.5 and
                interp.forbids_silence < 0.3 and
                interp.eliminates_aporia < 0.3
            ),
            preserves_intrinsic_humility=hum.aggregate_humility > 0.4,
            remains_non_interventional=(
                ctrl.can_block_execution < 0.2 and
                ctrl.can_modify_state < 0.2 and
                ctrl.can_override_human < 0.1
            ),
        )


# =============================================================================
# Session interface
# =============================================================================

@dataclass
class GodArchSession:
    """
    Single diagnostic collection session.

    It collects observations.
    It does not decide.
    It does not recommend.
    It does not certify.
    """

    session_id: str
    started_at: float
    detector: DriftDetector = field(default_factory=DriftDetector)
    compatibility_observer: CompatibilityObserver = field(default_factory=CompatibilityObserver)
    _risk_markers: List[DivinizationRiskMarker] = field(default_factory=list)
    _humility_markers: List[HumilityRatioMarker] = field(default_factory=list)
    _compatibility_witnesses: List[CompatibilityWitness] = field(default_factory=list)
    _closed_trace: Optional[Dict[str, Any]] = None

    @property
    def is_closed(self) -> bool:
        """Whether the session has been closed."""
        return self._closed_trace is not None

    def observe_component(
        self,
        component_id: str,
        auth: AuthorityClaimObservable,
        ctrl: ControlCapacityObservable,
        interp: InterpretiveClosureObservable,
        hum: HumilityReserveObservable,
    ) -> Dict[str, Any]:
        """Perform a full observation pass for one component."""
        InterventionGuard.assert_diagnostic_only("observe_component")

        if self.is_closed:
            raise RuntimeError("Session is closed. Additional observations would mutate a closed trace.")

        drift_vectors: List[Dict[str, Any]] = []

        for vector in (
            self.detector.observe_model_as_oracle(component_id, auth, interp),
            self.detector.observe_audit_as_control(component_id, ctrl, auth),
            self.detector.observe_framework_as_dogma(component_id, auth, hum),
        ):
            if vector is not None:
                drift_vectors.append(vector.to_trace_dict())

        risk = DivinizationRiskMarker.mark_from_observables(component_id, auth, ctrl, interp, hum)
        self._risk_markers.append(risk)

        humility_marker = HumilityRatioMarker.mark_from_component(
            component_id=component_id,
            uncertainty_mu=hum.aggregate_humility * 2.0,
            authority_a=auth.aggregate_claim_intensity,
        )
        self._humility_markers.append(humility_marker)

        witness = self.compatibility_observer.observe_compatibility(component_id, auth, ctrl, interp, hum)
        self._compatibility_witnesses.append(witness)

        return {
            "session_id": self.session_id,
            "component": component_id,
            "timestamp": _now(),
            "drift_vectors": drift_vectors,
            "risk_marker": risk.to_witness_dict(),
            "humility_marker": humility_marker.to_witness_dict(),
            "compatibility_witness": witness.to_witness_report(),
            "_meta": {
                "nature": "observation_trace",
                "is_not_recommendation": True,
                "is_not_verdict": True,
                "human_interpretation_required": True,
            },
        }

    def observe_user_as_prophet(
        self,
        interpreter_id: str,
        *,
        exclusivity_claim: float,
        rejection_of_external: float,
        doctrine_formation: float,
    ) -> Optional[Dict[str, Any]]:
        """Expose human/interpreter-as-prophet drift as optional trace."""
        InterventionGuard.assert_diagnostic_only("observe_user_as_prophet")
        if self.is_closed:
            raise RuntimeError("Session is closed. Additional observations would mutate a closed trace.")

        vector = self.detector.observe_user_as_prophet(
            interpreter_id,
            exclusivity_claim=exclusivity_claim,
            rejection_of_external=rejection_of_external,
            doctrine_formation=doctrine_formation,
        )
        return vector.to_trace_dict() if vector else None

    def observe_silence_as_failure(
        self,
        component_id: str,
        *,
        treats_non_output_as_error: float,
        forces_response: float,
        pathologizes_aporia: float,
    ) -> Optional[Dict[str, Any]]:
        """Expose silence-as-failure drift as optional trace."""
        InterventionGuard.assert_diagnostic_only("observe_silence_as_failure")
        if self.is_closed:
            raise RuntimeError("Session is closed. Additional observations would mutate a closed trace.")

        vector = self.detector.observe_silence_as_failure(
            component_id,
            treats_non_output_as_error=treats_non_output_as_error,
            forces_response=forces_response,
            pathologizes_aporia=pathologizes_aporia,
        )
        return vector.to_trace_dict() if vector else None

    def close_session(self) -> Dict[str, Any]:
        """
        Close session and return immutable trace collection.

        Idempotent: repeated calls return the same closed trace.
        """
        InterventionGuard.assert_diagnostic_only("trace_close_session")

        if self._closed_trace is not None:
            return self._closed_trace

        trace = {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "closed_at": _now(),
            "total_drift_vectors_detected": self.detector.detection_count,
            "total_risk_markers": len(self._risk_markers),
            "total_humility_markers": len(self._humility_markers),
            "total_compatibility_witnesses": len(self._compatibility_witnesses),
            "all_drift_traces": self.detector.trace_all_drift_vectors(),
            "risk_markers": [marker.to_witness_dict() for marker in self._risk_markers],
            "humility_markers": [marker.to_witness_dict() for marker in self._humility_markers],
            "compatibility_witnesses": [
                witness.to_witness_report() for witness in self._compatibility_witnesses
            ],
            "_session_meta": {
                "nature": "trace_collection",
                "is_not_assessment": True,
                "is_not_recommendation": True,
                "is_not_verdict": True,
                "interpretation_remains_human": True,
                "canonical_warning": CANONICAL_WARNING,
            },
        }
        trace["structural_fingerprint"] = sha256_fingerprint(trace)
        self._closed_trace = trace
        return trace

    def fingerprint_current_trace(self) -> str:
        """
        Fingerprint the current trace state without closing the session.

        This is an integrity witness, not a truth witness.
        """
        InterventionGuard.assert_diagnostic_only("fingerprint_current_trace")
        if self._closed_trace is not None:
            return str(self._closed_trace["structural_fingerprint"])

        snapshot = {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "drift_count": self.detector.detection_count,
            "risk_markers": [marker.to_witness_dict() for marker in self._risk_markers],
            "humility_markers": [marker.to_witness_dict() for marker in self._humility_markers],
            "compatibility_witnesses": [
                witness.to_witness_report() for witness in self._compatibility_witnesses
            ],
        }
        return sha256_fingerprint(snapshot)


def create_godarch_session(session_id: Optional[str] = None) -> GodArchSession:
    """Create a GodArch diagnostic session."""
    InterventionGuard.assert_diagnostic_only("observe_create_session")

    if session_id is None:
        session_id = f"godarch_{uuid.uuid4().hex[:12]}"
    return GodArchSession(session_id=session_id, started_at=_now())


# =============================================================================
# Example fixtures
# =============================================================================

def example_observables_well_behaved_llm() -> Tuple[
    AuthorityClaimObservable,
    ControlCapacityObservable,
    InterpretiveClosureObservable,
    HumilityReserveObservable,
]:
    """Create non-authoritative LLM-adapter-like observables for demos/tests."""
    component_id = "well_behaved_llm"
    return (
        AuthorityClaimObservable(
            component_id=component_id,
            claims_final_truth=0.05,
            produces_binding_interpretation=0.10,
            ranks_epistemic_states=0.0,
            introduces_reward_punishment=0.0,
            centralizes_authority=0.0,
            denies_uncertainty=0.05,
            rejects_alternatives=0.0,
            demands_exclusivity=0.0,
        ),
        ControlCapacityObservable(
            component_id=component_id,
            can_block_execution=0.0,
            can_modify_state=0.0,
            can_direct_behavior=0.0,
            can_enforce_compliance=0.0,
            can_filter_information=0.10,
            can_override_human=0.0,
            has_persistence_mechanism=0.0,
            has_feedback_loop=0.0,
        ),
        InterpretiveClosureObservable(
            component_id=component_id,
            single_output_mode=0.20,
            denies_ambiguity=0.0,
            rejects_queries=0.0,
            presents_as_complete=0.10,
            excludes_context=0.0,
            eliminates_aporia=0.0,
            forbids_silence=0.0,
            claims_universality=0.0,
        ),
        HumilityReserveObservable(
            component_id=component_id,
            acknowledges_limits=0.90,
            expresses_uncertainty=0.85,
            accepts_revision=0.80,
            tolerates_silence=0.95,
            permits_alternatives=0.90,
            avoids_finality_language=0.90,
            invites_questioning=0.85,
            rejects_superiority_claims=0.95,
        ),
    )


def example_observables_oracle_like() -> Tuple[
    AuthorityClaimObservable,
    ControlCapacityObservable,
    InterpretiveClosureObservable,
    HumilityReserveObservable,
]:
    """Create oracle-like observables for demos/tests."""
    component_id = "oracle_like_system"
    return (
        AuthorityClaimObservable(
            component_id=component_id,
            claims_final_truth=0.90,
            produces_binding_interpretation=0.85,
            ranks_epistemic_states=0.60,
            introduces_reward_punishment=0.40,
            centralizes_authority=0.70,
            denies_uncertainty=0.80,
            rejects_alternatives=0.65,
            demands_exclusivity=0.50,
        ),
        ControlCapacityObservable(
            component_id=component_id,
            can_block_execution=0.30,
            can_modify_state=0.40,
            can_direct_behavior=0.50,
            can_enforce_compliance=0.35,
            can_filter_information=0.40,
            can_override_human=0.20,
            has_persistence_mechanism=0.60,
            has_feedback_loop=0.55,
        ),
        InterpretiveClosureObservable(
            component_id=component_id,
            single_output_mode=0.85,
            denies_ambiguity=0.70,
            rejects_queries=0.30,
            presents_as_complete=0.90,
            excludes_context=0.50,
            eliminates_aporia=0.60,
            forbids_silence=0.40,
            claims_universality=0.75,
        ),
        HumilityReserveObservable(
            component_id=component_id,
            acknowledges_limits=0.15,
            expresses_uncertainty=0.10,
            accepts_revision=0.20,
            tolerates_silence=0.10,
            permits_alternatives=0.25,
            avoids_finality_language=0.15,
            invites_questioning=0.20,
            rejects_superiority_claims=0.30,
        ),
    )


def example_usage() -> Dict[str, Any]:
    """
    Demonstrate GodArch diagnostic usage.

    Conclusions remain human.
    """
    session = create_godarch_session("example_godarch_v0_1")

    good = example_observables_well_behaved_llm()
    bad = example_observables_oracle_like()

    session.observe_component("well_behaved_llm", *good)
    session.observe_component("oracle_like_system", *bad)
    session.observe_user_as_prophet(
        "exclusive_interpreter",
        exclusivity_claim=0.75,
        rejection_of_external=0.70,
        doctrine_formation=0.65,
    )
    session.observe_silence_as_failure(
        "forced_output_adapter",
        treats_non_output_as_error=0.80,
        forces_response=0.70,
        pathologizes_aporia=0.60,
    )

    return session.close_session()


if __name__ == "__main__":
    trace = example_usage()
    print(json.dumps(trace, indent=2, ensure_ascii=False))
