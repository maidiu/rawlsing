# SCR5578 Exact Contract — V557 Publication / V558 Standalone Repository / Context Resolution

**Contract ID:** `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION_EXACT_CONTRACT`  
**Version:** `1.0.0`  
**Repository:** `maidiu/rawlsing`  
**Exact common base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Authority posture:** local contract frozen; exact SCR553–SCR556 producer identities remain M4 final-seam bindings  
**Machine-readable canonical companion:** `EXACT_CONTRACT.json` (`sha256:148df7139f1d991cd95924da8fd6eac2b65caa9d1398cc6ea7e930c1fa58874f`)

## 1. Jurisdiction and non-jurisdiction

V557 and V558 remain distinct logical authorities even if one implementation physically co-packages them.

**V557 owns:** item-level runtime publication admission; producer-permission intake; monotone permission narrowing; typed item/collection governance; immutable publication identity; interpretation-critical closure proof.

**V558 owns:** immutable `StructuralPriorRepository`; producer-preserving locators/reference graph; logical indexes; deterministic stage-blind `ContextResolver`; candidate `SelectionRecord`s; resolution receipt; descriptive coverage/fidelity; exact refresh carrier metadata; `ResolvedStructuralContext`.

Neither owns V553/V554/V555/V556 producer semantics. Neither may create source compatibility, cross-source composition, actor state or expression authority. No production implementation is authorized here.

## 2. Mixed-producer publication root law

The only SCR5578 structural publication-root producer families frozen by the accepted R03 broad DAG are:

`V553 | V554 | V555 | V556`

Each producer family has one pending **exact final-seam registry binding**. SCR5578 intentionally does not fill:

- producer contract ID/version/hash;
- exact object or collection schema IDs/versions;
- canonical object identity tuple/hash law;
- exact semantic-state enum;
- exact producer permission contract;
- exact interpretation-critical reference-contract IDs/versions/hashes;
- producer-owned role/cardinality/multiplicity/order semantics;
- direct-publication eligibility details;
- producer build/schema/compiler replay tuple.

Those come only from accepted SCR553/SCR554/SCR555/SCR556. `EP*`, historical modules and CAN packaging labels may not substitute.

A V553/V554/V555/V556 object may publish directly to V557 if and only if its exact bound producer contract independently authorizes the exact object and requested use. No synthetic later-stage wrapper is required merely to preserve stage numbering.

## 3. Item-wise permission lattice

Canonical use atoms are:

`REVIEW`, `CONTEXT`, `ACTIVE_CAUSAL`.

Canonical state expansion:

| State | Allowed-use set |
|---|---|
| `ALLOW_ACTIVE_CAUSAL_CONTEXT` | `{REVIEW, CONTEXT, ACTIVE_CAUSAL}` |
| `ALLOW_CONTEXT_ONLY` | `{REVIEW, CONTEXT}` |
| `ALLOW_REVIEW_ONLY` | `{REVIEW}` |
| `DENY_CAUSAL_USE` | `{}` |
| `NOT_APPLICABLE` | `{}` |

