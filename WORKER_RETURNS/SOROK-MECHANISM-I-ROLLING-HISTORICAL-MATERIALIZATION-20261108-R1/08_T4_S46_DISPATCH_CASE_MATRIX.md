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
| D4 exact sever/restore | PASS scoped | Cold owner `physical_depth` detach/restore: HELD with no actual interval, then one actual interval after exact restore. Parent-event severance/restoration is in-process only; cold exact parent-event restore remains unproven. |
| D5 missing/wrong scope | PASS scoped | Wrong actor place holds `HISTORICAL_MATERIAL_NOT_IN_ACTIVITY_PLACE`; world/resource contradiction holds `HISTORICAL_MATERIAL_WORLD_MISMATCH`; an actual distinct-root requirement and a genuinely recorded foreign-scope requirement both fail closed before interval. |
| D6 cold replay/idempotence | PASS scoped | Separate-OS `work` hold, mock worker admission, crash after interval and crash before interval both recover to exactly one ACTUAL interval and one CONSUMED requirement; duplicate resume is HELD and consumes nothing. Recovery requires the interval's exact `activity_requirement_ref` and re-verifies the admitted target/job/fact provenance; a same-start unrelated ACTUAL interval is not credited and leaves the requirement HELD with no false `fact_id`. Ambiguous recovery is persisted as non-retryable `AMBIGUOUS`; repeated resume and cold reopen do not add an interval. Pre-repair persisted ambiguous HELD records are rechecked before any retry. |
| D7 unaffected control | PASS scoped | Existing `test_real_interval_binds_completed_output_without_inspection` and full P4 CLI court pass; legacy `run_p4.advance` remains unchanged. |
| D8 actor isolation | PARTIAL | D2/D8 show no INSPECT, unchanged perceived IDs, and changed user hypothesis plus user ATTEND do not alter the requirement. No tracked P6 proof runtime exists in this checkout; the separate `codex/sorok-p6-gaze-proof-20261107-r1@a075232f56b55bcce138df755db20e77e3ec5f3c` proof is not imported/touched. P6 gaze remains NOT_RUN. |
| D9 model failure | PASS scoped | Timeout from the injected provider leaves the requirement HELD and no ACTUAL interval/material change. |
| D10 branch/root isolation | PASS scoped | Child branch performs pending→admission→one actual consumption through normal dispatch; repeated parent readback shows parent material 1, no child target, parent requirement HELD and no ACTUAL interval. Separate root store also remains isolated. |

P11 is now sourcefree positive at the scoped level above (previously HELD).
N15 remains open: the existing P6 fixed-house regression was not run.

## Focused commands

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_activity.py
# 18 passed in 126.14s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_*.py
# 66 passed in 256.42s (prior full run)

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider --tb=short rawlsing_next/tests/test_sorok_history_*.py WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_cli.py
# 66 passed in 256.42s (prior full run)
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

## Independent adverse-case review

Reviewer `ses_e52a51c43ffeuVe7ZZhNcga5YP` returned `HOLD_SCOPED / REVISE`
at `484a147a9dd9f8e2ed4799d1d328ac93d48d895c`. Independent reruns
passed 15 focused tests, 62 history tests, and 63 including P4 CLI.
D4 passed scoped cold fact detach/restore. D5, D8 and D10 remain partial.
D6 is held: an unrelated ACTUAL interval at the same start clock was
credited to the pending requirement, which became CONSUMED with no
fact ID. The author is repairing exact recovery attribution and adding
the reproduced negative. P6 gaze and full sibling-parent readback
remain unrun.

## Independent-review D6 repair

Independent review of `484a147a9dd9f8e2ed4799d1d328ac93d48d895c`
reproduced the D6 attribution defect: `DISPATCHING` recovery matched an
ACTUAL interval by start/root/branch/actor/status, so an unrelated interval
at the same start could consume the requirement with `fact_id: null`.
This repair binds `run_p4.advance` to the durable requirement using
`activity_requirement_ref` in the S46 interval domain. Recovery accepts only
one exactly matching interval, revalidates the owner-admitted target/job/fact
provenance and expected value, and fails closed on ambiguity or missing
provenance. The newly added same-start unrelated-interval negative passes;
the genuine crash-before and crash-after recovery tests remain green.

## Independent D6 binding review

Reviewer `ses_e52a51c43ffeuVe7ZZhNcga5YP` returned `HOLD_SCOPED / REVISE`
at `b271b1bd086ba2b0067ff88fd5a5a556c5a1d721`. Independent reruns
passed 16 focused tests, 63 history tests and 64 including P4 CLI.
Same-start unrelated interval rejection and nominal crash recovery
passed. A separate ambiguity reproduction yielded one interval before
the hold and two after resume. The ordinary HELD state permits retry
of an ambiguous recovery. The author is repairing that transition.
D5, D8 and D10 remain partial.

## Residual ambiguity repair

The independent review of `dcc6f3f97857f59781640aa39f799d6ec5fd1546`
held a residual D6 defect: an ambiguous recovery was persisted as ordinary
`HELD`, so `resume_activity_requirements` retried it and produced a second
ACTUAL interval (`1 -> 2`). The repair persists ambiguity as non-retryable
`AMBIGUOUS`, rechecks pre-repair ambiguous HELD records before any retry,
and fails closed with no new interval. The reviewer reproduction is covered
with repeated resume and cold reopen; the exact-bound crash-before/after and
same-start unrelated interval negatives remain green.

## Independent D6 ambiguity closure

Reviewer `ses_e52a51c43ffeuVe7ZZhNcga5YP` returned `PASS_SCOPED` for D6
at `b040211589609d1d716692c42620ade614b7a058`. Reruns passed 5 D6 cases,
18 focused tests, 65 history tests, and 66 including P4 CLI.
Independent duplicate-interval and legacy HELD probes confirmed that
repeated resume and cold reopen preserve one interval and a non-consumed
AMBIGUOUS requirement. D5, D8 and D10 remain partial. D4 remains scoped
to cold fact detach/restore. The activity owner is continuing the
remaining adverse cases.

## Remaining adverse-case closure

D5 now includes a requirement actually recorded in the current owner index
whose root/branch target is foreign; it fails closed before interval. D10 now
executes child pending, child admission through the existing worker, one child
actual consumption through normal dispatch, and repeated parent readback at
each stage. D8 remains PARTIAL because no compatible P6 gaze runtime is tracked
in this checkout; the separate P6 gaze proof branch was not imported or
touched. D4 retains the cold parent-event restoration limit; its cold proof is
the sanctioned physical-depth detach/restore path.

## Independent D5 and D10 readback

At `092e7e283da80a533241cd2c101801281ed93b41`, the independent reviewer
`ses_e52a51c43ffeuVe7ZZhNcga5YP` returned `HOLD_SCOPED`. The activity
court passed 18 tests, history 65, and history plus P4 CLI 66. D10 passed
both selected tests and confirmed child dispatch and parent isolation.
Sibling readback remains unrun. D5 selected alone yielded one pass and
two failures due to an order-dependent run_p4 import. The foreign-scope
case also leaves target absence as an alternate cause of refusal.
The existing activity worker is repairing those tests and adding the
required sibling readback. D4 cold parent restoration and D8 P6 gaze
remain unproven.
