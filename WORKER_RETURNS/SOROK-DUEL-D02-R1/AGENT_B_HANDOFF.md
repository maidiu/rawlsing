# SOROK D02 Agent B — event-time access, event/current separation, exact source closure

**Task:** `D02` — actor-local situated-field projection of actual world, state and accessible relations.
**Status:** `IN_PROGRESS_PREREQUISITE_HELD`. The current-clock selector is repaired and the exact B02 ingress contract is fixed, but full D02 remains blocked on B02 qualification and the separate C01/B03 candidates. No dated period, completion, native actor, rights or protected acceptance is claimed.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Composition start:** `b169b1aafb5df53bef2a3e02b1ab780930dfcd32` (A D02 `76547199c20f29f63c0e0e43b13a12cdecb3d47a` + C01 B `0fd303e2af23d71b51b068393cfaa6f62d40fe38` + B03 A `5bc29474e769b928d9264f1607bab605e2b1c7e9`).
**Original rival head:** `0d591ff6eab1477bc7e5058e1dd7740813125d19` (A D01/D02 relay).
**Branch:** `codex/sorok-duel-d02-b-counter-20261112-r1`.
**B code cut:** `dba782ddf15dd9d8db261c08b515944dcea4b8e4`.
**Final artifact:** the branch HEAD containing this handoff and the B impact records. No remote or protected push was made.
**Ceiling:** `SOURCEFREE_S2_ONLY`; science, source rights, actor/human authority and protected merge remain held.

## 0. Independent reconstruction before reading A

D02 requires a thin, read-only P3 context adapter over actual P2/Pyat/actor owners. Its terminal consumer is a later actual P3 proposal/actor decision, on the ordinary provider API. The positive oracle is: a changed selected material fact or eligible actor observation changes the real sourcefree decision input and admissible options. The negative oracle is: a stale source/clock, unobserved parental private state or portal gaze enters Nadia's readset. Restoration is the identical eligible readset and stable hash at the same state. Dependencies are D01, B02 and C01; grade `SOURCEFREE_S2_ONLY`; PW links 01/07.

The selector must not create a new world/actor/psyche owner or scheduler. Objective material availability, the focal actor's actual qualified perception, event-time shared relations, and current objective co-presence are distinct facts. A material label is not an actor performed action, learning or private reason. A provider stub's fixed proposal is not native actor evidence. B02 calendar/as-of is unbuilt, so no period/date may be invented and full D02 cannot be claimed. C01 and B03 are candidate inputs at the composition, not accepted dependencies. The registered parent is distinct from the user/fixed historical B1 counterpart; a controlled B1 mediator must not be relabelled maternal learning.

## 1. Exact artifact and provenance

