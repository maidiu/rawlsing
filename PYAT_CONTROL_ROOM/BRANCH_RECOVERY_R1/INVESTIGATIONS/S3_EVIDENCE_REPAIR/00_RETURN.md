# PYAT 845 S3 evidence repair — independent function-row regrade

**Role:** fresh independent I2/I3 source/code/merit regrader; not original S3 author, not original reviewer, original scientific issuer, S6/H1/S7 author or own hostile reviewer.

**Repository:** `maidiu/rawlsing` (private). **Output branch:** `agent/pyat-845-s3-evidence-regrade-20261030-r1`. **Startup/frozen baseline:** `750548ddbb9b4392a16ce93097b856f349e16182`. **Actual PRE-MAIN head at audit close:** `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3`; all 22 S3-relevant paths are unchanged between the two heads. **Original return:** `65b83dee3385fc85d5d283c19acd270dea50a27d`. **Corrected common evidence law:** `f50651a2bb0758e9fe6d6a2852441dcc782344be`.

**Actual executor/capability:** OpenCode / `opencode-go/deepseek-v4.1-flash` (DeepSeek V4.1-Flash). MAX was requested; client effort is not independently observable. No model/harness switch. Isolated S3 worktree created; no existing S3-evidence worktree displaced. S1/S2/S4/S5 worktrees were not modified.

**Write scope:** only `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S3_EVIDENCE_REPAIR/`. No PRE-MAIN, original S3 return, production source, actor/science permission or merge was modified.

## FINDING

### 1. Machine invariants

- `FUNCTION_GRADE_CORRECTIONS.jsonl`: **398** rows, one per immutable original `FUNCTION_COURT.jsonl` row, same order, same `function_id`, unique correction keys; no drops.
- `BRANCH_RECONCILIATION.jsonl`: **174** rows, exact original branch names and tips; no drops; 168 no-code/control/return roles preserved, 111 unknown-review roles preserved.
- `RECEIVER_TEST_AND_SOURCE_PERMISSION_MATRIX.json`: **22** exact source/test paths, current PRE-MAIN blob/path, test/ABI/FF/time/current-use status and required issuer/operation.
- 398 original labels retained; 398 corrected six-axis records; 398 disposition/actions; no READY/SUPERSEDED/REBUILT/TRASH promotion.

### 2. Corrected composite distribution

| Corrected composite | Rows |
|---|---:|
| `NOT_PRODUCT_CODE` | 288 |
| `SOURCEFREE_INTEGRATION_CANDIDATE` | 62 |
| `HISTORICAL_ACCEPTANCE_ONLY` | 21 |
| `INSUFFICIENT_EVIDENCE` | 18 |
| `DEFECTIVE_BLOCK` | 6 |
| `SCIENCE_HOLD` | 3 |

- `UNIQUE_USEFUL_READY` = **0**
- `SUPERSEDED_BETTER` = **0**
- `INDEPENDENTLY_REBUILT_EQUIVALENT` = **0**
- generic `TRASH_WITH_GROUNDS` = **0**; the precise `_auth` defect is `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`.

### 3. Exact source cuts

