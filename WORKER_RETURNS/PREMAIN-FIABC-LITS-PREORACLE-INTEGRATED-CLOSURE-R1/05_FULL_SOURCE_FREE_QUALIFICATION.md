# Full Source-Free Qualification

## Focused court

GitHub Actions:
- run `35826661112`
- job `107069779873`
- CPython 3.11.16
- protocol: `20 passed in 0.08s`
- governed focused court: `80 passed in 39.12s`

Exact focused pytest targets:

```
rawlsing_next/tests/test_fiabc_lits_astra_substantive_parity.py
rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py
rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py
```

## Broad court

GitHub Actions:
- run `35826798791`
- job `107070206829`
- CPython 3.11.16
- protocol: `20 passed in 0.10s`
- governed broad court: `309 passed, 28 subtests passed in 90.19s`

Exact broad pytest targets:

```
rawlsing_next/tests/test_fiabc_lits_astra_substantive_parity.py
rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py
rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py
rawlsing_next/tests/test_fiabc_final_preflight_fanin.py
rawlsing_next/tests/test_fiabc_lits_a_absent_root_current_court.py
rawlsing_next/tests/test_fiabc_post_r1j_root_source_independent_courts.py
rawlsing_next/tests/test_r35_i01_physical_metadata.py
rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py
rawlsing_next/tests/test_fiabc_t6_live_r35_convergence.py
rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py
rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py
rawlsing_next/tests/test_fiabc_t4_live_accounting.py
rawlsing_next/tests/test_pre553_independent_parity_oracle.py
rawlsing_next/tests/test_fiabc_succession_preflight.py
rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py
rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py
rawlsing_next/tests/test_pre553_empirical_objects_authority.py
rawlsing_next/tests/test_pre553_empirical_query.py
rawlsing_next/tests/test_pre553_discovery_exact.py
rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py
rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py
rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
```

The broad court included the formerly stale WVS packaging qualification and passed.

## CI hygiene

Temporary draft PR #437 was used only to execute the governed bounded court. It is closed and unmerged.

After receipt capture:
- `.rabochii/court_spec.json` restored exact A-base blob `95bceba63be84c502e3ec46a1b1a3039365ff50d`;
- `.github/workflows/rabochii-governed-bounded-court.yml` restored exact A-base blob `a974469aa1d83514d896e3de591d7618310ca493`.

No source-backed work was used to obtain PASS.
