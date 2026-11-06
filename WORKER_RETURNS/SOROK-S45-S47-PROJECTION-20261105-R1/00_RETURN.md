# SOROK — bounded S45→WP19 projection/CLI contract, package-closure integrated

**RESULT:** `S45_WP19_PROJECTION_CLI_CONTRACT__ACTUAL_SAY_DO_HELP_ATTEND_PROJECTED__USER_ATTEMPT_SEPARATE_FROM_ACTOR_PERFORMANCE__ACTUAL_REFUSAL_AND_UNKNOWN__LOCAL_EXIT__HIDDEN_ACTOR_HISTORY_SOURCE_ABSENT__PACKAGE_IMPORT_CLOSURE_WIRED__11_PROJECTION_TESTS_PASS__NO_SECOND_UI__NO_ORIGINAL_PINNED_SOURCE_EDIT`.

This return implements the bounded projection/CLI integration contract and now consumes the shipped S45-S47 product import closure by default. It renders actual pinned S45 encounter results through the existing pinned WP19/S11 encounter surface. It does not perform S46/S47 material-interval work or the separate causal harness; those are covered by the shipped package and package-mode harness.

## 0. Adjacent shipping unit

The shipping unit is all three adjacent return directories: the product import closure, this projection adapter, and the causal harness. The package return alone does not contain `s45_projection`; all three must ship and be reviewed together.

## 0a. Independent review status

Independent reviewer session `ses_e526dc569ffe67E2MTl0k6Y38V` accepted the adjacent package+projection+harness unit at `da97d2624486b783bf5c4f465b17fdcdea3af20a` with 11 projection tests, 22 harness checks, cold replay, privacy and source cut/restore. That acceptance is historical for the focused fix commit; the new code requires focused closure.

## 1. Scope and pins

- Worktree base history: package `e42faf01b57a9188f0cf75baaccfcd57edb07173`; projection public `39ff2c2d479d8ad71c156b01c168894527a486e4`; cherry-picked closure branch commit `4e9ebc85d78995e93a7fbace0ead78d703067244`.
- S45 source: `f26a138e20d53c809d611cf8d834ec647b0804bf` (`WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1`).
- WP19: `3c4df43f813cd0727feff04f620aa0bbd9a63026` (`WORKER_RETURNS/SOROK-WP19-ENCOUNTER-PROTOTYPE-R1`).
- S11: `faec7ce909c54664e85320534bdf744b9bc47d37` (`WORKER_RETURNS/SOROK-S11-ENCOUNTER-EXIT-SPEC-R1`).
- Package closure: `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1`, 424 exact source blobs including S45-S47, WP19 and S11.
- Grade: `TEST_ONLY_S45_WP19_PROJECTION_NOT_NATIVE`; sourcefree model premise, not native personhood, psychology or human acceptance.

## 2. Exact consumed callables

From package-pinned `s45.session.S45Session`:

- `.start` / `.open`
- `.say(text)`
- `.do_help()`
- `.attend()`
- `.read_encounters()`
- `.events()` and `.user_perceived_ids()`
- `.world()` and `.clock()`
- `.close()`

From pinned WP19: `wp19.interface.VIEW_SCHEMA`, `RESULT_SCHEMA`, `render_text(view)`.
From pinned S11: `02_WP19_CONSUMABLE_INTERFACE.json` for controls, hidden fields, missing producers and typed-hold labels.

The adapter entrypoint is `s45_projection.adapter.S45Projection`; pure projection entrypoints are `s45_projection.projection.project_result` and `project_view`. The machine contract is `ADAPTER_CONTRACT.json` (`SOROK_S45_WP19_PROJECTION_CONTRACT@1`).

## 3. Package import closure

- `s45_projection.runtime` finds the shipped product package, installs `sorok_s45_s47.bootstrap`, and resolves `s45`, `wp19` and the dependency chain from `product/vendor`.
- `s45_projection.adapter.S45Projection.open/start` and `s45_projection.cli.main` install that closure before importing pinned source.
- Tests in `tests/_pinned.py` default to `mode=PACKAGE_CLOSURE` and use `product/vendor` directly. `S45_PROJECTION_USE_GIT=1` is an explicit fallback to independent git extraction.
- The single user-facing CLI is the product CLI: `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py`. Its `view`, `say`, `do-help`, `attend`, `status` and typed-hold commands use this adapter. `s45_projection.cli` remains the thin contract CLI used by tests.

