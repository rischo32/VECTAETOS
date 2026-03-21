import subprocess
import hashlib
import random

from infrastructure.projection_adapter_v2 import generate_projection_bundle


def get_git_hash():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip()


def seed_from_hash(commit_hash):
    return int(hashlib.sha256(commit_hash.encode()).hexdigest(), 16) % (10**8)


def generate_glyph_line():
    commit = get_git_hash()
    seed = seed_from_hash(commit)

    random.seed(seed)

    # minimal "query" — neinterpretujeme nič
    query = commit[:12]

    bundle = generate_projection_bundle(query)

    glyphs = bundle["glyphs"]

    # zložíme sekvenciu
    sequence = " | ".join(glyphs.values())

    return sequence


if __name__ == "__main__":
    print(generate_glyph_line())
