#!/usr/bin/env python3
# cli/run.py
"""
VECTAETOS CLI runner.

Status:
    candidate / execution-projection adapter

Boundary:
    - This module is an execution/projection adapter.
    - It must not redefine Φ, mutate ontology, optimize trajectories, or treat
      signatures, registry hashes, ontology bindings, ledgers, or fingerprints as truth.
    - Side effects are ordered after VNAL validation.
    - Runtime failures are emitted as QE-shaped JSON reports.

Import boundary:
    The repository currently contains mixed-case module roots such as:

        Core/
        VNAL/
        vortex/Core/

    Linux path resolution is case-sensitive. This CLI therefore uses a deterministic
    repository-local import path and file-based fallback imports instead of relying on
    ambient PYTHONPATH.

Run from repository root:

    python3 cli/run.py

Controlled run:

    PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:${PYTHONPATH:-}" python3 cli/run.py

Syntax check:

    python3 -m py_compile cli/run.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Sequence


# =============================================================================
# REPOSITORY PATH BOUNDARY
# =============================================================================

CLI_DIR = Path(__file__).resolve().parent
REPO_ROOT = CLI_DIR.parent

DEFAULT_REGISTRY_PATH = REPO_ROOT / "outputs" / "registry.jsonl"
DEFAULT_ONTOLOGY_HASH_PATH = REPO_ROOT / "ontology_hash.json"

REGISTRY_NODES = (
    "http://localhost:8001/append",
    "http://localhost:8002/append",
)


def configure_repo_pythonpath() -> None:
    """
    Add only explicit repository-local paths.

    This does not claim ontology.
    This does not hide missing modules.
    This only makes mixed-case historical paths importable on Linux.
    """
    candidates = (
        REPO_ROOT,
        REPO_ROOT / "core",
        REPO_ROOT / "Core",
        REPO_ROOT / "vnal",
        REPO_ROOT / "VNAL",
        REPO_ROOT / "vortex",
        REPO_ROOT / "vortex" / "Core",
    )

    for path in reversed(candidates):
        if not path.exists():
            continue

        as_text = str(path)
        if as_text not in sys.path:
            sys.path.insert(0, as_text)


configure_repo_pythonpath()


# =============================================================================
# OPTIONAL REQUESTS
# =============================================================================

try:
    import requests
except ImportError:  # pragma: no cover - only used in minimal deployments
    requests = None  # type: ignore[assignment]


# =============================================================================
# IMPORT HELPERS
# =============================================================================

class CliImportError(RuntimeError):
    """Repository-local import boundary could not be resolved."""


@dataclass(frozen=True)
class LoadedRuntime:
    """Resolved runtime classes/functions required by the CLI."""

    VortexConfig: type
    VectaetosSimulation: type
    VectaetosIdentity: type
    OntologyBinding: type
    VectaetosSignature: type
    VectaetosRegistry: type
    validate_output: Callable[[Any], bool]
    VNALViolation: type[Exception]


def _module_name_from_path(prefix: str, path: Path) -> str:
    safe = "_".join(path.with_suffix("").parts[-4:])
    safe = safe.replace("-", "_").replace(".", "_")
    return f"{prefix}_{safe}"


def load_module_from_file(path: Path, *, prefix: str) -> ModuleType:
    """Load a Python module directly from a repository-relative file path."""
    if not path.exists():
        raise CliImportError(f"missing module file: {path}")

    module_name = _module_name_from_path(prefix, path)
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None or spec.loader is None:
        raise CliImportError(f"cannot create import spec for: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def load_first_existing(relative_paths: Sequence[str], *, prefix: str) -> ModuleType:
    """Load the first existing file from a list of repository-relative candidates."""
    checked: list[str] = []

    for rel in relative_paths:
        path = REPO_ROOT / rel
        checked.append(str(path))
        if path.exists():
            return load_module_from_file(path, prefix=prefix)

    joined = "\n  ".join(checked)
    raise CliImportError(f"none of the candidate module files exist:\n  {joined}")


def require_attr(module: ModuleType, attr: str) -> Any:
    """Return a required attribute or raise a deterministic import error."""
    if not hasattr(module, attr):
        raise CliImportError(f"module {module.__name__} does not expose {attr}")

    return getattr(module, attr)


def resolve_runtime() -> LoadedRuntime:
    """
    Resolve runtime imports from current repository layout.

    Preferred canonical future paths:
        core/vortex.py
        core/identity.py
        core/ontology_binding.py
        core/signature.py
        core/registry.py
        vnal/vnal_guard.py

    Current historical fallbacks:
        Core/vortex_v1.2.3.py
        Core/identity.py
        Core/ontology_binding.py
        Core/signature.py
        Core/registry.py
        vortex/Core/vnal_guard.py
        VNAL/cli_guard.py
    """
    vortex_module = load_first_existing(
        (
            "core/vortex.py",
            "Core/vortex.py",
            "Core/vortex_v1.2.3.py",
            "vortex/vortex_v1_2_3.py",
            "vortex/vortex_v2.0.py",
        ),
        prefix="vectaetos_vortex",
    )

    identity_module = load_first_existing(
        (
            "core/identity.py",
            "Core/identity.py",
        ),
        prefix="vectaetos_identity",
    )

    ontology_binding_module = load_first_existing(
        (
            "core/ontology_binding.py",
            "Core/ontology_binding.py",
        ),
        prefix="vectaetos_ontology_binding",
    )

    signature_module = load_first_existing(
        (
            "core/signature.py",
            "Core/signature.py",
        ),
        prefix="vectaetos_signature",
    )

    registry_module = load_first_existing(
        (
            "core/registry.py",
            "Core/registry.py",
        ),
        prefix="vectaetos_registry",
    )

    vnal_module = load_first_existing(
        (
            "vnal/vnal_guard.py",
            "VNAL/vnal_guard.py",
            "vortex/Core/vnal_guard.py",
            "VNAL/cli_guard.py",
        ),
        prefix="vectaetos_vnal",
    )

    return LoadedRuntime(
        VortexConfig=require_attr(vortex_module, "VortexConfig"),
        VectaetosSimulation=require_attr(vortex_module, "VectaetosSimulation"),
        VectaetosIdentity=require_attr(identity_module, "VectaetosIdentity"),
        OntologyBinding=require_attr(ontology_binding_module, "OntologyBinding"),
        VectaetosSignature=require_attr(signature_module, "VectaetosSignature"),
        VectaetosRegistry=require_attr(registry_module, "VectaetosRegistry"),
        validate_output=require_attr(vnal_module, "validate_output"),
        VNALViolation=require_attr(vnal_module, "VNALViolation"),
    )


# =============================================================================
# JSON OUTPUT
# =============================================================================

def emit_json(payload: dict[str, Any]) -> None:
    """Emit deterministic human-readable JSON."""
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def emit_qe(reason: str, *, stage: str) -> None:
    """
    Emit a non-authoritative QE report.

    QE here exposes a boundary.
    It is not a fallback answer.
    It is not truth.
    It is not refusal.
    """
    emit_json(
        {
            "type": "QE",
            "stage": stage,
            "reason": reason,
            "uncertainty": {"level": "max"},
            "identity": "UNKNOWN",
        }
    )


# =============================================================================
# PROJECTION
# =============================================================================

def project_output(raw_result: dict[str, Any]) -> dict[str, Any]:
    """
    Project raw Vortex output into a serializable report structure.

    The proof field is treated as provenance/fingerprint material only.
    It must not be read as truth or ontological validity.
    """
    epistemic = raw_result.get("epistemic_cryptography", {})
    if not isinstance(epistemic, dict):
        epistemic = {}

    proof = (
        epistemic.get("proof")
        or epistemic.get("last_fingerprint")
        or epistemic.get("fingerprint")
        or raw_result.get("proof")
        or ""
    )

    identity = raw_result.get("identity", "UNKNOWN")

    return {
        "type": "trajectory",
        "uncertainty": {
            "level": "derived",
            "aporia_events": len(raw_result.get("aporia_events", [])),
        },
        "identity": identity,
        "proof": str(proof),
        "data": raw_result,
    }


def ensure_identity(raw_result: dict[str, Any], runtime: LoadedRuntime) -> dict[str, Any]:
    """
    Add fallback identity only when the simulation returned epistemic data
    but no identity block.

    This is descriptive normalization.
    It is not identity authority.
    """
    if "identity" in raw_result:
        return raw_result

    epistemic = raw_result.get("epistemic_cryptography")
    if not isinstance(epistemic, dict):
        return raw_result

    raw_result["identity"] = runtime.VectaetosIdentity.validate(
        {
            "topological_humility": epistemic.get("topological_humility", 0.0),
            "integrity": epistemic.get("integrity", 1),
            "dominant_mode": epistemic.get("dominant_mode", False),
        }
    )

    return raw_result


def attach_ontology_binding(
    output: dict[str, Any],
    runtime: LoadedRuntime,
    *,
    ontology_hash_path: Path = DEFAULT_ONTOLOGY_HASH_PATH,
) -> dict[str, Any]:
    """
    Attach ontology binding after projection, when output["proof"] exists.

    The binding is provenance / integrity evidence only.
    It is not truth.
    It is not interpretation.
    It is not authority.
    """
    proof = output.get("proof")
    if not proof:
        raise ValueError("Cannot bind ontology: output proof is missing.")

    if not ontology_hash_path.exists():
        raise FileNotFoundError(f"Missing ontology hash file: {ontology_hash_path}")

    binder = runtime.OntologyBinding(str(ontology_hash_path))
    output["ontology_binding"] = binder.bind(str(proof))
    return output


# =============================================================================
# REMOTE SYNC
# =============================================================================

def sync_to_nodes(output: dict[str, Any], nodes: Iterable[str] = REGISTRY_NODES) -> list[dict[str, Any]]:
    """
    Best-effort remote sync.

    Sync errors are represented in the report.
    They must not feed back into Φ.
    They must not retroactively alter the projected trajectory.
    """
    results: list[dict[str, Any]] = []

    if requests is None:
        return [
            {
                "node": node,
                "status": "SKIPPED",
                "error": "requests is not installed",
            }
            for node in nodes
        ]

    for node in nodes:
        try:
            response = requests.post(node, json=output, timeout=2)
            results.append(
                {
                    "node": node,
                    "status": response.status_code,
                }
            )
        except requests.RequestException as exc:
            results.append(
                {
                    "node": node,
                    "status": "ERROR",
                    "error": str(exc),
                }
            )

    return results


# =============================================================================
# CONFIG
# =============================================================================

@dataclass(frozen=True)
class CliArgs:
    steps: int | None
    poles: int | None
    seed: int | None
    dt: float | None
    output: Path | None
    registry: Path
    ontology_hash: Path
    quiet: bool
    no_crypto: bool
    no_sync: bool
    skip_ontology_binding: bool


def parse_args(argv: Sequence[str] | None = None) -> CliArgs:
    parser = argparse.ArgumentParser(
        description="VECTAETOS CLI projection runner."
    )

    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--poles", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--dt", type=float, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--ontology-hash", type=Path, default=DEFAULT_ONTOLOGY_HASH_PATH)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-crypto", action="store_true")
    parser.add_argument("--no-sync", action="store_true")
    parser.add_argument(
        "--skip-ontology-binding",
        action="store_true",
        help="Skip ontology binding for local smoke/debug runs only.",
    )

    args = parser.parse_args(argv)

    return CliArgs(
        steps=args.steps,
        poles=args.poles,
        seed=args.seed,
        dt=args.dt,
        output=args.output,
        registry=args.registry,
        ontology_hash=args.ontology_hash,
        quiet=args.quiet,
        no_crypto=args.no_crypto,
        no_sync=args.no_sync,
        skip_ontology_binding=args.skip_ontology_binding,
    )


def build_vortex_config(runtime: LoadedRuntime, args: CliArgs) -> Any:
    """
    Build VortexConfig using only attributes explicitly supplied by the user.

    This keeps compatibility with historical VortexConfig versions.
    """
    config_kwargs: dict[str, Any] = {}

    if args.steps is not None:
        config_kwargs["steps"] = args.steps
    if args.poles is not None:
        config_kwargs["poles"] = args.poles
    if args.seed is not None:
        config_kwargs["seed"] = args.seed
    if args.dt is not None:
        config_kwargs["dt"] = args.dt
    if args.output is not None:
        config_kwargs["out_file"] = str(args.output)
    if args.quiet:
        config_kwargs["verbose"] = False
    if args.no_crypto:
        config_kwargs["epistemic_crypto_enabled"] = False

    return runtime.VortexConfig(**config_kwargs)


# =============================================================================
# MAIN
# =============================================================================

def run_pipeline(args: CliArgs) -> dict[str, Any]:
    """
    Execute the CLI pipeline.

    Side effects are intentionally ordered:
        projection -> ontology binding -> VNAL validation -> signature -> registry -> sync

    Registry and sync happen only after validation.
    """
    runtime = resolve_runtime()

    config = build_vortex_config(runtime, args)
    sim = runtime.VectaetosSimulation(config)

    raw = sim.run()
    if not isinstance(raw, dict):
        raise TypeError("Simulation returned non-dict output.")

    raw = ensure_identity(raw, runtime)
    output = project_output(raw)

    if args.skip_ontology_binding:
        output["ontology_binding"] = {
            "status": "SKIPPED",
            "reason": "skip_ontology_binding was explicitly requested",
        }
    else:
        output = attach_ontology_binding(
            output,
            runtime,
            ontology_hash_path=args.ontology_hash,
        )

    runtime.validate_output(output)

    output["signature"] = runtime.VectaetosSignature.sign_output(output)

    registry_path = args.registry
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry = runtime.VectaetosRegistry(str(registry_path))
    record = registry.append(output)

    output["registry"] = {
        "path": str(registry_path),
        "entry_hash": record["entry_hash"],
    }

    if args.no_sync:
        output["sync"] = [
            {
                "status": "SKIPPED",
                "reason": "no_sync was explicitly requested",
            }
        ]
    else:
        output["sync"] = sync_to_nodes(output)

    return output


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        output = run_pipeline(args)
        emit_json(output)
        return 0

    except Exception as exc:
        # VNALViolation and all import/runtime failures fail closed into QE-shaped JSON.
        # This exposes the boundary instead of emitting a partial authoritative result.
        stage = "runtime"

        if isinstance(exc, CliImportError):
            stage = "import_boundary"
        else:
            try:
                runtime = resolve_runtime()
                if isinstance(exc, runtime.VNALViolation):
                    stage = "vnal_validation"
            except Exception:
                stage = "runtime"

        emit_qe(str(exc), stage=stage)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
