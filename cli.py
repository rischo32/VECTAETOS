#!/usr/bin/env python3
import json
import sys

from ek_core.hash import structural_hash

def main():
    if len(sys.argv) < 2:
        print("Usage: vectaetos <file.json>")
        return

    path = sys.argv[1]

    with open(path, "r") as f:
        data = json.load(f)

    # jednoduchý flatten → Δ (zatím basic)
    delta = {
        (i, i+1, i+2): float(len(str(v)))
        for i, v in enumerate(data.values())
    }

    h = structural_hash(delta)

    print(json.dumps({
        "hash": h,
        "stable": True
    }, indent=2))


if __name__ == "__main__":
    main()
