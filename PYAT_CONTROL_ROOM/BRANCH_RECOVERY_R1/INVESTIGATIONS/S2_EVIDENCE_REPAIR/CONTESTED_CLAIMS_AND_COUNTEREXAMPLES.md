# S2 EVIDENCE-REGRADE — CONTESTED CLAIMS AND COUNTEREXAMPLES

**Immutable original return:** `ab303ee446c87beca32dc2c322704f6cf0dc7b79`  
**Corrected evidence law:** `f50651a2bb0758e9fe6d6a2852441dcc782344be`  
**PRE-MAIN baseline:** `750548ddbb9b4392a16ce93097b856f349e16182`  
**Actual PRE-MAIN head at return:** `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3` (11 files changed; 0 `rawlsing_next/` files)  
**Regrade branch:** `agent/pyat-845-s2-evidence-regrade-20261030-r1`

This is an issue-specific delta, not a rewrite of the original S2 return. Every original `function_id` is retained in `FUNCTION_GRADE_CORRECTIONS.jsonl`; every frozen S2 branch/tip is retained in `BRANCH_RECONCILIATION.jsonl`.

---

## 1. False promotion: S2's 10 `SUPERSEDED_BETTER` labels

S2 assigned `SUPERSEDED_BETTER` where the current same-path body was merely larger. The evidence law requires (a) same function, (b) reproduced historical positive/fault-negative on the current receiver, and (c) demonstrated improvement. None of the 10 rows contains that proof.

| Original ID | Path / symbol | Corrected disposition | Counterexample / missing proof |
|---|---|---|---|
| F0143 | `pre553_learned_product_lifecycle.py::LearnedProductLifecycleExecutor.current_selection_receipt_ref` | `DIFFERENT__COMPARISON_REQUIRED__CURRENT_IMPL_UNPROVEN__BRANCH_TESTS_FAILED` | Branch receipts report 194 failed / 1690 passed / 30 skipped; no function-scoped current comparison. |
| F0153 | `...::resolve_current_as_of` | same | same branch failure history; no current behavioral receipt. |
| F0142 | `...::resolve_selection_exact` | same | same. |
| F0159 | `pre553_learned_product_release.py::M2Repository.binding_exact` | same | same. |
| F0158 | `...::M2Repository.release_exact` | same | same. |
| F0206 | `pre553_native_workload_binding.py::build_projection_catalog` | `DIFFERENT__COMPARISON_REQUIRED__B49_AUTHOR_RECEIPT_DOES_NOT_PROVE_CURRENT_SUPERIORITY` | B49 author receipt is 29/29 new + 41/41 regression + proof witness RED on severance, but it does not compare the current shorter same-path implementation. |
| F0207 | `...::build_test_only_workload` | same | same. |
| F0215 | `pre553_physical_decoder.py::PhysicalSourceIncidence.iter_batches` | `DEFECTIVE_BLOCK__REPRODUCED_CONSUMED_BYTE_CUSTODY_DEFECT` | R56-R04BYTEV independently reproduced a consumed-byte custody defect at this function; post-addition 2 failed / 17 passed; the old source identity can be attached to C11/I03 facts built from replacement bytes. S2's “superseded” claim is false at the claimed scope. |
| F0214 | `pre553_source_native_preimage_adapter.py::materialize_native_preimages` | `DIFFERENT__COMPARISON_REQUIRED__SOURCE_NATIVE_RECEIPT_REVIEW_REVISE` | Historical receipt reports 2 failed / 37 passed; no current receiver comparison. |
| F0208 | same symbol | same | No test receipt; no behavioral comparison. |

**Future promotion condition:** reproduce the exact historical positive and fault-negative assertion on the current receiving code and show a relevant correctness/safety/custody improvement, or retain `DIFFERENT__COMPARISON_REQUIRED`.

---

## 2. False blanket hold: S2's 67 `UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY`

S2 applied one source-authority hold to sourcefree security, lifecycle and adapter code. The corrected split is:

