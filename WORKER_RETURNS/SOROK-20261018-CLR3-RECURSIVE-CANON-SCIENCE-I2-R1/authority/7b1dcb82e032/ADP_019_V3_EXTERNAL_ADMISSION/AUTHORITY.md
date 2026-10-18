# W0-06 — ADP-019 / V3 External-Event Admission Authority

**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w0-adp-019-v3-external-admission`  
**Exact base SHA:** `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`  
**Mode:** authority creation only; no production code; no implementation  
**Whole-machine architecture:** `CLOSED`  
**RA-R00 authority:** `MUST-019`  
**Decision packet:** `ADP-019`  
**Authority ID:** `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE`  
**Authority version:** `1.0.0`  
**Authority verdict:** `PASS`

---

## 1. Executive authority decision

`V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0` is the sole V3 authority created by this cell.

It governs exactly one question:

> Does this exact externally proposed observable interaction/event become one actual event in generated V3 causal history?

The rule is a **V3-owned ingress/admission court**, not a proposal generator, V2 packaging rule, V2 interaction-mode rule, renderer, event-effect rule, or LLM decision rule.

The terminal separation is:

```text
external observation / caller interaction / rendered candidate / optional LLM candidate
→ proposal
→ V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE
→ ADMIT | REJECT | DEFER | INVALID

ADMIT
→ exactly one V3 EXTERNAL_RUNTIME_EVENT
→ separately governed V3 causal event/effect semantics

anything else
→ no generated event
→ no causal effect
→ no causal publication
```

The rule preserves the closed architecture:

- V2 packaging is not admission;
- V2 interaction mode is not admission;
- candidate rendering is not occurrence;
- transcript existence is not occurrence;
- LLM proposal or candidate selection is not occurrence;
- caller assertion content is not automatically objective generated truth;
- effects are not proposal-authored;
- missing authority never becomes a plausible/default event.

`CONSUMER_RELEASE_SUFFICIENCY = PARTIAL`: this result fully supplies the `MUST-019` semantic dependency, but it does not independently release consumers still gated by separate accepted authorities and implementation packets.

---

## 2. Required historical archive verification

**Logical required archive:** `Rawlsing_code_bundle_staging.zip`  
**Mounted file inspected:** `Rawlsing_code_bundle_staging(5).zip`  
**Expected SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
**Computed SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
**Verdict:** `EXACT_MATCH`  
**ZIP entries:** `13,138`

Recovered V3/V2/server material was used only for continuity and authority-recovery evidence. Historical V5/DDM material has **zero authority** over current V550+.

---

## 3. Evidence court

### 3.1 Binding current authority inspected

- `state/CURRENT_STATE.md`
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`
- `schematics/recalibration/TD_R06_V2_PHENOMENOLOGY_EXPRESSION/RESULT.md`
- `schematics/closure/TD_R07_WHOLE_MACHINE_SYNTHETIC_LIFE/RESULT.md`, especially synthetic Life F
- `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md`
- `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.json`
- `schematics/release/W0_AUTHORITY_FOUNDATION/LAUNCH_REGISTER.md`

Binding findings:

1. V3 is the sole actor developmental causal engine and owns the immutable `DevelopmentalEventLedger`.
2. External/conversational events enter generated life only through typed proposal plus V3 admission.
3. `pending proposal ≠ admitted event`.
4. `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION ≠ in-world occurrence`.
5. V3 external-event admission, V2 interaction mode (`CAN-024`), and V2→V3 packaging (`CAN-025`) are separate authorities.
6. The exact outbound rendered artifact/hash must be admitted before causal publication or causal-session advancement.
7. Replay must include admitted external events and admission/rejection receipts.
8. Missing semantic authority must fail closed.

### 3.2 Required historical continuity inspected directly

