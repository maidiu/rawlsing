# REQUEST / RECEIPT SEMANTIC SCHEMA + INGRESS CONSTITUTION R1

Status:

`NORMATIVE_SCHEMA_CANDIDATE__USES_EXISTING_EXACT_REF_AUTHORITY_VOCABULARY__NO_RUNTIME_IMPLEMENTATION`

## 1. Reference discipline

Every identifier below MUST be an exact immutable semantic/reference identity using current PRE553-style exact-ref / authority-ref / semantic-hash discipline wherever lawful.

No field may be satisfied by bare label, filename, cache key, array index, mutable `latest`, or carrier location when a semantic/authority identity is required.

## 2. World/root binding requirements

`WORLD_ROOT_REF` MUST identify a stable content-addressed world/release/replay horizon sufficient to recover:

```text
PRODUCER_RELEASE_REFS[]
SOURCE_UNIVERSE_REFS[] where relevant
AUTHORITY_HORIZON_REFS[]
RULE_AUTHORITY_REFS[] where relevant
CURRENTNESS_BASIS_REFS[]
DEPENDENCY_ROOTS[]
REPLAY_ROOT_REF
```

The root MAY be a manifest/reference graph and MAY dereference source-backed products. It need not contain proposition payloads.

## 3. `PREV3_V3_CONTEXT_RESOLUTION_REQUEST_R1`

Required semantic fields:

```text
constitution_ref
actor_ref
world_root_ref
effective_time_basis_ref
valid_time_basis_or_interval_ref
purpose_or_query_ref
downstream_consumer_or_ingress_purpose_ref
permission_use_ceiling_ref
resolver_semantic_version_ref
```

Optional only where semantically inapplicable, never merely inconvenient:

```text
requested_ingress_class_filter[]
requested_producer_scope_refs[]
requested_relation_scope_refs[]
```

Identity law:

`REQUEST_ID = ExactRef(semantic_hash(canonical_semantic_serialization(all required fields + semantically present optional fields)))`.

The canonical serialization MUST be versioned and deterministic.

Hard prohibitions:

- actor index may not infer psyche;
- consumer desire may not widen permission/use ceiling;
- queryability may not mint use authority;
- mutable release aliases may not enter identity.

## 4. `PREV3_V3_RESOLVED_RESULT_BINDING_R1`

Each result binding MUST preserve:

```text
proposition_ref
ingress_class
semantic_owner_ref
authority_instance_ref
producer_release_ref
root_ref
currentness_tuple
provenance_refs[]
witness_refs[]
claim_ceiling_ref
permission_use_ceiling_ref
causal_use_ceiling_ref
uncertainty_missingness_negative_state_ref
dependency_refs[]
invalidation_determinant_refs[]
supersedes_result_binding_ref? 
```

`currentness_tuple` MUST keep distinct currentness dimensions distinct where current architecture distinguishes them, including as applicable:

- proposition/fact currentness;
- rule currentness;
- rule-application currentness;
- witness currentness;
- producer release currentness;
- valid-time applicability;
- root/replay-horizon currentness.

No single `is_current=true` flag may erase those distinctions.

Hard laws:

`RESULT_BINDING != PROPOSITION_TRUTH`

`CARRIER_PRESENT != AUTHORITY_CURRENT`

`WITNESS_PRESENT != FACT_TRUE`.

## 5. `PREV3_V3_CONTEXT_RESOLUTION_RECEIPT_R1`

Required semantic fields:

```text
resolution_id
constitution_ref
request_ref
world_root_ref
actor_ref
purpose_or_query_ref
effective_valid_time_basis_refs[]
producer_release_refs[]
result_bindings[]
coverage_negative_blocker_bindings[]
dependency_closure_refs[]
resolver_semantic_version_ref
replay_identity_ref
supersedes_resolution_ref? 
```

Canonical result ordering MUST be deterministic. Default semantic ordering candidate:

```text
ingress_class
semantic_owner_ref
proposition_ref
authority_instance_ref
```

If a producer's internal ordering is itself semantically meaningful, that order MUST be preserved under an exact producer-owned ordering authority rather than silently resorted.

Identity law candidate:

