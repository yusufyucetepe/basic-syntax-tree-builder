# ---------- X-BAR TEMPLATE ----------
# Every phrase category shares one skeleton (head-initial, left-adjunction):
#   XP → (Spec) X'
#   X' → Adjunct X'  |  X0 (Complement)
# Each category below is a config for that template; build_xbar_rules()
# expands the configs into the phrase-structure rules the parser consumes.
CATEGORY_SCHEMA = {
    "N":   {"spec": "D",  "adjunct": "AdjP", "complement": None},
    "V":   {"spec": None, "adjunct": "AdvP", "complement": "NP"},
    "Adj": {"spec": None, "adjunct": None,   "complement": None},
    "Adv": {"spec": None, "adjunct": None,   "complement": None},
}

def build_xbar_rules(schema):
    rules = {}
    for cat, cfg in schema.items():
        xp = f"{cat}P"
        xbar = f"{cat}'"

        # XP → Spec X'  |  X'
        rules[xp] = ([[cfg["spec"], xbar]] if cfg["spec"] else []) + [[xbar]]

        # X' → X0 Complement  |  X0  |  Adjunct X'
        # Production order matters: the parser is first-match, so the
        # complement variant must come before the bare head.
        rules[xbar] = (
            ([[cat, cfg["complement"]]] if cfg["complement"] else [])
            + [[cat]]
            + ([[cfg["adjunct"], xbar]] if cfg["adjunct"] else [])
        )
    return rules

# Note: the old hand-written grammar also had a ["V", "NP", "V'"] rule under
# V' (ditransitive-shaped). It never fit the X-bar template and was unreachable
# with the current lexicon, so it is dropped here. If a ditransitive verb is
# ever added to the lexicon, extend the schema deliberately instead.
GRAMMAR = {"S": [["NP", "VP"]], **build_xbar_rules(CATEGORY_SCHEMA)}