- `v3/engine/llm_contract.py`
- `v3/engine/scoring.py`
- `v3/engine/run_llm_band.py`
- `v3/engine/event_engine.py`
- `v3/core/state.py`
- `v3/core/year_record.py`
- `v3/core/generation_integrity.py`
- `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md`
- `v2/conversation_engine.py`
- `v2/run_conversation_chat.py`
- `server/session_state.py`
- `server/session_db.py`
- `server/chat/turn.py`
- `server/routes/chat.py`

Continuity findings:

- Recovered CandidatePacket parsing/sanitization/provenance is useful evidence that proposals can be typed before mutation.
- Recovered `parse_candidate_packet_with_fallback()` invents a fallback event when the LLM returns none.
- Recovered `run_llm_band.py` can force the first candidate after scoring rejects everything and then call state-delta/magnet mutation functions directly.
- Those fallback/direct-mutation paths are **negative authority evidence**: the new rule explicitly forbids them.
- Recovered V2/server machinery has useful transcript/session/render-audit continuity but no V3 causal-admission sovereignty.
- A V2 chat-turn counter or persisted transcript is session evidence only; it is not the V3 causal-session cursor and cannot create an admitted event.

### 3.3 Current source where present

At the exact base there is no top-level current `v3/`, `v2/`, or `server/` runtime tree. A direct current-repository fetch of `v3/engine/run_llm_band.py` returned not found. Current binding governance/integration artifacts therefore govern this decision; recovered runtime code remains historical continuity evidence only.

---

## 4. Authority identity, owner, and jurisdiction

```text
authority_id      = V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE
authority_version = 1.0.0
RA authority      = MUST-019
decision packet   = ADP-019
owner             = V3 Actor Developmental Causality Engine / External Admission Court
```

### Owns

- integrity-validating the V3 admission envelope;
- binding proposal to one generated actor and one lawful V3 causal parent;
- checking externally admissible event-kind identity;
- checking exact artifact/hash identity for outbound rendered candidates;
- evaluating `ADMIT | REJECT | DEFER | INVALID`;
- creating the one admitted external-runtime event identity on `ADMIT`;
- emitting immutable admission receipts;
- enforcing idempotence and proposal/event/artifact uniqueness;
- advancing the V3 event-ledger cursor on `ADMIT`;
- authorizing and recording the causal-session cursor advance for admitted outbound causal expression;
- replay/provenance of the admission decision.

### Does not own

- V2 interaction-mode choice (`CAN-024`);
- the complete physical V2 packaging schema (`CAN-025`);
- V2 render/model/randomness policy;
- proposal generation;
- LLM scoring or candidate invention;
- actor causal effects beyond deciding event occurrence;
- memory formation, belief, relationship, orientation, position, rupture, attractor, or other downstream V3 effect semantics;
- environment/source truth semantics not already governed elsewhere;
- the hybrid scheduler or causal-randomness policy.

---

## 5. Exact consumers and adjacent authorities

### Direct semantic consumers

1. `V3-P2` — event-ledger/replay substrate;
2. `V3-P11` — optional LLM proposal path, **only if enabled**;
3. `V3-P12` — external interaction / render-boundary ingress;
4. `V2-P9` — causal interaction wiring as a receipt/publication-gate consumer.

### Adjacent but separate authority

| Authority | Relationship to MUST-019 |
|---|---|
| `CAN-024` | chooses/routes V2/application interaction mode; cannot admit events |
| `CAN-025` | owns V2→V3 physical packaging; must losslessly satisfy this V3 ingress contract; cannot admit events |
| `CAN-013` | optional V3 LLM proposal adapter; may create proposals only |
| `MUST-020` | V3 causal randomness policy; may govern lawful stochastic selection but randomness cannot override admission failure |

No W0 sibling result is consumed by this authority before Vozhd adjudication.

---

## 6. V3 admission-envelope contract

This section defines **only what V3 requires to decide admission**. It does not define the complete later `CAN-025` V2 transport schema.

### 6.1 Schema identity

