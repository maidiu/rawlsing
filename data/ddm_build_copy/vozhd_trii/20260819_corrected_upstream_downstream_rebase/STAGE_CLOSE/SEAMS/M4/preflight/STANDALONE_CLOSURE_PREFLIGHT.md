# M4 STANDALONE CLOSURE PREFLIGHT

**Authority:** `NON_DISPOSITIVE_PREFLIGHT_ONLY`  
**Target later barrier:** `M4_MIXED_PUBLICATION_STANDALONE_REPOSITORY`  
**Final M4 status:** `NOT CLOSED — M2/M3 final producer bindings still required`

## 1. Preflight theorem

A V557/V558 package is standalone only if deleting all raw V553/V554/V555/V556 producer directories changes neither the exact semantic interpretation nor the deterministic resolver result for any otherwise-valid fixed repository/query/policy/binding input.

The package may minimize repeated producer payload copies. It may not minimize away semantic closure.

For each published root and every interpretation-critical descendant, exactly one of the following must hold:

1. the immutable target content is packaged and verifies against the exact producer identity/hash; or
2. the package contains an exact immutable content-addressed/hash-bound locator/resolution contract that deterministically resolves the exact target under the exact identity/version/hash.

Anything weaker is not a closure leaf.

## 2. Required V557/V558 administrative material

The standalone package must physically contain its own immutable administrative/integrity substrate, including at minimum:

- V557 immutable publication bundle identity/content hashes;
- V557 publication manifest and exact root/collection bindings;
- V557 item governance records and collection manifests;
- producer build/schema/compiler bindings required by producer contracts;
- transitive semantic closure/reference graph manifest;
- per-root closure digests and aggregate closure digest;
- producer-preserving locator registry;
- producer material-store manifest or exact immutable external-content locator manifest;
- V558 immutable repository identity/content hashes;
- collection registry;
- logical index manifests;
- fidelity/negative-state manifest;
- publication policy binding;
- resolver policy ID/version/hash binding;
- every compatibility binding used by the package;
- atomic publication/repository state.

These objects are administrative or governance objects. They do not replace producer ontology.

## 3. Exact producer material closure

### 3.1 V553 roots/dependencies

When interpretation-critical, closure must preserve exact V553:

- `TEMPORAL_KEY` identity and source-universe/admission/rule refs;
- `TEMPORAL_OBSERVATION` identity, temporal key, value owner, support/uncertainty state;
- `TEMPORAL_RELATION` rule, exact participants, source-universe refs and external compatibility refs;
- `TEMPORAL_LIMIT` state/reason, governed use, requested operation, blocked family, missing/negative authority refs and upstream negatives.

V553's exact producer ref shape is `{family, object_id, content_hash, schema_version}`. Same labels/year/timestamps or provenance cannot substitute.

### 3.2 V554 roots/dependencies

When interpretation-critical, closure must preserve exact V554:

- canonical F1 `BOUNDED_STRUCTURAL_AFFORDANCE` identity;
- canonical selected basis semantic identity;
- exact rule/signature and authority-bundle fingerprint;
- exact F2 applicability-condition IDs and producer-negative/requirement refs;
- B1 identity/reference spine where required for replay or V555 ancestry;
- source/universe/estimand/measure/weight and source-comparability authority fingerprints where material;
- duplicate-equivalence and precedence authority version;
- exact nonpositive/valid-empty state.

Repository packaging may not use text equality, source labels, latest data or row order to reconstruct an omitted F1/F2/B1 dependency.

### 3.3 V555 roots/dependencies — preflight shape only

The local V555 contract requires closure over:

- exactly one exact V554 F1 reference;
- route rule ID/version;
- route shape ID/version;
- channel structural role ID;
- exact structural channel ref;
- receiving constraint kind;
- exact target receiving-position ref;
- exact ordered `SOURCE -> MEDIATION_LOCUS -> RECEIVER` semantics;
- typed route decision state;
- exact inherited V554 F2 refs where interpretation-critical;
- exact V555 owning authority and immutable seal/reference;
- producer use-permission ceiling.

