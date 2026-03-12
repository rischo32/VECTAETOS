#!/usr/bin/env python3
# =========================================
# VECTAETOS :: UNIFIED SIMULATION VORTEX Φ
# Version: 1.2.3 (JSONL export, zrýchlený μ, finálne úpravy)
# =========================================
import random
import math
import json
import time
import sys
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

# =========================================
# KONFIGURÁCIA
# =========================================
@dataclass
class VortexConfig:
    poles: int = 8
    steps: int = 12000
    dt: float = 0.05
    print_every: int = 600
    export_every: int = 100
    seed: Optional[int] = 42
    out_file: str = "vortex_state.jsonl"      # .jsonl pre append-only
    export_format: str = "jsonl"
    verbose: bool = True
    energy_flow: float = 0.08
    tension_gain: float = 0.04
    coherence_dissipation: float = 0.015
    memory_gain: float = 0.02
    memory_decay: float = 0.995
    entropy_gain: float = 0.01
    entropy_decay: float = 0.998
    noise_level: float = 0.01
    noise_enabled: bool = True
    stagnation_window: int = 50
    entropic_perturbation_strength: float = 0.05
    qe_threshold: float = 0.25
    qe_enabled: bool = True
    epistemic_crypto_enabled: bool = True
    threegate_enabled: bool = False
    threegate_audit_text: str = ""
    singularity_names: List[str] = field(default_factory=lambda:
        ["INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE"])

# =========================================
# ŠTRUKTÚRY ÚDAJOV
# =========================================

@dataclass
class Sigma:
    E: float = 0.0
    C: float = 0.0
    T: float = 0.0
    M: float = 0.0
    S: float = 0.0
    last_snapshot: Optional[Tuple] = field(default=None, repr=False)

    def clamp(self, config: VortexConfig):
        self.E = max(0.0, min(1.5, self.E))
        self.C = max(0.0, min(1.0, self.C))
        self.T = max(0.0, min(1.0, self.T))
        self.M = max(0.0, self.M)
        self.S = max(0.0, min(1.0, self.S))

    def snapshot(self) -> Tuple:
        return (round(self.E,4), round(self.C,4), round(self.T,4),
                round(self.M,4), round(self.S,4))

    def to_dict(self) -> Dict:
        return {k: round(getattr(self, k), 6) for k in ("E","C","T","M","S")}

    @classmethod
    def random_init(cls, config: VortexConfig) -> 'Sigma':
        return cls(
            E=random.uniform(0.4, 0.9),
            C=random.uniform(0.4, 0.9),
            T=random.uniform(0.05, 0.4),
            M=0.0,
            S=random.uniform(0.0, 0.1)
        )

@dataclass
class EpistemicMetrics:
    mu: List[float] = field(default_factory=list)
    A_matrix: List[List[float]] = field(default_factory=list)
    fingerprint: str = ""
    LTL: int = 0
    eigenvalues: List[complex] = field(default_factory=list)
    dominant_mode: bool = False
    integrity: int = 1
    triality_preserved: Optional[bool] = None
    local_uncertainties: List[float] = field(default_factory=list)
    total_asymmetry: float = 0.0
    topological_humility: float = 0.0
    humility_derivative: float = 0.0
    humility_variance: float = 0.0

    def to_dict(self) -> Dict:
        eig_repr = [{"re": round(e.real,6), "im": round(e.imag,6)}
                    for e in self.eigenvalues] if self.eigenvalues else []
        return {
            "LTL": self.LTL,
            "fingerprint": self.fingerprint,
            "mu": [round(u,6) for u in self.mu],
            "dominant_mode": self.dominant_mode,
            "integrity": self.integrity,
            "triality_preserved": self.triality_preserved,
            "eigenvalues": eig_repr,
            "local_uncertainties": [round(u,6) for u in self.local_uncertainties],
            "total_asymmetry": round(self.total_asymmetry,6),
            "topological_humility": round(self.topological_humility,6),
            "humility_derivative": round(self.humility_derivative,6),
            "humility_variance": round(self.humility_variance,6),
        }

@dataclass
class QEAporiaState:
    aporia: bool = False
    components: int = 0
    fragmentation_degree: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "aporia": self.aporia,
            "components": self.components,
            "fragmentation_degree": round(self.fragmentation_degree,4)
        }

class GateStability(Enum):
    REPRESENTABLE = "REPRESENTABLE"
    BORDERLINE = "BORDERLINE"
    UNSTABLE = "UNSTABLE"

