# T4 / S46 ordinary dispatch closure — issue #824

**Base:** PR #791 exact verified head `95941a7708dc8b34b02b3de5a38322b2b0693750`.
**Protected ref observed at dispatch:** `integration/pre-main-reconciliation-r1@2162d85db5e6822707e5cdff7aac2656ebef4761`; no protected write is made by this candidate.
**Grade:** sourcefree engineering, author-local S2. No live inference, native science, rights, independent review, or protected receiving is claimed.
**First caller:** `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py:56`
`advance_dispatched`; CLI entry `work` at line 333; owner resolve/hold at
`rawlsing_next/sorok_history/owner.py:311/323`; adapter at
`rawlsing_next/sorok_history/activity.py:477`.

## Actual producer/consumer path

- `run_p4.advance_dispatched` is the ordinary S46 path. It asks
  `HistoricalWorld.target_for_referent("world-resource:<actor-location>:tool", location=...)`
  to resolve the committed tool target; the caller supplies no target,
  predicate, or expected literal.
- `rawlsing_next.sorok_history.activity.produce_activity_requirement` emits the
  typed `S46_ACTUAL_REPAIR` requirement with root/branch, target, target
  version, `condition=serviceable`, exact parent event, job, and world readset.
  `HistoricalWorld.hold_activity_requirement` persists it in the same world
  checkpoint before any physical interval.
- `run_p4 work` is the static executable normal call site. `run_p4.advance` is
  retained unchanged for legacy/no-requirement activity.
- `rawlsing_next.sorok_history.activity.dispatch_activity_requirement` validates
  the admitted `physical_depth` fact (target, job, accepted fact, claim ref,
  parent event/hash, root/branch, actor place) and only then calls the existing
  `run_p4.advance`/P2/P3/S46 interval owner. It marks the requirement
  `CONSUMED` only after that call.
- `run_p4.run_history_worker` resumes held requirements after a real worker
  admission, without user inspection or a caller-supplied tuple.

## D1–D10

| Case | Result | Evidence / limitation |
|---|---|---|
| D1 missing-depth hold | PASS scoped | Normal `run_p4 ... work` emits a durable HELD requirement; zero ACTUAL intervals, clock 230 and material 1 unchanged; requirement survives owner reopen and repeated work. |
| D2 positive resume | PASS scoped | Existing worker core with injected mock transport admits `condition=serviceable`; auto-resume produces exactly one ACTUAL PARTIAL interval, material 1→0, clock 230→232; target/job/event/fact refs retained; observer perception unchanged. |
| D3 negative content | PASS scoped | Admitted `condition=broken` holds with `HISTORICAL_DEPTH_VALUE_MISMATCH`; no ACTUAL interval or material use. |
| D4 exact sever/restore | PASS scoped | Severing the exact target parent event through the session read interface holds with `HISTORICAL_PARENT_MISSING`; restoring the exact event requalifies and advances one actual interval. |
| D5 forged/wrong scope | PARTIAL | Forged target/job/root requirement is held before interval; wrong actor place, world/resource contradiction, and cross-root branch import are not all separately executed. |
| D6 cold replay/idempotence | PARTIAL | Durable requirement survives a separate `work` process/reopen; a consumed requirement replay is HELD with no double material use. Full separate-OS hold/admit/resume and crash-point matrix not run. |
| D7 unaffected control | PASS scoped | Existing `test_real_interval_binds_completed_output_without_inspection` and P4 CLI court pass; legacy `run_p4.advance` remains unchanged. |
| D8 actor isolation | PARTIAL | D2 confirms no INSPECT event and unchanged user-perceived IDs; differing actor gaze/user-hypothesis histories were not executed. |
| D9 model failure | PASS scoped | Timeout from the injected provider leaves the requirement HELD and no ACTUAL interval/material change. |
| D10 branch concurrency | NOT_RUN | Child/sibling branch activity requirement and material isolation were not executed here. |

P11 is now sourcefree positive at the scoped level above (previously HELD).
N15 remains open: the existing P6 fixed-house regression was not run.

## Focused commands

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_activity.py
# 7 passed

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_*.py
# 54 passed in 143.86s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_*.py WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_cli.py
# 55 passed in 186.15s
```

Author local S2 result only. Independent S2 rerun and native S3 are NOT_RUN.

## Independent receiving verdict

Reviewer `ses_e52a51c43ffeuVe7ZZhNcga5YP` returned `HOLD_SCOPED` on
`79c154d5de7f1c9483d32a22252a0c3a022329a6`. The exact-head reruns passed
7 focused tests, 54 history tests, and 55 history plus P4 CLI tests.
Normal dispatch and requirement provenance passed within that scope.
D1–D3, D7 and D9 passed executed review. D4 is partial because severance
and restoration were in-process only. D5, D6 and D8 remain partial.
D10 was not run. P11 remains scoped positive and N15 remains open.
The activity owner is continuing the missing adverse cases.
