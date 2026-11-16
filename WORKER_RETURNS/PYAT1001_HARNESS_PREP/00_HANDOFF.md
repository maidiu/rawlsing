# PYAT1001 — bounded scale-harness preparation

## Status

**`PREP_ONLY__NOT_RUN_FULL_SCALE`**

The reusable generator and measurement interfaces are prepared. The full
100,000-distinct-respondent / 6 GiB execution is **HOLD_DEPENDENCY_998** and was
not run. No production authority, source rights, CURRENT issuer or protected
merge is claimed.

## Generator cardinality

`rawlsing_next/tests/pyat1001_scale_harness.py`:

- validates exactly **1,000 distinct respondent IDs** using 999 ordinary
  respondents plus `SENTINEL-MANY-EVENTS`;
- sentinel has **257 events**, so event/slot counts are not respondent counts;
- `expected_events = 2,255` and `expected_slots = 2,255` for that validation
  plan;
- supports a lazy **100,000 distinct respondent** plan without materializing
  the full vertical: `expected_events = 300,997`, `events_are_not_respondent_count=true`;
- no 100k full run was performed.

## Measurement interface

The harness provides:

- a 2 ms `ps` parent-root process-tree RSS sampler, including live children;
- retained/peak-stage/source-open/full-build/whole-table counter interfaces;
- cold/repeat/native/recovery measurement hooks;
- explicit `FULL_SCALE_STATE = NOT_RUN__HOLD_DEPENDENCY_998`.

The sampler is prepared for the eventual integrated #998 vertical; it is not a
claim that the 6 GiB cap passed.

## Evidence

- `harness.py` (copy of the test harness)
- `test_scale_prep.py` (copy of the focused prep test)
- `scale_prep.txt`: **2 passed in 0.11s**

## Next dependency

An independently accepted exact #998 joined sourcefree vertical. Only then may
the same owner execute the full 100k/6 GiB court against that frozen cut.