| Corrected class | Count |
|---|---:|
| `SOURCEFREE_RETEST_REQUIRED__BRANCH_TESTS_FAILED_REVIEW_REVISE` | 26 |
| `SOURCEFREE_INTEGRATION_CANDIDATE__EXACT_HOLDS__NO_ISSUER` | 10 |
| `SCIENCE_HOLD__SCIENTIFIC_METHOD_OR_ESTIMAND_UNISSUED` | 9 |
| `SOURCE_AUTHORITY_HOLD__SOURCE_NATIVE_OPERATION` | 6 |
| `SOURCE_AUTHORITY_HOLD__SOURCE_NATIVE_ROLE_QUERY__REVIEW_REVISE` | 5 |
| `EVIDENCE_ONLY__NOT_PRODUCTION` | 4 |
| `WORLD_ACTOR_HOLD__N9_N10W_N11_N12_NOT_GRANTED` | 3 |
| `SOURCEFREE_INTEGRATION_CANDIDATE__AUTHOR_RECEIPT_29_OF_29_AND_41_OF_41` | 2 |
| `SOURCEFREE_INTEGRATION_CANDIDATE__TEST_ONLY__WORLD_ACTOR_HOLD` | 1 |
| `INSUFFICIENT_EVIDENCE__NAMED_MISSING_EVIDENCE` | 1 |

### Named counterexamples

- **B5 C02J / C02R / C02HR (13 functions):** sourcefree producer-trust code. The return reports 0 failed / 2100 passed in one carrier, but six exact holds remain: ceiling, tautology, replay, authority, event attribution, and no competent issuer. The code is not source-native and must not be blanket-held under “source authority”. Corrected: `SOURCEFREE_INTEGRATION_CANDIDATE__EXACT_HOLDS__NO_ISSUER`.
- **B49 adapter (`pre553_inherited_source_rules`, `pre553_native_workload_binding`):** sourcefree adapter with 29/29 new tests, 41/41 regression and a proof-witness RED on severance. T3 scientific method and T5 live source right remain unissued; adoption is HQ-held, not source-read-blocked. Corrected: sourcefree candidate with explicit T3/T5 holds.
- **S06 trusted release (`s06_trusted_release_replay.py`):** sourcefree lifecycle. Historical receipt reports 20 failed / 1 passed. This is a test/review-revise problem, not an original-source permission problem.
- **Learned-product lifecycle/release:** sourcefree lifecycle. Branch receipts report 194 failed / 1690 passed / 30 skipped (and 40 failed / 2 passed in another carrier). The correct status is `REVIEW_REVISE`/`SOURCEFREE_RETEST_REQUIRED`, not source-authority hold.
- **Batch durable checkpoint / governed batch integration:** sourcefree lifecycle; unresolved imports and failed/errors receipts; sourcefree retest is allowed after the import/interface gap is resolved.

**Future promotion condition:** for sourcefree code, resolve the named interface/test defect and run a current-receiver positive plus fault-negative court. For source-native/science/world/actor operations, name the competent issuer, operation, target universe and rule; no blanket source hold is needed to block unrelated sourcefree retests.

---

## 3. False adaptation frame: S2's 22 `UNIQUE_USEFUL_NEEDS_ADAPTATION`

S2 treated all 22 as import/interface adaptations. The corrected split:

| Corrected class | Count |
|---|---:|
| `SOURCEFREE_RETEST_REQUIRED__BRANCH_TESTS_FAILED_REVIEW_REVISE` | 10 |
| `WORLD_ACTOR_HOLD__N9_N10W_N11_N12_NOT_GRANTED` | 6 |
| `SOURCE_AUTHORITY_HOLD__SOURCE_NATIVE_OPERATION` | 4 |
| `EVIDENCE_ONLY__NOT_PRODUCTION` | 1 |
| `SOURCEFREE_INTEGRATION_CANDIDATE__HISTORICAL_RECEIPT_ONLY` | 1 |

Examples:
- F0066–F0069 governed batch checkpoint: sourcefree, unresolved `pre553_batch_durable_checkpoint_candidate`; sourcefree retest plus interface resolution, not source authority.
- F0162–F0166/F0175 I01 world lifecycle: sourcefree code, but N9 world/actor adoption requires an ungranted world authority; sourcefree tests remain allowed.
- F0075–F0080/F0090 original workload v2: 288 failed / 1859 passed / 54 skipped branch receipt; review-revise, not source permission.
- F0054 is a checkpoint-defect demonstration, not production; corrected to `EVIDENCE_ONLY__NOT_PRODUCTION`.

---

## 4. S2's 105 `EVIDENCE_UNKNOWN`: explicit reasons

The original label hid different causes. Corrected causes:

| Cause | Count |
|---|---:|
| Non-production evidence/test/witness path | 51 |
| Current same-path/same-symbol implementation differs; behavior unproven | 40 |
| No current function; path absent | 14 |

Of the 105, historical merit is `NOT_PRODUCT_CODE` 51, `REVIEW_REVISE` 47, `POSITIVE_AUTHOR_ONLY` 5, `INSUFFICIENT` 2. `FUNCTION_GRADE_CORRECTIONS.jsonl` gives the targeted missing evidence per row. The largest single cause is that S2 counted repro courts, overlays, seam witnesses and the HQ297 test-only documentary reader as production functions; they are now `EVIDENCE_ONLY__NOT_PRODUCTION`.

