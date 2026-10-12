# PYAT HQ282 P04 — Reproduction

## Evidence recorder

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ282-P04-SELECTED-WORLD-PROGRESSIVE-FIXTURE-R1/repro/p04_evidence_recorder.py
```

This executes the full P04 selected-world progressive chain and writes `p04_evidence.json`.

## Tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py -v
python3 -m pytest rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -v
```

Both suites pass: 24 + 18 = 42 tests.
