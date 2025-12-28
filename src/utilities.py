
def tokenize(sentence):
    return sentence.lower().split()

def get_category(word, lexicon):
    return lexicon.get(word, [])