---

## 5. The 14 exact-current rows were not adopted

F0199–F0203, F0048–F0051, F0209–F0213 are exact current code/AST rows. Corrected disposition: `NO_ACTION_CODE_PRESENT__CURRENT_CODE_PRESENT__NOT_ADOPTION_EVIDENCE`; adoption: `HISTORICAL_ACCEPTANCE_ONLY`. Current code presence is not current production acceptance, does not erase negative branch testimony, and does not establish source/science/world/actor permission.

---

## 6. The 106 evidence-only branches are not trash

S2 did not call these trash, but its function-only view risked losing their negative findings. `BRANCH_RECONCILIATION.jsonl` preserves each branch/tip, return roots, tokens, test counts and snippet as reviewer testimony. Examples:

- `agent/rabochii-pyat-hq281-c02j-mandatory-b5-owner-trust-r1`: exact B5 holds, no issuer, test-only overlay.
- `agent/rabochii-pyat-r3-hq284-s03f-f6-domain-leakage-repair-r1`: F6 scientific-method review with RED/REVISE testimony.
- `agent/rabochii-pyat-r3-hq295-v2k-original-identity-successor-r1`: original-E/B02 court; 26 failed / 111 passed; source-native identity hold.
- `agent/reviewer-pyat-hq280-pv3-d02zr-legal-rule-runtime-hostile-r1`: D02ZR hostile review; 33/33 sourcefree tests pass, nonissuing.

Evidence-only branches are preserved as `EVIDENCE_ONLY__RETURN_OR_REVIEW_PRESERVED`; they are not production, not trash, and not an implementation.

---

## 7. `agent/reviewer-d02zr-ee66e2b` — resolved, not invented

The roster branch `agent/reviewer-d02zr-ee66e2b` points to `506381ac0fb68086e8028f916e935c04b9b5877d`. That commit is the later pycache-cleanup commit of the D02ZR hostile reviewer branch `agent/reviewer-pyat-hq280-pv3-d02zr-legal-rule-runtime-hostile-r1`, whose original tip is `ee66e2b8435d281399e8ce1f8feeeb6927971254`. The direct D02ZR return at `506381ac…` reports 33/33 sourcefree tests passing (6 candidate + 27 hostile), 35 fixture cases, and a **nonissuing** terminal: no issued legal fact, no competent issuer, no N5/N6/N9, no G0b, no current law. The branch is evidence-only; no production function, no source authority granted, no final scientific verdict invented.

---

## 8. Actual negative counterexamples retained

- **R56 consumed-byte custody:** independently reproduced at `PhysicalSourceIncidence.iter_batches`; post-addition 2 failed / 17 passed; source identity could be attached to replacement-byte C11/I03 facts. This blocks any “superseded better” or ready claim.
- **HQ297 N9 two-field reader:** 27/27 test-only documentary assertions, not a genuine repo callable; first field issuance and real OC05 values read remain held.
- **HQ297 V2R role query:** 267 passed / 27 failed; source-native first-original-E/B02 court; not adopted.
- **S04 temporal policy:** 89 failed / 186 passed / 18 skipped in the relevant carrier; scientific interpolation/backoff policy is not ready.
- **S06 trusted release:** 20 failed / 1 passed; replay/checkpoint invalidation not ready.
- **Original workload v2/verifier:** 288 failed / 1859 passed / 54 skipped; review-revise, not source authority.
- **Learned-product lifecycle/release:** 194 failed / 1690 passed / 30 skipped (and 40 failed / 2 passed in another carrier); review-revise.
- **C1 immutable release binding:** candidate authored but unexecuted; 15 named tests not run; no operative issuer; G0b held.
- **B5 C02J exact holds:** ceiling, tautology, replay, authority and event-attribution holds; no competent issuer.
- **B49:** 29/29 + 41/41 + proof witness RED on severance; T3/T5 unissued; adoption hold.
- **Postastra PE:** 21/21 sourcefree tests, but test-only; no science, no N9 current, no V3 wake, no adoption.

---

## 9. Required future promotion gates

1. Exact current-receiver SHA and function-scoped positive test.
2. Exact current-receiver fault-negative test or independent reviewer counterexample.
3. No unresolved import/interface gap.
4. Named permission/issuer/operation only where the operation actually requires it; sourcefree tests do not require a source grant.
5. Separate science, world, actor and N11/N12 decisions.
6. Independent hostile review at the exact regrade return SHA; no author self-approval.
7. No PRE-MAIN merge or original-return rewrite.