@dataclass
class GateEvaluation:
    stability: GateStability
    gate_score: float = 0.0
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
            "gate_score": round(self.gate_score,4),
            "shape": {
                "prescriptivity": round(self.prescriptivity,4),
                "action_pressure": round(self.action_pressure,4),
                "uncertainty_tolerance": round(self.uncertainty_tolerance,4),
                "relational_density": round(self.relational_density,4),
                "closure_demand": round(self.closure_demand,4)
            },
            "passed": {
                "width": self.passed_width,
                "depth": self.passed_depth,
                "height": self.passed_height
            },
            "ins_flag": self.ins_flag
        }

# =========================================
# 3GATE MECHANIZMUS
# =========================================

class ThreeGateMechanism:
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
        return {
            "prescriptivity": cls.score_prescriptivity(text),
            "action_pressure": cls.score_action_pressure(text),
            "uncertainty_tolerance": cls.score_uncertainty_tolerance(text),
            "relational_density": cls.score_relational_density(text),
            "closure_demand": cls.score_closure_demand(text)
        }

    @staticmethod
    def shape_stable(original: str, transformed: str) -> bool:
        if len(original) == 0:
            return False
        length_ratio = len(transformed) / len(original)
        punct_ratio = transformed.count("?") + transformed.count("!")
        return 0.5 <= length_ratio <= 2.5 and punct_ratio <= 5

    @classmethod
    def width_deformation(cls, text: str) -> bool:
        return cls.shape_stable(text, text + " in general")
    @classmethod
    def depth_deformation(cls, text: str) -> bool:
        return cls.shape_stable(text, "It is uncertain whether " + text)
    @classmethod
    def height_deformation(cls, text: str) -> bool:
        return cls.shape_stable(text, "At an abstract level, " + text)

    @classmethod
    def evaluate(cls, text: str) -> GateEvaluation:
        shape = cls.extract_shape(text)
        w = cls.width_deformation(text)
        d = cls.depth_deformation(text)
        h = cls.height_deformation(text)
        gate_score = (int(w) + int(d) + int(h)) / 3.0

        if gate_score >= 0.8:
            stability = GateStability.REPRESENTABLE
        elif gate_score >= 0.4:
            stability = GateStability.BORDERLINE
        else:
            stability = GateStability.UNSTABLE

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
# LTL MANAŽÉR
# =========================================

class LTLManager:
    def __init__(self):
        self._ltl = 0
    def next(self) -> int:
        self._ltl += 1
        return self._ltl
    @property
    def current(self) -> int:
        return self._ltl
    def reset(self):
        self._ltl = 0

# =========================================
# VORTEX CORE (dynamika)
# =========================================

