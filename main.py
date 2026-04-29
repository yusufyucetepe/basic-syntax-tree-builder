from src.parser import parse
from src.renderer import render_anytree
from src.utilities import tokenize, get_category
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
        # Detect trailing adverbs — common cause is post-verbal AdvP which current grammar doesn't accept
        trailing_advs = []
        i = len(tokens) - 1

        while i >= 0 and 'Adv' in get_category(tokens[i], LEXICON):
            trailing_advs.insert(0, tokens[i])
            i -= 1
        contains_v_before = any('V' in get_category(t, LEXICON) for t in tokens[:i+1]) if trailing_advs else False

        print("\n✗ Syntax Error: sentence does not match the grammar.\n")

        if trailing_advs and contains_v_before:
            advs_str = ' '.join(trailing_advs)
            print(f"Note: The parser currently does not support adverbial phrases after the VP (post-verbal adverbs) like '{advs_str}'.")
            print("This builder only supports right-side recursion; try placing adverbs before the verb (e.g., 'quickly') or extend the grammar to allow post-verbal AdvP.\n")
        else:
            print("Hint: Try a different phrasing or consult the supported grammar.\n")
