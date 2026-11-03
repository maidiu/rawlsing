# SOROK S11@SPECIFY — encounter / exit / return interface specification for WP-19

**RESULT:** `S11_SPECIFY_COMPLETE__SOURCE_QUALIFIED_WP19_INTERFACE__SAY_DO_ATTEND_WAIT__ACCESSIBLE_EXIT_RETURN__ABSENCE_REFUSAL__HIDDEN_STATE_NONDISCLOSURE__ACTUAL_VS_MISSING_PRODUCERS__NO_RUNTIME__NO_HUMAN_TRIAL`.

This return supplies the smallest source-qualified S11 interface specification directly consumable by WP-19. It is design only. It does not run a runtime, human trial, provider call, new psychology, native grant or guide edit.

## 1. Exact sources read

- Guide commit `30de6d21963c64e832bc9220b870c8b26a6624ac`:
  - `06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md` blob `2e71d61965c82c2e94454472dfdde576d8936cef`, S11 row and S8/S9/S11 boundary.
  - `10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md` blob `a67c3d2e468adda8e0af90e0cb5871af3e97b9a7`, WP-19 dependency and S11/S14/S15 conjunction.
  - `14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl` blob `123cb09ed63212d5738c61f4e1336841f0a35f9c`, WP-W6B-37.
- Original Sorok sources at base `ce2478aa38eec7fb021aa95c01464a468a46fbc9`:
  - 31 `31_ENTRY_PRIMER_AND_BEGINNING_TO_KNOW_LOOP_R1.md` blob `c5f5290ff29e8810510b968a1dc1e632834876ce`.
  - 32 `32_DUAL_INTERFACE_SCENE_EXIT_MESSAGING_AND_SUCCESSION_R1.md` blob `af6dfa93fac46216f047dfc1ee87fc72ffcd8bfa`.
  - 35 `35_CONCRETE_FIRST_SESSION_SPINE_R1.md` blob `599cd66eb001947b63d48e1e9b52e5a4d449862c`.
  - 100 `100_MINIMAL_WHITE_WHALE_ALPHA_AND_FIDELITY_ESCALATION_CONSTITUTION_R1.md` blob `bd08a138ebf82522d7c90bb7e702d79697b3c240`.
  - 101 `101_BINDING_SURFACE_ACTOR_PHENOMENOLOGY_SEGREGATION_AND_TWO_CALL_RENDERING_R1.md` blob `51f0fd1fa95da641d40ec5fb94e879fcbf0ae7a1`.
- JOIN-E `5e63672543973ce2533129e1ca3224d82af0dffc`:
  - `evidence/positive_receipt.json` blob `72a2b53c3d4082fafdeb2c6a5ea18c8b08984920`.
  - `evidence/targetless_refusal.json` blob `54bd91c655df6f31def194f678a5ac32c026ab46`.
  - `evidence/b_event_contrast.json` blob `b2d819aff09f9c20ac1d9ada88a72eb9fb53ba3a`.
- CP-A5 `913765328e4fab12b150ea01421ed6b445158184`:
  - `candidate/cp_a5/encounter.py` blob `8d388c2f10eec6b6d6ab0f3e5f1566b0053098e6`.
  - `01_ACTUAL_A3_A5_LIFE_AND_ENCOUNTER_TRACE.json` blob `b52b0c9a9ff6b49acf5b3f648f33cd49ad7cebdb`.

Full blob/SHA-256 manifest: `evidence/source_manifest.json`.

## 2. Delivered artifacts

- `01_S11_WP19_INTERFACE_SPEC.md` — human-readable source-qualified interface specification.
- `02_WP19_CONSUMABLE_INTERFACE.json` — machine-readable controls, surfaces, visible/hidden fields, acceptance examples and producer gaps.
- `03_ACCEPTANCE_EXAMPLES.json` — exact A1–A8 examples keyed to existing encounter outputs.
- `evidence/source_manifest.json` — exact guide/original/JOIN-E/CP-A5 source hashes.
- `PROGRAMMA_DELTA.md` — one S11 delta.

## 3. The specification in brief

### Visible controls

- Portal: `SAY`, `DO`, `ATTEND`, `WAIT`, `EXIT`.
- Outside/hub: `OPEN_THREAD` (only actual channel), `SEND_MESSAGE` (only actual channel), `RETURN` (only actual meeting/opportunity), `WAIT/LEAVE`, `EXIT`.

### Visible facts

Only persisted, user-lawful observable events and exact heard speech/gesture. Event fields: `event_id`, `kind`, `clock`, `location`, `actor_visible_id`, `summary`, `body_public`, `source_ref`, `perceived_by_user`.

### Hidden state

Never displayed: traits, affinity, trust, suspicion, motive, private emotion, private actor model, unperceived event content, relationship score, rarity, completion, unlock level, future outcomes.

### Accessibility

Keyboard-only controls, visible focus order, screen-reader labels, text alternatives for gestures/visual cues, no color-only meaning, always-visible `EXIT`, explicit `RETURN` route or typed hold, announced `UNKNOWN`/clarification/mode changes, no real-time typing pressure, persisted event order, reduced-motion equivalents.

### Exit / return

