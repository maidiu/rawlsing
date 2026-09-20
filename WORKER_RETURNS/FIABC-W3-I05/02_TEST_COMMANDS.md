# FIABC-W3-I05 — Test Commands

No command below was executed by this browser/GitHub-only worker.

## Focused I05 oracle suite

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_independent_parity_oracle.py
```

Expected collection from this worker file: **15 tests**.

## PRE553 regression neighborhood

Run after the focused suite:

```bash
python -m pytest -q \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py
```

These tests exercise the new court-owned oracle beside the unchanged I03/I05 semantic owners.

## Integrated P2X fan-in qualification

After HQ fans in the Wave-3 implementation branches and binds the court runner to the I05 oracle, run the integrated runner/oracle tests selected by the fan-in planner. At minimum the integrated qualification must prove:

1. the source-local oracle exists and is frozen before candidate A emits output;
2. S03 consumes the frozen oracle identity rather than creating expected truth from the active candidate binding;
3. A/B/C each emit a candidate observation bound to that same oracle identity;
4. candidate self-replay remains a separate replay predicate only;
5. performance admission remains impossible until independent oracle match passes;
6. WVS7 source-derived oracle materialization completes before any WVS candidate run.

Do not interpret a passing focused unit suite as evidence that the WVS source oracle has been materialized or that measured P2X is lawful. Those require the local protocol and the Wave-3 succession/equal-work/terminal gates.
