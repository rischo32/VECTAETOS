# Epistemic Audit Interface (EAI)

EAI umožňuje rekonštruovať štruktúru systému výlučne z jeho reakcií na perturbácie.

This module implements the framework defined in:

/papers/vectaetos_non_intervention_framework.pdf

## Kľúčová veta

Systém je definovaný nie tým čo robí, ale tým ako sa mení.

## Pipeline

input → perturbácie → outputs → encode → Δ → R → Spec → κ → fingerprint

## Vlastnosti

* Black-box compatible
* Domain-agnostic
* Non-intervention
* Deterministic

## Výstup

Φ̂ = rekonštruované pole systému