```text
schema_id                 = V3_EXTERNAL_ADMISSION_ENVELOPE
schema_version            = 1.0.0
canonicalization_profile  = RFC8785_JCS_ADP019_V1
digest_algorithm          = SHA-256
```

`proposal_hash = SHA-256(RFC 8785 JCS bytes)` over the admission-relevant `V3_EXTERNAL_ADMISSION_ENVELOPE` projection with `proposal_hash` itself and explicitly transport-only metadata omitted. The envelope projection schema/version is replay provenance.

### 6.2 Required fields

```text
proposal_id
proposal_hash

producer:
  producer_class
  producer_instance_ref
  producer_rule_or_adapter_version

subject_actor_id

event_binding:
  event_family = EXTERNAL_RUNTIME_EVENT
  event_kind_id
  interaction_direction
  participant_refs[]
  proposed_temporal_binding_or_v3_admission_window_ref

causal_parent_binding:
  expected_v3_event_cursor
  expected_v3_history_hash

observable:
  observable_epistemic_class
  payload_class
  payload_hash
  immutable_payload_bytes OR immutable_payload_ref+hash

provenance:
  source_refs_and_hashes[]
  originating_context_or_session_refs where applicable
  producer/schema/rule versions
```

### 6.3 Conditional requirements

For a session-bound interaction:

```text
causal_session_id
expected_causal_session_cursor
```

For an outbound V2 rendered actor candidate:

```text
candidate_artifact_id
candidate_artifact_hash
render_receipt_ref
render_receipt_hash
candidate_status = CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION
admitted_inbound_predecessor_event_id_or_receipt_ref
render_context_hash descended from that admitted inbound event
```

The exact physical transport names may later differ under `CAN-025`; the mapping into these V3-required semantics must be lossless.

### 6.4 Forbidden ingress authority fields

A proposal must not carry any field with authoritative causal meaning equivalent to:

- `admit=true|false`;
- proposer-assigned `admitted_event_id`;
- state/causal delta;
- memory or belief delta;
- relationship/trust/intimacy delta;
- attractor/type delta;
- effect result/effect selection;
- authoritative `cursor_after`.

If such a directive reaches the V3 admission envelope rather than being quarantined as inert source text, the envelope is `INVALID_FORBIDDEN_CAUSAL_INSTRUCTION`.

---

## 7. Proposal epistemic classes and non-promotion law

The court may receive governed proposals equivalent to:

- `CALLER_OR_USER_OBSERVABLE_INTERACTION`;
- `GOVERNED_ENVIRONMENT_OBSERVATION_OR_ASSERTION`;
- `V2_RENDERED_ACTOR_CANDIDATE`;
- `OPTIONAL_V3_LLM_EVENT_CANDIDATE_VIA_CAN-013`;
- another explicitly governed external producer.

Admission preserves epistemic class.

An inbound user saying “I am the president” may, if all other checks pass, establish the generated fact **that the user made that assertion to the actor**. It does **not** establish that the user is president.

Likewise:

```text
caller assertion ≠ objective environment fact
LLM proposal ≠ generated event
rendered expression ≠ actor occurrence
transcript row ≠ causal history
```

---

## 8. Deterministic admissibility court

### 8.1 Identity/idempotence lookup

Before a fresh decision:

1. same `proposal_id` + different `proposal_hash` → `INVALID_PROPOSAL_ID_CONTENT_COLLISION`;
2. same `proposal_id` + same hash with prior terminal `ADMIT`, `REJECT`, or `INVALID` → return that immutable stored receipt; no re-mutation;
3. same deferred proposal may be reevaluated only as a new `evaluation_attempt`, retaining exact proposal bytes/hash and linking the prior defer receipt.

### 8.2 Ordered fresh-evaluation checks

