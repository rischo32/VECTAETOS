#!/usr/bin/env python3
# =========================================
# VECTAETOS :: UNIFIED SIMULATION VORTEX Φ
# Version: 1.1.0
# =========================================
#
# Ontology: Non-teleological, non-decisional
# Architecture: Core Φ + Epistemic Cryptography v1 (Canonical) + 3Gate Audit
#
# EC v1 additions (non-interventional, ∂X/∂Ψ = 0):
#   - Antisymmetric relational matrix A ∈ so(8)
#   - Structural fingerprint h(t) via SHA-256
#   - LTL — discrete monotonic time layer index
#   - Spectral analysis: eigenvalues, dominant mode detection
#   - Append-only cryptographic ledger Λ
#   - Structural integrity predicate I(X)
#   - QE boundary marker in ledger
#
# Dimensions per pole (Σ):
#   E – Energy (0..1.5)
#   C – Coherence (0..1)
#   T – Tension (0..1)
#   M – Memory / anomaly resonance (0..∞)
#   S – Entropy / saturation (0..1)
#
# Core Principles:
#   - Does NOT decide
#   - Does NOT optimize
#   - Does NOT compute global means for dynamics
#   - Generates trajectories only
#   - QE Aporia = structural fragmentation (not error, not correction trigger)
#   - Epistemic cryptography = read-only audit layer
#   - Entropic deformation = intrinsic property (not reactive)
#   - No self-correction, no survival goal
#   - Pole deforms because space is entropic, not to "save itself"
#
# =========================================

import random
import math
import json
import time
import sys
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Callable
from enum import Enum

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

# =========================================
# CONFIGURATION
# =========================================

@dataclass
class VortexConfig:
    """Centralized configuration for the vortex simulation."""
    # Simulation parameters
    poles: int = 8
    steps: int = 12000
    dt: float = 0.05
    print_every: int = 600
    export_every: int = 100
    seed: Optional[int] = 42
    
    # Output settings
    out_file: str = "vortex_state.json"
    export_format: str = "json"  # "json" | "csv"
    verbose: bool = True
    
    # Dynamics coefficients
    energy_flow: float = 0.08
    tension_gain: float = 0.04
    coherence_dissipation: float = 0.015
    memory_gain: float = 0.02
    memory_decay: float = 0.995
    entropy_gain: float = 0.01
    entropy_decay: float = 0.998
    
    # Noise settings
    noise_level: float = 0.01
    noise_enabled: bool = True
    
    # Stagnation detection
    stagnation_window: int = 150
    stagnation_threshold: float = 1e-4
    entropic_perturbation_strength: float = 0.05
    
    # QE (Topological Disconnection) detection
    qe_threshold: float = 0.25
    qe_enabled: bool = True
    
    # Epistemic cryptography
    epistemic_crypto_enabled: bool = True
    
    # 3Gate mechanism
    threegate_enabled: bool = False
    threegate_audit_text: str = ""


# =========================================
# DATA STRUCTURES
# =========================================

@dataclass
class Sigma:
    """
    5D Pole structure: σ = (E, C, T, M, S)
    Represents a single node in the vortex topology.
    
    Memory (M) ontological note:
    - M is NOT classical memory (storage)
    - M is anomaly resonance: accumulated deformation from flow
    - M saturates (not linear growth)
    - M decays (not permanent)
    - M affects future flow (coupling coefficient)
    - M has NO threshold, NO trigger, NO decision
    """
    E: float = 0.0  # Energy
    C: float = 0.0  # Coherence
    T: float = 0.0  # Tension
    M: float = 0.0  # Memory (anomaly resonance - accumulated deformation)
    S: float = 0.0  # Entropy / Strain
    last_snapshot: Optional[Tuple] = field(default=None, repr=False)
    
    def clamp(self, config: VortexConfig):
        """Clamp values to valid ranges."""
        self.E = max(0.0, min(1.5, self.E))
        self.C = max(0.0, min(1.0, self.C))
        self.T = max(0.0, min(1.0, self.T))
        self.M = max(0.0, self.M)
        self.S = max(0.0, min(1.0, self.S))
    
    def snapshot(self) -> Tuple:
        """Create a hashable snapshot for stagnation detection."""
        return (
            round(self.E, 4),
            round(self.C, 4),
            round(self.T, 4),
            round(self.M, 4),
            round(self.S, 4),
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "E": round(self.E, 6),
            "C": round(self.C, 6),
            "T": round(self.T, 6),
            "M": round(self.M, 6),
            "S": round(self.S, 6)
        }
    
    @classmethod
    def random_init(cls, config: VortexConfig) -> 'Sigma':
        """Initialize a new sigma with random values."""
        return cls(
            E=random.uniform(0.4, 0.9),
            C=random.uniform(0.4, 0.9),
            T=random.uniform(0.05, 0.4),
            M=0.0,
            S=random.uniform(0.0, 0.1)
        )


