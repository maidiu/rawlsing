# R04 PROPOSED PHYSICAL CONTRACT — CCIV

Status: `NON_DISPOSITIVE__DESIGN_ONLY`

This contract is a proposed execution/storage contract only. It does not amend C11, I03, I05, I04, source authority, or whole-machine architecture.

## 1. Contract objective

Provide a columnar/vector execution substrate capable of reconstructing the complete frozen logical C11 surface and executing all lawful I03/I05 workloads without exposing physical layout to semantic consumers.

## 2. Authority boundary

CCIV owns:

- batch/vector physical compilation;
- physical grouping/columnar layout;
- physical profile selection;
- nonauthoritative indexes/caches;
- late-materialization execution mechanics;
- virtual C11 reconstruction mechanics.

CCIV does **not** own:

- source meaning;
- source-family semantic rules;
- M01-M18 definitions;
- query/discovery/admission semantics;
- functional-dependency proof assigned to R02;
- acceptance equivalence oracle assigned to R03;
- whole-machine downstream meaning.

## 3. Sealed release contract

A release is authoritative only when a seal contains:

- exact source artifact SHA and source-format identity;
- exact decoder identity/configuration receipt;
- exact source-authority/C11 authority dependency set;
- logical C11 contract identifier;
- canonical member inventory with byte hashes;
- deterministic event/axis ordering laws used by the physical profile;
- exact profile descriptor identifying only physical capabilities;
- replay manifest/root;
- explicit authoritative-member versus optional-cache separation;
- format/schema versions for every member.

Missing, partial, or hash-mismatched authoritative members make the release nonauthoritative/fail-closed.

## 4. Uniform logical reader boundary

The logical consumer sees one representation-independent interface. The names below are pseudocode capabilities, not an implementation API commitment.

```text
C11LogicalReader
  release_identity()
  verify_release()
  resolve_exact(ref)
  iter_logical_objects(family, exact_scope)
  reconstruct_respondent_event(exact_event_selector)
  stream_semantic_audit()

  exact_risk_selector(query_semantics)
  exact_predicate_selector(predicate_semantics, governed_universe)
  exact_target_material(selector, target_plan)
  exact_weight_material(selector, measure_plan)
  exact_coordinate_material(selector, coordinate_plan)
```

I03/I05/I04 receive exact logical objects/results/refs, never a physical profile discriminator.

A backend may expose execution capabilities to an internal planner (`projection_pruning`, `vector_scan`, `bitmap_cache_available`), but those capability flags can change only the execution plan, never legal query meaning, candidate reachability, state interpretation, or result identity.

## 5. Physical profiles

### 5.1 `AXIS_DENSE`

Permitted only for a question/block when an independently accepted determinant proves the omitted coordinate/material for the exact release and defines an exact exception path.

The profile may use row position/column lane as a physical locator. It may not use physical position as semantic identity.

### 5.2 `EXPLICIT_EVENT`

Required when:

- dependency proof is absent;
- multiple events can exist per respondent/question;
- component/subitem/event identity matters;
- topology is repeated/ranked/ordered/multiselect/componentized/nonrectangular;
- exact exceptions exceed the lawful dense profile;
- a vector/type lane cannot represent an exact value without loss.

A release can mix profiles by block. The profile choice is physical metadata only.

## 6. Canonical member classes

### 6.1 Release metadata

Stores source/decoder/authority dependency and member-hash closure.

### 6.2 Respondent axis

Stores exact replay row ordinal and complete respondent-grain C11 material proven at that grain. Execution ordinals are dense and deterministic but nonsemantic.

### 6.3 Question/variable axis

Stores source variable ordinal/name/metadata and complete question-grain C11 material proven at that grain. Equal labels, equal value dictionaries, or equal raw vectors never imply question identity.

### 6.4 Incidence blocks

Bounded question groups. A question lane bundle may contain:

```text
raw_value_type_tag
raw_integer / raw_float_exact_lane / raw_string / raw_bytes-or-exact-fallback
physical_state_code
semantic_response_state_code
canonical_value_type_tag + canonical value lane if authorized
explicit event coordinate pointer when needed
```

Exact lane design is delegated to R02 type law. CCIV must support a lossless fallback representation.

### 6.5 Event/topology relation

Carries exact event identity, component/subitem, group, occurrence, order/rank/multiplicity, topology refs, and other event-specific material. It is canonical, not a cache.

### 6.6 Routing/applicability/risk-set relation

Separate canonical relation. It must not be encoded as null/missing response cells.

### 6.7 Coordinate / weight / measure / design relations

Separate canonical typed relations preserving exact value plus governing authority.

### 6.8 Authority / dependency / replay / source-relation relations

Separate canonical relations preserving exact refs and closure. Equal physical references may be dictionary encoded, but dictionary ordinal is never semantic identity.

### 6.9 Sparse exact exceptions

