# SOROK P2 PRODUCT FANIN R1 — RETURN

## RESULT

`SOROK_P2_PRODUCT_FANIN__LIFECYCLE_ACCESS_BOUNDARY__EXPLICIT_INTERVAL__LATER_EVENT_SOURCE_BOUND_CONTINUATION__ONE_S47_ROOT__COLD_CLI__ATTEMPT_VS_OBSERVATION__6_FOCUSED_TESTS_PASS__TEST_ONLY_NOT_NATIVE_NOT_INDEPENDENTLY_ACCEPTED`.

## BASE AND EXACT SOURCES

- Base accepted: `41bf45813fd0adeffd9b54e1306c2022abe96514` (independent ACCEPT scoped TEST_ONLY; PR697 unchanged/unmerged).
- Lifecycle source: `79b90e4a57cbd1b738a9b9484677736d1b6415ab`; independent ACCEPT review commit `6398888f1d28152b5d29fef816f0bb45e77dd43b`. Imported directory tree `1eda53e475f5e07c1251a6f61eacecacc1284ed6`.
- Explicit interval source: public-key/census repair `76d5a3d13e0219c1a085ebadd55071de2dd90e7d`, built on primary repair `7a256ed4` and historical `bdadbc57c...`. Imported directory tree `f7bd1c51f5420c83970487d5163d585a5c4e9e2c`.
- Primary no-auto-help repair is independently `PASS` at closure `89b33453eff13d8a3638a97cf516438c42e7af4f`; the remaining public-key rename/census fix in `76d5a3d` is `AUTHOR_TESTED` pending independent review. The independent integrated review currently covers exact `25d40806` (old interval import), not this refreshed fanin head.
- Historical bdad interval/fanin auto-DO_HELP defect evidence and the prior `89b334` REVISE closure remain preserved in Git history and in `evidence/upstream_interval_auto_do_help.json`. The new secondary repair is author-tested only; no acceptance promotion.
- Later-event source: public-boundary repair `b71624f21d0bc638e8817f3929cc6c01ab8b0f61` (code `4bdba46c4d3a667a9cd7845eb57caa980df76373`), imported tree `67f01db82c3722f6d5dcf98da722872db909a237`, 48 files. Historical `76fdb624` remains original `REVISE`; repair author evidence is 8 passed in 150.90s, independent closure running.
- Existing integrated cut `25d40806` is independently `ACCEPT_SCOPED_TEST_ONLY` at `332e00cb3da51b859a408a31f820b1afd7fe8fc0`; that exact scope is preserved and is not acceptance of this newer head.
- All three new `WORKER_RETURNS` directories were imported byte-exactly from those Git trees, with their evidence preserved. No accepted base/vendor/projection/PR697/programma working file was edited.
- New integration code/tests/evidence only under `WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/`.

Branch: `codex/sorok-p2-product-fanin-20261105-r1`. The focused fanin commit is this branch head; exact SHA is returned in the final chat readback. Parent is `41bf45813fd0adeffd9b54e1306c2022abe96514`.

## ACTUAL THROUGHLINE

One compatible `S47Session` root is opened by every command. The lifecycle wrapper is constructed around `S45Projection` over that S47 session, preserving the accepted local `PORTAL`/`OUTSIDE` boundary. Interval input uses the exact imported interval return. Later-event admission/read uses the exact imported later-event return. There is no second S45-only root and no new demo wrapper.

Callable/CLI entrypoint:

```text
python3 WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/run_fanin_cli.py <command> --state <path>
```

Commands: `new`, `view [--text]`, `say`, `do-help`, `attend`, `exit`, `return`, `status`, `lifecycle`, `interval --mode ... [--start] [--span]`, `later-event [--history-ref ...]`, `opportunity --event-ref ...`, `verify`.

## SEMANTICS