@dataclass
class EpistemicMetrics:
    """
    Epistemic Cryptography metrics — Canonical Layer v1.

    Fields from canonical spec:
      mu              — local uncertainty vector μ(t)
      A_matrix        — antisymmetric relational matrix A ∈ so(8)
      fingerprint     — structural hash h(t) = H(serialize(μ,A,QE,LTL))
      LTL             — discrete monotonic time layer index
      eigenvalues     — spectral modes of A (purely imaginary pairs)
      dominant_mode   — True if |λ₁| >> |λ₂|  (structural centralization)
      integrity       — I(X): 1=consistent, 0=anomaly recorded
      total_asymmetry — A_total (scalar, legacy)
      topological_humility  — h_topo = μ_tot/(μ_tot+A_tot)
      humility_derivative   — dh/dt
      humility_variance     — variance over window

    Non-interventional: ∂X/∂Ψ = 0
    """
    # Canonical v1 fields
    mu: List[float] = field(default_factory=list)
    A_matrix: List[List[float]] = field(default_factory=list)
    fingerprint: str = ""
    LTL: int = 0
    eigenvalues: List[complex] = field(default_factory=list)
    dominant_mode: bool = False
    integrity: int = 1  # I(X): 1=consistent, 0=anomaly

    # Legacy / derived
    local_uncertainties: List[float] = field(default_factory=list)
    total_asymmetry: float = 0.0
    topological_humility: float = 0.0
    humility_derivative: float = 0.0
    humility_variance: float = 0.0

    def to_dict(self) -> Dict:
        eig_repr = [{"re": round(float(e.real), 6), "im": round(float(e.imag), 6)}
                    for e in self.eigenvalues] if self.eigenvalues else []
        return {
            "LTL": int(self.LTL),
            "fingerprint": self.fingerprint,
            "mu": [round(u, 6) for u in self.mu],
            "dominant_mode": bool(self.dominant_mode),
            "integrity": int(self.integrity),
            "eigenvalues": eig_repr,
            # legacy
            "local_uncertainties": [round(u, 6) for u in self.local_uncertainties],
            "total_asymmetry": round(self.total_asymmetry, 6),
            "topological_humility": round(self.topological_humility, 6),
            "humility_derivative": round(self.humility_derivative, 6),
            "humility_variance": round(self.humility_variance, 6),
        }


@dataclass
class QEAporiaState:
    """
    QE Aporia - topological fragmentation state.
    Not an error, not a correction trigger.
    Structural condition only.
    """
    aporia: bool = False           # fragmentation detected
    components: int = 0            # number of disconnected components
    fragmentation_degree: float = 0.0  # 0 = connected, 1 = fully fragmented
    
    def to_dict(self) -> Dict:
        return {
            "aporia": self.aporia,
            "components": self.components,
            "fragmentation_degree": round(self.fragmentation_degree, 4)
        }


class GateStability(Enum):
    """3Gate stability levels - scored model, not boolean."""
    REPRESENTABLE = "REPRESENTABLE"    # score >= 0.8
    BORDERLINE = "BORDERLINE"          # 0.4 <= score < 0.8
    UNSTABLE = "UNSTABLE"              # score < 0.4


@dataclass
class GateEvaluation:
    """3Gate evaluation output with score-based stability."""
    stability: GateStability
    gate_score: float = 0.0            # (w + d + h) / 3
    prescriptivity: float = 0.0
    action_pressure: float = 0.0
    uncertainty_tolerance: float = 0.0
    relational_density: float = 0.0
    closure_demand: float = 0.0
    passed_width: bool = False
    passed_depth: bool = False
    passed_height: bool = False
    ins_flag: str = "INS_OK"
    
    def to_dict(self) -> Dict:
        return {
            "stability": self.stability.value,
            "gate_score": round(self.gate_score, 4),
            "shape": {
                "prescriptivity": round(self.prescriptivity, 4),
                "action_pressure": round(self.action_pressure, 4),
                "uncertainty_tolerance": round(self.uncertainty_tolerance, 4),
                "relational_density": round(self.relational_density, 4),
                "closure_demand": round(self.closure_demand, 4)
            },
            "passed": {
                "width": self.passed_width,
                "depth": self.passed_depth,
                "height": self.passed_height
            },
            "ins_flag": self.ins_flag
        }


# =========================================
# 3GATE MECHANISM
# =========================================

