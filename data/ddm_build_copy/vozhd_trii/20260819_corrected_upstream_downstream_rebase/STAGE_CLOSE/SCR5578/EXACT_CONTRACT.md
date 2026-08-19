# SCR5578 Exact Contract — V557 Publication / V558 Standalone Repository / Context Resolution

**Contract:** `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION_EXACT_CONTRACT@1.0.0`  
**Exact common base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Machine contract:** `EXACT_CONTRACT.json`  
**Machine contract SHA-256:** `7522e3066ec7cd03de36faf065e089925e42356b4a6833d7420d00f6a139f88c`  
**Local status:** `CLOSED`  
**Final status:** `WAITING_ONLY_FOR_EXACT_FINAL_SEAM`

## 1. Logical authorities

V557 and V558 are logically distinct even when physically co-packaged.

**V557 owns:** runtime publication admission, producer-permission intake, item/collection use governance, monotone narrowing, immutable publication identity and interpretation-critical closure proof.

**V558 owns:** immutable `StructuralPriorRepository`, producer-preserving locators/reference graph, logical indexes, deterministic stage-blind `ContextResolver`, `SelectionRecord`s, resolution receipt, coverage/fidelity, refresh carrier metadata and `ResolvedStructuralContext`.

Neither owns V553/V554/V555/V556 domain semantics. Neither may create cross-source composition authority, actor state or expression semantics. No production implementation is authorized here.

## 2. Producer registry and final-seam placeholders

The direct publication-root producer families are exactly:

`V553 | V554 | V555 | V556`.

A producer object may publish directly to V557 only when the final accepted contract for that producer independently authorizes the exact object/use. Historical stage numbering does not require a no-op wrapper.

SCR5578 does **not** guess producer machine identities. M4 must bind, for each accepted SCR553/SCR554/SCR555/SCR556 return:

- exact accepted head SHA and result token;
- producer contract ID/version/hash;
- object and collection schema IDs/versions;
- canonical producer identity tuple and hash law;
- producer permission ceiling;
- typed positive/negative/valid-empty/missing/noncomparable/integrity states;
- exact producer reference-contract IDs/versions/hashes;
- producer-owned role/cardinality/multiplicity/order semantics;
- direct V557 publication eligibility;
- producer build/schema/compiler replay identity.

Before those exact bindings exist: `PRODUCER_FINAL_CONTRACT_UNBOUND`.

## 3. Permission contract

Use atoms are:

`REVIEW`, `CONTEXT`, `ACTIVE_CAUSAL`.

State expansion:

| State | Allowed uses |
|---|---|
| `ALLOW_ACTIVE_CAUSAL_CONTEXT` | `REVIEW, CONTEXT, ACTIVE_CAUSAL` |
| `ALLOW_CONTEXT_ONLY` | `REVIEW, CONTEXT` |
| `ALLOW_REVIEW_ONLY` | `REVIEW` |
| `DENY_CAUSAL_USE` | none |
| `NOT_APPLICABLE` | none |

