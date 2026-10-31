# S1 evidence repair — contested claims and counterexamples

**Status:** `REGRADE_COMPLETE__NO_READY_SUPERSEDED_REBUILT_OR_TRASH_GRANTED__H1_S6_REVIEW_REQUIRED`

This is a delta against immutable S1 return `c85db39772a8ac09fd70c6bb94a39dd04274d2cb` at frozen baseline `750548ddbb9b4392a16ce93097b856f349e16182`, rechecked against actual current PRE-MAIN `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3`. The `rawlsing_next` tree is identical at both cuts; the only delta is `tests/test_copy_paste_commission_r1.py`. It does not overwrite the original return and does not adopt any function.

## 1. Corrected disposition counts

- `NO_ACTION_CODE_PRESENT`: **542**
- `HYPOTHESIZED_VALUE__NEEDS_ABI_AND_CONSUMER_TESTS`: **284**
- `SOURCEFREE_ENGINEERING_CANDIDATE__NEEDS_ABI_CONSUMER_TESTS`: **181**
- `SOURCEFREE_TEST_ALLOWED__OPERATION_PERMISSION_GRANT_REQUIRED`: **150**
- `DIFFERENT__COMPARISON_REQUIRED`: **73**
- `EVIDENCE_UNKNOWN`: **34**
- `HYPOTHESIZED_VALUE__PERMISSION_AND_TESTS_REQUIRED`: **15**

## 2. Corrected adoption counts

- `SOURCEFREE_INTEGRATION_CANDIDATE`: **615**
- `NEEDS_ABI/CONSUMER_TESTS`: **480**
- `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE`: **150**
- `INSUFFICIENT_EVIDENCE`: **34**

## 3. Permission-axis holds

`REQUIRED_UNGRANTED` appears only on named permission axes; no row receives a blanket source hold. Sourcefree test applicability is recorded separately.

- `SCIENTIFIC_RULE_ISSUE`: **164** rows
- `MODEL_USE`: **131** rows
- `SOURCE_NATIVE_READ`: **112** rows
- `WORLD_STRUCTURAL_ADMISSION`: **55** rows
- `SOROK_ACTOR`: **4** rows

## 4. The 73 `SUPERSEDED_BETTER` claims are all downgraded

The original S1 return claimed superiority from same-path/different-AST comparison. No old behavior assertion, current behavioral equivalence, current positive oracle, current fault-negative oracle, receiver execution or measurable safety/correctness improvement was supplied. Therefore all 73 are corrected to `DIFFERENT__COMPARISON_REQUIRED`, not `SUPERSEDED_BETTER`.

Representative rows: `RecurrenceIssuePlan` @ `rawlsing_next/universal_grammar/native_map.py`, `build_recurrence_issue_plan` @ `rawlsing_next/universal_grammar/native_map.py`, `execute_recurrence_generation` @ `rawlsing_next/universal_grammar/native_map.py`, `activate_next_generation` @ `rawlsing_next/universal_grammar/native_map.py`, `ScientificOperation` @ `rawlsing_next/universal_grammar/types.py`, `make_operation` @ `rawlsing_next/universal_grammar/types.py`, `current_native_contract` @ `rawlsing_next/universal_grammar/native_map.py`, `NativeCatalog` @ `rawlsing_next/universal_grammar/native_map.py`.

A future `SUPERSEDED_BETTER` requires: (a) same function/behavior at declared scope, (b) exact historical positive and fault-negative assertion, (c) reproduction or deliberate replacement on the current receiver, and (d) a linked receipt showing the specific improvement or removed defective reliance.

## 5. The 331 `SOURCE_HELD` claims are replaced by operation-specific axes and sourcefree applicability

The original S1 return treated path-level source context as a blanket authority hold. The correction separates `SOURCE_NATIVE_READ`, `SCIENTIFIC_RULE_ISSUE`, `MODEL_USE`, `WORLD_STRUCTURAL_ADMISSION`, `N11_N12` and `SOROK_ACTOR`. Data/class rows are not held merely because they live in a source-related module; their method-level operations remain unassessed. Entrypoints that require an ungranted operation are named with the function symbol and owner class.

Corrected held-family split:
- `SOURCEFREE_ENGINEERING_CANDIDATE__NEEDS_ABI_CONSUMER_TESTS`: **181**
- `SOURCEFREE_TEST_ALLOWED__OPERATION_PERMISSION_GRANT_REQUIRED`: **150**

Representative rows: `write_json` @ `rawlsing_next/source_configuration/tools/build_evidence.py`, `write_jsonl_gz` @ `rawlsing_next/source_configuration/tools/build_evidence.py`, `json_value` @ `rawlsing_next/source_configuration/tools/build_evidence.py`, `cmd_build_index` @ `rawlsing_next/source_configuration/cli.py`, `cmd_status` @ `rawlsing_next/source_configuration/cli.py`, `cmd_list` @ `rawlsing_next/source_configuration/cli.py`, `cmd_show` @ `rawlsing_next/source_configuration/cli.py`, `cmd_validate` @ `rawlsing_next/source_configuration/cli.py`, `cmd_fixture_call` @ `rawlsing_next/source_configuration/cli.py`, `cmd_native_results` @ `rawlsing_next/source_configuration/cli.py`, `cmd_original_plan` @ `rawlsing_next/source_configuration/cli.py`, `parser` @ `rawlsing_next/source_configuration/cli.py`.

The original blanket hold was false for sourcefree engineering/grammar/checkpoint/evidence-binding code. It was also false to treat source-read engineering as if all sourcefree tests were prohibited. The corrected rows state where sourcefree ABI/consumer tests are allowed and where an exact native/source/model/world/actor grant is required.

