from src.grammar import GRAMMAR
from src.lexicon import LEXICON
from src.utilities import get_category

class SyntaxNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

def parse(tokens, lexicon, grammar, start_symbol="S"):
    def expand(node_label, remaining_tokens):
        if node_label not in grammar:
            # Terminal node: match word
            if remaining_tokens and node_label in get_category(remaining_tokens[0], lexicon):
                return SyntaxNode(node_label, [SyntaxNode(remaining_tokens[0])]), remaining_tokens[1:]
            else:
                return None, remaining_tokens
        elif node_label in grammar:
            # Nonterminal: try each production rule
            for production in grammar[node_label]:
                if production == []:
                    return {
                        "label": node_label,
                        "children": []
                    }, remaining_tokens
                current_tokens = remaining_tokens
                children = []
                success = True
                for part in production:
                    child, current_tokens = expand(part, current_tokens)
                    if child is None:
                        success = False
                        break
                    children.append(child)
                if success:
                    return SyntaxNode(node_label, children), current_tokens
            return None, remaining_tokens
        return None, remaining_tokens

    tree, _ = expand(start_symbol, tokens)
    return tree