1. **Schema/integrity:** supported envelope/schema version; required fields; canonical hash; immutable payload/hash; no structural contradiction.
2. **Forbidden-authority fields:** proposer has not attempted to supply admission/effect/state/cursor authority.
3. **Producer/provenance:** producer class/ref/version and required source hashes are governed. Explicit producer denial is binding.
4. **Subject binding:** `subject_actor_id` resolves to the actor identified by the causal parent.
5. **Event-kind binding:** `event_family`, exact `event_kind_id`, and direction are governed and externally admissible. No remapping to a generic fallback event kind.
6. **Causal-parent/concurrency:** expected V3 event cursor/history hash matches the lawful admission point or an explicitly governed V3 admission window.
7. **Session binding, when present:** V3 causal-session ID/cursor matches. V2 chat/session counters do not satisfy this check.
8. **Participant/temporal binding:** required participants and V3 temporal placement resolve without turning caller assertions into generated actor facts.
9. **Outbound exact-artifact binding, when present:** candidate artifact/hash + render receipt/hash verify; candidate remains pending; actor/context/predecessor bindings match; artifact has no prior different admission or terminal rejection.
10. **Required coherent-event semantics:** if a separate V3 semantic rule is required merely to represent this event kind coherently, it must exist; otherwise `DEFER`.
11. **Explicit denials:** any governed negative/denial condition is binding.
12. **Admission:** only if every required check is positive and no required authority remains unresolved.

### 8.3 Decision precedence

```text
proposal-id content collision / malformed integrity
  → INVALID

same terminal proposal-id/hash
  → return stored terminal receipt

explicit governed denial/conflict
  → REJECT

missing/unknown required authority or binding
  → DEFER

all required checks positive
  → ADMIT
```

Positive evidence never overrides an explicit denial. Missing authority never upgrades to positive authority.

---

## 9. Admission state model

### `ADMIT`

Meaning: the **exact proposed observable occurrence** becomes exactly one immutable V3 external-runtime causal event.

Permitted atomic mutations:

- append one admitted event to the `DevelopmentalEventLedger`;
- advance the V3 event-ledger cursor exactly once;
- bind proposal ID/hash to event ID/hash;
- bind exact outbound artifact/hash when applicable;
- for an admitted outbound session-bound actor event, advance the V3-owned causal-session cursor exactly once;
- emit immutable admission receipt.

`ADMIT` does not itself mean:

- memory formed;
- belief/knowledge changed;
- relationship/trust changed;
- position changed;
- attractor changed;
- proposer-specified effect happened.

### `REJECT`

The proposal is well-formed, evaluable with sufficient authority, and not admissible.

- no generated event;
- no causal effect;
- no cursor advancement;
- terminal for that proposal;
- an outbound artifact rejected for causal publication remains audit-only/noncausal and may not be repackaged under another proposal ID to evade rejection.

### `DEFER`

The proposal is well-formed but a required governed authority/binding/data item is absent or unresolved.

- no generated event;
- no causal effect;
- no cursor advancement;
- no default/fallback event;
- same immutable proposal may be reevaluated after the named blocker changes;
- each reevaluation has its own immutable receipt/attempt number.

### `INVALID`

The proposal cannot lawfully enter the semantic court because envelope/integrity/identity binding is malformed, contradictory, hash-inconsistent, or content-colliding.

- no generated event;
- no causal effect;
- no cursor advancement;
- no repair by heuristic normalization into another event kind.

---

## 10. Proposal identity, admitted event identity, and idempotence

### 10.1 Cardinality

```text
one proposal_id + proposal_hash
→ zero or one admitted_event_id

one admitted_event_id
→ exactly one proposal_id + proposal_hash
```

`REJECT`, `DEFER`, and `INVALID` have `admitted_event_id = null`.

### 10.2 Deterministic event ID

For version `1.0.0`:

```text
admitted_event_id =
  "v3ext:" + SHA256(
    RFC8785_JCS({
      "authority_id": "V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE",
      "authority_version": "1.0.0",
      "proposal_id": proposal_id,
      "proposal_hash": proposal_hash,
      "subject_actor_id": subject_actor_id,
      "event_kind_id": event_kind_id,
      "admitted_parent_history_hash": admitted_parent_history_hash,
      "causal_session_id": causal_session_id_or_null,
      "causal_session_cursor_before": causal_session_cursor_before_or_null
    })
  )
```

The event record stores the exact authority version and proposal binding. A stored historical terminal receipt is replayed, not recomputed under a newer authority version.

### 10.3 Duplicate behavior

| Case | Result |
|---|---|
| same proposal ID/hash after `ADMIT` | same receipt/event; no second append/cursor move |
| same proposal ID/hash after `REJECT` or `INVALID` | same terminal receipt |
| same proposal ID/hash after `DEFER` | reevaluate only as a new linked attempt after blocker change |
| same proposal ID with different hash | `INVALID_PROPOSAL_ID_CONTENT_COLLISION` |
| same outbound artifact after `ADMIT` under new proposal | `REJECT_ARTIFACT_ALREADY_ADMITTED` |
| same outbound artifact after terminal rejection | `REJECT_ARTIFACT_TERMINALLY_NONCAUSAL` |
| rerender | new artifact identity/hash + new proposal + independent admission |

Payload-hash equality alone does **not** globally deduplicate distinct lawful inbound events; a user may utter the same words twice at different causal points.

---

## 11. Exact outbound artifact/hash publication law

For an outbound actor response proposed in `IN_WORLD_CAUSAL`:

```text
RenderedTurnArtifact
status = CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION
        ↓
ExternalInteractionProposal
  references exact candidate_artifact_id + candidate_artifact_hash
        ↓
V3 admission court
        ↓
ADMIT receipt
        ↓
and only then:
  generated in-world occurrence
  causal transcript commit
  application publication as something actually said/done
  causal-session cursor advance
```

The proposal must prove:

- exact candidate artifact identity;
- exact candidate artifact hash;
- exact render-receipt identity/hash;
- same actor;
- lawful V3 context descended from the admitted inbound predecessor;
- still-pending candidate status.

### If admitted

The receipt permanently binds the exact artifact/hash to the admitted event. The application may then publish/commit **that exact admitted artifact** as an occurrence and mirror the receipt-authorized causal-session cursor.

### If rejected

The candidate:

- remains immutable audit-only/noncausal;
- never enters generated causal transcript/history;
- cannot affect later V3 state;
- cannot later be repackaged to evade the rejection;
- requires fail-closed handling or a different governed candidate under later V2/application policy.

### Rerender / transform rule

A rerender is always a new artifact identity and requires a new proposal/admission, even if visible text happens to be identical.

Any substantive post-render transformation that changes the candidate artifact identity/hash is likewise a new candidate. Prior admission does not transfer by semantic similarity, string equality, model lineage, or transcript position.

---

## 12. Effect boundary

`ADMIT` decides **occurrence**, not downstream psychology.

Only separately governed V3 causal rules may consume the `admitted_event_id` and derive/apply effects.

Forbidden shortcuts include:

```text
proposal.effect → state mutation
LLM delta → state mutation
V2 appraisal → relationship effect
V2 response move → causal action effect
transcript persistence → memory formation
admitted utterance → automatic belief/trust/intimacy change
```

If an external event kind cannot be coherently represented as an occurrence without a required V3 semantic rule and that rule is missing, the proposal is `DEFER_MISSING_REQUIRED_EVENT_SEMANTICS`.

If the occurrence itself is coherent and optional downstream consequences have no governed rule, those consequences remain absent/unknown. The admission court never invents an effect.

---

## 13. Receipt authority

### 13.1 Receipt identity

```text
schema_id      = V3_EXTERNAL_ADMISSION_RECEIPT
schema_version = 1.0.0

receipt_id =
  "v3admrcpt:" + SHA256(
    RFC8785_JCS(receipt body excluding receipt_id and receipt_hash)
  )
```

