# SOROK — bounded S45→WP19 projection/CLI contract and tests

**RESULT:** `S45_WP19_PROJECTION_CLI_CONTRACT__ACTUAL_SAY_DO_HELP_ATTEND_PROJECTED__USER_ATTEMPT_SEPARATE_FROM_ACTOR_PERFORMANCE__ACTUAL_REFUSAL_AND_UNKNOWN__LOCAL_EXIT__HIDDEN_ACTOR_HISTORY_SOURCE_ABSENT__11_PROJECTION_TESTS_AND_21_PINNED_S45_AUTHOR_TESTS__NO_SECOND_UI__NO_ORIGINAL_PRODUCT_EDIT`.

This return implements only the bounded projection/CLI integration contract requested by the whole-person receiving commission. It consumes actual pinned S45 encounter results and renders them through the existing pinned WP19/S11 encounter surface. It does not perform import closure, S46/S47 material-interval work, or the separate causal harness.

## 1. Scope and pins

- Worktree base: `078d9c57bc835a34e90b3671bdef6c28a0f43747`.
- S45 source: `f26a138e20d53c809d611cf8d834ec647b0804bf` (`WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1`).
- Existing encounter surface: WP19 `3c4df43f813cd0727feff04f620aa0bbd9a63026` (`WORKER_RETURNS/SOROK-WP19-ENCOUNTER-PROTOTYPE-R1`) and S11 `faec7ce909c54664e85320534bdf744b9bc47d37` (`WORKER_RETURNS/SOROK-S11-ENCOUNTER-EXIT-SPEC-R1`).
- All three pinned sources are extracted from Git objects at test time into `.local-logs/s45-projection-runtime`; no original product file is edited.
- Grade: `TEST_ONLY_S45_WP19_PROJECTION_NOT_NATIVE`; sourcefree model premise, not native personhood, psychology or human acceptance.

## 2. Exact consumed callables

From pinned `s45.session.S45Session`:

- `.start` / `.open`
- `.say(text)`
- `.do_help()`
- `.attend()`
- `.read_encounters()`
- `.events()` and `.user_perceived_ids()`
- `.world()` and `.clock()`
- `.close()`

From pinned WP19:

- `wp19.interface.VIEW_SCHEMA` / `RESULT_SCHEMA`
- `wp19.interface.render_text(view)` for the CLI text view

From pinned S11:

- `02_WP19_CONSUMABLE_INTERFACE.json` for portal controls, hidden fields, missing-producer identities and typed-hold labels.

The adapter entrypoint is `s45_projection.adapter.S45Projection`; pure projection entrypoints are `s45_projection.projection.project_result` and `project_view`. The explicit machine-readable contract is `ADAPTER_CONTRACT.json` (`SOROK_S45_WP19_PROJECTION_CONTRACT@1`).

## 3. Public surface

The projection emits the existing WP19 schemas:

- `SOROK_WP19_ENCOUNTER_VIEW@1`
- `SOROK_WP19_INTERACTION_RESULT@1`
- `SOROK_WP19_STATUS@1`

Control mapping:

| Control | Actual S45 producer | Public result |
|---|---|---|
| `SAY` | `S45Session.say` | `attempted=true`, `performed=false`; actual actor expression or actual `UNKNOWN` |
| `DO_HELP` | `S45Session.do_help` | `attempted=true`, `performed=false`; `actor_response.performed` is true only for an actual admitted actor `REPAIR` action event |
| `ATTEND` | `S45Session.attend` | actual `NO_CHANGE`, `LOCAL_ATTEND_ONLY`, no world event |
| `WAIT` | none | `WAIT_UNSUPPORTED_TYPED_HOLD`; no clock/event change |
| `EXIT` | local only | `LOCAL_EXIT_ONLY`; no actor/world event |
| `RETURN` | none | `RETURN_UNSUPPORTED_TYPED_HOLD` |
| `ABSENCE` | none | `UNKNOWN`, `USER_ABSENCE_LIFE_ADVANCE_MISSING` |

