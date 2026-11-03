# SOROK WP-19 — runnable bounded encounter interface

**RESULT:** `WP19_RUNNABLE_BOUNDED_ENCOUNTER_INTERFACE__REAL_CP_A5_AND_JOIN_E_READERS__ACCESSIBLE_VIEW__LOCAL_EXIT__TYPED_RETURN_HOLD__HIDDEN_STATE_HELD__7_TESTS__NO_INVENTED_A_RESPONSE__NO_TIME_ADVANCE__NO_NATIVE_OR_HUMAN_CLAIM`.

This is a bounded low-fidelity interface over the pinned S11 specification. It reads real CP-A5 and JOIN-E read-side outputs; it does not use canned success. It is not a native, scientific or human-accepted product.

## 1. Base and sources

- Base: `faec7ce909c54664e85320534bdf744b9bc47d37` (S11).
- S11 spec consumed: `WORKER_RETURNS/SOROK-S11-ENCOUNTER-EXIT-SPEC-R1/02_WP19_CONSUMABLE_INTERFACE.json`, SHA-256 `ad4add0d10aadf3ebdb4f30ff36d30da0f0e9356e9c5ca714c6e0e55b3071619`.
- JOIN-E source: `5e63672543973ce2533129e1ca3224d82af0dffc`.
- CP-A5 source: `913765328e4fab12b150ea01421ed6b445158184`.
- Exact JOIN-E/CP-A5 evidence identities: `evidence/source_manifest.json`.

Both source trees are extracted from Git objects at runtime into `.runtime/` and are gitignored. The S35 branch and its untracked artifacts were not modified.

## 2. Implemented

- `wp19/spec.py` — loads the pinned S11 WP-19 consumable JSON.
- `wp19/sources.py` — extracts pinned JOIN-E/CP-A5 sources with `git archive`; runs the real readers; hashes stores.
- `wp19/join_e_probe.py` — starts/opens a real JOIN-E `JoinedSession`/`RefusalSession`, calls `do_help`, and returns persisted C12 events/perceptions/help.
- `wp19/interface.py` — bounded encounter view and controls:
  - accessible observation from CP-A5 `EncounterReader.view/ask` and JOIN-E C12 perceptions;
  - hidden state omitted;
  - `SAY`/`DO`/`WAIT`/`RETURN` typed holds because no user producer exists;
  - `EXIT` local-only, no actor/world event;
  - `ATTEND` local focus only, `UNKNOWN` for unperceived targets;
  - absence is not simulated; unperceived events remain unseen.
- `wp19/cli.py` — runnable entry point: `python3 -m wp19.cli --source cp-a5|join-e ...`.
- `tests/test_wp19_interface.py` — 7 focused tests over real readers.

## 3. Runnable evidence

Commands actually run from `WORKER_RETURNS/SOROK-WP19-ENCOUNTER-PROTOTYPE-R1`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m wp19.cli \
  --source cp-a5 --root .runtime/demo/cp-a5 demo
# exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m wp19.cli \
  --source join-e --root .runtime/demo/join-e-accept \
  --disposition PERFORMED --perform omit demo
# exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m wp19.cli \
  --source join-e --root .runtime/demo/join-e-refused \
  --disposition REFUSED demo
# exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m pytest -q \
  -p no:cacheprovider tests
# 7 passed
```

Evidence files:

- `evidence/cp_a5_demo.json`, `evidence/cp_a5_accessible_view.txt`.
- `evidence/join_e_accept_demo.json`, `evidence/join_e_refused_demo.json`.
- `evidence/acceptance_variants.json`.
- `evidence/test_run.txt`.
- `evidence/source_manifest.json`.

## 4. Exact observed interface outcomes

### CP-A5 real reader

- View: `clock=100`, `location=workshop`, 16 remembered events, `unperceived_event_count=4`.
- `ask("What happened to the workshop tool?")` → `OK`, exact answer: `A perceived B take the workshop tool, could not repair while it was away, and perceived its return.`, `read_only=true`.
- `ask("What did B do at the market?")` → `UNKNOWN`, exact answer: `UNKNOWN: A did not perceive B's market commission.`, `evidence_event_ids=[]`, `read_only=true`.
- Hidden market commission is not in `visible_events`.
- `SAY`, `DO`, `WAIT`, `RETURN` return typed holds; `EXIT` returns `LOCAL_EXIT_ONLY`; absence returns `UNKNOWN`; store is unmutated.

### JOIN-E performed share

- Real `JoinedSession` with `perform=omit`; `HELP_ACCEPT` is observed.
- Two actual R31E `HELP_ACCEPT` variants were observed across sessions:
  - `Put your hand on the near edge. I'll take the slack.` / `A clears a space at the bench.`
  - `Hold the near edge. I'll check the seam.` / `A sets the tool beside your hand.`
- Both are exact real JOIN-E outputs; the interface does not synthesize either one. The S11 A2 example pins the first variant; `evidence/acceptance_variants.json` records both.
- Visible `REPAIR` action and `HELP_ACCEPT` surface; no `SHARE_TOOL`/B private operation in the user view.

