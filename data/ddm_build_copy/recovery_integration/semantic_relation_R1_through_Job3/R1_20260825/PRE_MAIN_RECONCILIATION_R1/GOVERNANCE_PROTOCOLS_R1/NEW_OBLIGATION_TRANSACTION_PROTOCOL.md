# NEW OBLIGATION TRANSACTION PROTOCOL R1

`new_obligations` is fail-closed and pre-registration based.

A work return that discovers a new obligation may report the discovery locally, but an adoptive/reintegration packet cannot claim `NEW_OBLIGATIONS_REGISTERED` until the new ID has been added to the candidate central `OPEN_OBLIGATIONS.tsv` state by a grounded central-state update. The validation/adoption packet is then evaluated against that candidate state.

Therefore:

DISCOVERY != REGISTERED
LOCAL RETURN != ADOPTION
NEW OBLIGATION ABSENCE != CLOSURE

The machine intentionally prefers an overstrict two-step transaction to silent loss. There is no automatic creation of central obligations from free-text worker returns.
