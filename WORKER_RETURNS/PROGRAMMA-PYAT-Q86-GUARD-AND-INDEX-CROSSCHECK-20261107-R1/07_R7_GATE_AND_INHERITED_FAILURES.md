# R7 GATE AND INHERITED FAILURES

## R7 gate
- PR: `https://github.com/maidiu/rawlsing/pull/770`
- Exact head: `392de04e86202a2a80361a91808ef06fd34c1cc8`
- State: OPEN; latest reviews: none; review requests: none; `reviewDecision` empty.
- CI: `governed-court` failed on three tests; `canonical-tree` passed.
- The three failures are current protected-base/packaging assertions, not files changed by R7:
  - `test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope`
  - `test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state`
  - `test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law`
- R7 independent exact-head acceptance is therefore **PENDING**. This R8 PR does not claim it is satisfied and must not be merged on the basis of R7.

## Inherited focused failures
The GT34/A2 group was run on both the untouched R7 base and the R8 branch:

- R7 base: `1 failed, 12 passed, 3 errors in 172.41s`
- R8 branch: `1 failed, 12 passed, 3 errors in 173.61s`

Identical failure:
`test_wave1_gt12_a2_real_gt1.py::test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay`
`GT12BI03BindingError: validated projection domain omits an observed exact source-native response state`

Identical errors:
- `test_gt34_q2_same_source_c11_release.py::test_q2_builds_one_validated_same_source_release_without_identity_collapse`
- `test_gt34_q2_same_source_c11_release.py::test_q2_reuses_exact_objects_from_accepted_q86_claim_scoped_release`
- `test_gt34_q2_same_source_c11_release.py::test_q2_release_identity_is_deterministic_and_bounded`

These are inherited at the protected source/test cut and are not attributed to the R8 guard.

## R8 PR CI
- PR #774, `canonical-tree`: PASS.
- PR #774, `governed-court`: FAIL in the full court with the same three inherited packaging assertions: `3 failed, 144 passed in 48.93s`.
- The changed-test proof gate is satisfied by the two proof sidecars and did not report RED.
- No R8 guard test or sourcefree regression failed in CI.
