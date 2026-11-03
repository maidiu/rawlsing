# S11@SPECIFY — smallest source-qualified encounter / exit / return interface

Status: `S11_SPECIFY_SOURCE_QUALIFIED_INTERFACE__WP19_CONSUMABLE__NO_RUNTIME__NO_HUMAN_TRIAL`
Base: `ce2478aa38eec7fb021aa95c01464a468a46fbc9`
Guide: `30de6d21963c64e832bc9220b870c8b26a6624ac`
JOIN-E: `5e63672543973ce2533129e1ca3224d82af0dffc`
CP-A5: `913765328e4fab12b150ea01421ed6b445158184`

This is a design specification only. It does not implement a runtime, run a human trial, add psychology, edit the guide, or promote native authority.

## 1. Source-qualified product requirements

| Requirement | Source |
|---|---|
| The portal surface exposes `SAY / DO / ATTEND`; the persona may leave, become busy, redirect attention or end the encounter. | Sorok 32 `af6dfa93…` §1 |
| First co-presence ends because the scene develops a terminating cause, not a tutorial/beat. | Sorok 32 `af6dfa93…` §3; Sorok 35 `599cd66e…` §11 |
| The transition to an outside/message surface is a threshold; a contact channel is not guaranteed. | Sorok 32 `af6dfa93…` §§4–5; Sorok 35 `599cd66e…` §§12–14 |
| Message time is asynchronous to portal scene time; wall clock is not portal clock. | Sorok 32 `af6dfa93…` §6 |
| Do not expose rarity, affinity, completion percentage or unlock level. | Sorok 32 `af6dfa93…` §7 |
| Entry primes curiosity and beginning-to-know, not moral compliance; early failure is human-scale and recoverable. | Sorok 31 `c5f5290f…` §§2, 4, 8 |
| `SAY/DO/ATTEND`, clarification on uncertain ownership, attempt != outcome, natural scene endings. | Sorok 100 `bd08a138…` §C, §E, Gate 1 |
| User absence does not pause the actor; return conditions can change independently. | Sorok 100 `bd08a138…` §E, Gate 3 |
| Hidden causal state shapes outward expression but is not handed to the user-facing surface; exact dialogue is preserved where lawfully heard. | Sorok 101 `51f0fd1f…` §§6, 8, 12, 13 |
| Concrete humane entry, `SAY/DO/ATTEND`, absence/exit, uncertainty and accessible controls are the WP-37 deliverable. | Guide 14 `123cb09e…` WP-W6B-37 |
| WP-19 runnable low-fi interface is unlocked only after this S11 specification. | Guide 10 `a67c3d2e…` A5 row |
| CP-A5 read-only encounter exposes only A's perceived events and returns `UNKNOWN` for unperceived content. | CP-A5 `8d388c2f…` `EncounterReader.view/ask` |

## 2. Surfaces and states

### 2.1 Portal encounter

Visible surface:

```text
mode = PORTAL
clock = <persisted scene clock>
location = <A/user lawful location>
visible_events[] = only events in the user's lawful perception
visible_speech[] = exact SAY utterances lawfully heard
visible_actions[] = DO attempts/results lawfully observed
attend_target = <perceived event/object id or UNKNOWN>
exit_control = always visible and keyboard reachable
accessibility_announcement = <same information in text>
uncertainty[] = explicit UNKNOWN / clarification
```

Controls: `SAY(text)`, `DO(intent)`, `ATTEND(target)`, `WAIT`, `EXIT`.

### 2.2 Outside-portal / hub

Visible surface:

```text
mode = OUTSIDE
contacts[] = only contacts with an actual lawful channel
thread = <messages actually exchanged>
last_encounter = <actual persisted timestamp if available>
return_control = only where an actual meeting/opportunity exists
exit_control = always visible
```

Controls: `OPEN_THREAD` (if channel exists), `SEND_MESSAGE` (if channel exists), `RETURN` (only through actual meeting/opportunity), `WAIT/LEAVE`, `EXIT`.

If no channel was established, no contact/thread is shown. Do not fake a messaging thread.

## 3. Visible event contract

Every displayed event must be derived from an actual persisted event and its user-lawful perception:

```json
{
  "event_id": "TEST_ONLY_BP4_WORLD_EVT_…",
  "kind": "ARRIVAL|INSPECT|REPAIR|SPEECH|REFUSAL|…",
  "clock": 10,
  "location": "workshop|market|…",
  "actor_visible_id": "A|B|C|U|…",
  "summary": "observable summary",
  "body_public": {"only observable fields": "…"},
  "source_ref": "C12 world_event / E expression admission",
  "perceived_by_user": true
}
```

If an event is not in the user's perception rows, it is not displayed, not summarized and not hinted at. It remains `UNKNOWN`.

## 4. Control semantics

### SAY

- User input is an **attempt**, not a performed act.
- Exact actor speech that is lawfully heard is preserved verbatim.
- Do not paraphrase exact dialogue (Sorok 101 §13).
- If ownership/parse is uncertain, return explicit clarification before any world event.
- Hidden actor state must not appear in the spoken or narrated surface.

### DO

- Attempt and outcome are separate: `attempted`, `admitted`, `performed`, `refused`, `blocked`, `reason`.
- Only the observable world result is shown; no hidden motive, private model or unperceived event detail.
- A denied/blocked action shows the actual refusal/block, not a simulated success.

### ATTEND

- Target must be a perceived event/object or an explicit `UNKNOWN`.
- Attending an unperceived event shows `UNKNOWN` and no details.
- ATTEND changes the user's focus only; it does not create actor knowledge, motive or a world event.
- No actual user-facing `ATTEND` producer exists in JOIN-E/CP-A5; WP-19 may implement local focus UI only, labelled `LOCAL_ATTEND_ONLY`, until a receipt producer exists.

### WAIT

- `WAIT` must not fabricate time passage or events.
- No actual wait/time-advance receipt producer exists in the inspected JOIN-E/CP-A5 outputs.
- WP-19 must show `WAIT_UNSUPPORTED_TYPED_HOLD`, leave the persisted clock unchanged and create no world event.
- When a producer exists, WAIT must carry a receipt with `attempted`, `performed/omitted`, `clock_before`, `clock_after`, `events[]`, `reason`.

### EXIT

- `EXIT` is always visible, keyboard/screen-reader reachable and never hidden behind a menu.
- Exiting ends portal co-presence UI only. It must not fabricate an actor action, a world event or a relationship change.
- No actual user-facing exit/return receipt producer exists in the inspected outputs; WP-19 shows `LOCAL_EXIT_ONLY` and may close the portal view.
- Escape/back must not silently discard an in-progress input; confirm or preserve it.

### RETURN

- Return is lawful only through an actual meeting/opportunity/channel.
- Do not provide `Visit Nadia`, `Teleport to Nadia` or arbitrary re-entry.
- No actual user-facing return/absence producer exists in the inspected outputs; WP-19 shows `RETURN_UNSUPPORTED_TYPED_HOLD` unless a lawful channel/opportunity is supplied.
- On any lawful return, re-read persisted state; display new events only if they actually exist.

### ABSENCE

- User absence does not pause the actor (Sorok 100 §E).
- The interface must not claim events happened while the user was absent unless they are actual persisted events.
- Unperceived events remain `UNKNOWN`; use CP-A5 `unperceived_event_count`/`ask()` behavior as the acceptance model.
- No actual absence/life-advance producer is present in the inspected outputs; WP-19 must not simulate it.

### REFUSAL

- Refusal is a visible actor action/answer, not an error or hidden-state inference.
- Where exact speech exists, show it verbatim with the actor-visible surface.
- Do not infer motive, consent, liking or learned practice from a refusal.
- Exact JOIN-E refusal acceptance example is in §7/A7.

## 5. Accessibility acceptance requirements

WP-19 must implement and test:

