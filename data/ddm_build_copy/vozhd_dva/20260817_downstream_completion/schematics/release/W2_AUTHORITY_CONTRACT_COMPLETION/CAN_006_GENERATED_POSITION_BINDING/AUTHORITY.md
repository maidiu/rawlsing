# CAN-006 — Generated-Position Binding Canonicalization

**Assignment:** W2-06 — CAN-006 / Generated-Position Binding Canonicalization  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w2-can-006-generated-position-binding`  
**Exact launch base:** `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`  
**Canonicalization ID:** `CAN-006`  
**Canonical authority:** `V3_GENERATED_POSITION_BINDING_CONTRACT`  
**Authority version:** `1.0.0`  
**Binding schema:** `V3_GENERATED_POSITION_BINDING@1.0.0`  
**Echo schema:** `V558_GENERATED_POSITION_BINDING_ECHO_RECEIPT@1.0.0`  
**Owner:** `V3_CONTEXTRESOLVER_BINDING_SEAM`  
**Semantic position owner:** exact accepted V3 generated-position producer  
**Mode:** canonicalization only; no production code; no V558/V3 implementation; no architecture reopening  
**Historical ZIP:** `NOT_AUTHORIZED_NOT_USED`  
**Verdict:** `PASS`  
**CONSUMER_RELEASE_SUFFICIENCY:** `SUFFICIENT_FOR_CAN_006_JURISDICTION__DIRECT_CONSUMERS_REMAIN_OTHER_DEPENDENCY_AND_IMPLEMENTATION_GATED`

## 0. Binding holding

CAN-006 binds an already-lawful generated structural-position fact into the accepted stage-blind V558 `ContextQuery` without transferring semantic ownership to V558.

```text
Phase A
  time + geography + generation/development context
  -> ContextResolver over immutable StructuralPriorRepository R
  -> structural context; position-conditioned material may remain unbound

V3
  -> separately accepted position producer
  -> immutable generated position event/fact

Phase B
  exact generated-position binding
  -> ContextResolver over THE SAME immutable StructuralPriorRepository R
  -> additional lawful context for that exact position
  -> SelectionRecord + generated-binding echo provenance
```

Binding nonidentity:

```text
STRUCTURAL_PRIOR != GENERATED_POSITION_FACT != GENERATED_POSITION_BINDING
!= RESOLVER_DERIVED_CONTEXT != ACTOR_HISTORY_CREATED_BY_RESOLUTION