| Mode / command | Behavior |
|---|---|
| `PORTAL` `SAY`/`DO_HELP`/`ATTEND` | existing WP19 result through accepted `S45Projection` |
| `PORTAL` `EXIT` | existing `LOCAL_EXIT_ONLY`; lifecycle sidecar becomes `OUTSIDE`; no canonical actor/world mutation |
| `OUTSIDE` `SAY`/`DO_HELP`/`ATTEND` | `LOCAL_OUTSIDE_MODE_BLOCKED` before real S45 calls; no actor response, world event, clock change or delivery |
| `OUTSIDE` `RETURN` | `LOCAL_RETURN_ONLY`; restores `PORTAL`; no canonical actor/world mutation |
| `PORTAL` `RETURN` | existing `RETURN_UNSUPPORTED_TYPED_HOLD` |
| `interval --mode M` | explicit supplied interval through `p2_explicit_interval_flow.apply_explicit_interval`; no WAIT/absence auto-advance and no DO_HELP execution |
| `later-event` | real S43/S42 later-event admission and read; outputs an opportunity observation only, with `do_help_executed=false` |
| `opportunity --event-ref` | read-only later-event observation; no user attempt |
| `do-help` | only command that performs an explicit user DO_HELP attempt |

The supplied interval is not a user-WAIT/absence choice. It is an explicit interval input; the existing producer decides actual material participation. No autonomous absence life, world return, delivery or actor reaction is fabricated.

`OUTSIDE` blocks only the user encounter actions `SAY`/`DO_HELP`/`ATTEND`. Explicit `interval` and `later-event` are producer/world continuation inputs, not user encounter actions, and are never executed automatically by `exit` or `return`.

## ATTEMPT VERSUS OBSERVATION

This integration does not auto-execute user `DO_HELP` to show a predicted consequence. The later-event repair `b71624f` separates allowlisted public output from privileged engineering output (`*_engineering` / `--engineering-out`) and keeps DO_HELP as a separate explicit request. Fanin still uses only the preserved `P2Continuation.admit_later_event/read_later_event` primitives, performs its own internal engineering reads, and emits its existing `public_opportunity` allowlist; it does not import the standalone later CLI or its privileged evidence. The interval repair's reserved-key/census fix is also imported. Evidence: `evidence/later_refresh_oracle.json`, `evidence/later_public_boundary_repair_status.json`, `evidence/upstream_interval_auto_do_help.json`.

Fanin uses only:

- `p2_explicit_interval_flow.continuation.apply_explicit_interval` for the explicit interval.
- `p2_continuation.continuation.P2Continuation.admit_later_event/read_later_event` for the real later event and source-bound expression/C9 observation.
- The accepted lifecycle `SAY`/`DO_HELP`/`ATTEND` only on explicit CLI commands.

The cold CLI evidence proves encounter count remains `0` after interval, later-event observation and opportunity read, then becomes `1` only after explicit `do-help`.

## EXACT EXECUTED EVIDENCE

Focused tests:

```text
TMPDIR=$PWD/.local-logs/sorok-p2-product-fanin-20261105-r1/pytest-tmp \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/evidence/focused_fanin.xml \
  WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/tests
# 7 passed in 71.86s, exit 0
```

The refreshed interval return carries its own author evidence: **6 passed in 78.34s** at `76d5a3d`, with the original public privacy/receipt oracle PASS. Fanin did not rerun those tests or the 7 fanin tests because the fanin callsite is unchanged; the prior 7-fanin evidence `7 passed in 71.86s` is reused. Historical `7a256ed4` interval evidence (`6 passed in 76.97s`) is retained separately.

Covered:

0. Loaded repaired interval module is the refreshed return source; `admit_continuation` has no `adapter.do_help()`, while `explicit_do_help` does.
1. Same compatible S47 root across start/interval/later-event/cold reopen.
2. ACTUAL interval material `1 -> 0`; later event C9 `objective_material_eligible=false`; S43 expression `ACCEPTED`.
3. Observation of later opportunity does not increment encounters; explicit DO_HELP then refuses with `HELP_REFUSE`.
4. SCHEDULED_ONLY interval retains material `1`; observation does not auto-help; explicit DO_HELP is `HELP_ACCEPT`.
5. `OUTSIDE` cold reopen blocks `SAY`/`DO_HELP`/`ATTEND` before real S45 calls; local return restores without store/clock/event changes.
6. Interval condition cut refuses later admission with `S46_INTERVAL_CONDITION_REVOKED`; restore admits; cold C9 source hash persists.
7. Unsupported SAY is `UNKNOWN`; missing/invalid interval input is HELD/REFUSED without advance.
8. Privacy walker on views/action results/opportunity/local state/verify has no `root_hash`, `root_id`, private keys or forbidden markers.

