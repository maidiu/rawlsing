# Hostile Test Matrix

| Requirement | Evidence | Result |
|---|---|---|
| wrong runtime catalog identity fails closed | `test_i03_successor_wrong_runtime_catalog_identity_fails_closed` | PASS |
| same query/snapshot/universe/family/successor under another catalog cannot consume successor | `test_i03_same_scope_under_another_catalog_cannot_consume_successor` | PASS |
| absent runtime catalog identity fails closed | `test_i03_successor_absent_runtime_catalog_identity_fails_closed` | PASS |
| exact LiTS catalog `5983d7...` passes | `test_i03_exact_accepted_lits_catalog_and_parent_operation_pass` and full 60-query successor gate test | PASS |
| parent operation absent from historical snapshot fails closed | `test_i03_parent_operation_absent_from_historical_snapshot_fails_closed` | PASS |
| different governed parent operation does not satisfy contract | `test_i03_different_governed_parent_operation_does_not_satisfy_contract` | PASS |
| exact parent operation passes | `test_i03_exact_parent_operation_passes_as_distinct_jurisdiction` | PASS |
| contract catalog tamper without recomputing authority identity fails | tamper loop in `test_lits_i03_successor_rejects_unadopted_or_tampered_record` | PASS |
| contract parent-operation tamper without recomputing authority identity fails | same tamper loop | PASS |
| wrong parent authority still rejects | `test_i03_preexisting_exact_successor_dimensions_still_fail_closed` | PASS |
| wrong runtime snapshot hash still rejects | same | PASS |
| wrong successor operation still rejects | same | PASS |
| wrong query still rejects | same | PASS |
| wrong universe still rejects | same | PASS |
| wrong object family still rejects | same | PASS |
| WVS7 does not bind LiTS successor runtime context | `test_wvs7_functions_bind_no_lits_successor_runtime_context` | PASS |
| absent runtime context retains predecessor behavior | `test_i03_absent_runtime_context_retains_predecessor_failure` | PASS |
| frozen LiTS runtime catalog unchanged | `test_lits_frozen_catalog_is_unchanged_and_exact_successor_closes_i03_gate` | PASS |

## Qualification receipts

### Focused court

Run `35790373170`, job `106957146667`:

- protocol court: `20 passed in 0.11s`;
- jurisdiction/regression court: `149 passed, 28 subtests passed in 80.67s`.

Exact command:

```bash
python -m pytest -q \
  rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py \
  rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
  rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py \
  rawlsing_next/tests/test_fiabc_final_preflight_fanin.py \
  rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py \
  rawlsing_next/tests/test_fiabc_succession_preflight.py
```

### Broad source-free court

Run `35790682199`, job `106958138269`:

- protocol court: `20 passed in 0.15s`;
- broad regression court: `251 passed, 28 subtests passed in 85.00s`.

Exact command:

```bash
python -m pytest -q \
  rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py \
  rawlsing_next/tests/test_fiabc_final_preflight_fanin.py \
  rawlsing_next/tests/test_fiabc_lits_a_absent_root_current_court.py \
  rawlsing_next/tests/test_fiabc_post_r1j_root_source_independent_courts.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py \
  rawlsing_next/tests/test_fiabc_t6_live_r35_convergence.py \
  rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py \
  rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py \
  rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py \
  rawlsing_next/tests/test_fiabc_t4_live_accounting.py \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py \
  rawlsing_next/tests/test_fiabc_succession_preflight.py \
  rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py \
  rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
  rawlsing_next/tests/test_pre553_empirical_objects_authority.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
```

The broad court includes the repository's final-preflight source-free test set, plus the new LiTS I03 jurisdiction suite. It does not open raw survey bytes or execute Candidate A/B/C, measured P2X, P3, or source-backed LiTS I05.
