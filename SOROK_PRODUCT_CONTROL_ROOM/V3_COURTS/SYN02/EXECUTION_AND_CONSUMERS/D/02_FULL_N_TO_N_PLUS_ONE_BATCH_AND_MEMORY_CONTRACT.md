# SYN02-D / 02 — full N/N+1 batch, sequential realization and fallible retrospective contract

**Status:** `ARCHITECTURE_CONTRACT / SPECIFICATION_ONLY / NO IMPLEMENTATION / NO NATIVE RULE`.
**Supersedes for design purposes:** the current S48 one-call/one-prospective transport as a candidate for N11, not as a native positive.
**Sealed startup:** `cd1f4fd8158c2771d7c565b06ee397a7a60dc779`.
**Current source:** S42 `2489f8cd…`, S44 `923278fb…`, S45 `f26a138e…`, S46 `f0ef39b9…`, S47 `765a441f…`, S48 `9fe0d066…`, S49 `6604f2d9…`, S51 `2a4cdd2d…`, S52 `c821b488…`; JOIN-E `7bf2da30…`; S37 `e1f3c1da…`.

---

## 0. Contract decision

The target temporal cycle is:

```text
batch N-1 (already realized prefix)
  -> N+1 single LLM call:
       first half: actor-limited fallible retrospective/meaning
       second half: 3-5 conditional prospects for batch N
  -> post-call SCI05/ADP validation
  -> Rawlsing realizes batch N sequentially in clock order
       independent world/coactor, actual activity, actor access,
       C9 immediate response, CAN011 durable/NO_CHANGE/HELD,
       intervening lived interval
  -> committed prefix + unresolved suffix/faults
  -> next call
```

There is **one temporal LLM call per turn**, not Pass1/Pass2 plus retry. The current S48 transport has one call but only one prospective slot and no first-half retrospective; it is `TRANSPORT_REUSE_ONLY`, not N11.

The contract intentionally separates:

- objective occurrence;
- actor observation/access;
- subjective impression;
- transient recruitment/response;
- durable CAN011 state/operation/relation;
- fallible memory and later meaning;
- V2 expression.

No text output from an LLM is a hidden state write.

---

## 1. Type contracts

### 1.1 Turn and batch context

```text
TemporalTurn {
  turn_id: ContentId;                  // deterministic from actor/clock/parents/inputs
  actor_id: ActorId;
  branch_id: BranchId;
  state_version: StateVersionRef;
  world_version: WorldVersionRef;
  call_ordinal: uint;
  previous_batch_ref?: BatchRef;       // server-only internal linkage
  permitted_actor_access: ActorAccessScope;
  permitted_source_owners: SourceOwnerSet;
  temporal_policy: TemporalPolicy;
  created_at: LogicalClock;
}
```

`previous_batch_ref` is **not model-visible**. It is an internal linkage used to assemble `RetrospectivePacket`; it is never serialized into the model prompt.

### 1.2 Prospective batch (second half of call N)

```text
ProspectiveBatch {
  schema: "NEO_V3_PROSPECTIVE_BATCH@1";
  batch_id: ContentId;                 // local server identity
  actor_id: ActorId;
  branch_id: BranchId;
  expected_state_version: StateVersionRef;
  min_prospects: 3;
  max_prospects: 5;
  prospects: ConditionalProspect[3..5];
  batch_constraints: {
    allowed_event_kinds: EventKindRef[];
    forbidden_source_owners: SourceOwnerRef[];
    max_clock_span: Duration;
    requires_independent_world: bool;
  };
  source_visibility: ModelVisibleSourceRef[];   // legal references only
  uncertainty: UncertaintyLabel;               // not a coefficient
}
```

A batch is accepted only when it has 3–5 distinct `proposal_id`s, no duplicate ordinal, no unresolved forbidden reference and no model-visible target/source ID outside `source_visibility`. The engine may reject; it may not invent missing proposals.

