# VOZHD CHETIRI — MEASUREMENT & BAKEOFF LAW

Short tag: `VC4-COMPILER/PERSISTENCE`

Status: `PLANNED_COURT_LAW__NO_EXECUTION_AUTHORITY_YET`

## 0. PURPOSE

C09 may execute only after C01–C08 have frozen the logical workload and persistence/replay requirements. This prevents benchmark design from deciding architecture by convenience.

## 1. CANDIDATES

A — `PERSISTENT_CANONICAL_EVENT_CARRIER`

Use the exact accepted/frozen compact persistent implementation available when C09 is authorized. Do not benchmark the failed JSON-per-cell V1 as if it represented the repaired family.

B — `SOURCE_BACKED_VIRTUAL_C11`

Authoritative persistent empirical payload is the exact source artifact plus governed authority/receipts. No full transformed empirical payload is retained after court cleanup.

C — `SOURCE_BACKED_HYBRID`

Same authority floor as B, but bounded/transient or explicitly regenerable accelerators are allowed if listed before execution.

## 2. FAIRNESS LAW

All candidates must satisfy the same logical requests and produce the same semantic outputs/receipts where the frozen architecture defines them.

Forbidden benchmark bias:

- giving A prebuilt warm state while charging B/C for source certification unless warm/cold scenarios are measured separately;
- omitting build cost for one candidate;
- omitting cache-generation cost for C;
- counting source bytes against B/C but not A when A also requires source retention under source constitution;
- counting temporary scratch as permanent state;
- ignoring persistent cache bytes in C;
- accepting approximate/aggregated result parity;
- narrowing I05 workload to known cached predicates;
- selecting only WVS-friendly primitives;
- hiding decoder incompatibility setup cost;
- hiding cleanup/recovery cost.

## 3. PERSISTENT SIZE ACCOUNTING

Report separately:

- `SOURCE_AUTHORITATIVE_BYTES`
- `SEMANTIC_AUTHORITY_BYTES`
- `PROVENANCE_RECEIPT_BYTES`
- `COMPILED_STRUCTURAL_PRODUCT_BYTES` if the court produces a fixture product
- `PERSISTENT_CANONICAL_EMPIRICAL_BYTES`
- `PERSISTENT_REGENERABLE_CACHE_BYTES`
- `TOTAL_REQUIRED_PERMANENT_BYTES`
- `TOTAL_OPTIONAL_CACHE_BYTES`

Source bytes are common authoritative inputs where all architectures remain source-replayable; do not make them disappear from A's lifecycle merely because A also stores transformed data.

## 4. TRANSIENT RESOURCE ACCOUNTING

Report separately:

- peak RSS;
- peak scratch bytes;
- peak temp-file count;
- max single temp object;
- decoded frame size where full-frame reader path is unavoidable;
- cleanup bytes removed;
- residual scratch after success/failure.

## 5. TIME ACCOUNTING

At minimum:

- source verification/open;
- first compilation/setup;
- repeated compilation/setup;
- exact primitive query latency cold;
- exact primitive query latency warm;
- representative I05 batch wall time;
- audit/replay time;
- cache rebuild time;
- delete-all-caches recovery time;
- interrupted-build recovery overhead where measurable.

## 6. REQUIRED WORKLOAD SUITE

The exact suite is frozen by C04/C05, but must contain at least:

1. metadata/source identity verification;
2. governed reconstruction of hostile physical cells/events;
3. full sequential scan primitive;
4. one-variable distribution;
5. 2-way respondent conjunction;
6. 3-way respondent conjunction;
7. 5-way respondent conjunction;
8. conditional distribution;
9. subgroup/risk-set-correct operation;
10. weighted/design operation where exact proving authority exists;
11. typed-negative/refutation-domain case;
12. topology-general case;
13. representative bounded I05 discovery batch;
14. provenance/receipt emission;
15. full semantic/replay audit primitive;
16. fresh-process repeat;
17. delete-all-caches rebuild.

## 7. PROVING SOURCES

Required baseline:

- WVS7 exact SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- LiTS I exact SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

A third source may be added only when C03/C10 identifies a named property not exercised by WVS7/LiTS and HQ authorizes the additional source probe.

## 8. PARITY BEFORE PERFORMANCE

For each candidate require, where applicable:

- source identity parity;
- physical preservation parity;
- C11 observable parity;
- ExactRef/content-hash parity;
- topology/order parity;
- routing/risk-set parity;
- weight/design parity;
- I03 semantic parity;
- I05 frontier/result parity;
- I04 fixture admission parity if exercised;
- deterministic replay parity;
- integrity/fail-closed parity;
- no legacy fallback.

Any failed required parity excludes a candidate from performance selection.

## 9. PRIMARY DECISION METRICS

C09 SHALL publish at least:

`PERSISTENT_REQUIRED_BYTES`

`PERSISTENT_OPTIONAL_CACHE_BYTES`

`PEAK_TRANSIENT_BYTES`

`PEAK_RSS`

`FIRST_BUILD_SECONDS`

`REPEAT_BUILD_SECONDS`

`I03_WORKLOAD_SECONDS`

`I05_BATCH_SECONDS`

`AUDIT_REPLAY_SECONDS`

`CACHELESS_REBUILD_SECONDS`

`MOVING_PART_COUNT`

`FAILURE_RECOVERY_DISPOSITION`

`PERSISTENT_BYTES_REMOVABLE_WITH_ZERO_INFORMATION_LOSS`

## 10. NO SINGLE-SCORE MAGIC

C09 may not invent an opaque weighted score.

Report a Pareto comparison under the campaign's lexicographic laws.

A candidate is dominated if another candidate:

- passes all the same correctness/capability gates;
- is no worse on every governing objective relevant to the stage;
- and is materially better on at least one.

Where tradeoffs remain, C09 returns the tradeoff to HQ rather than hiding it in a score.

## 11. REQUIRED CLEANUP PROOF

For B/C:

- delete all transformed empirical scratch/cache designated disposable;
- prove no authoritative information was lost;
- re-open from source + authority;
- reproduce selected semantic/replay outputs.

For A:

- identify whether deletion of the persistent canonical event carrier causes information loss or only forces reconstruction;
- if reconstruction is possible, state exactly why the carrier nevertheless qualifies as mandatory persistent product rather than optional cache.

## 12. C09 ALLOWED DISPOSITIONS

- `C09_PARITY_PASS__A_PARETO_LEADER`
- `C09_PARITY_PASS__B_PARETO_LEADER`
- `C09_PARITY_PASS__C_PARETO_LEADER`
- `C09_PARITY_PASS__NONDOMINATED_TRADEOFF__HQ_REQUIRED`
- `C09_BLOCK__PARITY_FAILURE`
- `C09_BLOCK__RESOURCE_FAILURE`
- `C09_BLOCK__INCOMPARABLE_OR_UNFROZEN_WORKLOAD`
- `C09_BLOCK__TRUSTWORTHY_SOURCE_OR_ENVIRONMENT_UNAVAILABLE`

Any leader remains provisional until C10 hostile court and HQ synthesis.