# CAN-004 — Immutable V557 Publication → V558 Repository Bundle Policy

**Assignment:** `W2-B02-01`  
**Decision packet:** `CAN-004`  
**Canonical authority:** `V557_V558_IMMUTABLE_PUBLICATION_REPOSITORY_BUNDLE_POLICY@1.0.0`  
**Owner:** `V557_V558_PUBLICATION_REPOSITORY_BOUNDARY`  
**Semantic owner:** `NONE__PRODUCER_OWNERSHIP_IS_PRESERVED`  
**Repository / branch:** `maidiu/rawlsing` / `agent/vozhd-dva-w2-can-004-publication-repository-bundle`  
**Exact launch base:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**Mode:** canonicalization only; no production code; no V557/V558 implementation  
**Historical ZIP:** `NOT_AUTHORIZED_NOT_USED`  
**Verdict:** `PASS`

## 1. Holding

CAN-004 canonicalizes the immutable packaging boundary between V557 publication and the V558 `StructuralPriorRepository` without creating, renaming, repairing or semantically interpreting any producer-owned structural object.

The binding invariant is:

```text
PRODUCER OBJECT / RULE / PREDICATE / REFERENCE CONTRACT
  + exact producer identity/version/hash
  + CAN-003 item-use governance
  + role-preserving transitive semantic closure
  -> immutable V557 publication bundle
  -> integrity verification only
  -> immutable V558 repository bundle
```

The nonidentity law is:

```text
PRODUCER OBJECT ID
!= V557 GOVERNANCE RECORD ID
!= V557 PUBLICATION BUNDLE ID
!= V558 LOCATOR ID
!= V558 INDEX ID

PUBLICATION MEMBERSHIP
!= CAUSAL-USE PERMISSION

COLLECTION READY
!= ITEM ALLOWED

REFERENCE GRAPH ARC
!= NEW STRUCTURAL RELATION
```

V557 publishes producer meaning under bounded runtime-use governance. V558 links and indexes that already-valid publication. V558 may not repair an invalid publication, replace producer identity with repository identity, flatten producer epistemic/use state, or infer a missing semantic dependency.

A valid-empty collection or valid-empty publication is lawful. No filler object is created.

## 2. Evidence inspected

No historical ZIP was authorized or used.

Direct accepted/current evidence inspected at the exact W2 Batch-02 base included:

- `schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/BATCH_02_LAUNCH_REGISTER.md`;
- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`;
- `integration/W1_AUTHORITY_EXPANSION_CLOSURE_RULING.md`;
- `integration/W2_FIRST_BATCH_ADJUDICATION_RULING.md`;
- `integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`;
- accepted `CAN-003 / V557 runtime publication/use governance` authority;
- accepted `CAN-006 / V3_GENERATED_POSITION_BINDING_CONTRACT@1.0.0` for the same-repository Phase-A/Phase-B identity invariant only;
- accepted SI-R03 V556→V557 hostile seam result, especially role-preserving transitive semantic closure;
- accepted SI-R04 V557→V558 hostile seam result, especially immutable handoff/repository identity and no-repair law;
- RA-R00 release synthesis `RESULT.md` / `RESULT.json`;
- current `data/ddm_build_copy/ddm_v557_renderer_contract.py`;
- current `data/ddm_build_copy/ddm_v558_plus_governance.py`.

Focused base-code searches found no direct current test file naming either stale production surface. No semantic authority is inferred from that absence. The accepted seam courts and CAN-003 invariants remain the binding test/evidence layer for this canonicalization.

No sibling W2 Batch-02 result was consumed as authority.

## 3. Jurisdiction

CAN-004 owns only the administrative-integrity contract required to move an already-governed V557 publication into an immutable V558 repository:

1. immutable publication bundle and manifest packaging;
2. content-addressed publication identity and hashes;
3. producer-preserving locators;
4. exact transitive semantic-closure packaging and closure digests;
5. preservation of producer role/cardinality/order semantics;
6. exact binding of CAN-003 item and collection governance;
7. publication→repository handoff identity;
8. immutable repository bundle/manifest integrity envelope;
9. exact version/compatibility gating at this seam;
10. atomic visibility, fail-closed integrity and deterministic replay.

CAN-004 does **not** own:

- any producer domain-semantic family, ontology, rule or predicate;
- producer object identity;
- CAN-003 permission or item-use semantics;
- resolver selection, proxy, applicability or ranking logic;
- CAN-005 semantics or any sibling Batch-02 result;
- V3 generated facts/history or V2 rendering;
- production implementation of V557 or V558;
- semantic equivalence, fuzzy rematching, defaulting, repair or mutable-`latest` resolution.

Direct consumers are `V557-P4` and `V558-P1`.

## 4. Canonical administrative schemas

These schemas are packaging/linking contracts. They are not new structural semantic families.

### 4.1 `V557_IMMUTABLE_PUBLICATION_BUNDLE@1.0.0`

```text
V557ImmutablePublicationBundle {
  publication_bundle_id,
  bundle_schema_id,
  bundle_schema_version,
  publication_identity_hash,
  publication_content_hash,

  publication_manifest_ref,
  publication_manifest_hash,

  collection_manifest_bindings[],
  object_governance_record_bindings[],
  producer_build_bindings[],

  transitive_closure_manifest_ref,
  transitive_closure_manifest_hash,
  producer_material_store_manifest_ref,
  producer_material_store_manifest_hash,

  can003_authority_binding,
  publication_policy_bindings[],
  compatibility_bindings[],

  atomic_publication_state
}
```

`publication_bundle_id` is administrative content-addressed identity. It never replaces an authoritative producer object ID.

### 4.2 `V557_IMMUTABLE_PUBLICATION_MANIFEST@1.0.0`

```text
V557ImmutablePublicationManifest {
  publication_manifest_id,
  manifest_schema_id,
  manifest_schema_version,
  manifest_hash,
  publication_bundle_id,

  collection_bindings[] {
    can003_collection_manifest_id,
    can003_collection_manifest_hash,
    authoritative_producer_family,
    logical_collection_kind,
    authoritative_build_id,
    authoritative_build_hash,
    exact_object_count,
    collection_state
  },

  root_bindings[] {
    producer_preserving_locator_ref,
    authoritative_object_id,
    authoritative_object_hash,
    runtime_authorized_object_record_id,
    runtime_authorized_object_record_hash,
    root_closure_digest
  },

  producer_build_bindings[],
  policy_bindings[],
  content_inventory_digest,
  transitive_closure_manifest_ref,
  transitive_closure_manifest_hash
}
```

The manifest binds exact CAN-003 collection/item governance by ID+hash. It does not restate that governance as new CAN-004 semantics.

### 4.3 `PRODUCER_PRESERVING_OBJECT_LOCATOR@1.0.0`

```text
ProducerPreservingObjectLocator {
  locator_id,
  logical_collection_kind,

  authoritative_object_id,
  authoritative_object_hash,
  authoritative_producer_family,
  authoritative_build_id,
  authoritative_build_hash,
  producer_schema_id,
  producer_schema_version,
  producer_rule_predicate_reference_contract_bindings[],

  runtime_authorized_object_record_id,
  runtime_authorized_object_record_hash,

  content_blob_hash,
  storage_locator,
  provenance_locator
}
```

`locator_id` and `storage_locator` are nonsemantic. The authoritative producer tuple must be exactly reversible from the locator without prose, fuzzy lookup or a mutable catalog alias.

### 4.4 `V557_TRANSITIVE_SEMANTIC_CLOSURE_MANIFEST@1.0.0`

```text
V557TransitiveSemanticClosureManifest {
  closure_manifest_id,
  closure_schema_id,
  closure_schema_version,
  closure_policy_id,
  closure_policy_version,
  closure_policy_hash,

  root_closures[] {
    root_locator_ref,
    root_authoritative_object_id,
    root_authoritative_object_hash,
    root_governance_record_id,
    root_governance_record_hash,

    closure_nodes[],
    closure_edges[] {
      source_locator_ref,
      target_locator_ref,
      reference_contract_id,
      reference_contract_version,
      reference_contract_hash,
      edge_role,
      requiredness,
      participant_role,
      declared_cardinality,
      multiplicity_key,
      order_significant,
      semantic_ordinal
    },

    root_closure_digest
  },

  aggregate_closure_digest,
  closure_manifest_hash
}
```

Role/cardinality/order values are transported from producer/reference-contract authority. CAN-004 does not invent them.

### 4.5 `V558_STRUCTURAL_PRIOR_REPOSITORY_BUNDLE_MANIFEST@1.0.0`

```text
V558StructuralPriorRepositoryBundleManifest {
  repository_bundle_id,
  repository_schema_id,
  repository_schema_version,
  repository_identity_hash,
  repository_content_hash,

  source_v557_publication_bundle_id,
  source_v557_publication_identity_hash,
  source_v557_publication_content_hash,
  source_publication_manifest_ref,
  source_publication_manifest_hash,
  source_collection_manifest_bindings[],
  producer_build_bindings[],

  object_locator_registry_ref,
  object_locator_registry_hash,
  reference_graph_manifest_ref,
  reference_graph_manifest_hash,
  index_manifest_bindings[],
  collection_fidelity_negative_manifest_ref,
  collection_fidelity_negative_manifest_hash,
  producer_material_store_manifest_ref,
  producer_material_store_manifest_hash,

  publication_policy_bindings[],
  resolver_policy_binding,
  atomic_repository_state
}
```

`resolver_policy_binding` is opaque here. If a separately accepted resolver authority exists, the repository may bind its exact ID/version/hash. CAN-004 supplies no resolver logic, no default and no sibling Batch-02 semantics. Adding or changing such a binding creates a **new repository identity**.

## 5. Immutable identity and hash law

Canonical packaging serialization is `CAN004_CANONICAL_JSON_V1`:

- UTF-8 only;
- object keys in deterministic ascending Unicode scalar-value order;
- no insignificant whitespace;
- strings preserve exact Unicode scalar sequence: no normalization, trimming, case-folding or semantic rewriting;
- administrative integers use canonical base-10 representation;
- semantic arrays preserve producer-declared order;
- an unordered array may be sorted for deterministic bytes only when its governing producer/reference contract explicitly declares `order_significant=false`;
- self-hash fields and volatile transport metadata are excluded from the object they hash.

Canonical digest algorithm is `SHA-256`; textual form is `sha256:<64 lowercase hexadecimal digits>`.

### 5.1 Publication hashes

`publication_content_hash` binds, at minimum:

- canonical publication-manifest content excluding its own self-hash;
- every bound CAN-003 collection-manifest hash;
- every bound runtime-authorized-object-record hash;
- every producer material/blob hash;
- producer build IDs/hashes;
- transitive-closure manifest hash and every root closure digest;
- compatibility bindings;
- publication policy bindings.

`publication_identity_hash` binds:

- `publication_content_hash`;
- publication bundle/manifest schema IDs and versions;
- exact CAN-003 authority ID/version/hash binding;
- producer build identities/hashes;
- closure-policy ID/version/hash;
- all identity-bearing compatibility/policy bindings.

```text
publication_bundle_id = V557PUB:<publication_identity_hash>
```

### 5.2 Repository hashes

`repository_content_hash` binds:

- source V557 publication bundle ID/identity/content/manifest hashes;
- object-locator registry hash;
- reference-graph manifest hash;
- every index-manifest hash;
- collection-fidelity/negative-manifest hash;
- producer-material-store manifest hash;
- producer-build bindings;
- publication-policy bindings;
- opaque separately accepted resolver-policy binding when present.

`repository_identity_hash` binds the repository content hash, repository schema ID/version, source publication identity, and all exact bound authority/policy/version/hash identities.

```text
repository_bundle_id = V558REPO:<repository_identity_hash>
```

### 5.3 Immutability

Any change to producer object bytes/hash, producer build identity, CAN-003 item decision, manifest content, closure node/edge/role/cardinality/order, compatibility binding, bound policy, locator/reference/index material, or repository material creates a new content/identity hash and a new bundle ID.

Existing publication/repository bundles never mutate in place.

Same bundle ID with a different bound hash is `INTEGRITY_FAILURE__IDENTITY_HASH_CONFLICT`.

`latest`, `current`, `default`, filesystem path and wall clock may exist as nonauthoritative discovery/transport metadata. They are forbidden as identity, compatibility or replay authority.

## 6. Producer-preservation proof

Every published/repository object preserves exactly:

- authoritative producer family;
- authoritative object ID and object hash;
- authoritative producer build ID and build hash;
- producer schema ID/version;
- producer rule/predicate/reference-contract IDs/versions/hashes where applicable;
- producer epistemic class;
- producer permission ceiling and exact CAN-003 item-use decision;
- negative/missing/noncomparable/valid-empty state plus exact producer subtype;
- interpretation-critical semantic references;
- role/cardinality/order semantics;
- provenance refs.

V557 governance-record IDs, publication IDs and V558 locator/reference/index IDs are administrative only.

The V558 reference graph records reference arcs; it is not a new domain graph ontology. An index is a reversible access path over immutable producer-preserving locators, not a producer replacement.

Hash equality alone never proves semantic identity. Byte-identical objects with different authoritative producer IDs/build/version authority remain distinct.

The standalone V558 repository must remain resolvable with raw producer directories absent. Every admitted root and every required transitive semantic dependency must resolve from packaged material or an exact packaged content-addressed locator with a hash-bound resolution contract.

## 7. Transitive semantic closure

For each published root, V557 must prove `PER_ROOT_ROLE_PRESERVING_TRANSITIVE_SEMANTIC_CLOSURE` before publication is valid.

### 7.1 What closure follows

Recursively follow only references that producer schema/reference-contract authority declares interpretation-critical. Arbitrary prose, audit notes, comments and incidental provenance mentions are not semantic closure edges unless producer authority explicitly makes them so.

A closure leaf is satisfied only when one of these holds:

1. the target object/material is included and content-addressed in the bundle;
2. the governed authority/rule/predicate/version is included or exactly immutable-addressable under a packaged hash-bound contract; or
3. an explicit external immutable authority locator is packaged with exact identity/version/hash and a resolution contract that does not depend on mutable `latest`, raw-dir availability or fuzzy lookup.

A strong reference that producer law declares singular must resolve to exactly one compatible immutable target. Zero targets or multiple incompatible targets is integrity failure unless that producer/reference contract explicitly authorizes multiplicity or noncomparability.

### 7.2 Role preservation

Closure edges preserve exact producer/reference-contract roles, including where applicable:

`PARTICIPANT`, `TOPOLOGY`, `SOURCE`, `MEDIATOR`, `RECEIVER`, `CONDITION`, `PREDICATE`, `TEMPORAL_SUPPORT`, `TEMPORAL_LIMIT`, `STRATUM`, `ABSOLUTE_HORIZON`, `GEOGRAPHY`, `AUTHORITY`, `RULE`, `PROVENANCE`, `SEMANTIC_ORDER`, `MULTIPLICITY`, `CARDINALITY`.

This list is a packaging role vocabulary, not authorization to add a role absent producer authority.

### 7.3 Cardinality and multiplicity

- Producer-declared cardinality is transported, never re-derived into a new semantic claim.
- Where producer/reference-contract law binds participant cardinality, `declared_cardinality` must equal the number of exact role-qualified participant refs.
- Genuinely n-ary producer objects remain n-ary.
- V557/V558 may not dyadize, collapse, duplicate, synthesize or winner-select participants.
- Duplicate/ambiguous targets are never resolved by list order.

### 7.4 Semantic order

- Producer-declared semantic order is preserved by exact role/ordinal semantics.
- Serialization order is never semantic order.
- Unordered/symmetric sets may sort only for deterministic serialization when `order_significant=false` is already governed.
- Changing an order-significant ordinal or role changes the root closure digest and therefore publication/repository identity.

### 7.5 Closure digest

Each `root_closure_digest` deterministically binds canonical producer-preserving node locators/hashes plus typed reference edges, including reference-contract ID/version/hash, edge role, requiredness, participant role, cardinality/multiplicity, order-significance and semantic ordinal.

The aggregate closure digest binds all root digests under deterministic root ordering. Incidental collection iteration order has no semantic force.

V558 verifies, links and indexes an already-valid closure. It may not fetch raw producer directories, infer omitted edges, fuzzy-rematch labels, synthesize cardinality/order, or repair a failed closure.

## 8. Item-use governance and denial precedence

CAN-003 remains sovereign over producer permission ceilings and V557 item-use decisions.

Canonical precedence is:

1. physical/schema/hash/reference integrity must pass;
2. exact producer identity/version/reference-contract compatibility must pass;
3. producer permission ceiling bound by CAN-003 applies;
4. CAN-003 per-item V557 use decision may only narrow or deny;
5. producer epistemic/negative/missing/noncomparable/valid-empty state remains attached exactly;
6. collection/global readiness and aggregate counts are informational only;
7. V558 ingestion/indexing preserves the exact item state and grants no new use authority;
8. any later resolver may only narrow under its separately accepted policy.

Therefore:

```text
COLLECTION_READY + ITEM_DENY_CAUSAL_USE -> ITEM_DENY_CAUSAL_USE
```

Collection readiness can never override an item denial, missing-authority state, noncomparability, valid-empty state, or producer negative authority.

An active root does not transfer its permission to a dependency. A context-only, review-only or denied dependency retains its own CAN-003 state. Presence in a bundle/repository is not causal admission.

## 9. Semantic-state separation

Producer semantic states are not packaging failures and may not be flattened together:

- `NEGATIVE_AUTHORITY`;
- `MISSING_AUTHORITY`;
- `NONCOMPARABLE`;
- `VALID_EMPTY`;
- `DENY_CAUSAL_USE`;
- `NOT_APPLICABLE`;
- `INTEGRITY_FAILURE`.

A producer-authorized `MISSING_AUTHORITY` object/state is preserved as producer meaning.

By contrast, a required transitive semantic reference that **should** resolve under the publication contract but is physically absent, corrupt or version-incompatible is an integrity failure. V557/V558 may not relabel that packaging failure as producer `MISSING_AUTHORITY`.

## 10. Compatibility and version law

Canonical compatibility states are:

- `EXACT_SUPPORTED`;
- `EXACT_ONE_TO_ONE_COMPATIBILITY_ALIAS`;
- `UNSUPPORTED_VERSION`;
- `VERSION_CONFLICT`;
- `UNBOUND_SEPARATE_AUTHORITY`.

Rules:

1. exact producer/schema/rule/predicate/reference-contract IDs, versions and hashes govern;
2. unknown future versions are not grandfathered by family/name similarity;
3. mutable `latest/current/default` may be discovery metadata only;
4. a compatibility alias is lawful only when already governed as exact one-to-one, lossless and hash-bound;
5. CAN-004 does not author semantic adapters;
6. compatibility may not convert global permission to item permission, scalar/readiness to use state, missing to deny, noncomparable to negative, valid-empty to failure, merge temporal proxies, or widen permission;
7. same bytes under different producer identities/versions do not establish semantic equivalence;
8. any accepted compatibility or policy binding that changes packaged interpretation creates a new immutable publication/repository identity.

Resolver policy remains `UNBOUND_SEPARATE_AUTHORITY` until an exact separately accepted policy ID/version/hash is supplied. CAN-004 does not consume a sibling Batch-02 return.

## 11. Valid and fail-closed states

Top-level bundle/repository states:

- `VALID_NONEMPTY` — all required manifests, governance bindings and closure proofs verify and at least one runtime-published root exists;
- `VALID_EMPTY` — zero runtime-published roots is lawful when exact zero-count manifests/item states/closure inventory are explicit and internally consistent;
- `INVALID_FAIL_CLOSED` — any integrity/version/closure/atomicity requirement fails.

Canonical fail-closed codes:

- `BUNDLE_ID_HASH_MISMATCH`;
- `MANIFEST_HASH_MISMATCH`;
- `OBJECT_HASH_MISMATCH`;
- `PRODUCER_BUILD_HASH_MISMATCH`;
- `PRODUCER_IDENTITY_VERSION_MISMATCH`;
- `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`;
- `AMBIGUOUS_REQUIRED_TRANSITIVE_DEPENDENCY`;
- `REFERENCE_ROLE_CORRUPTION`;
- `CARDINALITY_MISMATCH`;
- `SEMANTIC_ORDER_CORRUPTION`;
- `CLOSURE_DIGEST_MISMATCH`;
- `ITEM_GOVERNANCE_BINDING_MISSING`;
- `FORBIDDEN_PERMISSION_WIDENING`;
- `UNSUPPORTED_SCHEMA_VERSION`;
- `COMPATIBILITY_MAPPING_NOT_EXACT`;
- `LOCATOR_NOT_REVERSIBLE`;
- `IN_PLACE_MUTATION_ATTEMPT`;
- `MUTABLE_LATEST_IDENTITY_ATTEMPT`;
- `PARTIAL_ATOMIC_PUBLICATION`;
- `V558_REPAIR_ATTEMPT`.

None of these may be coerced to valid-empty, producer missing authority, false, zero or an implementation warning.

## 12. Atomicity, replay and provenance

A V557 publication becomes visible/consumable only after bundle identity, manifests, producer material/locators, CAN-003 bindings and closure digests verify as one immutable unit.

A V558 repository becomes visible/consumable only after source-publication identity, object locators, reference graph, indexes, fidelity/negative manifest, material store and bound policy identities verify as one immutable unit.

Partial visibility is forbidden. Completion or repair in place is forbidden; create a new bundle identity.

Deterministic publication replay binds:

- publication bundle ID/identity/content hashes;
- publication manifest ID/hash;
- all CAN-003 item/collection record IDs/hashes;
- producer build/object IDs/hashes;
- closure manifest/root digests;
- exact schema/policy/compatibility authority bindings.

Deterministic repository replay additionally binds:

- repository bundle ID/identity/content hashes;
- source publication ID/identity/content hashes;
- locator/reference/index/fidelity/material manifest hashes;
- opaque separately accepted resolver-policy ID/version/hash if present.

Forbidden replay entropy includes wall clock, filesystem iteration order, raw producer-directory availability, mutable latest/current/default, fuzzy/descriptive matching, LLM inference and unversioned compatibility behavior.

## 13. Hostile fixtures

1. **Same bundle ID, different hash:** → `BUNDLE_ID_HASH_MISMATCH`; fail closed.
2. **Same producer object ID, changed bytes/hash under same publication ID:** → `OBJECT_HASH_MISMATCH` or new bundle; never mutate.
3. **Missing interpretation-critical transitive dependency:** → `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`; V558 cannot repair.
4. **Closure edge role changed while target remains the same:** → `REFERENCE_ROLE_CORRUPTION`.
5. **N-ary producer object dyadized/collapsed or participant multiplicity changed:** → cardinality/role failure; no replacement topology.
6. **Order-significant participant/semantic ordinal reordered:** → `SEMANTIC_ORDER_CORRUPTION`; closure digest changes.
7. **Incidental serialization order changes for governed unordered set:** → canonical bytes may sort only because `order_significant=false`; no semantic order invented.
8. **Collection ready but one item is `DENY_CAUSAL_USE`:** → denial wins.
9. **V558/resolver widens context-only/review-only/deny to active causal:** → `FORBIDDEN_PERMISSION_WIDENING`.
10. **Producer family/object matches but schema/rule/reference-contract version/hash differs:** → version mismatch or exact governed compatibility path; no name-based acceptance.
11. **Governed valid-empty producer collection:** → `VALID_EMPTY`; exact zero count; no filler row.
12. **Publication content/governance changes after publication under same ID:** → `IN_PLACE_MUTATION_ATTEMPT`; new identity required.
13. **`latest` requested as replay identity:** → `MUTABLE_LATEST_IDENTITY_ATTEMPT`.
14. **V558 locator treated as replacement semantic identity:** → reject; producer tuple remains authoritative.
15. **Byte-identical objects from distinct producer identities semantically deduplicated:** → reject semantic coalescing.
16. **V558 repairs closure using raw producer dirs or fuzzy labels:** → `V558_REPAIR_ATTEMPT`; fail closed.
17. **Many-to-one/fuzzy/lossy/unversioned compatibility mapping:** → `COMPATIBILITY_MAPPING_NOT_EXACT`.
18. **Active root depends on context-only/review-only/denied dependency:** → dependency keeps its own item state; no permission inheritance.
19. **Only part of intended publication/repository is visible while readiness says complete:** → `PARTIAL_ATOMIC_PUBLICATION`.
20. **Global/collection readiness overrides item deny/missing/noncomparable/valid-empty:** → reject; item state wins.
21. **Negative, missing, noncomparable and valid-empty collapsed to one null/false:** → reject semantic flattening.
22. **Closure walker follows arbitrary prose/audit mention as semantic dependency:** → do not follow unless producer schema/reference contract declares it interpretation-critical.
23. **CAN-003 decision, closure/publication policy or compatibility binding changes while bundle ID is reused:** → new identity required.
24. **Later separately accepted resolver-policy binding is attached by mutating an existing repository:** → forbidden; new repository bundle.
25. **Target object hash unchanged but edge role/cardinality/order metadata changes:** → closure digest and bundle identity change.
26. **Strong ref resolves to zero or multiple incompatible targets:** → missing/ambiguous required dependency; no arbitrary choice.

## 14. Governing Spirit check

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

The lawful ambiguity was narrow: closed architecture permits standalone V558 resolution from packaged producer material or exact content-addressed locators, while CAN-004 still had to choose exact packaging identity/closure mechanics without creating producer semantics or resolver policy.

The canonical choice is minimum-sufficient content-addressed immutable packaging, exact reversible producer locators, role-preserving transitive closure, per-item governance preservation and atomic fail-closed verification. Lawful empty/negative/missing/noncomparable states remain first-class. Repair, fuzzy identity, semantic coalescing and mutable latest are rejected.

This satisfies the governing principles of bounded jurisdiction, minimum sufficient machinery, downstream authority never exceeding producer authority, preservation of multiplicity/order, lawful absence and immutable replay/provenance.

The Governing Spirit supplies no new structural semantic content.

## 15. Consumer release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_004_IMMUTABLE_BUNDLE_CONTRACT_CLOSED_FOR_V557_P4_AND_V558_P1_AFTER_VOZHD_ACCEPTANCE__NO_V557_OR_V558_PRODUCTION_IMPLEMENTATION_RELEASED`

V557-P4 may implement the immutable publication handoff and V558-P1 may implement the immutable repository linker **after Vozhd acceptance**, subject to all other accepted dependencies. This authority does not release production implementation and does not close CAN-005 or any sibling Batch-02 authority.

## Final token

`CAN_004_IMMUTABLE_PUBLICATION_REPOSITORY_BUNDLE_CANONICALIZATION = PASS`