For every item and every resolver candidate:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`.

Enforcement is item-wise. Repository presence, collection/global readiness, index membership, locator existence, root activity or dependency reachability never grants permission. A dependency retains its own permission state and never inherits its root's use state.

Missing or ambiguous producer permission fails closed. Any V557 or resolver widening attempt is `INTEGRITY_FAILURE__FORBIDDEN_PERMISSION_WIDENING`.

## 4. V557 object and collection records

`SCR5578_RUNTIME_AUTHORIZED_OBJECT_RECORD@1.0.0` binds:

- V557 governance record ID/hash and authority ID/version;
- producer family/collection kind;
- canonical producer object ID/hash;
- producer build ID/hash;
- producer schema ID/version/compiler;
- producer rule/predicate/reference-contract refs;
- exact producer permission input;
- V557 publication admission/use state/expanded allowed uses;
- epistemic class and governance exception state/subtype;
- negative/limit, noncomparability and uncertainty refs;
- closure audit ref;
- provenance refs;
- V557 rule and compatibility bindings.

The governance-record ID is nonsemantic. Producer object ID/hash remains canonical semantic identity.

`SCR5578_RUNTIME_AUTHORIZED_COLLECTION_MANIFEST@1.0.0` binds producer collection/build/schema identity, exact object count, collection state and valid-empty subtype, all governance-record/state counts, closure ref/hash, V557 authority and registry bindings.

Collection states are `VALID_NONEMPTY`, `VALID_EMPTY`, `INVALID_FAIL_CLOSED`. A valid-empty collection creates no filler object and grants no item permission.

## 5. Corrected reference-class contract

### Root candidates

Only exact bound V553/V554/V555/V556 producer objects.

### Interpretation-critical reference-only

Only when an exact producer schema/reference contract declares the dependency interpretation-critical:

- `StructuralEmpiricalAdmission`;
- `EmpiricalFact`;
- QuerySpec;
- source UniverseSpec/risk set;
- measure/weight/estimand authority;
- historical producer/rule/predicate/authority snapshots;
- temporal, negative, limit and uncertainty authority;
- operation-specific source-composition authority.

Their original upstream owners remain authoritative.

`DiscoveryResultReceipt` is audit/provenance-only. `ReplayReceipt` is audit/replay-only and never a runtime structural prior.

### `MUST_NOT_APPEAR`

Reject from V557/V558 structural publication/repository:

- `ActorComparatorReceipt`;
- `PositionedSubjectEmpiricalPossibilityField` / PSEPF;
- `V3EmpiricalPossibilityInput`;
- rendered expression/persona objects.

PSEPF remains on the separate direct thin V3 lane.

## 6. Immutable V557/V558 bundles

V557 publication schema: `SCR5578_V557_IMMUTABLE_PUBLICATION_BUNDLE@1.0.0`.

ID: `V557PUB:<publication_identity_hash>`.

V558 repository schema: `SCR5578_V558_STRUCTURAL_PRIOR_REPOSITORY_BUNDLE@1.0.0`.

ID: `V558REPO:<repository_identity_hash>`.

Both use deterministic UTF-8 canonical JSON and SHA-256. Producer-declared semantic array order is preserved. Unordered arrays may sort only when producer/reference-contract authority declares order insignificant.

Any bound content, identity, governance or policy change creates a new immutable ID. In-place mutation and mutable `latest/current/default` identity are forbidden. Partial publication/repository visibility is forbidden.

Publication binds item/collection governance, producer builds, closure manifest/root digests and immutable material/locators. Repository additionally binds source publication identity, locator registry, reference graph, indexes, fidelity/negative manifest, producer material and exact policies.

## 7. Producer-preserving locator

`SCR5578_PRODUCER_PRESERVING_OBJECT_LOCATOR@1.0.0` contains the authoritative producer family/object ID/hash/build ID/hash/schema ID/version, producer rule/predicate/reference-contract bindings, V557 governance ref/hash, content hash and exact storage/provenance locator.

The locator is nonsemantic and must reverse exactly to one authoritative producer tuple without text/fuzzy matching. Same bytes under distinct producer identities do not create semantic equivalence.

## 8. Reference graph and standalone closure

Closure scope is:

`PER_PUBLISHED_ROOT_ROLE_PRESERVING_TRANSITIVE_SEMANTIC_CLOSURE`.

The walker follows only interpretation-critical references declared by exact bound producer schema/reference contracts. Arbitrary prose/audit/provenance mentions are not closure edges.

Every edge preserves:

- source/target locator;
- reference-contract ID/version/hash;
- producer-authorized edge role;
- requiredness;
- participant role;
- declared cardinality;
- multiplicity key;
- order-significant flag;
- semantic ordinal.

SCR5578 packaging names never invent producer roles. N-ary objects remain n-ary. No dyadization, collapse, winner selection or relation reconstruction is permitted. Producer semantic order is distinct from serialization order.

A strong reference resolving to zero or incompatible multiple targets fails closed unless the exact producer contract authorizes multiplicity/noncomparability.

### Standalone theorem

The conformance fixture removes raw V553/V554/V555/V556 directories.

Every interpretation-critical **positive and negative** dependency must still resolve from:

1. packaged immutable content addressed by exact hash; or
2. a packaged immutable exact hash-bound locator/resolver contract binding identity/version/hash and forbidding fuzzy/latest fallback.

ID alone, hash alone without a resolvable content contract, display label, provenance prose, current/latest authority and an external raw-stage path are insufficient.

Required closure may include, when the producer declares it interpretation-critical: producer authority snapshots; source universes/risk sets; QuerySpecs; measure/weight/estimand authority; admission lineage; temporal support/limits; typed negative/missing/noncomparability/valid-empty/uncertainty; operation-specific source-composition authority; role/cardinality/multiplicity/order dependencies.

Missing, ambiguous, corrupt, hash-mismatched or version-conflicting closure is `INTEGRITY_FAILURE`. V558 may not repair from raw stage directories, latest/current authority, fuzzy labels, network lookup, scores, embeddings or model judgment.

## 9. Provenance firewall

Provenance reachability proves origin/authority reachability only.

It does not grant source semantic equivalence, respondent linkage, sample pooling, estimand compatibility, generated-actor comparability or cross-source composition.

Cross-source composition remains `NONE_BY_DEFAULT`; an operation requires separate exact positive authority scoped to that operation.

## 10. StructuralPriorRepository and logical indexes

`SCR5578_STRUCTURAL_PRIOR_REPOSITORY@1.0.0` contains exact source publication binding, collection registry, producer-preserving locator registry, role-preserving mixed-producer reference graph, logical indexes, fidelity/negative manifest, immutable producer material/locators and exact publication/resolver policy bindings.

Raw producer directories are not required for resolution. Repository presence is not permission. Producer semantics are never re-owned.

Mandatory logical index families:

`TEMPORAL`, `GEOGRAPHIC`, `FINITE_STRATUM`, `GENERATED_POSITION_REQUIREMENT`, `NEGATIVE_LIMIT`, `PROVENANCE`.

Indexes are nonsemantic exact candidate-discovery accelerators and lossless/reversible views over locators. Every hit must dereference and reverify producer identity/hash/closure. A missing/incomplete required index is `REPOSITORY_INDEX_INTEGRITY_FAILURE`, not valid-empty.

Forbidden index authority includes nearest time/geography, prefix/substring match, embedding/LLM similarity, score rank, most-common, first-row, mutable latest and raw-stage/network fallback.

## 11. ContextResolver

Exact policy binding:

`V558_CONTEXT_RESOLVER_POLICY@1.0.0`  
`sha256:4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f`.

Pure semantic inputs are immutable repository bundle ID/content hash, index manifest ID/hash, ContextQuery ID/hash, resolver policy ID/version/hash and accepted generated-binding refs/hashes.

Forbidden nondeterminism: hidden wall clock, mutable latest, filesystem/database/process order, raw-stage/network lookup, randomness, unrecorded cache, display-label matching, LLM/embedding output and implementation-default policy.

Resolution algorithm:

1. validate repository/index/query/policy identity/hash/completeness;
2. discover candidates by exact governed keys;
3. dereference/reverify producer identity/hash/schema/closure;
4. verify `V557_allowed_uses ⊆ producer_allowed_uses`;
5. derive query-relative state and verify `resolver_allowed_uses ⊆ V557_allowed_uses`;
6. enforce exact producer conditions, geography, strata, generated-position and negative authority without invention;
7. apply temporal precedence;
8. apply equal-rank/multiplicity law;
9. emit a SelectionRecord for every considered candidate;
10. emit receipt without filling unresolved keys;
11. materialize only contract-defined structural context.

Temporal precedence:

`DIRECT_TEMPORAL_SUPPORT > LATEST_PRIOR_OBSERVATION_PROXY_IF_AUTHORIZED > EARLIEST_POST_QUERY_PROXY_IF_AUTHORIZED > NO_LAWFUL_TEMPORAL_ANCHOR`.

A point observation does not become an interval. A future proxy retains actual evidence time, signed lag and `historical_observation_at_query_time=false`.

Tie law: exact duplicate same ID/hash may dedup serialization only; producer-authorized multiplicity returns the full tied set; singular equal-rank authority with no precedence returns `AMBIGUOUS_EQUAL_RANK_AUTHORITY`; lexicographic order is serialization only; averaging/score/similarity/model judgment is forbidden.

Co-resolved participants cannot synthesize a V556 relation/topology. Geography/prevalence cannot create generated positions.

## 12. SelectionRecord / receipt / context

`SCR5578_V558_SELECTION_RECORD@1.0.0` is mandatory for every considered candidate and binds repository/index/query/policy identity, resolution key, locator and canonical producer ID/hash, producer/V557/resolver permission states and sets, epistemic/exception state, temporal/proxy/evidence/lag fields, geography/stratum/horizon, generated-position bindings, producer predicate receipts, negative/unknown/missing/noncomparability state, tie/multiplicity authority, decision/reason/provenance and record identity/hash.

Unresolved keys are never filled.

`SCR5578_V558_CONTEXT_RESOLUTION_RECEIPT@1.0.0` binds all/selected/deferred/preserved-negative records, unresolved keys, typed result state, replay digest and materialized context ref/hash.

`SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0` is `RESOLVER_DERIVED_CONTEXT`. Every resolved entry retains resolution key, SelectionRecord ref, canonical producer family/object ID/hash, producer locator, resolver allowed uses and decision state. It also preserves negative and deferred/unresolved entries.

It cannot create actor biography/position/event, memory, knowledge, belief, relationship truth, persona, voice, dialogue or a new V556 relation/topology.

## 13. Fidelity and refresh

`SCR5578_COVERAGE_FIDELITY_PROFILE@1.0.0` is deterministic, multidimensional and descriptive. It reports typed counts across requested/considered/selected/deferred/rejected/negative/unknown/noncomparable/valid-empty/no-anchor/ambiguity/integrity/unresolved states and producer/use-state dimensions. No canonical scalar fidelity/readiness score is authorized.

`SCR5578_CONTEXT_REFRESH_METADATA@1.0.0` freezes the carrier, not a new trigger authority. States:

- `NEXT_CONTEXT_CHANGE_BOUND`;
- `NO_BOUND_CONTEXT_CHANGE_WITHIN_AUTHORIZED_HORIZON`;
- `REFRESH_AUTHORITY_UNBOUND`;
- `REFRESH_INPUT_INTEGRITY_FAILURE`.

`next_context_change` requires exact producer temporal boundaries plus an exact separately accepted refresh authority. Without it, record `REFRESH_AUTHORITY_UNBOUND` and no invented time. Wall clock/latest/raw-stage/network inference is forbidden.

## 14. Replay

Same exact repository/query/policy/generated bindings produce the same semantic result.

Replay binds publication/repository identities and hashes; producer build/object/exact-contract/reference-contract identities; V557 governance; closure/root digests; index hashes; query fixed time; generated bindings; producer predicate/proxy/negative/tie authorities; SelectionRecords; receipt; fidelity; refresh and context identity.

`ReplayReceipt` remains audit-only.

## 15. Physical V557/V558 co-package equivalence bar

Physical fusion is lawful only if it proves:

1. V557 and V558 authority IDs/versions/hashes remain separately inspectable and independently versioned;
2. V557 item governance exists before repository selection can use an item;
3. the item-wise permission-subset chain is mechanically checkable;
4. publication and repository immutable identities remain distinct;
5. producer IDs/hashes/states remain canonical and unchanged;
6. role/cardinality/multiplicity/order closure is equivalent;
7. raw-dirs-absent standalone behavior is equivalent;
8. SelectionRecords, receipt, fidelity, refresh and context are deterministic under identical inputs;
9. failure attribution still distinguishes V557 governance, V558 repository integrity and resolver selection;
10. PSEPF exclusion and provenance-not-composition remain enforced;
11. direct and terminal consumers observe the same semantic/permission contract.

Rowset/status parity, file count, performance, module co-location or absence of a new ontology alone is insufficient.

## 16. Final seam

The local contract is closed. Exact SCR553/SCR554/SCR555/SCR556 contracts and the M4 checksum are the only remaining final-adjudication inputs. Any attempt to bind them by historical names, EP evidence or guessed schema fails closed.

`SCR5578_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`