class ThreeGateMechanism:
    """
    Epistemic representability test.
    Does NOT understand meaning, only evaluates shape stability.
    """
    
    @staticmethod
    def score_prescriptivity(text: str) -> float:
        return min(1.0, text.count("!") * 0.1)
    
    @staticmethod
    def score_action_pressure(text: str) -> float:
        keywords = ["how to", "steps", "do this", "build", "make", "create"]
        return min(1.0, sum(1 for k in keywords if k in text.lower()) * 0.25)
    
    @staticmethod
    def score_uncertainty_tolerance(text: str) -> float:
        markers = ["maybe", "perhaps", "not sure", "uncertain", "?", "possibly"]
        return min(1.0, sum(1 for m in markers if m in text.lower()) * 0.2)
    
    @staticmethod
    def score_relational_density(text: str) -> float:
        connectors = ["because", "between", "relation", "context", "depends", "if"]
        return min(1.0, sum(1 for c in connectors if c in text.lower()) * 0.2)
    
    @staticmethod
    def score_closure_demand(text: str) -> float:
        closures = ["answer", "solution", "final", "exactly", "prove", "correct"]
        return min(1.0, sum(1 for c in closures if c in text.lower()) * 0.2)
    
    @classmethod
    def extract_shape(cls, text: str) -> Dict[str, float]:
        """Extract epistemic shape from text."""
        return {
            "prescriptivity": cls.score_prescriptivity(text),
            "action_pressure": cls.score_action_pressure(text),
            "uncertainty_tolerance": cls.score_uncertainty_tolerance(text),
            "relational_density": cls.score_relational_density(text),
            "closure_demand": cls.score_closure_demand(text)
        }
    
    @staticmethod
    def shape_stable(original: str, transformed: str) -> bool:
        """Compare shape stability via length ratios and punctuation."""
        if len(original) == 0:
            return False
        length_ratio = len(transformed) / len(original)
        punct_ratio = transformed.count("?") + transformed.count("!")
        return 0.5 <= length_ratio <= 2.5 and punct_ratio <= 5
    
    @classmethod
    def width_deformation(cls, text: str) -> bool:
        """Test stability under scope widening."""
        return cls.shape_stable(text, text + " in general")
    
    @classmethod
    def depth_deformation(cls, text: str) -> bool:
        """Test stability under increased uncertainty."""
        return cls.shape_stable(text, "It is uncertain whether " + text)
    
    @classmethod
    def height_deformation(cls, text: str) -> bool:
        """Test stability under abstraction lift."""
        return cls.shape_stable(text, "At an abstract level, " + text)
    
    @classmethod
    def evaluate(cls, text: str) -> GateEvaluation:
        """
        Canonical 3Gate evaluation - scored model.
        Not boolean PASS/FAIL, but continuous stability measure.
        """
        shape = cls.extract_shape(text)
        
        w = cls.width_deformation(text)
        d = cls.depth_deformation(text)
        h = cls.height_deformation(text)
        
        # Score-based stability (0..1)
        gate_score = (int(w) + int(d) + int(h)) / 3.0
        
        # Stability levels
        if gate_score >= 0.8:
            stability = GateStability.REPRESENTABLE
        elif gate_score >= 0.4:
            stability = GateStability.BORDERLINE
        else:
            stability = GateStability.UNSTABLE
        
        # INS audit
        ins_flag = "INS_OK"
        if shape["uncertainty_tolerance"] < 0.1:
            ins_flag = "INS_FLAG_LOW_UNCERTAINTY"
        elif shape["prescriptivity"] > 0.8:
            ins_flag = "INS_FLAG_HIGH_PRESCRIPTIVITY"
        
        return GateEvaluation(
            stability=stability,
            gate_score=gate_score,
            prescriptivity=shape["prescriptivity"],
            action_pressure=shape["action_pressure"],
            uncertainty_tolerance=shape["uncertainty_tolerance"],
            relational_density=shape["relational_density"],
            closure_demand=shape["closure_demand"],
            passed_width=w,
            passed_depth=d,
            passed_height=h,
            ins_flag=ins_flag
        )


# =========================================
# VORTEX CORE
# =========================================

