# CAN-005 — Repository & ContextResolver Policy Binding

**Assignment:** W2-B02-02 — CAN-005 / Repository & ContextResolver Policy Binding  
**Repository:** `maidiu/rawlsing`  
**Assigned branch:** `agent/vozhd-dva-w2-can-005-context-resolver-policy`  
**Exact launch base:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**RA-R00 item:** `CAN-005`  
**Canonical authority:** `V558_CONTEXT_RESOLVER_POLICY`  
**Authority version:** `1.0.0`  
**ContextQuery schema:** `V558_CONTEXT_QUERY@1.0.0`  
**Logical index contract:** `V558_LOGICAL_INDEX_CONTRACT@1.0.0`  
**SelectionRecord schema:** `V558_SELECTION_RECORD@1.0.0`  
**Resolution receipt schema:** `V558_CONTEXT_RESOLUTION_RECEIPT@1.0.0`  
**Owner:** `V558_CONTEXT_RESOLVER`  
**Mode:** authority canonicalization only; no V558 implementation; no architecture reopening  
**Historical ZIP:** `NOT_AUTHORIZED_NOT_USED`  
**Verdict:** `PASS`

## 0. Binding holding

CAN-005 binds the accepted deterministic V558 repository / `ContextResolver`
policy into one immutable, versioned machine contract.

The resolver is a pure, read-only selection boundary over an already-valid,
immutable `StructuralPriorRepository`:

```text
immutable repository bundle + content hash
+ exact ContextQuery + query hash
+ exact V558_CONTEXT_RESOLVER_POLICY identity/version/hash
+ accepted caller-supplied generated bindings, where lawful
        ↓
exact index discovery
        ↓
exact producer-object dereference / authority verification
        ↓
permission + native scope + producer-condition evaluation
        ↓
temporal precedence / ties / lawful multiplicity
        ↓
SelectionRecord[] + ContextResolutionReceipt
        ↓
ResolvedStructuralContext materialization by the accepted V558 interface
```

For identical immutable repository content, exact query, exact policy and exact
accepted binding inputs, the semantic resolution result is identical.

The binding temporal precedence is exactly:

```text
DIRECT_TEMPORAL_SUPPORT
> authorized LATEST_PRIOR
> authorized EARLIEST_POST
> NO_LAWFUL_ANCHOR
```

`ADP-006` alone owns whether a prior/post observation is proxy-eligible.
`CAN-006` alone owns generated-position binding identity and transport.
Producer meaning, predicates, relations, temporal support, geography, strata,
negative authority and multiplicity remain producer-owned.

The constitutional noncollapse is:

```text
INDEX_HIT
!= SEMANTIC AUTHORITY

OBJECT_LOCATOR
!= PRODUCER SEMANTIC IDENTITY

STRUCTURAL PRIOR
!= GENERATED RUNTIME FACT
!= ACTOR HISTORY
!= ACTOR KNOWLEDGE

GEOGRAPHY
!= GENERATED POSITION
!= ACTOR IDENTITY

TEMPORAL PROXY
!= DIRECT SUPPORT
!= HISTORICAL OBSERVATION AT QUERY TIME
!= LIVED HISTORY

NEGATIVE / LIMIT AUTHORITY
!= FALSE
!= ZERO
!= MISSING

UNKNOWN / MISSING / UNBOUND
!= DEFAULT
!= MOST LIKELY
!= NEUTRAL

RESOLVER SELECTION
!= PRODUCER RELATION CREATION
!= ACTOR EVENT
!= ACTOR EXPERIENCE
```

No score, semantic similarity, nearest-time rule, nearest-geography rule,
lexicographic tie-break, wall clock, mutable `latest`, filesystem order,
network lookup, raw-stage lookup, RNG or LLM/model judgment can change semantic
resolution.

---

## 1. Governing authority and scope court

### 1.1 Direct governing law inspected

At exact launch base `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`, this cell directly inspected:

