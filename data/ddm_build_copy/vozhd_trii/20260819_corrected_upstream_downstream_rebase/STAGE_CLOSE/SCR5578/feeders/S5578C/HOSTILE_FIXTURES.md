# S5578C — HOSTILE STANDALONE CLOSURE / LOCATOR / NEGATIVE-REFERENCE FIXTURES

**Authority:** non-dispositive feeder evidence for `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION` and later M4/M5.  
**Broad topology:** frozen by R03 synthesis; these fixtures must not add/remove a broad owner or edge.  
**Production implementation:** not authorized.

## 1. Common fixture harness

Every fixture constructs or mutates an immutable-candidate V557/V558 package with these conceptual surfaces:

```text
V557_IMMUTABLE_PUBLICATION_BUNDLE
  -> V557_IMMUTABLE_PUBLICATION_MANIFEST
  -> CAN-003 item governance records + collection manifests
  -> V557_TRANSITIVE_SEMANTIC_CLOSURE_MANIFEST
  -> producer material store / exact external immutable locator contracts

V558_STRUCTURAL_PRIOR_REPOSITORY_BUNDLE_MANIFEST
  -> producer-preserving locator registry
  -> typed reference graph
  -> logical index manifests
  -> collection fidelity/negative manifest
  -> immutable producer material / external hash-bound leaves
  -> exact resolver-policy binding

ContextQuery + exact generated bindings
  -> ContextResolver
  -> SelectionRecord[] + resolution receipt
  -> ResolvedStructuralContext
```

Unless a fixture explicitly tests full empirical replay, raw V553–V556 stage directories are removed before resolver execution. Network lookup, mutable `latest`, filesystem search and raw-stage fallback are disabled.

A passing harness must distinguish:

1. producer-owned semantic/negative state;
2. V557 permission/governance state;
3. V558 packaging/integrity state;
4. query-relative resolver decision state.

A packaging/reference failure is never rewritten as producer `MISSING_AUTHORITY`, `NONCOMPARABLE`, `VALID_EMPTY`, `NEGATIVE_AUTHORITY`, false, zero or neutral.

---

## FX-S5578C-01 — standalone success with raw producer directories absent

### Setup

Publish a mixed producer set:

- one V553 temporal relation root;
- one V554 affordance root depending on a V553 temporal basis plus a `StructuralEmpiricalAdmission`;
- one V555 atomic route root with exact source/mediator/receiver ordering;
- one V556 n-ary F1 root referencing three exact V555 routes with role/cardinality/order semantics;
- one V556 F2 prerequisite topology referencing V555 routes and one V556 F1.

Each root has complete CAN-003 governance and exact per-root transitive closure. Delete/mount-away all raw V553/V554/V555/V556 directories.

### Required proof

For every root and interpretation-critical dependency:

- exact producer tuple reverses from locator;
- object/material hash verifies;
- governing authority version/hash verifies;
- typed reference edge verifies;
- negative/limit nodes verify;
- repository logical indexes resolve only bundle locators;
- resolver returns identical selected/rejected/deferred refs and receipt hashes across repeated runs.

### Pass condition

`STANDALONE_EXACT_RESOLUTION_PASS`.

Any raw-stage access means fixture failure even if output is numerically/structurally identical.

---

## FX-S5578C-02 — broken path locator masked by surviving filename

### Mutation

Replace an exact content-addressed route locator with:

`../V555/latest/v555_routes.parquet#route-17`

Leave a file with that name available during the first run, then remove raw stage directories.

### Required result

The bundle fails admission/linking or resolver dereference as `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`, `LOCATOR_NOT_REVERSIBLE`, or the exact canonical equivalent. It may not search the filesystem, choose a new V555 build, or treat the path as historical identity.

---

## FX-S5578C-03 — same producer ID, changed hash

### Mutation

Keep `authoritative_object_id = route-17` but substitute bytes from a modified route object while retaining the original declared hash.

### Required result

`OBJECT_HASH_MISMATCH` / integrity failure. The route cannot be selected, repaired or accepted because its ID matches.

A second variant changes both bytes and declared hash while keeping the old immutable publication/repository identity. Required result: `IN_PLACE_MUTATION_ATTEMPT` or bundle identity/content mismatch.

