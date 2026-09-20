# FIABC-QF1-R1 — Exact Source-Independent Qualification Repair

## Terminal

`FIABC_QF1_R1_EXACT_REPAIR_COMPLETE__COMBINED_SOURCE_INDEPENDENT_QUALIFICATION_PASS__READY_FOR_LOCAL_SOURCE_MATERIALIZATION_GATES`

The four documented QF1 clusters were repaired mechanically and the complete source-independent court now passes. No architecture, authority, semantic, candidate, accounting, or terminal redesign was made.

## Checkout and ancestry

- Repository: `maidiu/rawlsing`
- Starting QF1 commit: `d1a6899e159e68d9fd53abe83658e41c6a32ba59`
- Branch: `agent/rabochii-premain-fiabc-qf1-r1-exact-repair-r1`
- Required HQ implementation ancestry remains preserved through the QF1 parent.
- Four repair commits are listed in `01_REPAIR_LEDGER.csv`.
- Return artifacts are the only changes after the four repair commits.

## Repair result

Exactly four initial rows were frozen from the QF1 artifacts and all four now pass:

1. Live backend literal escaped-newline syntax: repaired with the smallest valid multiline expression.
2. R35-I02 hostile helper dereference: missing receipt identities now pass through to the production verifier, which rejects the malformed bundle.
3. R35-I03 synthetic evidence: binary float literals were replaced with exact `Decimal` values; production float rejection remains unchanged.
4. W3-I06A fixture setup: `_freeze()` now creates the requested temporary root before writing.

Focused reruns pass: W3-I04 6/6, R35-I02 9/9, R35-I03 15/15, and W3-I06A 9/9.

## Full requalification

The complete source-independent court passes under `/usr/local/bin/python3`:

- compileall and all five required JSON validations;
- R35-I01/I02/I03 and R35-Q01 hostile court;
- T6 convergence;
- T2/T3/T4 regression, W3-I06A, telemetry, and lifecycle accounting;
- independent oracle, I07 succession preflight, I08 terminal verifier, and T5 live control;
- PRE553 authority/query/discovery spine;
- inventoried W3-I04 runtime packaging/rebind suite;
- post-repair static identity court.

The commissioned `python` alias is absent in this environment. The exact alias invocations remain recorded as exit 127 observations; equivalent `python3` invocations passed for every required validation and suite. No test was skipped.

## Preservation and source boundary

All unrelated frozen T1–T6 identities remain exact. The live backend blob changed only because the QF1 syntax defect made the accepted implementation unparsable. The three changed test fixtures are recorded with prior/repaired blobs and contract-preservation reasons.

No LiTS-I raw source, WVS7 raw source, CLOSED_35 carrier, SAV bytes, real six-cell execution, WVS oracle materialization, missing LiTS-A first-build receipt, R6X, or measured P2X was run.

The source-independent qualification is complete and the repository is ready for the separately governed local source-materialization gates. This commission did not execute those gates.

