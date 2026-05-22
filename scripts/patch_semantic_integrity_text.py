#!/usr/bin/env python3
from pathlib import Path

REPLACEMENTS = {
    "EMPIRICAL_EVIDENCE_ROADMAP_ANCHOR.md": {
        "LLM-as-decision-maker": "language-adapter authority assignment",
    },
    "LICENSE.md": {
        "represents VECTAETOS as an autonomous agent": (
            "presents the framework as carrying execution power, "
            "control power, or outcome authority"
        ),
    },
    "anchors/TRIADIC_ARCHITECTURE_AND_TRIALITY.md": {
        "ASI_MOD claims truth authority": (
            "the dialogic layer is treated as the source of epistemic ground"
        ),
    },
}

DISAMBIGUATION_INSERTS = {
    "formal/EPISTEMIC_LAYERS_AND_STREAMS.md": {
        "## 5. EAT – Error Accountability Trace": (
            "Canonical meaning in this context: EAT = Error Accountability Trace.\n"
        ),
    },
    "formal/EPISTEMIC_LAYER_GLOSSARY.md": {
        "## EAT – Error Accountability Trace": (
            "Canonical meaning in this context: EAT = Error Accountability Trace.\n"
        ),
        "## NIR — Non-Intervention Regime": (
            "Canonical meaning in this context: NIR = Non-Intervention Regime.\n"
        ),
    },
    "formal/NIR.md": {
        "# NIR — Non-Intervention Regime": (
            "Canonical meaning in this context: NIR = Non-Intervention Regime.\n"
        ),
    },
    "formal/PIPELINE.md": {
        "## 9. NIR — Non-Intervention Regime": (
            "Canonical meaning in this context: NIR = Non-Intervention Regime.\n"
        ),
    },
    "infrastructure/web/WEB_INTERACTION_LIMITS.md": {
        "NIR (Non-Intervention Regime):": (
            "Canonical meaning in this context: NIR = Non-Intervention Regime.\n"
        ),
    },
    "infrastructure/web/WEB_SILENCE_MODES.md": {
        "### 3.2 Ticho NIR (Non-Intervention Regime)": (
            "Canonical meaning in this context: NIR = Non-Intervention Regime.\n"
        ),
    },
}


def replace_exact(path: Path, replacements: dict[str, str]) -> bool:
    if not path.exists():
        print(f"MISS file: {path}")
        return False

    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in replacements.items():
        if old not in text:
            print(f"MISS text in {path}: {old}")
            continue
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"PATCHED: {path}")
        return True

    return False


def insert_after_heading(path: Path, inserts: dict[str, str]) -> bool:
    if not path.exists():
        print(f"MISS file: {path}")
        return False

    text = path.read_text(encoding="utf-8")
    original = text

    for heading, line in inserts.items():
        if line.strip() in text:
            continue
        if heading not in text:
            print(f"MISS heading in {path}: {heading}")
            continue

        text = text.replace(heading, f"{heading}\n\n{line}", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"DISAMBIGUATED: {path}")
        return True

    return False


def main() -> int:
    changed = False

    for file_name, replacements in REPLACEMENTS.items():
        changed |= replace_exact(Path(file_name), replacements)

    for file_name, inserts in DISAMBIGUATION_INSERTS.items():
        changed |= insert_after_heading(Path(file_name), inserts)

    if changed:
        print("Done. Re-run semantic integrity check.")
    else:
        print("No changes made. Check paths or exact text.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