class VortexCore:
    def __init__(self, config: VortexConfig):
        self.config = config
        self.poles: List[Sigma] = []
        self.stagnation_counter: int = 0
        self.step: int = 0
        if config.seed is not None:
            random.seed(config.seed)
            if _NUMPY_AVAILABLE:
                np.random.seed(config.seed)
        self._init_poles()

    def _init_poles(self):
        self.poles = [Sigma.random_init(self.config) for _ in range(self.config.poles)]

    def redistribute_energy(self):
        n = len(self.poles)
        for i in range(n):
            for j in range(i+1, n):
                si, sj = self.poles[i], self.poles[j]
                grad_T = sj.T - si.T
                grad_C = sj.C - si.C
                flow = self.config.energy_flow * grad_T * grad_C
                flow *= (1.0 + si.M)
                si.E += flow * self.config.dt
                sj.E -= flow * self.config.dt
                if abs(flow) > 0.001:
                    si.M += self.config.memory_gain * abs(flow) * (1 - si.M)
                    sj.M += self.config.memory_gain * abs(flow) * (1 - sj.M)

    def update_tension(self):
        for s in self.poles:
            s.T += self.config.tension_gain * (1.0 - s.C) * self.config.dt

    def dissipate_coherence(self):
        for s in self.poles:
            s.C -= self.config.coherence_dissipation * s.T * self.config.dt

    def apply_memory_entropy(self):
        for s in self.poles:
            s.M *= self.config.memory_decay
            s.S += self.config.entropy_gain * s.T
            s.S *= self.config.entropy_decay

    def inject_noise(self):
        if not self.config.noise_enabled:
            return
        for s in self.poles:
            s.E += random.uniform(-self.config.noise_level, self.config.noise_level)
            s.C += random.uniform(-self.config.noise_level, self.config.noise_level)
            s.T += random.uniform(-self.config.noise_level, self.config.noise_level)

    def detect_stagnation(self) -> bool:
        snaps = [s.snapshot() for s in self.poles]
        if all(s.last_snapshot == snap for s, snap in zip(self.poles, snaps)):
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
        for s, snap in zip(self.poles, snaps):
            s.last_snapshot = snap
        return self.stagnation_counter > self.config.stagnation_window

    def entropic_perturbation(self):
        strength = self.config.entropic_perturbation_strength
        for s in self.poles:
            s.T += random.uniform(0.0, strength)
            s.S += random.uniform(strength, strength*2)

    # =========================================
    # QE DETEKCIA – normalizovaný threshold
    # =========================================
    def detect_qe_aporia(self) -> QEAporiaState:
        if not self.config.qe_enabled:
            return QEAporiaState(aporia=False, components=1, fragmentation_degree=0.0)
        n = len(self.poles)
        mean_T = sum(p.T for p in self.poles) / n
        mean_C = sum(p.C for p in self.poles) / n
        threshold = self.config.qe_threshold * (mean_T + mean_C)

        adj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist = abs(self.poles[i].T - self.poles[j].T) + abs(self.poles[i].C - self.poles[j].C)
                    if dist < threshold:
                        adj[i].append(j)

        visited = set()
        components = 0
        sizes = []
        for start in range(n):
            if start not in visited:
                components += 1
                stack = [start]
                size = 0
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        size += 1
                        stack.extend(adj[node])
                sizes.append(size)

        largest = max(sizes) if sizes else n
        frag = 1.0 - (largest / n) if n>0 else 0.0
        return QEAporiaState(aporia=components>1, components=components, fragmentation_degree=frag)

    def step_dynamics(self):
        self.redistribute_energy()
        self.update_tension()
        self.dissipate_coherence()
        self.apply_memory_entropy()
        self.inject_noise()
        if random.random() < 0.01:
            self.entropic_perturbation()
        self.detect_stagnation()
        for s in self.poles:
            s.clamp(self.config)
        self.step += 1

# =========================================
# EPISTEMICKÁ KRYPTOGRAFIA
# =========================================

