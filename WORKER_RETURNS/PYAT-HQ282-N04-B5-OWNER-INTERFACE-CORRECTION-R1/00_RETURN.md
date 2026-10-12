# PYAT HQ282 N04 — B5 checkpoint and interface correction

**TERMINAL:** `PYAT_HQ282_N04_B5_CHECKPOINT_INTERFACE_CORRECTION__SOURCEFREE_ONLY__NONISSUING`
**RESULT:** `PASS__BOUNDED_PRODUCT_REAL_OWNERS__15_TESTS_PASS__CHECKPOINT_DEFECT_REPRODUCED_AND_CORRECTED__METHOD_INVENTORY_DOCUMENTED__KNOWN_GAPS_PRESERVED`

**Branch:** `agent/rabochii-pyat-hq282-n04-b5-owner-interface-correction-r1`
**Sealed startup (verified before mutation):** `d3455cfeba4f436533395d58206b9959e84e648c`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).

## 1. What was built (new files only — zero owner edits)

| File | Role |
|---|---|
| `rawlsing_next/pre553_n04_b5_checkpoint_interface_correction.py` | checkpoint correction candidate (`PYAT_HQ282_N04_B5_CHECKPOINT_INTERFACE_CORRECTION@1.0.0`) |
| `rawlsing_next/repro/n04_corrected_overlay.py` | corrected B5 overlay that fixes the checkpoint path |
| `rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py` | 15 tests |

No accepted lifecycle/M2 owner is edited. The C02J verifier and overlay are not modified.

## 2. The concrete defect and correction

**Defect:** `verify_checkpoint_subject` calls `self._m2.subject_exact(subject.release_ref)`. The M2 `subject_exact` expects a `release_subject_ref` (the producer subject), not a `release_ref` (the release identity). This mismatch causes valid checkpoint restores to be falsely rejected with `RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered`.

**Correction:** Use `resolve_subject_exact(repository, release_ref)` which:
1. Resolves the release via `release_exact`
2. Extracts `release.release_subject_ref`
3. Calls `subject_exact` with the correct ref
4. Verifies producer-contract and subject-kind consistency

**Identity mismatch:** `release_ref != release.release_subject_ref`

## 3. Test results

| Test | Status | Notes |
|---|---|---|
| `test_corrected_verify_checkpoint_subject_resolves_valid_subject` | PASS | corrected call resolves valid subject |
| `test_original_defect_reproduced_and_correction_works` | PASS | defect reproduced, correction works |
| `test_valid_checkpoint_restores_without_overlay` | PASS | valid restore works without overlay |
| `test_valid_checkpoint_restores_with_overlay_and_corrected_verifier` | PASS | valid restore works with corrected overlay |
| `test_truncated_history_accepted_by_raw_executor_documents_gap` | PASS | known gap: raw executor accepts truncated history |
| `test_altered_state_accepted_by_raw_executor_documents_gap` | PASS | known gap: raw executor accepts altered state |
| `test_bad_hash_still_rejected` | PASS | bad hash correctly rejected |
| `test_incomplete_publication_still_rejected` | PASS | incomplete publication correctly rejected |
| `test_method_inventory_covers_b5_wrapped_methods` | PASS | inventory covers wrapped B5 methods |
| `test_method_inventory_identifies_unwrapped_methods` | PASS | inventory identifies unwrapped B5 methods |
| `test_method_inventory_identifies_m2_unwrapped_methods` | PASS | inventory identifies unwrapped M2 methods |
| `test_method_inventory_documents_checkpoint_defect` | PASS | inventory documents checkpoint defect |
| `test_effects_declare_no_rights` | PASS | all rights declared false |
| `test_module_import_surface_contains_no_forbidden_owner` | PASS | no forbidden imports |
| `test_no_raw_sav_dta` | PASS | no raw data |

**Combined suite:** 98 tests pass (15 N04 + 83 owner).

## 4. Method inventory summary

### B5 state-changing methods
- **WRAPPED** (8): `stage_release`, `stage_protocol`, `register_product`, `publish_product`, `record_recertification`, `select_current`, `declare_no_current`, `from_checkpoint`
- **UNWRAPPED** (9): `supersede_current`, `withdraw_product`, `declare_invalidation`, `record_rebuild_eligibility`, `link_rebuild`, `record_cache_materialized`, `record_cache_dropped`, `attest_gc_eligibility`, `record_payload_gc`
- **PARTIAL** (2): `declare_no_current` (only checked if `subject_release_ref` supplied), `record_recertification` (registry lookup only)

### M2 state-changing methods
- **WRAPPED** (2): `register_producer_subject`, `constitute_release`
- **UNWRAPPED** (8): `M2Repository.register_subject`, `M2Repository.register_closure`, `M2Repository.register_release`, `M2Repository.register_representation`, `M2Repository.register_binding`, `constitute_closure`, `register_representation`, `publish_binding`

## 5. Known gaps (not new defects)

1. **Truncated history accepted by raw executor**: The checkpoint implementation restores saved state mappings rather than replaying event transitions to derive and compare state.
2. **Altered state accepted by raw executor**: Same root cause as above.
3. **Unwrapped B5/M2 methods**: 9 B5 + 8 M2 state-changing methods are not covered by the C02J overlay.
4. **`declare_no_current` partial coverage**: Only checked if `subject_release_ref` supplied.
5. **`record_recertification` partial coverage**: Registry lookup only, no event/authority check.

## 6. Scope and boundaries

- Source-free: 0 .sav/.dta; no respondent row
- No G0b/model-use/Field-Forge/temporal/CURRENT/V3 right
- No canonical/accepted-owner edit
- No self-adoption
- No production publication
- No external authority issuance
