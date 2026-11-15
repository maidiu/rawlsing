# Source-free qualification matrix

All qualification ran under the pinned Darwin runtime:

- CPython 3.11.3, macOS 13.2.1, x86_64
- `pyreadstat 1.3.6`, `pyarrow 25.0.1`, `pytest 9.0.2`
- Exact implementation head: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Fresh checkout: `/private/tmp/fiabc-succession-fresh-3d8f2ad62`; clean at the real producer invocation and still clean after preflight.

## Complete prior repair qualification

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /private/tmp/fiabc-lits-onepass-r1-runtime.kHpXQb/bin/python -m pytest -q --junitxml=/private/tmp/fiabc-run3-full-3d8f2ad62.xml rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py rawlsing_next/tests/test_pre553_candidate_c_production_binding.py tests/test_ee_p2x_darwin_court_driver.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_carrier_execution.py rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py rawlsing_next/tests/test_fiabc_run3_postmeasurement_repair_stack.py rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py
```

Result: **115 passed, 0 failures, 0 errors, 0 skipped** in 38.310 seconds. JUnit evidence: `10_SOURCE_FREE_TEST_REPORT.xml`.

## Succession provenance producer/preflight regressions

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /private/tmp/fiabc-lits-onepass-r1-runtime.kHpXQb/bin/python -m pytest -q --junitxml=/private/tmp/fiabc-succession-target-3d8f2ad62.xml rawlsing_next/tests/test_fiabc_succession_producer.py rawlsing_next/tests/test_fiabc_succession_preflight.py
```

Result: **24 passed, 28 subtests passed, 0 failures, 0 errors, 0 skipped** in 12.680 seconds. JUnit evidence: `11_SUCCESSION_TEST_REPORT.xml`.

The succession regressions prove that all four direct execution dependencies are required in the manifest’s `current_head_bindings.required_files`; refs must match the manifest’s exact generated head, and the preflight P00 evidence resolver verifies their Git blobs and content hashes. Removing or rebinding a required path blocks preflight. The existing current owner map remains unchanged.

## Live source-free qualification

The real succession producer and actual preflight evaluator ran against a fresh clean checkout at `3d8f2ad62600b6777dcb23a28404a067502e77a0`. The producer returned `PASS`; the preflight returned `PASS` on 11/11 checks with no failure codes. Producer receipts show candidate processes `0`, outputs `0`, roots `[]`, and the exact six-cell order. Exact generated objects and hashes are banked in `current_head_succession/`, with summaries in `11_SUCCESSION_PROVENANCE_CLOSURE.json` and `12_LIVE_SUCCESSION_QUALIFICATION.json`.

No LiTS/WVS respondent-level source was opened or hashed. No measured P2X or candidate subprocess ran.
