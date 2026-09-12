# ASTRA-C06 — Objective Non-Event Serving and V3 Ingress Contract Candidate R1

Status: `CANDIDATE_PASS_AT_BOUNDED_CONTRACT_OWNER_GRAIN__NOT_HQ_ADOPTED__NOT_RUNTIME_IMPLEMENTED`

Exact grain: `PREV3_OBJECTIVE_NON_EVENT_SERVING_AND_V3_INGRESS_R1_ONLY`

Candidate contract identity:

`PREV3_OBJECTIVE_NON_EVENT_SERVING_AND_V3_INGRESS_CONTRACT@1.0.0-CANDIDATE.C06`

## 1. Scope grounding

This candidate is produced on existing worker branch `agent/rabochii-astra-c06-non-event-serving-v3-ingress-r1` from commissioned tip `f167a696984647979e5438083a3d09cf871c00be`, whose frozen dispatch parent is `2a88795031d80cb5bc49979c34ace0dd2427ca6e`.

The clean semantic floor remains `3468673673db2f3de804d6e825585f86ff98e870`. Quarantined OBL063 terminal driver/type semantics remain quarantined and are not consumed.

Current ledger identifier `OBL062` is already occupied by the post-V3/pre-V2 Psychic Field Forge reconciliation grain. C06 therefore does **not** rename, overwrite, close, or consume `OBL062`. This candidate uses its own exact semantic identity above while C01 independently reconciles obligation naming.

No sibling worker return is consumed as authority.

## 2. Constitutional result

A generic non-event receipt/ingress contract is semantically possible without moving person construction into PRE-V3.

The controlling noncollapses are:

```text
OBJECTIVE_ACTOR_POSITION != PERSON_STATE
OBJECTIVE_OPPORTUNITY != ACTOR_UPTAKE
STANDING_CONDITION != PRECIPITATING_EVENT
MACHINE_READING != ACTOR_UPTAKE
STRUCTURAL_CONTEXT_ELIGIBILITY != V3_MUTATION_PERMISSION
CURRENT OBJECTIVE FACT != ACTOR EXPERIENCE
```

PRE-V3 may serve exact objective standing, durative, relational and possibility facts, including actor-indexed objective facts. It may not infer whether an actor noticed, interpreted, cared about, believed, appraised, remembered, preferred, desired, resisted, or responded to them.

## 3. Eligible objective non-event semantics

The minimal positive baseline is intentionally narrower than the complete SDTF temporal-form vocabulary.

Eligible non-event forms at this contract grain:

- `CONDITION`
- `DIRECTED_RELATION`
- `RECURRENT_ACTIVITY`

Eligible assertion kinds at this contract grain:

- `K1 CONSTITUTIVE_POSITIONAL`
- `K2 QUALIFIED_POSSIBILITY`
- `K4 ACTIVE_DURATIVE`

`K3 REALIZED_OCCURRENCE` is not a non-event input and must remain on an occurrence/event route.

`TRANSITION` and `ORDERED_HISTORY` are not silently admitted as generic non-event ingress by this candidate; they require their exact owner/consumer contract so their internal occurrence semantics are not flattened.

`UNKNOWN_NOT_PROVEN` is never a fact and cannot be emitted as an actor state.

A K4 Path-B instance is lawful only when all of the following survive exactly: owner-declared continuing-state semantics; type-compatible support with a validity interval overlapping query time; complete authoritative termination/supersession/invalidation coverage through query time; and no defeating closing fact. An establishment event plus silence is insufficient.

Negative truth remains source/owner governed. Missing, stale, expired, absent, unresolved, or failed-positive evidence is not converted into a negative fact.

## 4. Producer-preserving receipt

A runtime implementation of this candidate MUST create a content-addressed receipt equivalent to the following semantic record. Field names are normative in meaning, not a physical storage mandate.

```text
OBJECTIVE_NON_EVENT_SERVING_RECEIPT
  schema_id
  schema_version
  receipt_id
  receipt_content_hash

  producer_object_ref
  producer_locator_ref
  canonical_producer_family
  producer_semantic_class
  producer_owner_authority_ref
  producer_schema_ref

  temporal_form
  assertion_kind
  polarity
  currentness
  modality
  proof_adjudication
  valid_time_binding_ref
  decision_effective_time_ref

  objective_actor_binding_ref_or_null
  objective_position_context_binding_ref_or_null
  world_or_release_root_ref_or_null

  source_evidence_refs[]
  determinant_or_witness_refs[]
  negative_or_closure_refs[]

  producer_allowed_uses[]
  publication_allowed_uses[]
  resolver_allowed_uses[]

  repository_ref
  context_query_ref
  resolution_receipt_ref
  selection_record_ref

  currentness_receipt_ref_or_null
  v3_transition_owner_declaration_ref_or_null
  structural_peer_use_receipt_ref_or_null

  ingress_effect
  actor_state_effect = false
```

