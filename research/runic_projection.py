#!/usr/bin/env python3
# =========================================
# VECTAETOS — RUNIC PROJECTION (DESCRIPTIVE)
# =========================================
# Runy sú projekcia stavu poľa Φ
# ŽIADNE rozhodovanie, ŽIADNA spätná väzba
# =========================================

from enum import Enum
from dataclasses import dataclass
from typing import List


# -------------------------------------------------
# EPISTEMICKÉ STAVY RUNY
# -------------------------------------------------

class RuneState(Enum):
    STABLE = "◯"        # koherentný, nízke napätie
    TENSION = "△"       # rastúca tenzia
    TRANSITION = "◇"    # prechodový stav
    APORIA = "⊘"        # nerealizovateľná projekcia (QE)


# -------------------------------------------------
# AXIOMATICKÉ ŤAŽISKÁ
# -------------------------------------------------

class Axiom(Enum):
    INT = "ᚨ"   # Intention
    LEX = "ᛚ"   # Existence
    VER = "ᚱ"   # Truth
    LIB = "ᚦ"   # Freedom
    UNI = "ᛜ"   # Unity
    REL = "ᚷ"   # Relation
    WIS = "ᛟ"   # Wisdom
    CRE = "ᛞ"   # Creation


# -------------------------------------------------
# STAV Σ (SIGMA)
# -------------------------------------------------

@dataclass(frozen=True)
class SigmaState:
    E: float   # energia / aktivita
    C: float   # koherencia
    T: float   # tenzia
    M: float   # pamäť (rezonančná)
    S: float   # entropia / rozpad


# -------------------------------------------------
# RUNA (PROJEKCIA)
# -------------------------------------------------

@dataclass(frozen=True)
class Rune:
    symbol: str
    axiom: Axiom
    state: RuneState
    dynamics: str      # rising | falling | stable | oscillating


# -------------------------------------------------
# JADRO PROJEKCIE Σ → RUNA
# -------------------------------------------------

def project_sigma_to_rune(
    sigma: SigmaState,
    axiom: Axiom,
    kappa: float
) -> Rune:
    """
    Čisto deskriptívna projekcia stavu Σ do runy.
    Neobsahuje rozhodovanie ani spätný zásah.
    """

    # QE / Aporia — nerealizovateľná projekcia
    if sigma.C < kappa or sigma.S > 0.85:
        return Rune(
            symbol="⊘",
            axiom=axiom,
            state=RuneState.APORIA,
            dynamics="undefined"
        )

    # Epistemický stav podľa tenzie
    if sigma.T < 0.25:
        state = RuneState.STABLE
    elif sigma.T < 0.55:
        state = RuneState.TENSION
    else:
        state = RuneState.TRANSITION

    # Dynamika ako stopa pohybu (nie smer akcie)
    if sigma.E > 0.65 and sigma.C > 0.6:
        dynamics = "rising"
    elif sigma.E < 0.35 or sigma.S > 0.6:
        dynamics = "falling"
    elif abs(sigma.T - 0.5) < 0.05:
        dynamics = "oscillating"
    else:
        dynamics = "stable"

    return Rune(
        symbol=axiom.value,
        axiom=axiom,
        state=state,
        dynamics=dynamics
    )


# -------------------------------------------------
# PROJEKCIA CELÉHO POĽA Φ → RUNY
# -------------------------------------------------

def project_field_to_runes(
    sigmas: List[SigmaState],
    kappa: float
) -> List[Rune]:
    """
    Projekcia Φ → runová konfigurácia.
    Bez optimalizácie, bez spätnej väzby.
    """
    runes: List[Rune] = []

    for sigma, axiom in zip(sigmas, Axiom):
        runes.append(
            project_sigma_to_rune(sigma, axiom, kappa)
        )

    return runes


# -------------------------------------------------
# TEST / DEMO (LEN NA LOKÁLNE OVERENIE)
# -------------------------------------------------

if __name__ == "__main__":
    sigmas = [
        SigmaState(0.7, 0.8, 0.1, 0.2, 0.1),
        SigmaState(0.4, 0.6, 0.3, 0.3, 0.2),
        SigmaState(0.2, 0.5, 0.6, 0.5, 0.3),
        SigmaState(0.9, 0.9, 0.2, 0.1, 0.1),
        SigmaState(0.5, 0.7, 0.4, 0.4, 0.2),
        SigmaState(0.6, 0.8, 0.2, 0.3, 0.1),
        SigmaState(0.3, 0.6, 0.5, 0.6, 0.4),
        SigmaState(0.8, 0.9, 0.15, 0.2, 0.1),
    ]

    runes = project_field_to_runes(sigmas, kappa=0.4)

    for r in runes:
        print(f"{r.symbol} {r.state.value} ({r.dynamics})")
