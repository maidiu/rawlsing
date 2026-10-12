# PYAT HQ282 N04 — Reproduction

## Tests

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py -v
```

15 tests pass.

## Combined suite

```bash
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n04_b5_checkpoint_interface_correction.py rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py -q
```

98 tests pass.

## Evidence recorder

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ282-N04-B5-OWNER-INTERFACE-CORRECTION-R1/repro/n04_evidence_recorder.py
```

This executes the checkpoint defect demonstration and method inventory, and writes `n04_evidence.json`.
