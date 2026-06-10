# VECTAETOS™ — PIS Research Notes

**Path:** `research/pis/`  
**Status:** research / proposal layer  
**Active enforcement:** no  
**Ontology authority:** none  

## Purpose

This directory contains research notes for the **Protected Immutable Surface** model.

PIS is a repository-perimeter idea for protecting sensitive paths from silent mutation.

It is not active CI policy yet.

## Current Scope

The current minimal direction is to protect only:

```text
anchors/
formal/
contracts/
guards/core/
```

The full PIS model remains research until the minimal layer is stable.

## Files

Expected files may include:

```text
PIS_PROTECTED_IMMUTABLE_SURFACE_MODEL.md
PIS_MINIMAL_APPLIED_PROFILE.md
protected_surface_manifest.minimal.json
UNLOCK_TEMPLATE_SOLO_MAINTAINER.json
PIS_MINIMAL_IMPLEMENTATION_NOTES.md
```

## Boundary

These files do not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

They do not prove truth, safety, or deployment validity.

They describe repository hardening proposals.

## Solo Maintainer Mode

Current assumption:

```text
one human maintainer
AI review is advisory only
solo signature is temporary audit friction
```

A minimal unlock record may use:

```text
signed_by: Richard Fonfára
confirmation: I confirm solo-maintainer protected-surface unlock.
```

## Future Migration

If the minimal model becomes stable, selected parts may move from:

```text
research/pis/
```

to active locations such as:

```text
contracts/
guards/
.github/workflows/
```

Only after review and testing.

## Final Boundary

```text
research/pis/ explores protected repository surfaces.
It does not decide what VECTAETOS is.
```
