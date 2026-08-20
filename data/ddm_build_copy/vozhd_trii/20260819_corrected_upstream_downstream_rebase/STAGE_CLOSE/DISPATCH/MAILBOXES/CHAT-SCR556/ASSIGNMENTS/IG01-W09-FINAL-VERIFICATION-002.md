# IG01-W09-FINAL-VERIFICATION-002 — FINAL BYTE-EXACT TEST EXECUTION COURT

**Worker #9** — `CHAT-SCR556`  
**Most recent submitting agent:** `IG_M3_SIDELINE_IMPLEMENTATION`  
**New agent:** `IG_FINAL_BYTE_EXACT_VERIFICATION`  
**Worker class:** `INSPECTORATE`  
**Repository:** `maidiu/rawlsing`  
**Mission branch:** `agent/vozhd-trii-ig-final-verification`  
**EXACT BRANCH BASE:** `b66e282f4185ece6682723bc5e53c1a23534d5f0`  
**Authority:** verification-only; no implementation or semantic authority.

## Mission

Close the sole outstanding verification receipt for final-integration candidate `b66e282f4185ece6682723bc5e53c1a23534d5f0`.

The integration candidate already returned `IG_INTEGRATION_BOUNDED_EXACT_BINDING_FAILURE` solely because its environment could not perform a fresh byte-exact rerun of every unchanged accepted package-local test. No semantic violation/conflict was found, H01–H20 plus P01–P12 passed, and the exact seven-path integration diff is already frozen as candidate evidence.

Your job is ONLY to execute the exact accepted tests from the exact final candidate tree and return a machine-verifiable receipt. Do not redesign, repair, refactor, reformat, or modify runtime/tests.

## Read first

From exact base `b66e282f4185ece6682723bc5e53c1a23534d5f0`, read:

- `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_INTEGRATION_FINAL/RESULT.json`
- `.../IG_INTEGRATION_FINAL/FINAL_TREE_BINDINGS.json`
- `.../IG_INTEGRATION_FINAL/HOSTILE_TEST_RESULTS.json`
- `rawlsing_next/tests/test_whole_machine_integration.py`

Treat accepted M1–M6/render/PSEPF runtime/test blobs in `FINAL_TREE_BINDINGS.json` as immutable pins.

## Branch precondition

Before any write:

1. verify branch HEAD == `b66e282f4185ece6682723bc5e53c1a23534d5f0`;
2. verify working tree clean;
3. verify all 17 pinned `rawlsing_next` paths/blobs in `FINAL_TREE_BINDINGS.json` exactly match the base tree.

If any mismatch exists, return `IG_FINAL_VERIFICATION_EXACT_BINDING_FAILURE` and make no semantic/runtime repair.

## Required execution

Run exactly these accepted test files from the exact branch tree, with repository root on `PYTHONPATH`:

1. `rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`
2. `rawlsing_next/tests/test_m2_v555_atomic_route.py`
3. `rawlsing_next/tests/test_m3_v556_higher_order_structural.py`
4. `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`
5. `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`
6. `rawlsing_next/tests/test_m6_actor_safe_expression.py`
7. `rawlsing_next/tests/test_psepf_zero_positive_guard.py`
8. `rawlsing_next/tests/test_render_bounded_expression.py`
9. `rawlsing_next/tests/test_whole_machine_integration.py`

Preferred command:

```bash
PYTHONPATH=. pytest -q \
  rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py \
  rawlsing_next/tests/test_m2_v555_atomic_route.py \
  rawlsing_next/tests/test_m3_v556_higher_order_structural.py \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py \
  rawlsing_next/tests/test_m6_actor_safe_expression.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_render_bounded_expression.py \
  rawlsing_next/tests/test_whole_machine_integration.py
```

Record exact command, Python version, pytest version, working-tree status, test counts, elapsed time, and stdout/stderr summary.

## Write scope

Write ONLY:

- `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_FINAL_VERIFICATION/RESULT.md`
- `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_FINAL_VERIFICATION/RESULT.json`
- `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_FINAL_VERIFICATION/TEST_EXECUTION_RECEIPT.json`

No `rawlsing_next/**` write is permitted. No legacy runtime write. No semantic-contract write. No dispatch write.

## Adjudication law

- If all exact test files pass on the exact candidate tree and all pinned blobs remain unchanged: return `IG_FINAL_VERIFICATION_COMPLETE__READY_FOR_FINAL_RECLOSURE_ADJUDICATION`.
- If any test fails: return `IG_FINAL_VERIFICATION_TEST_FAILURE` with exact failing node IDs/traces; do not repair.
- If exact base/blob binding fails: return `IG_FINAL_VERIFICATION_EXACT_BINDING_FAILURE`.
- If the environment itself cannot execute the exact tree: return `IG_FINAL_VERIFICATION_ENVIRONMENT_BLOCKED` with the exact missing capability. Do not substitute reconstructed files or partial execution.

Positive SPDM remains `BLOCKED_NAMED_AUTHORITY_REQUIRED`. Deployment, cutover, retirement, and legacy mutation remain forbidden.