`RESOLUTION_ID = ExactRef(semantic_hash(request_ref + world_root_ref + resolver_semantic_version_ref + canonical ordered result_bindings + coverage_negative_blocker_bindings + dependency_closure_refs))`.

Replay identity MUST additionally bind the exact executable resolver/serializer version needed to reproduce the receipt from the pinned semantic inputs.

## 6. Ingress-class constitution

### `OBJECTIVE_WORLD_FACT`

Use for actor-independent objective proposition/fact authority.

May condition later generated-life realization only through a competent downstream owner.

### `OBJECTIVE_ACTOR_POSITION_OR_POSITIONED_CONSEQUENCE`

Use only where exact authority already owns an objective actor-indexed position/consequence.

`POSITION != PSYCHE`.

### `OPPORTUNITY_OR_APPLICABILITY`

Use for lawful possibility/applicability basis.

`OPPORTUNITY != OCCURRENCE` and `APPLICABILITY != ENCOUNTER`.

### `NON_EVENT_CONDITION`

Use for durative objective conditions not semantically eventful.

Must preserve interval/currentness/termination.

### `DIRECTED_RELATION`

Use for objective relations with exact directed endpoints/roles.

Direction may not be flattened into an unordered context tag.

### `RECURRENT_ACTIVITY`

Use for objective recurrent processes/activities with exact recurrence/duration/currentness semantics.

Recurrence does not authorize creation of synthetic event instances absent occurrence authority.

### `EVENT_OR_OCCURRENCE_BASIS`

Use for exact event/occurrence bases under competent event/admission authority.

Does not establish actor encounter or response.

### `WITNESS_OR_CURRENTNESS_EVIDENCE`

Use for evidence that bears on fact/rule/application/currentness without becoming the fact itself.

### `TYPED_UNKNOWN_NEGATIVE_OR_BLOCKER`

Use for exact negative/unknown/blocker states, including PRE553-style distinctions such as unavailable, unresolved, not-applicable, noncomparable, valid-empty, integrity-failure, denied/out-of-scope authority and other exact current states.

No negative state may be silently coerced to numeric zero or Boolean false.

## 7. Realization routing

Resolution creates **objective availability**, not generated-person realization.

Routing candidate:

```text
OBJECTIVE_WORLD_FACT
OBJECTIVE_ACTOR_POSITION_OR_POSITIONED_CONSEQUENCE
OPPORTUNITY_OR_APPLICABILITY
NON_EVENT_CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
        -> exact competent V3 contextual/realization owner

EVENT_OR_OCCURRENCE_BASIS
        -> existing occurrence/admission ingress
        -> V3 generated occurrence/encounter only under exact authority
        -> CAN-008 R2 person×event coupling

WITNESS_OR_CURRENTNESS_EVIDENCE
TYPED_UNKNOWN_NEGATIVE_OR_BLOCKER
        -> evidence/coverage/currentness handling only
```

PFF and V2 remain downstream and may not rescue missing realization.

## 8. Non-event minimum contract for future OBL062 owner

The future owner MUST accept read-only exact objective context bindings containing, as applicable:

```text
context_proposition_ref
actor_ref? (only where objective actor-index authority exists)
relation_endpoint_refs[] / direction
valid_interval_ref
duration_ref
recurrence_basis_ref
termination_ref
currentness_tuple
semantic_owner_ref
authority_instance_ref
witness/provenance_refs[]
permission/use/causal-use ceilings
dependency/invalidation refs[]
negative/blocker state
```

Output at this gate is contextual availability/conditioning eligibility only.

No fake event; no subjective promotion.

## 9. Event minimum contract

The event boundary MUST preserve at least:

```text
event_or_occurrence_basis_ref
occurrence_or_admission_authority_ref
world_root_ref
effective/valid time
objective participant/target/relation refs where separately owned
provenance/witness/currentness refs
permission/use ceiling
dependency/replay refs
```

The PRE-V3 seam stops before receivability, uptake/appraisal, recruitment, response/metabolism or durable change.

Terminal:

`REQUEST_RECEIPT_AND_INGRESS_SCHEMA_COMPLETE_AS_CANDIDATE__NO_RUNTIME_CLAIM`
