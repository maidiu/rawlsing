# REMONTATHON R16 — verified corrections from independent local-machine R12 cut

**Source parent:** frozen R15 draft #1220 exact `6075792420e1d87b30036ebe6f352815783e47c2`.
**Outside source:** R12 draft #1199 HEAD `943b52c08d6b0fa9cdfdff9f7b751ab2eafcccb6` (248/248 Python 3.11.3 as user reported). This candidate selectively inherits the non-overlapping corrections into R15; it does **not** fast-forward from R12 or accept the R12 author's sourcefree return.

## Exact reproducible local court

From this extracted archive root:

```bash
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m unittest tests.test_r16_r12_local_machine_reconcile -v
python -m um_sorok_organism demo --db /tmp/remont_r16_fresh.sqlite3
```

Four new R16 test methods were RED on unchanged frozen R15 source (5 actor snapshot ERROR subcases, 5 world snapshot FAIL subcases, recruitment ordering and different-end trial takeup). The actual R16 code made these PASS. Author Python 3.13.5 full court: **280 normal, 280 optimized, pytest 280 +32 subtests**; original R15 276 preserved. Fresh extracted archive to be checked independently.

Scope: sourcefree typed persisted snapshot validation, deterministic actor-facing recruited forms, and same-event any-end motive-takeup denial. Current R13 `REORGANIZE_PROJECT` guard already existed; it is NOT reported as a new repair. No extra defect ID, no promotion of original 73 records. P019/P022 reserved for SORACLE; P009 native disclosure, P012/P018 native/scientific issues remain. Independent exact-head receiving and Python 3.11 test of this R16 HEAD pending.
