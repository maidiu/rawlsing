# CAN-007 — Static Next-Context-Change vs Generated-Life Requery Canonicalization

**Assignment:** W2-B02-03  
**RA-R00 item:** `CAN-007`  
**Canonical authority:** `V558_V3_CONTEXT_REFRESH_REQUERY_CONTRACT`  
**Authority version:** `1.0.0`  
**Static metadata schema:** `V558_STATIC_NEXT_CONTEXT_CHANGE_METADATA@1.0.0`  
**Generated trigger schema:** `V3_GENERATED_LIFE_REQUERY_TRIGGER@1.0.0`  
**Replay receipt schema:** `V558_CONTEXT_REFRESH_REPLAY_RECEIPT@1.0.0`  
**Owner:** `V558_CONTEXTRESOLVER__V3_SCHEDULER_REFRESH_SEAM`  
**Exact launch base:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**Mode:** bounded authority canonicalization only  
**Historical ZIP:** `NOT_AUTHORIZED_NOT_USED`  
**Verdict:** `PASS`

## 1. Binding holding

CAN-007 canonicalizes the already-accepted **two-channel context-refresh contract** at the V558→V3 seam.

```text
CHANNEL A — REPOSITORY-STATIC
fixed immutable repository
+ fixed resolver policy
+ current ContextQuery / generated-binding fingerprint
→ deterministic next_context_change metadata
→ STATIC_CONTEXT_CHANGE_WAKE when an exact future structural boundary exists

CHANNEL B — GENERATED-LIFE
committed V3 generated fact/state transition
+ exact declaration that the changed fact participates in the current query
+ changed generated-binding fingerprint
→ GENERATED_STATE_REQUERY
→ fresh ContextQuery against the SAME immutable repository
```

The constitutional noncollapse is:

```text
STATIC NEXT_CONTEXT_CHANGE
!= ACTOR EVENT PREDICTION
!= GENERATED-LIFE REQUERY
!= POLLING CADENCE
!= ANNUAL TIMESTEP
!= CAUSAL EVENT

GENERATED V3 EVENT
!= QUERY-RELEVANT GENERATED CHANGE

REQUERY
!= REPOSITORY MUTATION
!= ACTOR-FACT CREATION
!= PRIOR-HISTORY REWRITE
```

V558 may predict only a deterministic boundary already derivable from the immutable published structural repository, the bound resolver policy, and the exact current query. It may not predict a migration, new position, relationship, household, genealogy event, developmental transition, or any other actor event.

V3 separately owns generated-life causality. A committed generated change triggers Channel B only when an accepted contract declares the changed binding/state relevant to the current `ContextQuery`. CAN-006 generated-position binding changes are the currently accepted concrete example.

A static wake can never substitute for an already-required generated-life requery. A generated-life requery can occur before, after, or at the same effective time as a static wake. Both are noncausal resolution barriers and do not themselves advance the V3 causal cursor.

## 2. Governing law and evidence

No historical ZIP was authorized or used.

Directly inspected at exact base `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`:

- W2 Batch-02 launch register, common law and W2-B02-03;
- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`;
- whole-machine architecture closure;
- implementation-release synthesis;
- W0 and W1 closure rulings;
- W2 first-batch adjudication;
- V557/V558 completion ruling;
- V3 completion ruling;
- RA-R00 release-synthesis result;
- TD-R04 V557/V558 terminal-demand result;
- SI-R05 V558→V3 hostile seam result, especially H2 two-channel refresh;
- accepted CAN-006 generated-position binding authority;
- accepted ADP-008 developmental-phase authority;
- accepted ADP-009 position/mobility authority;
- accepted ADP-021 hybrid scheduler authority;
- current `data/ddm_build_copy/ddm_v558_runtime_input_gate.py`;
- current `data/ddm_build_copy/ddm_v558_plus_governance.py`.

No same-Batch-02 W2 result was consumed.

Binding authority already establishes:

1. `ContextResolver` is deterministic, read-only and stage-blind.
2. `StructuralPriorRepository` is immutable per bundle.
3. `next_context_change` is deterministic refresh metadata, not an actor-life scheduler.
4. SI-R05 H2 requires repository-predictable refresh and caller/V3 generated-binding invalidation as distinct channels.
5. ADP-021 already owns scheduler trigger classes `STATIC_CONTEXT_CHANGE_WAKE` and `GENERATED_STATE_REQUERY`, with no polling and no universal timestep.
6. CAN-006 already owns exact generated-position transport and reuses query purpose `STRUCTURAL_CONTEXT_REFRESH`.
7. ADP-009 already requires re-resolution after a bindable committed position/location change.
8. ADP-008 phase identity is separate from resolver Phase A/B and is query-relevant only where an exact query/predicate actually declares it.
9. Current V558 gate/governance code is superseded implementation terrain. Its fail-closed/hash/audit discipline may be retained operationally, but its wall-clock audit timestamps and readiness machinery are not refresh semantics.

## 3. Jurisdiction

### 3.1 CAN-007 owns

CAN-007 owns exactly:

1. the two refresh-channel meanings and noncollapse;
2. deterministic Channel-A metadata identity;
3. Channel-B generated-life invalidation trigger identity;
4. query-relevance declaration/fingerprint binding;
5. exact `STRUCTURAL_CONTEXT_REFRESH` query-purpose use;
6. prior context/query/repository/policy lineage required for refresh;
7. changed-binding/state references for Channel B;
8. effective causal/query time binding;
9. ADP-021 scheduler handoff for both channels;
10. exact-trigger deduplication;
11. exact-equivalent cross-trigger coalescence;
12. stale/superseded wake handling;
13. refresh request/result/replay receipts;
14. valid-empty, no-change, unknown, missing, deferred and integrity behavior;
15. prohibition on polling, annual cadence, geography→position inference, repository mutation and historical rewrite.

### 3.2 CAN-007 does not own

CAN-007 does **not** own:

- producer structural semantics or V553 temporal evidence;
- temporal-proxy eligibility;
- immutable repository construction or repository-version selection;
- ContextResolver selection/predicate semantics;
- generated position semantics or mobility;
- relationship/household/genealogy semantics;
- developmental-phase semantics;
- which domain facts exist in V3;
- whether a V3 causal event is admitted or what it means;
- scheduler precedence beyond consuming accepted ADP-021;
- causal RNG;
- V3 causal cursor semantics;
- actor knowledge, memory, response, attractor or V2 expression;
- a polling frequency, annual clock, fallback timer or wall-clock wake;
- a universal inventory saying every generated fact is query-relevant.

A neighboring semantic owner may declare that one of its generated facts changes an exact query binding. CAN-007 validates and transports the resulting refresh reason; it does not create the neighboring fact or its semantics.

### 3.3 Exact consumers

RA-R00 consumers are:

- `V558-P4` — `ResolvedStructuralContext`, SelectionRecords, fidelity and two-channel refresh;
- `V3-P4` — hybrid scheduler / context / requery integration.

CAN-007 closes only its named semantic blocker. It does not globally release either packet.

## 4. Query-purpose and generated-binding fingerprint contract

### 4.1 Refresh query purpose

Both channels use the accepted CAN-006 query purpose:

`STRUCTURAL_CONTEXT_REFRESH`

The reason/channel is carried separately in the refresh trigger/receipt.

CAN-007 does **not** create separate semantic query purposes such as `STATIC_REFRESH` and `LIFE_REFRESH`. This is deliberate: when both reasons are exactly equivalent at one effective time, one normalized `ContextQuery` may lawfully satisfy both while preserving both trigger lineages.

Other already-governed query purposes remain separate:

- `STRUCTURAL_CONTEXT_PHASE_A`;
- `STRUCTURAL_CONTEXT_PHASE_B`;
- `REPLAY_AUDIT_EXPLANATION`.

### 4.2 `GeneratedQueryBindingFingerprint`

Channel B compares only generated facts/state that the current query has explicitly declared query-relevant.

A semantic equivalent is:

```text
GeneratedQueryBindingFingerprint {
  generation_subject_ref,
  actor_id_or_null,
  query_scope_id,
  entries[] {
    binding_key_ref,
    query_relevance_basis_ref,
    source_authority_id,
    source_authority_version,
    source_authority_hash,
    generated_fact_or_state_ref,
    generated_fact_or_state_hash,
    effective_from,
    currentness_or_view_ref,
    currentness_or_view_hash,
    binding_or_transport_ref,
    binding_or_transport_hash,
    epistemic_class = GENERATED_RUNTIME_FACT_REF
  },
  fingerprint_hash
}
```

Rules:

- entries are included only when the active query/predicate contract declares that exact binding/state relevant;
- query time itself is excluded from this fingerprint, so mere passage of time cannot masquerade as a generated-life change;
- exact duplicate entries may canonicalize for serialization;
- order never creates semantic precedence;
- missing/unknown generated state is represented by its governed state, never filled by geography, prevalence or a default;
- a changed generated fact that is not in the declared query-relevance set does not require Channel B.

Currently accepted concrete binding:

- CAN-006 `V3_GENERATED_POSITION_BINDING` / binding-set change.

Other generated state—relationship, household/family, location, development phase or other facts—may participate only when an accepted owner/interface and the active query explicitly bind them. The closed architecture identifies those families as possible query inputs; CAN-007 does not make every instance globally relevant.

## 5. Channel A — repository-static next-context-change

### 5.1 Meaning

Channel A answers:

> Given this fixed immutable repository, fixed resolver policy, exact prior query/context and current generated-binding fingerprint, what is the earliest future effective time already knowable from those materials at which static structural resolution **could** change?

It is not a prediction that the resolved context will necessarily change.

### 5.2 Lawful boundary sources

Only exact deterministic boundaries derivable from the fixed repository/query/policy are lawful, including where governed:

- V553 support/observation/relation/limit boundaries;
- producer-owned temporal applicability boundaries;
- deterministic resolver/proxy-selection boundaries already authorized by the bound policy;
- other exact producer-governed structural boundaries represented in the fixed bundle.

A future publication, a not-yet-selected repository bundle, a policy amendment, or an actor event is not something Channel A predicts.

A separately accepted new repository or resolver policy starts a new resolution episode; CAN-007 does not forecast when such external publication/selection will occur.

### 5.3 `V558StaticNextContextChangeMetadata`

```text
V558StaticNextContextChangeMetadata {
  metadata_id,
  schema_version,

  generation_subject_ref,
  actor_id_or_null,
  query_scope_id,

  repository_bundle_id,
  repository_content_hash,
  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  source_context_ref,
  source_context_hash,
  source_query_ref,
  source_query_hash,
  source_query_time,
  source_query_time_granularity,
  generated_query_binding_fingerprint,

  status,
  next_context_change_time_or_null,
  next_context_change_granularity_or_null,
  boundary_basis_refs_and_hashes[],
  static_basis_hash,

  provenance_refs[],
  metadata_hash
}
```

Identity is content-addressed from semantic fields. Wall clock, process time, filesystem order, mutable `latest`, random values, model output and container iteration are forbidden identity inputs.

### 5.4 Earliest-boundary / tie law

If multiple lawful static boundaries exist, Channel A reports the earliest future boundary in the query's governed temporal basis.

If several exact bases share that earliest time, retain **all** of their basis refs/hashes. Lexical ordering may stabilize serialization only and cannot choose a semantic winner.

### 5.5 No-known-boundary law

If no exact future static boundary is derivable:

`STATIC_NEXT_CHANGE_NONE_KNOWN`

with:

```text
next_context_change_time_or_null = null
```

ADP-021 schedules no static wake.

This is not permission to poll later. No day/week/month/year fallback exists.

If the next boundary is factually unknown:

`STATIC_NEXT_CHANGE_UNKNOWN`

If authority required to derive it is missing:

`STATIC_NEXT_CHANGE_DEFERRED_MISSING_AUTHORITY`

Neither state authorizes an invented timestamp.

### 5.6 Scheduler handoff

A positive Channel-A metadata record may produce the accepted ADP-021 envelope:

```text
trigger_class = STATIC_CONTEXT_CHANGE_WAKE
effective_time = next_context_change_time
semantic_payload_ref = V558StaticNextContextChangeMetadata
```

The wake is noncausal and does not advance the causal cursor.

## 6. Channel B — V3 generated-life requery

### 6.1 Admission predicate

A Channel-B requery is required only when all are true:

1. an accepted V3 authority has committed an exact generated fact/state transition;
2. the transition has an exact effective causal time;
3. the active `ContextQuery` declares the changed generated fact/state as query-relevant through an exact relevance basis;
4. the prior `GeneratedQueryBindingFingerprint` verifies;
5. the post-commit fingerprint verifies or is explicitly typed deferred/unbound;
6. the two fingerprints differ in a query-relevant entry;
7. prior context/repository/policy lineage verifies.

Thus:

```text
CAUSAL EVENT COMMITTED
+ QUERY-RELEVANT BINDING CHANGE
= GENERATED-LIFE REQUERY REQUIRED

