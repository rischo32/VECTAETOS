# core/proof.py

import json
import hashlib
from itertools import permutations, combinations


class CanonicalIdentityProof:
    """
    Canonical Identity Proof (S₈ + Triality + Identity binding)

    Guarantees:
    - invariant under permutation of poles (S₈)
    - sensitive to triality breaking
    - bound to epistemic identity
    """

    # =========================
    # CANONICALIZATION (S₈)
    # =========================
    @staticmethod
    def canonicalize(A):
        """
        Find canonical representative under S₈ permutations.
        Lexicographic minimum over all permutations.
        """
        n = len(A)

        if n == 0:
            return A

        best_key = None
        best_matrix = None

        for perm in permutations(range(n)):
            B = [[A[perm[i]][perm[j]] for j in range(n)] for i in range(n)]

            key = tuple(
                tuple(round(v, 6) for v in row)
                for row in B
            )

            if best_key is None or key < best_key:
                best_key = key
                best_matrix = B

        return best_matrix

    # =========================
    # DELTA (Δ)
    # =========================
    @staticmethod
    def compute_delta(A):
        """
        Δ(i,j,k) = A_ij + A_jk + A_ki
        """
        n = len(A)
        delta = []

        if n < 3:
            return []

        for i, j, k in combinations(range(n), 3):
            val = A[i][j] + A[j][k] + A[k][i]
            delta.append(round(val, 6))

        # canonical ordering
        return sorted(delta)

    # =========================
    # TRIALITY INVARIANT
    # =========================
    @staticmethod
    def triality_score(delta):
        """
        Variance of Δ distribution
        Low variance → preserved symmetry
        High variance → broken symmetry
        """
        if not delta:
            return 0.0

        mean = sum(delta) / len(delta)
        var = sum((d - mean) ** 2 for d in delta) / len(delta)

        return round(var, 6)

    # =========================
    # IDENTITY BLOCK
    # =========================
    @staticmethod
    def identity_block(ep):
        """
        Extract epistemic identity invariants
        """
        return {
            "h": round(ep.get("topological_humility", 0.0), 6),
            "integrity": int(ep.get("integrity", 0)),
            "dominant": bool(ep.get("dominant_mode", False))
        }

    # =========================
    # NORMALIZATION
    # =========================
    @staticmethod
    def normalize_matrix(A):
        """
        Ensure stable float representation
        """
        return [
            [round(v, 6) for v in row]
            for row in A
        ]

    # =========================
    # FINAL PROOF
    # =========================
    @classmethod
    def compute_proof(cls, A, ep):
        """
        Canonical Identity Proof

        P = H( canonical(A) + Δ + triality + identity )
        """

        if A is None:
            raise ValueError("A matrix is None")

        # 1. canonical form
        A_canon = cls.canonicalize(A)

        # 2. normalize (prevents float drift)
        A_norm = cls.normalize_matrix(A_canon)

        # 3. delta
        delta = cls.compute_delta(A_norm)

        # 4. triality invariant
        triality = cls.triality_score(delta)

        # 5. identity binding
        identity = cls.identity_block(ep)

        # 6. payload
        payload = {
            "A": A_norm,
            "delta": delta,
            "triality": triality,
            "identity": identity
        }

        # 7. deterministic serialization
        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        )

        # 8. hash
        return hashlib.sha256(serialized.encode()).hexdigest()
