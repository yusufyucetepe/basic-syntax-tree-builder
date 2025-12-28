GRAMMAR = {
    "S": [["NP", "VP"]],

    # ---------- NOUN PHRASE ----------
    "NP": [["D", "N'"], ["N'"]],
    "N'": [["N"],["D'", "NP"]],
    "N'": [["N"], ["AdjP", "N'"]],
    
    # ---------- VERB PHRASE ----------
    "VP": [["V'"]],
    # allow post-verbal adverbs and prefer matching AdvP after V when present
    "V'": [["V", "NP", "V'"], ["V", "NP"], ["V"], ["AdvP", "V'"]],

    # ---------- ADJECTIVE & ADVERB PHRASES ----------
    "AdjP": [["Adj'"]],
    "Adj'": [["Adj"]],
    "AdvP": [["Adv'"]],
    "Adv'": [["Adv"]],
}
