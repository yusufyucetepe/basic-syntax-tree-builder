# ---------- X-BAR TEMPLATE ----------
# Every phrase category shares one skeleton (head-initial):
#   XP → (Spec) X'
#   X' → Adjunct X'  |  X0 (Complement) (RAdjunct)
# "adjunct" is a pre-head (left-adjoined) modifier; "radjunct" is a post-head
# modifier. Textbook X-bar writes right adjunction as X' → X' RAdjunct, but
# that rule is left-recursive and would loop the recursive-descent parser
# forever, so it is flattened onto the head production instead (one radjunct
# per bar level; stacked PPs still nest via the NP inside the PP).
# "comp_required" marks heads whose complement is obligatory (P: *"sat on")
# — the bare-head X' → X0 variant is not emitted for those. Verbs keep it
# because the complement is optional (intransitive "sat").
# Each category below is a config for that template; build_xbar_rules()
# expands the configs into the phrase-structure rules the parser consumes.
CATEGORY_SCHEMA = {
    "N":   {"spec": "D",  "adjunct": "AdjP", "complement": None, "radjunct": "PP", "comp_required": False},
    "V":   {"spec": None, "adjunct": "AdvP", "complement": "NP", "radjunct": "PP", "comp_required": False},
    "P":   {"spec": None, "adjunct": None,   "complement": "NP", "radjunct": None, "comp_required": True},
    "Adj": {"spec": None, "adjunct": None,   "complement": None, "radjunct": None, "comp_required": False},
    "Adv": {"spec": None, "adjunct": None,   "complement": None, "radjunct": None, "comp_required": False},
}

def build_xbar_rules(schema):
    rules = {}
    for cat, cfg in schema.items():
        xp = f"{cat}P"
        xbar = f"{cat}'"

        # XP → Spec X'  |  X'
        rules[xp] = ([[cfg["spec"], xbar]] if cfg["spec"] else []) + [[xbar]]

        # X' → X0 Complement RAdjunct  |  X0 Complement  |  X0 RAdjunct
        #    |  X0  |  Adjunct X'
        # Production order matters: the parser is first-match, so longer
        # variants must come before their prefixes (else the short one
        # matches and the trailing material is left unconsumed).
        variants = []
        if cfg["complement"] and cfg["radjunct"]:
            variants.append([cat, cfg["complement"], cfg["radjunct"]])
        if cfg["complement"]:
            variants.append([cat, cfg["complement"]])
        if cfg["radjunct"] and not cfg["comp_required"]:
            variants.append([cat, cfg["radjunct"]])
        if not cfg["comp_required"]:
            variants.append([cat])
        if cfg["adjunct"]:
            variants.append([cfg["adjunct"], xbar])
        rules[xbar] = variants
    return rules

# Note: the old hand-written grammar also had a ["V", "NP", "V'"] rule under
# V' (ditransitive-shaped). It never fit the X-bar template and was unreachable
# with the current lexicon, so it is dropped here. If a ditransitive verb is
# ever added to the lexicon, extend the schema deliberately instead.
GRAMMAR = {"S": [["NP", "VP"]], **build_xbar_rules(CATEGORY_SCHEMA)}