| Path | SHA-256 |
|---|---|
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/situated_context.py` | `1242d0ce39cc356e0591a5ff4eb73fba3e58000a9488b40dffa32759a2726ccf` |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_b_repairs.py` | `89d1e6277ab07c67639ba9b9de178aa20cee4453f4b2cca7494a964095171987` |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/D02_B02_INGRESS_CONTRACT.md` | `ddc1497c3e544ba4da7476233209834a580946a057aa400a4133363a0fb0ac4c` |
| C01 B `supporting_actor.py` (input) | `35e43d8c924d6ea30b4376ef8bed4a8af5b68dd81d636e1cf9033da4320b9c5a` |
| B03 A `house.py` (input) | `6c892ea7525bc608ccd332dce9ee5ea7dc25397092f9c2db9ef44bd4e17d3436` |
| D01 relay `p3_owner.py` (inherited) | `81be18dae3c4c5d9d79f68ee7146be13055a24c4b63bb54019b8ce9d3931b44b` |
| D01 relay `state_store.py` (inherited) | `fc878ce928d9aca305166bfd1b24f4f5c31923b9479f6d47ac4a0bd54402589a` |
| S45 projection reader (input) | `6e7771000b0d50abcdc990192a2d834171640371e6e814694a918eb9286386fd` |
| A D02 code cut (rival) | `76547199c20f29f63c0e0e43b13a12cdecb3d47a` |
| A D01 relay code cut (rival) | `a3ead75aad5a40a0c96224f8f747e9c48b6f085f` |

Execution commands (worktree root, no bytecode):

```sh
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_composition_prereq.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
```

Receipts: D02 selector + composition + B repairs **16 passed in 376.06 s** (`evidence/d02_b_all_pytest.log`); composition alone **1 passed in 17.87 s** (`evidence/d02_b_composition_pytest.log`); D01 all **15 passed in 84.85 s** (`evidence/d01_b_regression_pytest.log`); P3 owner/store/rules/projections/goal-residual **77 passed, 1 skipped in 48.24 s** (`evidence/p3_b_regression_pytest.log`).

Only `p3/situated_context.py`, the new B tests, the B02 contract document and D02 evidence were added/changed. `p2_owner.py`, `supporting_actor.py`, `house.py`, P6 `situated.py`, C01/B03/other pair files, guides, workflows, Pyat, global config, protected and remote refs were not edited. A's D02 handoff, tests and evidence remain in place; the B records are separate `PROGRAMMA_DELTA_B.json` / `impact_B.json`.

## 2. A's valid work, explicitly conceded

- **D01 relay deletion repair is correct.** A found that B's record-to-receipt binding was one-way. A's `verify()` now compares the full canonical record list for each operation against the rows committed by that operation, catching a chain-consistent deletion, extra row or replacement. I reproduced the deletion defect and preserve A's repair. D01's earlier retention work is adequate; I did not reopen it.
- **D01 actual-owner closure is correct.** `P3Owner.__init__` calls `store.verify()` before the config anchor and closes on failure. This is the correct correctness call for the actual owner, not only the D01 loader. It is preserved; D01 suite passes.
- **D02 material/access split is sound.** Objective `read_household` availability is kept separate from focal position affordance; household/tool options require the actor to be in a household room. Objective availability is not treated as conscious knowledge.
- **Parent-private and portal-gaze exclusion is sound.** Relations use the C01 public registration/access rows; private state, private-state hash and `perceived_by_user` do not enter the readset. The negative test is genuine.
- **The fresh-root composition is the right proof shape.** A's composition test uses one actual root for B01 household, C01 participation/access, D01 retention and D02 selector. I reran it at the current composition with C01 B/B03 A; it passes. This is not three separate green suites.
- **The provider boundary is honestly stated.** The selector is passed as the existing `RecursionCycle` provider `context`; the provider request is the actual decision input. A scripted provider does not prove native cognition or a fabricated choice. I preserve that boundary.
- **The D02 prerequisite hold is correct.** B02 is unbuilt and C01/B03 are candidates; A did not claim D02 completion. I also do not claim it.
- **A's D02-1/D02-2 self-findings are real partial repairs:** objective material was separated from position access; current position was used to remove the address option. They are preserved and strengthened below.

## 3. Defects established with exact evidence

### D02-B1 — The latest-perceived scan selects by current read clock and lexical action ID, not event time

A's `_latest_perceived` builds `(access["world_clock"], event_ref, access)` candidates. `read_actor_access` returns the **current** `session.world().clock` for every candidate, so all candidates tie on the first key; the final sort chooses the lexicographically largest action event ID. An earlier actual event whose hash is lexically larger replaces a later actual occurrence.

- `evidence/D02_A_CURRENT_SELECTION_CONFLICT.txt` captures A's D02 code cut on ten actual committed events/receipts. Every access row reports `world_clock` 252; the latest event is clock 252, but A's selector returns the event at clock **246** because its action ID is lexically larger.
- A's own D02-3 acknowledged the scan but described it as bounded; it did not identify the constant-read-clock/lexical-ID failure.
- `evidence/D02_B_FIXED_SELECTION.txt` shows B selecting the actual latest event (clock 252) while the lexically largest action ID belongs to an event at clock 234.
- `test_actual_events_select_latest_event_time_not_lexical_action_id` uses ten actual events; `test_temporal_helper_uses_event_clock_when_world_clock_is_constant` isolates the constant-world-clock failure. `_event_temporal` also refuses a projected event clock that disagrees with the row's event time (`D02_EVENT_CLOCK_MISMATCH`).

### D02-B2 — The access hash conflated read time with event access identity

A hashed the whole `read_actor_access` document, including its current `world_clock`, into `observation.access_hash` and each relation `access_hash`. The same historical event therefore changed its "access identity" whenever the world clock advanced, even though the event, receipt and viewer did not.

B normalizes the access identity by excluding `world_clock`; the event, receipt, viewer, status, root/branch and event content remain in the hash. `read_world_clock` is still exposed separately in the observation, and the selector's identity clock is current. `test_event_access_hash_is_stable_when_world_clock_advances` shows the access/relation hashes stable while the overall selector hash changes for the later state.

### D02-B3 — Current co-presence and remembered event relation were not explicitly separated

A's relation row used one `co_present` boolean computed from current world positions. That is a current objective position, not the event-time shared perception that made the relation eligible, and it did not distinguish "Nadia perceived this other in the selected event" from "the other is currently in the same room."

B now exposes:

- `event_co_present` from the selected event's actual access receipt channel;
- `current_co_present`/`co_present` from current objective positions;
- `event_access_scope` and `current_scope`;
- `ADDRESS_ELIGIBLE_OTHER` requires both the event-time shared perception and current objective co-presence.

`test_remembered_event_relation_is_not_current_co_presence` preserves the relation and event access hash when the parent moves away, removes only the current address option, and confirms the observation is still the selected event. `test_current_co_presence_without_event_perception_is_not_eligible` puts the parent in the focal position without any selected-event perception and confirms no relation/option.

### D02-B4 — The exact D02 source closure was absent

A's `p3_owner._code_pins()` therefore did not change when `situated_context.py`, `supporting_actor.py`, `house.py` or the actual S45 event projector changed. A acknowledged the pin gap in its challenge but did not close it.

B adds a D02-specific 12-file closure: the selector, `p3/__init__.py`, the C01 supporting-actor reader, the B03/P6 household reader, the S45 projection reader, and the existing P3 owner/projection/rule/compression/store/engine-contract pins. It is included in the selector body, readset and hash. It is **not** added to the global `P3Owner` config pin, so unrelated P3 modes are not coupled to the D02 readers.

- Module identity is exact: a foreign `house`/`supporting_actor`/projection module refuses `D02_HOUSE_SOURCE_IDENTITY`/`D02_SUPPORTING_SOURCE_IDENTITY`/`D02_PROJECTION_SOURCE_IDENTITY`.
- A missing selected file refuses `D02_SOURCE_MISSING`.
- An expected closure from the same state but a changed selected file refuses `D02_SOURCE_CLOSURE_CHANGED`; exact restoration returns the baseline closure and selector hash (`test_changed_selected_source_refuses_then_restores`).
- The closure test shows the exact labels/hashes and excludes P6 `situated.py`/the rest of the repository (`test_source_closure_is_exact_selected_reader_set`).
- The changed-source test uses a temp copy of the selector with a changed hash to exercise the closure boundary; it does not edit the repository file. This is a source-pin simulation, stated as such.

### D02-B5 — A pending P3 operation was not refused

The selector read the owner snapshot and world while a P3 operation could be PREPARED/WORLD_COMMITTED/PSYCH_COMMITTED. A pending operation makes the exact later-consumer context unsafe; D01's boundary already refuses pending. B refuses `D02_PENDING_OPERATION` before material/access reads (`test_pending_p3_operation_refuses_a_new_context`). The caller must reconcile the exact pending operation first.

### D02-B6 — Read-boundary labels were imprecise

A's read boundary claimed `psyche_store: NOT_READ`, but `P3Owner.snapshot()` reads the durable psyche head to form the P3 state hash. B records `P3_HEAD_ONLY_NOT_RECORDS` and separates material as `OBJECTIVE_FOCAL_POSITION_NOT_PERCEPTION` with `knowledge_claim: NOT_CLAIMED`. This is not a new read; it removes a false `NOT_READ` claim. Parent private state and portal user view remain `NOT_READ`.

### D02-B7 — B02 ingress was a hold, not a finite contract

A's date hold was correct but did not state the exact accepted ingress/refusal shape. B adds `D02_B02_INGRESS_CONTRACT.md` and the selector's `b02_ingress` field, still `PREREQUISITE_HELD_NOT_QUALIFIED`. It specifies the exact owner, S46/P2 units, period bounds/split, source/world/material/actor-as-of hashes, refusal conditions and required cold/later-reader evidence. No period, date, mock calendar or workshop-tick-to-year mapping is invented.

## 4. Corrections implemented

- `p3/situated_context.py`
  - event-time/ordinal selection (`EVENT_TIME_THEN_ORDINAL_NOT_READ_TIME`), explicit event clock binding, `selected_event_clock`/`selected_event_ordinal`, separate `read_world_clock`, no skip of access-integrity failures;
  - normalized event access identity (`world_clock` excluded) for observation and relation hashes;
  - `event_co_present` vs `current_co_present`/`co_present`, event/current scopes, option requiring both;
  - objective material `access_basis` and `knowledge_claim: NOT_CLAIMED`;
  - exact 12-file D02 source closure in body/readset/hash, expected closure refusal/rebuild/restore, module identity checks;
  - session/root/branch/clock alignment, pending-operation refusal, state-hash format check;
  - `b02_ingress` contract reference and explicit held status.
- New `D02_B02_INGRESS_CONTRACT.md`.
- New `tests/test_d02_b_repairs.py` covering ten actual-event temporal selection, constant-clock helper selection, stable access hash, remembered/current separation, unobserved current co-presence, source closure, changed-source refusal/restore, foreign module, pending refusal and B02 hold.
- A's tests and composition test pass unchanged. A's D01 relay deletion/actual-owner repair is preserved. No P2/house/supporting/P6/other pair edits.

## 5. Proof of improvement and preservation

- **Full D02 suite:** 16 passed in 376.06 s (`evidence/d02_b_all_pytest.log`). This includes A's five selector tests, A's composition test, and B's ten repair tests.
- **Composition at `b169b1aa`:** one fresh actual root exercises B03 household, C01 B access/registration, D01 retention/cold reopen and the D02 selector; 1 passed in 17.87 s (`evidence/d02_b_composition_pytest.log`).
- **D01 regression:** 15 passed in 84.85 s (`evidence/d01_b_regression_pytest.log`), including A's deletion/actual-owner repairs and B's earlier D01 tests.
- **P3 regression:** 77 passed, 1 skipped in 48.24 s (`evidence/p3_b_regression_pytest.log`), including the actual-owner full verify path inherited from A.
- **Temporal defect:** A-current log selects clock 246 while latest is 252; B fixed log selects 252 while the lexical maximum is 234. Actual committed events/receipts, not expected-output prose.
- **Preservation:** A's material/access split, parent-private/portal exclusion, composition test, provider-context boundary, and D02 prerequisite hold are retained. No native/CAN/ADP/Pyat/human/rights/protected claim is made.
- **Measured cost:** 376.06 s D02, 17.87 s composition, 84.85 s D01, 48.24 s P3. The selector reads the 12 closure files and takes an extra base snapshot per build. Tokens/USD are `UNKNOWN`.

## 6. Challenges refuted, conceded, or bounded

- **Conceded:** A's D01 deletion/record-list repair and actual-owner `store.verify()` closure are correct. No further retention round is justified by this packet.
- **Conceded:** A's D02 objective-material/position split, private/portal exclusion, provider-input boundary and B02 hold are correct.
- **Refuted as sufficient:** A's D02-3 scan. It does not select the latest real occurrence; it selects a lexical action ID tied by the current read clock. Fixed with actual evidence.
- **Partially refuted:** A's D02-2 current-co-presence repair handles the address option but does not distinguish event-time relation from current position. B adds the distinction and preserves both.
- **Refuted:** A's read-boundary `psyche_store: NOT_READ` wording. The snapshot reads the P3 head; the truthful label is `P3_HEAD_ONLY_NOT_RECORDS`.
- **Bounded:** A's "provider test is not native actor evidence" is accepted. B proves input dependence at the actual provider request, not actor cognition or a chosen action.
- **Bounded:** A's source-pin challenge is accepted; B closes the new-reader gap at the D02 boundary but does not pin the entire P2/S47 transitive estate or global P3 modes.
- **Own attack:** A same-state closure comparison cannot prove a changed source executes differently; B's changed-source test is a closure simulation over a temp copy. The actual protection is exact file identity/refusal, not a behavioral replay of the changed file.

## 7. New attack surfaces and risks

- The D02 source closure is file-granular and 12 files. A change to any selected file changes the context hash; a consumer holding an old expected closure refuses. This is intentional, but it also means unrelated edits inside `house.py`/`supporting_actor.py` invalidate the D02 context. A symbol-level closure would be narrower but is not exact source authority; no such claim is made.
- The closure does not pin the entire S47/P2 session/product estate or `model_cycle.py` (the provider context seam). The existing P2/P3 identity and the provider-request test remain the boundary. Do not treat the closure as a whole-repository or Byzantine root.
- `observation.access_hash` and relation `access_hash` are normalized and no longer include `world_clock`. Any downstream consumer comparing old hashes must update; use `read_world_clock`/identity separately.
- `co_present` remains the current objective position for ABI compatibility; use `event_co_present` for the selected-event relation and `current_co_present` for current position. `ADDRESS_ELIGIBLE_OTHER` requires both.
- The selector now refuses any pending P3 operation. A caller with a pending operation must recover it before building a context.
- `_check_session_alignment` takes an extra base snapshot; the source closure reads 12 files. Both are bounded but not separately microbenchmarked.
- B02 is only a static ingress contract; no actual period is accepted. Any future B02 implementation must reconcile the exact contract and prove the required cold/later-reader evidence.
- C01 B and B03 A remain candidate composition inputs, not accepted dependencies. Their exact files are pinned in this D02 closure; later changes require a new context/expected closure.

## 8. Surviving disagreements and blockers

- **Event occurrence vs delayed perception.** I selected the latest actual event time/ordinal. If an actor can learn of an older event at a later perception receipt, a two-clock selection may be required. That is not demonstrated in the current P2 co-present fixtures; it is a real future question.
- **Current co-presence as addressability.** I require selected-event shared perception plus current objective co-presence for `ADDRESS_ELIGIBLE_OTHER`. A case where an observed but not currently co-present relation should still be addressable (e.g., remote communication) is not supported; that would need a relation/channel contract, not a position conflation.
- **Source closure granularity.** File-level exact hashes are conservative and may over-invalidate; a symbol/ABI closure could be narrower but would need exact source identity for selected symbols. The S47/P2 transitive estate is not pinned here.
- **Provider seam.** `model_cycle.py` is the existing context transport and was not modified or included in the closure. Whether the D02 contract should pin it is a downstream D03/E integration decision.
- **B02.** No built calendar/as-of/period owner exists. Full D02 remains `PREREQUISITE_HELD`; the ingress contract is not acceptance, mock data or a date.
- **C01/B03.** C01 B and B03 A are returned candidates still running separately; this composition uses them as inputs, not accepted dependencies.
- **D03–D05.** The selector's admissible options are input labels, not choices, performed acts, acquired state or native CAN/ADP. D03/D04 must add their own response/consumer contracts and must not fabricate provider choices.
- Native CAN/ADP/Pyat, source rights, actor/human, C12 and protected merge remain held.

## 9. Challenge to the same A

1. **Break event-time selection with an actual delayed-perception case.** Construct committed events/receipts where the latest perception receipt belongs to an older event; decide whether D02 must select by occurrence or receipt clock. If both are needed, propose the exact two-clock contract and implement it.
2. **Break access normalization.** Find a current-world field that legitimately belongs in event access identity, or show the normalized hash accepts a changed access. If so, separate event identity from read-time state without reintroducing the conflation.
3. **Break the source closure.** Find a decisive reader missing from the 12 files (e.g., a transitive S47/P2/projection symbol) or a selected file that is over-coupled, and propose a minimal exact closure with a changed-source refusal/restore test. Do not add every repository file.
4. **Break current/event co-presence semantics.** Construct a real case where an observed relation should remain addressable without current co-presence, or where current co-presence without selected-event perception should be eligible. If so, implement the exact channel/relation contract.
5. **Break the pending policy.** Find a legitimate current-clock D02 build during a verifiable pending P3 operation; if one exists, show the exact recovery path and why the selector should allow it.
6. **Implement B02 against the ingress contract.** Use the existing P3/S46/P2 owners; prove the period split, material/actor as-of, cold replay and later actual P3 consumer. Do not invent a calendar or promote workshop ticks to years.
7. **Wire D02 into D03/D04.** Consume the selector through the existing provider input and show a real sourcefree response/proposal effect; do not treat `admissible_options` as native choices or a provider stub as actor cognition.
8. **Only reopen D01 if a product-blocking defect remains.** The deletion/actual-owner repair is adequate; do not restart retention dueling for its own sake.

## 10. Limits and proof boundaries

- `SOURCEFREE_S2_ONLY`; no native CAN/ADP/Pyat, source rights, actor/human, C12, production or protected merge.
- D02 is **not complete**: B02 calendar/as-of is unbuilt; C01 and B03 are candidates; no dated historical recursion, period split or full D02 acceptance.
- The selector's options are input labels, not choices or performed actions. The provider is transport; no native actor evidence.
- The source closure is exact file-level for the selected readers plus P3 owner pins, not the entire S47/P2 estate or a Byzantine authenticated root.
- The changed-source test is a closure simulation over a temp copy, not a repository source edit or a behavioral replay of changed code.
- The provider context is transitive input evidence; no model calls/tokens were made or measured. Token/USD is `UNKNOWN`; wall times are recorded.
- Old-code P3/world roots and pre-composition fixtures refuse under the current exact pins; no migration is claimed.