Final M4 must substitute the **M2-accepted** sealed V555 reference contract. The local seven-field tuple may be exercised by preflight fixtures but cannot be promoted to final M4 authority on this branch.

### 3.4 V556 roots/dependencies — preflight shape only

The local V556 contract requires closure over:

- one exact V556 semantic family;
- exact V556 rule authority ID/version/content hash;
- 2..n exact V555 participant occurrences;
- participant role;
- ordinal when governed;
- multiplicity index/key;
- exact rule-declared cardinality and same-route-reuse policy;
- exact source composition/compatibility authority when required;
- semantic payload;
- typed outcome state;
- producer use-permission ceiling.

V556 may not re-ID or reconstruct a V555 route. Final M4 must substitute the **M3-accepted** exact participant/reference binding.

## 4. Corrected upstream transitive closure

A structural root can depend transitively on corrected upstream empirical authority. When the producer/reference contract declares the dependency interpretation-critical, the closure may need exact immutable resolution of:

- `StructuralEmpiricalAdmission`;
- exact admitted `EmpiricalFact` identity/result binding;
- exact `QuerySpec` / query AST identity;
- exact source universe / risk set / routing authority;
- exact measure / weight / design / estimand authority;
- exact support/uncertainty state;
- exact historical authority snapshots;
- operation-specific source equivalence/linkage/pooling/composition authority when a producer actually claims such an operation;
- exact replay/C11 content identity to the extent required by the replay claim.

The repository does not become semantic owner of these objects.

### Structural standalone resolution is not full empirical replay

M4 must preserve the distinction:

- **Standalone structural resolution:** raw structural stage directories are absent; producer structural semantics and every interpretation-critical authority/reference resolve exactly from the immutable package or exact hash-bound locators.
- **Full offline empirical replay:** additionally requires exact historical empirical substrate/material or an exact immutable content-addressed resolver sufficient to reproduce the governed upstream computation under the historical authority/risk-set/measure inputs.

A stored hash alone cannot support a claim of full offline replay if the exact historical content is not resolvable.

## 5. Strong-reference algorithm

For each published root:

1. verify producer family/object ID/hash/build/schema and exact local/final contract binding;
2. verify producer permission ceiling;
3. verify V557 governance record and publication/use decision;
4. start from producer/reference-contract-declared interpretation-critical references only;
5. for each strong reference, verify exact reference-contract ID/version/hash;
6. preserve edge role and requiredness;
7. preserve participant role/cardinality/multiplicity/order metadata;
8. resolve exactly one target unless producer law explicitly permits governed multiplicity;
9. verify target identity/hash/version/schema;
10. recurse only through target-declared interpretation-critical semantic references;
11. bind every root closure digest;
12. verify publication/repository atomic identity before any consumer visibility;
13. build only reversible logical indexes over producer-preserving locators;
14. during query resolution, dereference/reverify each candidate before semantic selection;
15. apply `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`;
16. emit a `SelectionRecord` for every considered candidate;
17. preserve unresolved, denied, negative, noncomparable and valid-empty states exactly;
18. never repair a failed step from raw dirs, network, `latest`, fuzzy labels, score, embeddings, LLM output or implementation defaults.

## 6. Required fail-closed distinctions

### 6.1 Packaging/integrity failures

Representative packaging failures include:

- missing required transitive dependency;
- ambiguous strong reference;
- object hash mismatch;
- producer identity/version mismatch;
- reference role corruption;
- cardinality mismatch;
- multiplicity loss;
- semantic-order corruption;
- closure-digest mismatch;
- governance binding missing;
- permission widening;
- locator not reversible to producer tuple;
- unsupported/unbound version;
- mutable-latest identity attempt;
- partial atomic publication/repository;
- partial n-ary object exposure;
- V558 repair attempt.

These are `INTEGRITY_FAILURE` class failures. They are not producer semantic negatives.

### 6.2 Producer semantic states

Producer states may include, according to producer contract:

- positive support/eligibility/authorized route;
- explicit denial;
- negative or temporal-limit authority;
- missing semantic authority;
- noncomparability;
- unknown/conflicting authority;
- valid-empty;
- unresolved participant/identity state.

These states are preserved only after their exact producer object/reference/authority closure verifies.

