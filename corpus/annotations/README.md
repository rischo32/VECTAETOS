# ZMYSEL SIGMA ANNOTATIONS

## Purpose

This directory contains machine-readable Σ-bound semantic sidecars for ZMYSEL Corpus entries.

Each `.sigma.json` file describes how a human-readable corpus entry relates to the eight VECTAETOS singularities:

- INT
- LEX
- VER
- LIB
- UNI
- REL
- WIS
- CRE

These files are semantic annotations.

They are not decision files.

They are not formal proofs.

They are not runtime instructions.

They are not authority layers.

---

## Rules
___
presná hranica:

slovo nesmie vstúpiť do Φ
do systému môže vstúpiť iba ohraničená Σ anotácia
___
Every annotation must preserve:

    json
    {
    "authority": false,
    "decision_effect": false,
    "optimization_effect": false,
    "ranking_effect": false,
    "phi_effect": false
    }

Umožňuje fragmentom ZMYSEL korpusu niesť strojovo čitateľnú existenciálnu nosnosť vo vzťahu k axiomatickým singularitám VECTAETOS, bez autority, skóre, priority, optimalizácie alebo spätného vplyvu na Φ.

Prečo „sidecar“

Sidecar znamená: hlavný text sa nemení, ale vedľa neho existuje strojovo čitateľná anotácia.

Výhoda:

+ ľudský text ostáva čistý
+ strojová vrstva je auditovateľná
+ vyššia vrstva vie čítať význam
+ Φ sa nemení
+ parser nerozhoduje

Correct Use

Allowed:

+ semantic grounding,
+ retrieval support,
+ interpretive context,
+ fragment explanation,
+ higher-layer reading.

Forbidden:

+ truth verdicts,
+ ranking,
+ scoring,
+ priority assignment,
+ optimization,
+ execution,
+ feedback into Φ,
+ changing VECTAETOS ontology.

Canonical Sentence

A .sigma.json file is a read-only semantic sidecar that lets a ZMYSEL fragment carry existential meaning in relation to VECTAETOS singularities without producing authority, priority, decision, optimization, or influence on Φ.
