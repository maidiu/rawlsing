# ADP-021 — V3 Hybrid Causal Scheduler & Slow-Cadence Authority

**Assignment:** W1-05 — ADP-021 / V3 hybrid causal scheduler & slow-cadence authority  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w1-adp-021-v3-hybrid-scheduler`  
**Exact launch base:** `10a8e60f171e3a70bf48336fff73d37040cc1b93`  
**RA-R00 item:** `MUST-021`  
**Authority ID:** `V3_HYBRID_CAUSAL_SCHEDULER_POLICY`  
**Authority version:** `1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Mode:** authority creation only; no production code; no V3 implementation; no architecture reopening  
**Verdict:** `PASS`  
**CONSUMER_RELEASE_SUFFICIENCY:** `PARTIAL__MUST_021_CLOSED__V3_P4_REMAINS_DEPENDENCY_GATED`

## 0. Binding holding

V3 uses an **event-driven hybrid causal scheduler with explicit noncausal barriers**, not a universal timestep loop.

The scheduler coordinates six trigger classes:

1. `STATIC_CONTEXT_CHANGE_WAKE`;
2. `GENERATED_STATE_REQUERY`;
3. `PHASE_BOUNDARY_CANDIDATE`;
4. `DISCRETE_CAUSAL_EVENT`;
5. `SLOW_PROCESS_DUE`;
6. `DERIVED_PUBLICATION_REQUEST`.

Its default same-effective-time precedence, after satisfying explicit dependency edges, is:

```text
context requery barrier
→ phase-boundary evaluation
→ discrete causal event work
→ governed slow-process due work
→ pure derived recomputation/publication
```

This is a **coordination order**, not semantic ownership. A dependency edge from an accepted owning authority outranks class precedence. A generated event can therefore cause a phase candidate at the same effective time; the event runs first because the phase candidate depends on it. A causal rule can explicitly depend on a frozen derived receipt; that dependency likewise controls that pair.

The scheduler never creates semantic content merely because a queue is empty or a time boundary was reached. It may consume a trigger, invoke the exact owning rule, record a no-op receipt, jump directly to a later governed trigger, or become quiescent. It may not create filler biography.

Chronological time is an ordered coordinate supplied to V3. **No duration unit is made ontological by this authority.** A year is lawful only where another accepted semantic/update authority plus an explicit cadence binding requires a year-sized interval for that process.

`causal_cursor` advances only when V3 commits a causal event/state transition under its owning authority. Resolver refresh, trigger evaluation without transition, slow-process invocation with no causal mutation, derived recomputation/publication, checkpoints, queue housekeeping and serialization do not advance it.

---

## 1. Governing authority and evidence

This authority was created under:

- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`;
- `integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- RA-R00 `RESULT.md` / `RESULT.json`;
- accepted TD-R05 V3 developmental-runtime result;
- accepted TD-R07 whole-machine synthetic-life result;
- accepted SI-R05 V558→V3 seam hardening;
- accepted W0 ADP-008 `V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`;
- accepted W0 CAN-014 `V3_PURE_DERIVED_STATE_SCHEDULE@1.1.0`;
- W1 common law and W1-05 launch cell.

No sibling W1 result was consumed.

### 1.1 Required historical archive — direct verification

Required logical archive:

`Rawlsing_code_bundle_staging.zip`

Expected SHA256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

Directly computed SHA256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

**SHA verdict:** `EXACT_MATCH`  
**ZIP entries:** `13,138`

Recovered V3/V2/server material is continuity / authority-recovery evidence only. Historical V5/DDM material has **zero authority** over current V550+.

Directly inspected scheduler-relevant recovered files:

| Recovered path | SHA256 | Finding | Disposition |
|---|---|---|---|
| `v3/v3_yearly_step_order.yaml` | `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc` | hard-coded `timestep: year`; ordered mutation spine; derived schedule; event cap; explicit mutation prohibitions | preserve explicit ordering/invariant intent; reject yearly ontology |
| `v3/engine/step_runner.py` | `5a737c1704eaa6dc2c67f6c2db3118a6daa8a213b44d559bc37eadbc9c09d95a` | runs N compulsory yearly passes after initial derived recompute | continuity evidence only |
| `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | mutates through one ordered annual pass, interleaves derived recompute, increments `year` and `age` after every pass | decompose causal, slow and derived clocks |
| `v3/engine/event_engine.py` | `b57e7ef4df5dabd996dc7de19c1c2c273ad90ee89d73570df1fd85674dd98ded` | deterministically pseudo-samples 0–N events inside annual buckets from mutable actor state | reject as event authority; event generation/admission belongs to owning V3 authorities |
| `v3/core/year_record.py` | `4bbd7518a6ec8bc8dd22758a2f9e876882253dfd59021a998a6d541b23e5cfc2` | stable content hashing / replay-friendly record normalization | preserve replay/accountability direction |
| `v3/tests/test_architecture_invariants.py` | `bb2baec1c57de169a2e1e05533b9721b4b05191403ff4993d61df17ac29d05fa` | ordered spine, render nonmutation, events not directly mutating selected domains/topology, stored-vs-derived discipline | preserve invariant intent, not annual clock |
| `server/generation/simulation.py` | `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1` | generation orchestration uses age/year bands and legacy runtime loop | cadence/use evidence only; not authority |

At the exact launch base there is no top-level current production `v3/` directory to canonicalize. The accepted current architecture and W0 authorities therefore govern; recovered runtime code is not silently promoted.

---

## 2. Jurisdiction

### 2.1 ADP-021 owns

ADP-021 owns exactly:

1. scheduler trigger-envelope identity and validation;
2. coordination among the six trigger classes;
3. same-effective-time default class precedence;
4. dependency-before-class-precedence law;
5. fail-closed handling of unresolved noncommuting same-time causal order;
6. monotone causal-time advancement;
7. causal-cursor versus scheduler-receipt-cursor separation;
8. context requery barrier scheduling and coalescing mechanics;
9. invocation timing for ADP-008 phase-boundary candidates without phase-semantic ownership;
10. invocation timing for separately governed slow processes;
11. the minimum binding contract every slow cadence must expose;
12. coordination with CAN-014 pure derived recomputation/publication;
13. same-time closure, progress, quiescence and cycle detection;
14. scheduler replay identity/provenance.

### 2.2 ADP-021 does not own

ADP-021 does **not** own:

- what any causal event means, whether it is admissible, or what effects it has;
- stochastic candidate generation/selection or RNG streams (`ADP-020` where applicable);
- actor initialization;
- generated position/mobility semantics;
- encounter/opportunity/exposure semantics;
- relationship/household/genealogy semantics;
- developmental phase identity, boundary predicates or transition semantics (`ADP-008`);
- ContextResolver semantic selection/proxy/predicate law;
- which generated fields are resolver-relevant; that comes from the accepted resolver/binding contract;
- slow-process update formulas, thresholds, state variables or substantive meaning;
- an annual/default slow cadence;
- semantic existence/formula/dependency graph of a derived output;
- CAN-014 evaluator order inside pure-derived recomputation;
- V2 render/session scheduling;
- checkpoints as causal events;
- filler events or biography.

The scheduler invokes authority; it never becomes a substitute authority.

---

## 3. Canonical scheduler trigger envelope

Every scheduled item is represented by a record terminally equivalent to:

```text
V3SchedulerTrigger {
    trigger_id,
    trigger_class,
    actor_or_entity_scope_ref,
    effective_time,
    source_authority_id,
    source_authority_version,
    source_authority_content_hash,
    semantic_payload_ref,
    dependency_trigger_refs[],
    causal_parent_refs[],
    same_time_order_constraints[],
    source_receipt_refs[],
    provenance_refs[],
    trigger_content_hash
}
```

Requirements:

- `trigger_id` is stable and content/provenance bound;
- `effective_time` uses the actor/runtime's exact versioned causal-time basis;
- the scheduler may not infer missing `effective_time`, owner, dependency or semantic payload;
- queue insertion order, arrival order, thread order, filesystem order, source-code order, dictionary order and lexical ID order never become semantic precedence;
- exact duplicate trigger identities deduplicate without a second invocation;
- nonidentical triggers never deduplicate merely because their labels/times match.

`same_time_order_constraints` may cite only constraints supplied by an accepted owning authority or this ADP-021 class-precedence law. The scheduler may not invent a domain-specific priority score.

---

## 4. Six trigger classes

### 4.1 `STATIC_CONTEXT_CHANGE_WAKE`

Source: deterministic ContextResolver `next_context_change` metadata from a fixed immutable repository/query/policy state.

Meaning: “the currently bound structural context must be re-resolved at this effective time.”

It is **not** a causal event and does not advance the causal cursor.

No polling tick is authorized. If V558 can expose no next structural boundary, ADP-021 schedules none.

### 4.2 `GENERATED_STATE_REQUERY`

Source: a committed V3 generated runtime fact/state change whose accepted resolver/binding contract says it changes the query binding fingerprint.

Examples remain owner-defined; SI-R05 establishes the family includes generated location, position, relationship, household/family, genealogy subject and governed phase inputs where relevant.

Meaning: “re-resolve the same immutable repository using the new caller/V3-owned generated-binding fingerprint.”

It is a noncausal scheduler barrier caused by prior causal history. It never transfers actor-fact ownership to V558.

### 4.3 `PHASE_BOUNDARY_CANDIDATE`

Source: `ADP-008` only.

Canonical source shape: `V3PhaseBoundaryTriggerCandidate` or terminal equivalent carrying actor ID, phase-rule/version, transition definition, trigger time, basis hash and provenance.

The scheduler invokes ADP-008 evaluation at the candidate time. The candidate itself is not a phase transition. If ADP-008 commits a phase transition/state change, that committed transition is causal V3 state and is cursor-bearing according to the phase authority/runtime event law. If evaluation yields no transition, no filler event is created.

Event/fact-based phase rules that do not expose a deterministic future time generate no guessed scheduler boundary; they are reevaluated when their declared input event/fact arrives.

### 4.4 `DISCRETE_CAUSAL_EVENT`

Source: an exact accepted V3 generation/admission authority.

This class covers an already-generated/admitted event or causal transition candidate with a lawful effective time and semantic owner. ADP-021 neither generates the event nor chooses among stochastic candidates.

A committed event/transition advances the causal cursor exactly once. A rejected/deferred candidate does not.

### 4.5 `SLOW_PROCESS_DUE`

Source: a valid `V3SlowCadenceBinding` under §8.

Meaning: the separately governed process update authority is due to be invoked.

“Due” is not itself a causal event. If the owning process rule produces no causal state mutation, no event is fabricated. If it produces a lawful mutation/event, that owner supplies the causal record and the cursor advances once per committed causal record.

### 4.6 `DERIVED_PUBLICATION_REQUEST`

Source: V3 runtime/consumer request governed by CAN-014.

Meaning: perform the requested CAN-014 pure derived recomputation/publication against the exact frozen stored-state identity named by the request after dependency/precedence obligations are satisfied.

The request, evaluation and publication are noncausal. They never advance causal time/cursor or manufacture history.

---

## 5. Same-time precedence and tie law

### 5.1 First law: explicit dependency outranks class rank

At one `effective_time`, construct the dependency DAG over ready triggers.

An explicit dependency from accepted authority always runs before the dependent trigger, even if default class rank would otherwise place the dependent class earlier.

A dependency cycle is `SCHEDULER_DEPENDENCY_CYCLE` and fails closed. No edge is dropped heuristically.

### 5.2 Default class precedence among dependency-ready peers

For triggers at the same effective time with no unsatisfied dependency edge between them:

```text
P0  STATIC_CONTEXT_CHANGE_WAKE
    GENERATED_STATE_REQUERY

