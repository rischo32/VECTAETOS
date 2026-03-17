# =========================================
# VECTAETOS :: TETRAGLYPH VALIDATOR
# Version: 1.1.0 (cycle-corrected)
# Pure Topological Validator (No Semantics)
# =========================================

from typing import List, Dict, Tuple, Set


# =========================================
# DÁTOVÁ ŠTRUKTÚRA
# =========================================

class GlyphFragment:
    def __init__(self, nodes: List[int], edges: List[Tuple[int, int]]):
        self.nodes = nodes
        self.edges = edges


# =========================================
# POMOCNÉ FUNKCIE
# =========================================

def build_adjacency(fragment: GlyphFragment) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = {n: [] for n in fragment.nodes}
    for a, b in fragment.edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def degree(node: int, adj: Dict[int, List[int]]) -> int:
    return len(adj[node])


# =========================================
# 1. CONNECTIVITY
# =========================================

def is_connected(fragment: GlyphFragment) -> bool:
    if not fragment.nodes:
        return False

    adj = build_adjacency(fragment)
    visited: Set[int] = set()

    stack = [fragment.nodes[0]]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(adj[node])

    return len(visited) == len(fragment.nodes)


# =========================================
# 2. CYCLE DETECTION (kľúčové!)
# =========================================

def has_cycle(fragment: GlyphFragment) -> bool:
    adj = build_adjacency(fragment)
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for n in fragment.nodes:
        if n not in visited:
            if dfs(n, -1):
                return True

    return False


# =========================================
# 3. DOMINANT PATTERN (opravené)
# =========================================

def has_dominant_pattern(fragment: GlyphFragment) -> bool:
    adj = build_adjacency(fragment)
    n = len(fragment.nodes)

    # malé grafy nemajú dominanciu
    if n < 4:
        return False

    degrees = [degree(node, adj) for node in fragment.nodes]

    return max(degrees) > (0.75 * (n - 1))


# =========================================
# 4. BALANCE (sprísnené)
# =========================================

def is_balanced(fragment: GlyphFragment) -> bool:
    adj = build_adjacency(fragment)

    if not fragment.nodes:
        return False

    degrees = [degree(node, adj) for node in fragment.nodes]

    return (max(degrees) - min(degrees)) <= 1


# =========================================
# 5. VALIDATOR
# =========================================

def validate(fragment: GlyphFragment) -> str:
    """
    Returns:
        "COHERENT_REGION"
        "CONFLICT_REGION"
        "QE"
    """

    # QE = nesúvislosť
    if not is_connected(fragment):
        return "QE"

    # QE = bez cyklu (žiadna krivosť)
    if not has_cycle(fragment):
        return "QE"

    # konflikt = dominancia
    if has_dominant_pattern(fragment):
        return "CONFLICT_REGION"

    # koherencia = vyvážená cyklická topológia
    if is_balanced(fragment):
        return "COHERENT_REGION"

    # fallback
    return "CONFLICT_REGION"


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    # 1. LINE (QE)
    line = GlyphFragment(
        nodes=[0,1,2],
        edges=[(0,1),(1,2)]
    )

    # 2. TRIANGLE (COHERENT)
    triangle = GlyphFragment(
        nodes=[0,1,2],
        edges=[(0,1),(1,2),(2,0)]
    )

    # 3. STAR (CONFLICT)
    star = GlyphFragment(
        nodes=[0,1,2,3],
        edges=[(0,1),(0,2),(0,3)]
    )

    print("Line:", validate(line))         # QE
    print("Triangle:", validate(triangle)) # COHERENT_REGION
    print("Star:", validate(star))         # CONFLICT_REGION