### JOIN-E refusal

- Real `RefusalSession`; `HELP_REFUSE` is observed.
- Exact speech: `The tool's gone. I can't do it today.`; gesture: `A looks at the empty tool space.`
- No `REPAIR` action; refusal is visible; hidden motive is not shown.
- `SAY`/`DO`/`WAIT`/`RETURN` holds; `EXIT` local-only; store unmutated.

## 5. Acceptance example mapping

| S11 example | WP-19 behavior |
|---|---|
| A1 SAY refusal | JOIN-E refusal view shows exact refusal speech/gesture/surface. |
| A2 SAY accept | JOIN-E performed view shows a real `HELP_ACCEPT` surface; both observed variants recorded. |
| A3 DO visible | JOIN-E view shows actual `REPAIR`/`INSPECT` events and public deltas. |
| A4 ATTEND known/unknown | CP-A5 known event attend returns its visible summary; unperceived target returns `UNKNOWN` with no content. |
| A5 WAIT | `WAIT_UNSUPPORTED_TYPED_HOLD`; no clock/event change. |
| A6 EXIT/RETURN | `LOCAL_EXIT_ONLY`; `RETURN_UNSUPPORTED_TYPED_HOLD`. |
| A7 REFUSAL/absence | `HELP_REFUSE` visible; absence is `UNKNOWN`, not simulated. |
| A8 hidden state | CP-A5 market commission remains absent from `visible_events`; question returns `UNKNOWN`. |

## 6. Actual available vs missing producers

Available and exercised through real readers: CP-A5 `EncounterReader.view/ask`; JOIN-E C12 `world_events`/`perceptions`, E expression admission, performed/omitted/refused help contrast, material/tool state.

Missing and represented honestly as holds/local state: user `SAY`/`DO` attempt/admission, user `ATTEND` receipt, `WAIT` time advance, portal `EXIT`/`RETURN`/absence receipt, message channel/establishment/delivery, accessibility preference acknowledgement.

No world event, clock advance, actor response, message delivery or native grant was invented.

## 7. Courts

| Court | Grade |
|---|---|
| **ENGINEERING** | `PASS_SCOPED_LOW_FIDELITY_INTERFACE__REAL_READERS__7_TESTS__CLI_EXIT_0__NO_STORE_MUTATION`. |
| **SCIENTIFIC** | `UX_PROTOTYPE_ONLY__TEST_ONLY_SOURCEFREE__NO_HUMAN_TRIAL__NO_PSYCHOLOGY`. |
| **AUTHORITY** | `HOLD` — no native CAN/ADP/C8/C9/C12/Pyat/A5, no production, no human acceptance. |

**DONE:** runnable bounded interface, real CP-A5/JOIN-E readers, accessible observation, local exit, typed return, hidden-state non-disclosure, refusal/absence handling, honest holds for missing producers, exact tests and demo evidence.

**REMAINING:** WP-19 usability/accessibility review with an independent user; missing user action/attend/wait/exit/return/absence/message producers; S14/S15/S5/A5 gates; native authority.

**CRITICAL BLOCKER:** no actual user `SAY`/`DO`/`ATTEND`/`WAIT`/`EXIT`/`RETURN`/message producer exists; the interface truthfully holds these rather than simulating them.

**LARGEST MOVE:** an independent accessibility/usability review of this low-fidelity interface, then competent producer owners fill the typed gaps.

**FLIGHT:** local sourcefree interface only; no provider, human trial, native lane or guide edit.

## 8. PROGRAMMA_DELTA

`PROGRAMMA_DELTA:` WP-19 now has a runnable bounded encounter prototype consuming the pinned S11 WP-19 JSON and real CP-A5/JOIN-E read-side outputs: accessible observation of remembered/perceived events, exact refusal/accept surfaces, hidden-state non-disclosure, local-only exit, typed holds for return/SAY/DO/ATTEND/WAIT/absence/message producers, and no invented actor response, time advance, delivery, native authority or human trial. Seven focused tests and a real CLI demo pass; S35 and untracked artifacts remain untouched.

## 9. Publication

Scoped implementation commit `b5d96a1c55bcd68132f3c3b01e908b0e7b994473` was pushed with an ordinary non-force push to `origin/codex/sorok-wp19-encounter-prototype-r1`. Direct remote readback:

```text
git rev-parse HEAD
b5d96a1c55bcd68132f3c3b01e908b0e7b994473
git ls-remote origin refs/heads/codex/sorok-wp19-encounter-prototype-r1
b5d96a1c55bcd68132f3c3b01e908b0e7b994473  refs/heads/codex/sorok-wp19-encounter-prototype-r1
```

`PUBLICATION_RECEIPT.json` records the exact branch/base/S11/JOIN-E/CP-A5 references and readback. This metadata update is a follow-up scoped commit; the final branch tip SHA is returned in the handback. The S35 branch and untracked `.s35-sources`/`.runtime` artifacts were not modified.