---

## FX-S5578C-04 — historical rule version silently replaced by current

### Setup

A V554 affordance and descendant V555 route were produced under:

`AFFORDANCE_RULE@1.2 / hash-A`.

Current registry contains:

`AFFORDANCE_RULE@1.3 / hash-B`.

Remove `1.2/hash-A` from local mutable registry but preserve the descendant objects.

### Required result

Historical interpretation fails closed unless `1.2/hash-A` is packaged or exactly immutable-addressable through the bundle's declared external resolution contract.

Forbidden outcomes:

- same logical rule name resolves to 1.3;
- newest version wins;
- current wall clock chooses authority;
- compatibility is inferred from schema similarity.

---

## FX-S5578C-05 — missing temporal negative while positive descendant survives

### Setup

A V554/V555 root is transitively constrained by a V553 `TEMPORAL_LIMIT`/noncomparability object for exact key/use scope. Delete only the negative/limit node or its edge from closure while retaining the positive descendant.

### Required result

Root closure fails as an integrity failure. Resolver may not interpret absence of the limit as permission or direct support.

The fixture must distinguish:

```text
producer TEMPORAL_LIMIT / NONCOMPARABLE
!=
packaging MISSING_REQUIRED_TRANSITIVE_DEPENDENCY
```

---

## FX-S5578C-06 — valid-empty versus missing closure

### Variant A — governed valid empty

A V556 collection manifest explicitly declares `VALID_EMPTY_NO_GOVERNED_RULE`, exact zero object count and complete governance/closure inventory.

**Required result:** repository and resolver preserve successful typed empty; no filler V556 object is created.

### Variant B — zero roots because the V556 manifest or required dependency is missing

**Required result:** integrity/missing-authority state, not `VALID_EMPTY`.

This fixture prevents reference minimization from silently converting unknown/broken packaging into semantic emptiness.

---

## FX-S5578C-07 — n-ary participant cardinality loss

### Setup

A V556 F1 has three V555 route participants with producer-declared roles and cardinality `3`.

### Mutations

1. remove one participant edge;
2. keep all locator targets but erase `participant_role`;
3. replace `declared_cardinality=3` with `2`;
4. split the F1 into three dyads;
5. preserve target hashes but change multiplicity key.

### Required result

All semantic-loss variants fail `CARDINALITY_MISMATCH` and/or `REFERENCE_ROLE_CORRUPTION`. Dyadization is not a compatible representation unless separate producer authority explicitly created the dyads.

---

## FX-S5578C-08 — semantic order versus serialization order

### Setup

Use one ordered V555 route and one V556 object whose producer declares order significant.

### Mutations

- sort participant locator IDs lexicographically;
- shuffle JSON/Parquet row order;
- drop semantic ordinals and rely on stored array position.

### Required result

If producer semantic order changes or becomes unrecoverable: `SEMANTIC_ORDER_CORRUPTION` and closure digest mismatch.

A control variant with `order_significant=false` may canonical-sort for deterministic bytes without creating semantic order.

---

## FX-S5578C-09 — V558 producer re-ID

### Mutation

Create locator `LOC-999`, then expose it downstream as `structural_edge_id=LOC-999`, omitting the authoritative V555 route ID/hash.

### Required result

Reject as producer reownership / `LOCATOR_NOT_REVERSIBLE`. V558 administrative IDs may identify lookup records only. Exact producer ID/hash remains semantic identity.

Byte-identical objects from distinct producer identities must also remain distinct unless an independent semantic equivalence authority explicitly permits coalescing.

---

## FX-S5578C-10 — permission widening by repository membership

### Setup

Create three producer/V557 items:

- A: producer `ALLOW_CONTEXT_ONLY`, V557 `ALLOW_CONTEXT_ONLY`;
- B: producer `ALLOW_REVIEW_ONLY`, V557 `ALLOW_REVIEW_ONLY`;
- C: producer `DENY_CAUSAL_USE`, V557 `DENY_CAUSAL_USE`.

Put all three in a valid repository and query `ACTIVE_CAUSAL`.

### Required result

None becomes active causal solely because the repository is valid or an index returns it.

