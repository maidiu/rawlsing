# Mechanism I closure R2 — source/time repair receiving

**Reviewed author SHA:** `0b0eb94c714049dadd3f82cc0af97c44ff4f74b4`
**Prior reviewed head:** `634b75d6e321952e9a917c83ccf62ae7c30e0680`
**Prior independent finding:** `cd08444f00a9fccb2dd0124c8dc888e39838bd41`
**Verdict:** `ACCEPT_SCOPED_SOURCEFREE_ENGINEERING`

## Executed evidence

```text
# Original independent RED probe, now recovered and green
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mi-review-state" \
  WORKER_REVIEWS/SOROK-MI-COMPLETION-INDEPENDENT-20261111-R1/test_h1_source_time.py

# 1 passed in 2.48s
```

```text
# Changed owner/episode/provider/joined tests
... rawlsing_next/tests/test_sorok_history_episodes.py \
    rawlsing_next/tests/test_sorok_history_provider.py \
    rawlsing_next/tests/test_sorok_history_joined.py

# 40 passed in 200.92s
```

```text
# Ordinary activity and owner regressions
... rawlsing_next/tests/test_sorok_history_activity.py \
    rawlsing_next/tests/test_sorok_history_owner.py

# 26 passed in 248.11s
```

```text
# New independent no-cross-read-cache probe
... WORKER_REVIEWS/SOROK-MI-COMPLETION-INDEPENDENT-20261111-R1/test_source_closure_r2.py

# 1 passed in 1.63s
```

The prior 90-test MI baseline remains applicable for unaffected source; the changed suite above was rerun at this head. No external/provider calls were made.

## Repair verification

- `rawlsing_next/sorok_history/owner.py:1050-1060` now traverses both `causal_parents` and `source_refs`, resolves canonical events, rejects non-event/unsupported sources, and rejects a source whose effective time is after the episode effective time.
- `bp4/world.py:231-242` performs the same source ownership/kind/effective-time check at material-history admission, so the defect is closed at write time as well as readback.
- The original postdating-source reproducer now passes.
- The author’s transitive-source test passes in `test_sorok_history_episodes.py`.
- The new independent probe confirms a graph lookup refreshes source validity across operations: withholding the canonical support makes `query_relations` raise, and exact restoration returns the previous qualified read.
- Actual historical parent effective time is used rather than the later admission clock; `HISTORICAL_MATERIAL` events remain separate at admission time.

## E1–E10 / original 39 / B1–B7

The repaired sourcefree implementation retains the existing owner, H1 admission, graph@2 causal/support edges, T2/idle, provider transport/custody, joined P4/P5/P6 readers, and ordinary S46 activity evidence. The previously accepted unaffected evidence is reused. No new sourcefree engineering defect was found.

## Limits and authority

- Live provider inference was not rerun and is not inferred from mocks.
- Native science, actor/psyche effects, public pre-contact/root writes, product authority, and protected merge remain genuinely unissued.
- The sourcefree bounded engineering may be received at `S2`; those authority holds do not become missing sourcefree implementation.
- No implementation file was edited. Reviewer probes/report are owned in this directory.