```text
ConditionalProspect {
  proposal_id: LocalProposalId;       // model-local, not an objective event ID
  ordinal: 1..5;
  prospect_kind: EventKindRef;
  narrative_slots: {                     // compact, not full prose
    setting_ref?; object_ref?; activity_ref?; relation_ref?;
    possible_other_actor_role?
  };
  preconditions: ConditionExpr[];       // evaluated by owner services
  source_requirement: {
    world_source_owner: SourceOwnerRef;
    event_source_owner: SourceOwnerRef;
    coactor_source_owner?: SourceOwnerRef;
    actor_access_requirement: AccessRequirement;
  };
  proposed_clock_window: ClockWindow;
  interval_before: IntervalRequest;     // actual activity/time, no prose-only time
  expected_actor_access: AccessRequirement;
  expected_other_actor: OtherActorRequirement;
  possible_outcomes: PossibleOutcome[]; // realized / not performed / no change / held
  depends_on: ProposalDependency[];     // proposal IDs or retrospective claim IDs
  not_event_alternative: NO_EVENT | HELD_MISSING_RULE | SOURCE_UNAVAILABLE;
  uncertainty: UncertaintyLabel;
}
```

`depends_on` distinguishes:

- `proposal_dependency`: event B cannot be considered unless event A realized;
- `retrospective_claim_dependency`: event B is premised on an N+1 first-half self-claim and must be invalidated if SCI05 denies it;
- `world_dependency`: event B requires a particular world/source state;
- `coactor_dependency`: an independent B act/access must be present.

A conditional proposal is **not** a promise to create an event. `NO_EVENT` and `NOT_PERFORMED` are lawful outcomes; a missing rule is `HELD_MISSING_RULE`, not `NO_CHANGE`.

### 1.3 Batch realization

```text
BatchRealization {
  batch_attempt_id: ContentId;
  batch_id: ContentId;
  actor_id: ActorId;
  started_state_version: StateVersionRef;
  started_world_version: WorldVersionRef;
  policy: TemporalPolicy;
  entries: RealizationEntry[];          // at most 5, in ordinal order
  committed_prefix: CommittedEventRef[];
  unresolved_suffix: UnresolvedProspect[];
  batch_outcome: COMPLETE | PREFIX_COMMITTED | WHOLE_BATCH_REJECTED | HELD;
  receipt: BatchReceipt;
}
```

```text
RealizationEntry {
  proposal_id: LocalProposalId;
  ordinal: 1..5;
  status: PROPOSED
        | PRECONDITION_UNMET
        | SOURCE_HELD
        | COACTOR_HELD
        | ACCESS_NOT_RECEIVED
        | RULE_HELD
        | NOT_PERFORMED
        | NO_CHANGE
        | REALIZED
        | INTERVAL_HELD
        | DENIED;
  world_event_ref?: CanonicalWorldEventRef;
  actor_access_ref?: ActorAccessRef;
  response_ref?: C9ResponseRef;
  durable_decision_ref?: Can011DecisionRef;
  interval_ref?: LivedIntervalRef;
  committed_event_ref?: CanonicalEventRef;
  fault?: TypedFault;
}
```

An entry cannot be `REALIZED` without a canonical world event, actor access record (or explicit `NOT_RECEIVED`), a C9 response/held record and a durable/no-change/held decision. `world_event_ref` alone is not a realized person event.

### 1.4 N+1 retrospective packet

```text
RetrospectivePacket {
  schema: "NEO_V3_RETROSPECTIVE_PACKET@1";
  actor_id: ActorId;
  branch_id: BranchId;
  completed_batch_ref: internal BatchRef;  // server-only, not model-visible
  actor_accessible_history: ActorAccessibleEpisode[];  // only realized prefix
  memory_traces: ActorMemoryTrace[];
  contradictions: ContradictionRef[];
  allowed_uncertainty: UncertaintyLabel;
  omitted_counts: OmittedCountBucket;      // coarse; never exact unseen event count/order
  forbidden_feature_policy: AnalystFieldDenylist;
}
```

