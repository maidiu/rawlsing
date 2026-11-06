# SOROK P2 explicit interval continuation R1 — auto-DO_HELP repair

**RESULT:** `PASS` — focused repair of automatic user-attempt manufacture.

**Grade:** `TEST_ONLY_S45_S47_EXPLICIT_INTERVAL_CONTINUATION_NOT_NATIVE`.

**Repair base:** `bdadbc57c2664d3155a97853422e74b6128261f8` (historical, immutable).
**Product base:** `41bf45813fd0adeffd9b54e1306c2022abe96514` (unchanged).
**Defect source:** `WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/evidence/upstream_interval_auto_do_help.json`.

The previous `admit_continuation` called `adapter.do_help()` while presenting a
continued opportunity, automatically executing a user attempt. This repair
removes only that automatic user-attempt manufacture. No product, vendor,
projection, fan-in, later-lifecycle or PROGRAMMA working file was edited.

## Repair behavior

- `apply_explicit_interval`, `admit_continuation` and `continue_after_request`
  are now observation-only. They return the real event-bound public
  opportunity/read result from the existing projected S47 view.
- Observation result fields: `do_help: null`, `do_help_executed: false`,
  `user_attempt_executed: false`, unchanged encounter count,
  `encounters_unchanged: true`, public `opportunity` containing only projected
  view data (clock/location/visible event count/encounter admission/tool
  availability/controls/return availability).
- No raw private C9 readset, source hash, actor state or root hash is added to
  the public opportunity.
- `explicit_do_help(state, ...)` and CLI `do-help` are separate explicit user
  operations. They execute a real DO_HELP and report the projected result and
  encounter increment.
- WAIT/ABSENCE without an explicit interval input remain typed holds. No
  default activity or ACTUAL mode is selected.
- The original positive causal material evidence is preserved: ACTUAL material
  `0`, C9 `objective_material_eligible=false`; SCHEDULED_ONLY material `1`, C9
  `true`; cut/restore and cold continuity remain tested.

## Exact commands and results

Focused tests:

```text
SOROK_P2_BASE_ROOT=<checkout>/.local-logs/p2-explicit-interval-flow/base \
TMPDIR=<return>/logs/tmp \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=<return>/evidence/focused_tests.xml <return>/tests
```

Result: **6 passed** in `69.14s`, 0 failed/error/skipped. The affected tests now
assert no auto-help and no encounter mutation on observation, then call the
explicit do-help operation for the real admitted/refused user attempt.

CLI receipts (fresh process, clean env, `python3 -I -B`):

| Case | Observation | Encounters | Explicit `do-help` |
|---|---|---:|---|
| WAIT, no input | `HELD`, no advance | unchanged | not executed |
| ACTUAL, span 4 | `CONTINUED`; material `0`; C9 `false` | `0 → 0`, unchanged | `REFUSED` / `HELP_REFUSE`, `0 → 1` |
| SCHEDULED_ONLY, span 4 | `CONTINUED`; material `1`; C9 `true` | `0 → 0`, unchanged | `OK` / `HELP_ACCEPT`, `0 → 1` |

All observation and explicit-do-help paths report `cold_continuity: true`.
Interval reports preserve `actual_daily_events_invented: 0`,
`actor_knowledge_inferred: false`, `psychology_state_written: false`.

Dependency cut/restore remains covered: `S46_INTERVAL_CONDITION_REVOKED` on
admission after cut; restore continues, then explicit DO_HELP refuses under the
ACTUAL material result.

## Evidence

- `evidence/result.json` — PASS checks, repair metadata and authored-file hashes.
- `evidence/focused_tests.xml`, `logs/focused_tests.log` — 6 focused tests.
- `evidence/cli/hold-wait.json` — typed hold.
- `evidence/cli/continue-actual.json`, `continue-scheduled.json` — observation
  only, `do_help: null`, encounter count unchanged.
- `evidence/cli/do-help-actual.json`, `do-help-scheduled.json` — explicit user
  DO_HELP refused/accepted with encounter increment.
- Base product source manifest SHA-256 is recorded in `evidence/result.json`.

## Limitations

- TEST_ONLY sourcefree explicit continuation; not general autonomous absence
  life, native psychology, or a new actor/motive producer.
- Observation never executes a user attempt; explicit `do-help` is a separate
  user request only.
- Focused checks only; inherited full estate/full55 was not rerun.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority.
- Not independent acceptance. Historical `bdadbc57c...` remains immutable.

## Next receiving owner action

HQ/fan-in should consume this exact repair commit's observation-only API and
explicit `do-help` operation. Existing independent review of the repair commit
is required before any receiving acceptance. No protected write or PR697 merge
follows from this return.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: focused repair and evidence
only; no PROGRAMMA canonical product, seam/gate register, native science or
receiving authority changed.

## Publication

Branch: `codex/sorok-p2-explicit-interval-flow-20261105-r1`. Exact repair commit
and pushed SHA: `PUBLICATION_RECEIPT.json`.
