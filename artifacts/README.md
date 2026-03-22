# VECTAETOS — Artifacts

This directory contains generated outputs from the Vortex Φ runtime.

## Contents

### multi_run.json
Latest multi-trajectory projection of the field Φ.

Includes:
- aggregated metrics (E, C, T, M, S)
- variance (T_var)
- aporia distribution
- trajectory samples

This file is continuously updated by CI.

---

### snapshots/
Optional visual outputs from selected Vortex runs.

Contains:
- representative projections
- diagnostic visualizations
- NOT full history

---

## Principles

Artifacts are:

- deterministic outputs of the system
- non-authoritative representations
- projections, not decisions

No optimization, filtering, or selection is applied.

---

## Notes

- This directory may change frequently due to CI updates.
- Only selected visual outputs should be stored to avoid repository bloat.
- Full history is not preserved here.

---

## Relation to Φ

Artifacts are:

```text
Π(Φ | Σᵢ)
