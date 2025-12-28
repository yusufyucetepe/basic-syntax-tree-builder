from src.parser import parse
from src.renderer import render_anytree
from src.utilities import tokenize
from src.grammar import GRAMMAR
from src.lexicon import LEXICON

if __name__ == "__main__":
    for word in LEXICON.keys():
        print(word)
    sentence = input("\nEnter a sentence with supported dictionary: ")
    tokens = tokenize(sentence)
    tree = parse(tokens, LEXICON, GRAMMAR)
    
    for word in tokens:
        if word not in LEXICON:
            print(f"\n✗ Error: '{word}' is not in the dictionary.\n")
            exit()

    if tree:
        render_anytree(tree)
        print("\n✓ Syntax Tree Generated.\n")
    else:
        print("\n✗ Syntax Error: sentence does not match the grammar.\n")