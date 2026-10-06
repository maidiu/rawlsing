# PYAT HQ224 — N10E EXACT-DETERMINANT LIFECYCLE HOSTILE REREVIEW — R1

**DISPOSITION:** `N10E_EXACT_DETERMINANT_LIFECYCLE_AUTHORITY_OVERREACH`

**REVIEW BRANCH:** `agent/reviewer-pyat-hq224-n10e-exact-determinant-lifecycle-r1`  
**COMMISSION TIP / REVIEW PARENT:** `df754e3685aa0a923ed568f8117e9a89720c2f87`  
**CANDIDATE:** `agent/rabochii-pyat-hq223-n10e-exact-determinant-lifecycle-repair-r1 @ 22a868cede42b9c92dc78ef746f89ba85d6d8189`  
**PRIOR REVIEW:** `bdf025b3a412560db17224813a822ad64e283229`

## Verdict

HQ223 adds a real graph-mechanics improvement, but its claimed AT19 closure is not admissible.

The positive N10E provider → analytical composition → producer-derived slice → positioned-subject consumer path remains alive. The new adapter can also emit a genuine two-hop path, governed authority root → exact determinant → N10E product, **when** a caller supplies a correct `ExactDeterminantOwnership`.

The candidate nevertheless fails the hostile rereview for five reasons.

### 1. The old reachability defect remains legal and remains the actual fresh-runner shape

`AnalyticalProductRegistration.determinant_ownerships` defaults to empty. The constructor checks that supplied ownership rows refer to consumed refs, but never checks the converse: every `determinant_exact_ref` need not have an ownership row.

Therefore exact query/predicate/consumer/witness refs can still be serialized and silently ignored by `build_graph()`.

The candidate explicitly reports `existing_registration_still_works_without_ownerships = true`.

More importantly, `n10e_provider_replay_lifecycle_runner.py` still registers four `determinant_exact_refs` and **no `determinant_ownerships`**. Its actual lifecycle path remains model-authority-only. The repaired census exists only in the court's private `_census_registry()`.

### 2. The consumed determinant census is incomplete

The provider request explicitly identity-binds query, predicate, release refs, consumer query, binding fingerprint, model-rule hash, witness ref, **source-universe ref**, and target ref. Analytical composition executes and consumes an exact `EmpiricalFact`, verifies source-universe/release/target relations, and the provider receipt carries `producer_fact_ref`, source universes, releases, query/predicate/consumer/witness identities and model rule.

HQ223's test census registers only query, predicate, consumer query, witness, release and target.

It omits at least:

- the exact source-universe ref, which HQ223's own return says has a stageable `C1-AT07-SOURCE` root;
- the exact producer `EmpiricalFact` ref, the natural `DEPENDENT_PRODUCT_DETERMINANT` case;
- conditioner-binding exact material including subject-fact and empirical-coordinate refs.

Under AT19, the missing stageable source-universe edge is a failed cross-owner dependency.

### 3. The new query/predicate governed-change witness impersonates the sealed successor authority

`_query_authority_revision()` correctly asks `AuthorityMaintenanceExecutor` to adjudicate and seal a `C1-AT07-QUERY@2.0.0` candidate.

But `_rebuild_under_query_authority()` does **not** consume that sealed snapshot.

Instead it clones the old fixture query-authority semantic fields, changes only version, interpretation fingerprint, and `authority_content_hash`, then assigns the sealed successor's content hash to that different body and puts it in a fresh `AuthorityRegistry`.

The sealed candidate material differs in scope envelope, effective time, parent/supersession refs, replay protocol, dependencies/provenance and other fields.

The public `AuthoritySnapshot` validator checks that the hash field is syntactically SHA-256; it does not recompute the authority content hash from the snapshot body. `AuthorityRegistry` keys by the exposed `authority_ref`. Consequently the cloned old body can impersonate the sealed successor exact key.

That is fixture self-authorization / authority-identity laundering, not proof that the governed sealed successor drives the recomputation.

### 4. The predicate lifecycle replacement is actually a query ref

`test_r03` registers one determinant callback for both the empirical query and empirical predicate, and that callback always returns `rebuilt["query"].ref`.

The candidate's own `03_AT19_SELECTIVE_INVALIDATION_COURT.json` exposes:

- old `EmpiricalQuerySpec@1.0.0` → new `EmpiricalQuerySpec@1.0.0`;
- old `EmpiricalPredicate@1.0.0` → the **same new EmpiricalQuerySpec@1.0.0`.

The actual rebuilt predicate ref is never recorded as the predicate replacement. The accepted owner checks only new-ref inequality, not family continuity, so the malformed replacement passes.

The claim that query, predicate and N10E product each received a real recomputed exact replacement is therefore false for the predicate.

### 5. Determinant ownership is caller-asserted, not production-bound to the determinant

`ExactDeterminantOwnership` checks that rooted owners are `AuthorityRef` objects and nonempty. It does not prove that those owners are recorded on the determinant.

The court's `test_r12` also uses one global union of owner refs recorded anywhere across query, predicate, binding and witness. It does not verify owner evidence per determinant.

No direct ExactRef→AuthorityRef coercion was found, but an arbitrary existing AuthorityRef can still be attached to the wrong determinant and manufacture a reachable root edge.

## What does survive

Inside the specially classified test registry, the graph traversal mechanics are genuine:

- `SemanticDeterminantGraph.affected()` reaches determinant and product;
- deleting owner→determinant removes the seed;
- deleting determinant→product removes downstream reachability;
- a separately registered nonconsumer stays unaffected.

The underlying positive path also remains intact:

`exact fixture determinants -> provide_empirical_possibility_slice -> compose_positioned_subject_possibility -> producer-derived PossibilitySliceEvidence -> evaluate_positioned_subject_possibility`.

The candidate did not mutate provider, composition, consumer, authority maintenance, learned lifecycle/release, or live C4/C7.

The HQ222 documentary corrections are materially present: producer/provider paths are separated; H02 uses one measured nonzero subprocess code; H12 no longer claims an observed exception.

This Browser/GitHub reviewer did not rerun pytest, so “188 passed” remains candidate-reported execution evidence.

## Named remaining limitations

- **C11LogicalRelease release ref:** `UPSTREAM_OWNER_CONTRACT_BLOCKER`. It is consumed and unowned; HQ223 correctly refuses to invent an authority.
- **Comparability root:** `UPSTREAM_AUTHORITY_MATERIAL_BLOCKER`. A recorded comparability ref exists, but installed material is not a full `AuthoritySnapshot` and no current authority kind names comparability. Reachability shape exists; governed revision proof does not.
- **Affected-but-identical recomputation:** `ACCEPTED_OWNER_CONTRACT_LIMITATION`. `AuthorityMaintenanceExecutor._recompile` rejects unchanged exact refs categorically. HQ223 states this honestly; it is not the cause of rejection.

## Required next repair

A successor must, at minimum:

- require every registered consumed exact determinant to be classified or explicitly refused;
- wire the classified registry into the actual N10E lifecycle path, not only a private court helper;
- include source-universe and upstream EmpiricalFact dependency classes and finish the binding census;
- consume the **actual sealed successor snapshot** in the query/predicate revision witness;
- return `rebuilt["predicate"].ref` for the predicate;
- enforce replacement family compatibility;
- bind each determinant owner to determinant-specific recorded owner evidence.

**TERMINAL:** `N10E_EXACT_DETERMINANT_LIFECYCLE_AUTHORITY_OVERREACH`