- `BATCH_02_LAUNCH_REGISTER.md`, common law and W2-B02-02 only;
- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/W2_FIRST_BATCH_ADJUDICATION_RULING.md`;
- accepted `ADP-006 / RA-MUST-006-TEMPORAL-PROXY-ELIGIBILITY@1.0.0`;
- accepted `CAN-006 / V3_GENERATED_POSITION_BINDING_CONTRACT@1.0.0`;
- accepted `CAN-003 / CAN_003_V557_RUNTIME_USE`;
- SI-R05 V558→V3 seam result;
- RA-R00 release synthesis and V558 packet dependency ledger;
- current `ddm_v558_runtime_input_gate.py`;
- current `ddm_v558_plus_governance.py`.

No Batch-02 sibling result was consumed.

No historical ZIP was authorized or used.

### 1.2 Current implementation terrain disposition

The checked-in V558 modules are review/readiness/normalization terrain for an
earlier runtime-graft path. They do not implement the accepted immutable
mixed-producer repository or deterministic `ContextResolver`.

Their useful fail-closed presence/hash/status habits may be retained during
future implementation only where compatible.

Their `utc_now()` / `created_at` / `normalized_at` fields are **audit metadata
only**. Hidden current time is categorically excluded from CAN-005 query,
selection, policy identity and replay semantics.

Current implementation status therefore remains:

`SUPERSEDED_IMPLEMENTATION_TERRAIN__NO_CAN_005_SEMANTIC_AUTHORITY`.

---

## 2. Exact jurisdiction

CAN-005 owns exactly:

1. `V558_CONTEXT_RESOLVER_POLICY` identity, version and immutable content hash;
2. `ContextQuery` interpretation and validation;
3. logical index-family use and index-to-object verification law;
4. deterministic candidate discovery under exact query scope;
5. query-relative permission narrowing beneath producer and CAN-003 ceilings;
6. temporal rank application while delegating proxy eligibility to ADP-006;
7. native geographic filtering without proximity inference;
8. finite-stratum and Absolute-Horizon query filtering without identity inference;
9. generated-position requirement evaluation only through exact CAN-006 bindings;
10. preservation/application of producer negative, limit, missing, unknown,
    noncomparability and valid-empty authority;
11. equal-rank ambiguity and lawful multiplicity handling;
12. deterministic `SelectionRecord` production for every considered candidate;
13. deterministic query/resolution receipt identity;
14. provenance and replay requirements;
15. fail-closed policy/query/index/authority/integrity states.

CAN-005 does **not** own:

- V557 publication or repository bundle construction semantics (`CAN-004` remains
  separate and this sibling result was not consumed);
- temporal-proxy eligibility (`ADP-006`);
- generated-position production or binding semantics (`ADP-009` / `CAN-006`);
- static-vs-generated refresh trigger semantics (`CAN-007`);
- producer object meaning, predicates, evaluators or semantic relations;
- geography ontology or geographic hierarchy creation;
- finite-stratum ontology or Absolute-Horizon semantics;
- actor positions, relationships, households, genealogy, history, memory,
  knowledge, personality or attractors;
- V3 causal admission or V2 rendering;
- physical index/storage/database implementation.

---

## 3. Policy identity, version and hash

Canonical policy:

```text
policy_id      = V558_CONTEXT_RESOLVER_POLICY
policy_version = 1.0.0
policy_hash    = 4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f
```

The canonical policy hash is:

```text
SHA256(
  UTF8(
    canonical_json(
      policy_semantic_payload_without_policy_hash
    )
  )
)
```

Canonical JSON means sorted field names, no insignificant whitespace and stable
UTF-8 serialization. Array order is semantic only where this authority declares
order semantic, including temporal precedence. Unordered reference arrays must
use canonical content ordering for hashing; that ordering never creates semantic
precedence.

The policy semantic payload binds:

- accepted query-purpose vocabulary;
- `ContextQuery` schema version;
- logical index-contract version;
- temporal rank order;
- tie/multiplicity law;
- permission monotonicity;
- geographic/stratal/position/negative non-inference law;
- SelectionRecord schema version;
- resolution-receipt schema version;
- forbidden nondeterminism set;
- accepted dependency authority versions.

A query that omits policy identity/version/hash is invalid.

A policy ID/version with a different hash is:

`RESOLVER_POLICY_HASH_MISMATCH`.

An unknown policy version is:

`RESOLVER_POLICY_VERSION_UNBOUND`.

There is no implementation-default policy and no implicit `latest` policy.

---

## 4. `V558_CONTEXT_QUERY@1.0.0`

A query is an immutable semantic request envelope.

```text
V558ContextQuery {
  context_query_id,
  context_query_schema_version,

  repository_bundle_id,
  repository_content_hash,
  repository_index_manifest_ref,
  repository_index_manifest_hash,

  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  query_purpose,
  requested_use_class,

  generation_subject_ref | null,
  actor_id | null,

  query_time,
  query_time_granularity,

  requested_semantic_resolution_keys[],
  requested_producer_collection_refs[],

  native_geography_scope_refs[],
  finite_stratum_filter_refs[],
  absolute_horizon_filter_refs[],

  generated_position_binding_set_ref | null,
  generated_position_binding_set_hash | null,

  phase_a_context_ref | null,
  phase_a_context_hash | null,

  replay_selection_record_refs_and_hashes[],

  provenance_refs[],
  context_query_hash
}
```

### 4.1 Query identity

`context_query_hash` is SHA256 of canonical semantic query fields.

`context_query_id` is content-addressed from schema identity plus query hash:

```text
context_query_id =
SHA256(
  "V558_CONTEXT_QUERY_V1"
  || context_query_hash
)
```

Display strings, file paths, wall clock, database row order and mutable aliases
are never query identity.

### 4.2 Accepted query purposes

CAN-005 v1 accepts only already-governed purposes:

- `STRUCTURAL_CONTEXT_PHASE_A`;
- `STRUCTURAL_CONTEXT_PHASE_B`;
- `STRUCTURAL_CONTEXT_REFRESH`;
- `REPLAY_AUDIT_EXPLANATION`.

Unknown/ad-hoc/debug purpose tokens fail closed as:

`UNBOUND_CONTEXT_QUERY_PURPOSE`.

CAN-005 does not define what causes a refresh query. That remains CAN-007.

`REPLAY_AUDIT_EXPLANATION` may reproduce an earlier resolution against its exact
historical bundle/query/policy/binding lineage. It may not make a new proxy
decision or silently resolve against newer repository material.

### 4.3 Requested use class

The query carries exactly one requested use class from the accepted CAN-003
allowed-use representation:

- `ACTIVE_CAUSAL`;
- `CONTEXT`;
- `REVIEW`.

The resolver may only narrow:

```text
producer allowed uses
⊇ V557 CAN-003 allowed uses
⊇ resolver query-relative allowed uses
```

A context-only object cannot become active-causal because the query requests it.
A review-only object cannot enter ordinary V3 structural context.

### 4.4 Semantic request identity

`requested_semantic_resolution_keys[]` and
`requested_producer_collection_refs[]` contain exact producer-owned identities
or repository-preserved exact refs.

The resolver does not invent semantic keys from labels, prose, embeddings,
column names or similarity.

Exact same display label with distinct producer semantic refs remains distinct.

An empty explicit semantic request is lawful:

`VALID_EMPTY_CONTEXT_QUERY_REQUEST`.

It does not authorize a scan for “something relevant.”

---

## 5. Logical index contract

### 5.1 Index families

The accepted V558 architecture requires stage-agnostic logical indexes. CAN-005
binds the policy use of exactly these resolver-facing index families:

1. `TEMPORAL`;
2. `GEOGRAPHIC`;
3. `FINITE_STRATUM`;
4. `GENERATED_POSITION_REQUIREMENT`;
5. `NEGATIVE_LIMIT`;
6. `PROVENANCE`.

The immutable repository also retains its collection registry, producer-preserving
ObjectLocators and mixed-producer reference graph. Those are repository
substrate, not new semantic index authority.

Physical storage layout, database technology and query engine are implementation
choices.

### 5.2 `V558_LOGICAL_INDEX_CONTRACT@1.0.0`

Each logical index family exposed to this policy must have a manifest record
equivalent to:

```text
V558LogicalIndexRecord {
  repository_bundle_id,
  repository_content_hash,

  index_family,
  index_schema_version,
  index_content_hash,
  completeness_state,

  exact_key_contract_ref,
  indexed_object_locator_refs[],
  indexed_authoritative_object_refs_and_hashes[],

  build_provenance_refs[],
  integrity_state
}
```

`completeness_state` must positively attest that the index was built against
the exact immutable repository content claimed by the query. A partial index
cannot masquerade as a complete candidate universe.

### 5.3 Indexes are nonsemantic accelerators

An index hit means only:

> this exact repository locator is a candidate for further policy evaluation.

It does **not** mean:

- temporal applicability;
- geographic applicability;
- permission;
- predicate satisfaction;
- actor position;
- relationship;
- causal relevance;
- winner status.

Every index-produced locator must dereference to an exact repository object and
verify authoritative ID/hash before semantic use.

### 5.4 No fuzzy index path

Forbidden discovery mechanisms include:

- nearest timestamp;
- nearest geography;
- prefix/substring semantic matching;
- embedding/LLM similarity;
- score rank;
- “most common” object;
- first filesystem/database row;
- mutable latest object;
- fallback raw-stage/network search.

CAN-005 v1 authorizes no semantic fallback from a missing/corrupt required
index to fuzzy lookup.

A missing, stale or incomplete required index is:

`REPOSITORY_INDEX_INTEGRITY_FAILURE`.

It is not a valid-empty semantic result.

Exact duplicate locator entries with the same authoritative object ID and hash
may deduplicate for serialization. Same semantic object ID with a different hash
is an integrity failure.

---

## 6. Canonical candidate discovery

For each exact requested semantic resolution key:

1. validate repository bundle/content hash;
2. validate policy identity/version/hash;
3. validate ContextQuery hash;
4. validate required logical-index manifest identities/hashes;
5. discover candidate locators through exact logical index keys;
6. dereference every locator to its immutable producer-preserving object;
7. verify producer object ID/hash/schema/reference closure and CAN-003 governance;
8. preserve producer epistemic/negative/missing/noncomparability/valid-empty state;
9. apply exact query scope and producer-governed conditions;
10. apply temporal precedence;
11. apply equal-rank/multiplicity law;
12. emit a SelectionRecord for every considered candidate.

The resolver may narrow the candidate universe. It may never invent a new
candidate object.

A producer dependency reached through the repository reference graph is
dereferenced by exact reference. It is not semantically copied into the
dependent object.

---

## 7. Permission and epistemic law

### 7.1 Integrity before semantics

Identity/hash/schema/reference-closure corruption is:

`INTEGRITY_FAILURE`.

It never becomes:

- missing authority;
- negative authority;
- not-applicable;
- false;
- zero;
- valid-empty.

### 7.2 Producer and CAN-003 ceiling

Resolver active-causal selection requires that exact producer permission and
CAN-003 item-use governance both permit active-causal use.

`ALLOW_CONTEXT_ONLY` may be visible only for a compatible `CONTEXT` request.
It cannot become active causal.

`ALLOW_REVIEW_ONLY` is restricted to compatible review/audit use.

`DENY_CAUSAL_USE` and `NOT_APPLICABLE` remain distinct and are preserved.

### 7.3 Query-relative narrowing

The resolver may further narrow because of:

- query purpose;
- query time;
- native geography;
- exact stratum filter;
- required generated-position binding;
- producer predicate/condition result;
- negative/limit authority;
- temporal-anchor result.

It cannot widen permission because another candidate is absent.

### 7.4 Epistemic classes

Producer/repository epistemic class remains preserved.

A resolver result is `RESOLVER_DERIVED_CONTEXT`, referring to exact source /
structural / negative objects.

A CAN-006 position binding may be echoed only as
`GENERATED_RUNTIME_FACT_REF`.

The resolver does not convert producer evidence into actor knowledge or
generated history.

---

## 8. Temporal selection law

### 8.1 Resolution is per semantic key

Temporal ranking operates only among candidates for the same exact
producer-governed semantic resolution key.

Different pressures, routes, relation participants or semantic keys do not
become competitors merely because their support times coincide.

### 8.2 Rank 1 — direct support

`DIRECT_TEMPORAL_SUPPORT` is available only when producer-governed support
actually contains the query time at the declared compatible granularity.

A point observation is not an interval.

A later/earlier observation cannot be promoted to direct support because it is
nearby.

If one or more lawful direct candidates exist, lower temporal ranks are not
considered as winners for that semantic key.

### 8.3 Rank 2 — authorized latest prior

Only after no direct-support winner exists may ADP-006-authorized prior
candidates be considered.

Proxy eligibility is evaluated by exact ADP-006 authority/rule version.

Among eligible prior observations for the same key, the temporal target is the
greatest lawful observation reference time strictly before query time.

This is **LATEST_PRIOR**, not nearest absolute time.

If multiple nonidentical candidates occupy that same latest-prior rank/time,
apply the tie/multiplicity law in §13.

### 8.4 Rank 3 — authorized earliest post

Only after no direct-support winner and no lawful latest-prior winner exist may
ADP-006-authorized forward candidates be considered.

The ordinary rule is ADP-006's precoverage-only earliest-post authority.

Among eligible post observations, the temporal target is the least lawful
observation reference time strictly after query time.

This is **EARLIEST_POST**, not nearest absolute time.

`EARLIEST_POST_BIRTH_ANCHOR` is only the accepted reporting specialization. It
does not create a fifth precedence rank.

### 8.5 Rank 4 — no lawful anchor

If no direct, prior or post candidate is lawfully selectable:

`NO_LAWFUL_TEMPORAL_ANCHOR`.

No interpolation, default value, nearest wave or model estimate is substituted.

### 8.6 Future proxy truth conditions

Every future proxy SelectionRecord preserves:

- actual evidence/reference time;
- positive signed lag under ADP-006 convention;
- exact proxy rule/version;
- `historical_observation_at_query_time = false`;
- `future_evidence_used_as_proxy = true`.

A future proxy remains structural context/explanatory prior at the earlier query
time. It is not evidence that the future observation had already happened, was
already true as a lived actor event, or was actor-known.

---

## 9. Geographic policy

The resolver enforces **native producer geography**.

A candidate may match query geography only through:

1. an exact shared governed geography ref; or
2. an exact producer-owned geographic applicability/containment relation already
   preserved in the repository and applicable to the requested use.

CAN-005 creates no geography relation.

Forbidden:

- nearest city/region/country;
- geographic centroid distance;
- neighboring-region fallback;
- label similarity;
- country → class/sect/party/household/family;
- geography → generated position;
- geography → actor identity/psyche.

If an object requires a geographic binding and the query supplies none:

`MISSING_REQUIRED_GEOGRAPHIC_BINDING`.

If supplied geography is outside the producer-governed scope:

`GEOGRAPHIC_SCOPE_NOT_APPLICABLE`.

This is not evidence that the represented condition is false everywhere.

---

## 10. Finite-stratum and Absolute-Horizon policy

Finite-stratum filters operate only against exact producer-preserved stratum
refs.

No numeric stratum distance or hierarchy score exists.

An empty `finite_stratum_filter_refs[]` means **no additional query narrowing by
stratum**. It does not assert that the object has no stratum.

Absolute Horizon remains distinct and uses
`absolute_horizon_filter_refs[]`. It is never folded into the nine finite
strata or treated as stratum 10.

A stratum ref may select structural material. It may not create actor
identification, alienation, belief, class consciousness, morality, personality
or generated position.

Different simultaneously applicable strata and pressures remain separate
resolved objects unless producer semantics explicitly relate them.

---

## 11. Generated-position policy

Generated structural position is not inferred inside CAN-005.

Position-conditioned producer material uses only exact
`V3_GENERATED_POSITION_BINDING@1.0.0` / binding-set identity from accepted
CAN-006.

Rules:

- zero generated-position bindings is lawful in Phase A;
- if a candidate requires a generated position and no exact binding is present,
  emit/defer as `UNBOUND_REQUIRES_RUNTIME_POSITION`;
- binding actor/subject mismatch propagates CAN-006 failure;
- stale/superseded binding propagates CAN-006 failure;
- binding-key mismatch does not trigger fuzzy rematching;
- exact explicit-position-absence assertion remains explicit absence according
  to producer/CAN-006 semantics;
- resolver may evaluate only already-governed position predicates;
- resolver never runs ADP-009 candidate selection or constructs a position.

A geography-only attempt to satisfy a position requirement is:

`FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE`.

A temporal-proxy attempt to satisfy a position requirement is:

`FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE`.

CAN-005 does not define Phase-A→Phase-B refresh triggering. It only consumes the
query once lawfully formed.

---

## 12. Negative, limit, unknown, missing and valid-empty law

### 12.1 Negative / limit authority

Producer negative or limit objects remain
`NEGATIVE_OR_LIMIT_AUTHORITY`.

They may block/narrow a candidate only within the exact scope declared by their
producer semantics.

A key/use-scoped denial cannot be bypassed by selecting another observation for
that same prohibited scope.

A negative object scoped to key A cannot silently deny key B.

Generic negative metadata that does not govern the requested use is preserved
as context; CAN-005 does not enlarge its blocking scope.

### 12.2 Unknown

Producer unknown remains unknown.

Unknown is not false, zero, neutral, missing or a request to choose a plausible
value.

### 12.3 Missing authority

If an evaluator, permission, proxy rule, binding authority or indispensable
producer authority required for selection is absent:

`MISSING_REQUIRED_RESOLUTION_AUTHORITY`
or a narrower recorded subtype.

No candidate is invented.

### 12.4 Noncomparability

Producer `NONCOMPARABLE` remains noncomparable. The resolver does not average or
order it.

### 12.5 Valid-empty

A producer-governed valid-empty collection/state is preserved as a successful
typed empty.

A valid-empty result is never synthesized merely because an index returned no
candidate.

No candidate because of missing/corrupt authority is not valid-empty.

### 12.6 Explicit zero

An exact producer observation whose lawful semantic value is numeric zero
remains an observation. Zero is not missingness.

---

## 13. Equal-rank ties and lawful multiplicity

Tie handling applies only after all higher-order permission, scope, condition
and temporal-rank filtering.

### 13.1 Exact duplicates

Same authoritative semantic object ID **and** same authoritative content hash
may deduplicate for serialization/audit.

Same ID with different hash is:

`AUTHORITATIVE_OBJECT_IDENTITY_CONFLICT`.

### 13.2 Lawful multiplicity

When exact producer/reference-contract authority explicitly permits multiple
equal-rank results for the resolution operation:

- return the **full tied set**;
- preserve every producer object ID/hash;
- preserve every SelectionRecord;
- canonical sort only for serialization/hash stability;
- do not synthesize an aggregate object.

Result state:

`LAWFUL_EQUAL_RANK_MULTIPLICITY`.

### 13.3 Singular resolution

When one semantic winner is required and multiple nonidentical equal-rank
candidates remain without exact producer-governed precedence:

`AMBIGUOUS_EQUAL_RANK_AUTHORITY`.

No candidate is activated as the winner.

Forbidden tie breakers:

- averaging;
- weighted averaging;
- score;
- confidence total;
- semantic similarity;
- embedding distance;
- lexicographic ID;
- first row;
- source filename;
- producer stage number;
- most recent build;
- model judgment.

### 13.4 Contradiction is not automatically a tie

Two objects representing different semantic keys, participants, directed
relations or simultaneous pressure streams remain separate.

The resolver does not force them into one resolution court merely to simplify
downstream state.

---

## 14. Producer predicates and dependent objects

The resolver may evaluate only a predicate/condition whose exact producer-owned
identity, evaluator authority/version/hash and input contract are already
present and authorized.

Missing evaluator authority yields:

`DEFERRED_MISSING_PRODUCER_EVALUATOR`.

The resolver cannot replace it with a heuristic.

For dependent V554/V555/V556 objects:

- all indispensable exact temporal dependencies must resolve lawfully;
- all required generated bindings must be available;
- producer conditions must evaluate under their own contracts;
- item permission must remain lawful.

If an indispensable temporal dependency has no lawful anchor, the dependent
object is deferred/excluded according to its producer condition semantics.

The resolver never “proxies the route,” “proxies the interaction,” or “proxies
the F2 topology” as a shortcut.

Co-resolving the participants of a V556 relation does not create a new V556
relation/topology.

---

## 15. `V558_SELECTION_RECORD@1.0.0`

Every considered candidate receives one immutable SelectionRecord, including
selected, rejected, denied, deferred, ambiguous and integrity-failed candidates.

```text
V558SelectionRecord {
  selection_record_id,
  selection_record_schema_version,

  repository_bundle_id,
  repository_content_hash,
  repository_index_manifest_hash,

  context_query_id,
  context_query_hash,

  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  query_purpose,
  requested_use_class,
  semantic_resolution_key_ref,

  candidate_object_locator_ref,
  authoritative_producer_object_ref,
  authoritative_producer_object_hash,
  producer_family,
  producer_collection_ref,
  producer_authority_refs_and_versions[],

  index_family_witness_refs_and_hashes[],

  producer_permission_state,
  v557_can003_item_use_state,
  resolver_query_relative_use_state,
  epistemic_class,
  producer_exception_state,

  query_time,
  query_time_granularity,
  producer_evidence_time_or_support_ref,
  temporal_rank,
  temporal_resolution_mode,
  temporal_proxy_authority_ref | null,
  temporal_proxy_rule_ref | null,
  signed_lag | null,
  historical_observation_at_query_time | null,
  future_evidence_used_as_proxy | null,

  query_geography_refs[],
  candidate_geography_refs[],
  geography_match_authority_refs[],

  query_finite_stratum_filter_refs[],
  candidate_finite_stratum_refs[],
  query_absolute_horizon_filter_refs[],
  candidate_absolute_horizon_refs[],

  generated_position_binding_refs_and_hashes[],
  producer_predicate_refs_and_versions[],
  predicate_evaluation_receipts[],

  negative_or_limit_refs[],
  unknown_missing_noncomparability_refs[],

  tie_group_id | null,
  equal_rank_count,
  multiplicity_authority_ref | null,

  decision_state,
  decision_reason_codes[],
  provenance_refs[],
  selection_record_hash
}
```

### 15.1 Record identity

```text
selection_record_hash =
SHA256(canonical_json(selection_record_semantic_fields))

