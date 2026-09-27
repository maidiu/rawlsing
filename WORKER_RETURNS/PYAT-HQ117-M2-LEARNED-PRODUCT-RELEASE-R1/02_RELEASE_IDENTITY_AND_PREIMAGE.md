# PYAT HQ117 — Release Identity and Preimage

## 1. Purpose

Define the minimum immutable identity of a learned-product release without copying or re-owning the producer's semantics.

This is a documentary contract. It does not claim that a live schema/API already exists.

## 2. Identity equation

A future conforming implementation SHALL define:

RELEASE_ID = ContentHash(Canonicalize(RELEASE_CORE_PREIMAGE))

The canonical release-core preimage contains exactly the release-level facts required to distinguish one historical publication claim from another while leaving family semantics with the producer.

Minimum fields:

| Field | Requirement | Why release-constitutive |
|---|---|---|
| release_contract_ref | exact | prevents schema/interpretation drift |
| release_subject_ref | exact | identifies the already producer-owned semantic product/disposition/service |
| release_subject_kind | exact enum | determines lawful resolution semantics without changing subject meaning |
| semantic_producer_contract_ref | exact | prevents publication from laundering producer ownership |
| authority_closure_ref | exact immutable closure | different authority/evidence instance can yield a different release even when semantic subject survives |
| dependency_closure_ref | exact immutable closure | pins direct governed prerequisites of this released subject |
| determinant_closure_ref | exact immutable closure | pins everything whose governed change can affect rebuild/revalidation |
| replay_reconstruction_ref | exact immutable contract/receipt closure | makes historical reconstruction auditable |
| explanation_lineage_ref | exact immutable lineage closure | makes the release explainable back to producer/evidence roots |

The release id MUST NOT be based on a mutable filesystem path, mutable row id, process-local object id, database insertion order, timestamp order, Git recency, version-string recency, current pointer or consumer permission.

## 3. Exact subject rule

release_subject_ref must dereference to the complete producer-owned semantic identity.

M2 does not define the subject's semantic fields.

Examples:
- an exact learned empirical relation produced by a competent relation owner;
- an exact typed VALID_EMPTY disposition;
- an exact Field Forge relation if/when instantiated by its owner;
- an exact governed learned service contract;
- an exact structural product owned by its structural producer.

Not sufficient:
- "the latest LiTS relation";
- an unhashed filename;
- a copied payload with no producer ref;
- a query whose output is not frozen/identifiable at the claimed product grain;
- a generic dictionary of fields whose family-specific semantics cannot be recovered.

If an n-ary/higher-order subject is referenced, exact dereference must recover full role/cardinality/order/multiplicity anatomy.

## 4. Release identity versus semantic identity

P1 permits the same semantic claim/product to be recertified under a different authority instance.

Therefore:
SAME_SEMANTIC_SUBJECT + DIFFERENT_AUTHORITY_CLOSURE
may lawfully produce:
DIFFERENT_RELEASE_ID

This is not semantic duplication. It is historical release distinction.

Conversely:
SAME_RELEASE_CORE_PREIMAGE
must produce:
SAME_RELEASE_ID

regardless of serializer, storage backend, cache state, endpoint or build host.

## 5. Closure-object rule

A closure ref may point to a canonical content-addressed closure object instead of inlining every member.

That is lawful only if:
- the closure object is immutable;
- dereference is exact;
- complete ordered/set semantics are defined;
- canonical member identities are recoverable;
- no "latest" registry lookup is needed to know what the closure contained historically.

A hash with unavailable/unrecoverable members is not sufficient replay closure.

## 6. Authority closure

The authority closure contains every authority instance constitutively required to justify the release claim.

It may include:
- source-semantic authority;
- validation/adjudication authority;
- source/universe relation authority;
- measurement/comparability authority where required;
- model/proxy authority where required;
- producer semantic contract;
- explicit exclusion/refusal authority where a negative disposition depends on it.

M2 does not decide which authorities a semantic family requires. The producer contract does.

Evidence-only recertification that changes authority closure while preserving semantic subject identity creates a new release id and gives M3 a possible RECERTIFIES relationship to classify later.

## 7. Dependency closure

Dependency closure records exact direct upstream semantic/source/product refs on which the subject depends.

It is not automatically every file read during execution.

A dependency is release-relevant when the producer's contract says the subject's valid derivation or interpretation depends on it.