GEOGRAPHY != STRUCTURAL_POSITION
TEMPORAL_PROXY != GENERATED_POSITION
DEVELOPMENTAL_PHASE != RESOLVER_PHASE_A_OR_B != STRUCTURAL_POSITION
POSITION_OWNERSHIP != BINDING_TRANSPORT != PREDICATE_EVALUATION
```

V3 owns generated position truth. V558 receives caller/V3-owned `GENERATED_RUNTIME_FACT_REF`, validates the transport/integrity contract, evaluates only already-governed structural predicates against it, and echoes exact provenance. V558 may not create, mutate, end, supersede, reinterpret or backfill the position.

A valid binding does not require a nonempty Phase-B delta. `VALID_EMPTY_POSITION_BOUND_CONTEXT_DELTA` is lawful.

## 1. Evidence inspected

No historical ZIP was authorized or used.

Directly inspected at exact W2 base:

- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`;
- `integration/W1_AUTHORITY_EXPANSION_CLOSURE_RULING.md`;
- `integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- RA-R00 `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md` and `RESULT.json`;
- accepted `ADP-009 / V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE@1.0.0` MD/JSON;
- corrected accepted `CAN-001 / V554_APPLICABILITY_PREDICATE_CONTRACT@1.0.0`, especially K01;
- accepted `ADP-006 / RA-MUST-006-TEMPORAL-PROXY-ELIGIBILITY@1.0.0`;
- accepted `ADP-008 / V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`;
- accepted TD-R04 V557/V558 result;
- accepted SI-R05 V558→V3 result;
- current `data/ddm_build_copy/ddm_v558_runtime_input_gate.py`;
- current `data/ddm_build_copy/ddm_v558_plus_governance.py`;
- current `data/ddm_build_copy/test_w03_v551j_v3_fail_closed.py`;
- W2 common law and W2-06 section only.

No other W2 return was consumed.

Accepted architecture already fixes immutable per-build repository identity, deterministic/read-only ContextResolver behavior, explicit generated-position query bindings, typed unbound state before position generation, generated-binding echo as `GENERATED_RUNTIME_FACT_REF`, and same-repository Phase-A/Phase-B resolution. Current checked-in V558 runtime-gate/governance code is superseded implementation terrain and supplies no generated-position semantics.

## 2. Jurisdiction

CAN-006 owns only:

1. stable generated-position binding serialization and identity;
2. exact generated-subject/actor binding;
3. exact producer authority ID/version/hash and acceptance snapshot;
4. exact generated position fact/event refs and hashes;
5. exact requirement/binding-key identity;
6. effective/as-of time plus current-position-view proof;
7. admissible query-purpose binding for Phase B, refresh and replay;
8. same-repository Phase-A→Phase-B proof;
9. binding-set fingerprint;
10. Phase-B generated-binding echo receipt;
11. SelectionRecord linkage;
12. stale/superseded/unknown/missing/forbidden/integrity behavior;
13. deterministic replay/provenance.

CAN-006 does **not** create actors, generated entities, positions, transitions, relationships, households, genealogy, developmental phases, temporal-proxy semantics, repository bundles, resolver policies, V554 F2 semantics, actor experience/history, or a broad refresh policy. It does not reinterpret ADP-009.

## 3. Producer-authority contract

A binding is admissible only from a separately accepted authority that owns the exact generated position fact.

The generic interface namespace remains the corrected CAN-001 namespace:

`V3_GENERATED_POSITION_BINDING_PRODUCER`

This is an interface namespace, not semantic authority.

Current generic producer:

```text
authority_id      = V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE
authority_version = 1.0.0
decision_packet   = ADP-009
semantic_class    = GENERATED_RUNTIME_FACT
```

Every binding carries:

```text
producer_authority {
  authority_id,
  authority_version,
  authority_hash_algorithm,
  authority_hash,
  authority_acceptance_snapshot_ref,
  authority_acceptance_snapshot_hash
}
```

Unknown/unaccepted producer → `POSITION_BINDING_PRODUCER_AUTHORITY_UNBOUND`.
Version/hash mismatch → `POSITION_BINDING_PRODUCER_AUTHORITY_MISMATCH`.

Genealogy is not a universal producer. A later accepted authority may supply this interface only if it actually owns the exact position fact and emits exact immutable generated-fact/event identity. Geography, demographics, prevalence, labels, resolver context and temporal proxies can never satisfy this producer contract.

## 4. Canonical binding schema

### `V3_GENERATED_POSITION_BINDING@1.0.0`

```text
V3GeneratedPositionBinding {
  binding_id,
  binding_schema_version,

  generation_subject_ref,
  generation_subject_identity_hash,
  actor_id,

  binding_key_ref,

  position_fact_ref,
  position_fact_hash,
  position_assertion_kind,
  establishing_or_current_position_event_ref,
  establishing_or_current_position_event_hash,

  producer_authority {
    authority_id,
    authority_version,
    authority_hash_algorithm,
    authority_hash,
    authority_acceptance_snapshot_ref,
    authority_acceptance_snapshot_hash
  },

  position_rule_id,
  position_rule_version,
  position_effective_from,
  binding_as_of_effective_time,

  current_position_view_ref,
  current_position_view_hash,

  generated_runtime_epistemic_class = GENERATED_RUNTIME_FACT_REF,
  provenance_refs[],
  binding_content_hash
}
```

`actor_id` is required for ADP-009 actor positions. `generation_subject_ref` must resolve to that same actor. If stable actor identity is not established, return `POSITION_BINDING_ACTOR_ID_UNESTABLISHED`.

`binding_key_ref` must be the exact position dimension/requirement governed by the source fact. Stratum labels, prose synonyms or fuzzy matches are insufficient.

`position_assertion_kind` passes through the source fact unchanged:

- `POSITIVE_POSITION`;
- `EXPLICIT_POSITION_ABSENCE`.

Unknown/missing/unbound is never converted into explicit absence.

### Identity

Canonical binding identity is content-addressed:

```text
binding_content_hash = SHA256(canonical_utf8_json(binding_semantic_fields))
binding_id = SHA256("V3_GENERATED_POSITION_BINDING_V1" || binding_content_hash)
```

The identity includes the exact source authority, actor/subject, fact/event, binding key, effective/as-of time and current-position-view proof. It is a query-time immutable envelope, not a mutable `current_position` slot.

Canonical sorting of unordered reference arrays is serialization only and never semantic precedence.

## 5. Currentness, stale and change law

A prospective binding is valid only when all of these verify at `binding_as_of_effective_time`:

- actor/subject identity;
- source authority/version/hash;
- fact/event identity and hash;
- binding key;
- fact is effective;
- `current_position_view_ref/hash` establishes that the fact is current for the requested binding key;
- no governing end/superseding event has become effective at or before the as-of time.

If the fact has been ended or superseded for a prospective query:

`POSITION_BINDING_STALE_SUPERSEDED`

The resolver may **not** silently substitute the newest/nearest/lexicographically first position. Caller/V3 must submit the exact replacement binding.

If currentness cannot be established:

`POSITION_BINDING_CURRENTNESS_UNKNOWN`

If query/as-of time precedes the fact's effective time:

`POSITION_BINDING_NOT_EFFECTIVE_AT_QUERY_TIME`

A later ADP-009 transition creates a new generated fact/event, a new binding delta and a new prospective binding/query lineage. Earlier facts, bindings, contexts, SelectionRecords and actor history remain immutable.

Historical replay may lawfully consume a fact that is superseded *now* only when the original query time, original currentness proof, original repository identity and original binding/SelectionRecord lineage all verify.

## 6. Binding set contract

A ContextQuery may carry zero or more exact position bindings because multiple independent/coexisting position facts are lawful.

```text
V3GeneratedPositionBindingSet {
  generation_subject_ref,
  actor_id,
  binding_refs_and_hashes[],
  binding_set_hash
}
```

Rules:

- zero bindings is lawful and preserves `UNBOUND_REQUIRES_RUNTIME_POSITION` where required;
- no canonical dominant position exists;
- exact duplicate ref+hash may deduplicate for serialization;
- same binding ID with different hash is `POSITION_BINDING_IDENTITY_CONFLICT`;
- list/ID order cannot select a semantic winner;
- incompatible source facts must be resolved by their owning V3 authority, never by V558.

## 7. Phase-A law

Canonical Phase-A query purpose:

`STRUCTURAL_CONTEXT_PHASE_A`

Inputs are time, geography, generation/development context and already-lawful non-position bindings. A generated position binding is not required.

Position-conditioned producer objects for which no exact generated position exists remain typed unbound/deferred. The resolver may expose target options/requirements as structural context, but those are not actor position facts.

Forbidden:

- geography→class/sect/party/institution/occupation/household/family/Self;
- prevalence→membership or probability;
- resolved target→actor occupancy;
- resolver selection→generated position;
- temporal proxy→position.

A resolver attempt to author a position is `FORBIDDEN_POSITION_GENERATION_IN_RESOLVER`.
A geography-derived binding is `FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE`.

## 8. Phase-B law

Canonical Phase-B query purpose:

`STRUCTURAL_CONTEXT_PHASE_B`

Required Phase-B inputs include:

- exact Phase-A ContextQuery/context receipt refs and hashes;
- exact Phase-A repository bundle ID/content hash;
- same generation subject/actor;
- exact generated-position binding set/hash;
- query time/granularity and geography identity;
- independently governed developmental-phase ref/hash where supplied;
- exact resolver-policy identity/version/hash;
- requested prior kinds.

Before evaluation, assert:

```text
phase_b.repository_bundle_id == phase_a.repository_bundle_id
phase_b.repository_content_hash == phase_a.repository_content_hash
```

Different bundle → `PHASE_B_REPOSITORY_IDENTITY_MISMATCH`.
Same bundle ID with different content hash → `REPOSITORY_CONTENT_INTEGRITY_FAILURE`.

The resolver evaluates already-governed predicates, including CAN-001 K01, against the exact binding. It does not inspect ADP-009 candidates, rerun position selection or reinterpret the position.

A valid binding may yield no newly selected structural objects; emit `VALID_EMPTY_POSITION_BOUND_CONTEXT_DELTA` rather than filler context.

## 9. Refresh and replay query purposes

After a later generated position change, the caller/V3 requery purpose is:

`STRUCTURAL_CONTEXT_REFRESH`

The newly current binding is used prospectively. The same immutable repository is used unless a separately accepted repository transition independently selects a different immutable bundle. A new bundle starts a new resolution episode; it never mutates prior Phase-A/Phase-B records.

`REPLAY_AUDIT_EXPLANATION` may reproduce a prior lawful binding/selection decision but may not create a new position or a new temporal-proxy decision.

CAN-006 does not absorb CAN-007's broader static-vs-generated refresh contract.

## 10. ADP-008 phase relation

ADP-008 phase identity is independent input context.

Accepted universal phase identities remain:

- `V3DP_GENERATION_PENDING`;
- `V3DP_DEVELOPMENT_ACTIVE`.

A supplied phase ref/hash may be echoed in ContextQuery provenance where a consumer needs it. It cannot be used as a position binding unless a separate accepted position producer has actually generated the corresponding position fact.

Resolver `PHASE_A`/`PHASE_B` labels are query roles, not ADP-008 developmental phases.

## 11. ADP-006 temporal-proxy relation

Temporal proxy eligibility is orthogonal to generated-position identity.

After an exact generated position is supplied, ADP-006 may independently authorize a structural temporal anchor for position-conditioned producer material under its own rules.

A proxy observation is never a generated position source or repair mechanism. A future/prior proxy cannot create, change, end or backdate an actor position.

Attempted proxy→position promotion:

`FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE`

Selection provenance must preserve both independent lineages:

1. exact generated-position binding authority/fact/event; and
2. exact ADP-006 temporal anchor/rule/lag provenance where proxying occurred.

## 12. Phase-B echo receipt

### `V558_GENERATED_POSITION_BINDING_ECHO_RECEIPT@1.0.0`

```text
V558GeneratedPositionBindingEchoReceipt {
  receipt_id,
  receipt_schema_version,

  repository_bundle_id,
  repository_content_hash,
  context_query_id,
  context_query_hash,
  query_purpose,
  phase_a_context_ref,
  phase_a_context_hash,

  generation_subject_ref,
  actor_id,
  generated_position_binding_set_hash,
  consumed_binding_refs_and_hashes[],

  echoed_generated_runtime_fact_refs[],
  echoed_epistemic_class = GENERATED_RUNTIME_FACT_REF,

  selection_record_refs_and_hashes[],
  resolved_structural_context_ref,
  resolved_structural_context_hash,
  result_state,

  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,
  temporal_proxy_authority_refs[],
  provenance_refs[],
  receipt_hash
}
```

The echo receipt states only: *these exact caller-owned generated position facts were used as query criteria for this resolution*. It does not assert a new actor fact, memory, experience or history.

Every position-conditioned `SelectionRecord` must retain the exact binding ref/hash, source fact/event ref/hash, producer authority identity, binding key/as-of time, query/repository identity, predicate/evaluator identity and independent temporal-proxy provenance where applicable.

## 13. Result / error states

Canonical states:

- `POSITION_BOUND_CONTEXT_SELECTED`;
- `VALID_EMPTY_POSITION_BOUND_CONTEXT_DELTA`;
- `POSITION_BOUND_CONTEXT_DEFERRED_OTHER_REQUIREMENT`;
- `POSITION_BINDING_REPLAY_REPRODUCED`;
- `POSITION_BINDING_MISSING`;
- `POSITION_BINDING_ACTOR_ID_UNESTABLISHED`;
- `POSITION_BINDING_CURRENTNESS_UNKNOWN`;
- `POSITION_BINDING_STALE_SUPERSEDED`;
- `POSITION_BINDING_PRODUCER_AUTHORITY_UNBOUND`;
- `POSITION_BINDING_PRODUCER_AUTHORITY_MISMATCH`;
- `POSITION_BINDING_SUBJECT_MISMATCH`;
- `POSITION_BINDING_KEY_MISMATCH`;
- `POSITION_BINDING_NOT_EFFECTIVE_AT_QUERY_TIME`;
- `POSITION_BINDING_IDENTITY_CONFLICT`;
- `FORBIDDEN_POSITION_GENERATION_IN_RESOLVER`;
- `FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE`;
- `FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE`;
- `PHASE_B_REPOSITORY_IDENTITY_MISMATCH`;
- `REPOSITORY_CONTENT_INTEGRITY_FAILURE`;
- `POSITION_BINDING_INTEGRITY_FAILURE`.

`POSITION_BINDING_MISSING` is not explicit position absence. `POSITION_BINDING_CURRENTNESS_UNKNOWN` is not stale. `VALID_EMPTY_POSITION_BOUND_CONTEXT_DELTA` means the binding was valid and the position-bound query lawfully added no new selected context.

## 14. Immutable-repository proof

CAN-006 passes the immutable-repository court because:

1. the binding is query-local and never inserted into repository storage;
2. its epistemic class remains `GENERATED_RUNTIME_FACT_REF`;
3. every Phase-A→Phase-B pair verifies one identical repository ID and content hash;
4. mismatch fails before position-bound selection;
5. generated actor fact identity remains distinct from structural object identity;
6. fixed bundle + query + resolver policy + generated bindings is deterministic;
7. hidden raw-stage, network, filesystem, wall-clock, mutable-latest or LLM sources are forbidden;
8. later repository publication yields a new immutable bundle and a new resolution episode.

`IMMUTABLE_REPOSITORY_PROOF = PASS`

## 15. Geography→identity rejection proof

The only admissible binding must carry a separately accepted generated-position producer plus exact actor/fact/event/current-view provenance. Geography has none of these fields.

If geography is the only relevant context:

```text
geography -> lawful structural context
position-conditioned object -> UNBOUND_REQUIRES_RUNTIME_POSITION
actor position fact -> NOT CREATED
```

`GEOGRAPHY_TO_IDENTITY_REJECTION_PROOF = PASS`

## 16. Replay / provenance

Replay identity includes at minimum:

- immutable repository bundle ID/content hash;
- resolver policy ID/version/hash;
- exact Phase-A query/context receipt for Phase-B pairs;
- exact Phase-B/refresh/replay ContextQuery ID/hash;
- query purpose and time/granularity;
- geography identity;
- generation subject/actor identity;
- exact ADP-008 phase ref/hash where supplied;
- complete generated-position binding set/hash;
- producer authority IDs/versions/hashes/acceptance snapshots;
- position fact/event/current-position-view refs/hashes;
- binding key and effective/as-of time;
- CAN-001 predicate/evaluator refs where evaluated;
- ADP-006 rule/anchor/lag refs where proxying is used;
- every SelectionRecord ID/hash;
- resolved context ID/hash;
- echo receipt ID/hash;
- integrity/fail-closed outcomes.

Given identical immutable inputs, binding validation, SelectionRecords, resolved context and echo receipt must reproduce exactly. Hidden wall clock, mutable latest, filesystem order, raw-stage discovery, heuristic mapping and LLM judgment are forbidden replay inputs.

## 17. Compatibility disposition

| Existing accepted/current shape | Disposition |
|---|---|
| TD-R04 `ContextQuery.generated_position_bindings[]` | `PRESERVE_AND_CANONICALIZE` |
| SI-R05 generated-binding echo `GENERATED_RUNTIME_FACT_REF` | `PRESERVE_AND_CANONICALIZE` |
| ADP-009 `V3GeneratedPositionBindingDelta` | `PRESERVE_SEMANTIC_TRIGGER__WIRE_SCHEMA_BOUND_HERE` |
| CAN-001 `V554_K01_GENERATED_POSITION_BINDING_SOURCE@1.0.0` | `PRESERVE_COMPATIBLE_SOURCE_ENVELOPE__CAN006_SUPERSET_FOR_QUERY_REPLAY` |
| ADP-006 Phase-A/B/refresh purpose vocabulary | `PRESERVE_QUERY_PURPOSE_ONLY__NO_POSITION_AUTHORITY` |
| ADP-008 exact phase refs | `PRESERVE_AS_INDEPENDENT_QUERY_CONTEXT` |
| current V558 runtime-input/readiness/governance code | `COMPATIBILITY_IMPLEMENTATION_TERRAIN_ONLY__DOES_NOT_IMPLEMENT_CAN006` |
| current fail-closed regression direction | `PRESERVE_AS_ACCEPTANCE_HARNESS_DIRECTION` |
| mutable `latest` actor-position slot | `REMOVE_REJECT` |
| geography/demography/prevalence-derived binding | `REMOVE_REJECT` |
| genealogy-required default producer | `REMOVE_REJECT` |
| temporal proxy as position source | `REMOVE_REJECT` |
| resolver-created actor position/history | `REMOVE_REJECT` |

## 18. Hostile fixtures

| ID | Attack | Required outcome |
|---|---|---|
| H01 | exact ADP-009 positive binding; no genealogy | valid binding; Phase B proceeds |
| H02 | geography-only resolver creates class/sect | `FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE` |
| H03 | prevalence/demography offered as binding | reject; remain unbound |
| H04 | actor A fact bound into actor B query | `POSITION_BINDING_SUBJECT_MISMATCH` |
| H05 | generation subject does not resolve to actor | `POSITION_BINDING_SUBJECT_MISMATCH` |
| H06 | producer authority unaccepted/version/hash mismatch | producer unbound/mismatch |
| H07 | fact or event hash mismatch | `POSITION_BINDING_INTEGRITY_FAILURE` |
| H08 | binding key differs from fact dimension | `POSITION_BINDING_KEY_MISMATCH` |
| H09 | query precedes fact effective time | `POSITION_BINDING_NOT_EFFECTIVE_AT_QUERY_TIME` |
| H10 | fact superseded before prospective query | `POSITION_BINDING_STALE_SUPERSEDED`; no replacement |
| H11 | superseded-now fact replayed at original historical query | reproduce original binding/receipt if lineage verifies |
| H12 | currentness proof missing | `POSITION_BINDING_CURRENTNESS_UNKNOWN` |
| H13 | exact ADP-009 explicit-absence fact | transport exact absence; evaluator owns satisfaction |
| H14 | no generated position fact | remain `UNBOUND_REQUIRES_RUNTIME_POSITION` |
| H15 | ADP-006 proxy offered as position | `FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE` |
| H16 | Phase B different repository bundle | `PHASE_B_REPOSITORY_IDENTITY_MISMATCH` |
| H17 | same repo ID, different content hash | `REPOSITORY_CONTENT_INTEGRITY_FAILURE` |
| H18 | exact same repo/binding/query replay | identical selection/echo |
| H19 | valid binding yields no additional objects | `VALID_EMPTY_POSITION_BOUND_CONTEXT_DELTA` |
| H20 | multiple lawful coexisting position facts | preserve all; no dominant position |
| H21 | same binding ID, different hashes | `POSITION_BINDING_IDENTITY_CONFLICT` |
| H22 | lexical/list order used as semantic winner | reject ordering authority |
| H23 | later position transition after prior history | new prospective binding; old history/receipts immutable |
| H24 | resolver output written as new position/history fact | reject jurisdiction breach |
| H25 | ADP-008 phase/age used as position | reject; independent query context only |
| H26 | resolver Phase-B label treated as developmental phase | reject namespace collapse |
| H27 | genealogy absence defers despite valid ADP-009 binding | reject; ADP-009 binding is sufficient producer prerequisite |
| H28 | hidden mutable latest silently replaces stale binding | reject; caller must submit new exact binding |
| H29 | SelectionRecord lacks binding/fact/producer lineage | `POSITION_BINDING_INTEGRITY_FAILURE` |
| H30 | exact duplicate binding appears twice | dedup serialization only; same semantic set |

## 19. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

Hard authority uniquely fixes semantic ownership, two-phase flow, same-repository law, exact generated-fact provenance, no geography/demography shortcut, no proxy→position laundering, prospective change and fail-closed stale/unknown behavior.

A bounded canonicalization choice remained:

1. mutable “current position” slot owned by V558;
2. copied/fat actor-position payload inside resolver state;
3. thin content-addressed query-time envelope over exact V3 fact/event/current-view refs plus an independent V558 echo receipt.

Choice: **3**. It is the minimum sufficient machinery and preserves producer ownership, dynamic history, actor/structure separation and replay without duplicating actor state in V558. The Governing Spirit supplied no position taxonomy, candidate, default, phase meaning, proxy rule or causal outcome.

## 20. Consumer release sufficiency

RA-R00's normalized direct mapping binds CAN-006 to:

- `V558-P3` — deterministic ContextResolver;
- `V3-P1` — V558/V3 interface/initialization substrate;
- `V3-P4` — generated-position binding/context-refresh integration.

CAN-006 closes its bounded semantic contract only. It does not independently release those packets.

Remaining independent gates include, as applicable:

- `CAN-005` repository/ContextResolver policy binding;
- `MUST-006 / ADP-006` where temporal proxying is used;
- `CAN-007` broader static-vs-generated refresh contract;
- packet-specific accepted V3 authorities;
- `EXT-006` completed V557 publication;
- `IMP-006` / `IMP-007` V558 implementation;
- `EXT-007` completed standalone V558 where required;
- production scheduling and acceptance harnesses.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_CAN_006_JURISDICTION__DIRECT_CONSUMERS_REMAIN_OTHER_DEPENDENCY_AND_IMPLEMENTATION_GATED`

## 21. Final verdict

No production code was modified. V558/V3 were not implemented. No historical ZIP was used. No W2 sibling return was consumed. No generated position, geography-derived identity, temporal-proxy-derived identity or actor history was created by this canonicalization.

`CAN_006_GENERATED_POSITION_BINDING_CANONICALIZATION = PASS`
