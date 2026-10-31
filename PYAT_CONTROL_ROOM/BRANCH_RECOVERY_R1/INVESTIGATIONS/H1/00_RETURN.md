# PYAT 845 H1 — independent hostile evidence and function court

## Identity and frame

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Role | Independent hostile historical-code, scientific-evidence and integration reviewer; NOT S1–S5 author, S6, original reviewer, source/scientific issuer or own reviewer |
| Branch | `review/pyat-845-s1-s5-independent-hostile-court-20261030-r1` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-845-s1-s5-independent-hostile-court-20261030-r1` |
| Device | `mainMac` (`scutil`) |
| Harness / agent | OpenCode `1.18.34`, agent `build` |
| Model / effort | `opencode-go/deepseek-v4.1-flash`, session variant `max` |
| Session | `ses_e7285576bffeqo0lE8N0HYK6gc` |
| Startup | `750548ddbb9b4392a16ce93097b856f349e16182` |
| Actual current PRE-MAIN checked | `5fc1d43e3d5412194d1f1eaa30ff448f84635e99` |
| Shared evidence law | `f50651a2bb0758e9fe6d6a2852441dcc782344be` |
| Final H1 SHA | reported externally after push; a commit cannot contain its own hash |

## Inputs

Original S1–S5: `c85db39772a8ac09fd70c6bb94a39dd04274d2cb`, `ab303ee446c87beca32dc2c322704f6cf0dc7b79`, `65b83dee3385fc85d5d283c19acd270dea50a27d`, `8f4ad92aa47b7ae53d625bc2587357092af96e27`, `1aa0407869620cd8ba2e8ca1f1533b99fd097162`.

Corrected S1–S5: `6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5`, `3042fca8a2165e07871d408118e1741686020cdc`, `ebdb51a5c79209b2e552cfce648f7847b19386c2`, `d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb`, `32dac59b3741dcc54f507321c7826e65174af372`.

The five original returns and five corrected returns were read at their exact commits. The original S3/S4 `FUNCTION_COURT.jsonl` files were extracted and compared directly; the original S1/S2/S5 row hashes were checked where present.

## Machine-visible outputs

| Artifact | Count |
|---|---:|
| `H1_S1_S5_GRADE_CHALLENGES.jsonl` | **2,146** challenge rows: 2,138 function claims, 5 court receipts, 2 custody-schema rows, 1 current-receiver partial receipt |
| `BRANCH_COUNT_AND_FUNCTION_CUSTODY_VERIFICATION.json` | 845 branches, 3,135 function rows across five shards |
| `SCOPE_AND_AUTHORITY_NEGATIVES.md` | scope, tests, authority negatives |
| `HANDOFF_TO_S6_S7.md` | S6/S7 gates and verdict matrix |
| `00_RETURN.md` | this return |

The H1 challenge file preserves each challenged original/corrected row ID, exact path/blob/tip, original reviewer assertion, current competing function, verdict and falsifier. The custody file records direct S3/S4 attribute verification and the original-row-hash schema gap.

## Direct findings

### 1. S1's 150 `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE` — REVISE

All 150 S1 rows carry `COMPATIBILITY` statuses `NOT_TESTED`, `positive_oracle=NOT_TESTED`, `receipts=[]`, and zero E3 current-receiver execution. S1 itself did not run a current receiver test. H1 independently ran 105 current tests at actual PRE-MAIN `5fc1d43e` across `test_universal_grammar.py`, `test_universal_workload.py`, `test_universal_source_byte_custody.py` and `test_universal_source_projection.py`: **105 passed, exit 0**. That is module-level coverage, not row-level acceptance for all 150; 27 of the 150 rows are in modules outside those four test files (`_pre553_query_common` 12, `physical_decoder` 7, `source_native_preimage_adapter` 5, `empirical_query` 2, `analytical_composition` 1). Verdict: `ENGINEERING_REVISE__ROW_SCOPE_CURRENT_ACCEPTANCE_UNPROVEN`.

### 2. S4's 325 `RENAMED_EQUIVALENT_PROVEN` — RED

All 325 rows have `evidence_strength=E1_EXACT_CURRENT_BODY_PRESENCE` only; `first_consumer` is empty for all; `positive_oracle` and `fault_negative_oracle` are `NOT_TESTED`; `receipts=0`; 323/325 original paths are `WORKER_RETURNS` test/corpus, not current production. Exact body presence at a renamed path is not behavioral equivalence. Verdict: `ENGINEERING_RED__RENAMED_EQUIVALENCE_UNPROVEN__E1_ONLY`; required action is `RENAMED_BODY_EXACT__RUN_CURRENT_ABI_CONSUMER_AND_NEGATIVE_ORACLE`.

### 3. S3 seam / PE / V2K — ACCEPT THE NEGATIVES

H1 extracted the exact tips and reran the S3 courts:

- Seam at `ed34944e…`: **26 passed, 1 failed**, exit 1. Failure `test_s00c_change_source_owned_synthetic_numeric_values_changes_result: KeyError exact_probabilities`. H1 initially saw a second manifest failure because its sparse tree lacked `WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json`; after materializing that exact path, H1 reproduced the worker's 26/1.
- PE strict at `e61a26ce…` with `HQ297_EXACT_PE_ROOT` set to the exact tree: **4 passed, 9 failed**, exit 1.
- V2K at `694fb450…`: **collection error, exit 2**, missing `pre553_original_workload_contract_v2_candidate`.
- Selected-world at `ed34944e…`: **24 passed**, exit 0.
- E03 at `ed34944e…`: **18 passed**, exit 0.

These are genuine sourcefree receipts. They are not native, whole-service, GT2, N9/N10W, actor or scientific acceptance.

### 4. All original READY / SUPERSEDED / TRASH / HELD / uniqueness claims

- **119 S5 `UNIQUE_USEFUL_READY`**: all downgraded to `HISTORICAL_ACCEPTED_SCOPED_CURRENT_UNTESTED`; H1 verdict RED for current readiness.
- **89 original `SUPERSEDED_BETTER`** across S1/S2/S5: 88 explicitly `REVISE__SUPERIORITY_UNPROVEN`; 1 is already a preserved specific defect. No superiority is accepted without current behavior and positive/fault-negative receipts.
- **555 original `SOURCE_HELD`** across S1–S5: 546 replaced by operation-specific axes, 9 preserved specific defects. No blanket source hold is accepted; lawful sourcefree tests remain allowed.
- **713 original adaptation/uniqueness claims**: retained as `HYPOTHESIZED_VALUE`/`UNIQUE_VALUE_AND_CURRENT_TESTS_UNPROVEN`; no READY, unique capability or current integration claim.
- **187 original INVALID/TRASH**: 171 flat-trash labels downgraded to evidence-only/insufficient; 16 original trash-labeled rows preserved as specific defects. Including 9 S4 held and 3 S3 adaptation rows that corrected to defective blocks, **28 specific defective findings are preserved**; no generic trash is accepted.
- **S1 542 exact rows**: code presence only; no source/science acceptance. **S4 1 same-path exact row**: code presence only, not current adoption.

### 5. S3/S4 original-row hash gap — CUSTODY ACCEPT WITH SCHEMA GAP

S3 and S4 corrected rows do not carry `original_row_sha256`. H1 verified the original attributes directly rather than relying on IDs:

- S3: all **398/398** rows match original `function_id`, `path`, `symbol`, `historical_blob`, `original_label`, `original_branch` and `tip_sha`; 0 mismatches.
- S4: all **897/897** rows match original `function_id`, `name`, `primary_blob`, `primary_branch`, `primary_tip_sha` and `original_label`; corrected `original_path` is one of the original occurrence paths for 897/897; 0 mismatches.
- S5 has `original_row_sha256` for 343/343 rows.

The absent hash field is a schema deficiency, not lost custody. Future schema should add `original_row_sha256` for every row.

## Three courts

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `H1_REVIEW_COMPLETE__S1_ROW_SCOPE_REVISE__S4_RENAMED_EQUIVALENCE_RED__S3_NEGATIVES_REPRODUCED__CUSTODY_VERIFIED` | 2,146 challenges; actual sourcefree receipts; 845/3,135 custody; no PRE-MAIN mutation |
| SCIENTIFIC | `HOLD__NO_ORIGINAL_SOURCE_OR_SCIENTIFIC_ISSUANCE` | no original survey/response, no source-native read, no CAN/ADP/SCI, no N11/N12 |
| AUTHORITY | `HOLD__NO_ADOPTION__S6_533_AND_S7_538_REQUIRED` | no source/actor/model/world grant, no merge, no self-adoption |

## Tests and NOT_RUN

Actual H1 tests: seam 26/1; PE 4/9; V2K collection error; selected-world 24/0; E03 18/0; current universal module coverage 105/0. All other branch tests, S4/S5 F7/P07 reruns, native/source/world/actor operations and current first-consumer tests are `NOT_RUN`.

## Hand-back

The exact H1 SHA is reported externally after push. Independent H1 review does not adopt; S6 #533 must join cross-shard families and preserve the 28 specific defects; S7 #538 must apply the evidence ladder. No self-adoption, merge or source/actor issuance occurred.