CAUSAL EVENT COMMITTED
+ NO QUERY-RELEVANT FINGERPRINT CHANGE
= NO GENERATED-LIFE REQUERY
```

### 6.2 `V3GeneratedLifeRequeryTrigger`

```text
V3GeneratedLifeRequeryTrigger {
  trigger_id,
  schema_version,

  generation_subject_ref,
  actor_id_or_null,
  query_scope_id,

  source_causal_event_ref,
  source_causal_event_hash,
  source_authority_id,
  source_authority_version,
  source_authority_hash,
  effective_causal_time,

  repository_bundle_id,
  repository_content_hash,
  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  prior_context_ref,
  prior_context_hash,
  prior_query_ref,
  prior_query_hash,

  prior_generated_binding_fingerprint,
  new_generated_binding_fingerprint_or_deferred_ref,
  changed_binding_or_state_refs_and_hashes[],
  query_relevance_basis_refs_and_hashes[],

  query_purpose = STRUCTURAL_CONTEXT_REFRESH,
  status,
  provenance_refs[],
  trigger_hash
}
```

Trigger identity is content-addressed. The source causal event is already committed and remains the causal fact. This requery trigger is a noncausal barrier record.

### 6.3 Required / irrelevant / deferred states

If query-relevant fingerprint changes:

`GENERATED_REQUERY_REQUIRED`

If a causal event commits but the declared query-relevant fingerprint is unchanged:

`GENERATED_REQUERY_NOT_REQUIRED`

If the changed fact is not declared query-relevant to the active query:

`GENERATED_EVENT_QUERY_IRRELEVANT`

If a query-relevant source change is known but the replacement binding/currentness proof is not yet lawfully available:

`GENERATED_REQUERY_DEFERRED_UNBOUND_BINDING`

The runtime may not silently keep using stale context for a context-consuming operation whose declared requirement depends on that unresolved binding.

Missing replacement binding is not permission for V558 to infer one from geography or previous context.

### 6.4 Current accepted concrete example

An accepted ADP-009 committed position/location change emits a prospective generated binding delta. CAN-006 binds the newly current exact fact into the next query.

This produces Channel B immediately at the generated event's effective causal time, even if the currently scheduled Channel-A boundary lies later.

### 6.5 Scheduler handoff

A required Channel-B trigger maps to the accepted ADP-021 envelope:

```text
trigger_class = GENERATED_STATE_REQUERY
effective_time = source generated transition effective_causal_time
semantic_payload_ref = V3GeneratedLifeRequeryTrigger
```

ADP-021 owns ordering and barrier execution. CAN-007 creates no new precedence.

The requery is noncausal and does not advance the causal cursor.

## 7. Prospective context, ordering and stale-wake law

### 7.1 Prospective only

A successful refresh produces new structural context from its effective query time forward.

It does not rewrite:

- earlier generated facts/events;
- earlier ContextQuery objects;
- earlier ResolvedStructuralContext objects;
- prior SelectionRecords;
- earlier causal-event structural receipts;
- actor memory or biography.

Historical replay may consume a context that is stale **now** when its original repository/query/binding/effective-time lineage verifies.

### 7.2 Generated change before static boundary

If Channel B occurs at `T2` and the prior Channel-A metadata scheduled a wake at later `T3`:

```text
commit generated query-relevant change at T2
→ GENERATED_STATE_REQUERY at T2
→ resolve fresh context at T2
→ compute fresh Channel-A metadata from that new context
→ prior T3 wake is stale/superseded if its source context lineage no longer governs the actor/query scope
```

A stale wake is not silently retargeted.

Status:

`STATIC_WAKE_STALE_SUPERSEDED`

### 7.3 Same-time dependency law

ADP-021 remains sovereign.

Examples:

- a static wake already due at `T` may refresh context before a same-time context-consuming causal event;
- if a causal event at `T` must commit first under an explicit dependency and that event creates a query-relevant generated change, the event runs first and Channel B follows immediately;
- after any causal commit, ADP-021 reopens P0 barrier evaluation before the next context-consuming causal work when the accepted query-binding contract requires requery.

CAN-007 never invents a deterministic total order for causal peers.

## 8. Exact deduplication and coalescence

### 8.1 Exact duplicate trigger

An identical `trigger_id + trigger_hash` is idempotent:

`REFRESH_TRIGGER_EXACT_DUPLICATE_DEDUPED`

Invoke at most once.

Same trigger ID with a different hash:

`REFRESH_TRIGGER_IDENTITY_CONFLICT`

Fail closed.

Two nonidentical triggers do not deduplicate merely because their labels, channel, effective times or source actor match.

### 8.2 Exact-equivalent coalescence

Multiple nonidentical ready refresh reasons may share **one resolver call** only when all of these are exact-equivalent:

1. same generation subject / actor / query scope;
2. same effective query time and temporal granularity;
3. same immutable repository bundle ID/content hash;
4. same resolver policy ID/version/hash;
5. same `STRUCTURAL_CONTEXT_REFRESH` purpose;
6. same geographic/static query scope;
7. same requested prior kinds and query constraints;
8. same newest already-committed generated-binding fingerprint valid for that effective time;
9. same normalized `ContextQuery` hash;
10. no accepted dependency requires an intermediate resolution between the reasons.

This includes a ready Channel-A wake and a ready Channel-B trigger at the same effective time **only when** the same normalized query can truthfully satisfy both.

The receipt must retain every trigger ID/hash/channel/reason. Coalescence reduces duplicate read-only work; it does not collapse causation/provenance.

### 8.3 Forbidden coalescence

Do not coalesce when any differs:

- effective time/granularity;
- subject/actor/query scope;
- repository bundle;
- resolver policy;
- query purpose;
- geography/static scope;
- requested prior set;
- current generated-binding fingerprint;
- normalized query;
- dependency requiring an intermediate context.

Do not delay a required static or generated refresh merely hoping that another future reason will arrive and make coalescence convenient.

## 9. Refresh request and replay receipt

### 9.1 Normalized refresh request

A refresh request is the exact normalized `ContextQuery` plus its trigger set.

```text
refresh_request_id = SHA256(
  "RAWLSING\0CAN-007\0CONTEXT_REFRESH_REQUEST_V1\0"
  || normalized_context_query_hash
  || canonical_trigger_set_hash
  || effective_query_time
)
```

Trigger-set canonical ordering is serialization only.

### 9.2 `V558ContextRefreshReplayReceipt`

```text
V558ContextRefreshReplayReceipt {
  receipt_id,
  schema_version,

  refresh_request_id,
  generation_subject_ref,
  actor_id_or_null,
  query_scope_id,

  effective_query_time,
  effective_query_time_granularity,

  trigger_refs_and_hashes[],
  trigger_channels[],
  coalesced,
  exact_equivalence_proof_hash_or_null,

  repository_bundle_id,
  repository_content_hash,
  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  prior_context_ref,
  prior_context_hash,
  prior_query_ref,
  prior_query_hash,

  prior_generated_binding_fingerprint,
  applied_generated_binding_fingerprint,

  normalized_refresh_query_ref,
  normalized_refresh_query_hash,
  query_purpose = STRUCTURAL_CONTEXT_REFRESH,

  result_context_ref,
  result_context_hash,
  selection_record_refs_and_hashes[],
  coverage_fidelity_ref_and_hash,
  context_delta_hash_or_null,
  result_status,

  superseded_trigger_refs_and_hashes[],
  next_static_change_metadata_ref_and_hash,

  scheduler_trigger_refs[],
  scheduler_completion_receipt_refs[],
  provenance_refs[],
  receipt_hash
}
```

The receipt is a resolution/audit object, not a causal event.

### 9.3 Result states

Canonical refresh results:

- `REFRESH_RESOLVED_CONTEXT_CHANGED`;
- `REFRESH_RESOLVED_NO_CONTEXT_DELTA`;
- `REFRESH_RESOLVED_VALID_EMPTY_DELTA`;
- `REFRESH_DEFERRED_UNBOUND_BINDING`;
- `REFRESH_BLOCKED_STALE_PRIOR_CONTEXT`;
- `REFRESH_BLOCKED_REPOSITORY_IDENTITY_MISMATCH`;
- `REFRESH_BLOCKED_POLICY_IDENTITY_MISMATCH`;
- `REFRESH_BLOCKED_TRIGGER_IDENTITY_CONFLICT`;
- `REFRESH_INTEGRITY_FAILURE`.

A wake that re-resolves to the same context is lawful. It does not create a causal event or filler history.

A valid-empty structural delta is lawful and remains distinct from unknown or missing authority.

## 10. Immutable repository episode law

Channel B re-resolves the **same immutable repository bundle** as the prior context.

Channel A is likewise computed and consumed inside one immutable repository/policy episode.

If a separately accepted authority/caller selects a different valid immutable repository or different accepted resolver policy, that begins a new resolution episode. CAN-007:

- does not predict when that selection will occur;
- does not mutate the old repository;
- does not rewrite prior contexts;
- does not define repository-selection precedence.

Attempt by V3 to mutate repository content:

`FORBIDDEN_V3_REPOSITORY_MUTATION`

Attempt to reuse one bundle ID with different content:

`REFRESH_BLOCKED_REPOSITORY_IDENTITY_MISMATCH`

## 11. Time, cadence and wall-clock law

Keep distinct:

```text
producer evidence/support time
!= resolver query time
!= Channel-A static boundary time
!= V3 generated-event effective causal time
!= scheduler receipt time
!= host/audit wall clock
```

A year boundary has no CAN-007 significance merely because a year elapsed.

No daily, monthly, annual or other periodic refresh cadence is authorized.

No polling interval is authorized.

If no static boundary exists and no query-relevant generated change occurs, the correct machine state may remain quiescent indefinitely.

Current legacy V558 modules may stamp audit/output artifacts with `utc_now()`. Such timestamps are compatibility/audit metadata only and MUST be excluded from:

- Channel-A boundary calculation;
- Channel-B effective causal time;
- trigger IDs;
- query identity;
- dedup/coalescence;
- resolver outcome;
- replay identity.

## 12. Unknown, missing, deferred, negative and valid-empty behavior

### Channel-A states

- `STATIC_NEXT_CHANGE_SCHEDULED`;
- `STATIC_NEXT_CHANGE_NONE_KNOWN`;
- `STATIC_NEXT_CHANGE_UNKNOWN`;
- `STATIC_NEXT_CHANGE_DEFERRED_MISSING_AUTHORITY`;
- `STATIC_NEXT_CHANGE_INTEGRITY_FAILURE`.

### Channel-B states

- `GENERATED_REQUERY_REQUIRED`;
- `GENERATED_REQUERY_NOT_REQUIRED`;
- `GENERATED_EVENT_QUERY_IRRELEVANT`;
- `GENERATED_REQUERY_DEFERRED_UNBOUND_BINDING`;
- `GENERATED_REQUERY_STALE_PRIOR_CONTEXT`;
- `GENERATED_REQUERY_SOURCE_AUTHORITY_UNBOUND`;
- `GENERATED_REQUERY_INTEGRITY_FAILURE`.

### General law

- unknown is not no-change;
- missing authority is not a negative result;
- deferred is not a default binding;
- valid-empty is not failure;
- same-context refresh is not a pseudo-event;
- no-known-static-boundary is not a polling request;
- stale prior binding is not permission to use mutable `latest`.

## 13. Replay and provenance

Given the same:

- immutable repository bundle ID/content hash;
- resolver policy ID/version/hash;
- generation subject/actor/query scope;
- prior query/context IDs/hashes;
- exact effective query time/granularity;
- exact generated-binding fingerprint;
- exact trigger set IDs/hashes;
- query purpose and requested prior kinds;
- all producer/negative/proxy authority reachable through the query;

replay must reproduce:

- normalized refresh query/hash;
- SelectionRecords/hashes;
- ResolvedStructuralContext/hash;
- CoverageFidelityProfile/hash;
- context-delta classification/hash;
- next Channel-A metadata/hash;
- refresh replay receipt/hash.

Replay must not depend on:

- host wall clock;
- mutable `latest`;
- thread/arrival order;
- filesystem order;
- raw-stage discovery;
- hidden network lookup;
- RNG;
- LLM/model output;
- unrecorded process/environment state.

Divergence must identify the relevant changed identity rather than silently repairing it, including at minimum repository, policy, prior context, generated-binding fingerprint, trigger set, query normalization or producer-selection lineage.

## 14. Compatibility and current-terrain dispositions

| Recovered/current mechanism or ruling | Disposition | Canonical use |
|---|---|---|
| TD-R04 unified refresh list | `ADAPT_AND_SPLIT` | Preserve identified refresh causes, but separate repository-static prediction from generated-life invalidation under SI-R05 H2. |
| SI-R05 H2 two-channel refresh | `PRESERVE_AND_MACHINE_BIND` | Direct semantic basis for CAN-007. |
| ADP-021 `STATIC_CONTEXT_CHANGE_WAKE` | `REUSE_EXACT_SEMANTICS` | Scheduler handoff for Channel A. |
| ADP-021 `GENERATED_STATE_REQUERY` | `REUSE_EXACT_SEMANTICS` | Scheduler handoff for Channel B. |
| ADP-021 P0 exact-equivalent coalescing | `CANONICALIZE` | One read-only resolver call allowed only under exact equivalence with every reason retained. |
| CAN-006 `STRUCTURAL_CONTEXT_REFRESH` | `REUSE_EXACT_QUERY_PURPOSE` | Shared refresh purpose for both channels. |
| CAN-006 generated-position binding set | `REUSE_AS_CONCRETE_CHANNEL_B_BINDING` | Accepted current example of query-relevant generated change. |
| ADP-009 position/location requery obligation | `PRESERVE` | A committed bindable position/location change forces Channel B. |
| ADP-008 phase state | `CONDITIONAL_INPUT_ONLY` | Requery only where exact query/predicate declares the phase relevant. |
| current `ddm_v558_runtime_input_gate.py` | `SUPERSEDED_IMPLEMENTATION_TERRAIN` | Fail-closed/hash/audit patterns only; no terminal refresh semantics. |
| current `ddm_v558_plus_governance.py` | `SUPERSEDED_IMPLEMENTATION_TERRAIN` | Audit/readiness continuity only. |
| legacy `utc_now()` timestamps | `AUDIT_ONLY` | Never semantic trigger/effective-time/replay input. |
| compulsory annual refresh | `REJECT` | Annual loop is not terminal scheduler/context ontology. |
| refresh after every causal event | `REJECT` | Only declared query-relevant fingerprint changes trigger Channel B. |
| geography→position inference | `REJECT` | Geography may be its own exact query binding; it cannot create a generated position. |
| wall-clock polling | `REJECT` | No polling cadence exists. |

No historical ZIP content was used or dispositioned.

## 15. Forbidden inferences and implementation shortcuts

A conforming implementation must reject:

- “no static boundary is known, therefore check again in one year/day/hour”;
- “a V3 event happened, therefore requery” without a declared query-relevant fingerprint change;
- “the actor moved geographically, therefore their class/sect/party/household position changed”;
- “the scheduled static boundary is near, therefore delay an already-required generated requery”;
- “a static wake will happen eventually, therefore skip the generated requery”;
- “same timestamp means same trigger”;
- “same label means duplicate”;
- “same actor means one query scope”;
- “a newer context exists, therefore replace historical context in old event provenance”;
- “V3 needs new structure, therefore mutate the repository”;
- “current host time reached X, therefore wake” absent the exact accepted static trigger;
- “latest repository/policy” as a semantic selector;
- filesystem/list order as trigger precedence;
- a hidden timer as a safety fallback;
- model/LLM inference of query relevance.

## 16. Hostile fixture court

A conforming implementation must prove at minimum:

1. known static structural boundary with no actor event → Channel A wake;
2. Channel A resolution advances no causal cursor;
3. CAN-006 position change before later static date → immediate Channel B;
4. Channel-B refresh recomputes static metadata and supersedes stale old wake where appropriate;
5. irrelevant causal event with unchanged query fingerprint → no Channel B;
6. generated relationship/household/phase/etc. change not declared relevant to current query → no Channel B;
7. exact generated state declared query-relevant and changed → Channel B;
8. geographic change alone cannot fabricate a position binding;
9. same-time already-ready Channel A + Channel B with identical normalized query → one resolver call may coalesce and must retain both reasons;
10. due static refresh required before a context-consuming event may not be delayed waiting for a future coalescence opportunity;
11. different query purpose → no coalescence;
12. different query/actor scope → no coalescence;
13. different repository or resolver policy → no coalescence;
14. exact duplicate trigger ID/hash → one invocation;
15. same trigger ID/different hash → integrity failure;
16. same label/time but distinct trigger identities → no deduplication;
17. stale generated binding/prior context → fail closed; no mutable-latest substitution;
18. Channel B uses the same immutable repository as the prior context;
19. V3 attempt to mutate repository content → reject;
20. static wake cannot replace an already-required Channel B requery;
21. refresh cannot rewrite prior query/context/SelectionRecord/actor history;
22. `STATIC_NEXT_CHANGE_NONE_KNOWN` → no poll/fallback wake;
23. static boundary unknown/missing authority → no invented date;
24. multiple exact static bases at same earliest boundary → preserve all basis refs;
25. refresh resolving to same context → `REFRESH_RESOLVED_NO_CONTEXT_DELTA`, no pseudo-event;
26. lawful valid-empty delta → no filler context or event;
27. annual tick without exact static/generated trigger → no refresh;
28. host wall-clock change alone → no refresh;
29. same immutable inputs/trigger set → replay exact query/context/receipt hashes;
30. changed generated-binding fingerprint → explicit replay divergence, never silent repair.

## 17. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

Hard accepted architecture uniquely fixes the existence and ownership of the two refresh channels. The genuine remaining design ambiguity is narrower:

**Alternative A:** execute one resolver call for every nonidentical ready refresh reason.

**Alternative B:** permit one resolver call for multiple nonidentical ready reasons only when the normalized query is exactly equivalent, while retaining every trigger/reason in the replay receipt and never skipping a required intermediate resolution.

Chosen:

`EXACT_EQUIVALENT_COALESCENCE_WITH_FULL_CAUSAL_REASON_PROVENANCE`.

Tie-break principles:

- historical causality/provenance without redundant semantic machinery;
- minimum sufficient machinery;
- exact multiplicity without flattening;
- no convenience-driven delay of required refresh;
- deterministic replay;
- separation between read-only context resolution and causal history.

The Governing Spirit supplied no trigger, cadence, static boundary, query-relevance fact, generated actor fact, resolver selection rule or repository transition semantics.

## 18. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_CAN007_BLOCKER`.

CAN-007 closes the named semantic blocker for:

- `V558-P4`;
- `V3-P4`.

It does not release production implementation.

Remaining independent gates include:

- physical canonical V558 repository/resolver implementation and `EXT-007` before real V3-P4 integration;
- V558 implementation packets and acceptance harnesses;
- any other packet-specific physical/authority gate already bound by RA-R00;
- same-Batch-02 CAN-004/CAN-005 remain independently adjudicated and were not consumed here.

CAN-007 has not invented their semantics.

## 19. Final token

`CAN_007_CONTEXT_REFRESH_REQUERY_CANONICALIZATION = PASS`
