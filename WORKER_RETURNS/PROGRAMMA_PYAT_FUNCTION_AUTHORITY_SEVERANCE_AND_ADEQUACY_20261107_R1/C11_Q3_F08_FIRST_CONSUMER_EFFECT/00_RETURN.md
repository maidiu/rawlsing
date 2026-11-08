# C11 — Q3/F08 question-use authority → historical consumer → Q4 successor

**Lane:** issue #777 primary Q3 finite operation, same existing OpenCode session/model.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
**Branch:** `agent/pyat777-source-consumer-20261107-r1`
**Starting HEAD:** `02a13a5e01880835434b30d9a3587147f9dab0de`
**C6 corrected cut read:** `0d548b033a0a20c9738fa4a3412ba5acd01217c5`
**C6 archive source pin:** `9ba4764bef551b1ce498e5772d60b73d69337d4b`

## Q3 RESULT — selected historical authority is real; invocation is test-time replay only

C6 had already selected the authority and static consumer edge but recorded `ACTUAL_HISTORICAL_INVOCATION_NOT_OBSERVED` / `RUNTIME_NOT_RUN`. This commission exercised the **exact historical authority consumer** on one exact selected nonrespondent authority row. It did **not** establish that the original historical run occurred.

Selected authority bytes (verified SHA-256):

| Release | Locator | Bytes | SHA-256 | State |
|---|---|---:|---|---|
| AR-0047 itinerary | `data/ddm_build_copy/manifests/question_wave_itinerary.csv` @9ba4764 | 11,059 | `866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3` | selected |
| AR-0048 override | `data/ddm_build_copy/manifests/question_use_overrides.csv` @9ba4764 | 1,702 | `29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479` | selected |
| AR-0049 QSR baseline | archive path, LMQ-010 accepted baseline | 26,582,348 | `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b` | selected accepted baseline |
| AR-0050 taxonomy | `data/ddm_build_copy/manifests/question_type_taxonomy.yaml` @9ba4764 | 3,487 | `3612c6b400008467471b71cc38d811b8c5349bac0617e974a72e76e584e86b27` | selected |

Exact historical code/entrypoint:

```text
module: data/ddm_build_copy/ddm_v550_question_use.py @9ba4764
module SHA-256: 254542f96dcb8f07c9ff8fa136d6d13f5923b43ec04c7d2bb1d8a14f46955f31
entrypoint: build_question_use_contract -> build_question_use_contract_row
selectors: load_question_use_overrides; load_question_wave_itinerary; _select_override; _select_itinerary
```

The selected witness row was **GSS / 1973 / `uswar`**:

- AR-0048 selected override: `source=GSS`, `wave=1973`, `var_code=uswar`, role `RELATION_EVIDENCE`, reason `promote_memory_of_catastrophe_direct_evidence`, selectivity basis `source_wave_var_code`.
- AR-0047 selected itinerary: GSS 1973, `review_priority=high`, `manual_designation_required=false`.
- AR-0049 selected row: `question_id=GSS:1973:uswar`, `var_name=uswar`, classification `substantive_single_choice`; exact join `source+wave+question_id`.
- AR-0050 selected taxonomy: `single_choice`, structural role `answer`; loaded by the historical register-builder consumer, not by the QUC contract entrypoint.

Observed unchanged-consumer effect:

```text
manual_override_used = true
manual_override_basis = source_wave_var_code
manual_override_reason = promote_memory_of_catastrophe_direct_evidence
semantic_role = RELATION_EVIDENCE
itinerary_review_priority = high
source_structure_classification = substantive_single_choice
source_structure_fields_joined = true
review_required = true
allowed_as_v551_relation_evidence = false
question_use_contract_hash = 6c94c7a8bbbf4dbae511dece64a312a1ee7fd5fa3a8e4008f004783057288cb1
positive contract-summary hash = 1c78a386f0b433dd4ffb97768314f92b09e7476d1c31f4a92f8343cb26f253b1
```

The selected authority was consumed and changed the override/use contract. The result is **not a full operational PASS**: the same contract remains `review_required` because separate semantic, directional and structural authorities are missing. That limitation is preserved rather than hidden.

