# SOROK CG-A G5-D1 corrective return

**Commission:** #982 corrective author (not G5 receiver)
**Status:** `D1_REPAIRED_PENDING_INDEPENDENT_G5`
**Base implementation:** `37c5842e04892421c9ce74a39956c3cdcf57f0f5` (PR #976 head)
**Final author HEAD:** the commit containing this return; verify with `git rev-parse HEAD`
**Changed implementation file:** `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py` only
**Protection:** no protected PRE-MAIN, actor/world owner, P3/P4/P5 producer, receiver frozen evidence or native authority changed.

## Repair

`current_p3_actor_access` now accepts an outward cue from `source_receipt` only when:

1. the receipt interval is exactly the caller's current interval; and
2. the interval end equals the current world clock.

This rejects an old authentic receipt both when a caller broadens the interval and when a caller presents the old receipt with its original interval. A genuine current receipt still satisfies both conditions; the normal P6 `reconsider` path passes the current `receipt["interval"]`.

## Local results

- Full 37-test review/author suite: **37 passed, 0 failed**, 2422.84 s.
- G5 D1 hostile probe (verbatim copy for regression): **passed**.
- Author D1 regression (stale receipt, old interval, current receipt): **passed**.
- Repair test command: **2 passed, 0 failed**, 27.73 s.

## Evidence

- `evidence/37_tests_fixed.log` — full 37-test output at the fixed source.
- `evidence/repair_tests.log` — G5 probe + author regression.
- `evidence/DIFF.patch` — exact 9-line fix.
- `evidence/SOURCE_STATE.txt`, `evidence/ENVIRONMENT.txt`, `evidence/SHA256SUMS`.

## Residual limit

This fixes the exact authentic-stale-receipt defect. It does not authenticate a forged receipt; a caller with raw writer access can still forge an interval and cue. That direct-caller trust boundary is the pre-existing author-held limitation, not a new D1 permission. No native psychology, actor/human right, production rule or protected merge is claimed.

## Handoff

A genuinely independent nonauthor G5 reviewer must verify this exact HEAD, the 37-test suite, the G5 probe and the author regression, and decide whether the direct-caller trust boundary remains an integration hold. The author does not self-approve.