Dependencies may include:
- exact source/release roots;
- exact empirical facts;
- exact candidate/validation receipts;
- upstream learned releases;
- exact structural admissions;
- governed service/model releases.

Direct producer refs remain intact; M2 never substitutes itself as dependency owner.

## 8. Determinant closure

Determinants answer a different question:

what governed change could alter the release's reconstruction, validation, or semantic validity?

Examples:
- decoder/projection identity;
- source content hash;
- question/topology/routing/risk-set authority;
- weights/design/estimand identity;
- discovery frontier/profile;
- validation rule;
- model/configuration;
- algorithm version;
- adaptive branch/tie/budget/stop/randomness law;
- explicit source relation/comparability authority.

Dependency and determinant sets may overlap but MUST NOT be blindly equated.

Cache keys and physical locators are determinants of a cache/materialization only, not necessarily of the semantic release.

## 9. Replay/reconstruction ref

This exact ref binds sufficient material to establish one of the following declared replay grades:

- EXACT_MATERIALIZED_DEREFERENCE: immutable semantic payload directly recoverable;
- EXACT_DETERMINISTIC_REBUILD: exact semantic payload can be rebuilt from pinned roots/determinants;
- EXACT_SERVICE_REEXECUTION: exact governed service invocation can be replayed given pinned invocation receipt;
- HISTORICAL_EXPLANATION_ONLY: semantic subject remains citable/explainable but executable reconstruction is not promised.

A future implementation MAY support multiple grades but MUST declare one exactly.

It MUST NOT call a release "replayable" when it only remembers a library name/version or a mutable external endpoint.

## 10. Explanation lineage

Explanation lineage must support reverse traversal:

release_id
-> exact release subject
-> producer contract
-> producer-owned claims/dispositions
-> exact supporting/adjudicative evidence and authority
-> source/release roots as applicable

The lineage may be a DAG.

It must preserve typed gaps. A BLOCKED/MISSING_AUTHORITY node cannot be omitted merely to produce a clean explanation path.

## 11. Product/service kind

Minimum subject kinds:
- IMMUTABLE_LEARNED_PRODUCT
- TYPED_DISPOSITION
- LEARNED_SERVICE_CONTRACT

A future implementation may add narrower kinds only under governed schema evolution.

For LEARNED_SERVICE_CONTRACT:
- callable semantics and output contract are part of the producer subject;
- service implementation/model/configuration determinants are pinned as required by the producer;
- network/process endpoint is publication binding, not release identity;
- individual invocation inputs/results have their own execution receipts and, if later published as products, their own release ids.

## 12. Scope/time/universe identity

M2 does not invent a generic scope model.

If scope, universe, time, wave, population, risk set, measure or estimand is constitutive of the semantic subject, the release_subject_ref MUST recover it through the producer's semantic identity.

If an implementation needs a release-level searchable projection of these fields, that projection is nonauthoritative metadata unless exact equality to the producer-owned subject is verified.

Searchability never becomes semantic ownership.

## 13. Excluded from release-core preimage by default

- publication binding / physical locator;
- serializer and compression;
- physical payload copy hash when it is only one representation of the same semantic subject;
- local database primary key;
- cache/index key;
- mirror/replica identity;
- endpoint URL;
- machine hostname;
- publication timestamp;
- Git commit order;
- current-selected status;
- consumer permission.

A physical representation may itself receive a separate integrity hash and publication_binding_id.

## 14. Publication-binding identity

A conforming implementation SHALL separately define:

PUBLICATION_BINDING_ID = ContentHash(Canonicalize(
  release_id,
  publication_contract_ref,
  resolution_mode,
  exact_resolver_or_locator_ref,
  representation_integrity_ref
))

The binding may point directly to the producer.

Changing only a physical binding creates a new publication_binding_id, not a new release_id.

Multiple valid publication bindings can coexist for one release.

## 15. Historical identity invariant

Once published:
- release core is immutable;
- release id is immutable;
- publication binding records are immutable;
- predecessor release history is never rewritten;
- a lost cache or moved endpoint does not mutate release identity;
- a failed resolver produces a typed resolution failure, not silent selection of another release.

M3 may later select, supersede, correct, recertify or withdraw at lifecycle grain. M2 preserves the exact historical release objects that make those events meaningful.
