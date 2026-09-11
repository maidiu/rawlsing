# WITNESS CURRENTNESS FOCUSED PROOFS R1

Focused test identity:
`rawlsing_next/tests/test_sdtf_r4_witness_currentness.py`

Tested Git blob identity:
`e3ccedf6ffd694aa01728b8282582e5229b6bc4f`

## Proof cases

1. `test_01_current_k1_positive_proof_is_proven_and_active_remains_umbrella_descriptor`
   - current K1 positive proof succeeds;
   - `ACTIVE` remains an umbrella descriptor and does not convert K1 to K4.
2. `test_02_replaced_type_authority_stales_proof_before_use`
   - type-authority replacement becomes `STALE_REQUIRES_REPLAY` before proof use.
3. `test_03_revoked_witness_fails_closed_and_never_becomes_negative_by_revocation_alone`
   - revoked witness fails closed for positive and negative assertions;
   - revocation alone does not manufacture negative truth.
4. `test_04_unknown_authority_currentness_is_unknown_not_proven`
   - unproved authority currentness returns `UNKNOWN_NOT_PROVEN`.
5. `test_05_k4_path_a_current_then_invalidating_replay_dependency_stales_proof_visible_witness`
   - current Path A proves;
   - a declared invalidating contact-authority replay dependency replacement makes the proof-visible witness stale.
6. `test_06_k4_path_b_survives_unrelated_replay_churn_but_not_owner_source_revision`
   - unrelated replay churn is not inferred as invalidating;
   - owner/source authority revision invalidates Path B.
7. `test_07_k4_path_b_requires_overlap_complete_closure_coverage_and_no_defeating_fact`
   - four parameterized fail-closed cases cover no overlap, incomplete closure coverage, defeating closing fact, and unknown closure coverage.
8. `test_08_old_establishment_event_plus_silence_cannot_prove_k4_path_b`
   - historical establishment plus silence cannot become current K4 support.
9. `test_09_negative_truth_requires_explicit_negative_proof_not_failed_positive_proof`
   - failed positive proof does not establish negative truth;
   - explicit negative proof can establish a negative assertion.
10. `test_10_axes_remain_orthogonal_for_projected_historical_request`
    - assertion kind, fact currentness, and modality remain independent.
11. `test_11_adapter_owner_or_type_mismatch_fails_closed_without_semantic_inference`
    - owner/type mismatch fails closed without cross-family inference.
12. `test_12_current_check_must_bind_expected_and_observed_exactly`
    - a check labeled current cannot pass when expected and observed authority refs differ.

Pytest expands the parameterized Path-B proof into four cases, yielding 15 executed focused cases total.