```text
ActorAccessibleEpisode {
  episode_ref: LocalEpisodeRef;      // not a C12 objective event ID/hash
  actor_local_time: LogicalClock;
  access_status: ACCESSIBLE | PARTIAL | DISTORTED | NOT_RECALLED;
  received_impression?: ActorImpressionRef;
  public_action?: PublicActionRef;
  memory_trace_ref?: ActorMemoryTraceRef;
  source_status: ACTOR_ACCESSIBLE | SOURCE_REVOKED | UNKNOWN;
}
```

The packet must not include:

- unresolved/suffix events;
- objective event IDs, hashes, ordinal/count/order of events the actor did not access;
- coactor private motives or analyst-only reasons;
- world facts outside the actor-access scope;
- `completed_batch_ref` in the prompt;
- hidden C9 mutation provenance or a full C12 record.

A coarse `omitted_counts` bucket is allowed only if it cannot reveal the number/order of inaccessible events; `NONE`/`SOME`/`MANY` must be precomputed under the access policy, not derived from a raw event ledger.

### 1.5 N+1 single-call envelope

```text
NPlusOneCallOutput {
  schema: "NEO_V3_TURN_ENVELOPE@1";
  retrospective_text: string;          // proposed narrative, not state
  self_account: null | string;         // proposed reflexive act, not state
  prospective: ConditionalProspect[3..5];
  proposal_ids: LocalProposalId[];
  uncertainty: UncertaintyLabel;
}
```

The same response contains both halves. There is no second normal LLM call for retrospective text and no separate Pass 2 that writes state. If a V2 display render is separately authorized after state commit, it is a non-causal surface render and cannot create or alter `self_account`, C9 or CAN011 state. The strict N11 path uses `retrospective_text` from this envelope as the surface narrative.

---

## 2. N/N+1 execution sequence

### 2.1 Call N (no previous completed batch or after prior batch)

1. Build `TemporalTurn` from the actor state/world versions and permitted access.
2. If a prior batch exists, build `RetrospectivePacket` only from its committed prefix and actor-access records.
3. Call the product **once** with `NPlusOneCallOutput` schema. The prompt includes only permitted actor-accessible history and legal source slots.
4. Parse 3–5 `ConditionalProspect`s. No 0/1/2 accepted as a full batch; no >5; no silent filler.
5. Before engine resolution, commit `ProspectiveBatch` as a **proposal record**, not an event. It has no world or actor effect.
6. `BatchRealizer` resolves in ordinal order (see §2.3).
7. Return `BatchRealization` with prefix/unresolved/faults and a `BatchReceipt`.

The model can condition the second half on the first-half text because both are in one generated response. That is a **linguistic dependency**, not a native SCI05 admission. Any proposal that says it is premised on the self-account must carry `retrospective_claim_dependency`.

### 2.2 Call N+1 (next turn)

```text
build RetrospectivePacket from committed_prefix
 -> one LLM call {retrospective_text, self_account, 3-5 prospective}
 -> parse / validate
 -> SCI05 postcall decision
 -> invalidate prospective entries whose retrospective_claim_dependency denied
 -> if remaining batch has <3 admissible prospects: typed BATCH_INCOMPLETE (no filler)
 -> realize each remaining event sequentially
```

No extra temporal LLM call. Replay of the same call uses the same `turn_id` and cached output; a retry after transport failure is not a new semantic call and must preserve `provider_call_count`/dispatch identity.

### 2.3 Sequential realization state machine

For each prospect in ordinal order:

```text
PRECONDITION
  fail -> PRECONDITION_UNMET (no event; no actor state)
  pass -> SOURCE
SOURCE
  world/event/coactor source absent or refused
       -> SOURCE_HELD / COACTOR_HELD
       -> commit no world event (or only a source-refusal record if owner allows)
       -> stop prefix under PREFIX_CONTIGUOUS
  present -> OCCURRENCE
OCCURRENCE
  world owner creates canonical occurrence + C8 event
       -> ACTOR_ACCESS
ACTOR_ACCESS
  no witness / not received -> ACCESS_NOT_RECEIVED
       -> world event may persist, no actor impression/response
       -> actor state unchanged; record access status
  witnessed -> C9
C9
  concrete CAN008 rule absent -> RULE_HELD (not NO_CHANGE)
  response chosen -> response record
       -> CAN011
CAN011
  concrete rule absent -> RULE_HELD
  rule says no change -> NO_CHANGE (durable decision record)
  rule says change -> commit durable target/state/operation
       -> INTERVAL
INTERVAL
  actual activity/time unavailable -> INTERVAL_HELD
  available -> LivedInterval committed
       -> COMMITTED_EVENT (only if event+access+response+durable/no-change complete)
```

`COMMITTED_EVENT` can represent a lawful no-change/no-event interval as well as a durable change; it must not be treated as “something dramatic happened.”

### 2.4 Prefix policy

Three policies must be explicit:

1. **`PREFIX_CONTIGUOUS` (recommended engineering default for external world)**
   Evaluate in ordinal order. The first held/denied/unresolved prospect terminates realization. The committed prefix is durable; suffix entries are recorded `UNRESOLVED_SUFFIX`, never as events. This matches truthful partial history and avoids fabricating later events after a denied predecessor.
2. **`INDEPENDENT_SUFFIX` (owner decision only)**
   A later proposal may be evaluated after a gap only if it has no `proposal_dependency`/`world_dependency` on the failed entry and its own source/access is valid. This permits non-contiguous life but requires explicit gap/order semantics. Not the default.
3. **`WHOLE_BATCH_ATOMIC` (owner decision only)**
   No actor/world effect is visible until all 3–5 entries resolve. This is inappropriate where an independent world/coactor action cannot be rolled back; it can be used for a contained simulation only. It must not be sold as “the batch happened” when an external B already acted.

The owner must choose among these; SYN02-D recommends `PREFIX_CONTIGUOUS` for real external encounters and records the alternative. It does not self-issue the policy.

### 2.5 Event 2 denied case (required)

If prospect 2 is `SOURCE_HELD`/`COACTOR_HELD`/`DENIED`:

- E2 is not a canonical event;
- E3–E5 are not realized under `PREFIX_CONTIGUOUS`, even if their textual proposals look independent;
- the batch receipt contains only the truthful prefix (E1 and any earlier entries);
- the N+1 retrospective packet contains only the realized prefix and the explicit gap/absence record if the actor could perceive it;
- no model-visible “E3 happened” state exists.

Under an owner-approved `INDEPENDENT_SUFFIX`, E3–E5 could be independently considered only with explicit gap records; the default design rejects accidental suffix execution.

---

## 3. SCI05 and internal-act dependency

### 3.1 First-half self-account is pending, not committed

The first-half text and `self_account` are **proposed** during the same call. They cannot write actor state, memory, practice, relation or target state at generation time. After the call:

```text
SCI05Admission {
  admission_id;
  turn_id;
  self_account_hash;
  status: PENDING | ADMITTED | DENIED | HELD;
  owner_ref;
  rule_version;
  source_refs;
  reason;
}
```

- `SCI05_HOLD`/`HELD` means no state change.
- `DENIED` means no state change and all `retrospective_claim_dependency` proposals invalidated.
- `ADMITTED` permits a separately owned `ReflectiveAct` transition; the text itself is not the state. The owner must write a typed `InternalAct` event with source, clock, actor, parent and rule version.

### 3.2 Dependency invalidation

```text
RetrospectiveClaim {
  claim_id;
  turn_id;
  text_ref;
  actor_access_refs[];
  source_grade;
  status: PENDING | ADMITTED | DENIED | HELD;
  contradictions[];
}
```

```text
ProposalDependency {
  kind: RETROSPECTIVE_CLAIM | PROPOSAL | WORLD | COACTOR | SOURCE;
  ref: ClaimId | LocalProposalId | WorldVersionRef | ActorId | SourceRef;
}
```

