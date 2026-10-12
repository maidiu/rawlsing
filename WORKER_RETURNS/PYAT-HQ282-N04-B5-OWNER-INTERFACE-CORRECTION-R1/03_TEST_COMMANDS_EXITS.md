# PYAT HQ282 N04 — Test commands and exits

## Environment

- Python: 3.11.3
- pytest: 9.1.1
- Machine: local Mac
- Model: opencode-go/mimo-v2.6-pro

## Commands and exits

### N04 candidate tests

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py -x -q
```

**Exit:** 0
**Result:** 15 passed in 0.22s

### Owner tests (baseline)

```bash
PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py
```

**Exit:** 0
**Result:** 83 passed in 0.86s

### Combined suite

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py -q
```

**Exit:** 0
**Result:** 98 passed in 0.60s

### C02J owner court (baseline)

```bash
PYTHONPATH=. python3 -m rawlsing_next.repro.c02j_owner_court
```

**Exit:** 0
**Result:** 24 cases executed (19 behavioral, 5 controls)

## Historical vs current tests

- **Historical tests** (from C02J commit `895980397cc0533043c7ca0e493ebbb455666c1e`): 83 owner tests, 24-case court
- **Current tests** (executed in this N04 work): 15 N04 tests, 83 owner tests, 24-case court

All current tests executed locally with exit code 0.
