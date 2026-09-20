# FIABC-T3 — Test Commands

No tests were executed by this GitHub/browser worker. No result is fabricated.

No command below requires real LiTS/WVS source materialization or measured P2X.

## T3 focused freeze/order tests

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
```

Covers:

- arbitrary non-LiTS/WVS source IDs;
- canonical source SHA and source-identity authority fields;
- derivative/provenance pairing;
- freeze causal ordering;
- rejection of post-candidate-output freeze;
- removal of candidate self-replay as S03 expected truth;
- driver direct-backend bypass rejection;
- process-envelope cell sealing.

## I06A process-isolation hostile suite

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py
```

Expected inherited hostile coverage: 9 tests.

## I05 independent-oracle suite

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_independent_parity_oracle.py
```

Expected inherited focused coverage: 15 tests.

## T2 regression

```bash
python -m pytest -q \
  rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py \
  rawlsing_next/tests/test_pre553_candidate_c_production_binding.py
```

## Source-independent combined T2/T3 qualification

```bash
python -m pytest -q \
  rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py \
  rawlsing_next/tests/test_pre553_candidate_c_production_binding.py \
  rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py \
  rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py
```

## Syntax-only check

```bash
python -m py_compile \
  rawlsing_next/ee_p2x_darwin_court_driver.py \
  rawlsing_next/ee_p2x_darwin_stage_backend.py \
  rawlsing_next/ee_p2x_candidate_process_envelope.py \
  rawlsing_next/ee_p2x_process_isolated_backend.py \
  rawlsing_next/pre553_independent_parity_oracle.py
```

## Explicitly forbidden in this T3 qualification

Do not:

- materialize the real WVS7 oracle;
- rebuild real LiTS candidate state;
- open real CLOSED_35 source carriers;
- execute measured P2X;
- treat a source-independent unit-test PASS as empirical court completion.
