# SOROK P2 explicit interval continuation R1

**RESULT:** `PASS` — additive TEST_ONLY explicit interval continuation.

**Grade:** `TEST_ONLY_S45_S47_EXPLICIT_INTERVAL_CONTINUATION_NOT_NATIVE`.

Base: `41bf45813fd0adeffd9b54e1306c2022abe96514` (independently ACCEPTED
scoped TEST_ONLY; PR697 unchanged/unmerged). No inherited product, vendor,
projection or PROGRAMMA working file was edited. All new code/evidence is under
`WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/` with checkout-local
staging under `.local-logs/p2-explicit-interval-flow/`.

## What was added

A callable/CLI continuation over the existing shipped S45-S47 product:

- `continue_after_request(state, request, interval_input)` — WAIT/ABSENCE alone
  return typed holds. Only an explicit interval input (`mode` plus optional
  `start`/`span`) continues.
- `apply_explicit_interval(...)` — calls the existing `run_s45_s47.py interval`
  command.
- `admit_continuation(...)` — calls the existing `run_s45_s47.py admit` and
  `c9` commands, then exposes the public `S45Projection` continued encounter
  view and `DO_HELP` consequence.
- CLI: `run_explicit_interval_flow.py continue|interval|admit`.

No S46/S47 producer, S42 admission, projection or public CLI code was rebuilt or
edited. The integration delegates to the shipped commands and public projection
API.

## Explicit activity versus user wait

- `WAIT` without interval input: `HELD`,
  `WAIT_UNSUPPORTED_TYPED_HOLD`, `advanced: false`, no state/clock change.
- `ABSENCE` without interval input: `HELD`,
  `USER_ABSENCE_LIFE_ADVANCE_MISSING`, `advanced: false`, no state/clock change.
- No default `ACTUAL`; missing/invalid mode returns `HELD`/`REFUSED` without
  advance.
- `SCHEDULED_ONLY`, `UNKNOWN`, `BLOCKED`, `DECLINED`, `CONSTRAINED` preserve
  their existing producer semantics.
- `general_autonomous_absence_life: false` is explicit in every result. This is
  not a general autonomous absence-life producer.

## Exact commands and results

Focused tests:

```text
SOROK_P2_BASE_ROOT=<checkout>/.local-logs/p2-explicit-interval-flow/base \
TMPDIR=<return>/logs/tmp \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=<return>/evidence/focused_tests.xml <return>/tests
```

Result: **6 passed** in `55.59s`, 0 failed/error/skipped. Tests cover:
WAIT/ABSENCE holds, invalid/missing mode non-advance, ACTUAL material change and
DO_HELP refusal, SCHEDULED_ONLY retention and DO_HELP acceptance, UNKNOWN mode
preservation, and exact dependency cut/refusal/restore plus cold continuity.

CLI smoke (fresh process, clean env, `python3 -I -B`):

```text
<base-product>/run_s45_s47.py new --state <state-actual>
<return>/run_explicit_interval_flow.py --base-root <base> continue \
  --state <state-actual> --request WAIT
<return>/run_explicit_interval_flow.py --base-root <base> continue \
  --state <state-actual> --request WAIT --mode ACTUAL --span 4

<base-product>/run_s45_s47.py new --state <state-scheduled>
<return>/run_explicit_interval_flow.py --base-root <base> continue \
  --state <state-scheduled> --request ABSENCE --mode SCHEDULED_ONLY --span 4
```

Observed:

| Case | Interval | Material | C9 material | DO_HELP | Cold |
|---|---|---|---:|---|---|
| WAIT, no input | none | unchanged | none | none | none |
| ACTUAL, span 4 | `PARTIAL`, coverage `[[222, 223]]` | `0` | `false` | `REFUSED` / `HELP_REFUSE` | `true` |
| SCHEDULED_ONLY, span 4 | `NOT_PERFORMED`, coverage `[]` | `1` | `true` | `OK` / `HELP_ACCEPT` | `true` |

Both intervals report `actual_daily_events_invented: 0`,
`actor_knowledge_inferred: false`, `psychology_state_written: false`.

Dependency cut/restore (focused test):
`S46_INTERVAL_CONDITION_REVOKED` on `admit` after the interval; restore then
continues with C9 material `false` and DO_HELP `HELP_REFUSE`, cold continuity
true.

## Evidence

- `evidence/result.json` — combined PASS checks and authored-file hashes.
- `evidence/focused_tests.xml`, `logs/focused_tests.log` — 6 focused tests.
- `evidence/cli/hold-wait.json`, `continue-actual.json`,
  `continue-scheduled.json` — public CLI receipts.
- `evidence/cli/product-new-*.json` — fresh-state creation receipts.
- Base product source manifest SHA-256 is recorded in `evidence/result.json`.

## Limitations

- TEST_ONLY sourcefree explicit continuation; not general autonomous absence
  life, native psychology, or a new actor-motive producer.
- User WAIT/ABSENCE never select activity. Activity is only the explicitly
  supplied S46 interval input; the existing producer decides actual material
  participation.
- No actor choice, B state, paid counterpart, motive or native grant is
  fabricated.
- Focused checks only; inherited full estate/full55 was not rerun.
- This is not self-acceptance. Independent review and PRE-MAIN receiving remain
  separate owner actions.

## Next receiving owner action

HQ/lead may fan this additive return into the accepted S45-S47 product line,
but must first obtain the existing independent review for this exact additive
commit. No protected PRE-MAIN write or PR697 merge follows from this return.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: additive callable/CLI
integration and evidence only; no PROGRAMMA canonical product, seam/gate
register, native science or receiving authority changed.

## Publication

Branch: `codex/sorok-p2-explicit-interval-flow-20261105-r1`. Exact final commit
and pushed SHA: `PUBLICATION_RECEIPT.json`.
