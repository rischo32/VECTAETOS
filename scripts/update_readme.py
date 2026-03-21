from pathlib import Path
from scripts.glyph_generator import generate_glyph_line


README = Path("README.md")


def update():
    content = README.read_text()

    glyph_line = generate_glyph_line()

    new_block = f"<!-- GLYPH_SEQUENCE_START -->\n{glyph_line}\n<!-- GLYPH_SEQUENCE_END -->"

    import re

    content = re.sub(
        r"<!-- GLYPH_SEQUENCE_START -->.*<!-- GLYPH_SEQUENCE_END -->",
        new_block,
        content,
        flags=re.DOTALL
    )

    README.write_text(content)


if __name__ == "__main__":
    update()
