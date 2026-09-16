# EE-W5 — NAMED UNIVERSE / SOURCE-CELL READINESS MATRIX R1

Status: `COMMISSIONED`

Repository: `maidiu/rawlsing`

Exact branch: `agent/rabochii-prev3-ee-w5-universe-cell-readiness-r1`

Commission base: `40a79b595270a9a3bbec019ed1ef1867ccd505f5`

## Role

You are **NAMED UNIVERSE / SOURCE-CELL READINESS / EE-W5**.

Your job is to freeze the candidate-neutral named-source cells that can lawfully enter the final A/B/C comparison and identify exactly which workload families each source/universe is eligible to exercise.

This is an authority/readiness lane, not a benchmark lane and not a source-pooling lane.

## Canonical start

Read current `HQ_HANDOFF/LATEST.json` and its checkpoint, then read:

- `.../PREV3_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1/01_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1.md`;
- `02_ABC_COMPARISON_AND_CLOSURE_SEQUENCE.md`;
- `04_REQUIREMENT_MATRIX.json`;
- current empirical comparability authority;
- current source-universe composition authority;
- accepted WVS7 documentary/source authority;
- accepted LiTS-I source authority;
- D17 exact-source preflight return;
- D02-R2 runtime return;
- existing C09/HB05 parity/input manifests.

## Exact grain

`FREEZE_EXACT_NAMED_EMPIRICAL_UNIVERSE_CELLS_AND_WORKLOAD_ELIGIBILITY_FOR_FINAL_ABC_COMPARISON_ONLY`

## Source identities already known and to be verified

At minimum account for:

### WVS7

- exact authoritative payload: `WVS Wave 7.sav`
- bytes: `185163494`
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

### LiTS-I

- exact authoritative payload: `LITS-2006-data.dta`
- bytes: `139531180`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Do not infer that these two sources are semantically poolable merely because both can enter one comparison harness.

## Required output

For each exact eligible empirical universe/cell, freeze:

- universe ID;
- source family;
- source payload/hash;
- wave/release/time scope;
- country/society/shard scope where applicable;
- target population/sample-frame authority status;
- routing/risk-set authority status;
- respondent namespace / same-respondent capability;
- design/weight/estimand authority relevant to each workload family;
- source-semantic authority relevant to each workload family;
- exact query/frontier authority available;
- exact learned-product/validation authority available;
- exact comparison metrics that are lawful;
- workload families for which the cell is `ELIGIBLE`;
- workload families for which it is `MISSING_AUTHORITY`;
- workload families for which it is `NONCOMPARABLE_FOR_THIS_METRIC`;
- exact blocker refs for every ineligible state.

## Deliverables

Under `WORKER_RETURNS/EE-W5/` produce:

1. `00_RETURN.md`
2. `01_UNIVERSE_CELL_REGISTRY.json`
3. `02_WORKLOAD_ELIGIBILITY_MATRIX.csv`
4. `03_AUTHORITY_GAP_MATRIX.csv`
5. `04_COMPARABILITY_AND_NONPOOLING_RECEIPT.md`

## Governing law

Use the accepted source-universe rule:

`FAIR_MULTI_UNIVERSE_PARITY = SAME_CANDIDATES × SAME_ELIGIBLE_UNIVERSE_CELLS × SAME_OPERATION_LAW × SAME_METRICS`

not:

`POOL_ALL_SOURCES`.

A missing authority cell must not become numeric zero, performance failure, or candidate penalty.

Preserve:

`COMMON_QUERY_INTERFACE != POOLED_EMPIRICAL_UNIVERSE`

`COMPARABLE_FOR_RUNTIME != COMPARABLE_FOR_SUBSTANTIVE_ESTIMATE`

`SAME_LABEL_OR_CODE != SEMANTIC_EQUIVALENCE`

## Scope

No Library materialization is required unless an exact repository authority explicitly makes byte-level re-verification necessary. Default permission is `NO`; use existing accepted source-identity receipts.

No A/B/C execution.
No architecture ranking.
No new harmonization.
No cross-source scale/value portability.
No Field Forge/Dva/V3 semantics.
No MAIN or semantic PRE-MAIN mutation.

PASS means EE-W1/EE-W4 can consume one exact source-cell registry without having to rediscover source eligibility or invent pooling/comparability rules.

Commit the governed return and report final branch tip.