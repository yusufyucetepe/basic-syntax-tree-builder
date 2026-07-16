from src.parser import parse
from src.renderer import render_anytree
from src.svg_renderer import render_svg
from src.utilities import tokenize
from src.grammar import GRAMMAR
from src.lexicon import LEXICON

if __name__ == "__main__":
    for word in LEXICON.keys():
        print(word)
    sentence = input("\nEnter a sentence with supported dictionary: ")
    tokens = tokenize(sentence)

    for word in tokens:
        if word not in LEXICON:
            print(f"\n✗ Error: '{word}' is not in the dictionary.\n")
            exit()

    tree = parse(tokens, LEXICON, GRAMMAR)

    if tree:
        render_anytree(tree)
        svg_path = render_svg(tree)
        print(f"\n✓ Syntax Tree Generated. Diagram saved to {svg_path}\n")
    else:
        print("\n✗ Syntax Error: sentence does not match the grammar.\n")
        print("Hint: Try a different phrasing or consult the supported grammar.\n")