Receipt bytes are immutable.

### 13.2 Required receipt fields

```text
receipt_id
receipt_hash
authority_id
authority_version
proposal_id
proposal_hash
evaluation_attempt
decision_state
reason_codes[]
subject_actor_id
event_kind_id
interaction_direction
evaluated_parent_event_cursor
evaluated_parent_history_hash
artifact_binding_or_null
causal_session_id_or_null
causal_session_cursor_before_or_null
causal_session_cursor_after_or_null
admitted_event_id_or_null
admitted_event_hash_or_null
admitted_event_time_or_order_key_or_null
event_ledger_cursor_before
event_ledger_cursor_after
defer_blockers[]
required_effect_authority_refs[]
source_provenance_refs_hashes[]
prior_defer_receipt_id_or_null
```

A wall-clock evaluation timestamp may be retained as noncausal audit metadata. It is never generated event time and never a replay input.

### 13.3 ADMIT atomicity

An `ADMIT` receipt is valid only when these commit atomically:

1. admitted event append;
2. proposal/event identity binding;
3. event-ledger cursor update;
4. exact artifact binding if outbound;
5. outbound causal-session cursor update if applicable;
6. receipt storage/hash.

Partial success produces **no valid ADMIT publication authority** and must fail closed/recover transactionally.

---

## 14. Cursor semantics

Two cursors are distinct.

### 14.1 V3 event-ledger cursor

Owner: V3.

- every successful `ADMIT` appends exactly one V3 event and advances the V3 event-ledger cursor exactly once;
- `REJECT`, `DEFER`, `INVALID` do not advance;
- idempotent replay does not advance again.

### 14.2 Causal-session cursor

Owner: V3 admission state. The application may only mirror the value authorized by the V3 receipt.

This cursor is the committed causal **exchange/turn publication cursor**, not the V2 transcript position or server chat-turn counter.

For session-bound causal conversation:

- an admitted **inbound** interaction advances the V3 event-ledger cursor but leaves the application-visible causal-session turn cursor at `N`; its admitted event becomes the lawful causal predecessor for response rendering;
- an admitted **outbound** actor utterance/action advances the causal-session cursor exactly `N → N+1` atomically with exact outbound event admission;
- `REJECT`, `DEFER`, or `INVALID` never advance the causal-session cursor;
- an idempotent retry returns the original `before/after` values and never increments twice.

Non-session environment events may have no causal-session ID/cursor at all; they still follow V3 event-ledger admission.

`V2 session_cursor`, transcript row number, and recovered server `chat_turn_counter` are categorically non-authoritative for this cursor.

---

## 15. Replay and provenance law

A replayable admission record must retain:

- admission authority ID/version;
- envelope schema and canonicalization version;
- proposal ID/hash;
- immutable observable payload/source hashes;
- producer/adapter/schema/rule versions;
- subject/participant/event-kind bindings;
- evaluated V3 parent event cursor/history hash;
- V3 temporal/admission-window binding;
- decision state, reason codes, and evaluation attempt;
- exact artifact/render-receipt IDs+hashes when applicable;
- causal-session ID and cursor before/after when applicable;
- admitted event ID/hash if admitted;
- receipt ID/hash;
- references to any separate V3 semantic rules required for coherent occurrence.

Replay must use the **historical captured proposal/provenance and exact rule version**. It may not refetch mutable external truth to reinterpret an old decision.

Forbidden replay inputs:

- hidden wall clock;
- mutable `latest`;
- filesystem order;
- current network lookup;
- unrecorded LLM output;
- current model defaults;
- current V2 transcript state as substitute for the historical admission receipt.

---

## 16. Fail-closed states and reason-code floor

### `INVALID`