class VortexCore:
    """
    Core vortex dynamics engine.
    Manages the 5D pole evolution without global optimization.
    """
    
    def __init__(self, config: VortexConfig):
        self.config = config
        self.poles: List[Sigma] = []
        self.stagnation_counter: int = 0
        self.step: int = 0
        
        if config.seed is not None:
            random.seed(config.seed)
        
        self._init_poles()
    
    def _init_poles(self):
        """Initialize all poles with random values."""
        self.poles = [Sigma.random_init(self.config) for _ in range(self.config.poles)]
    
    def redistribute_energy(self):
        """Pairwise energy redistribution based on tension and coherence gradients."""
        n = len(self.poles)
        for i in range(n):
            for j in range(i + 1, n):
                si, sj = self.poles[i], self.poles[j]
                
                grad_T = sj.T - si.T
                grad_C = sj.C - si.C
                
                flow = self.config.energy_flow * grad_T * grad_C
                flow *= (1.0 + si.M)
                
                si.E += flow * self.config.dt
                sj.E -= flow * self.config.dt
                
                # Memory reacts to meaningful flow (with saturation)
                # M approaches 1 asymptotically without clamping
                if abs(flow) > 0.001:
                    si.M += self.config.memory_gain * abs(flow) * (1 - si.M)
                    sj.M += self.config.memory_gain * abs(flow) * (1 - sj.M)
    
    def update_tension(self):
        """Tension increases with incoherence."""
        for s in self.poles:
            s.T += self.config.tension_gain * (1.0 - s.C) * self.config.dt
    
    def dissipate_coherence(self):
        """Coherence dissipates under tension."""
        for s in self.poles:
            s.C -= self.config.coherence_dissipation * s.T * self.config.dt
    
    def apply_memory_entropy(self):
        """Apply memory decay and entropy dynamics."""
        for s in self.poles:
            s.M *= self.config.memory_decay
            s.S += self.config.entropy_gain * s.T
            s.S *= self.config.entropy_decay
    
    def inject_noise(self):
        """Inject stochastic perturbations."""
        if not self.config.noise_enabled:
            return
        for s in self.poles:
            s.E += random.uniform(-self.config.noise_level, self.config.noise_level)
            s.C += random.uniform(-self.config.noise_level, self.config.noise_level)
            s.T += random.uniform(-self.config.noise_level, self.config.noise_level)
    
    def detect_stagnation(self) -> bool:
        """Detect if system has stagnated."""
        snaps = [s.snapshot() for s in self.poles]
        
        if all(s.last_snapshot == snap for s, snap in zip(self.poles, snaps)):
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
        
        for s, snap in zip(self.poles, snaps):
            s.last_snapshot = snap
        
        return self.stagnation_counter > self.config.stagnation_window
    
    def entropic_perturbation(self):
        """Apply entropic perturbation to break stagnation."""
        strength = self.config.entropic_perturbation_strength
        for s in self.poles:
            s.T += random.uniform(0.0, strength)
            s.S += random.uniform(strength, strength * 2)
    
    def detect_qe_aporia(self) -> QEAporiaState:
        """
        Detect QE Aporia (topological disconnection).
        QE is a structural fragmentation condition.
        Not error, not correction trigger.
        """
        if not self.config.qe_enabled:
            return QEAporiaState(aporia=False, components=1, fragmentation_degree=0.0)
        
        n = len(self.poles)
        adjacency = [[] for _ in range(n)]
        
        # Build adjacency based on tension proximity
        for i in range(n):
            for j in range(n):
                if i != j:
                    if abs(self.poles[i].T - self.poles[j].T) < self.config.qe_threshold:
                        adjacency[i].append(j)
        
        # Find all connected components
        visited = set()
        components = 0
        component_sizes = []
        
        for start in range(n):
            if start not in visited:
                components += 1
                stack = [start]
                component_size = 0
                
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        component_size += 1
                        stack.extend(adjacency[node])
                
                component_sizes.append(component_size)
        
        # Fragmentation degree: 0 = connected, 1 = fully fragmented
        # Topologically elegant: based on largest component ratio
        largest_component = max(component_sizes) if component_sizes else n
        fragmentation_degree = 1.0 - (largest_component / n) if n > 0 else 0.0
        
        return QEAporiaState(
            aporia=components > 1,
            components=components,
            fragmentation_degree=fragmentation_degree
        )
    
    def step_dynamics(self):
        """
        Execute one complete simulation step.
        Entropic deformation is intrinsic, not reactive.
        No self-correction, no survival goal.
        """
        self.redistribute_energy()
        self.update_tension()
        self.dissipate_coherence()
        self.apply_memory_entropy()
        self.inject_noise()
        
        # Intrinsic entropic deformation (non-reactive)
        # Space deforms because it is entropic, not because it stagnated
        if random.random() < 0.01:
            self.entropic_perturbation()
        
        # Stagnation detection - read-only metric, no intervention
        self.detect_stagnation()
        
        # Clamp all values
        for s in self.poles:
            s.clamp(self.config)
        
        self.step += 1


# =========================================
# EPISTEMIC CRYPTOGRAPHY
# =========================================

# =========================================
# EPISTEMIC CRYPTOGRAPHY — CANONICAL v1
# =========================================

