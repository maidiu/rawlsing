# SOROK P2 ENCOUNTER LIFECYCLE R1 — RETURN

## RESULT

`SOROK_P2_ENCOUNTER_LIFECYCLE__PERSISTENT_LOCAL_PORTAL_OUTSIDE__COLD_EXIT_REOPEN_LOCAL_RETURN__OUTSIDE_ACTION_BOUNDARY__ROOT_BOUND_LOCAL_STATE__FOCUSED_5_TESTS_PASS__TEST_ONLY_NOT_NATIVE`.

## BASE AND SCOPE

- Base: `41bf45813fd0adeffd9b54e1306c2022abe96514`, independently ACCEPTED scoped TEST_ONLY for the adjacent package+projection+harness unit.
- PR697 remains unchanged and unmerged.
- Branch: `codex/sorok-p2-encounter-lifecycle-20261105-r1`.
- Focused fix commit is this branch head; exact SHA is returned in the final chat readback. Parent is `41bf45813fd0adeffd9b54e1306c2022abe96514`.
- Assigned write scope only: `WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/`.
- No inherited product/vendor/projection edits, protected writes, global config changes, PROGRAMMA working-file changes, native rights, fabricated motives or B states.

## OBSERVED DEFECT AND FIX

The accepted `S45Projection` keeps `adapter.mode` only in memory and resets it to `PORTAL` on every CLI open, so a local `EXIT` did not survive a fresh command. Its `RETURN` also always reported the existing world-return hold.

This return adds an additive lifecycle wrapper and CLI around the accepted adapter:

- Local `PORTAL`/`OUTSIDE` mode is persisted in a sidecar at `<state_root>/.sorok_p2_local/encounter_lifecycle.json`.
- The sidecar is separate from the canonical actor/world store and records only local UI state, a monotonically increasing local sequence, last local action, and a root binding.
- Opening binds the sidecar to the current canonical root hash. A sidecar from another root is refused with `LOCAL_LIFECYCLE_ROOT_MISMATCH`; it cannot inherit `OUTSIDE`.
- `OUTSIDE` survives cold reopen and blocks `SAY`/`DO_HELP`/`ATTEND` before the real S45 callables are invoked.
- Local `RETURN` from `OUTSIDE` restores `PORTAL` without world time, world activity, delivery, actor reaction, or canonical store mutation.
- `RETURN` while already in `PORTAL` preserves the existing WP19/S11 world-return typed hold `RETURN_UNSUPPORTED_TYPED_HOLD`; no world-return producer is invented.

## ACTION SEMANTICS

| Local mode | Control | Result |
|---|---|---|
| `PORTAL` | `SAY` | existing WP19 result from `S45Projection.say` |
| `PORTAL` | `DO_HELP` | existing WP19 result from `S45Projection.do_help` |
| `PORTAL` | `ATTEND` | existing WP19 result from `S45Projection.attend` (`NO_CHANGE`) |
| `PORTAL` | `EXIT` | existing `LOCAL_EXIT_ONLY`; sidecar becomes `OUTSIDE`; no world/store mutation |
| `PORTAL` | `RETURN` | existing WP19 `HELD` / `RETURN_UNSUPPORTED_TYPED_HOLD` |
| `OUTSIDE` | `SAY`/`DO_HELP`/`ATTEND` | local result `REFUSED` / `LOCAL_OUTSIDE_MODE_BLOCKED`; actor_response `null`; no clock/world/delivery |
| `OUTSIDE` | `RETURN` | local result `OK` / `LOCAL_RETURN_ONLY`; sidecar becomes `PORTAL`; no actor/world mutation |
| `OUTSIDE` | `VIEW` | existing WP19 view with `mode=OUTSIDE`; privacy preserved; no fabricated absence activity |

The outside-mode refusal is a local UI boundary, not an actor refusal and not a world `UNKNOWN`. `UNKNOWN` and privacy remain owned by the existing WP19 projection. No `WAIT`, absence/life-advance, external delivery, or world-return producer is added.

