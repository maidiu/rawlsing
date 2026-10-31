# S3 evidence repair — contested claims, counterexamples and promotion conditions

**Original return:** `65b83dee3385fc85d5d283c19acd270dea50a27d`. **Frozen PRE-MAIN baseline:** `750548ddbb9b4392a16ce93097b856f349e16182`; **actual PRE-MAIN head at audit close:** `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3` (22/22 S3-relevant paths unchanged). **Corrected evidence law:** `f50651a2bb0758e9fe6d6a2852441dcc782344be`.

This file records only claims whose original S3 label or implication is corrected, contradicted, or materially qualified. Every correction is keyed in `FUNCTION_GRADE_CORRECTIONS.jsonl`; every branch is preserved in `BRANCH_RECONCILIATION.jsonl`.

## 1. Seam witness: author-reported pass is contradicted by actual sourcefree execution

**Original S3 claim/implication:** `r3_s02_seam_witness.py` is `UNIQUE_USEFUL_NEEDS_ADAPTATION`; the author reports 18 seam tests and 60 combined tests pass; no current path/consumer.

**Independent receipt:** exact tip `ed34944e253b78714a28d72b8ca2a6521ce15930`; extracted `rawlsing_next` plus the exact `WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1` fixture:

```sh
PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q rawlsing_next/tests/test_r3_s02_seam_witness.py
# 26 passed / 1 failed; exit 1
```

Failure: `test_s00c_change_source_owned_synthetic_numeric_values_changes_result` at line 321, `KeyError: 'exact_probabilities'`. The test mutates source-owned synthetic numeric values and expects the consumer result to expose `exact_probabilities["1"] == {"$exact_fraction": [1, 2]}`; the current consumer result does not.

**Corrected finding:** the seam family is not proven pass. `build_source_free_native_joint_bundle`, `ContractOnlySeamConsumer.compute_scenario`, and `_content_hash` are `REVIEW_REVISE` / `DEFECTIVE_BLOCK`; the remaining seam typed/schema helpers are `SOURCEFREE_INTEGRATION_CANDIDATE` only. The seam test row is `NOT_PRODUCT_CODE` with `FAIL_WITH_RECEIPT`, not a production defect and not a pass.

**Condition for future promotion:** repair the exact mutation path, rerun all 27 seam tests with 0 failures, prove the current P41/C1/N9 consumer and sourcefree integration, then obtain original owner and independent H1 review. Do not promote from the old author count.

## 2. PE generic complete contract vs independent typed/schema helpers

**Original S3 claim:** `serve_generic_world_situated_possibility` and `verify_generic_world_situated_replay` are `INVALID`; `_auth` is `TRASH_WITH_GROUNDS`; the rest are adaptation helpers.

**Independent receipts:** exact tip `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`, exact PE blob `58484f4c3d9aae148d4116dcf00420c432aefcbd`.

```sh
# author court
PYTHONPATH=. ... pytest -q rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py
# 21 passed; exit 0

# independent strict court, exact PE root
HQ297_EXACT_PE_ROOT=<extracted-tree> PYTHONPATH=. ... \
pytest -q rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py
# 4 passed / 9 failed; exit 1
```

The independent failures include `test_strict_reverse_scoped_issuer_forgery_must_refuse` plus eight strict schema/world failures. This directly confirms the `_auth` defect: a non-null role-reversal authority ref is not dereferenced against competent reversed target/risk/denominator scope.

**Corrected finding:** the complete contract remains rejected/defective. `_auth` is precisely `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`, not generic trash. The typed/schema helpers are **not** condemned by the complete-contract failure; they are `SOURCEFREE_INTEGRATION_CANDIDATE` only, with no current path/consumer. The 21 author passes do not close the 9 independent strict failures. Full SC0 K9 8 / K10 28 remains NOT_REACHED.

**Condition for future promotion:** replace/repair `_auth`; make reverse-scoped issuer forgery refuse; run the 13 independent strict cases plus full K9/K10; prove a current receiver and original PE/SC0 owner review. No generic `TRASH` label and no helper promotion without separate proof.

## 3. V2K original identity: reported 24 + 111 tests are not reproducible at the exact branch

**Original S3 claim:** V2K is a useful unadopted schema; independent court reports 21 diagnostic + 24 candidate + 111 owner tests pass; foreign issuer and removed-held-row acceptance remain; semantic adoption withheld.

**Independent receipt:** exact tip `694fb45085cd5e4891949921a44edb77c3f603f2`:

```sh
PYTHONPATH=. ... pytest -q \
  rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py \
  rawlsing_next/tests/test_hq294_a04b_actual_scope_variants.py \
  rawlsing_next/tests/test_hq294_a04b_identity_court.py \
  rawlsing_next/tests/test_postastra_pv_v2k_independent.py
# collection error; exit 2
# ImportError: cannot import name 'pre553_original_workload_contract_v2_candidate'
```

The exact branch tree does not carry `pre553_original_workload_contract_v2_candidate.py`; the tests cannot collect. The reported 24 + 111 passes are therefore **not reproduced at the exact source cut**.