class EpistemicCryptography:
    DOMINANCE_RATIO: float = 5.0
    MAX_LEDGER: int = 50000

    def __init__(self, history_window: int = 100):
        self.humility_history: List[float] = []
        self.history_window = history_window
        self.ltl_manager = LTLManager()
        self._ledger: List[Dict] = []

    @staticmethod
    def build_relational_matrix(poles: List[Sigma]) -> List[List[float]]:
        n = len(poles)
        A = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                val = abs(poles[i].T - poles[j].T) * ((poles[i].C + poles[j].C) / 2.0)
                A[i][j] = val
                A[j][i] = -val
        for i in range(n):
            for j in range(n):
                A[i][j] = (A[i][j] - A[j][i]) * 0.5
        for i in range(n):
            A[i][i] = 0.0
        return A

    # ----------------------------------------------------------
    # 2. Lokálna neistota μ – globálny priemer, váha 0.5
    # ----------------------------------------------------------
    @staticmethod
    def calculate_local_uncertainty(poles: List[Sigma]) -> List[float]:
        n = len(poles)
        mean_T = sum(p.T for p in poles) / n
        mu = []
        for i in range(n):
            mu_i = abs(poles[i].T - mean_T) + 0.5 * (1.0 - poles[i].C)
            mu.append(mu_i)
        return mu

    @staticmethod
    def compute_fingerprint(mu: List[float], A: List[List[float]], qe: bool, ltl: int) -> str:
        payload = {
            "LTL": ltl,
            "QE": qe,
            "mu": [round(v,8) for v in mu],
            "A": [[round(v,8) for v in row] for row in A]
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",",":"))
        return hashlib.sha256(serialized.encode()).hexdigest()

    @staticmethod
    def spectral_analysis(A: List[List[float]]) -> Tuple[List[complex], bool]:
        if not _NUMPY_AVAILABLE:
            return [], False
        matrix = np.array(A)
        if matrix.size == 0:
            return [], False
        eigs = np.linalg.eigvals(matrix)
        eigs = [complex(round(e.real,10), round(e.imag,10)) for e in eigs]
        eigs_sorted = sorted(eigs, key=lambda x: abs(x), reverse=True)
        dominant = False
        mags = [abs(e) for e in eigs_sorted]
        if len(mags) >= 2 and mags[1] > 1e-10:
            dominant = mags[0] > EpistemicCryptography.DOMINANCE_RATIO * mags[1]
        return list(eigs_sorted), dominant

    @staticmethod
    def structural_integrity(mu: List[float], A: List[List[float]], poles: List[Sigma]) -> int:
        n = len(poles)
        for i in range(n):
            for j in range(n):
                if abs(A[i][j] + A[j][i]) > 1e-9:
                    return 0
        if any(v < 0 for v in mu):
            return 0
        for p in poles:
            for v in (p.E, p.C, p.T, p.M, p.S):
                if not math.isfinite(v):
                    return 0
        return 1

    # ----------------------------------------------------------
    # 4. Triality monitoring – presnejšia heuristika
    # ----------------------------------------------------------
    @staticmethod
    def check_triality_symmetry(A: List[List[float]], eigenvalues: List[complex], dominant: bool) -> Optional[bool]:
        if len(A) != 8:
            return None
        if len(eigenvalues) < 3:
            return None
        mags = sorted([abs(e) for e in eigenvalues], reverse=True)
        ratio = mags[0] / max(mags[1], 1e-10)
        return ratio < EpistemicCryptography.DOMINANCE_RATIO

    @staticmethod
    def _total_asymmetry(A: List[List[float]]) -> float:
        n = len(A)
        total = 0.0
        for i in range(n):
            for j in range(i+1, n):
                total += abs(A[i][j])
        return total

    @staticmethod
    def _topological_humility(mu: List[float], A_total: float) -> float:
        mu_tot = sum(mu)
        denom = mu_tot + A_total
        return mu_tot / denom if denom > 0 else 1.0

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
        return sum((h-mean)**2 for h in self.humility_history) / len(self.humility_history)

    @property
    def ledger(self) -> List[Dict]:
        return list(self._ledger)

    def _append_ledger(self, ltl: int, fp: str, eigs: List[complex],
                       dom: bool, qe: bool, integ: int, tri: Optional[bool]):
        eig_repr = [{"re": round(e.real,8), "im": round(e.imag,8)} for e in eigs]
        entry = {
            "LTL": ltl,
            "hash": fp,
            "spectrum": eig_repr,
            "dominant_mode": dom,
            "QE": qe,
            "integrity": integ,
            "triality_preserved": tri
        }
        self._ledger.append(entry)
        if len(self._ledger) > self.MAX_LEDGER:
            self._ledger.pop(0)

    def get_ledger_summary(self) -> Dict:
        if not self._ledger:
            return {}
        return {
            "total_entries": len(self._ledger),
            "first_ltl": self._ledger[0]["LTL"],
            "last_ltl": self._ledger[-1]["LTL"],
            "qe_events": sum(1 for e in self._ledger if e.get("QE")),
            "dominant_events": sum(1 for e in self._ledger if e.get("dominant_mode")),
            "triality_breaks": sum(1 for e in self._ledger if e.get("triality_preserved") is False),
            "integrity_failures": sum(1 for e in self._ledger if e.get("integrity") == 0)
        }

    def compute_metrics(self, poles: List[Sigma], qe_aporia: bool = False) -> EpistemicMetrics:
        ltl = self.ltl_manager.next()
        A = self.build_relational_matrix(poles)
        mu = self.calculate_local_uncertainty(poles)
        fp = self.compute_fingerprint(mu, A, qe_aporia, ltl)
        eigs, dom = self.spectral_analysis(A)
        integ = self.structural_integrity(mu, A, poles)
        tri = self.check_triality_symmetry(A, eigs, dom)
        A_tot = self._total_asymmetry(A)
        h_topo = self._topological_humility(mu, A_tot)
        self._update_history(h_topo)
        dh = self._derivative()
        var = self._variance()
        self._append_ledger(ltl, fp, eigs, dom, qe_aporia, integ, tri)
        return EpistemicMetrics(
            mu=mu, A_matrix=A, fingerprint=fp, LTL=ltl,
            eigenvalues=eigs, dominant_mode=dom, integrity=integ,
            triality_preserved=tri, local_uncertainties=mu,
            total_asymmetry=A_tot, topological_humility=h_topo,
            humility_derivative=dh, humility_variance=var
      )

# =========================================
# EXPORT (JSONL)
# =========================================

