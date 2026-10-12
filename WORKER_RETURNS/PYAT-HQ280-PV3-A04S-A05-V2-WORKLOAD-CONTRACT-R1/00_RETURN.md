# PYAT HQ280 PV3 A04S — A04→A05 canonical v2 workload contract

**TERMINAL:** `HQ280_PV3_A04S_SOURCEFREE_V2_EXPECTATION_BINDER_ORACLE_ACTUAL_JOIN_RETURNED_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`
**RESULT:** `PASS__V2_SUCCESSOR_CONNECTS_A04_BINDER_TO_INDEPENDENT_ORACLE__26_TESTS_PASS__16_OF_16_HOSTILES_DETECTED__A04_41_AND_A05_18_UNCHANGED__SOURCEFREE_ONLY__NONISSUING`
**Branch:** `agent/rabochii-pyat-hq280-pv3-a04s-a05-v2-workload-contract-r1`
**Sealed startup (verified before mutation):** `0f8c6d085513588c5fdfcf371c1e8fe1e7927059`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).
**A04 base:** `cbe047cf15a2285b0e918bd77640037f7bec63ef` (binder blob `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5` — **intact, verified**).
**A04R reviewer:** `fca056a3e8497a3acd6c6de597c269e3000df875`.
**A05 oracle:** `9491d0296c95ee2942fe80eadc6aa9f54b07c634` — **verified 18/18 still pass** in its own worktree.

## 1. What was built

Two NEW files. **No A04/A05 file edited, no accepted owner touched** (`git diff` on `rawlsing_next/` is empty).

| File | Blob | Lines | Role |
|---|---|---|---|
| `rawlsing_next/pre553_original_workload_contract_v2_candidate.py` | `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` | 1150 | v2 canonical schema + mapping + oracle |
| `rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py` | `0b9f1addf2b28f2a8e489fe44f1567a137a166f2` | ~800 | 26 tests |

A04's binder is **reused as-is** (blob verified identical). A05's oracle contract is **translated to, never coerced, never rehashed**.

## 2. A04R findings resolved (all seven)

| A04R finding | v2 resolution | Test |
|---|---|---|
| Semantic operation class vs owner dispatch class conflated | `SEMANTIC_TO_DISPATCH`: `UNARY_DISTRIBUTION`/`PAIR_RESPONSE_COTRAVEL`/`NONSCALAR_TOPOLOGY_PRESERVATION` → `I03_UNARY_OR_JOINT_QUERY`; `BOUNDED_DISCOVERY` → `I05_BOUNDED_DISCOVERY` | `test_v2_semantic_vs_dispatch_classes_are_separate` |
| RAW vs GOVERNED_WEIGHTED not in A05 | `measure_kind` in **both** `v2_semantic_operation_key` and `v2_dispatch_operation_key` | `test_v2_raw_and_weighted_are_distinct_operations` |
| condition_order missing from A05 | Ordered `condition_order` in both operation keys; v2 verifies it equals the owner's own semantic target order (short-name form) | `test_v2_condition_order_preserved_and_verified` |
| Consumer folded into expected_work_key (A04) | `v2_expected_work_key` has **no consumer**; `v2_consumer_obligation_key` is a **separate identity kind** | `test_v2_consumer_obligation_separate_from_expected_work` |
| Matching schema token is FALSE proof | `V2IssuerRecord` (issuer id + authority ref + signature + timestamp) and pre-run `V2CustodianRecord` (frontier digest + preimage hash + custodian timestamp) — not just a version string | `test_v2_issuer_and_custodian_records` |
| Expectations merely hash-equal afterward | Custodian record is frozen **before** execution; positive run asserts `frontier == custodian.frozen_frontier_digest` | recorder `frontier_matches_custodian: true` |
| Old A05 keys coerced or rehashed | `v2_to_a05_universe()` is a **translation** of independently declared v2 records; old A05 hashes are never recomputed or reinterpreted | `test_a05_interop_translation` |

Seven distinct identity kinds: documentary item, semantic operation, dispatch operation, expected work, consumer obligation, execution attempt, produced output.

## 3. Genuine positive run (actual measured output)

Same honest synthetic source-free fixture as A04 (4 respondents, items X/Y/O/R, 3 rows). **No raw SAV/DTA.**