The user attempt is always separated from performance. `user_attempt.performed` is false; actor performance is reported only in `actor_response.performed` with `performed_by="A"`.

## 4. Actual observed outcomes

The tests exercise actual pinned S45 sessions, not canned success:

- `say("Can I help?")` → actual `HELP_INVITE`, exact native text plus exact labeled English; user attempt false performance.
- `do_help()` → actual `HELP_ACCEPT` with actual `REPAIR` action event; `user_attempt.performed=false`, `actor_response.performed=true`.
- Refusal fixture with zero material → actual `HELP_REFUSE`; projected `status=REFUSED`, no action, exact refusal speech/translation pair from the pinned S45 language pairs.
- Unsupported `say("What is the weather?")` → actual S45 `UNSUPPORTED`; projected `status=UNKNOWN`, no actor response, no fabricated silence.
- `attend()` → actual `NO_CHANGE`, no world event.
- `exit()` → local-only `LOCAL_EXIT_ONLY`; store hash unchanged, no world event.
- `wait` / `return` / `absence` → typed holds; store hash unchanged.

Public views contain only user-perceived world events and whitelisted observable event fields. Omitting `source_event_refs`, `access_receipt_ids`, `admission_id`, `plan_hash`, `contract_hash`, `c9`, `world_before`, `history_refs`, `generation_source_refs`, actor state, root hash/ID, encounter IDs and raw LME data. Unperceived events are represented only by an integer count and remain `UNKNOWN`.

## 5. Tests actually run

Projection/CLI suite from this return:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m pytest -q \
  -p no:cacheprovider --junitxml=evidence/junit.xml tests
# 11 passed in 27.59s, exit 0
```

The suite verifies:

1. contract pins and WP19/S11 semantic identity;
2. extracted pinned files match their Git blobs;
3. actual SAY attempt vs actor response;
4. actual DO_HELP attempt vs actor REPAIR;
5. actual ATTEND `NO_CHANGE`;
6. public view fields and hidden/source absence;
7. actual refusal preservation;
8. actual unsupported `UNKNOWN`;
9. local exit and non-fictional typed holds;
10. in-process CLI end-to-end;
11. subprocess `python -m s45_projection.cli` on pinned source.

Pinned S45 author suite was also rerun from the extracted pinned tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m pytest -q \
  -p no:cacheprovider --junitxml=evidence/s45_author_junit.xml tests
# 21 passed in 118.56s
```

Evidence: `evidence/test_run.json`, `evidence/junit.xml`, `evidence/s45_author_junit.xml`, `evidence/source_manifest.json`, `logs/pytest-evidence.log`, `logs/pinned-s45-author-tests.log`.

## 6. CLI

Runnable contract:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<return>:<pinned-s45-return> \
python3 -B -m s45_projection.cli --root <state-root> --start view
```

Commands: `view [--text]`, `say TEXT`, `do-help`/`do`, `attend`, `wait`, `exit`, `return`, `absence`, `status`, `demo`. Output is JSON; `view --text` uses pinned WP19 `render_text`. The CLI is a thin wrapper over the same projected surface, not a second UI.

Demo evidence: `evidence/cli_demo.json` (actual view, SAY, DO_HELP, ATTEND, EXIT, WAIT, RETURN, ABSENCE, STATUS).

## 7. Limitations and non-claims

- S45 only. S46/S47 material interval, event-local C9 conditioning, import closure and the separate causal harness remain with their owners.
- No WAIT/time-advance, lawful return, absence/life-advance, message-channel or delivery producer is invented.
- No actor-private motive, history, source refs, access receipts, plan hashes or hidden state is exposed.
- No native CAN/ADP/C8/C9/C12/Pyat/A5 grant, human trial, production person claim or psychological rule is made.
- No second UI and no edits to original product code.
- The CLI requires the caller/main receiving package to provide pinned S45 and WP19/S11 source on `PYTHONPATH`; this return deliberately does not own import closure.
