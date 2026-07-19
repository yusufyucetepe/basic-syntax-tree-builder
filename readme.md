# X-Bar Syntax Tree Builder
X-Bar Syntax Tree Builder parses English sentences and draws their syntax trees the way a syntax textbook would — as X-bar structures with specifiers, complements, and adjuncts. It is written in pure Python with no external dependencies: type a sentence, and the program prints the tree in the terminal and saves a publication-style SVG diagram of it.

Under the hood, the grammar is not a hand-listed set of phrase-structure rules. Instead, every category (N, V, P, Adj, Adv) is a configuration of one shared X-bar template — XP → (Specifier) X′, X′ → Adjunct X′ | X (Complement) — and the concrete rules the parser consumes are generated from that schema. This mirrors the central claim of X-bar theory: all phrases, regardless of category, share the same internal skeleton. A recursive-descent parser matches sentences against the generated rules using a curated lexicon, and two renderers (plain text and SVG) turn the resulting tree into diagrams.

The project exists to show how ideas from theoretical syntax translate directly into executable code: the grammar module reads like the theory, and the trees it produces read like the textbook.

# Examples
**"the small cat chased the dog"** — a transitive verb with its NP complement; the adjective left-adjoins to N':

![Syntax tree for "the small cat chased the dog"](examples/tree_transitive.svg)

**"every clever child arrived on the mountain"** — an intransitive verb with a post-verbal PP right-adjoined to V':

![Syntax tree for "every clever child arrived on the mountain"](examples/tree_postverbal.svg)

**"the small dog behind the ancient castle slowly chased my curious cat"** — a pre-verbal adverb left-adjoined to V'; the PP nests inside the subject NP:

![Syntax tree for "the small dog behind the ancient castle slowly chased my curious cat"](examples/tree_preverbal.svg)

# Features
- Right-branching recursion (e.g. stacked PPs: "in the castle on the mountain")
- English phrase-structure grammar covering NP, VP, PP, AdvP, AdjP, and determiners
- Post-verbal modifiers: PPs and adverbs after the verb (e.g. "my curious cat slept beside the river quietly")
- Text-based syntax tree rendering
- SVG tree diagram output (saved as tree.svg, no extra dependencies)
- Grammar rules generated from a single X-bar category schema

# How to Run
From the project root directory:
python main.py

# Motivation
This project was created to combine Python programming with linguistic theory, particularly syntax and phrase structure, and to make the machinery of X-bar theory something you can run, inspect, and extend.