## MISSING PRODUCERS / NON-CLAIMS

The existing S11 missing producers remain missing and are not fabricated:

- `WAIT_TIME_ADVANCE_RECEIPT`
- `PORTAL_EXIT_RETURN_RECEIPT`
- `USER_ABSENCE_LIFE_ADVANCE`
- `MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY`
- `ACCESSIBILITY_PREFERENCE_ACK`

`LOCAL_RETURN_ONLY` is a local UI mode transition, not `PORTAL_EXIT_RETURN_RECEIPT`. No actual elapsed life, absence activity, delivery, human usability, native C8/C9/C12, CAN008/CAN011, ADP, Pyat or B positive is claimed.

## CODE AND CLI

- `sorok_p2_lifecycle/lifecycle.py`: `LifecycleEncounter`, `LifecycleRefusal`, persistent sidecar, action boundary, local return.
- `sorok_p2_lifecycle/runtime.py`: read-only installation of the shipped package closure and accepted projection adapter.
- `sorok_p2_lifecycle/cli.py` and `run_lifecycle_cli.py`: additive user-facing lifecycle CLI.
- Commands: `new`, `view [--text]`, `say`, `do-help`, `attend`, `exit`, `return`, `status`, `lifecycle`.

Usage:

```text
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py new --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py view --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py say --state <path> "Can I help?"
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py do-help --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py attend --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py exit --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py return --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py status --state <path>
python3 WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/run_lifecycle_cli.py lifecycle --state <path>
```

## EXECUTED EVIDENCE

Focused tests, run with pytest temporary staging under the checkout `.local-logs`:

```text
TMPDIR=$PWD/.local-logs/sorok-p2-encounter-lifecycle-20261105-r1/pytest-tmp \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/evidence/focused_lifecycle.xml \
  WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/tests
# 5 passed in 20.61s, exit 0
```

Covered:

1. Positive `SAY`/`DO_HELP`/`ATTEND` through the real accepted S45 projection.
2. Cold `EXIT` -> fresh reopen `OUTSIDE` -> blocked actions -> local `RETURN` -> access restored.
3. Canonical store hash unchanged across `EXIT` and local `RETURN`.
4. Another root cannot inherit persisted `OUTSIDE` (`LOCAL_LIFECYCLE_ROOT_MISMATCH`).
5. Sidecar cut resets to `PORTAL`; sidecar restore recovers `OUTSIDE` cold.
6. Fresh CLI subprocess sequence: `new`, `exit`, cold `view`/`status`, blocked `say`, `return`, permitted `say`, `lifecycle`.
7. Privacy walker: `new`, views, WP19 results, local results and public lifecycle state expose no `root_hash`, private keys or forbidden markers.

Evidence:

- `evidence/test_run.json`
- `evidence/focused_lifecycle.xml`
- `logs/focused_lifecycle.log`
- `evidence/cli_sequence.json`
- `evidence/cli/` (18 cold CLI receipts)
- `evidence/lifecycle_refusals.json`

CLI cold sequence result: modes `PORTAL -> OUTSIDE -> PORTAL`; canonical store hash unchanged; blocked `SAY`/`DO_HELP`/`ATTEND` all `LOCAL_OUTSIDE_MODE_BLOCKED` with `actor_response=null`, `world_event_created=false`, `clock_changed=false`; local return `LOCAL_RETURN_ONLY`; subsequent `SAY` is a real WP19 result again.

Refusal/cut evidence: foreign-root sidecar refused `LOCAL_LIFECYCLE_ROOT_MISMATCH`; removing the sidecar resets cold mode to `PORTAL`; restoring it recovers `OUTSIDE`.

## LIMITS

- TEST_ONLY local UI lifecycle; not native psychology, not a world-return producer, not human validation.
- No actual elapsed life, no fabricated absence activity/time/delivery, no actor reaction outside mode.
- The inherited 55-test full estate was not rerun.
- This new code has no independent acceptance yet; it requires focused review.
- No PROGRAMMA working files or inherited return directories were altered.