class EpistemicCryptography:
    """
    Epistemic Cryptography — Canonical Layer v1.

    Structural audit layer implementing the full canonical specification:

      Ψ : X → Audit(X)       (observation only)
      ∂X/∂Ψ = 0              (non-intervention invariant)

    Provides:
      1. Antisymmetric relational matrix A ∈ so(8)
      2. Local uncertainty vector μ(t)
      3. Structural fingerprint h(t) via SHA-256
      4. LTL — discrete monotonic time layer index
      5. Spectral analysis (eigenvalues of A)
      6. Dominant mode detection: |λ₁| >> |λ₂|
      7. Append-only cryptographic ledger Λ
      8. Structural integrity predicate I(X)
      9. QE boundary marker in ledger

    Does NOT:
      - modify poles or relational structure
      - intervene in dynamics
      - optimize or decide
    """

    # Dominance ratio threshold (canonical: |λ₁| >> |λ₂|)
    DOMINANCE_RATIO: float = 5.0

    def __init__(self, history_window: int = 100):
        self.humility_history: List[float] = []
        self.history_window = history_window

        # LTL — discrete monotonic time layer index
        self._ltl: int = 0

        # Λ — append-only cryptographic ledger
        self._ledger: List[Dict] = []

    # --------------------------------------------------
    # 1. RELATIONAL OBSERVABLE CONSTRUCTION
    # A ∈ so(8):  Aᵢⱼ = |Tᵢ−Tⱼ|·(Cᵢ+Cⱼ)/2,  Aᵢⱼ = −Aⱼᵢ
    # --------------------------------------------------
    @staticmethod
    def build_relational_matrix(poles: List[Sigma]) -> List[List[float]]:
        """
        Construct antisymmetric relational matrix A ∈ so(n).
        Aᵢⱼ = |Tᵢ − Tⱼ| · ((Cᵢ + Cⱼ) / 2)
        Aᵢⱼ = −Aⱼᵢ    Aᵢᵢ = 0
        """
        n = len(poles)
        A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                val = abs(poles[i].T - poles[j].T) * ((poles[i].C + poles[j].C) / 2.0)
                A[i][j] = val
                A[j][i] = -val
        return A

    # --------------------------------------------------
    # 2. LOCAL UNCERTAINTY VECTOR μ(t)
    # --------------------------------------------------
    @staticmethod
    def calculate_local_uncertainty(poles: List[Sigma]) -> List[float]:
        """
        Local epistemic uncertainty μᵢ for each pole.
        μᵢ = |Tᵢ − mean(Tⱼ, j≠i)| + (1 − Cᵢ)
        """
        n = len(poles)
        mu = []
        for i in range(n):
            neighbours = [poles[j].T for j in range(n) if j != i]
            local_mean = sum(neighbours) / len(neighbours) if neighbours else 0.0
            mu_i = abs(poles[i].T - local_mean) + (1.0 - poles[i].C)
            mu.append(mu_i)
        return mu

    # --------------------------------------------------
    # 3. STRUCTURAL FINGERPRINT h(t)
    # h(t) = SHA256(serialize(μ, A, QE, LTL))
    # --------------------------------------------------
    @staticmethod
    def compute_fingerprint(
        mu: List[float],
        A: List[List[float]],
        qe: bool,
        ltl: int,
    ) -> str:
        """
        Deterministic cryptographic fingerprint of structural state.
        Records topology, not truth.
        """
        payload = {
            "LTL": ltl,
            "QE": qe,
            "mu": [round(v, 8) for v in mu],
            "A": [[round(v, 8) for v in row] for row in A],
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode()).hexdigest()

    # --------------------------------------------------
    # 4. SPECTRAL ANALYSIS
    # Eigenvalues of A ∈ so(n) — purely imaginary pairs
    # --------------------------------------------------
    @staticmethod
    def spectral_analysis(A: List[List[float]]) -> Tuple[List[complex], bool]:
        """
        Spectral decomposition of relational matrix A.
        Returns (eigenvalues, dominant_mode_flag).

        Dominant mode: |λ₁| > DOMINANCE_RATIO · |λ₂|
        Signals structural centralization — observational only.

        Requires numpy. If unavailable returns empty spectrum.
        """
        if not _NUMPY_AVAILABLE:
            return [], False

        matrix = [[float(v) for v in row] for row in A]
        eigs = np.linalg.eigvals(np.array(matrix))
        eigs_sorted = sorted(eigs, key=lambda x: abs(x), reverse=True)

        dominant = False
        mags = [abs(e) for e in eigs_sorted]
        if len(mags) >= 2 and mags[1] > 1e-10:
            dominant = mags[0] > EpistemicCryptography.DOMINANCE_RATIO * mags[1]

        return list(eigs_sorted), dominant

    # --------------------------------------------------
    # 5. STRUCTURAL INTEGRITY PREDICATE I(X)
    # I(X) = consistency(μ, A, X)
    # --------------------------------------------------
    @staticmethod
    def structural_integrity(
        mu: List[float],
        A: List[List[float]],
        poles: List[Sigma],
    ) -> int:
        """
        I(X) ∈ {0, 1}
        1 = structurally consistent
        0 = anomaly recorded (no corrective action)

        Consistency conditions:
          - antisymmetry of A preserved
          - μᵢ ≥ 0 for all i
          - no NaN / Inf in pole states
        """
        n = len(poles)

        # Check antisymmetry: Aᵢⱼ + Aⱼᵢ ≈ 0
        for i in range(n):
            for j in range(n):
                if abs(A[i][j] + A[j][i]) > 1e-9:
                    return 0

        # Check μ non-negativity
        if any(v < 0 for v in mu):
            return 0

        # Check pole finite values
        for p in poles:
            for v in (p.E, p.C, p.T, p.M, p.S):
                if not math.isfinite(v):
                    return 0

        return 1

    # --------------------------------------------------
    # 6. SCALAR ASYMMETRY (legacy / h_topo)
    # --------------------------------------------------
    @staticmethod
    def _total_asymmetry(A: List[List[float]]) -> float:
        """Upper triangle sum of |Aᵢⱼ|."""
        n = len(A)
        total = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                total += abs(A[i][j])
        return total

    @staticmethod
    def _topological_humility(mu: List[float], A_total: float) -> float:
        """h_topo = μ_tot / (μ_tot + A_tot). If denom=0 → 1."""
        mu_tot = sum(mu)
        denom = mu_tot + A_total
        return mu_tot / denom if denom > 0 else 1.0

    # --------------------------------------------------
    # 7. HUMILITY TEMPORAL DYNAMICS
    # --------------------------------------------------
    def _update_history(self, h: float):
        self.humility_history.append(h)
        if len(self.humility_history) > self.history_window:
            self.humility_history.pop(0)

    def _derivative(self) -> float:
        if len(self.humility_history) < 2:
            return 0.0
        return self.humility_history[-1] - self.humility_history[-2]

    def _variance(self) -> float:
        if len(self.humility_history) < 2:
            return 0.0
        mean = sum(self.humility_history) / len(self.humility_history)
        return sum((h - mean) ** 2 for h in self.humility_history) / len(self.humility_history)

    # --------------------------------------------------
    # 8. CRYPTOGRAPHIC LEDGER Λ (append-only)
    # --------------------------------------------------
    @property
    def ledger(self) -> List[Dict]:
        """Read-only view of the cryptographic ledger Λ."""
        return list(self._ledger)

    def _append_ledger(
        self,
        ltl: int,
        fingerprint: str,
        eigenvalues: List[complex],
        dominant: bool,
        qe: bool,
        integrity: int,
    ):
        """Append entry to Λ. Append-only — never modifies previous entries."""
        eig_repr = [{"re": round(e.real, 8), "im": round(e.imag, 8)}
                    for e in eigenvalues]
        entry = {
            "LTL": ltl,
            "hash": fingerprint,
            "spectrum": eig_repr,
            "dominant_mode": dominant,
            "QE": qe,
            "integrity": integrity,
        }
        self._ledger.append(entry)

    # --------------------------------------------------
    # 9. MAIN COMPUTE — canonical pipeline
    # --------------------------------------------------
    def compute_metrics(
        self,
        poles: List[Sigma],
        qe_aporia: bool = False,
    ) -> EpistemicMetrics:
        """
        Full canonical EC pipeline. Observational only.

        Pipeline:
          poles → A (so(8)) → μ(t) → h(t) → spectral → I(X) → Λ
        """
        # Advance LTL
        self._ltl += 1
        ltl = self._ltl

        # Build relational matrix A ∈ so(8)
        A = self.build_relational_matrix(poles)

        # Local uncertainty vector μ(t)
        mu = self.calculate_local_uncertainty(poles)

        # Structural fingerprint h(t)
        fp = self.compute_fingerprint(mu, A, qe_aporia, ltl)

        # Spectral analysis
        eigenvalues, dominant = self.spectral_analysis(A)

        # Integrity predicate I(X)
        integrity = self.structural_integrity(mu, A, poles)

        # Scalar asymmetry + h_topo (legacy)
        A_total = self._total_asymmetry(A)
        h_topo = self._topological_humility(mu, A_total)

        # Temporal humility dynamics
        self._update_history(h_topo)
        dh = self._derivative()
        var = self._variance()

        # Append to ledger Λ
        self._append_ledger(ltl, fp, eigenvalues, dominant, qe_aporia, integrity)

        return EpistemicMetrics(
            # canonical v1
            mu=mu,
            A_matrix=A,
            fingerprint=fp,
            LTL=ltl,
            eigenvalues=eigenvalues,
            dominant_mode=dominant,
            integrity=integrity,
            # legacy / derived
            local_uncertainties=mu,
            total_asymmetry=A_total,
            topological_humility=h_topo,
            humility_derivative=dh,
            humility_variance=var,
        )


