def generate_svg(report, glyphs, diagnostics):
    """
    SVG projekcia Φ pre README
    """

    singularity = report.get("singularity", 0)
    entropy = report.get("entropy", 0.0)
    qe = report.get("qe", False)

    # 8 singularít (vizuál)
    nodes = ""
    for i in range(8):
        color = "#ff4444" if i == singularity else "#888"
        nodes += f'<circle cx="{50+i*40}" cy="60" r="12" fill="{color}" />\n'
        nodes += f'<text x="{50+i*40}" y="90" fill="#aaa" font-size="10" text-anchor="middle">Σ{i}</text>\n'

    # glyph string
    glyph_line = " ".join(glyphs.values())

    # diagnostika (len critical/high)
    issues = []
    for p in diagnostics.get("problems", [])[:5]:
        issues.append(f"{p.type}:{p.metric}")

    issues_text = " | ".join(issues) if issues else "OK"

    svg = f"""
<svg width="420" height="200" xmlns="http://www.w3.org/2000/svg">

<style>
text {{ font-family: monospace; }}
</style>

<!-- singularities -->
{nodes}

<!-- glyph -->
<text x="20" y="120" fill="#fff">glyph: {glyph_line}</text>

<!-- entropy -->
<text x="20" y="140" fill="#aaa">entropy: {entropy:.3f}</text>

<!-- QE -->
<text x="200" y="140" fill="#aaa">QE: {"YES" if qe else "NO"}</text>

<!-- diagnostics -->
<text x="20" y="170" fill="#ff8888">diag: {issues_text}</text>

</svg>
"""
    return svg