The receipt is a serving/provenance envelope, not a new semantic owner. It MUST NOT copy, normalize, reclassify, average, synthesize, or rewrite the producer payload in a way that changes source meaning. Exact producer identity remains authoritative.

If an objective actor is indexed, the actor binding proves only the objective fact's applicability to that actor/position/context/time grain. It supplies no subjective premise.

## 5. Permission law

Every downstream use is an item-wise subset intersection:

```text
resolver_allowed_uses
  subset_of publication_allowed_uses
  subset_of producer_allowed_uses
```

No adapter may widen `REVIEW` or `CONTEXT` into `ACTIVE_CAUSAL` merely because V3 requests the object.

Exact identity/hash/closure and permission failure must fail closed. No latest/default/fuzzy repair is permitted.

## 6. Serving leg

The existing M4 runtime supplies the accepted producer-preserving pattern:

```text
exact producer object
-> exact governance record
-> exact producer locator
-> immutable repository/index
-> exact query
-> SelectionRecord
-> ResolutionReceipt
```

M4 resolution preserves producer family/object/hash, enforces producer/publication permission subsets, rejects audit-only material as semantic context, rejects fuzzy/latest repair, and deliberately returns no `ResolvedStructuralContext`.

This candidate reuses those laws; it does **not** claim that the present M4 root-family allowlist already admits generic SDTF D1-prime/non-event products. The current generic D1-prime publication/serving adapter remains an implementation gap.

## 7. V3 ingress leg

The accepted M5 pattern is the lawful ingress shape when a V3 transition owner elects to consult structural context:

```text
exact M4 ResolutionResult
+ exact CURRENT structural-currentness receipt
+ exact V3 transition-owner peer requirement declaration
-> ResolvedStructuralContext
-> validation receipt
-> structural peer use receipt
```

The only effect authorized by the existing M5 seam is:

`STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION`

and `actor_state_effect` remains `false`.

Therefore this candidate authorizes **availability to V3**, not subjective uptake. V3 remains responsible for any later person-side appraisal, interpretation, response, learning, memory, belief, motive, preference, durable state, or biography under its own transition-owner authority.

A historical/noncurrent objective fact may remain lawfully servable as historical objective context under an exact consumer contract, but it cannot be relabeled `CURRENT` merely to satisfy M5 current-peer materialization. This candidate does not invent a historical-person effect path.

## 8. CAN-008 firewall

CAN-008 R2 requires an exact generated/admitted precipitating **event** basis for its person×event coupling. A standing condition, objective opportunity, directed relation, recurring activity, or structural context receipt MUST NOT be converted into a synthetic precipitating event to enter CAN-008.

If a real event separately occurs, CAN-008 may consume that real event under its own authority while V3 separately consults authorized structural context. The non-event object remains context; the event remains event; the actor's uptake/appraisal remains V3-owned.

## 9. World/release binding

This contract can be specified before C02 or C05 produces real populated world instances. A concrete current-world receipt, however, may claim world/release membership only when an exact competent world/release/root reference and its temporal/currentness bindings exist.

Absence of a world instance at C06 time is therefore `SOURCE_INSTANCE_MISSING_FOR_RUNTIME_PROOF`, not a reason to fabricate one and not a blocker to this bounded contract specification.

## 10. Exact implementation gap preserved

Current M4 code admits frozen root families `V553`, `V554`, `V555`, `V556`. The Astra system map independently records the generic `SDTF D1-prime -> publication` edge as missing.

Accordingly:

- semantic owner conflict: **not found** at this candidate grain;
- contract shape: **recovered/specifiable**;
- generic D1-prime/non-event publication adapter: **not implemented/proved**;
- real source-backed non-event instance through this generic adapter: **not proved**;
- independent hostile runtime qualification: **not proved**;
- HQ adoption: **not performed**.

An implementation successor must bind exact eligible producer families/classes into producer-preserving publication/resolution without weakening M4 guards or broadening permissions, then qualify positive and negative cases.

## 11. PASS condition

The bounded owner/contract court passes because standing/durative/context information can be represented losslessly by exact producer identity plus explicit temporal/currentness/permission/provenance bindings, objective actor indexing remains objective, M4/M5 already prove the required no-widening/no-person-state seam pattern, and CAN-008 supplies an explicit event boundary that prevents event laundering.

This PASS does not assert a functioning generic runtime vertical.

Terminal:

`ASTRA_C06_OBJECTIVE_NON_EVENT_SERVING_AND_V3_INGRESS_CONTRACT_CANDIDATE_PASS__PRODUCER_OWNERSHIP_PRESERVED__NO_EVENT_LAUNDERING__V3_UPTAKE_REMAINS_V3__GENERIC_D1_PRIME_ADAPTER_STILL_REQUIRES_IMPLEMENTATION_AND_QUALIFICATION`