Permitted only against a separately proved default/derivation. Exception representation must be total for counterexamples; overflow or unrepresentable exceptions invalidate the optimization rather than discard the exception.

## 7. Vector compiler contract

Input is the frozen decoder/source-authority logical material. The vector compiler may consume bounded decoder batches directly.

It must validate, vectorially or by exact fallback, every observable invariant formerly enforced by object constructors/C11 integrity. Minimum invariant classes:

1. exact `ExactRef` shape and lowercase SHA-256;
2. exact `AuthorityRef` shape/version/hash;
3. public versus internal family separation;
4. allowed typed-state vocabularies;
5. required semantic fields;
6. nonempty authority closure where required;
7. canonical authority/dependency set ordering and duplicate collapse;
8. deterministic exact-value canonicalization;
9. reserved identity-field exclusion;
10. response-state/typed-state equality;
11. deterministic semantic projection/content hash/object ID;
12. respondent/universe referential closure;
13. native/canonical question binding closure;
14. routing/risk-set closure;
15. topology/order/rank/multiplicity validity;
16. exact weight/design/estimand closure;
17. source relation closure;
18. replay manifest and member closure;
19. duplicate/conflict rejection;
20. full M01-M18 semantic projection parity.

The compiler may not call an incomplete subset “equivalent.” Missing vector validation requires an exact validated fallback or rejection.

## 8. Exact selector contract

An exact selector is an ephemeral or cached set of scoped respondent identities/ordinals relative to a sealed release and governed universe.

Selector operations:

- AND = exact intersection;
- OR = exact union;
- NOT = exact complement within the governed universe/risk set **after** exact routing applicability resolution;
- branch membership = exact governed member set/replay binding;
- cross-question alignment = exact scoped respondent identity, not physical row coincidence unless the release law proves their equivalence.

A selector must carry enough dependency identity to prove which release, risk set, predicate semantics, and authorities it represents.

## 9. Cache/index contract

Default status for every bitmap/index/cache:

`NONAUTHORITATIVE__REGENERABLE_CACHE`

Cache key must include:

- canonical release identity;
- exact logical predicate/index definition;
- relevant authority dependency hashes;
- cache schema/version.

Cache mismatch/corruption => discard and regenerate/scan.

Canonical release identity excludes cache member hashes. Cache deletion/rebuild must not alter logical refs, replay identity, I03/I05/I04 results, or coverage.

No query/discovery candidate may be rejected because a cache is absent.

## 10. Late-materialization contract

Execution ordering must preserve negative truth:

1. verify sealed release;
2. resolve exact authority and source scope;
3. resolve routing/risk set and unresolved/nonmember/inapplicable states;
4. evaluate condition predicates by exact selector algebra;
5. fetch target/topology/coordinate/weight data only for exact survivors;
6. assemble target configuration/joint at respondent grain;
7. execute exact measure/support/uncertainty semantics;
8. materialize final logical objects/receipts.

Any optimization that filters before the evidence required to distinguish negative/failure states is forbidden.

## 11. I05 open-world contract

The canonical physical release must be sufficient to evaluate any later exact-bounded I05 candidate composed from lawful existing C11 atoms/questions within authority scope.

Therefore:

- no finite predicate catalog is canonical;
- no pair/k-way preaggregation is sufficient by itself;
- no bitmap vocabulary defines reachability;
- an uncached candidate is evaluated by vector scanning canonical incidence;
- exact new combinations require no re-ingest;
- storage-tuned pruning is forbidden.

## 12. Determinism and re-layout law

Given identical source bytes, source authority, C11 authority, compiler version/configuration, and accepted physical-profile selection law, canonical output is deterministic.

A semantically equivalent physical re-layout may change physical release/member hashes if the physical compilation version changes, but virtual logical C11 semantic projections/refs/hashes must remain identical. Filesystem order, block width, row-group size, compression settings, and cache state never enter semantic identity.

## 13. Corruption law

- authoritative member corruption -> fail closed;
- release seal mismatch -> fail closed;
- authority dependency mismatch -> fail closed;
- canonical member absent -> fail closed;
- optional cache corrupt/stale -> discard cache, canonical scan/rebuild;
- no partial plausible result from an authoritative corruption.

## 14. Acceptance law

CCIV is not accepted because it is smaller. It must:

1. pass the independent R03 semantic/source/I03/I05/I04 oracle;
2. pass hostile source heterogeneity including SAV/DTA, WVS/LiTS and cross-corpus exceptions;
3. preserve arbitrary conjunctions and unseen I05 combinations without re-ingest;
4. preserve deterministic replay/integrity/fail-closed behavior;
5. beat the simplest passing lower-risk representation by a materially sufficient end-to-end margin or solve a blocking hard-gate failure.

Otherwise disposition:

`REJECT_CCIV__PREFER_SIMPLER_STREAMING_LONG`.
