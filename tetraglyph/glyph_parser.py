#!/usr/bin/env python3
# =========================================
# VECTAETOS :: TETRAGLYPH PARSER v1
# =========================================

from typing import List, Dict, Tuple
import json
import hashlib

# =========================================
# DEFINÍCIA SYMBOLov
# =========================================

SYMBOLS = {"⧗","⟡","↺","⊲","⌀","◇","□"}
CONNECTORS = {"─","│","╲","╱"}

# =========================================
# DÁTOVÉ ŠTRUKTÚRY
# =========================================

class Node:
    def __init__(self, id: str, symbol: str, x: int, y: int):
        self.id = id
        self.symbol = symbol
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "pos": (self.x, self.y)
        }

class GlyphFragment:
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: List[Tuple[str,str]] = []

    def to_dict(self):
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": self.edges
        }

# =========================================
# PARSER
# =========================================

class GlyphParser:

    def __init__(self):
        self.node_counter = 0

    def parse(self, ascii_glyph: str) -> GlyphFragment:
        lines = ascii_glyph.split("\n")
        grid = [list(line) for line in lines]

        fragment = GlyphFragment()

        node_map = {}

        # 1️⃣ Detekcia uzlov
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char in SYMBOLS:
                    node_id = f"n{self.node_counter}"
                    self.node_counter += 1

                    node = Node(node_id, char, x, y)
                    fragment.nodes.append(node)
                    node_map[(x,y)] = node

        # 2️⃣ Detekcia spojení
        for (x,y), node in node_map.items():

            # smer → vpravo
            self._scan_direction(grid, node_map, fragment, node, dx=1, dy=0)

            # smer ↓ dole
            self._scan_direction(grid, node_map, fragment, node, dx=0, dy=1)

            # diagonála ↘
            self._scan_direction(grid, node_map, fragment, node, dx=1, dy=1)

            # diagonála ↙
            self._scan_direction(grid, node_map, fragment, node, dx=-1, dy=1)

        return fragment

    def _scan_direction(self, grid, node_map, fragment, node, dx, dy):
        x, y = node.x, node.y

        cx, cy = x + dx, y + dy

        path_valid = False

        while 0 <= cy < len(grid) and 0 <= cx < len(grid[cy]):

            char = grid[cy][cx]

            if char in CONNECTORS:
                path_valid = True
                cx += dx
                cy += dy
                continue

            if (cx,cy) in node_map and path_valid:
                target = node_map[(cx,cy)]
                edge = (node.id, target.id)

                if edge not in fragment.edges and (target.id, node.id) not in fragment.edges:
                    fragment.edges.append(edge)
                return

            break

# =========================================
# HASH
# =========================================

def compute_hash(fragment: GlyphFragment) -> str:
    data = json.dumps(fragment.to_dict(), sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    glyph = """
⧗──⟡──↺
│      │
◇──□──⊲
""".strip("\n")

    parser = GlyphParser()
    fragment = parser.parse(glyph)

    print(json.dumps(fragment.to_dict(), indent=2))
    print("\nHash:", compute_hash(fragment))
