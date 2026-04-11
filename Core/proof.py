# Core/proof.py

import json
import hashlib
from itertools import permutations, combinations

class CanonicalIdentityProof:

    @staticmethod
    def canonicalize(A):
        """
        S₈ canonical form (lexicographic minimum)
        """
        n = len(A)
        best = None

        for perm in permutations(range(n)):
            B = [[A[perm[i]][perm[j]] for j in range(n)] for i in range(n)]
            key = tuple(tuple(round(v, 6) for v in row) for row in B)

            if best is None or key < best[0]:
                best = (key, B)

        return best[1]

    @staticmethod
    def compute_delta(A):
        """
        Δ(i,j,k) = A_ij + A_jk + A_ki
        """
        n = len(A)
        delta = []

        for i, j, k in combinations(range(n), 3):
            val = A[i][j] + A[j][k] + A[k][i]
            delta.append(round(val, 6))

        return sorted(delta)

    @staticmethod
    def triality_score(delta):
        """
        jednoduchý invariant:
        nízka variancia = zachovaná trialita
        """
        if len(delta) < 2:
            return 0.0

        mean = sum(delta) / len(delta)
        var = sum((d - mean) ** 2 for d in delta) / len(delta)

        return round(var, 6)

    @staticmethod
    def identity_block(ep):
        return {
            "h": round(ep["topological_humility"], 6),
            "integrity": ep["integrity"],
            "dominant": ep["dominant_mode"]
        }

    @classmethod
    def compute_proof(cls, A, ep):
        """
        FINAL PROOF
        """

        A_canon = cls.canonicalize(A)
        delta = cls.compute_delta(A_canon)
        triality = cls.triality_score(delta)

        payload = {
            "A": A_canon,
            "delta": delta,
            "triality": triality,
            "identity": cls.identity_block(ep)
        }

        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