Cold CLI sequence (17 fresh commands):

- `new -> interval ACTUAL -> verify -> later-event -> opportunity -> verify -> do-help -> verify -> attend -> say UNKNOWN -> exit -> blocked say -> return -> say -> status -> verify`.
- Encounter counts: after interval `0`, after later observation `0`, after opportunity read `0`, after explicit DO_HELP `1`.
- ACTUAL interval `PARTIAL`, coverage `[[222,223]]`, material `0`.
- Later observation and opportunity read: `event_status=OK`, `c9_material_eligible=false`, `language_status=ACCEPTED`, `do_help_executed=false`, `user_attempt=false`.
- Explicit DO_HELP: `REFUSED`, `attempted=true`, `performed=false`, `refusal=true`.
- ATTEND: `NO_CHANGE`, `world_event_created=false`, `clock_changed=false`, `performed=false`.
- Outside: blocked SAY `LOCAL_OUTSIDE_MODE_BLOCKED`, `actor_response=null`; local return `LOCAL_RETURN_ONLY`; then real WP19 SAY result again.
- Final status `PORTAL`, verify `ok=true`; no `root_hash` in public `new`/later-event/status/verify outputs.

Cut/restore evidence: `evidence/cut_restore.json` records cut code, unchanged event count, restored source hash `e196c974...`, later C9 source in readset, no auto DO_HELP, and cold source/root verification.

Evidence:

- `evidence/test_run.json`, `evidence/focused_fanin.xml`, `logs/focused_fanin.log`
- `evidence/cli/` (17 cold command receipts plus `summary.json`)
- `evidence/cut_restore.json`
- `evidence/upstream_interval_auto_do_help.json` (historical defect + interval repair status)
- `evidence/later_refresh_oracle.json`, `evidence/later_public_boundary_repair_status.json`
- `evidence/later_public_boundary_focused.xml`, `logs/later_public_boundary_focused.log`
- `evidence/later_public_boundary_test_run.json`, `evidence/later_public_boundary_oracle.json`, `evidence/later_public_boundary_source_manifest.json`
- `evidence/interval_public_receipt_focused.xml`, `logs/interval_public_receipt_focused.log` (76d5a3d author tests)
- `evidence/interval_public_receipt_repair_tests.json`, `evidence/interval_refresh_oracle.json`
- `evidence/interval_repair_focused.xml`, `logs/interval_repair_focused.log` (historical 7a256 tests)
- `evidence/source_manifest.json` (fanin files plus exact imported-tree hashes)
- `PR_READY_RECEIVING_DESCRIPTION.md` (HQ receiving description; no merge permission)

## NOT RUN / HOLDS

- No independent review of this refreshed fanin commit.
- Primary interval no-auto-help repair is independently PASS at `89b334`; secondary public-key/census repair `76d5a3d` is AUTHOR_TESTED only, pending independent review.
- Later-event `76fdb624` original `REVISE` and public-CLI limits remain historically preserved; repair `b71624f` is AUTHOR_TESTED with independent closure still running.
- Independent integrated review currently covers exact `25d40806` (old interval/later imports), not this refreshed head.
- No routine rerun of unchanged fanin tests/CLI after later primitive API preservation; 8 later author tests and prior 7 fanin tests are reused.
- Inherited full 55-test estate was not rerun.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human usability, B-owned context or paid action is claimed.
- No actual elapsed life, absence activity, delivery, world return or external message channel is claimed.
- No protected merge, PR697 merge or PROGRAMMA working-file edit.
