# Candidate adoption transaction

Classification: `TRANSACTION_SEMANTICS_SOUND` / terminal shorthand `sound`.

The validator does not require the candidate SHA to be the live canonical PRE-MAIN SHA before adoption. Candidate code can evaluate a packet whose receipt/update/work-return heads name the current canonical PRE-MAIN head, while separately identifying the exact candidate result for adoption. The reintegration act can then advance PRE-MAIN, after which later packets must use the new head.

Therefore the live-head model is not circular. This holding does **not** cure the separate governance-self-modification problem: the candidate enforcement code is participating in judgment of the governance machinery that introduces it.