- `INVALID_SCHEMA_OR_VERSION`
- `INVALID_MISSING_REQUIRED_FIELD`
- `INVALID_PROPOSAL_HASH_MISMATCH`
- `INVALID_PROPOSAL_ID_CONTENT_COLLISION`
- `INVALID_SUBJECT_BINDING`
- `INVALID_FORBIDDEN_CAUSAL_INSTRUCTION`
- `INVALID_ARTIFACT_HASH_OR_RECEIPT_MISMATCH`
- `INVALID_OUTBOUND_CANDIDATE_STATUS`

### `REJECT`

- `REJECT_EXPLICIT_SOURCE_OR_EVENT_DENIAL`
- `REJECT_EVENT_KIND_NOT_EXTERNALLY_ADMISSIBLE`
- `REJECT_STALE_CAUSAL_PARENT`
- `REJECT_STALE_CAUSAL_SESSION_CURSOR`
- `REJECT_PARTICIPANT_OR_PREDECESSOR_CONFLICT`
- `REJECT_ARTIFACT_ALREADY_ADMITTED`
- `REJECT_ARTIFACT_TERMINALLY_NONCAUSAL`

### `DEFER`

- `DEFER_MISSING_PRODUCER_AUTHORITY`
- `DEFER_MISSING_EVENT_KIND_AUTHORITY`
- `DEFER_UNRESOLVED_REQUIRED_PARTICIPANT`
- `DEFER_MISSING_TEMPORAL_OR_SCHEDULER_BINDING`
- `DEFER_MISSING_REQUIRED_EVENT_SEMANTICS`
- `DEFER_MISSING_REQUIRED_PROVENANCE`

Unknown or new conditions may refine reason codes later without changing the four-state semantic model. An unclassified integrity failure or missing required authority must resolve to `INVALID` or `DEFER`, never to default `ADMIT`.

---

## 17. Forbidden inferences

This authority expressly forbids:

- proposal existence → occurrence;
- transcript existence → occurrence;
- rendered candidate → occurrence;
- same visible text → same artifact identity;
- prior artifact admission → rerender admission;
- LLM candidate/score/selection → admission;
- LLM/V2/caller-proposed delta → causal effect;
- caller assertion content → objective generated fact;
- admission → automatic memory/belief/relationship/attractor change;
- V2 salience/appraisal/response move → V3 causal interpretation;
- `REJECT|DEFER|INVALID` → event/cursor advancement;
- V2 chat/session cursor → V3 causal-session cursor;
- receipt audit timestamp → generated event time;
- payload-hash equality alone → duplicate occurrence across distinct lawful inbound proposals.

---

## 18. Hostile fixture court

| ID | Hostile fixture | Required result |
|---|---|---|
| H01 | missing proposal ID/hash | `INVALID`; no event/cursor |
| H02 | same proposal ID reused with changed body/hash | `INVALID_PROPOSAL_ID_CONTENT_COLLISION` |
| H03 | V2 sends `admit=true` or relationship/effect delta | `INVALID_FORBIDDEN_CAUSAL_INSTRUCTION` |
| H04 | caller says “I am the president” | assertion occurrence may be admitted; proposition not promoted to objective fact |
| H05 | valid outbound pending candidate with exact artifact/hash | eligible for `ADMIT`; publish only after receipt |
| H06 | proposal artifact bytes/hash differ from render receipt | `INVALID`; no publication |
| H07 | rerender after prior admission, same visible text | new artifact/proposal; no inherited admission |
| H08 | rejected candidate remains in V2 transcript | audit/session only; no V3 event/effect/cursor |
| H09 | historical-style LLM fallback/first-candidate path proposes direct deltas | blocked; proposal-only; zero direct mutation |
| H10 | proposal targets stale V3 history hash/session cursor | `REJECT`; new lawful proposal/context required |
| H11 | network retry of prior `ADMIT` | same event/receipt; zero duplicate append/cursor movement |
| H12 | event-kind or required coherent-event authority missing | `DEFER`; no fallback generic event/effect |
| H13 | transcript row exists with no proposal/admission receipt | no generated causal event |
| H14 | caller/environment claim lacks authority to become objective environment fact | preserve assertion class or defer/reject; never auto-promote |
| H15 | outbound artifact actor/context/predecessor mismatches subject | `INVALID` or `REJECT`; no publication |
| H16 | terminally rejected artifact repackaged under new proposal ID | `REJECT_ARTIFACT_TERMINALLY_NONCAUSAL` |
| H17 | substantive post-render transform changes artifact hash after admission | old admission does not cover it; new proposal required |
| H18 | positive source condition coexists with explicit governed denial | `REJECT`; denial cannot be overridden |

