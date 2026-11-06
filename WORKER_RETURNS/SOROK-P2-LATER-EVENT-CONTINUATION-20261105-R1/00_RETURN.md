# SOROK P2 later-event continuation — public-boundary repair

**RESULT:** `P2_LATER_EVENT_CONTINUATION__PUBLIC_PRIVACY_AND_EXPLICIT_DO_HELP_REPAIR__PASS__8_FOCUSED_TESTS__TEST_ONLY_SOURCEFREE__NOT_NATIVE`.

**Grade:** `TEST_ONLY_SOURCEFREE_P2_LATER_EVENT_CONTINUATION_NOT_NATIVE`.

**Repair base:** `76fdb624afc7674f088d10c349bfe15ffd0b865a` (historical, immutable).
**Reviewer:** `f1a2872487b3aa492632a497ad7481e8529d937e`.
**Accepted product base:** `41bf45813fd0adeffd9b54e1306c2022abe96514` (unchanged).

This repair addresses the two exact reviewer findings against `76fdb624a`:

1. Public CLI/report privacy: positive/scheduled output no longer prints internal
   `c9`/`s43`/plan/source/history/readset/root engineering fields.
2. Auto user attempt: positive/scheduled observation no longer calls
   `project_do_help()`. DO_HELP is a separate explicit operation/flag.

No product, vendor, projection, fan-in, lifecycle, interval producer,
PROGRAMMA working file or protected branch was edited. PR697 remains unchanged
and unmerged.

## Preserved causal primitives

Unchanged and compatible:

- `P2Continuation.produce_input_interval(mode, span)`
- `P2Continuation.admit_later_event(history_refs, ...)`
- `P2Continuation.read_later_event(event_ref)`
- `cold_read(state_root, event_refs)`

The real S41/S42/S43 producer/reader and S47 C9 source semantics are unchanged.
The interval is still the existing S46 input; no motive, rule, weight, world
schedule or lifecycle was added.

## Public versus privileged engineering output

Public allowlisted API/CLI now provides:

- `public_report(report)` — public interval summary + projected `view` +
  `opportunity` + only explicitly executed projected actions.
- `run_positive_public(...)`, `run_scheduled_public(...)`.
- `public_cut_restore_report(report)`, `public_cold_report(report)`.
- `privacy_hits(value)` using the shipped projection `PRIVATE_KEYS` and
  `FORBIDDEN_VALUE_MARKERS`.
- CLI `positive`, `scheduled`, `cut-restore`, `cold`, `admit`, `verify` default
  to public summaries. `--engineering-out PATH` writes the full privileged
  engineering report separately.

Public outputs contain **0** projection privacy-walker hits. The full
engineering evidence is retained only in `*_engineering.json` files and the
primitive return values.

## Explicit DO_HELP

Observation/default execution never manufactures a user attempt:

- `positive`/`scheduled` without actions: `do_help: null`,
  `do_help_executed: false`, `encounter_count_before_action: 0`,
  `encounter_count_after_action: 0`.
- Explicit `--do-help` (or `project_do_help()` called by the caller) executes
  the real user attempt:
  - ACTUAL: `REFUSED` / `HELP_REFUSE`, encounters `0 -> 1`.
  - SCHEDULED_ONLY: `OK` / `HELP_ACCEPT`, encounters `0 -> 1`.
- Explicit `--say` and `--attend` flags are similarly opt-in; attend remains
  presentation-only.

## Original independent oracle reproduction

Historical `76fdb624a` CLI and primitive were re-run from a git-archive
snapshot under `.local-logs/p2-later-repair/oracle-snapshot`:

- Old CLI positive: auto `do_help` present, encounter count `3`.
- Old CLI positive privacy: `59` hits with the shipped private-key walker
  (reviewer reported `61` with a broader walker; same defect class reproduced).
- Old primitive: interval + two later events yielded `0` encounters and no
  DO_HELP, confirming the primitive itself was sound.
- Repaired CLI public default: `0` privacy hits, no `do_help`, encounters `0`.
- Repaired CLI explicit `--do-help`: `0` privacy hits, `REFUSED`/`HELP_REFUSE`,
  encounters `0 -> 1`.
- Scheduled repaired public: `0` privacy hits, no auto DO_HELP; explicit action
  accepted.

Receipt: `evidence/oracle_reproduction.json`.

## Focused tests and evidence

```text
SOROK_P2_BASE_ROOT=<checkout>/.local-logs/p2-later-repair/base \
TMPDIR=<return>/logs/tmp PYTHONPATH=<return> PYTHONDONTWRITEBYTECODE=1 \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=<return>/evidence/junit.xml <return>/tests
# 8 passed in 150.90s, exit 0
```

Coverage includes: positive later-event chain, named producer/first consumers,
same-root scheduled control, observation with no auto user action and zero
encounters, public privacy zero, explicit DO_HELP refusal/acceptance with
encounter increment, interval cut/refusal/restore, cold/source-intact, and CLI
public default plus explicit action.

Evidence:

- `evidence/junit.xml`, `logs/pytest-repair.log` — 8 focused tests.
- `evidence/test_run_repair.json` — exact test receipt.
- `evidence/positive_public.json`, `positive_action_public.json` — public reports.
- `evidence/positive_engineering.json`, `positive_action_engineering.json` —
  privileged engineering reports (separate by filename).
- `evidence/scheduled_public.json`, `scheduled_action_public.json`,
  `scheduled_engineering.json`, `scheduled_action_engineering.json`.
- `evidence/cut_restore_public.json`, `cut_restore_engineering.json`.
- `evidence/cold_public.json`, `cold_engineering.json`.
- `evidence/cli/positive-default.json`, `positive-action.json`,
  `scheduled-default.json`, `cut-restore.json`, `cold.json`.
- `evidence/oracle_reproduction.json`, `evidence/source_manifest_repair.json`.
- Historical `76fdb` engineering files (`positive.json`, `scheduled.json`,
  `cut_restore.json`, `cold.json`, `verify_positive.json`) remain as old
  evidence; the historical JUnit is preserved as
  `evidence/legacy_76fdb_junit.xml`. The repair uses the new
  `*_public`/`*_engineering` files and `evidence/junit.xml` receipt.

## Limits and holds

- TEST_ONLY sourcefree later-event continuation; B remains a fixture coactor,
  not an owned current B context or independent counterpart.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human validation, external
  delivery or paid action.
- No inherited full55 suite rerun; focused repair checks only.
- Reviewer-reported privacy hit count was 61 under their walker; the shipped
  walker reproduces 59 on the historical CLI, with the same private fields.
- This is implementer evidence, not self-acceptance or independent acceptance.
  Historical `76fdb624a` remains immutable.

## Next owner action

The independent reviewer or HQ fan-in should consume the public API/CLI
(`run_positive_public`, `run_scheduled_public`, `public_report`, explicit
`--do-help`) and inspect the new repair commit. Independent re-review of this
exact commit is required before receiving acceptance or protected writes.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: focused public-boundary and
explicit-action repair only; no PROGRAMMA canonical product, seam/gate register,
native science or receiving authority changed.

## Publication

Branch: `codex/sorok-p2-later-public-boundary-repair-20261105-r1`.
Repair commit: `4bdba46c4d3a667a9cd7845eb57caa980df76373`.
Final pushed head and receipt: `PUBLICATION_RECEIPT.json`.