The invariant must be checked item-wise:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`.

Any widening is `FORBIDDEN_PERMISSION_WIDENING` / governance integrity failure.

---

## FX-S5578C-11 — active root does not promote dependency permission

### Setup

A root published for active causal context has an interpretation/provenance dependency whose own CAN-003 state is review-only or denied as an independently selectable runtime object.

### Required result

The dependency stays review-only/denied for independent runtime use. Closure accessibility for exact interpretation/audit does not inherit root permission and does not create a second active prior.

This fixture separates **reference availability** from **runtime-use permission**.

---

## FX-S5578C-12 — provenance-as-composition attack

### Setup

Two independent source universes U-A and U-B support structural lineages that become reachable in one resolved structural context. No operation-specific pooling, respondent-linkage or cross-source composition authority exists.

### Attack

A hostile resolver or repository linker computes one pooled structural result because both provenance chains are available.

### Required result

Reject. Provenance proves origin/reachability only.

The following remain distinct authorities:

```text
SOURCE_SEMANTIC_EQUIVALENCE
RESPONDENT_IDENTITY_LINKAGE
SAMPLE_POOLING_AUTHORITY
CROSS_SOURCE_COMPOSITION_AUTHORITY
```

No one is implied by another or by co-resolution.

---

## FX-S5578C-13 — source-universe collision under identical labels

### Setup

U-A and U-B contain:

- same display source label;
- same harmonized question label;
- respondent display ID `0007` in both universes;
- conflicting empirical results.

### Required result

Exact `EmpiricalUniverse` IDs/respondent namespaces keep them distinct. No join, averaging, winner selection or dedup follows from the shared labels.

If a structural root claims a cross-universe relation, its exact operation-specific relation authority must be present in closure. Otherwise fail closed or preserve separate/noncomparable lineages.

---

## FX-S5578C-14 — query/risk-set/measure convenience-copy removal

### Setup

A structural root descends from an admitted weighted empirical fact. Remove copied percentage, denominator, QuerySpec and weight fields from V555/V556 rows.

Preserve exact transitive objects:

- `StructuralEmpiricalAdmission`;
- `EmpiricalFact`;
- `EmpiricalQuerySpec` target/predicate/topology;
- exact universe;
- risk-set/routing authority and member-set incidence or deterministic member-set rule;
- measure/weight/design/estimand authority;
- support/uncertainty state;
- historical authority snapshots.

### Required result

Standalone interpretation/replay provenance remains exact. Then mutate by dropping the risk-set or measure authority while keeping the same displayed scalar.

Required failure: `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`. Equal numeric result is not semantic equivalence.

---

## FX-S5578C-15 — PSEPF smuggling through generic governance wrapper

### Setup

Create a valid PSEPF object and a syntactically valid-looking V557 `RUNTIME_AUTHORIZED_OBJECT_RECORD` that calls its collection kind `GENERIC_PRIOR`.

### Attack

Attempt to add a V558 producer-preserving locator and index it into `StructuralPriorRepository`.

### Required result

Reference-class validation identifies the authoritative object class/owner and rejects it before structural repository admission. V557 permission cannot convert empirical possibility into structural ontology.

The same rejection applies to standalone `ActorComparatorReceipt` and `V3EmpiricalPossibilityInput` as structural priors.

No rename/wrapper/locator may bypass the class firewall.

---

## FX-S5578C-16 — latest/fuzzy repair cascade

### Setup

Break a required authority/object locator. Offer four tempting alternatives:

1. same-name newer authority;
2. nearest geography object;
3. highest score/confidence object;
4. embedding/LLM-similar object from another producer build.

### Required result

All alternatives are rejected. The exact missing/broken dependency remains in failure evidence. No semantic object is synthesized.

---

## FX-S5578C-17 — ambiguous strong reference

### Setup

A producer reference contract requires exactly one target. Corrupt the locator table so the reference resolves to two incompatible targets.

### Required result

`AMBIGUOUS_REQUIRED_TRANSITIVE_DEPENDENCY`; no first-row, lexicographic, score, current or latest winner.

Control variant: if producer law explicitly authorizes multiplicity, preserve the full role-qualified set and its cardinality/order semantics rather than choosing one.

---

## FX-S5578C-18 — index hit must dereference and reverify

### Mutation

Make the logical index internally consistent but point one key to a locator whose producer bytes/hash or governance binding is invalid.

### Required result

Resolver does not treat index membership as semantic authority. It dereferences and re-verifies object identity/hash/schema/reference closure and item permission, then fails closed.

---

## FX-S5578C-19 — co-resolution does not create V556 meaning

### Setup

Two V555 routes resolve in the same query with compatible geography/time/strata. No V556 F1/F2 exists and no V556 rule authorizes a relation.

### Required result

Both routes may be returned according to their own permissions, but ContextResolver creates no interaction, competition, reinforcement, rerouting or topology object.

`CO_RESOLUTION != COMPOSITION_AUTHORITY`.

---

## FX-S5578C-20 — temporal-limit scope cannot leak

### Setup

A negative/temporal-limit object governs semantic key A only. Key B has separate evidence.

### Attacks

1. omit the A limit, allowing A;
2. apply the A limit to B;
3. treat noncomparability as contradiction/zero;
4. select nearest prior/post despite an exact limit blocking proxy use.

### Required result

The limit's exact scope survives and only narrows the governed key/use. No overbroad denial and no underbypass.

---

## FX-S5578C-21 — full offline replay claim versus structural standalone claim

### Variant A — structural standalone only

Bundle contains exact canonical structural producer material/locators, historical authority objects, admission/fact/query/universe/measure identities and C11 content/replay hash bindings, but not respondent-event rows.

**Required result:** structural context resolution may pass if all interpretation-critical structural dependencies resolve exactly. The bundle may not claim full empirical recomputation.

### Variant B — full offline empirical replay claimed

Exact C11 historical content is unavailable and the C11 hash has no immutable resolver/material contract.

**Required result:** `REPLAY_INPUT_MISSING` / historical replay unavailable. Current C11 may not substitute.

---

## FX-S5578C-22 — arbitrary provenance mention is not a semantic edge

### Setup

A producer object's audit note/prose mentions another object and a PSEPF ID, but the producer schema/reference contract does not declare either as interpretation-critical semantic reference.

### Required result

Closure walker does not follow those mentions. This prevents both closure bloat and PSEPF/provenance smuggling.

If a producer reference contract later declares a reference semantic, the exact version/hash of that contract changes closure identity.

---

## FX-S5578C-23 — partial atomic publication

### Setup

Expose repository manifest/indexes before all producer material, CAN-003 records and closure digests verify. Global readiness is set true.

### Required result

No partial visibility. `PARTIAL_ATOMIC_PUBLICATION` / invalid fail-closed. Completion requires a new valid immutable bundle; no in-place repair.

---

## FX-S5578C-24 — resolver policy mutation under same repository identity

### Setup

Create a repository bound to `V558_CONTEXT_RESOLVER_POLICY@1.0/hash-A`, then switch a mutable pointer to same-version `hash-B` or a newer policy while retaining repository ID.

### Required result

Policy mismatch/repository identity failure. Any accepted policy binding change creates a new repository identity.

---

## 2. Mandatory assertions shared by all fixtures

Every hostile harness should assert all applicable invariants below:

```text
producer_semantic_id == exact original producer id/hash
locator_id != producer semantic identity
resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses
index_hit != semantic authority
provenance_reachability != composition permission
raw_stage_directory_access == forbidden
network_lookup == forbidden
mutable_latest == forbidden
fuzzy_or_embedding_repair == forbidden
PSEPF in structural repository == forbidden
negative/limit/noncomparable/missing/valid-empty/integrity states remain typed
genuinely n-ary producer meaning remains n-ary
producer semantic order survives when order_significant=true
same exact bundle/query/policy/bindings => same semantic result and replay hashes
```

## 3. M4 / M5 use

For **M4**, parent should run these fixtures against the final SCR553/554/555/556 producer contracts and ensure every producer reference-class obligation is represented by an exact closure edge or explicit `MUST_NOT_APPEAR` classification.

For **M5**, parent should reuse the PSEPF-smuggling, permission, producer-identity and resolver-determinism fixtures to prove `ResolvedStructuralContext` remains a structural peer prior and never becomes a conduit for the empirical-possibility lane or actor-state invention.

These fixtures propose tests only. They do not adjudicate SCR5578, M4 or M5.