### 6.3 Forbidden state rewrites

M4 must reject:

- physical missing file -> producer `MISSING_AUTHORITY`;
- empty index -> `VALID_EMPTY`;
- hash mismatch -> producer `DENIED`;
- missing participant -> smaller positive n-ary relation;
- missing negative object -> assumed absence of positive relation;
- noncomparability -> zero/false;
- valid-empty -> failure;
- integrity failure -> semantic negative.

## 7. Permission preflight

For every root and dependency, record all three layers:

1. producer permission / use ceiling;
2. V557 item publication/use state and expanded allowed-use set;
3. resolver query-relative allowed-use set.

The only lawful direction is narrowing.

Repository presence, index membership, collection readiness, root authorization or co-resolved dependency never grants a missing capability.

If a root is `ACTIVE_CAUSAL` but a dependency is review-only/context-only/denied, the dependency keeps its own state. A consumer must fail/defer/narrow according to the exact dependency contract; it may not inherit the root's capability.

## 8. Reference-class preflight

### Structural roots allowed in principle

Only exact producer-bound V553/V554/V555/V556 structural producer objects are structural publication root candidates under SCR5578.

### Reference-only corrected upstream classes

Only when producer/reference-contract authority declares them interpretation-critical:

- StructuralEmpiricalAdmission;
- EmpiricalFact;
- QuerySpec;
- Universe/risk-set;
- measure/weight/estimand authority.

### Audit-only

- DiscoveryResultReceipt;
- ReplayReceipt.

### Must not appear in structural repository semantics

- PSEPF / PositionedSubjectEmpiricalPossibilityField;
- ActorComparatorReceipt;
- V3EmpiricalPossibilityInput;
- rendered expression/persona.

Any attempted PSEPF insertion fails the structural-reference-class firewall; it is not repaired or retyped.

## 9. Provenance/source preflight

A reference graph can prove that two sources are reachable. It cannot prove they may be combined.

Positive cross-source semantics require exact operation-specific authority covering the exact source-universe refs and exact participants.

The following never suffice alone:

- same labels;
- same denominator;
- same time;
- same geography;
- same stratum;
- same endpoint;
- adjacency;
- co-resolution;
- common provenance ancestor;
- byte-equal displayed result.

Absent exact positive authority, preserve separation or the exact producer denial/noncomparability/unknown/conflict state.

## 10. Atomicity preflight

A publication or repository is visible/consumable only after all identity, material, governance, closure, locator, graph, index, negative/fidelity and policy bindings verify as one immutable unit.

The following are forbidden:

- exposing a verified subset while another required root/dependency is missing;
- exposing a valid n-ary V556 object with one participant unresolved;
- using global readiness to hide an item-level failure;
- repairing an immutable bundle in place.

Any bound change creates a new immutable identity.

## 11. Deterministic resolver preflight

The resolver operates only over exact immutable inputs:

- repository bundle ID/content hash;
- index manifest ID/hash;
- ContextQuery ID/hash;
- resolver policy ID/version/hash;
- accepted generated-position binding refs/hashes where applicable.

Forbidden semantic inputs include wall clock, mutable latest/current/default, file/database/process order, raw-stage availability, network state, ambient randomness, LLM/embedding judgment and unrecorded cache state.

Identical exact inputs must yield identical considered candidates, SelectionRecords, resolution receipt and ResolvedStructuralContext identity/hash.

## 12. Final M2/M3 seam boundary

Preflight does not fill final V555/V556 producer slots from the local branches.

Final M4 must first receive the exact accepted M2/M3 outputs listed in `FINAL_M2_M3_BINDING_SLOTS.json`, then rerun:

- V555 route identity/reference checksum;
- V556 participant/reference checksum;
- mixed-producer registry checksum;
- raw-directories-absent standalone closure fixture;
- item-wise permission monotonicity fixture;
- role/order/cardinality/multiplicity fixture;
- PSEPF/reference-class firewall;
- provenance-not-composition fixture;
- deterministic replay fixture.

No other SCR5578 local semantic change is authorized by this preflight.

Preflight disposition: `M4_PREFLIGHT_COMPLETE`.