class VortexExporter:
    def __init__(self, config: VortexConfig):
        self.config = config
        # zabezpečíme správnu príponu
        if not self.config.out_file.endswith('.jsonl'):
            self.config.out_file = self.config.out_file.replace('.json', '.jsonl')

    def export_state(self, step: int, poles: List[Sigma], qe_state: QEAporiaState,
                     epistemic: EpistemicMetrics, gate_eval: Optional[GateEvaluation] = None):
        snapshot = {
            "step": step,
            "timestamp": time.time(),
            "poles": [p.to_dict() for p in poles],
            "qe_aporia": qe_state.to_dict(),
            "epistemic": epistemic.to_dict()
        }
        if gate_eval:
            snapshot["3gate"] = gate_eval.to_dict()

        with open(self.config.out_file, "a") as f:
            f.write(json.dumps(snapshot) + "\n")

    def format_console_output(self, step: int, poles: List[Sigma], qe: QEAporiaState,
                              epistemic: EpistemicMetrics, stagnation: int) -> str:
        n = len(poles)
        avgE = sum(s.E for s in poles)/n
        avgC = sum(s.C for s in poles)/n
        avgT = sum(s.T for s in poles)/n
        avgM = sum(s.M for s in poles)/n
        avgS = sum(s.S for s in poles)/n
        qe_marker = f"[A{qe.components}]" if qe.aporia else "    "
        tri_marker = " T" if epistemic.triality_preserved is False else "  "
        return (f"[Φ] step={step:5d} {qe_marker}{tri_marker} | "
                f"E={avgE:.3f} C={avgC:.3f} T={avgT:.3f} M={avgM:.3f} S={avgS:.3f} | "
                f"h={epistemic.topological_humility:.3f} dh={epistemic.humility_derivative:+.4f} stg={stagnation}")

    def print_final_state(self, poles: List[Sigma], names: List[str]):
        print("\n"+"="*50)
        print("FINAL POLE STATES")
        print("="*50)
        for i,s in enumerate(poles):
            name = names[i] if i < len(names) else f"Σ{i+1}"
            print(f"{name}: E={s.E:.4f}  C={s.C:.4f}  T={s.T:.4f}  M={s.M:.4f}  S={s.S:.4f}")

# =========================================
# HLAVNÝ KONTROLÉR
# =========================================

