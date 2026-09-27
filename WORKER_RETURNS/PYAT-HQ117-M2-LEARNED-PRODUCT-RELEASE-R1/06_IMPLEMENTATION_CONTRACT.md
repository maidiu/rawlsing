# PYAT HQ117 — M2 Future Implementation Contract

## Status

DOCUMENTARY_CONSTITUTION_ONLY__NO_RUNTIME_IMPLEMENTATION_AUTHORIZED_BY_THIS_RETURN

This file defines the minimum behavioral contract a later explicitly authorized implementation must satisfy.

It does not select a module name, database, repository backend, serialization format, process topology or deployment model.

## 1. Required logical types

A future implementation must expose equivalents of the following logical types.

### ReleaseSubjectRef

Exact ref to an already producer-owned:
- learned semantic product;
- typed disposition/adjudication;
- learned service contract.

Required properties:
- immutable exact identity;
- exact producer/semantic-owner contract;
- complete producer-owned semantic anatomy recoverable;
- no mutable selector.

### ReleaseCore

Immutable content-addressed M2 release manifest.

Required fields:
- release_contract_ref;
- release_subject_ref;
- release_subject_kind;
- semantic_producer_contract_ref;
- authority_closure_ref;
- dependency_closure_ref;
- determinant_closure_ref;
- replay_reconstruction_ref;
- explanation_lineage_ref;
- derived release_id.

Forbidden fields with semantic effect:
- current flag;
- latest flag;
- consumer permission;
- inferred structural admission;
- mutable endpoint;
- mutable path.

### PublicationBinding

Immutable content-addressed serving binding.

Required fields:
- release_id;
- publication_contract_ref;
- resolution_mode;
- exact_resolver_or_locator_ref;
- representation_integrity_ref;
- derived publication_binding_id.

### ResolutionReceipt

Immutable audit result for one exact resolve operation.

Required fields:
- requested release_id;
- publication_binding_id;
- resolved release_core_hash;
- resolved release_subject_ref;
- resolver_contract_ref;
- integrity result;
- typed resolution state;
- explicit assertion that no selector substitution occurred.

### Closure objects

Exact immutable content-addressed objects or exact refs for:
- authority;
- dependency;
- determinant;
- replay/reconstruction;
- explanation lineage.

A closure object must be fully dereferenceable at historical replay time.

## 2. Required operations

Names below are semantic roles, not mandated function names.

### constitute_release

Input:
- exact ReleaseSubjectRef;
- exact producer contract ref;
- exact closure refs;
- exact release contract ref.

Behavior:
1. verify the subject resolves exactly;
2. verify producer identity;
3. validate required closure presence according to producer/release contract;
4. reject fuzzy/mutable selectors;
5. canonicalize release-core preimage;
6. derive content-addressed release_id;
7. return the immutable ReleaseCore.

It MUST be idempotent:
same canonical preimage -> same release_id.

It MUST NOT:
- adjudicate subject semantics;
- infer currentness;
- assign consumer permission.

### publish_binding

Input:
- exact release_id;
- exact publication contract;
- exact resolution mode;
- exact locator/resolver ref;
- exact representation integrity ref.

Behavior:
- verify release_id exists/resolves exactly;
- verify binding resolves or is certifiably capable of resolving only that exact release;
- derive publication_binding_id;
- persist/return immutable binding.

Multiple bindings per release are allowed.

### resolve_release_exact

Input:
- exact release_id;
- optionally exact publication_binding_id.

Behavior:
- resolve that exact release only;
- verify release-core identity;
- resolve/return exact release subject ref;
- emit typed ResolutionReceipt.

Forbidden:
- latest/default/fuzzy/nearest/semver fallback;
- silently using another release if requested binding is unavailable.

### resolve_subject_exact

Input:
- exact release_id.

Output:
- exact producer-owned release_subject_ref and producer contract ref.

M2 does not return a copied re-owned semantic object unless a representation is explicitly a mirror and producer identity remains authoritative.

### explain_release

Input:
- exact release_id.

Output:
- exact explanation-lineage DAG refs plus exact authority/dependency/determinant/replay closure.

Human-readable projections may be added but are nonauthoritative unless separately governed.

### affected_release_refs

Optional generic graph utility:
Input:
- exact changed determinant ref.

Output:
- exact release ids reachable through registered determinant/dependency edges.

This utility may compute graph reachability only.

It MUST NOT classify lifecycle meaning or mutate current selection.

## 3. Required validation order

A future implementation should fail closed in this order:

1. schema/contract identity exactness;
2. release subject exactness;
3. producer ownership exactness;
4. subject-kind compatibility;
5. authority closure;
6. dependency closure;
7. determinant closure;
8. replay/reconstruction closure;
9. explanation lineage;
10. canonical release-id recomputation;
11. publication-binding integrity;
12. resolution exactness.

A failure at an earlier step cannot be "repaired" by a later publication layer.

## 4. Canonicalization rules

The implementation must define deterministic canonicalization for all M2-owned manifests.

Requirements:
- stable field ordering;
- stable exact-ref representation;
- explicit set versus ordered-list semantics;
- duplicate exact refs rejected or canonically deduplicated only where set semantics are governed;
- no timestamp in release identity;
- no process-local ids;
- no physical insertion order;
- no noncanonical floating or locale-dependent textual formatting if such data appears in M2-owned metadata.

