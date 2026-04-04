# Re-export submodules for clean API

from epistemic_cryptography.ek_core import canonical
from epistemic_cryptography.ek_core import representability
from epistemic_cryptography.ek_core.canonical import canonicalize, apply_permutation
from epistemic_cryptography.ek_core.hash import structural_hash
from epistemic_cryptography.ek_core.representability import is_representable
from epistemic_cryptography.ek_core.pipeline import run_pipeline
from epistemic_cryptography.ek_core.kappa import kappa_signature

__all__ = [
    "canonical",
    "representability",
]