**Corrected finding:** `OwnerScopePlan`, `_validate_original_against_c11`, `run_sourcefree` remain `REVIEW_REVISE` / `SCIENCE_HOLD` for foreign-issuer and removed-held-row behavior; the identity/schema functions are `INSUFFICIENT` / `NEEDS_ABI/CONSUMER_TESTS`, not current-ready. No source authority is issued. The source-native/rule hold does not ban sourcefree inspection or tests; it bans treating the sourcefree pass as native/semantic adoption.

**Condition for future promotion:** restore or explicitly bind the missing dependency at the exact receiver; rerun the four suites with actual receipts; repair foreign issuer and removed-held-row acceptance; obtain original U/E/source owner and independent review. Prior 24 + 111 counts alone are insufficient.

## 4. Selected-world progressive contract: accepted sourcefree scope, not current integration

**Original S3 label:** `UNIQUE_USEFUL_NEEDS_ADAPTATION`; author reports 24 P04 tests and 60 combined tests pass; no current path/consumer.

**Independent receipt:** exact tip `ed34944e...`, selected-world test file:

```sh
PYTHONPATH=. ... pytest -q rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py
# 24 passed; exit 0
```

Current PRE-MAIN has the exact sourcefree E03 progressive module `pre553_n9_n10w_progressive_candidate.py` blob `84d40414...`; it does **not** have the selected-world contract, seam consumer, or current P41/N9/N10W service. The current E03 chain is an alternative implementation context, not proven equivalence.

**Corrected finding:** selected-world contract source functions are `PREVIOUSLY_ACCEPTED_SCOPED` at sourcefree offline scope and `SOURCEFREE_INTEGRATION_CANDIDATE`; test rows are `NOT_PRODUCT_CODE` / evidence-only. They are not current equivalents and not a whole N9/N10W service.

**Condition for future promotion:** current P41/C1/N9 adapter/consumer, exact owner review, sourcefree integration test on current receiving code, and independent review. Do not infer current function from path absence alone; do not infer whole N9/N10W from accepted sourcefree scope.

## 5. E03 exact current: sourcefree code present, not whole N9/N10W

**Original S3 claim:** 39 E03 source/test symbols are `EXACT_ALREADY_IN_PREMAIN`.

**Independent receipt:** exact current source `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` blob `84d404147547767be8ecd4b6e1541f5fa3a8c8a2`; exact current test; 18 current tests pass.

**Corrected finding:** exact code presence is retained (`IDENTICAL_BLOB`), but historical merit/adoption is `HISTORICAL_ACCEPTANCE_ONLY` at sourcefree E03 scope. It does **not** establish whole N9/N10W, native source, GT2 value, FF/N9-N12, actor/person or scientific rule. Test rows are `NOT_PRODUCT_CODE`. Sourcefree tests remain allowed; only the whole-service/native claim is held.

**Condition for future promotion:** none from this row set. A whole-service/native claim needs separate P41/N9/N10W owner, source/science permission, current consumer and tests.

## 6. Test and fixture rows were not code defects

**Original S3 labels:** many test/fixture rows were `UNIQUE_USEFUL_NEEDS_ADAPTATION`, `EVIDENCE_UNKNOWN`, or `INVALID`.

**Corrected finding:** **288** test/fixture rows are `NOT_PRODUCT_CODE`. They are evidence-only or unknown evidence, not production functions, not trash. `INVALID` label on `test_hq297_k9e_port_repro.py` test rows is removed; the complete PE contract retains invalidity only at its exact scope. Test results are recorded separately (selected-world 24 pass; seam 26/1; PE author 21 pass; PE independent 4/9; E03 18 pass; HQ273 19 pass; B2 8 pass; V2K collection error).

**Condition for future promotion:** never promote a test/fixture row to production code. A test may support or refute a source function; it is not itself a source recovery candidate.

## 7. B2 EE14 and HQ273: test evidence now actually run, still not production

**Original S3 claims:** B2 EE14 8-case candidate `UNEXECUTED`; HQ273 C01 19 tests reported but not rerun.

**Independent receipts:**

```sh
# B2 tip a159bff6
PYTHONPATH=. ... pytest -q rawlsing_next/tests/test_pre553_ee14_selected_lifecycle_source_free_integration.py
# 8 passed

# HQ273 tip 2406a4d7
PYTHONPATH=. ... pytest -q rawlsing_next/tests/test_hq273_c01_true_i03_conditioned_denominators.py
# 19 passed
```

**Corrected finding:** both are test-only evidence. B2 still lacks G0b/source-qualified producer binding and current service; HQ273 remains a sourcefree court, not production integration. Test pass does not create source/actor authority.

## 8. No unsupported promotion survived

The correction set contains:

- `UNIQUE_USEFUL_READY = 0`
- `SUPERSEDED_BETTER = 0`
- `INDEPENDENTLY_REBUILT_EQUIVALENT = 0`
- no generic `TRASH_WITH_GROUNDS`; the one `_auth` row is `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`
- no new source/native/science/actor permission
- no PRE-MAIN mutation or merge

Any future READY/SUPERSEDED/REBUILT/TRASH claim must cite an exact current receiver, actual positive and fault-negative tests or a specific reviewer counterexample at the claimed scope, and independent review.
