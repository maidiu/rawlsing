# LiTS retained I03 fact-preimage closure

## Preserved source-backed blocker

The local pre-candidate court at
`fe1d6ef246d9b796635f2cb87c4a712de47b9d6c` passed runtime, both source SHA
gates, WVS standardization, LiTS C11 replay, and the complete candidate-neutral
I05 frontier.  It then stopped during constituent-I03 packaging with:

`CarrierExecutionBindingError: query_ref exact preimage unavailable; no latest/default/fuzzy/hash-inversion fallback`

No A/B/C process or measured P2X cell was started.

## Exact cause and repair

I05 compiles exact derived query objects from frozen templates and predicates,
executes them, and retains their exact fact refs in its receipts.  The fan-in
then attempted to rerun those derived query refs through the static template
catalog.  That catalog lawfully contains template preimages, not every derived
query preimage, so exact resolution had to fail.

Code head `f6914345c9856acefba9879ff325c12ab6040b5c` retains the canonical exact
EmpiricalFact preimages produced during I05 beside their already-existing refs.
The constituent fan-in now verifies:

- retained preimages close exactly over the global I05 fact-ref set;
- each receipt's sorted fact states match the retained exact objects;
- every candidate fact set matches its receipt refs;
- per-query-role retained fact refs close exactly over that candidate fact set;
- the global constituent manifest closes exactly over the I05 result.

No catalog fallback, latest/default lookup, fuzzy lookup, hash inversion, or
query reconstruction is introduced.  Missing, conflicting, or malformed
preimages fail closed.

## Source-free qualification

Qualification closure head: `d578d19be7d58eb1866778bf5f42b0e1cfcf5fb6`.

- `187 passed, 28 subtests passed in 25.55s`
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`

The qualification was source-free and performed no oracle construction, T3
freeze, A/B/C work, or measured P2X.  A fresh local source-backed pre-candidate
court remains required.