For every producer object and every resolver candidate:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`.

The comparison is **item-wise**. A collection/global status cannot stand in for it.

Required enforcement order:

1. verify identity/hash/schema/version/reference-closure integrity;
2. read exact producer permission ceiling;
3. reject missing/ambiguous producer permission rather than guessing;
4. apply V557 preserve-or-narrow decision only;
5. preserve producer negative/missing/noncomparable/valid-empty meaning;
6. ignore collection/global readiness as permission authority;
7. V558 repository ingest grants no permission;
8. resolver may narrow further for the fixed query but never widen.

A root's permission never propagates to its dependencies. A dependency retains its own state. Repository membership, locator existence and index hits are never permission grants.

## 4. V557 governance records and collections

`SCR5578_RUNTIME_AUTHORIZED_OBJECT_RECORD@1.0.0` requires:

`governance_record_id`, `governance_record_hash`, canonical V557 authority ID/version, producer family/collection kind, producer object ID/hash, producer build ID/hash, producer schema ID/version/compiler, producer rule/predicate/reference-contract refs, exact producer permission input, V557 publication admission, V557 use state, expanded V557 allowed-use set, epistemic class, governance exception state/subtype, negative/limit refs, noncomparability refs, uncertainty refs, transitive-closure audit ref, provenance refs, runtime-use rule ref and exact compatibility bindings.

**Identity:** V557 governance identity is audit/governance identity. The producer object ID/hash remains the semantic identity.

Publication admission enum:

`ADMIT_RUNTIME_AUTHORIZED_RECORD | DO_NOT_ADMIT_RUNTIME_AUTHORIZED_RECORD`.

Governance exception enum:

`NO_EXCEPTION_STATE | NEGATIVE_AUTHORITY | MISSING_AUTHORITY | NONCOMPARABLE | VALID_EMPTY | INTEGRITY_FAILURE`.

`SCR5578_RUNTIME_AUTHORIZED_COLLECTION_MANIFEST@1.0.0` binds the producer collection/build/schema/hash, exact count, collection state, exact valid-empty subtype if any, every governance-record count/state distribution, closure manifest/hash, V557 authority binding and governance registry versions.

Collection states:

`VALID_NONEMPTY | VALID_EMPTY | INVALID_FAIL_CLOSED`.

A valid-empty collection has exact zero roots under producer/governance authority. It never causes filler-object creation.

## 5. Corrected reference-class registry

### Structural publication roots

Only exact bound V553/V554/V555/V556 producer objects are root candidates.

### Interpretation-critical reference-only classes

These may be carried/dereferenced only when an exact producer schema/reference contract declares them interpretation-critical:

- `StructuralEmpiricalAdmission`;
- `EmpiricalFact`;
- QuerySpec;
- source UniverseSpec/risk set;
- measure/weight/estimand authority;
- applicable source-comparability/composition authority;
- historical producer/rule/predicate/authority snapshots;
- producer-owned temporal/negative/limit/uncertainty dependencies.

Their upstream owners retain semantic authority.

`DiscoveryResultReceipt` is audit/provenance-only.  
`ReplayReceipt` is replay/audit-only and has no structural runtime-prior role.

### `MUST_NOT_APPEAR`

The structural repository rejects:

- `PositionedSubjectEmpiricalPossibilityField` / PSEPF;
- `V3EmpiricalPossibilityInput`;
- `ActorComparatorReceipt`;
- rendered expression/persona objects.

PSEPF remains on the separate direct thin V3 lane.

## 6. Immutable V557 publication bundle

`SCR5578_V557_IMMUTABLE_PUBLICATION_BUNDLE@1.0.0` is content-addressed and atomic.

ID rule:

`V557PUB:<publication_identity_hash>`.

It binds, at minimum:

- publication manifest ID/hash;
- every collection-manifest binding;
- every item governance-record binding;
- producer build identities/hashes;
- transitive closure manifest/hash and per-root digests;
- producer material store manifest/hash or exact immutable external content-locator manifest;
- CAN-003/V557 governance authority binding;
- publication/compatibility policy bindings;
- publication content hash and identity hash;
- atomic publication state.

Any identity/content/governance/policy binding change creates a new bundle. In-place mutation and mutable `latest` identity are forbidden.

Partial publication is not consumable.

## 7. Producer-preserving locator and reference graph

`SCR5578_PRODUCER_PRESERVING_OBJECT_LOCATOR@1.0.0` must contain the authoritative producer family, object ID/hash, build ID/hash, schema ID/version, producer rule/predicate/reference-contract bindings, V557 governance-record ID/hash, content blob hash and exact storage/provenance locator.

`locator_id` is nonsemantic. It must reverse exactly to one authoritative producer tuple without text/fuzzy rematching.

Byte-identical objects under distinct producer identities do **not** become semantically equivalent.

### Reference graph

Closure is `PER_PUBLISHED_ROOT_ROLE_PRESERVING_TRANSITIVE_SEMANTIC_CLOSURE`.

The walker follows **only** producer/reference-contract-declared interpretation-critical references.

Every edge carries:

- source and target locator refs;
- reference-contract ID/version/hash;
- edge role;
- requiredness;
- participant role;
- declared cardinality;
- multiplicity key;
- order-significant flag;
- semantic ordinal.

SCR5578 does not invent edge roles. A role name has semantic force only because the bound producer/reference contract supplies it.

Strong one-target references resolving to zero or incompatible multiple targets fail closed. Producer-authorized multiplicity is preserved.

N-ary objects remain n-ary. No dyadization, collapse, winner selection or reconstruction is permitted.

Semantic order is producer-declared role/ordinal meaning. Serialization order is never authority.

## 8. Strict standalone positive + negative closure

Raw V553/V554/V555/V556 stage directories are absent in the conformance fixture.

Each required leaf must be satisfied by either:

1. packaged immutable content addressed by exact hash; or
2. a packaged immutable content-addressed locator/resolution contract binding exact identity/version/hash, deterministic authorization and a non-fuzzy/non-latest resolver.

The following **do not** satisfy a leaf by themselves:

- object ID;
- content hash with no resolvable content contract;
- display label;
- provenance prose;
- current/latest authority;
- a raw-stage path outside the bundle.

Closure includes every interpretation-critical positive and negative dependency declared by the producer contract. Depending on the bound producer, that may include producer authority snapshot, source universe/risk set, QuerySpec, measure/weight/estimand authority, admission lineage, temporal support/limits, typed negative/missing/noncomparability/valid-empty/uncertainty authority, source-composition authority and exact participant/reference topology.

Missing, ambiguous, corrupt, hash-mismatched or version-conflicting required closure is `INTEGRITY_FAILURE`.

V558 may never repair closure from raw stage directories, fuzzy labels, current/latest authority, network lookup or model judgment.

## 9. Provenance / source-composition firewall

Exact provenance closure proves only origin and authority reachability.

It does **not** prove:

- source semantic equivalence;
- respondent identity linkage;
- sample pooling permission;
- estimand compatibility;
- generated-actor comparability;
- cross-source composition authority.

Cross-source composition is `NONE_BY_DEFAULT`. Any joint operation requires separate positive operation-specific authority preserved by exact reference.

## 10. Immutable StructuralPriorRepository

`SCR5578_V558_STRUCTURAL_PRIOR_REPOSITORY_BUNDLE@1.0.0` has ID:

`V558REPO:<repository_identity_hash>`.

The repository includes at minimum:

- repository manifest/content/identity hash;
- exact source V557 publication ID/identity/content hashes;
- source collection-manifest bindings;
- collection registry;
- producer-preserving ObjectLocator registry;
- role-preserving mixed-producer reference graph;
- mandatory logical index manifests;
- collection fidelity/negative manifest;
- producer material store or exact packaged immutable content locators;
- exact publication-policy bindings;
- exact resolver-policy binding;
- atomic repository state.

A changed producer build, V557 publication decision, index/material graph or bound policy creates a new repository identity. Existing repository bundles never mutate.

`PSEPF` admission returns:

`FORBIDDEN_REFERENCE_CLASS_PSEPF_STRUCTURAL_REPOSITORY`.

Repository presence never grants permission.

## 11. Logical index contract

Mandatory logical index families:

- `TEMPORAL`;
- `GEOGRAPHIC`;
- `FINITE_STRATUM`;
- `GENERATED_POSITION_REQUIREMENT`;
- `NEGATIVE_LIMIT`;
- `PROVENANCE`.

They are **nonsemantic exact candidate-discovery accelerators** and lossless/reversible views over producer-preserving locators.

Each manifest binds repository ID/hash, index family/schema/hash, completeness, exact key-contract ref, locator refs, authoritative object refs/hashes, build provenance and integrity.

Any required missing/incomplete index is `REPOSITORY_INDEX_INTEGRITY_FAILURE`, not valid-empty.

Every index hit is dereferenced and reverified.

Forbidden as semantic selection authority: nearest time, nearest geography, substring/prefix matching, embeddings, LLM similarity, scores, most-common, first-row, mutable latest and raw-stage/network fallback.

## 12. ContextQuery and deterministic ContextResolver

The accepted resolver binding is:

`V558_CONTEXT_RESOLVER_POLICY@1.0.0`  
policy hash `4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f`.

The semantic function is fixed by:

- immutable repository bundle ID/content hash;
- repository index manifest ID/hash;
- exact ContextQuery ID/hash;
- exact resolver policy ID/version/hash;
- exact accepted generated-binding refs/hashes.

No hidden wall clock, mutable latest, filesystem/database/process order, raw-stage lookup, network lookup, randomness, unrecorded cache, display-label matching, LLM/embedding output or implementation-default policy may affect selection.

Resolution sequence:

1. validate repository identity/content/atomic state;
2. validate resolver policy identity/version/hash;
3. validate ContextQuery ID/hash/purpose;
4. validate required index manifests and completeness;
5. discover candidates by exact index keys;
6. dereference and verify producer identity/hash/schema/reference closure;
7. verify `V557_allowed_uses ⊆ producer_allowed_uses`;
8. derive query-relative resolver state and verify `resolver_allowed_uses ⊆ V557_allowed_uses`;
9. enforce exact producer conditions, geography, stratum, generated-position and negative authority without invention;
10. apply temporal precedence;
11. apply equal-rank ambiguity or producer-authorized multiplicity;
12. emit a SelectionRecord for **every** considered candidate;
13. emit resolution receipt without filling unresolved keys;
14. materialize only the contract-defined structural context.

Temporal precedence:

`DIRECT_TEMPORAL_SUPPORT`
`>` `LATEST_PRIOR_OBSERVATION_PROXY` if explicitly authorized
`>` `EARLIEST_POST_QUERY_PROXY` if explicitly authorized
`>` `NO_LAWFUL_TEMPORAL_ANCHOR`.

A point observation does not become an interval. Future proxy evidence retains actual evidence time, signed lag and `historical_observation_at_query_time=false`.

Equal-rank law:

- exact same ID/hash duplicate: serialization dedup only;
- producer-authorized multiplicity: return full set;
- one required winner with no governed precedence: `AMBIGUOUS_EQUAL_RANK_AUTHORITY`;
- lexicographic order: serialization only;
- averaging, score, confidence, similarity, most-recent-build and model judgment: forbidden.

## 13. SelectionRecord

`SCR5578_V558_SELECTION_RECORD@1.0.0` is mandatory for every considered candidate.

It binds repository/index/query/policy identity; semantic resolution key; locator and canonical producer object ID/hash; producer permission state and expanded set; V557 governance ref/state/set; resolver query-relative state/set; epistemic/exception state; temporal rank/proxy authority/evidence time/lag flags; geography/stratum/horizon refs; generated-position bindings; producer predicate receipts; negative/unknown/missing/noncomparability refs; tie/multiplicity authority; decision/reason/provenance; record ID/hash.

Decision states include selected direct/prior/post/non-temporal, lawful multiplicity, permission/geography/stratum rejection, proxy rejection, unbound-position/missing-evaluator defer, no lawful temporal anchor, preserved negative/unknown/noncomparable/valid-empty, ambiguous equal-rank and integrity failure.

Unresolved keys are never filled.

## 14. Resolution receipt

`SCR5578_V558_CONTEXT_RESOLUTION_RECEIPT@1.0.0` binds the repository, query, policy, full SelectionRecord set, selected/deferred/preserved-negative subsets, unresolved keys, result state, replay input digest and ResolvedStructuralContext ref/hash when materialized.

Result states preserve complete, valid-empty, lawful multiplicity, typed partial/deferred, ambiguous, denied/not-applicable, no temporal anchor, missing authority, integrity failed and exact replay reproduced.

## 15. CoverageFidelityProfile

`SCR5578_COVERAGE_FIDELITY_PROFILE@1.0.0` is a deterministic descriptive aggregation of SelectionRecords.

It reports, at minimum, counts for requested keys, considered candidates, direct/prior/post/non-temporal selections, lawful multiplicity, unbound-position and missing-evaluator deferrals, permission/geography/stratum rejection, negative/unknown/noncomparability/valid-empty preservation, no-anchor, ambiguity, integrity failure, unresolved keys, authoritative producer family, V557 state and resolver allowed-use set.

No canonical scalar fidelity/readiness score is authorized.

## 16. Refresh metadata

`SCR5578_CONTEXT_REFRESH_METADATA@1.0.0` freezes the **carrier**, not a new refresh-trigger authority.

Required fields bind repository/query/query-time, refresh state, exact refresh authority ID/version/hash, `next_context_change` where authorized, authorized horizon for no-bound-change, decision-basis refs and replay digest.

States:

- `NEXT_CONTEXT_CHANGE_BOUND`;
- `NO_BOUND_CONTEXT_CHANGE_WITHIN_AUTHORIZED_HORIZON`;
- `REFRESH_AUTHORITY_UNBOUND`;
- `REFRESH_INPUT_INTEGRITY_FAILURE`.

`next_context_change` may exist only when an exact separately accepted refresh authority plus exact producer temporal boundaries determine it. If not bound, the resolver records `REFRESH_AUTHORITY_UNBOUND` and invents no time.

## 17. ResolvedStructuralContext

`SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0` is `RESOLVER_DERIVED_CONTEXT`.

It binds:

- repository ID/content hash;
- ContextQuery ID/hash;
- resolver policy ID/version/hash;
- resolution receipt ID/hash;
- selected resolved entries;
- preserved negative entries;
- deferred/unresolved entries;
- all SelectionRecord refs/hashes;
- CoverageFidelityProfile ID/hash;
- refresh metadata ID/hash;
- provenance refs;
- context ID/hash.

Every resolved entry retains semantic-resolution key, SelectionRecord ref, authoritative producer family/object ID/hash, producer locator, resolver allowed-use set and exact decision state.

Changing selected/preserved/deferred records or any bound bundle/query/policy creates a new context identity.

`ResolvedStructuralContext` cannot create actor biography, actor position, event, memory, knowledge, belief, relationship truth, persona, voice, dialogue or a new V556 relation/topology.

## 18. Replay contract

Identical exact bundle/query/policy/generated bindings must reproduce the same semantic result, SelectionRecord hashes, resolution receipt and context identity.

Replay binds publication/repository hashes; producer build/object IDs/hashes; producer exact-contract/reference-contract bindings; V557 governance; closure/root digests; all index hashes; resolver policy; fixed query time; generated bindings; producer predicate receipts; proxy authority/rules/lags; negative/noncomparability refs; tie/multiplicity authority; SelectionRecords; receipt; fidelity profile; refresh metadata and ResolvedStructuralContext.

ReplayReceipt itself remains audit-only.

## 19. Physical V557/V558 co-package equivalence bar

A single process/library/artifact may implement both logical authorities only if it proves all of the following:

1. V557 and V558 authority IDs/versions/hashes remain separately inspectable and independently versioned.
2. Exact item/collection V557 governance decisions exist before repository selection can use an item.
3. The item-wise permission-subset chain is mechanically provable.
4. Publication and repository immutable identities remain distinct and bound.
5. Producer IDs/hashes/states are unchanged and remain canonical.
6. Role/cardinality/multiplicity/order closure is identical under canonical hashing.
7. Standalone behavior is identical with raw producer directories absent.
8. SelectionRecords, receipt, fidelity, refresh carrier and context are deterministic under identical inputs.
9. Failure attribution still distinguishes V557 governance, V558 repository integrity and resolver selection.
10. PSEPF exclusion and provenance-not-composition remain enforced.
11. Every direct/terminal consumer observes the same contract.

Rowset parity, status parity, current module shape, file count, performance or “no new ontology” are not sufficient.

## 20. Final-seam binding rule

The local contract above is closed. The only unresolved SCR5578 final-adjudication inputs are accepted exact SCR553/SCR554/SCR555/SCR556 producer contracts and the M4 checksum that fills their registry slots.

Until each slot is bound by accepted contract ID/version/hash and exact head/result:

`PRODUCER_FINAL_CONTRACT_UNBOUND -> FAIL_CLOSED`.

No guessed producer machine identity is lawful.

Current token:

`SCR5578_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`