| Artifact | Exact cut |
|---|---|
| Original S3 return | `65b83dee3385fc85d5d283c19acd270dea50a27d` |
| Corrected evidence law | `f50651a2bb0758e9fe6d6a2852441dcc782344be` |
| PRE-MAIN frozen baseline | `750548ddbb9b4392a16ce93097b856f349e16182` |
| PRE-MAIN actual head at audit close | `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3`; 22/22 relevant paths unchanged |
| Selected-world branch | `agent/reviewer-pyat-r3-hq291-s00v3x-independent-offline-execution-r1` @ `ed34944e253b78714a28d72b8ca2a6521ce15930` |
| Selected-world source | `rawlsing_next/pre553_selected_world_progressive_contract.py` `e9caea543bcc4e1418905f1442d2c7c97eef04b2` |
| Seam source | `rawlsing_next/r3_s02_seam_witness.py` `b1ec1814c4616f61a1e3fc8bbc0b102d690a577f` |
| PE branch | `agent/reviewer-pyat-r3-hq297-k9k10-execution-recovery-r1` @ `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65` |
| PE source | `rawlsing_next/pre553_postastra_pe_generic_world_possibility.py` `58484f4c3d9aae148d4116dcf00420c432aefcbd` |
| V2K branch | `agent/reviewer-pyat-r3-postastra-pv-v2k-independent-r1` @ `694fb45085cd5e4891949921a44edb77c3f603f2` |
| V2K source | `rawlsing_next/pre553_original_identity_v2k_successor_candidate.py` `e3ef9a2469966b8ecfbcd178b971f54c687aef22` |
| E03 exact source | `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` |
| E03 exact test | `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py` `2161c0fff86ecb7a2c9a40b29852075e802841fd` |
| HQ273 branch | `agent/step5-pyat-hq273-c01-source-free-true-conditional-owner-court-r1` @ `2406a4d713bd39f29c48defc983938e3e89a81b0` |
| B2 EE14 branch | `agent/vozhd-pyat-hq280-b2-test-custody-correction-r1` @ `a159bff63b779b994d7b1e83f8a2d6a303b81ea2` |

### 4. Actual sourcefree test receipts (truly run; isolated extracted trees)

| Court | Exact tip | Actual result |
|---|---|---|
| Selected-world contract | `ed34944e...` | **24 passed**, exit 0 |
| Seam witness | `ed34944e...` | **26 passed / 1 failed**, exit 1; failure `test_s00c_change_source_owned_synthetic_numeric_values_changes_result: KeyError exact_probabilities` |
| PE author | `e61a26ce...` | **21 passed**, exit 0 |
| PE independent strict | `e61a26ce...`, exact PE root | **4 passed / 9 failed**, exit 1; includes reverse-scoped issuer forgery failure |
| V2K four suites | `694fb450...` | **collection error**, exit 2; missing `pre553_original_workload_contract_v2_candidate` |
| E03 current | `ed34944e...` | **18 passed**, exit 0 |
| HQ273 C01 | `2406a4d7...` | **19 passed**, exit 0 |
| B2 EE14 | `a159bff6...` | **8 passed**, exit 0 |

All other tests are `NOT_RUN`. The tests were sourcefree pytest suites in isolated extracted trees; no production source, survey response, actor, native source, provider or arbitrary branch executable was run.

### 5. Named corrections

1. **Seam witness:** original author-reported 18/60 pass is contradicted by actual 26/1; implicated functions are `REVIEW_REVISE`/`DEFECTIVE_BLOCK`, not pass. Test rows are `NOT_PRODUCT_CODE`.
2. **PE:** complete contract remains invalid only for exact reverse-scope failure; `_auth` is precisely `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`; typed/schema helpers are sourcefree candidates, not trash. The 21 author passes do not close 9 independent strict failures; full K9 8/K10 28 NOT_REACHED.
3. **V2K:** reported 24 + 111 tests are not reproducible at the exact branch; collection fails on missing dependency. Owner-scope functions are `SCIENCE_HOLD`; schema pieces are `INSUFFICIENT`/needs ABI/consumer, not ready.
4. **Selected-world:** independent sourcefree scope is accepted and 24 tests pass; it is `SOURCEFREE_INTEGRATION_CANDIDATE`, not a current equivalent or whole N9/N10W. Current E03 is an alternative context, not proven equivalence.
5. **E03 exact current:** exact sourcefree code/test is present; 18 tests pass; adoption is `HISTORICAL_ACCEPTANCE_ONLY` for sourcefree E03 only, not whole N9/N10W, native source, GT2, FF/N9-N12, actor/person or scientific rule.
6. **Test rows:** 288 rows corrected to `NOT_PRODUCT_CODE`; test/fixture/evidence material is not production trash or adaptation code.
7. **B2/HQ273:** B2 EE14 actually 8 passed and HQ273 19 passed; both remain test evidence only; B2 still lacks G0b/source-qualified producer binding.

### 6. Unresolved mismatches / limits