## 6. The 299 `NEEDS_ADAPTATION` claims are not proven unique value

Path absence, a same-name/different-AST candidate or a branch-level positive return does not prove a unique worthwhile function. All 299 are corrected to `HYPOTHESIZED_VALUE__NEEDS_ABI_AND_CONSUMER_TESTS` or `HYPOTHESIZED_VALUE__PERMISSION_AND_TESTS_REQUIRED`; 615 rows overall are only `SOURCEFREE_INTEGRATION_CANDIDATE` at best. No row is `READY_FOR_SOURCEFREE_INTEGRATION_COURT`.

Representative rows: `EvidenceBindingError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceRequestShapeError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceBindingMismatch` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceCacheIntegrityError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceAssociationError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `TypedValue` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `OccurrenceKey` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `TypedCondition` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `AdmittedEvidenceContext` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceRequest` @ `rawlsing_next/pre553_universal_evidence_binding.py`.

Promotion requires an exact current function-absence proof, ABI/schema/import closure, current first consumer, sourcefree positive and fault-negative tests, and regression results. None were executed in this regrade.

## 7. The 34 `EVIDENCE_UNKNOWN` rows remain unknown

These rows have no current equivalent, no exact/no-id AST match and no branch-specific verdict sufficient for promotion. They are retained as `EVIDENCE_UNKNOWN`/`INSUFFICIENT_EVIDENCE`, not dropped and not called valuable.

Representative rows: `git_blob` @ `rawlsing_next/source_configuration/tools/build_evidence.py`, `ref` @ `rawlsing_next/source_configuration/tools/publish_p3.py`, `EvidenceBindingError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceRequestShapeError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceBindingMismatch` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceCacheIntegrityError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `EvidenceAssociationError` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `TypedValue` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `TypedCondition` @ `rawlsing_next/pre553_universal_evidence_binding.py`, `AdmittedEvidenceContext` @ `rawlsing_next/pre553_universal_evidence_binding.py`.

## 8. The 542 exact-AST matches are code presence only

They are preserved as `EXACT_AST_SAME_PATH` and `NO_ACTION_CODE_PRESENT`. That is not a source-science, original-method, model, actor or N11/N12 acceptance. Current operation permission is recorded separately. Representative rows: `current_native_contract` @ `rawlsing_next/universal_grammar/native_map.py`, `NativeCatalog` @ `rawlsing_next/universal_grammar/native_map.py`, `LoweringRecord` @ `rawlsing_next/universal_grammar/native_map.py`, `lower_operation` @ `rawlsing_next/universal_grammar/native_map.py`, `LoweringPlan` @ `rawlsing_next/universal_grammar/native_map.py`, `lower_frontier` @ `rawlsing_next/universal_grammar/native_map.py`, `native_receipt_anti_join` @ `rawlsing_next/universal_grammar/native_map.py`, `RecurrenceRefusal` @ `rawlsing_next/universal_grammar/native_map.py`.

## 9. No READY, independent rebuild, invalid/trash or new permission

- `UNIQUE_USEFUL_READY`: **0**. No candidate + current receiver tests were executed.
- `INDEPENDENTLY_REBUILT_EQUIVALENT`: **0**. No alternate-path behavioral equivalence proof was executed; same-name/different-AST candidates remain unproven.
- `INVALID/TRASH_WITH_GROUNDS`: **0** production functions. Test/probe/doc-only material is excluded from the function court; no production function had a direct at-scope scientific/behavioral falsifier with an original or independently reproduced counterexample.
- No source/actor/CAN/ADP/SCI/N11/N12 permission was created, inferred or self-granted.

## 10. Mandatory no-silent-loss precedents outside this S1 row set

These are not adjudicated by S1 and must be handled in the independent H1 #534 / S6 #533 cross-shard join: S5 119 READY-vs-NOT_RUN, S2 10 SUPERSEDED_BETTER, S4 171 INVALID/TRASH, S4/S5/S1/S2 blanket HELD counts, S3 `_auth` PE role reversal, original C3 six-blob vs PR526 decoder snapshot and R9 broker, E03 byte-identity with P41 vendor but larger P41 service not integrated, R61-R09 child-authored forged capture RED, and F7/P07 alias/unauthenticated receipt. S1 neither absolves nor condemns them here.

## 11. Currentness check

- Frozen baseline: `750548ddbb9b4392a16ce93097b856f349e16182`.
- Actual current PRE-MAIN checked: `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3`.
- `git diff --stat 750548dd..5ad805e5 -- rawlsing_next` is empty; the exact current function comparisons therefore remain valid. A `tests/test_copy_paste_commission_r1.py` test was added, not a production function. If PRE-MAIN moves again, the current-presence and receiver rows must be rechecked.

## 12. Conditions for future promotion

1. `SUPERSEDED_BETTER`: same behavior + current positive/fault-negative receipt + specific improvement/removed defect.
2. `READY_FOR_SOURCEFREE_INTEGRATION_COURT`: current function-absence proof + ABI/schema/permission/consumer closure + executed sourcefree positive/fault-negative/regression tests.
3. `INDEPENDENTLY_REBUILT_EQUIVALENT`: alternate path/owner + matching observable behavior + negative boundaries, not name/AST heuristic.
4. `TRASH/INVALID`: direct at-scope falsifier and original/independent counterexample, not absence of production wiring.
5. `SOURCE_AUTHORITY_HOLD`: named operation, competent issuer, exact universe/consent/use and target, plus a statement of lawful sourcefree work that may continue.