1. **Keyboard-only**: every control (SAY input, DO, ATTEND, WAIT, EXIT, RETURN) reachable without pointer.
2. **Focus order**: transcript → input → actions → exit/return; visible focus indicator; no focus trap except explicit modal clarification with an accessible escape.
3. **Screen-reader labels**: each control has an accessible name and state; mode changes (`PORTAL`/`OUTSIDE`), clock, location, new event and refusal are announced.
4. **Text alternatives**: gestures and visual cues have text equivalents (e.g. `A looks at the empty tool space.`); no meaning conveyed by color alone.
5. **Exit always available**: `EXIT` visible and announced; `Escape` does not discard input silently; confirmation/return is explicit.
6. **Return always explained**: if no lawful return exists, say so and show the actual route; no fake button.
7. **Uncertainty announced**: `UNKNOWN`, clarification and typed holds are text, not a silent empty area.
8. **No real-time typing pressure**: portal scene time is not wall-clock typing speed (Sorok 32 §6).
9. **Screen-reader event order**: announce events in persisted clock/sequence order; do not announce unperceived events.
10. **Reduced motion / no animation-only information**: every animation has a static text equivalent.

Acceptance criterion: a keyboard/screen-reader user can enter the portal, issue SAY/DO/ATTEND, wait, exit, return lawfully or see an explicit typed hold, and receive the same observable facts as a pointer/visual user.

## 6. Hidden-state non-disclosure

Never display to the user:

- hidden traits, affinity, trust, suspicion, motive, emotion or private actor model;
- unperceived event summaries, hidden market commissions, private B/C activity or future outcomes;
- relationship scores, rarity, completion, unlock levels or progress bars;
- private actor state merely because CP-A5 can read test internals;
- a narrator explanation of a hidden cause.

Lawful visible evidence is only the outward observable event, exact spoken utterance, observable gesture/action, user-lawful perception and explicit `UNKNOWN`.

## 7. Acceptance examples from existing encounter outputs

### A1 — SAY visible (refusal)

Given the JOIN-E targetless refusal output at `5e6367` (`targetless_refusal.json`, blob `54bd91c6…`):
- `accepted=false`
- `strategy=HELP_REFUSE`
- `speech="The tool's gone. I can't do it today."`
- `gesture="A looks at the empty tool space."`
- `surface=["the repair worker says: \"The tool's gone. I can't do it today.\" A looks at the empty tool space."]`
- `tools_remaining=0`

When the portal displays the refusal, then it shows the exact speech/gesture/surface and does not infer B's motive or A's hidden state.

### A2 — SAY visible (accept)

Given the existing JOIN-E performed-share / omitted-A encounter output in `WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/evidence/actual_a_evidence.json` (blob `6d0a2978…`), `performed-omit.join_e.help`:
- `accepted=true`
- `strategy=HELP_ACCEPT`
- `speech="Put your hand on the near edge. I'll take the slack."`
- `gesture="A clears a space at the bench."`
- `tools_remaining=1`

Then the portal may show the exact speech/gesture as observable; it does not claim a relationship score or hidden affection.

### A3 — DO visible (inspect / repair)

Given the existing JOIN-E encounter outputs (`performed-e2` for `INSPECT`, `performed-omit` for `REPAIR`):
- `INSPECT` `{"changed": false}` at clock 10 with event id `TEST_ONLY_BP4_WORLD_EVT_a50e6ddd…` (`performed-e2`);
- `REPAIR` `{"cash_delta": 2, "completed_delta": 1, "hours_delta": -1, "material_delta": -1, "source_owned": true}` at clock 10 (`performed-omit`).

When the user observes A inspect/repair, the portal shows the observable action and actual material result, not hidden actor state.

### A4 — ATTEND visible / unperceived held

Given CP-A5 `EncounterReader.view()` (`9137653`, `encounter.py` blob `8d388c2f…`) exposes:
- `remembered_events[]` with event id/kind/clock/location/summary;
- `unperceived_event_count=4` in the executed trace;
- `ask("What happened to the workshop tool?")` → `status=OK`, exact answer `"A perceived B take the workshop tool, could not repair while it was away, and perceived its return."`, three evidence event ids, `read_only=true`;
- `ask("What did B do at the market?")` → `status=UNKNOWN`, exact answer `"UNKNOWN: A did not perceive B's market commission."`, `evidence_event_ids=[]`, `read_only=true`.

When the user attends a remembered event, the interface may show only that event's visible summary. When the user attends the unperceived market commission, it must show `UNKNOWN` and no market detail.

### A5 — WAIT typed hold

Given no actual wait/time-advance producer exists in JOIN-E/CP-A5, when the user selects `WAIT`, then:
- display `WAIT_UNSUPPORTED_TYPED_HOLD`;
- do not advance the persisted clock;
- do not append a world event;
- keep the last actual visible clock/events unchanged.

