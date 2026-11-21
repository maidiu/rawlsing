# SOROK REMONTATHON R15 — first reader (November 20, 2026)

**Frozen parent:** draft REMONT R14 PR #1214 at `f8c0d8dc901116d5fd1bfa7ec992dffa90a9aef0`.
**Scope:** P012 (inhibitor stratification) and P018 (source seal and auxiliary state custody) as strictly sourcefree REMONT engineering. P009 native private disclosure is separately HELD; P019/P022 remain SORACLE-owned. No protected writes or independent acceptance.

## Run

Extract this ZIP into a clean directory, cd there, then:

```bash
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m um_sorok_organism demo --db ./r15_demo.sqlite3
```

**Actual author cut:** 276 unit tests PASS normal, 276 PASS optimized, 276 pytest PASS plus 22 subtests, nine-event cold SQLite chain verified; all copied from the frozen source files recorded in `R15_SOURCE_SHA256.json`. Python 3.13.5; Python 3.11 and independent reviewer execution pending.

The R14 source had 265 tests. This candidate adds exactly 11. `R15_RED.txt` captures six failing first-fault test methods on original R14; `R15_SOURCE_IDENTITY_RED.txt` captures the later two new failing test methods before source admission validation. Do not conflate author-executed evidence and independent receiving.