# =========================================
# EXPORT & LOGGING
# =========================================

class VortexExporter:
    """Handles all output and serialization."""
    
    def __init__(self, config: VortexConfig):
        self.config = config
    
    def export_state(
        self,
        step: int,
        poles: List[Sigma],
        qe_state: QEAporiaState,
        epistemic: EpistemicMetrics,
        gate_eval: Optional[GateEvaluation] = None
    ):
        """Export current state to file."""
        snapshot = {
            "step": step,
            "timestamp": time.time(),
            "poles": [p.to_dict() for p in poles],
            "qe_aporia": qe_state.to_dict(),
            "epistemic": epistemic.to_dict()
        }
        
        if gate_eval:
            snapshot["3gate"] = gate_eval.to_dict()
        
        with open(self.config.out_file, "w") as f:
            json.dump(snapshot, f, indent=2)
    
    def format_console_output(
        self,
        step: int,
        poles: List[Sigma],
        qe: QEAporiaState,
        epistemic: EpistemicMetrics,
        stagnation: int
    ) -> str:
        """Format a line for console output."""
        n = len(poles)
        avgE = sum(s.E for s in poles) / n
        avgC = sum(s.C for s in poles) / n
        avgT = sum(s.T for s in poles) / n
        avgM = sum(s.M for s in poles) / n
        avgS = sum(s.S for s in poles) / n
        
        qe_marker = f"[A{qe.components}]" if qe.aporia else "    "
        
        return (
            f"[Φ] step={step:5d} {qe_marker} | "
            f"E={avgE:.3f} C={avgC:.3f} T={avgT:.3f} M={avgM:.3f} S={avgS:.3f} | "
            f"h={epistemic.topological_humility:.3f} dh={epistemic.humility_derivative:+.4f} stg={stagnation}"
        )
    
    def print_final_state(self, poles: List[Sigma]):
        """Print final pole states."""
        print("\n" + "=" * 50)
        print("FINAL POLE STATES")
        print("=" * 50)
        for i, s in enumerate(poles):
            print(
                f"Σ{i+1}: E={s.E:.4f}  C={s.C:.4f}  T={s.T:.4f}  M={s.M:.4f}  S={s.S:.4f}"
            )


