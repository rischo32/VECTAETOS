# =========================================
# VECTAETOS :: EPISTEMIC MERKLE TREE
# Version: 1.0.1 (compat fix)
# =========================================

import hashlib
from typing import List


# =========================================
# HASH FUNKCIA
# =========================================

def hash_pair(left: str, right: str) -> str:
    combined = left + right
    return hashlib.sha256(combined.encode()).hexdigest()


# =========================================
# MERKLE TREE
# =========================================

class EpistemicMerkleTree:
    def __init__(self, leaves: List[str]):
        self.leaves = leaves
        self.levels = []

        if leaves:
            self.build_tree()

    def build_tree(self):
        current_level = self.leaves[:]
        self.levels.append(current_level)

        while len(current_level) > 1:
            next_level = []

            for i in range(0, len(current_level), 2):

                left = current_level[i]

                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left

                parent = hash_pair(left, right)
                next_level.append(parent)

            self.levels.append(next_level)
            current_level = next_level

    def root(self) -> str:
        if not self.levels:
            return ""
        return self.levels[-1][0]

    def get_levels(self) -> List[List[str]]:
        return self.levels


# =========================================
# LEDGER (APPEND)
# =========================================

class EpistemicMerkleLedger:
    def __init__(self):
        self.hashes: List[str] = []

    def append(self, h: str):
        self.hashes.append(h)

    # 🔥 NOVÉ: kompatibilita s metrics
    def add_leaf(self, data: str):
        """
        umožní priamo pridať raw dáta (nie hash)
        """
        h = hashlib.sha256(data.encode()).hexdigest()
        self.append(h)

    def build_tree(self) -> EpistemicMerkleTree:
        return EpistemicMerkleTree(self.hashes)

    def root(self) -> str:
        tree = self.build_tree()
        return tree.root()

    # 🔥 KRITICKÝ FIX
    def get_root(self) -> str:
        return self.root()


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    hashes = [
        "a1"*32,
        "b2"*32,
        "c3"*32,
        "d4"*32
    ]

    ledger = EpistemicMerkleLedger()

    for h in hashes:
        ledger.append(h)

    tree = ledger.build_tree()

    print("Merkle Root:", tree.root())

    print("\nLevels:")
    for level in tree.get_levels():
        print(level)