On denial, the engine marks dependent proposals `INVALIDATED_BY_SCI05` and does not realize them. A proposal with no such dependency remains independently admissible, but still must pass its own source/access/rule gates. The engine may not replace denied proposals to keep a five-event count.

### 3.3 No native mid-call approval

The single call cannot contain a native mid-call SCI05 interruption. The design accepts that the second half may be linguistically premised on an unadmitted first half; the postcall validator is the only actual admission point. This is the key limitation of the one-call architecture; it is preferable to adding an extra ordinary call because the latter would violate the user-settled cadence. The alternative is an explicit two-call design only after user/owner decision; it is not the recommended default.

---

## 4. Memory and actor-limited information

### 4.1 Distinct records

```text
ActorAccessRecord {
  access_id; actor_id; event_ref; access_clock;
  status: ACCESSIBLE | PARTIAL | NOT_WITNESSED | DISTORTED | REVOKED;
  scene_ref; source_refs[]; evidence_hash;
}
```

```text
ActorMemoryTrace {
  memory_id; actor_id; access_id; event_ref;
  trace_kind: EVENT | PRACTICAL | RELATIONAL | BODILY | LINGUISTIC;
  strength_label: STRONG | PARTIAL | WEAK | ABSENT;  // no invented numerical law
  uncertainty; source_refs[]; contradictions[]; last_recalled;
}
```

```text
ActorMemoryEpisode {
  episode_id; actor_id; event_ref; access_id;
  remembered_content_ref; recalled_at;
  fallibility: NONE | OMISSION | DISTORTION | CONFABULATION_WITH_SOURCE;
  source_grade; access_scope;
}
```

- `ActorMemoryEpisode` is not a copy of objective event text. It is an actor-accessible reconstruction with source grade and fallibility.
- A false belief is an `ADP017`-style proposition with provenance; it is not an invented positive episodic detail.
- Nondeclarative practical trace and episodic recall are separate; loss of source/access must invalidate dependent recall.
- The model-visible retrospective packet is generated from these records, never from raw C12 world events.

### 4.2 No leakage

The `RetrospectivePacket` must contain no:

- unresolved suffix event IDs or hashes;
- objective event order/count when not actor-accessible;
- `completed_batch_ref` (server-only);
- C9 mutation provenance;
- B private motive;
- full C12 state.

A coarse omission bucket may be included only if it is independent of the inaccessible count/order. If one permitted source feature is removed, all direct/indirect narration of that feature must cease; the packet builder must not reconstruct it from another field.

### 4.3 Subjective impression vs memory vs meaning

The contract distinguishes:

1. **occurrence** — world event admitted by C8;
2. **access** — ADP017 actor access witness;
3. **impression** — C9/CAN008 immediate actor-relative response;
4. **durable state** — CAN011 target/operation/relation/NO_CHANGE;
5. **memory** — ADP016 event/trace/episode with fallibility;
6. **meaning/self-account** — SCI05/admitted internal act, not narrative;
7. **expression** — V2 surface, non-causal.

A renderer may express only 1–6 through permitted access; it cannot author 3–6.

---

## 5. Current S48 mapping and required change

### 5.1 What S48 currently does

- `S48Session.run_turn` obtains one current event, builds one payload and calls a product runner once (`s48/session.py:202-290`).
- `parse_envelope` accepts `{narrative, self_account, prospective}`; `run_turn` rejects `len(prospective) != 1` (`s48/session.py:351-402`).
- `candidate_specs()` is `[]`; `issue_current_source` raises `SOURCE_OWNER_HOLD` (`s48/sources.py:17-26`).
- `self_account_present` returns `SCI05_HOLD` with `prospective_not_realized=true`; no dependency invalidation (`s48/session.py:326-349`).
- `build_payload` includes exact `event_ref`, `event_hash`, `event_ordinal`, `event_time`, occurred event, C9 result and world facts (`s48/product.py:61-115`); this is not an actor-limited N+1 retrospective packet.
- A product world-mutation check exists; dispatch/replay/caching exists; one-call transport is real.