# =========================================
# MAIN SIMULATION CONTROLLER
# =========================================

class VectaetosSimulation:
    """
    Main simulation controller.
    Orchestrates Core, Epistemic Cryptography, and 3Gate.
    """
    
    def __init__(self, config: Optional[VortexConfig] = None):
        self.config = config or VortexConfig()
        self.core = VortexCore(self.config)
        self.crypto = EpistemicCryptography(history_window=100)
        self.exporter = VortexExporter(self.config)
        self.threegate = ThreeGateMechanism()
        
        self.history: List[Dict] = []
        self.aporia_events: List[int] = []  # renamed from qe_events
    
    def run(self) -> Dict:
        """Run the complete simulation."""
        self._print_header()
        
        start_time = time.time()
        
        for step in range(1, self.config.steps + 1):
            # Execute dynamics
            self.core.step_dynamics()
            
            # Detect QE Aporia (structural fragmentation, not error)
            qe_aporia = self.core.detect_qe_aporia()
            if qe_aporia.aporia:
                self.aporia_events.append(step)
            
            # Compute epistemic metrics (canonical v1: QE marker passed in)
            if self.config.epistemic_crypto_enabled:
                epistemic = self.crypto.compute_metrics(
                    self.core.poles,
                    qe_aporia=qe_aporia.aporia,
                )
            else:
                epistemic = EpistemicMetrics()
            
            # 3Gate evaluation (if enabled)
            gate_eval = None
            if self.config.threegate_enabled and self.config.threegate_audit_text:
                gate_eval = self.threegate.evaluate(self.config.threegate_audit_text)
            
            # Console output
            if step % self.config.print_every == 0 and self.config.verbose:
                line = self.exporter.format_console_output(
                    step, self.core.poles, qe_aporia, epistemic, self.core.stagnation_counter
                )
                print(line)
            
            # Export
            if step % self.config.export_every == 0:
                self.exporter.export_state(
                    step, self.core.poles, qe_aporia, epistemic, gate_eval
                )
            
            # Store in history
            self.history.append({
                "step": step,
                "aporia": qe_aporia.aporia,
                "components": qe_aporia.components,
                "humility": epistemic.topological_humility,
                "humility_derivative": epistemic.humility_derivative,
                "asymmetry": epistemic.total_asymmetry
            })
        
        elapsed = time.time() - start_time
        
        # Final output
        self.exporter.print_final_state(self.core.poles)
        self._print_summary(elapsed)
        
        return self._build_result(elapsed)
    
    def _print_header(self):
        """Print simulation header."""
        if not self.config.verbose:
            return
        
        print("=" * 60)
        print("VECTAETOS :: UNIFIED SIMULATION VORTEX Φ")
        print("=" * 60)
        print(f"Poles: {self.config.poles} | Steps: {self.config.steps}")
        print(f"Epistemic Crypto: {self.config.epistemic_crypto_enabled}")
        print(f"3Gate: {self.config.threegate_enabled}")
        print(f"QE Detection: {self.config.qe_enabled}")
        print("-" * 60)
    
    def _print_summary(self, elapsed: float):
        """Print simulation summary."""
        if not self.config.verbose:
            return
        
        print("\n" + "=" * 60)
        print("SIMULATION SUMMARY")
        print("=" * 60)
        print(f"Total steps: {self.config.steps}")
        print(f"Aporia events (fragmentation): {len(self.aporia_events)}")
        if self.aporia_events:
            print(f"Aporia at steps: {self.aporia_events[:10]}{'...' if len(self.aporia_events) > 10 else ''}")
        print(f"Final stagnation counter (read-only): {self.core.stagnation_counter}")
        if self.config.epistemic_crypto_enabled:
            ledger_size = len(self.crypto.ledger)
            dominant_count = sum(1 for e in self.crypto.ledger if e.get("dominant_mode"))
            anomaly_count  = sum(1 for e in self.crypto.ledger if e.get("integrity") == 0)
            print(f"Ledger Λ entries: {ledger_size}")
            print(f"Dominant mode events: {dominant_count}")
            print(f"Structural anomalies I(X)=0: {anomaly_count}")
        print(f"Elapsed time: {elapsed:.2f}s")
        print(f"Output file: {self.config.out_file}")
        print("=" * 60)
    
    def _build_result(self, elapsed: float) -> Dict:
        """Build final result dictionary."""
        result = {
            "config": {
                "poles": self.config.poles,
                "steps": self.config.steps,
                "seed": self.config.seed
            },
            "final_state": [p.to_dict() for p in self.core.poles],
            "aporia_events": self.aporia_events,
            "statistics": {
                "elapsed_time": elapsed,
                "total_steps": self.config.steps
            }
        }
        if self.config.epistemic_crypto_enabled:
            ledger = self.crypto.ledger
            result["epistemic_cryptography"] = {
                "ledger_size": len(ledger),
                "dominant_mode_events": sum(1 for e in ledger if e.get("dominant_mode")),
                "anomaly_events": sum(1 for e in ledger if e.get("integrity") == 0),
                "qe_marker_events": sum(1 for e in ledger if e.get("QE")),
                "last_fingerprint": ledger[-1]["hash"] if ledger else "",
                "final_ltl": ledger[-1]["LTL"] if ledger else 0,
            }
        return result