P1  PHASE_BOUNDARY_CANDIDATE

P2  DISCRETE_CAUSAL_EVENT

P3  SLOW_PROCESS_DUE

P4  DERIVED_PUBLICATION_REQUEST
```

Rationale:

- P0 makes the current structural context coherent before a context-consuming rule acts;
- P1 makes a deterministically due governed phase state available before unrelated lower-priority same-time work;
- P2 preserves discrete lived history before maintenance/integration;
- P3 integrates only after higher-priority same-time history known to the scheduler has been committed;
- P4 defaults to the stabilized causal state rather than an incidental intermediate state.

A causal parent may reverse this apparent class order locally. Example: event `E` at `T` produces an event-based phase candidate `P`; `P` depends on `E`, so `E → P` despite P1 preceding P2 by default.

### 5.3 P0 coalescing

If static-boundary and generated-binding requery triggers target the same actor/query scope at the same effective time, one resolver call may satisfy them **only when** it uses:

- the same immutable repository bundle/policy identity;
- the newest already-committed binding fingerprint valid for that point;
- one normalized `ContextQuery`.

The resolver receipt records every coalesced trigger/reason. Coalescing may reduce duplicate read-only work but cannot erase provenance.

Different query scopes remain distinct. Canonical processing order among independent read-only P0 queries is serialization only and has no semantic meaning.

### 5.4 Within-class causal ties

For two nonidentical same-time causal triggers in the same precedence class:

1. obey explicit causal/dependency/order constraints from their owning authorities;
2. exact duplicates may deduplicate;
3. peers may be canonically serialized by stable ID **only if** their owning contracts establish that the operations are semantically order-independent/commutative;
4. if operations can produce different causal outcomes under different order and no accepted authority orders them, return `AMBIGUOUS_SAME_TIME_CAUSAL_ORDER` and do not choose a lexical/arrival-order winner.

A convenient deterministic total order is forbidden when it would silently become causal semantics.

### 5.5 Re-open after causal commit

After **every** committed causal mutation at time `T`, before the next context-consuming causal rule at `T`:

- enqueue/consume any generated-state requery required by the resolver binding contract;
- enqueue any newly lawful ADP-008 event/fact-triggered candidate;
- enqueue any other explicit downstream trigger created by accepted owners;
- restart same-time precedence selection from the highest dependency-ready class.

This is a barriered microcycle, not one fixed once-per-tick pipeline.

---

## 6. Causal time and cursor law

Canonical logical state is terminally equivalent to:

```text
V3SchedulerCursor {
    actor_or_runtime_scope_id,
    time_basis_id,
    time_basis_version,
    current_effective_time,
    causal_event_sequence,
    last_causal_event_hash,
    scheduler_receipt_sequence,
    consumed_trigger_set_hash,
    scheduler_policy_id,
    scheduler_policy_version,
    cursor_hash
}
```

Rules:

1. `effective_time` is monotone; ADP-021 defines no universal seconds/days/months/years unit.
2. If pending work exists at current time, same-time closure runs before advancing time.
3. Otherwise jump directly to the minimum later effective time among lawfully scheduled triggers.
4. Empty intervals produce no synthetic ticks/events.
5. A new trigger earlier than `current_effective_time` is `SCHEDULER_RETROGRADE_TRIGGER` unless it is an exact already-consumed replay duplicate.
6. `causal_event_sequence` advances only on a committed causal event/state-transition record.
7. `scheduler_receipt_sequence` may advance for noncausal refresh/evaluation/derived/no-op work; it is audit order, not actor history.
8. A checkpoint may snapshot cursor/state but cannot advance causal truth.
9. Caller-supplied run horizons may stop execution, but a horizon is an execution request, not ontology.

No wall clock participates in simulation effective time.

---

## 7. Resolver-requery law

ADP-021 binds SI-R05's two channels mechanically without acquiring resolver semantics.

### 7.1 Channel A — static

When the current resolver receipt exposes a lawful future `next_context_change`, create one `STATIC_CONTEXT_CHANGE_WAKE` for that exact boundary and receipt identity.

After refresh, replace only the **current prospective context binding** and schedule the newly returned next boundary if any.

### 7.2 Channel B — generated state

After a committed generated-runtime fact changes the accepted query-binding fingerprint, create `GENERATED_STATE_REQUERY` at the same effective time with a dependency on the causal record that caused the change.

Requery uses the **same immutable repository bundle** unless an explicitly selected new immutable bundle is separately supplied by governing runtime policy.

### 7.3 Prospective-only effect

A refreshed `ResolvedStructuralContext`:

- may govern later evaluations/events at or after its effective binding point;
- may not re-adjudicate, mutate, delete, relabel or rehash an already committed causal event;
- may not convert earlier structural availability into earlier lived exposure;
- may not rewrite an earlier resolver receipt.

Late evidence or a newly selected immutable repository version requires explicit replay/migration if historical recomputation is desired. Live refresh is never silent retroactive rewrite.

### 7.4 Requery progress

A resolver refresh must terminate in one of:

- a new context/binding identity;
- a lawful unchanged context with the triggering reason consumed;
- explicit fail-closed state.

A returned next boundary `<= current_effective_time` that would recreate the same unconsumed trigger identity is `SCHEDULER_NONPROGRESSING_CONTEXT_BOUNDARY`. No spin/poll loop is authorized.

---

## 8. Slow-cadence binding contract

No process is “slow” merely because recovered code updated it annually.

Every slow process scheduled by ADP-021 must present a machine record terminally equivalent to:

```text
V3SlowCadenceBinding {
    slow_process_id,
    actor_or_entity_scope_ref,

    process_semantic_authority_id,
    process_semantic_authority_version,
    process_semantic_authority_content_hash,

    cadence_authority_id,
    cadence_authority_version,
    cadence_authority_content_hash,

    cadence_binding_id,
    cadence_binding_version,
    time_basis_id,
    current_due_time,
    next_due_evaluator_ref,
    reschedule_policy_ref,
    same_time_order_constraints[],
    binding_input_hash,
    provenance_refs[],
    cadence_binding_hash
}
```

Binding law:

1. `process_semantic_authority_*` owns **what** is read/updated and what a no-op/change means.
2. `cadence_authority_*` owns **when** that process is due, initial due semantics, rescheduling and any catch-up/coalescing rule.
3. These may physically share an authority only if that accepted authority explicitly owns both semantics and cadence. The fields remain logically distinguishable.
4. ADP-021 owns only validation, queuing, invocation and coordination.
5. Missing process authority or missing cadence authority => `SLOW_PROCESS_UNGOVERNED`; do not run.
6. The historical yearly loop is never a fallback cadence.
7. After a due trigger is consumed, cadence authority must yield a strictly later due time, an explicit finite distinct same-time subtrigger/dependency, or an exhausted/condition-waiting state. Recreating the same due identity at the same time is nonprogress.
8. A missed interval never implies N synthetic catch-up ticks unless the cadence authority explicitly requires that behavior.
9. A no-op slow evaluation creates a scheduler receipt only; no pseudo-event.
10. Slow processes with unresolved relative ordering follow §5.4; scheduler ID order cannot decide noncommuting state semantics.

Authority `1.0.0` defines **zero universal slow-process cadence values**. In particular:

```text
DEFAULT_SLOW_CADENCE = NONE
ANNUAL_SLOW_CADENCE = NOT_AUTHORIZED_BY_ADP_021
```

A future accepted process authority may lawfully bind annual cadence for its own process; that would not make “year” a V3 ontology.

---

## 9. CAN-014 interaction

The constitutional separation remains:

```text
V3 causal scheduler / slow cadence
!=
V3 pure derived-state schedule
!=
V2 render/session scheduling
```

ADP-021 decides **when a CAN-014 request becomes dependency-ready in the causal event loop**. CAN-014 decides:

- which independently authorized outputs are registered;
- pure evaluator/dependency ordering;
- frozen stored-state input identity;
- full/incremental recomputation semantics;
- field freshness/provenance;
- derived publication integrity.

ADP-021 may not inspect recovered derived names and schedule them as ontology.

### 9.1 Default placement

Absent an explicit dependency requiring otherwise, a pending `DERIVED_PUBLICATION_REQUEST` runs after same-time causal/phase/slow work has stabilized.

Its `StoredStateRef` is the exact frozen state selected by the request at execution. If prior same-time causal mutation made an earlier derived request/state ref stale, the runtime must either regenerate/rebind the request under its governing consumer policy or return CAN-014's stale/integrity result; the scheduler cannot silently substitute a newer state ref.

### 9.2 Derived-to-causal use

CAN-014 publication never creates causal work by itself.

If a separately governed causal rule consumes a derived result, that rule must explicitly emit/present a new causal trigger with an exact dependency on the derived receipt/state identity. ADP-021 schedules that supplied trigger normally. It does not infer causal significance from a changed derived value.

### 9.3 Valid-empty registry

CAN-014's current `VALID_EMPTY_DERIVED_OUTPUT_REGISTRY` is a complete lawful state. A derived request may therefore produce an empty derived view. ADP-021 creates no placeholder output/event to make the cycle “productive.”

---

## 10. Phase-boundary interaction

ADP-008 remains semantic owner.

ADP-021 may:

- queue exact future `V3PhaseBoundaryTriggerCandidate`s published by ADP-008;
- invoke ADP-008 at their effective times;
- order their invocation against other trigger classes;
- record scheduler receipts;
- schedule required context requery after a committed phase change where the resolver contract marks phase as query-relevant.

ADP-021 may not:

- invent a human-development segment;
- infer a phase from age;
- create a future boundary for event-based phase rules;
- mutate phase directly because a boundary time arrived;
- choose among ambiguous phase transitions inside ADP-008 semantics;
- retroactively reclassify prior history.

A boundary candidate with no committed ADP-008 transition remains noncausal.

---

## 11. Replay identity

Exact scheduler replay requires, at minimum:

- immutable structural repository bundle ID/content hash;
- resolver policy/version and exact context/SelectionRecord receipts consumed;
- scheduler authority ID/version/content hash;
- time-basis ID/version;
- initial scheduler cursor/hash;
- all trigger envelopes and trigger hashes;
- all dependency/order constraints and their owning authority refs;
- all committed causal event/transition IDs/hashes and parent refs;
- all generated-binding fingerprints and requery receipts;
- ADP-008 authority/registry/rule/candidate/evaluation/transition identities where used;
- every slow-process semantic authority and cadence-binding identity/hash;
- CAN-014 schedule/registry/evaluator/state refs for every derived request/publication;
- named causal RNG provenance from ADP-020 where a separate event-generating authority uses randomness;
- admitted external events/artifacts where applicable;
- checkpoints only as verified caches/snapshots.

Replay with the same immutable authorities/inputs/triggers must reproduce:

- the same trigger consumption order;
- the same scheduler receipts;
- the same causal event sequence and parentage;
- the same causal cursor/checkpoint hashes;
- the same requery/context identities;
- the same derived publication identities for the same requested state refs.

Hidden ambient state is an integrity failure.

---

## 12. Progress, closure and termination

For each scheduler iteration, at least one of these must become true:

1. a previously unconsumed trigger identity is consumed;
2. at least one new causal record is committed and `causal_event_sequence` advances;
3. effective time advances strictly to the next later governed trigger;
4. execution enters an explicit terminal/quiescent/blocked state.

A consumed trigger cannot be reintroduced under the same identity.

Same-time closure continues while dependency-ready triggers remain at `current_effective_time`. Every newly emitted same-time trigger must have distinct lineage/identity or be an exact duplicate. Dependency cycles, repeated same-time identical self-rescheduling, and resolver boundaries that recreate themselves without new state fail closed rather than being hidden behind an arbitrary numeric iteration cap.

Canonical loop outcomes include:

- `QUIESCENT_NO_PENDING_TRIGGER`;
- `TARGET_HORIZON_REACHED`;
- `BLOCKED_MISSING_AUTHORITY`;
- `AMBIGUOUS_SAME_TIME_CAUSAL_ORDER`;
- `SCHEDULER_DEPENDENCY_CYCLE`;
- `SCHEDULER_RETROGRADE_TRIGGER`;
- `SCHEDULER_NONPROGRESSING_TRIGGER`;
- `SCHEDULER_NONPROGRESSING_CONTEXT_BOUNDARY`;
- `SCHEDULER_INTEGRITY_FAILURE`.

Quiescence is valid. It does not require a filler event or timestep.

An open runtime may later receive a separately admitted external trigger and resume from the exact cursor. That is not background wall-clock progression.

---

## 13. Failure / unknown / negative behavior

| Condition | Required behavior |
|---|---|
| no triggers now or in known future | `QUIESCENT_NO_PENDING_TRIGGER`; no filler |
| slow process lacks cadence authority | `SLOW_PROCESS_UNGOVERNED`; do not invoke |
| slow cadence exists but semantic update authority missing | `SLOW_PROCESS_UNGOVERNED`; do not invoke |
| same-time noncommuting causal peers lack order | `AMBIGUOUS_SAME_TIME_CAUSAL_ORDER`; fail closed |
| dependency cycle | `SCHEDULER_DEPENDENCY_CYCLE`; fail closed |
| trigger effective time goes backward | `SCHEDULER_RETROGRADE_TRIGGER`; fail closed |
| context boundary recreates identical due trigger | `SCHEDULER_NONPROGRESSING_CONTEXT_BOUNDARY`; fail closed |
| phase candidate absent | no phase scheduler trigger |
| ADP-008 candidate evaluates no transition | consume candidate; no causal event |
| derived registry valid-empty | lawful empty derived publication |
| derived evaluator attempts causal mutation | CAN-014 integrity failure; causal cursor unchanged |
| current context changes | prospective replacement only; history immutable |
| hidden wall clock / filesystem / mutable-latest dependency detected | `SCHEDULER_INTEGRITY_FAILURE` |
| scheduler asked to invent semantic event/cadence/rule | `BLOCKED_MISSING_AUTHORITY` |

---

## 14. Hostile fixture court

| Fixture | Hostile input | Required verdict |
|---|---|---|
| `ADP021-H01` | recovered annual loop offered as universal clock | reject; annual cadence not authorized |
| `ADP021-H02` | five years with no governed trigger | jump over interval / quiesce; zero filler events |
| `ADP021-H03` | two same-time noncommuting causal events, no dependency/priority authority | `AMBIGUOUS_SAME_TIME_CAUSAL_ORDER` |
| `ADP021-H04` | same events inserted in reversed queue/filesystem order | identical lawful result or same ambiguity; no race-order semantics |
| `ADP021-H05` | static context boundary and unrelated discrete event at same T | refresh barrier first; admitted event identity/history not rewritten |
| `ADP021-H06` | generated move/position commit changes query fingerprint | same-time dependent requery before next context-consuming causal rule |
| `ADP021-H07` | requery yields same context but trigger reason is consumed | lawful no-change receipt; no spin |
| `ADP021-H08` | resolver returns identical next boundary at `<= T` repeatedly | `SCHEDULER_NONPROGRESSING_CONTEXT_BOUNDARY` |
| `ADP021-H09` | ADP-008 time-bound candidate at T | invoke ADP-008; scheduler cannot mutate phase itself |
| `ADP021-H10` | event-based phase rule has no future time | schedule no guessed boundary |
| `ADP021-H11` | event E at T causes phase candidate P at T | explicit `E → P` dependency outranks default P1/P2 class order |
| `ADP021-H12` | slow process exists with no governed cadence | `SLOW_PROCESS_UNGOVERNED`; no yearly fallback |
| `ADP021-H13` | slow due evaluates to no change | receipt only; no event |
| `ADP021-H14` | cadence self-reschedules identical due identity at T | `SCHEDULER_NONPROGRESSING_TRIGGER` |
| `ADP021-H15` | long gap crosses many nominal periods but catch-up law absent | no synthetic catch-up ticks |
| `ADP021-H16` | CAN-014 request during same-time causal work with no explicit dependency | execute after causal stabilization |
| `ADP021-H17` | CAN-014 evaluator mutates causal state/cursor | reject under CAN-014; cursor unchanged |
| `ADP021-H18` | CAN-014 registry valid-empty | empty derived view; no placeholder |
| `ADP021-H19` | derived output changes and scheduler infers a causal event | forbidden; causal owner must explicitly emit trigger |
| `ADP021-H20` | late context refresh attempts to rewrite earlier event provenance | reject; prospective-only |
| `ADP021-H21` | static and generated requery target same query at same T | coalesce only with same bundle/policy and current committed binding fingerprint; record both reasons |
| `ADP021-H22` | trigger is earlier than current causal time | `SCHEDULER_RETROGRADE_TRIGGER` |
| `ADP021-H23` | explicit causal dependency cycle | fail closed; never break by ID order |
| `ADP021-H24` | hidden wall clock / mutable `latest` / thread-arrival order changes result | `SCHEDULER_INTEGRITY_FAILURE` |

---

## 15. Consumer contract

Primary consumer:

- `V3-P4` hybrid scheduler/context/requery integration.

ADP-021 is sufficient to close `MUST-021` itself. It does **not** release V3-P4 by itself.

RA-R00 separately gates V3-P4 on the standalone V558 repository/resolver and other accepted authority/canonicalization items, including generated-position/requery/randomness dependencies. This authority does not consume or prejudge sibling W1 results and does not convert those external blockers into ADP-021 semantics.

```text
CONSUMER_RELEASE_SUFFICIENCY =
PARTIAL__MUST_021_CLOSED__V3_P4_REMAINS_DEPENDENCY_GATED
```

---

## 16. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

### Genuine ambiguity

After hard architecture and the two accepted direct dependencies were satisfied, more than one lawful scheduling shape remained:

1. retain a clean coarse universal timestep and fit events/refresh/slow updates inside it;
2. use a globally total deterministic same-time ID order for convenience;
3. use a hybrid event-driven scheduler that jumps between actual governed triggers, treats context/derived work as noncausal barriers, requires separately governed slow cadence, and fails closed when noncommuting same-time causation lacks semantic order.

### Choice

Authority `1.0.0` chooses option 3.

The recovered annual spine is preserved only as evidence that explicit ordering, slow integration and replay matter. It is not promoted into a universal human clock. Stable IDs can stabilize serialization only after semantic order-independence exists; they cannot manufacture causal precedence. Empty stretches remain empty. Generated events can create later same-time consequences through explicit dependency, so path-dependent divergence survives rather than being flattened into a predetermined tick pipeline.

### Tie-break principles applied

- historical causality without inevitability;
- agency as situated divergence whose consequences become later causes;
- dynamic history over static classification/timestep convenience;
- causal provenance/replay without reductive total explanation;
- enough generative openness for divergent lives under the same structural field;
- minimum sufficient machinery without duplicated semantic ownership;
- lawful absence rather than fabricated content.

No Governing-Spirit principle was used to invent a semantic event, phase, cadence, RNG rule or derived output.

---

## 17. Final authority statement

### THIS AUTHORITY IS RESPONSIBLE FOR

Deterministic/replayable temporal coordination of exact V3 causal triggers, ContextResolver refresh barriers, ADP-008 phase candidates, separately governed slow-process due work and CAN-014 pure-derived requests; causal time/cursor discipline; same-time precedence/ambiguity law; progress/quiescence; scheduler provenance.

### THIS AUTHORITY IS NOT RESPONSIBLE FOR

The semantic content of any invoked rule, causal RNG, phase meaning, resolver semantics, generated positions/encounters/relationships, slow update formulas, derived-output meaning/evaluator semantics, V2 scheduling, or a universal annual ontology.

### TERMINAL NONCOLLAPSE

```text
scheduler trigger
!= causal event
!= resolver context
!= phase semantic rule
!= slow-process semantic update
!= pure derived publication

causal time
!= recovered annual timestep

deterministic serialization
!= semantic precedence

context refresh
!= retroactive history rewrite
```

**Final token:** `ADP_021_V3_HYBRID_SCHEDULER_AUTHORITY = PASS`