`EXIT` is always visible and does not fabricate actor/world events. `RETURN` requires an actual meeting/opportunity/channel; no teleport. No actual user-facing exit/return/absence producer exists at this cut, so WP-19 must use `LOCAL_EXIT_ONLY` and `RETURN_UNSUPPORTED_TYPED_HOLD` without world writes.

### Absence / refusal

User absence does not pause actor life, but the interface must not claim events happened while absent unless actual persisted events exist. Unperceived content stays `UNKNOWN` (CP-A5 model). Refusal uses the actual public surface; no hidden motive inference.

## 4. Actual available data and missing producers

**Actual available:** C12 `world_events`/`perceptions`, exact E expression admission (`speech`, `gesture`, `strategy`, `surface`, `accepted`), CP-A5 read-only `view()`/`ask()` with `known_event_ids`/`remembered_events`/`unperceived_event_count`/`UNKNOWN`, JOIN-E performed/omitted/refused help contrast, material/tool state.

**Missing producers:** `USER_SAY_DO_ATTEMPT_ADMISSION`, `USER_ATTEND_RECEIPT`, `WAIT_TIME_ADVANCE_RECEIPT`, `PORTAL_EXIT_RETURN_RECEIPT`, `USER_ABSENCE_LIFE_ADVANCE`, `MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY`, `ACCESSIBILITY_PREFERENCE_ACK`.

WP-19 may use local UI state for these gaps only if labelled local/typed hold and no world state is written.

## 5. Exact acceptance examples

| ID | Existing output used | Acceptance |
|---|---|---|
| A1 | JOIN-E `targetless_refusal.json` | exact `HELP_REFUSE`, speech `The tool's gone. I can't do it today.`, gesture `A looks at the empty tool space.`, tools 0 |
| A2 | S35 `actual_a_evidence.json` performed-omit | exact `HELP_ACCEPT`, speech `Put your hand on the near edge. I'll take the slack.`, gesture `A clears a space at the bench.`, tools 1 |
| A3 | JOIN-E C12 world events | visible `INSPECT {"changed": false}` and `REPAIR` cash/completed/hours/material deltas, clock 10 |
| A4 | CP-A5 trace | tool question `OK` with exact answer; market question `UNKNOWN` with `evidence_event_ids=[]`, `read_only=true`, unperceived count 4 |
| A5 | missing wait producer | `WAIT_UNSUPPORTED_TYPED_HOLD`; no clock/event change |
| A6 | missing exit/return producer | `LOCAL_EXIT_ONLY`; `RETURN_UNSUPPORTED_TYPED_HOLD`; no teleport/fabricated event |
| A7 | JOIN-E `b_event_contrast.json` | performed accept, omitted/refused `HELP_REFUSE`; no forced private-cause contrast |
| A8 | CP-A5 market UNKNOWN | show `UNKNOWN` only; no market summary/id/hidden cause |

Exact machine copy: `03_ACCEPTANCE_EXAMPLES.json`.

## 6. Courts

| Court | Grade |
|---|---|
| **ENGINEERING** | `SPECIFY_COMPLETE_SOURCE_QUALIFIED_WP19_CONSUMABLE` — design artifact only; no runtime. |
| **SCIENTIFIC** | `NO_NEW_PSYCHOLOGY__NO_HUMAN_TRIAL__UX_SPEC_ONLY` — existing TEST_ONLY encounter outputs used as interface evidence. |
| **AUTHORITY** | `HOLD` — no native CAN/ADP/C8/C9/C12/Pyat/A5 grant; no human participant; no guide adoption. |

**DONE:** source-qualified S11 interface, visible SAY/DO/ATTEND/wait, accessible exit/return, absence/refusal, hidden-state non-disclosure, actual-vs-missing producer separation, exact A1–A8 acceptance examples, WP-19 consumable JSON.

**REMAINING:** WP-19 low-fi implementation; competent user-action, ATTEND, wait, exit/return, absence, message-channel and accessibility producers; independent usability test; S14/S15/S5/A5 gates.

**CRITICAL BLOCKER:** no actual user SAY/DO/ATTEND/wait/exit/return producer exists at this cut; the interface can specify and hold these as typed gaps but cannot honestly claim them as implemented.

**LARGEST MOVE:** WP-19 builds the low-fidelity interface from this spec, then a separately authorized accessibility/usability review tests it.

**FLIGHT:** specification only; no runtime, provider, human trial, guide edit or native lane.

**DELTA:** S11 moves from an unvalidated UX name to a concrete, source-qualified WP-19-consumable interface with exact existing-output acceptance examples and typed producer gaps.

## 7. PROGRAMMA_DELTA

`PROGRAMMA_DELTA:` S11@SPECIFY now has a concrete source-qualified WP-19-consumable interface specification: visible SAY/DO/ATTEND/wait, always-accessible EXIT and lawful RETURN with typed holds where producers are absent, absence/refusal semantics, strict hidden-state non-disclosure, exact A1–A8 acceptance examples from JOIN-E/CP-A5 outputs, and an explicit split between actual available encounter data and seven missing user/accessibility/message/absence producers. No runtime, human trial, new psychology, native grant or guide edit; WP-19 remains the next implementation owner.

## 8. Publication

Exact scoped commit and ordinary-push readback are recorded in `PUBLICATION_RECEIPT.json` after publication and returned in the final handback.