### 5.2 What can be reused

- `S48Session` dispatch/replay/cache/pending-unknown semantics, with injected product transport.
- Prompt/envelope validation pattern, but envelope schema must be extended to `retrospective_text` + 3–5 prospects and postcall validation.
- `S48` source-owner refusal (`SOURCE_OWNER_HOLD`) as the correct absence behavior.
- `S48` self-account hold as a **starting** SCI05 state, but not as the complete admission system.

### 5.3 What must be replaced/created

- one prospective slot -> 3–5 `ConditionalProspect` batch;
- `narrative` only -> explicit `RetrospectivePacket` + proposed retrospective text + self-account;
- immediate SCI05 hold -> postcall `SCI05Admission` + dependency invalidation;
- exact event refs in model payload -> actor-accessible opaque memory refs;
- one call source -> current B/world source registry;
- no batch transaction -> per-event transaction/prefix receipt.

The current S48 path is not a sourcefree demonstration to extend by duplicating calls; it is a transport seam to reuse with a new contract.

---

## 6. Required discriminating cases

All six are **SPECIFICATION_ONLY** unless separately executed. The 116 sourcefree tests in the return do not execute these.

1. **E1→E2 semantic positive, qualified NO_CHANGE and missing-rule HOLD**
   - same actor, world and B;
   - E2 sees the C9/actor state derived from E1 via a concrete rule;
   - a lawfully evaluated no-change branch leaves semantic values identical;
   - a missing rule is `HELD_MISSING_RULE`, not no-change;
   - a severed E1-formation edge changes/removes the later semantic read.

2. **Event 2 source denied**
   - E2 source/owner absent or denied;
   - no E2 canonical event; no phantom E3–E5 under `PREFIX_CONTIGUOUS`;
   - committed prefix only; N+1 packet truthful; replay shows the gap.

3. **SCI05 first-half denied with dependent second-half proposals**
   - output proposes new insight plus events depending on it;
   - postcall SCI05 denies;
   - dependent proposals invalidated; unrelated proposal may be separately validated;
   - no self-account state write; no filler replacement.

4. **Render prose flip with fixed objective world/event**
   - change only V2/retrospective prose;
   - no C9/CAN011/actor state change;
   - failed Pass2/render cannot mark event applied+clean;
   - render failure leaves objective event committed with `render_failed`, no state rewrite.

5. **Same person/world, support changes**
   - external B/resource support changes while actor functional organization fixed;
   - distinguish resource intervention from earned psychological operation;
   - no inference that improved outcome proves learning.

6. **Independent B refusal / no default predicates**
   - no actual B source -> `SOURCE_OWNER_HOLD`/`B_CONTEXT_HOLD`;
   - controlled `PRIOR_B_REFUSAL` is labeled controlled, not actual;
   - no default `repair_urgent=True`/`avoid_debt=True` in the actual B source.

---

## 7. Exact acceptance conditions

The N/N+1 implementation is not accepted unless all of the following are actual consumer tests with owner-qualified sources:

1. 3–5 prospects are proposed, and the engine **actually resolves** them sequentially, not one-by-one through repeated LLM calls.
2. Each event reads the state after the previous committed event/interval; event 2 cannot use the pre-event state.
3. An event 2 source denial produces a truthful prefix and no phantom suffix.
4. N+1 retrospective packet is built only from actor-accessible realized prefix and contains no objective suffix IDs/count/order.
5. SCI05 denial invalidates only dependent proposals; independent proposals remain separately admissible.
6. A lawful no-change is distinguished from missing rule, source hold and render failure.
7. Replay produces the same event/state/memory identities without unseeded randomness or hidden model calls.
8. No renderer prose becomes actor state without an ADP016/017/SCI05/CAN owner transition.