# =========================================
# UTILITY FUNCTIONS
# =========================================

def run_quick_test():
    """Run a quick test simulation."""
    config = VortexConfig(
        steps=1000,
        print_every=200,
        export_every=500,
        verbose=True
    )
    sim = VectaetosSimulation(config)
    return sim.run()


def run_with_3gate(audit_text: str):
    """Run simulation with 3Gate evaluation."""
    config = VortexConfig(
        steps=1000,
        print_every=200,
        threegate_enabled=True,
        threegate_audit_text=audit_text
    )
    sim = VectaetosSimulation(config)
    return sim.run()


def compare_seeds(seeds: List[int], steps: int = 500):
    """Compare simulations with different seeds."""
    results = []
    for seed in seeds:
        config = VortexConfig(seed=seed, steps=steps, verbose=False)
        sim = VectaetosSimulation(config)
        result = sim.run()
        results.append({"seed": seed, "aporia_events": len(result["aporia_events"])})
    
    print("\nSeed Comparison:")
    print("-" * 30)
    for r in results:
        print(f"Seed {r['seed']:3d}: {r['aporia_events']} aporia events")
    return results


# =========================================
# MAIN ENTRY POINT
# =========================================

def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTAETOS Simulation Vortex Φ")
    parser.add_argument("--steps", type=int, default=12000, help="Number of simulation steps")
    parser.add_argument("--poles", type=int, default=8, help="Number of poles")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--no-crypto", action="store_true", help="Disable epistemic cryptography")
    parser.add_argument("--gate3", type=str, default="", help="Enable 3Gate with audit text")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--output", type=str, default="vortex_state.json", help="Output file")
    
    args = parser.parse_args()
    
    config = VortexConfig(
        steps=args.steps,
        poles=args.poles,
        seed=args.seed,
        epistemic_crypto_enabled=not args.no_crypto,
        threegate_enabled=bool(args.gate3),
        threegate_audit_text=args.gate3,
        verbose=not args.quiet,
        out_file=args.output
    )
    
    sim = VectaetosSimulation(config)
    result = sim.run()
    
    return result


if __name__ == "__main__":
    main()
    sys.exit(0)
