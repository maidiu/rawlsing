# R12 hostile G5 correction — 2026-11-20

**Reviewed base:** `9db0e6f64bf568409e638ff2215af8b8a414487f`
**Scope:** sourcefree hostile review correction; not independent acceptance, native authority, or protected receiving.

## Finding

The R12 `ADD_PROJECT` guard passed the six imported R11 reviewer tests, but the broader current-trial project-motive boundary was still bypassable with `REORGANIZE_PROJECT`. A pre-existing neutral project could be relabeled with a mature motive during the issued current-trial event while the possible end remained `POSSIBLE_NOT_ACQUIRED_MOTIVE`.

Pre-fix runtime observation:

```text
project_after_add    motive=NEUTRAL_ORDINARY
trial_event_outcome  COMMITTED
project_after_trial  motive=MATURE_RHYTHM_MOTIVE_FROM_CURRENT_TRIAL
end_status           POSSIBLE_NOT_ACQUIRED_MOTIVE
trial_history_len    1
verify               valid
```

## Correction

- `development.admit` rejects `ADD_PROJECT` and `REORGANIZE_PROJECT` whenever `issued_trial` is present, and rejects any `TAKE_UP_POSSIBLE_END` in that event.
- `storage.verify_chain` emits typed `WORLD_SNAPSHOT_NOT_OBJECT` / `ACTOR_SNAPSHOT_NOT_OBJECT` errors for canonical non-object snapshots.
- `constitution.compose` sorts the qualified active-form closure; fresh demo event ordering no longer depends on `PYTHONHASHSEED`.

Post-fix runtime observation:

```text
trial_event_outcome  REFUSED:InvalidDevelopment:CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT
project_after_trial  motive=NEUTRAL_ORDINARY
trial_history_len    0
verify               valid
```

## Regression tests

- `tests.test_r12_independent_review_repairs.TrialPurposeAuthorityR12.test_current_trial_cannot_reorganize_existing_project_into_motive`
- `tests.test_r12_independent_review_repairs.HostileG5Continuity.test_canonical_nonobject_world_and_actor_snapshots_are_typed_red`

## Execution on Python 3.11.3

```text
python3.11 -m unittest discover -s tests -q         248 tests OK
python3.11 -O -m unittest discover -s tests -q      248 tests OK
python3.11 -m pytest -q                             248 passed + 16 subtests
python3.11 -m unittest tests.test_independent_r11_receiving -v   6/6 OK
```

Fresh demo runs were identical across processes and `PYTHONHASHSEED` values: 9 events, last hash `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363`, `PRAGMA integrity_check=ok`, cold-reopen valid.

The original 246-test R12 receipt is preserved as a historical cut. All 71 P records and six E holds remain unchanged. R12 remains sourcefree author-tested and awaits distinct independent receiving.
