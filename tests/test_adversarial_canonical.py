import pytest
import numpy as np
from ek_core.canonical import canonicalize, apply_permutation

def random_delta():
    return {(i,j,k): np.random.randn()
            for i in range(8)
            for j in range(i+1,8)
            for k in range(j+1,8)}

def test_orbit_invariance():
    delta = random_delta()

    perm = tuple(np.random.permutation(8))
    delta_perm = apply_permutation(delta, perm)

    c1 = canonicalize(delta)
    c2 = canonicalize(delta_perm)

    assert c1 == c2, "Canonicalization breaks orbit invariance"