### Negative / restore (disposable copies)

| Negative | Observed |
|---|---|
| AR-0048 selected row removed | `manual_override_used=false`, basis/reason empty, contract hash `6dd4fa85...`; role remains `RELATION_EVIDENCE` from inference |
| AR-0048 selected row duplicated | `RuntimeError: ambiguous manual override match ... source_wave_var_code: 2 rows` |
| AR-0049 register absent | fallback `missing_register`, join `none`, `source_structure_fields_joined=false`, contract hash `a8010c5...` |
| AR-0047 GSS 1973 itinerary removed | `itinerary_review_priority=normal` (was `high`), contract hash `57cf755d...` |
| Restore exact bytes | positive contract hash/output hash restored exactly (`1c78a386...`) |

## Q4 — current successor location

The current installed successor is **not a QUC/question-use reader**. The C6 mapping is still exact:

- `rawlsing_next/pre553_empirical_objects.py:677` — `EmpiricalQuerySpec` carries query targets, condition, scope and `requested_output_grain`.
- `rawlsing_next/pre553_empirical_query.py:403-438` — current I03 consumes optional `target_use_ref` / `TARGET_USE_PERMISSION` only inside exact query/authority closure.
- `rawlsing_next/pre553_empirical_authority.py:41` — `TARGET_USE_PERMISSION` authority kind.
- `rawlsing_next/pre553_universal_workload.py:473,633` — current governed-frontier compile/execute owners.

No installed non-test `question_use`/itinerary/taxonomy reader was found in current `rawlsing_next`; target-use permission is a **different current authority**, not a QUC equivalent. C6 records AR-0047/AR-0048/AR-0050 bytes as historical and protected-same-bytes but current adoption **not proved**; AR-0049's current protected path is absent. There is no selected current operation in the examined C6/current evidence that demands the historical QUC input, so **severance is not called**. The current classification is:

```text
FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED
  __NO_SELECTED_CURRENT_QUC_OPERATION
  __NO_QUC_READER_IN_CURRENT_OWNER
```

Exact remaining boundary: `question_use_contract / itinerary / taxonomy` semantics are not represented in current `EmpiricalQuerySpec`/I03 target-use permission; a current selected operation requiring them would need a QUC reader/typed current representation at the existing query/authority owner. No new resolver, engine or Q_USE implementation was added. Sourcefree replay is **not** original equivalence.

## EVIDENCE DISTINCTIONS

| Dimension | Status |
|---|---|
| Historical selection | Exact AR-0047/48/49/50 bytes and rows selected by C6 |
| Historical original runtime | `NOT_RUN` / `ACTUAL_HISTORICAL_INVOCATION_NOT_OBSERVED` |
| Test-time replay now | Positive/negative/restore observed with exact historical consumer on authority metadata |
| Current adoption | AR-0047/48/50 bytes not proved adopted; AR-0049 current protected path absent; no QUC reader |
| Current selected QUC operation | None observed; no severance verdict |

## COVERAGE / EXECUTION LIMITS

- AR-0047: 35 itinerary rows; AR-0048: 7 overrides; AR-0049: 18,792 register rows; AR-0050: 8 question types. These declared rows are preserved; one selected row is a witness only. No witness substitutes for all35.
- The outer `build_determinicity_wave_shard_v550.py:1567` shard entrypoint was not run because it requires source/respondent shard rows; its exact QUC callee was run on frozen, nonrespondent authority metadata.
- Test-time historical replay now is not evidence that the original historical run occurred.
- No source/respondent/SAV/DTA/DB read, source-byte copy/upload, native/S3/science/actor effect, production/existing-test/HQ/peer/protected write, environment install, new worker or model/provider/effort change.
- Prior C6 selection/status evidence and all relation statuses are preserved.

## EVIDENCE

`TRACE.jsonl` contains the row/rule, file and module pins, positive/negative/restore hashes, execution distinction and current owner/boundary. Probe output and log are under `probes/` and `logs/`.
