from anytree import Node, RenderTree

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
    # Specifier: visiually printed as: '∅' when empty
    base_label = label.rstrip("'") if isinstance(label, str) else ''
    if isinstance(base_label, str) and base_label.endswith('P'):
        has_D = any(getattr(c, 'name', '') == 'D' for c in nd.children)
        if not (base_label == 'NP' and has_D):
            if not any(getattr(c, 'name', '') == '∅' for c in nd.children):
                Node('∅', parent=nd)
    return nd

def render_anytree(node):
    root = build_anytree(node)
    for pre, _, nd in RenderTree(root):
        print(pre + nd.name)
    return root