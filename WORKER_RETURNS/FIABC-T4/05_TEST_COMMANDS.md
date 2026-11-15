# FIABC-T4 — Source-independent test commands

## Execution status on this worker

**NOT EXECUTED.**

No GitHub Actions run fired for this branch, and this browser-only repository worker has no repository execution shell.

No measured P2X was run.

## Focused T4

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t4_live_accounting.py
```

Covers the requested hostile surface including:

- cross-candidate metric leakage;
- metric overwrite;
- missing metric != zero;
- endpoint size != observed I/O;
- scratch endpoint != peak;
- formula/law-hash/temp-file surrogate rejection;
- invalid warm reuse;
- wrong replay terminal identity;
- derivative parentage absence;
- child-process CPU exactly-once and RSS max semantics.

## Accepted I06B / I06C regression

```bash
python -m pytest -q tests/test_fiabc_telemetry_semantics.py
python -m pytest -q tests/test_fiabc_lifecycle_accounting.py
```

These include preserved-work incompatibility/no-credit cases and the accepted lifecycle hostile tests.

## T3 / I06A regression

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
python -m pytest -q rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py
```

## T2 current six-cell regression

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py
```

## Local-court source-independent integration regression

```bash
python -m pytest -q rawlsing_next/tests/test_ee_p2x_local_court_driver_integration.py
python -m pytest -q rawlsing_next/tests/test_ee_p2x_local_court_receipts.py
```

Do not substitute a real-source or measured P2X invocation for these qualification commands.
