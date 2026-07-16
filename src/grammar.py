from itertools import combinations

# ---------- X-BAR TEMPLATE ----------
# Every phrase category shares one skeleton (head-initial):
#   XP → (Spec) X'
#   X' → Adjunct X'  |  X0 (Complement) (RAdjuncts...)
# "adjunct" is a pre-head (left-adjoined) modifier; "radjuncts" lists the
# post-head modifier categories. Textbook X-bar writes right adjunction as
# X' → X' RAdjunct, but that rule is left-recursive and would loop the
# recursive-descent parser forever, so it is flattened onto the head
# production instead: at most one of each radjunct category per bar level,
# in the listed order only (V takes "on the mat quickly" but not
# "quickly on the mat"; stacked PPs still nest via the NP inside the PP).
# "comp_required" marks heads whose complement is obligatory (P: *"sat on")
# — the bare-head X' → X0 variant is not emitted for those. Verbs keep it
# because the complement is optional (intransitive "sat").
# Each category below is a config for that template; build_xbar_rules()
# expands the configs into the phrase-structure rules the parser consumes.
CATEGORY_SCHEMA = {
    "N":   {"spec": "D",  "adjunct": "AdjP", "complement": None, "radjuncts": ["PP"],         "comp_required": False},
    "V":   {"spec": None, "adjunct": "AdvP", "complement": "NP", "radjuncts": ["PP", "AdvP"], "comp_required": False},
    "P":   {"spec": None, "adjunct": None,   "complement": "NP", "radjuncts": [],             "comp_required": True},
    "Adj": {"spec": None, "adjunct": None,   "complement": None, "radjuncts": [],             "comp_required": False},
    "Adv": {"spec": None, "adjunct": None,   "complement": None, "radjuncts": [],             "comp_required": False},
}

def _radjunct_subsets(radjuncts):
    # All order-preserving subsets of the radjunct list, longest first,
    # ending with the empty subset (no radjunct).
    subsets = []
    for r in range(len(radjuncts), -1, -1):
        subsets.extend(list(combo) for combo in combinations(radjuncts, r))
    return subsets

def build_xbar_rules(schema):
    rules = {}
    for cat, cfg in schema.items():
        xp = f"{cat}P"
        xbar = f"{cat}'"

        # XP → Spec X'  |  X'
        rules[xp] = ([[cfg["spec"], xbar]] if cfg["spec"] else []) + [[xbar]]

        # X' → X0 (Complement) (RAdjuncts...)  |  Adjunct X'
        # expanded into one variant per radjunct subset.
        # Production order matters: the parser is first-match, so longer
        # variants must come before their prefixes (else the short one
        # matches and the trailing material is left unconsumed).
        variants = []
        for subset in _radjunct_subsets(cfg["radjuncts"]):
            if cfg["complement"]:
                variants.append([cat, cfg["complement"], *subset])
        if not cfg["comp_required"]:
            for subset in _radjunct_subsets(cfg["radjuncts"]):
                variants.append([cat, *subset])
        if cfg["adjunct"]:
            variants.append([cfg["adjunct"], xbar])
        rules[xbar] = variants
    return rules

# Note: the old hand-written grammar also had a ["V", "NP", "V'"] rule under
# V' (ditransitive-shaped). It never fit the X-bar template and was unreachable
# with the current lexicon, so it is dropped here. If a ditransitive verb is
# ever added to the lexicon, extend the schema deliberately instead.
GRAMMAR = {"S": [["NP", "VP"]], **build_xbar_rules(CATEGORY_SCHEMA)}
