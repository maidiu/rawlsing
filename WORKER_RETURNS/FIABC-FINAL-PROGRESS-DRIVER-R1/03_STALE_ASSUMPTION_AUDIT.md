# FIABC FINAL PROGRESS DRIVER — stale-assumption audit

## Removed live defects

| Area | Before | After |
|---|---|---|
| backend failure receipt cell order | literal five-cell list ended at `WVS7/B`; `WVS7/C` raised during `order.index` | current validated manifest supplies cell order; WVS7/C is sixth |
| initial prefix | hardcoded LiTS/A S00 + S01 preservation | manifest-derived stages strictly before `first_unfinished`; READY pre-entry stages cannot be synthesized |
| LiTS/A current S01 | stale historical preservation path could suppress current measured S01 | current manifest entry S01 remains executable; only S00 prefix is mechanically bound |
| ledger topology | fixed expected source/candidate order persisted | source/candidate order persisted from loaded manifest |
| common-source propagation | fixed candidate loop and fixed next `/A/S00` | source cells, stage order, next source/cell/stage derive from manifest |
| current cell terminal gate | fixed source/candidate loops + hardcoded S16 address | last governed stage per manifest cell |
| source-oracle load loop | fixed expected source tuple | manifest source order |
| candidate-local finalization | failure could flow to success-only S17 path | fully terminal candidate failures produce clean court candidate-local terminal; S17 success verifier is not run |

## Static scan result

Against current branch production paths:

- exact historical five-cell literal `["LITS_I/A","LITS_I/B","LITS_I/C","WVS7/A","WVS7/B"]`: **absent**
- obsolete symbol `bind_initial_preserved_prefix`: **absent**
- literal progress counts `102` or `89` in driver/backend production code: **absent**
- backend WVS7/C topology special case: **absent**; sequence order is manifest-derived

## Deliberately retained explicit law references

Some explicit WVS7/C references remain in `ee_p2x_darwin_court_driver.py` for two bounded reasons:

1. historical continuation-map validation/preservation, which remains immutable compatibility history; and
2. exact current WVS7/C zero-accelerator cache-law validation.

Those are semantic/law checks, not a five-cell ordering assumption.

The backend's existing LiTS A/B `preserved` accounting distinctions were not generalized in this lane because the commission explicitly forbids changing telemetry semantics/completeness law owned by other workers.

## Current manifest audit

`WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json` was read as committed JSON only. Its topology is:

1. LITS_I/A
2. LITS_I/B
3. LITS_I/C
4. WVS7/A
5. WVS7/B
6. WVS7/C

Its cell stage catalog contains 17 S00–S16 slots; the current entry is LiTS/A S01; adding success-only court S17 yields 102 governed positions from the current entry, of which 89 are READY/executable. Production code derives all of these cardinalities.
