def glyph_to_svg(glyph: str) -> str:
    """
    Convert glyph string (e.g. △◇◯⌓) into SVG
    """

    shape_map = {
        "◯": '<circle cx="{x}" cy="50" r="15" fill="none" stroke="black"/>',
        "◇": '<rect x="{x_minus}" y="35" width="30" height="30" fill="none" stroke="black" transform="rotate(45 {x} 50)"/>',
        "△": '<polygon points="{x_minus},65 {x},35 {x_plus},65" fill="none" stroke="black"/>',
        "⌓": '<rect x="{x_minus}" y="35" width="30" height="30" fill="black" stroke="black"/>',
    }

    svg_parts = []
    spacing = 60

    for i, char in enumerate(glyph):
        x = 30 + i * spacing
        x_minus = x - 15
        x_plus = x + 15

        template = shape_map.get(char, "")
        svg_parts.append(template.format(x=x, x_minus=x_minus, x_plus=x_plus))

    width = spacing * len(glyph)

    return f'''
<svg width="{width}" height="100" xmlns="http://www.w3.org/2000/svg">
    {"".join(svg_parts)}
</svg>
'''