### A6 — EXIT / RETURN typed hold

Given no actual user-facing exit/return/absence producer exists in JOIN-E/CP-A5, when the user selects `EXIT`, then:
- display `LOCAL_EXIT_ONLY`;
- close/leave the portal view only;
- do not fabricate an actor leave event or relationship change.

When the user requests `RETURN` without a lawful meeting/opportunity/channel, then display `RETURN_UNSUPPORTED_TYPED_HOLD`; do not teleport or reopen a thread.

### A7 — Refusal / absence distinction

Given the JOIN-E refused-B source output (`5e6367`, `b_event_contrast.json`, blob `b2d819af…`):
- `refused_help={"accepted": false, "strategy": "HELP_REFUSE"}`;
- `omitted_help={"accepted": false, "strategy": "HELP_REFUSE"}`;
- `performed_help={"accepted": true, "strategy": "HELP_ACCEPT"}`.

Then the interface may show the same public `HELP_REFUSE` surface for different B histories, but must not infer B's private cause, A's motive or a forced speech contrast.

### A8 — Hidden-state non-disclosure

Given the CP-A5 market question returns `UNKNOWN` while the C12 history contains the market commission, when WP-19 renders the encounter, then it must not display the market commission summary, event id or hidden cause. It may display `UNKNOWN` and the count of unperceived events only if sourced.

## 8. Actual available data vs missing producers

### Actually available at this cut

- C12 `world_events` and `perceptions`; clock, location, actor-visible event fields (JOIN-E).
- E expression admission with exact `speech`, `gesture`, `strategy`, `surface`, `accepted` (JOIN-E/R31E).
- CP-A5 read-only `view()`/`ask()`: `known_event_ids`, `remembered_events`, `unperceived_event_count`, `tool_available`, `read_only`, `UNKNOWN` answers.
- JOIN-E performed/omitted/refused E help contrast.
- Material/tool availability from actual world state.

### Missing producers (exact dependencies)

| Missing producer | Required receipt | WP-19 interim behavior |
|---|---|---|
| `USER_SAY_DO_ATTEMPT_ADMISSION` | user attempt, parse/clarification, admitted/performed/refused, event id/clock | local input only; no world write; use actual C12 events for display |
| `USER_ATTEND_RECEIPT` | target, perceived event/object, clock, focus result, no world write | `LOCAL_ATTEND_ONLY`; `UNKNOWN` for unperceived |
| `WAIT_TIME_ADVANCE_RECEIPT` | clock before/after, performed/omitted, events, reason | `WAIT_UNSUPPORTED_TYPED_HOLD`; no clock/event change |
| `PORTAL_EXIT_RETURN_RECEIPT` | exit/return actor or user action, root/branch/clock, absence interval, lawful route | `LOCAL_EXIT_ONLY` / `RETURN_UNSUPPORTED_TYPED_HOLD` |
| `USER_ABSENCE_LIFE_ADVANCE` | absence interval, independent events, perception filter, return state | do not simulate; show only actual persisted events |
| `MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY` | channel route, consent, message event, delivery time | no thread if no actual channel; no fabricated messages |
| `ACCESSIBILITY_PREFERENCE_ACK` | preference, announcement policy, acknowledgement | local preferences only; no world write |

These are source-level dependencies, not permission to invent actor choice or native law.

## 9. WP-19 consumption

WP-19 may build the low-fidelity interface directly from this spec:

1. render `visible_events`/`remembered_events` from actual data;
2. expose `SAY/DO/ATTEND/WAIT/EXIT` controls with the visible/hidden rules;
3. implement the accessible requirements in §5;
4. use typed holds for every missing producer in §8;
5. use A1–A8 as acceptance tests, not as a human trial;
6. never display hidden actor state or unperceived event content;
7. never claim native, scientific, human or relationship-score success.

## 10. Limits

- No runtime, human participant, provider call or guide edit is made by this specification.
- Existing encounter outputs are TEST_ONLY sourcefree; they are UX evidence, not native personhood or empirical usability.
- The missing producers above must be supplied by their competent owners before S11 can claim actual SAY/DO/ATTEND/wait/exit/return production.
- No new psychology, relationship metric or acquired-practice claim.