selection_record_id =
SHA256(
  "V558_SELECTION_RECORD_V1"
  || selection_record_hash
)
```

No generated timestamp participates.

### 15.2 Decision states

Canonical SelectionRecord states include:

- `SELECTED_DIRECT_TEMPORAL_SUPPORT`;
- `SELECTED_AUTHORIZED_LATEST_PRIOR`;
- `SELECTED_AUTHORIZED_EARLIEST_POST`;
- `SELECTED_NON_TEMPORAL_APPLICABLE`;
- `LAWFUL_EQUAL_RANK_MULTIPLICITY_MEMBER`;
- `REJECTED_HIGHER_TEMPORAL_RANK_EXISTS`;
- `REJECTED_PROXY_NOT_AUTHORIZED`;
- `REJECTED_PERMISSION_CEILING`;
- `REJECTED_GEOGRAPHIC_SCOPE`;
- `REJECTED_STRATUM_FILTER`;
- `DEFERRED_UNBOUND_GENERATED_POSITION`;
- `DEFERRED_MISSING_PRODUCER_EVALUATOR`;
- `NO_LAWFUL_TEMPORAL_ANCHOR`;
- `NEGATIVE_OR_LIMIT_AUTHORITY_PRESERVED`;
- `UNKNOWN_AUTHORITY_PRESERVED`;
- `NONCOMPARABLE_PRESERVED`;
- `VALID_EMPTY_PRODUCER_STATE_PRESERVED`;
- `AMBIGUOUS_EQUAL_RANK_AUTHORITY`;
- `INTEGRITY_FAILED`.

These states are resolver audit/decision states. They do not redefine producer
domain semantics.

---

## 16. `V558_CONTEXT_RESOLUTION_RECEIPT@1.0.0`

CAN-005 binds a compact deterministic receipt for one completed resolver call.

```text
V558ContextResolutionReceipt {
  resolution_receipt_id,
  resolution_receipt_schema_version,

  repository_bundle_id,
  repository_content_hash,
  repository_index_manifest_hash,

  context_query_id,
  context_query_hash,

  resolver_policy_id,
  resolver_policy_version,
  resolver_policy_hash,

  selected_object_refs_and_hashes[],
  selected_selection_record_refs_and_hashes[],
  deferred_selection_record_refs_and_hashes[],
  ambiguous_selection_record_refs_and_hashes[],
  denied_negative_integrity_record_refs_and_hashes[],

  generated_position_binding_set_ref | null,
  generated_position_binding_set_hash | null,

  result_state,
  resolved_structural_context_ref | null,
  resolved_structural_context_hash | null,

  provenance_refs[],
  resolution_receipt_hash
}
```

The receipt does not own the complete `ResolvedStructuralContext` schema and
does not define CAN-007 refresh metadata.

Result states:

- `RESOLUTION_COMPLETE`;
- `RESOLUTION_COMPLETE_VALID_EMPTY`;
- `RESOLUTION_COMPLETE_WITH_LAWFUL_MULTIPLICITY`;
- `RESOLUTION_PARTIAL_TYPED_DEFERRED`;
- `RESOLUTION_AMBIGUOUS_EQUAL_RANK`;
- `RESOLUTION_DENIED_OR_NOT_APPLICABLE`;
- `RESOLUTION_NO_LAWFUL_TEMPORAL_ANCHOR`;
- `RESOLUTION_MISSING_REQUIRED_AUTHORITY`;
- `RESOLUTION_INTEGRITY_FAILED`;
- `REPLAY_RESOLUTION_REPRODUCED`.

A mixed query may retain successfully resolved keys while separately exposing
typed deferred/negative/ambiguous keys. The receipt must never make the context
look complete by filling unresolved keys.

---

## 17. Replay and provenance

A complete CAN-005 replay binds:

- immutable repository bundle ID and content hash;
- repository index manifest identity/hash;
- exact policy ID/version/hash;
- `ContextQuery` ID/hash;
- exact query purpose/use/time/granularity;
- exact semantic resolution key refs;
- exact geography/stratum/Horizon refs;
- exact CAN-006 generated-position bindings where supplied;
- producer object IDs/hashes and transitive refs;
- producer permission / CAN-003 governance refs;
- producer predicate/evaluator refs and receipts;
- ADP-006 authority/rule/version and lag data where proxying occurred;
- negative/limit/noncomparability refs;
- tie/multiplicity authority refs;
- every SelectionRecord ID/hash;
- resolution receipt ID/hash;
- resolved-context hash/ref where materialized.

Identical immutable inputs reproduce identical semantic result sets, decision
states, SelectionRecord hashes and resolution receipt hash.

Forbidden replay inputs:

- current wall-clock time;
- mutable `latest`;
- filesystem/database iteration order;
- process/thread order;
- network state;
- raw V553–V556 stage directories;
- random state;
- LLM/model/embedding output;
- unrecorded cache contents;
- display labels;
- implementation-default policy.

A physical cache may accelerate an exact lookup only if its returned object set
is identical to the canonical repository/index result and every object is
reverified. Cache state itself is never authority.

---

## 18. Compatibility disposition

Current/superseded V558 review-gate mechanics are classified:

| Recovered/current mechanism | CAN-005 disposition |
|---|---|
| presence/version/hash fail-closed checks | `ADAPT_AS_IMPLEMENTATION_MECHANICS` |
| immutable/stale-safe artifact habits | `ADAPT` |
| global readiness/status fields | `AUDIT_ONLY__NEVER_ITEM_SELECTION_AUTHORITY` |
| normalized runtime-input object | `REPLACE_WITH_ACCEPTED_REPOSITORY_QUERY_CONTRACT` |
| prompt/render governance | `OUT_OF_CAN_005_SCOPE` |
| `utc_now()` timestamps | `AUDIT_ONLY__FORBIDDEN_IN_SEMANTIC_IDENTITY` |
| review/graft readiness statuses | `SUPERSEDED_FOR_CONTEXTRESOLVER_SEMANTICS` |
| row/file ordering | `SERIALIZATION_OR_IMPLEMENTATION_ONLY` |
| any score/nearest/fuzzy convenience | `FORBIDDEN` |

No current implementation vocabulary is promoted merely because it already
exists.

---

## 19. Fail-closed state summary

Canonical query/policy/integrity failures:

- `RESOLVER_POLICY_VERSION_UNBOUND`;
- `RESOLVER_POLICY_HASH_MISMATCH`;
- `CONTEXT_QUERY_HASH_MISMATCH`;
- `REPOSITORY_IDENTITY_MISMATCH`;
- `REPOSITORY_CONTENT_INTEGRITY_FAILURE`;
- `REPOSITORY_INDEX_INTEGRITY_FAILURE`;
- `UNBOUND_CONTEXT_QUERY_PURPOSE`;
- `MISSING_REQUIRED_QUERY_INPUT`;
- `MISSING_REQUIRED_GEOGRAPHIC_BINDING`;
- `MISSING_REQUIRED_RESOLUTION_AUTHORITY`;
- `DEFERRED_MISSING_PRODUCER_EVALUATOR`;
- `UNBOUND_REQUIRES_RUNTIME_POSITION`;
- CAN-006 generated-position failure states;
- `FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE`;
- `FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE`;
- `NO_LAWFUL_TEMPORAL_ANCHOR`;
- `AMBIGUOUS_EQUAL_RANK_AUTHORITY`;
- `AUTHORITATIVE_OBJECT_IDENTITY_CONFLICT`;
- `FORBIDDEN_RESOLVER_SEMANTIC_INFERENCE`;
- `FORBIDDEN_NONDETERMINISTIC_RESOLUTION_INPUT`;
- `INTEGRITY_FAILURE`.

None may be repaired with zero, false, midpoint, average, first-row,
nearest-time, nearest-geography or model output.

---

## 20. Hostile fixture court

| ID | Attack | Required outcome |
|---|---|---|
| H005-01 | direct-support candidate and closer prior proxy both exist | direct wins; proxy rejected because higher temporal rank exists |
| H005-02 | no direct; lawful latest-prior and earlier prior exist | latest lawful prior wins |
| H005-03 | no direct/prior; lawful earliest-post and later post exist | earliest lawful post wins |
| H005-04 | future observation is chronologically closer than lawful prior | prior still outranks post |
| H005-05 | post observation exists but ADP-006 forward proxy is unauthorized | `REJECTED_PROXY_NOT_AUTHORIZED`; no anchor/fallback |
| H005-06 | prior observation exists but query purpose not ADP-006 eligible | no proxy selection |
| H005-07 | point observation near query time | cannot become direct interval support |
| H005-08 | future proxy selected | actual future evidence time preserved; `historical_observation_at_query_time=false` |
| H005-09 | no lawful direct/prior/post anchor | `NO_LAWFUL_TEMPORAL_ANCHOR`; no default |
| H005-10 | two incompatible direct candidates for singular key | `AMBIGUOUS_EQUAL_RANK_AUTHORITY` |
| H005-11 | two equal-rank candidates with producer-authorized multiplicity | return full tied set |
| H005-12 | tie candidates differ only by list order | identical canonical result |
| H005-13 | lexicographically smaller candidate conflicts with other candidate | lexicographic order cannot choose winner |
| H005-14 | resolver score/confidence favors one equal-rank candidate | score ignored/rejected as authority |
| H005-15 | embedding/LLM similarity offered as tie-break | reject |
| H005-16 | exact duplicate same ID/hash appears twice in index | deduplicate serialization only |
| H005-17 | same authoritative ID appears with two hashes | integrity failure |
| H005-18 | required logical index missing/incomplete | `REPOSITORY_INDEX_INTEGRITY_FAILURE`; not valid-empty |
| H005-19 | index hit claims candidate but object dereference/hash fails | integrity failure |
| H005-20 | index score orders candidates | score has no semantic effect |
| H005-21 | nearest geography suggested when exact native scope absent | reject nearest-geography fallback |
| H005-22 | geography-only query attempts to infer actor class/sect/party | `FORBIDDEN_GEOGRAPHY_TO_POSITION_INFERENCE` |
| H005-23 | query stratum ref used to infer actor identification/belief | reject semantic promotion |
| H005-24 | Absolute Horizon folded into finite-stratum filter | reject; preserve separate channel |
| H005-25 | position-conditioned object with no CAN-006 binding | `UNBOUND_REQUIRES_RUNTIME_POSITION` |
| H005-26 | CAN-006 binding actor/subject mismatch | propagate binding failure; no repair |
| H005-27 | stale/superseded CAN-006 binding | propagate stale failure |
| H005-28 | temporal proxy offered as generated position | `FORBIDDEN_TEMPORAL_PROXY_TO_POSITION_INFERENCE` |
| H005-29 | exact position binding yields no new applicable object | lawful typed empty delta; no filler |
| H005-30 | producer negative authority blocks proxy use for key A | key A candidate excluded/preserved under exact negative scope |
| H005-31 | negative authority for key A offered to deny unrelated key B | reject overbroad negative scope |
| H005-32 | producer unknown value | preserve unknown; no zero/false/default |
| H005-33 | producer noncomparability | preserve noncomparability; no ordering/average |
| H005-34 | producer valid-empty collection | preserve valid-empty as successful typed empty |
| H005-35 | empty index result with missing authority | missing/deferred, never synthesized valid-empty |
| H005-36 | CAN-003 context-only item requested as active causal | deny active use; no widening |
| H005-37 | globally READY collection contains item-level denial | item denial controls |
| H005-38 | dependent route/F1/F2 lacks indispensable temporal anchor | defer/exclude dependent object; never proxy the dependent object itself |
| H005-39 | V556 participant routes co-resolve but no V556 relation object exists | no new interaction/topology created |
| H005-40 | raw V553–V556 directory contains a tempting replacement object | resolver may not access it |
| H005-41 | network API returns newer object | ignore/forbid; immutable repository is sole source |
| H005-42 | wall clock changes between identical calls | result and hashes remain identical |
| H005-43 | filesystem/database order changes | result and hashes remain identical |
| H005-44 | mutable `latest` points to different bundle/policy | ignored; exact bound identity controls |
| H005-45 | policy version same but policy hash differs | `RESOLVER_POLICY_HASH_MISMATCH` |
| H005-46 | same bundle ID with different content hash | repository integrity failure |
| H005-47 | explicit empty semantic request | `VALID_EMPTY_CONTEXT_QUERY_REQUEST`; no relevance scan |
| H005-48 | `REPLAY_AUDIT_EXPLANATION` tries to create a new proxy selection | reject; replay only |
| H005-49 | same exact bundle/query/policy/bindings replayed | same selected refs, SelectionRecord hashes and receipt hash |
| H005-50 | Batch-02 sibling authority result offered to change policy | reject sibling authority consumption |

---

## 21. GOVERNING_SPIRIT_CHECK

**Status:** `NOT_APPLICABLE__HARD_AUTHORITY_UNIQUE`.

The material semantic choices are already fixed by accepted law:

- deterministic immutable repository resolution;
- exact producer-preserving refs;
- hard temporal precedence;
- ADP-006-owned proxy eligibility;
- CAN-006-owned generated-position binding;
- producer semantics remain producer-owned;
- equal-rank ambiguity unless multiplicity is independently lawful;
- missing/negative/noncomparability/valid-empty distinctions;
- no geography→identity or proxy→history laundering;
- no fuzzy/default/model nondeterminism.

The Governing Spirit was read as required and is fully compatible with that
result, especially its requirements to preserve contradiction/multiplicity,
lawful absence, provenance and non-invention. It was not needed to choose
between multiple lawful semantic policies and supplied no missing resolver
semantics.

---

## 22. CONSUMER_RELEASE_SUFFICIENCY

**Status:**
`SUFFICIENT_FOR_CAN_005_JURISDICTION__NO_PRODUCTION_RELEASE`.

CAN-005 is semantically sufficient for its exact RA-R00 consumers:

- `V558-P2` — logical temporal/geographic/stratal/position/negative/provenance
  index use contract;
- `V558-P3` — deterministic ContextResolver policy;
- `V558-P5` — exact stage-blind/raw-stage-absent replay court.

If accepted, this result closes the CAN-005 semantic blocker.

For `V558-P2`, accepted CAN-006 already closes the separately named
generated-position binding dependency, but physical V558 repository construction
and predecessor gates remain.

For `V558-P3`, accepted ADP-006 and CAN-006 already close the other named direct
semantic dependencies, but V558-P1/P2 implementation and physical predecessor
gates remain.

`V558-P5` still requires the actual completed V558 implementation/court before
it can create `EXT-007`.

This result does not consume or close sibling Batch-02 CAN-004 or CAN-007:

- CAN-004 remains responsible for immutable publication/repository bundle policy;
- CAN-007 remains responsible for static next-context-change versus
  generated-life requery triggers.

No V558 production implementation is released by this authority file.

---

## 23. Final token

`CAN_005_CONTEXT_RESOLVER_POLICY_BINDING_CANONICALIZATION = PASS`