## 4. Public surface

The projection emits the existing WP19 schemas:

- `SOROK_WP19_ENCOUNTER_VIEW@1`
- `SOROK_WP19_INTERACTION_RESULT@1`
- `SOROK_WP19_STATUS@1`

Control mapping:

| Control | Actual S45 producer | Public result |
|---|---|---|
| `SAY` | `S45Session.say` | `attempted=true`, `performed=false`; actual actor expression or actual `UNKNOWN` |
| `DO_HELP` | `S45Session.do_help` | `attempted=true`, `performed=false`; `actor_response.performed` true only for an actual admitted actor `REPAIR` action |
| `ATTEND` | `S45Session.attend` | actual `NO_CHANGE`, `LOCAL_ATTEND_ONLY`, no world event |
| `WAIT` | none | `WAIT_UNSUPPORTED_TYPED_HOLD`; no clock/event change |
| `EXIT` | local only | `LOCAL_EXIT_ONLY`; no actor/world event |
| `RETURN` | none | `RETURN_UNSUPPORTED_TYPED_HOLD` |
| `ABSENCE` | none | `UNKNOWN`, `USER_ABSENCE_LIFE_ADVANCE_MISSING` |

The user attempt is always separated from performance. `user_attempt.performed` is false; actor performance is reported only in `actor_response.performed` with `performed_by="A"`.

## 5. Actual observed outcomes

The tests exercise actual package-pinned S45 sessions, not canned success:

- `say("Can I help?")` → actual `HELP_INVITE`, exact native text plus exact labeled English; user attempt false performance.
- `do_help()` → actual `HELP_ACCEPT` with actual `REPAIR` action event; `user_attempt.performed=false`, `actor_response.performed=true`.
- Refusal fixture with zero material → actual `HELP_REFUSE`; projected `status=REFUSED`, no action, exact refusal speech/translation pair.
- Unsupported `say("What is the weather?")` → actual S45 `UNSUPPORTED`; projected `status=UNKNOWN`, no actor response, no fabricated silence.
- `attend()` → actual `NO_CHANGE`, no world event.
- `exit()` → local-only `LOCAL_EXIT_ONLY`; store hash unchanged, no world event.
- `wait` / `return` / `absence` → typed holds; store hash unchanged.
- Privacy walker passes for projected views/results; hidden/source/history fields remain absent.

## 6. Tests actually run

Package-closure projection/CLI suite:

```text
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/evidence/junit.xml \
  WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/tests
# 11 passed in 30.08s, exit 0
```

The suite verifies contract/pins, package source exactness, actual SAY attempt vs actor response, actual DO_HELP vs actor REPAIR, ATTEND `NO_CHANGE`, public-field privacy, actual refusal, actual unsupported `UNKNOWN`, typed holds/local exit, in-process CLI and subprocess CLI.

The prior pinned S45 author suite (21 passed) is retained in git history/prior evidence but was not rerun in this integration, per the no-duplicate-full-suite instruction. `evidence/test_run.json` records this honestly.

Evidence: `evidence/test_run.json`, `evidence/junit.xml`, `logs/pytest-evidence.log`; package copies at `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/evidence/PROJECTION_PACKAGE_TESTS.*`.

## 7. Limitations and non-claims

- S45 projection surface only. S46/S47 interval, event-local C9, cold/sever/restore evidence is in the shipped package demo and package-mode causal harness.
- No WAIT/time-advance, lawful return, absence/life-advance, message-channel or delivery producer is invented.
- No actor-private motive, history, source refs, access receipts, plan hashes or hidden state is exposed.
- No native CAN/ADP/C8/C9/C12/Pyat/A5 grant, human trial, production person claim or psychological rule is made.
- No second UI and no edits to pinned S45/S46/S47/S37/S42 source or original product behavior.
- Independent review and PRE-MAIN receiving remain separate holds.
