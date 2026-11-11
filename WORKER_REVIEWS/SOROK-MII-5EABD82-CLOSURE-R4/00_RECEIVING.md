# MII closure receiving — 5eabd82

**Final bounded sourcefree verdict:** `ACCEPT_SCOPED_SOURCEFREE_ENGINEERING`.
The prior R3 defect is repaired and independently reproduced as closed. No concrete missing required sourcefree behavior was found. Final sourcefree engineering may be received on this exact head.

**Tested author SHA:** `5eabd82074fab9318cb50838feeb6e78743dffdd`
**Prior author:** `49720bf5e532cfd0588d7ae8255ee103cd6ced76`
**Prior independent R3:** `afd006ae51d328f3576f2f6159797f916b8d68cd`
**Prior early references:** `319a2060d`, `d33e58d5b4b8b841227f7e2356a970d44171508d`, `99f428fc1`.

## Executed evidence

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py

# 18 passed in 639.86s
```

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_REVIEWS/SOROK-MII-5EABD82-CLOSURE-R4/test_prior_final_reproducer.py

# 2 passed in 40.34s
```

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_REVIEWS/SOROK-MII-5EABD82-CLOSURE-R4/test_replay_interrupted.py

# 2 passed in 75.18s
```

The prior R3 reproducer was recovered exactly from `git show afd006ae:...` and passes at this head. It verifies:
- `candidates` and `offered` remain distinct;
- successful duplicate `look` leaves adaptive weight unchanged.

The new replay probes use `run_p6.experience` for the full path and verify:
- successful duplicate returns the same surface/detail, unchanged ledger bytes, unchanged exposure count, and unchanged weight;
- an interrupted `mii.save_profile` after a successful P4 turn leaves the ledger committed; retry with the same request ID applies evidence once (weight 2), preserves ledger bytes, returns the expected surface and recognized inspection, and a later duplicate makes no further exposure or weight change.

## Delta review

The only implementation delta is `run_p6.py:139-188`: it tracks `turns_before`, `replayed`, and `exposure_created`, then calls `mii.update_attention` only for a new exposure or a non-replayed action. This directly addresses the R3 duplicate-adaptive defect; no unrelated implementation change was introduced. `test_mii.py` adds the integrated stale/correction test and the interrupted-retry duplicate weight assertion.

## E1–E10 / original 44

- E1 committed source denial/restore, E2 observer and per-object qualification, E3 candidates/offered/selected preservation, E4 earned/taught/forged recognition, E5 competing/stale/correction behavior, E6 surface budget, E7 existing P6 ingress, E8 profile/fork/interruption controls, E9 measurement artifact, and E10 runnable path/README are all represented at sourcefree scope.
- The updated `test_mii.py` includes real-P6 integrated E5/G03/G08 assertions (stale decay and correction alter subsequent `view` selection), not only helper calls.
- The 44-ID mapping now uses actual symbolic fixtures for M01/M02, user-derivative isolation for M04/M05, and prior unchanged HOUSE/GAZE/REC/MIII evidence for the unaffected IDs. No PASS-by-absence remains for the symbolic watch/icon cases, and no specific original behavior was found missing after the repair.
- Inherited suites were not rerun because their source behavior was unaffected; prior exact-source evidence remains applicable.

## Performance

The unique-command workload and measurement artifact are unchanged from the previously audited `49720bf` cut; `measure_mii.py`/`measurements.json` were not part of this delta. Retained audit: cold CLI n=13, p50 6.340 s, p95 9.688 s, max 12.873 s; warm import n=5, p50 3.101 s, p95 3.106 s, max 7.629 s; provider calls/tokens 0; child RSS 50.730 MiB; state 1,600,669 bytes. No full timing rerun was required or performed.

## Holds

Native science, human validity, live provider proof, production privacy approval, and protected merge remain excluded authority, not missing sourcefree implementation. No protected merge or author checkout was touched. Only reviewer tests/report are owned under `WORKER_REVIEWS/SOROK-MII-5EABD82-CLOSURE-R4`.

**ENGINEERING:** `ACCEPT_SCOPED_SOURCEFREE_ENGINEERING`.
**SCIENTIFIC:** no native/human claim.
**AUTHORITY:** no production/live/protected claim.
