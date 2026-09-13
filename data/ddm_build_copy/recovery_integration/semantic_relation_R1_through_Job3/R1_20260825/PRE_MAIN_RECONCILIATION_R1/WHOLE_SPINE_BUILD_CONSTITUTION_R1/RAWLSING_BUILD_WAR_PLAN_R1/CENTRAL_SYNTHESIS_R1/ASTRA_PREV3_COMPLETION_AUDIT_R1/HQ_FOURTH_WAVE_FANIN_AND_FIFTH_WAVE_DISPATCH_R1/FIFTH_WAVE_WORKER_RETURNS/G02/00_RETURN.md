# W5-G02 — learned-world real execution R2 — governed return

Status: `PASS__FULL_FROZEN_50_CANDIDATE_77_QUERY_ROLE_LITS1_WORKLOAD_EXECUTED_AND_DETERMINISTICALLY_REPLAYED`

Exact grain:
`PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_REAL_EXECUTION_AND_REPLAY_R2_ONLY`

Branch:
`agent/rabochii-prev3-w5-g02-learned-real-execution-r2`

Commission tip:
`4aa2a75326b150a8c47202f21a62a8933ea473cf`

## Holding

G02 executed the F02-resealed D02 learned-world frontier against the exact LiTS-I carrier and completed the whole frozen workload without frontier mutation, pruning, ranking, selector substitution after execution start, or semantic promotion.

Source identity:
- Library file id: `file_0000000036dc81f8b8b546e356590a03`
- carrier: `LITS-2006-data.dta`
- bytes: `139531180`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows / variables: `29002 / 1198`

Inherited exact authority:
- D02 authority commit: `40cb8585f076a66d9884b99022a59bb909606c03`
- D02 frozen-frontier Git blob: `5399a3f64642c8d9f8a0644db0adc15d38642971`
- F02 adopted return commit: `482bb884a99e31ba77e904d0df39fffc872cbed3`
- F02 C11 release hash: `bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`
- F02 selector replay hash: `89bb3e9140ae0e0fcc9a3e205fd6b60ae721153d88a4730dd66f4fc16e238b1f`
- F02 frontier-readoption hash: `07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851`

The entire candidate/role membership was compiled and sealed before source-data access. Preexecution frontier-seal hash:
`ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`

## Exact execution accounting

- candidates: `50 / 50` terminal
- query roles: `77 / 77` executed
- terminal candidates: `49 EVALUATED_SUPPORTED`, `1 EVALUATED_VALID_EMPTY`
- required P0 positive controls: `5 / 5 EVALUATED_SUPPORTED`
- P1 joint dependence: `1 / 1 EVALUATED_SUPPORTED`
- P2 K=3 conditioned frontier: `18 / 18 EVALUATED_SUPPORTED`
- P3 conditional-reversal lane: `1 / 1 EVALUATED_VALID_EMPTY`
- P4 complete 5x5 joint-cell reachability: `25 / 25 EVALUATED_SUPPORTED`

The P3 terminal valid-empty is a substantive lawful outcome, not a blocker and not a failed execution. For target q301_7 native cell 5, the pooled sign is `+1` and all three q310 stratum signs are `[+1,+1,+1]`; therefore the exact frozen `CONDITIONAL_REVERSAL` validator is false rather than supported. No frontier or validator was changed in response.

## F02 selector-source replay

The source scan reproduced F02 exactly before the learned result was accepted:

- q310 counts: `1=12340, 2=7511, 3=9085, MISSING=66`
- q310 row root: `a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`
- q311 counts: `1=16582, 2=4548, 3=7826, MISSING=46`
- q311 row root: `af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`

All six exact F02 selector-membership roots reproduced. The carrier was used only to replay accepted logical-release members; no new source semantics were minted.

## Deterministic replay

Two fresh-process full executions were byte-identical.

- semantic replay hash: `f90eebe66d5ce1c13004a82dd0aed9e5c3f8d016a6788e8922bc636c8f946771`
- run 1 output SHA-256: `8669bfc3052ad7d65970f125d25e1e0fe775f33c0291b7c6b5b0dfca2933ae85`
- run 2 output SHA-256: `8669bfc3052ad7d65970f125d25e1e0fe775f33c0291b7c6b5b0dfca2933ae85`

## Hard stop line preserved

All of the following execution counters are exactly zero:

- post-data frontier mutation
- pruning
- ranking/top-k
- selector substitution after execution start
- structural admission
- causal promotion
- population generalization
- person-state construction
- V3-state construction

Negative ceiling remains:
`PREV3_LEARNED_EMPIRICAL_ONLY__NO_STRUCTURAL_ADMISSION__NO_CAUSAL_PROMOTION__NO_POPULATION_GENERALIZATION__NO_PERSON_STATE__NO_V3`

## Implementation and qualification

Implementation:
- path: `rawlsing_next/prev3_learned_real_execution_r2.py`
- commit: `1e625fe587089f9467abc2197bbf46799137b977`
- Git blob: `7a9b8b53e36041b453eb62e7a22a52ff0d392c16`

Tests:
- path: `rawlsing_next/tests/test_prev3_learned_real_execution_r2.py`
- semantic-candidate commit: `7f5d1e371f79d3b1340fdbcb41efb2c4e0686beb`
- Git blob: `129e350915ba3401690eccdfadf6b9acf779bee4`
- local bounded suite: `11 passed`

Governed bounded court:
- run: `34781554096`
- job: `103789381614`
- result: `PASS`
- evidence execution SHA: `d3ec66ede469a3e6f4b3aacab8b9444716ec5cf3`
- Python: `3.12.14` / CPython
- determinism mode: `EXACT`
- exit code: `0`
- artifact id: `10324354888`
- artifact: `rabochii-court-receipt-34781554096`
- artifact digest: `sha256:4b86f6e36fa6a1a9c4d5a6477b76b8eb72c2705f4841626ccd45050944a554fb`

Temporary PR `#362` was used only to trigger the court and was closed unmerged. Temporary `.rabochii/court_spec.json` was removed at `0a24c97e0c06b141452bd18b78a10f32904ce7b3`.

## Governed artifacts

- `01_PREEXECUTION_FRONTIER_SEAL.json`
- `02_F02_SELECTOR_SOURCE_REPLAY_RECEIPT.json`
- `03_TERMINAL_50_CANDIDATE_LEDGER.json`
- `04_77_QUERY_ROLE_EXECUTION_MANIFEST.json`
- `05_DETERMINISTIC_FRESH_PROCESS_REPLAY_RECEIPT.json`
- `06_TEST_AND_GOVERNED_COURT_RECEIPT.json`

## Disposition

G02 owns no structural admission and performs no self-promotion. Return this PASS to HQ for fifth-wave fan-in. PRE-V3 remains objective-world only.

Terminal:
`G02_PASS__F02_RESEALED_LITS1_LEARNED_WORLD_50_OF_50_CANDIDATES_AND_77_OF_77_QUERY_ROLES_EXECUTED__P0_5_OF_5_POSITIVE__49_SUPPORTED_PLUS_1_LAWFUL_VALID_EMPTY__TWO_FRESH_PROCESSES_BYTE_IDENTICAL__NO_POST_DATA_FRONTIER_MUTATION__RETURN_TO_HQ`