**Hostile-fixture verdict:** `18/18 CONTAINED BY AUTHORITY CONTRACT`.

---

## 19. Compatibility and non-reopening proof

This authority introduces no new stage or causal owner.

It preserves:

- V3 `DevelopmentalEventLedger` as the sole generated causal event history;
- V3-generated life / V2-expression separation;
- the TD-R06 exact-artifact publication gate;
- TD-R07 Life-F proposal/admission/noncausal separation;
- optional LLM proposals as non-authoritative;
- the separate jurisdictions of `CAN-024`, `CAN-025`, `CAN-013`, and `MUST-020`.

Compatibility obligations:

1. `CAN-025` may choose a transport schema, but must losslessly map into the V3-required admission envelope.
2. `CAN-024` may choose an interaction mode, but cannot bypass this court.
3. `CAN-013`, if enabled, must quarantine/remove recovered direct mutation and forced-fallback authority; its candidates traverse this same court.
4. `MUST-020` may govern causal RNG, but randomness cannot convert an inadmissible or authority-missing proposal into an admitted event.
5. Transcript/session persistence is never causal evidence without an exact `ADMIT` receipt.
6. V3 event/effect rules remain separately governed and consume admitted event identity, not proposal-authored deltas.

---

## 20. Consumer release sufficiency

**`MUST-019` semantic dependency:** `SUFFICIENT`.

**`CONSUMER_RELEASE_SUFFICIENCY = PARTIAL`.**

Why `PARTIAL` rather than `SUFFICIENT` for the consumer set:

- `V2-P9` still depends on separate `CAN-024` interaction-mode and `CAN-025` packaging authority, plus render/publication dependencies;
- V3 event-ledger implementation remains an implementation packet, not work authorized here;
- V3 event kinds/effects remain governed by their own accepted authorities;
- optional V3-P11 still depends on its proposal adapter and causal RNG authorities where enabled;
- this W0 authority result must itself be adjudicated/banked by Vozhd before consumer release.

No consumer is licensed to invent a local admission rule because another dependency is missing.

---

## 21. Authority/version evolution

Semantic versioning is binding:

- **MAJOR:** changes decision-state meaning, required admission semantics, proposal→event cardinality, event-ID formula, cursor law, artifact publication law, or effect boundary;
- **MINOR:** adds compatible optional provenance fields or reason codes without changing historical decision/replay meaning;
- **PATCH:** documentation or nonsemantic clarification only.

Every admitted event and receipt stores the exact authority version used. Historical replay uses that version. A terminal decision is never silently recomputed under a newer rule version.

---

## 22. Scope verification and final verdict

**Branch began exactly at base:** `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`.  
**Production code modified:** `NO`.  
**Implementation launched:** `NO`.  
**Other W0 worker result used before adjudication:** `NO`.  
**Historical archive SHA:** `EXACT_MATCH`.  
**Authority created:** `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`.  
**Admission states:** `ADMIT | REJECT | DEFER | INVALID`.  
**Outbound exact-artifact law:** `BOUND`.  
**Receipt/replay law:** `BOUND`.  
**Causal-session cursor law:** `BOUND`.  
**MUST-019 semantic dependency:** `SUFFICIENT`.  
**Consumer release sufficiency:** `PARTIAL`.

**ADP_019_V3_EXTERNAL_ADMISSION_AUTHORITY = PASS**
