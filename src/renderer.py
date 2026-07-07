from anytree import Node, RenderTree

from src.grammar import CATEGORY_SCHEMA

def _needs_empty_spec(label, children):
    if not isinstance(label, str) or not label.endswith('P'):
        return False
    # label[:-1] maps "NP"→"N", "AdjP"→"Adj", etc. A future category named
    # "P" (whose XP is "PP") would need this lookup revisited.
    cfg = CATEGORY_SCHEMA.get(label[:-1])
    if not cfg or not cfg['spec']:
        return False
    return not any(getattr(c, 'name', '') == cfg['spec'] for c in children)

def _normalize(node):
    if hasattr(node, "label"):
        return node.label, getattr(node, "children", [])
    elif isinstance(node, dict):
        return node.get("label") or node.get("type") or repr(node), node.get("children", [])
    elif isinstance(node, (tuple, list)):
        if node and node[0] == "TOKEN":
            return str(node[1] if len(node) > 1 else node), []
        return (str(node[0]) if node else "[]"), list(node[1:])
    else:
        return str(node), []

def build_anytree(node, parent=None):
    label, children = _normalize(node)
    nd = Node(label) if parent is None else Node(label, parent=parent)
    for c in children:
        build_anytree(c, nd)
    # Specifier: visually printed as '∅' when the category has a spec
    # slot in CATEGORY_SCHEMA but no child fills it
    if _needs_empty_spec(label, nd.children):
        if not any(getattr(c, 'name', '') == '∅' for c in nd.children):
            Node('∅', parent=nd)
    return nd

def render_anytree(node):
    root = build_anytree(node)
    for pre, _, nd in RenderTree(root):
        print(pre + nd.name)
    return root