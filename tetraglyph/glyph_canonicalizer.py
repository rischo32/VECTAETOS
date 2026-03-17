# =========================================
# VECTAETOS :: TETRAGLYPH CANONICALIZER
# Version: 1.0.0
# Topology → Canonical Form → Hash
# =========================================

import hashlib
import json
from typing import List, Tuple, Dict


# =========================================
# DÁTOVÁ ŠTRUKTÚRA
# =========================================

class GlyphFragment:
    def __init__(self, nodes: List[int], edges: List[Tuple[int, int]]):
        self.nodes = nodes
        self.edges = edges


# =========================================
# 1. NORMALIZÁCIA HRÁN
# =========================================

def normalize_edges(edges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Každú hranu zoradí (menší, väčší)
    """
    return [tuple(sorted(edge)) for edge in edges]


# =========================================
# 2. KANONICKÉ USPORIADANIE
# =========================================

def canonical_form(fragment: GlyphFragment) -> Dict:
    """
    Vytvorí deterministickú reprezentáciu grafu
    """

    # zoradiť uzly
    nodes_sorted = sorted(fragment.nodes)

    # normalizovať hrany
    edges_normalized = normalize_edges(fragment.edges)

    # zoradiť hrany
    edges_sorted = sorted(edges_normalized)

    return {
        "nodes": nodes_sorted,
        "edges": edges_sorted
    }


# =========================================
# 3. SERIALIZÁCIA
# =========================================

def serialize_canonical(canonical: Dict) -> str:
    """
    Deterministická JSON reprezentácia
    """
    return json.dumps(canonical, sort_keys=True, separators=(",", ":"))


# =========================================
# 4. HASH (SHA256)
# =========================================

def compute_hash(serialized: str) -> str:
    return hashlib.sha256(serialized.encode()).hexdigest()


# =========================================
# 5. HLAVNÁ FUNKCIA
# =========================================

def canonicalize(fragment: GlyphFragment) -> Dict:
    """
    Returns:
        {
            canonical_form,
            serialized,
            hash
        }
    """

    canon = canonical_form(fragment)
    serialized = serialize_canonical(canon)
    h = compute_hash(serialized)

    return {
        "canonical_form": canon,
        "serialized": serialized,
        "hash": h
    }


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    # graf A
    g1 = GlyphFragment(
        nodes=[2,1,0],
        edges=[(2,1),(0,1)]
    )

    # rovnaký graf, iné poradie
    g2 = GlyphFragment(
        nodes=[0,1,2],
        edges=[(1,0),(1,2)]
    )

    c1 = canonicalize(g1)
    c2 = canonicalize(g2)

    print("Hash 1:", c1["hash"])
    print("Hash 2:", c2["hash"])

    print("Match:", c1["hash"] == c2["hash"])
