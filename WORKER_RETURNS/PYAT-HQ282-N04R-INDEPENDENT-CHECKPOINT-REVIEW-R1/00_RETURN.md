# PYAT HQ282 N04R — Independent checkpoint review

**TERMINAL:** `PYAT_HQ282_N04R_INDEPENDENT_CHECKPOINT_REVIEW__SOURCEFREE_ONLY__NONISSUING`
**RESULT:** `PASS__INDEPENDENT_VALIDATION_OF_BOUNDED_CHECKPOINT_CORRECTION__14_REVIEWER_TESTS_PASS__112_COMBINED_PASS__KNOWN_GAPS_CONFIRMED__DS_STORE_CLEANUP_REQUIRED`

**Branch:** `agent/reviewer-pyat-hq282-n04r-checkpoint-independent-finaltree-r1`
**Sealed startup (verified before mutation):** `f6e20f14e73ea2bb13b65b91eea2f737df916e0e`
**N04 frozen tree under review:** `b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2`
**N04 start:** `d3455cfeba4f436533395d58206b9959e84e648c`

## Disposition

**Independent validation** of the bounded source-free checkpoint correction. The correction is technically correct: `resolve_subject_exact(repository, release_ref)` properly resolves the release first, extracts `release.release_subject_ref`, then calls `subject_exact` with the correct ref. The original call `subject_exact(subject.release_ref)` is confirmed defective (passes a `release_ref` where a `release_subject_ref` is expected).

**Not approved:** B5 publication, external producer identity, event/revocation issuers, G0b, N9, or V3.

## Test results

| Suite | Tests | Result |
|---|---|---|
| N04 candidate | 15 | ALL PASS |
| Owner tests | 83 | ALL PASS |
| Independent reviewer | 14 | ALL PASS |
| **Combined** | **112** | **ALL PASS** |

## What passed

1. Valid checkpoint restoration (published and current states) through the corrected path
2. `subject_exact` correctly rejects a `release_ref` (not a subject ref)
3. `resolve_subject_exact` correctly resolves through the release
4. `resolve_subject_exact` rejects an unrelated subject
5. Bad hash and incomplete publication correctly rejected
6. Unwrapped methods (`withdraw_product`, `declare_invalidation`, `supersede_current`) reachable without verifier
7. No production authority, no forbidden imports, no raw data

## What remains untested / known gaps

1. **Altered publication state accepted by raw executor** (known gap): The checkpoint implementation restores saved state mappings without replaying event transitions to derive and compare state. This is a pre-existing owner defect, not introduced by the correction.
2. **Truncated history accepted by raw executor** (known gap): Same root cause.
3. **Unwrapped B5/M2 methods**: 9 B5 + 8 M2 state-changing methods are not covered by the C02J overlay. Representative examples (`withdraw_product`, `declare_invalidation`, `supersede_current`) confirmed reachable without verifier.
4. **`declare_no_current` partial coverage**: Only checked if `subject_release_ref` supplied.
5. **`record_recertification` partial coverage**: Registry lookup only, no event/authority check.

## Git provenance / cleanup requirement

The N04 diff includes:
- **New N04 code** (3 files): `pre553_n04_b5_checkpoint_interface_correction.py`, `n04_corrected_overlay.py`, `test_pre553_n04_b5_checkpoint_interface_correction.py`
- **New N04 return packet** (8 files): `WORKER_RETURNS/PYAT-HQ282-N04-B5-OWNER-INTERFACE-CORRECTION-R1/`
- **Copied historical C02J return tree** (11 files): `WORKER_RETURNS/PYAT-HQ281-C02J-REAL-B5-M2-PRODUCER-TRUST-R1/`
- **Copied historical P02R return tree** (9 files): `WORKER_RETURNS/PYAT-HQ282-P02R-C02J-INDEPENDENT-INTERFACE-VERIFICATION-R1/`
- **Copied historical C02J code** (3 files): `pre553_b5_owner_held_verifier_candidate.py`, `c02j_mandatory_overlay.py`, `c02j_owner_court.py`
- **macOS metadata** (1 file): `.DS_Store` in `WORKER_RETURNS/PYAT-HQ282-N04-B5-OWNER-INTERFACE-CORRECTION-R1/`

**Cleanup recommendation:** Remove `.DS_Store` from the N04 branch (or add to `.gitignore`). The copied historical trees are acceptable for provenance but should be clearly labeled as copied history, not new N04 work.

## Reference correctness

The defect is confirmed by direct inspection of M2 source:
- `subject_exact(ref)` does `_exact(ref, "release_subject_ref")` and looks up `self._subjects`
- `release_exact(ref)` does `_exact(ref, "release_ref")` and looks up `self._releases`
- `resolve_subject_exact(repository, release_ref)` correctly chains: `release_exact` → `release.release_subject_ref` → `subject_exact`