- C11 release: `95de34f09fa9ae4aac6c6a3c73ea7ff9dff5ef18189bac940805f30126fce88c`
- Route B dependency root: `9db3c38159688863f816b52ea648234e8d23b76a4dbb47af1af8397f72bf9ba1`
- I03: **5 queries**, real `EmpiricalFact` states; I05: **1/1 covered** (`DISCOVERED_RESULT_SUPPORTED`)
- Batch: `COMPLETED`, `FULL_MANIFEST_COVERAGE`, **6/6 units**
- Reconciliation: **ok=True**, 6 expected keys, 6 job keys, 0 omitted, 0 extra
- Route B effects all false; custodian frontier matches pre-execution digest

**Command:** `PYTHONPATH=. python3 repro/a04s_evidence_recorder.py`

## 4. Hostile court — 16/16 must-fail detected, 3/3 controls pass

| # | hostile | observed |
|---|---|---|
| H1 | A-only, A+B expected | FAIL `EXPECTED_OPERATION_OMITTED` |
| H3 | missing J2 | FAIL `EXPECTED_OPERATION_OMITTED` |
| H4 | missing B | FAIL `EXPECTED_OPERATION_OMITTED` |
| H5 | unauthorized extra (undeclared yx query) | FAIL `UNAUTHORIZED_EXTRA_JOB` |
| H6 | same count, different keys | FAIL omission + extra |
| H7 | condition-order substitution | FAIL omission + extra |
| H8 | own-_dk co-topic fake joint | FAIL `CANDIDATE_OWN_DK_JOINT` |
| H9 | altered document version | FAIL `EXPECTED_OPERATION_OMITTED` |
| H10 | source identity mismatch | FAIL `SOURCE_IDENTITY_MISMATCH` (declared **and** constructed sides) |
| H11a | post-result laundering self-certified | **PASS — deliberately** |
| H11b | same execution vs frozen universe | FAIL `EXPECTED_OPERATION_OMITTED` |
| H12 | consumer omitted, all jobs present | FAIL `REQUIRED_CONSUMER_OMITTED` |
| H13 | held/denied/NA invisible | FAIL `HELD_OR_DENIED_WORK_NOT_VISIBLE` |
| H14/H15 | duplicate semantic job / multiplicity | FAIL at bind time |
| H16 | undeclared authority | FAIL at bind time |
| H17 | missing I05 | FAIL at bind time |
| P0/P1 | honest submission / stable reorder | **PASS** |

**H11a/H11b is the decisive pair:** the truncated manifest reconciled against itself shows zero omissions; the identical execution against the frozen universe shows 4. Self-certification is not no-drop evidence.

## 5. Old evidence untouched, old suites green

- A04 binder blob `7d8b3902…` verified identical to `cbe047cf`; test file untouched.
- A04's 41 tests: **41 passed** (run in the A04 worktree).
- A05 oracle: **18/18 `all_expectations_met: true`** (run in the A05 worktree).
- v2's 26 tests: **26 passed**. Widest targeted run (v2 + 5 owner suites): **103 passed**.
- Owner blobs: route_b `2385cd32…` == E18; discovery_exact `905f24d1…` == E19.

## 6. Two genuine defects found by running (v2 layer)

1. **I first violated my own commission** by editing A04's `_owner_target_order` to extract short names. Caught on review, **reverted** (blob verified), and the translation moved into the v2 layer where it belongs: v2 declarations use short names; A04 declarations are built with the owner's exact URN tokens; both reconcile paths use the same translation.
2. **Reconciliation compared key spaces.** v2 expected keys and A04 job keys are different hashes; comparing them directly can never detect extras. Fixed with an explicit `declared_to_a04_key` mapping computed with the identical URN translation, so omission is checked in v2 space and extras in A04 space.

## 7. Ceilings and holds

Source-free development only. No original-source read, no raw SAV/DTA (0 files), no all-35 eligibility, no model permission, no G0b/EE12, no operative publication, no canonical/PRE-MAIN mutation, no self-adoption, no merge. Consumers in the positive run are **modelled from real produced refs** (B02's licensed act remains: invoke a real C1/Field-Forge owner under existing authority). No real-source issuance is claimed; the v2 frontier is a development-grade successor, not an issued authority.

**Terminal:** `HQ280_PV3_A04S_SOURCEFREE_V2_EXPECTATION_BINDER_ORACLE_ACTUAL_JOIN_RETURNED_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`.