# Source-free qualification matrix

All tests ran with the pinned Darwin environment:

- CPython 3.11.3, macOS 13.2.1, x86_64
- `pyreadstat 1.3.6`, `pyarrow 25.0.1`, `pytest 9.0.2`
- Command: `/private/tmp/fiabc-lits-onepass-r1-runtime.kHpXQb/bin/python -m pytest -q --junitxml=WORKER_RETURNS/FIABC-RUN3-POSTMEASUREMENT-REPAIR-STACK-R1/10_SOURCE_FREE_TEST_REPORT.xml rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py rawlsing_next/tests/test_pre553_candidate_c_production_binding.py tests/test_ee_p2x_darwin_court_driver.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_carrier_execution.py rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py rawlsing_next/tests/test_fiabc_run3_postmeasurement_repair_stack.py rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py`
- Result: **115 passed, 0 failed, 0 skipped** in 36.58 seconds.

| Area | Source-free checks | Result |
| --- | --- | --- |
| A provenance | Exact SOURCE_ARTIFACT reference; missing id/wrong kind fail closed; frozen A accepts tiny R5; physical member rows remain unchanged; deterministic identity | PASS |
| B owner universe | Split current/frozen type universe fails; exact B projection/nested types and keys work; repository/release binds through common runner; parent module remains unchanged | PASS |
| LiTS bridge | Authorized float64 and system-missing cases; source, slot pair, type/token, missing state/declaration, source-family and release hostile cases | PASS |
| A/B/C semantic truth | Same release reference on bounded fixture and production composition seam; C policy receipt remains current and does not move semantic ownership | PASS |
| WVS shared-infrastructure regression | WVS source identity unchanged; synthetic A/R5 stream and physical member payload remain stable | PASS |
| Existing process/control regression | T2, T3 process-envelope, W3 process-isolation, and T5 terminal-control suites | PASS |

The complete JUnit evidence is `10_SOURCE_FREE_TEST_REPORT.xml`. The test-only exact-owner imports are removed/restored after each new qualification test so unrelated process-isolation tests see the original parent interpreter module namespace.

No LiTS/WVS respondent-level file was opened. Frozen A/B code was exercised only with bounded synthetic carriers/projections; no measured P2X or candidate subprocess ran.
