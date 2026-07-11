from xml.sax.saxutils import escape

from src.renderer import build_anytree

FONT_SIZE = 16
LEVEL_HEIGHT = 64
CHAR_WIDTH = 9      # approximate glyph width at FONT_SIZE, for layout only
MIN_SLOT = 36       # minimum horizontal space reserved per leaf
PADDING = 24

def _layout(root):
    # Leaves get sequential x slots sized by their label width;
    # each internal node is centered over its first and last child.
    positions = {}
    cursor = [PADDING]

    def place(node, depth):
        if not node.children:
            slot = max(len(node.name) * CHAR_WIDTH, MIN_SLOT)
            x = cursor[0] + slot / 2
            cursor[0] += slot + PADDING
        else:
            xs = [place(child, depth + 1) for child in node.children]
            x = (xs[0] + xs[-1]) / 2
        positions[node] = (x, PADDING + FONT_SIZE + depth * LEVEL_HEIGHT)
        return x

    place(root, 0)
    return positions, cursor[0]

def to_svg(tree):
    root = build_anytree(tree)
    positions, width = _layout(root)
    height = PADDING * 2 + FONT_SIZE + root.height * LEVEL_HEIGHT

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" '
        f'font-family="Georgia, serif" font-size="{FONT_SIZE}" text-anchor="middle">',
        f'<rect width="100%" height="100%" fill="white"/>',
    ]

    for node, (x, y) in positions.items():
        for child in node.children:
            cx, cy = positions[child]
            parts.append(
                f'<line x1="{x:.1f}" y1="{y + 5:.1f}" x2="{cx:.1f}" y2="{cy - FONT_SIZE:.1f}" '
                f'stroke="#333" stroke-width="1"/>'
            )
        # Leaves are the words themselves (or ∅): italic, like textbook trees
        style = ' font-style="italic" fill="#555"' if not node.children else ' fill="#111"'
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}"{style}>{escape(node.name)}</text>')

    parts.append('</svg>')
    return "\n".join(parts)

def render_svg(tree, path="tree.svg"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_svg(tree))
    return path