- Seam has not been repaired; the one failing assertion remains.
- PE `_auth`/complete contract are not repaired; 9 independent strict failures and full K9/K10 remain.
- V2K cannot collect at the exact branch; missing dependency and foreign-issuer/held-row behavior remain.
- Selected-world/seam/E03/PE/V2K have no current path/consumer except exact E03 test; current P41/C1/N9 alternatives are not proven equivalent.
- 24 unclassified roster names remain preserved, not promoted.
- 111 branches have no branch-specific return evidence; preserved as unknown, not pass.
- No source/native/science/model/world/N11-N12/Sorok actor permission is issued.

## INTERPRETATION

The original S3 disposition was directionally cautious but still used flat labels that mixed production evidence, test evidence, accepted sourcefree scope, current presence and adoption. The corrected record separates those axes. The most important new facts are the actual seam failure, the actual PE independent 9 failures, and the V2K exact-branch collection failure. These are stronger than the original documentary claims and prevent a sourcefree candidate from being promoted as current/native.

## HQ ACTION

1. Preserve `65b83dee...` unchanged; use this 398-row delta and 174-row branch reconciliation instead of rewriting the old return.
2. Route selected-world/E03 to P41/C1/N9 owner for current-consumer boundary; route seam to sourcefree repair owner for the exact mutation failure; route PE to PE/SC0 owner for `_auth`/full K9/K10; route V2K to original U/E/source owner and restore the missing dependency before any replay.
3. Treat 288 test/fixture rows as `NOT_PRODUCT_CODE`; do not convert test evidence into production recovery.
4. Do not merge, adopt, execute arbitrary branch code, or issue source/actor/science permission.

## OWNER

Original Pyat source/semantic owners for selected-world/E03/P41/N9/N10W, seam repair owner, PE/SC0 owner, V2K original U/E/source owner, HQ273/HQ280 owners, incumbent HQ for intake, and a distinct H1 reviewer after exact SHA. No self-review.

## Three courts

- **ENGINEERING:** `PARTIAL_PASS_SCOPED_WITH_ACTUAL_SOURCEFREE_RECEIPTS__SEAM_AND_PE_REDS_PRESERVED`.
- **SCIENCE:** `HOLD__NO_ORIGINAL_SOURCE_OR_PERSON_AUTHORITY`.
- **AUTHORITY:** `HOLD__NO_ADOPTION__NO_MERGE__NO_SOURCE_GRANT`.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** 398/398 keyed corrections; 174/174 branch reconciliation; 22-path receiver matrix; exact source cuts; actual sourcefree receipts; named contested-claim counterexamples; no drops or reorder.

**REMAINING:** seam repair and rerun; PE `_auth`/full K9/K10; V2K dependency and foreign-issuer repair/replay; selected-world current consumer; E03 whole-service boundary; independent H1/S6/S7 review.

**BLOCKERS:** seam failure; PE 9 strict failures; V2K collection failure; no current receivers/source permissions; 111 evidence-unknown branches; 24 unclassified names.

**LARGEST PRODUCTIVE MOVE:** repair seam mutation and PE `_auth` first, then restore V2K dependency and rerun the exact four suites; route selected-world/E03 to current P41/C1/N9 owner. Do not merge S3 reviewer branches.

**FLIGHT:** `S3_398_KEYED_REGRADE + 174_BRANCH_RECONCILIATION + ACTUAL_SOURCEFREE_RECEIPTS + SEAM_PE_V2K_REDS + SCIENCE_AUTHORITY_HOLD + NO_ADOPTION`.

**DELTA:** `+` six-axis correction for every original row; `+` actual positive/negative receipts; `+` branch preservation; `+` named counterexamples; `−` no source/native/science/actor permission; `−` no PRE-MAIN mutation or merge.

## Return artifacts

- `FUNCTION_GRADE_CORRECTIONS.jsonl` — exactly 398 rows.
- `BRANCH_RECONCILIATION.jsonl` — exactly 174 rows.
- `CONTESTED_CLAIMS_AND_COUNTEREXAMPLES.md`.
- `RECEIVER_TEST_AND_SOURCE_PERMISSION_MATRIX.json` — 22 paths.
- `00_RETURN.md` — this file.

**Exact immutable pushed remote SHA:** reported after push/readback; self-reference excluded. Post-return gates: independent H1 #534, S6 #533 cross-shard join, then S7 #538.
