import pytest
import numpy as np
from ek_core.representability import is_representable

def random_invalid_delta():
    # náhodný Δ mimo Im(d)
    return np.random.randn(56)

def test_reject_non_representable():
    delta = random_invalid_delta()
    assert not is_representable(delta), "Non-representable Δ passed"