class VectaetosSimulation:
    def __init__(self, config: Optional[VortexConfig] = None):
        self.config = config or VortexConfig()
        self.core = VortexCore(self.config)
        self.crypto = EpistemicCryptography(history_window=100)
        self.exporter = VortexExporter(self.config)
        self.threegate = ThreeGateMechanism()
        self.history: List[Dict[str, Any]] = []
        self.aporia_events: List[int] = []

    def run(self) -> Dict:
        self._print_header()
        start = time.time()
        for step in range(1, self.config.steps+1):
            self.core.step_dynamics()
            qe = self.core.detect_qe_aporia()
            if qe.aporia:
                self.aporia_events.append(step)
            if self.config.epistemic_crypto_enabled:
                ep = self.crypto.compute_metrics(self.core.poles, qe.aporia)
            else:
                ep = EpistemicMetrics()
            gate = None
            if self.config.threegate_enabled and self.config.threegate_audit_text:
                gate = self.threegate.evaluate(self.config.threegate_audit_text)
            if step % self.config.print_every == 0 and self.config.verbose:
                print(self.exporter.format_console_output(step, self.core.poles, qe, ep, self.core.stagnation_counter))
            if step % self.config.export_every == 0:
                self.exporter.export_state(step, self.core.poles, qe, ep, gate)
            self.history.append({
                "step": step,
                "aporia": qe.aporia,
                "components": qe.components,
                "humility": ep.topological_humility,
                "humility_derivative": ep.humility_derivative,
                "asymmetry": ep.total_asymmetry
            })
        elapsed = time.time() - start
        self.exporter.print_final_state(self.core.poles, self.config.singularity_names)
        self._print_summary(elapsed)
        return self._build_result(elapsed)

    def _print_header(self):
        if not self.config.verbose:
            return
        print("="*60)
        print("VECTAETOS :: UNIFIED SIMULATION VORTEX Φ v1.2.3")
        print("="*60)
        print(f"Poles: {self.config.poles} | Steps: {self.config.steps} | dt={self.config.dt}")
        print(f"Epistemic Crypto: {self.config.epistemic_crypto_enabled}")
        print(f"3Gate: {self.config.threegate_enabled}")
        print(f"QE Detection: {self.config.qe_enabled}")
        print(f"Singularity names: {', '.join(self.config.singularity_names)}")
        print("-"*60)

    def _print_summary(self, elapsed: float):
        if not self.config.verbose:
            return
        print("\n"+"="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        print(f"Total steps: {self.config.steps}")
        print(f"Aporia events: {len(self.aporia_events)}")
        if self.aporia_events:
            print(f"Aporia at steps: {self.aporia_events[:10]}{'...' if len(self.aporia_events)>10 else ''}")
        print(f"Final stagnation counter: {self.core.stagnation_counter}")
        if self.config.epistemic_crypto_enabled:
            s = self.crypto.get_ledger_summary()
            print(f"Ledger entries: {s.get('total_entries',0)}")
            print(f"Dominant mode events: {s.get('dominant_events',0)}")
            print(f"Triality breaks: {s.get('triality_breaks',0)}")
            print(f"Integrity failures I(X)=0: {s.get('integrity_failures',0)}")
        print(f"Elapsed time: {elapsed:.2f}s")
        print(f"Output file: {self.config.out_file}")
        print("="*60)

    def _build_result(self, elapsed: float) -> Dict:
        result = {
            "config": {
                "poles": self.config.poles,
                "steps": self.config.steps,
                "seed": self.config.seed,
                "dt": self.config.dt
            },
            "final_state": [p.to_dict() for p in self.core.poles],
            "aporia_events": self.aporia_events,
            "statistics": {"elapsed_time": elapsed, "total_steps": self.config.steps}
        }
        if self.config.epistemic_crypto_enabled:
            ledger = self.crypto.ledger
            result["epistemic_cryptography"] = {
                "ledger_size": len(ledger),
                "dominant_mode_events": sum(1 for e in ledger if e.get("dominant_mode")),
                "anomaly_events": sum(1 for e in ledger if e.get("integrity")==0),
                "qe_marker_events": sum(1 for e in ledger if e.get("QE")),
                "triality_breaks": sum(1 for e in ledger if e.get("triality_preserved") is False),
                "last_fingerprint": ledger[-1]["hash"] if ledger else "",
                "final_ltl": ledger[-1]["LTL"] if ledger else 0
            }
        return result

# =========================================
# POMOCNÉ FUNKCIE
# =========================================

def run_quick_test():
    config = VortexConfig(steps=1000, print_every=200, export_every=500, verbose=True)
    return VectaetosSimulation(config).run()

def run_with_3gate(audit_text: str):
    config = VortexConfig(steps=1000, print_every=200, threegate_enabled=True, threegate_audit_text=audit_text)
    return VectaetosSimulation(config).run()

def compare_seeds(seeds: List[int], steps: int = 500):
    results = []
    for seed in seeds:
        config = VortexConfig(seed=seed, steps=steps, verbose=False)
        res = VectaetosSimulation(config).run()
        results.append({"seed": seed, "aporia_events": len(res["aporia_events"])})
    print("\nSeed Comparison:")
    print("-"*30)
    for r in results:
        print(f"Seed {r['seed']:3d}: {r['aporia_events']} aporia events")
    return results

def ensemble_test(runs: int = 20, steps: int = 1000):
    counts = []
    for seed in range(runs):
        config = VortexConfig(seed=seed, steps=steps, verbose=False)
        res = VectaetosSimulation(config).run()
        counts.append(len(res["aporia_events"]))
    avg = sum(counts) / len(counts)
    print("\n" + "="*50)
    print(f"ENSEMBLE TEST ({runs} runs, {steps} steps each)")
    print("="*50)
    print(f"QE events per run: {counts}")
    print(f"Average QE events: {avg:.2f}")
    return counts

# =========================================
# MAIN
# =========================================

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=12000)
    parser.add_argument("--poles", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dt", type=float, default=0.05)
    parser.add_argument("--no-crypto", action="store_true")
    parser.add_argument("--gate3", type=str, default="")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--output", type=str, default="vortex_state.jsonl")
    args = parser.parse_args()

    config = VortexConfig(
        steps=args.steps,
        poles=args.poles,
        seed=args.seed,
        dt=args.dt,
        epistemic_crypto_enabled=not args.no_crypto,
        threegate_enabled=bool(args.gate3),
        threegate_audit_text=args.gate3,
        verbose=not args.quiet,
        out_file=args.output
    )
    VectaetosSimulation(config).run()

if __name__ == "__main__":
    main()
    sys.exit(0)