M2 canonicalization never canonicalizes the producer's semantics itself. It canonically references the producer's exact semantic object.

## 5. Error taxonomy

Minimum typed errors/states:
- RELEASE_CONTRACT_MISMATCH
- RELEASE_SUBJECT_NOT_FOUND
- RELEASE_SUBJECT_REF_NOT_EXACT
- PRODUCER_CONTRACT_MISMATCH
- RELEASE_SUBJECT_KIND_MISMATCH
- AUTHORITY_CLOSURE_INCOMPLETE
- DEPENDENCY_CLOSURE_INCOMPLETE
- DETERMINANT_CLOSURE_INCOMPLETE
- REPLAY_CLOSURE_INCOMPLETE
- EXPLANATION_LINEAGE_INCOMPLETE
- RELEASE_ID_MISMATCH
- PUBLICATION_BINDING_MISMATCH
- RESOLVER_NOT_EXACT
- REPRESENTATION_INTEGRITY_FAILURE
- RELEASE_UNAVAILABLE
- REBUILD_UNAVAILABLE
- REBUILD_SEMANTIC_MISMATCH
- FORBIDDEN_SELECTOR
- PERMISSION_WIDENING_ATTEMPT
- CURRENTNESS_INFERENCE_ATTEMPT
- SEMANTIC_REOWNERSHIP_ATTEMPT
- NEGATIVE_STATE_LAUNDERING_ATTEMPT

Errors may be implemented as exceptions or typed results. They must remain distinguishable in audit/replay.

## 6. Idempotence and concurrency

Because release_id and publication_binding_id are content-addressed:
- duplicate constitution of the same release is idempotent;
- concurrent publication of the same exact release core converges on the same id;
- concurrent addition of different physical bindings creates separate binding ids under one release;
- commit/insertion order has no current-selection meaning;
- a race cannot choose "latest".

If a storage engine requires mutable indexes for lookup, those indexes are nonauthoritative projections over immutable release/binding records.

## 7. Storage neutrality

A conforming implementation may use:
- content-addressed files;
- Git objects;
- relational database rows with immutable semantic hashes;
- object storage;
- family-local repositories;
- distributed resolver registries;
- direct producer repositories.

No one backend is constitutionally required.

The implementation must prove:
- exact resolution;
- immutability;
- producer-preserving dereference;
- no hidden selector;
- historical closure.

## 8. Materialized and virtual parity

The implementation must support, or at minimum not prohibit, both:
- materialized release subject representation;
- virtual deterministic reconstruction.

A materialized representation cannot receive stronger semantic authority than a virtual representation merely because bytes are retained.

A virtual representation cannot claim exact replay unless its reconstruction closure passes the declared replay grade.

## 9. Service releases

A conforming service release implementation must separate:
- logical service contract release;
- physical endpoint binding;
- invocation receipt;
- invocation output product release where any.

Endpoint failover is allowed only among bindings proven to resolve the same release id.

Failover between different release ids requires external lifecycle/current-selection authority.

## 10. Negative product support

The implementation must permit release subjects whose semantic state is nonpositive or unresolved.

It must not require:
- a nonempty payload;
- a positive relation;
- a numeric effect;
- a truth-bearing negative polarity.

A release can validly identify a typed disposition only.

The implementation must preserve distinctions in 05_NEGATIVE_PRODUCT_PUBLICATION.tsv.

## 11. M3 integration contract

M3 receives exact release ids from M2.

M2 must expose enough graph data for M3 to:
- select an exact release;
- attach typed lifecycle events;
- compute determinant-affected sets;
- preserve predecessor history.

M2 must not expose an API whose semantic meaning is:
- set_latest;
- promote_newest;
- select_highest_version;
- auto_supersede;
- auto_withdraw_on_missing;
- current_if_only_release.

Any current-selection interface belongs to M3 and must require explicit jurisdiction + target + scope + purpose.

## 12. Consumer integration contract

A consumer can:
- resolve exact release;
- verify producer subject;
- inspect authority/replay/explanation closure.

A consumer cannot treat successful M2 resolution as:
- use permission;
- structural admission;
- source comparability;
- target permission;
- actor knowledge;
- causal permission.

Consumer-specific authority must remain explicit.

## 13. Reference-only implementation capital

A future implementation may inspect:
- B5 learned-product lifecycle candidate;
- C5R2 owner/executor prototype;
- current AuthoritySnapshot maintenance mechanics;
- current structural M4 publication/repository mechanics;
- current replay audit;
- C07 product/service DAG.

But it must not copy their owner ids or bounded family permissions into generic M2 authority.

## 14. Implementation admission gate

Before production adoption, an M2 implementation should demonstrate:
- all hostile tests in 07_HOSTILE_RELEASE_TEST_PLAN.md;
- release-id stability across physical relayout;
- release-id change across constitutive closure change;
- exact negative-state preservation;
- direct producer dereference without ownership laundering;
- virtual rebuild with exact replay where claimed;
- no selector/currentness/permission leakage;
- M3 handoff by exact release id only.

This return authorizes no implementation. It makes that later implementation target exact.
