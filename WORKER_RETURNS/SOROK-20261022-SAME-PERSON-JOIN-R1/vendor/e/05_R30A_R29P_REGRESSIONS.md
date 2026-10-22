# Baseline and inherited regression receipts

No upstream test is double-counted.

## R31E new tests

```bash
cd WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest tests -q --junitxml=evidence/junit/r31e.xml
```

Actual: **15 passed, 0 failed** (`evidence/junit/r31e.xml`).

## R30A baseline, vendored exact code

```bash
cd vendor/r30a
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest tests -q --junitxml=../../evidence/junit/r30a_baseline.xml
```

Actual: **10 passed, 0 failed** (`evidence/junit/r30a_baseline.xml`). This preserves the R30A first-session/C12/M6/fault baseline at its own author grade; it is not R31E novelty.

## Selected R29P inherited integration subset

```bash
cd vendor/r30a/vendor/r29p
PYTHONPATH="$PWD:$PWD/candidate:$PWD/candidate/vendor/bp2:$PWD/candidate/vendor/bp4:$PWD/r26e:$PWD/n1" \
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_r29p.py \
  -k 'baseline or m6 or fork or no_global or seven' -q \
  --junitxml=../../../../evidence/junit/r29p_subset.xml
```

Actual: **5 passed, 0 failed** (`evidence/junit/r29p_subset.xml`): baseline/cold C12, M6, fork, no global builder mutation, and the seven same-observable source faults. **Full 155 inherited suite is NOT_RUN** and not claimed.

## Actual execution totals

| Layer | Tests | Status |
|---|---:|---|
| R31E expression/product | 15 | PASS |
| R30A baseline | 10 | PASS |
| R29P selected subset | 5 | PASS |
| Full inherited R29P 155 | 0 | NOT_RUN |

## C12 verification

`evidence/c12_verification.json`: both `root` and `first_session` verify for the available and pressed C12 copies with `R26E_QUALIFIED_C12_PREIMAGE`.
