# PYAT HQ282 N04R — Independent tests

## Test design

Reviewer-owned tests independently verify the checkpoint correction without borrowing the author's expected outcomes. Tests cover:

1. **Normal positive**: Valid checkpoint restoration (published and current states)
2. **Negative restoration**: Altered publication state, bad hash, incomplete publication
3. **Reference correctness**: `subject_exact` rejects `release_ref`; `resolve_subject_exact` accepts `release_ref`; rejects unrelated subject
4. **Method reachability**: `withdraw_product`, `declare_invalidation`, `supersede_current` reachable without verifier
5. **Scope and privacy**: No production authority, no forbidden imports, no raw data

## Commands and results

### Independent reviewer tests

```bash
PYTHONPATH=. python3 -m pytest WORKER_RETURNS/PYAT-HQ282-N04R-INDEPENDENT-CHECKPOINT-REVIEW-R1/repro/test_n04r_independent_review.py -v
```

**Exit:** 0
**Result:** 14 passed in 0.17s

| Test | Status |
|---|---|
| `test_reviewer_valid_checkpoint_restores_correctly` | PASS |
| `test_reviewer_valid_current_checkpoint_restores_correctly` | PASS |
| `test_reviewer_altered_publication_state_accepted_by_raw` | PASS (documents known gap) |
| `test_reviewer_bad_hash_rejected` | PASS |
| `test_reviewer_incomplete_publication_rejected` | PASS |
| `test_reviewer_subject_exact_rejects_release_ref` | PASS |
| `test_reviewer_resolve_subject_exact_accepts_release_ref` | PASS |
| `test_reviewer_resolve_subject_exact_rejects_unrelated_subject` | PASS |
| `test_reviewer_unwrapped_withdrawal_succeeds_without_verifier` | PASS |
| `test_reviewer_unwrapped_invalidation_succeeds_without_verifier` | PASS |
| `test_reviewer_unwrapped_supersede_succeeds_without_verifier` | PASS |
| `test_reviewer_no_production_authority` | PASS |
| `test_reviewer_no_forbidden_imports` | PASS |
| `test_reviewer_no_raw_data` | PASS |

### N04 candidate tests

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py -v
```

**Exit:** 0
**Result:** 15 passed in 0.19s

### Owner tests

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py -q
```

**Exit:** 0
**Result:** 83 passed in 0.46s

### Combined suite

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py WORKER_RETURNS/PYAT-HQ282-N04R-INDEPENDENT-CHECKPOINT-REVIEW-R1/repro/test_n04r_independent_review.py -q
```

**Exit:** 0
**Result:** 112 passed in 0.76s

## Differences from historical P02R (41 PASS / 14 FAIL / 3 UNTESTED)

The P02R review found 14 failures and 3 untested cases. The N04 correction addresses the checkpoint restoration defect (the primary failure). The remaining P02R failures (unwrapped methods, partial coverage) are documented as known gaps, not repaired by the correction. The independent reviewer tests confirm these gaps remain open.

## Important note

"Test documents known failure" is not proof the underlying failure is repaired. The tests `test_reviewer_altered_publication_state_accepted_by_raw` and `test_reviewer_unwrapped_*` pass by documenting existing behavior, not by fixing defects.
