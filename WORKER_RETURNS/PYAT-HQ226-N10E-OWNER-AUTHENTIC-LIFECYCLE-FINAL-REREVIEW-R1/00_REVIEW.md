# PYAT HQ226 — N10E OWNER-AUTHENTIC LIFECYCLE FINAL HOSTILE REREVIEW — R1

**DISPOSITION:** `N10E_OWNER_AUTHENTIC_LIFECYCLE_AUTHORITY_OVERREACH`

**REVIEW BRANCH:** `agent/reviewer-pyat-hq226-n10e-owner-authentic-lifecycle-final-rereview-r1`  
**COMMISSION TIP / REVIEW PARENT:** `46a66533b26f37c6ee261ddb0c35e9099df1bacf`  
**CANDIDATE:** `agent/rabochii-pyat-hq225-n10e-owner-authentic-lifecycle-repair-r1 @ b5ba9ebfc7bc8e6c07aa8799ce9c76d64d5ca03d`  
**IMPLEMENTATION HEAD BEFORE RETURN:** `5be967b5e9eb393032726924496368606ebce82c`  
**PRIOR HOSTILE REVIEW:** `1dc665a67d20fac2960a113a7fb3dcaa415f1dc6`  
**MODE:** Browser/GitHub final hostile rereview; read-only candidate; no repair; no self-adoption.

## 1. Verdict

HQ225 materially repairs four important pieces of the HQ224 failure:

- `build_graph()` now fails closed if any registered `determinant_exact_ref` lacks a classification;
- the fresh runner now uses the classified registry rather than the old model-only exact-ref list;
- `DeterminantOwnerEvidence` cryptographically ties the selected exact-determinant owner relation to that determinant's own hashed semantic material;
- the query-revision court now consumes the exact successor snapshot returned by the accepted owner, and cross-family recompilation is refused.

Those repairs are real.

The final rereview nevertheless **rejects adoption** because owner authenticity still fails in the actual runner's model-rule lifecycle, at exactly the authority boundary HQ225 claims to close.

Two source-level defects are decisive:

1. **The actual fresh runner seeds `AuthorityMaintenanceExecutor` with an unauthenticated model-authority snapshot.**  
   `fx.model_authority_snapshot(direction)` copies the base snapshot's `authority_content_hash`, then changes constitutive authority fields including authority ID, authority kind, governed operations, governed object families, parent/supersession material and state. `AuthoritySnapshot.authority_ref` simply exposes that carried hash. Current `validate_authority_snapshot()` verifies only shape/state and SHA syntax; it does not recompute the authority-content hash from the body. `AuthorityMaintenanceExecutor.__init__` therefore accepts the copied-hash snapshot as an exact initial authority.

   This is the same semantic class of defect HQ224 found in the query-revision witness: authority body and exact authority identity are not proved to correspond.

   HQ225's new `assert_authority_snapshot_body_matches_ref()` would detect this class of impersonation, but the actual runner never applies that guard to `fx.model_authority_snapshot()`. It applies the guard only in the separate query-revision court.

2. **The consumed model-rule identity is still not represented or owner-authenticated in the dependency graph.**  
   The provider request binds `model_rule_hash`, and the positioned-subject result includes `model_rule_hash` in its exact result identity. `PositionedSubjectPossibilityModelRule.rule_hash` hashes the full rule material: model authority, walkback authority, source-universe refs, walkback steps and positive proxy authorities.

   HQ225 registers direct model/walkback/proxy `AuthorityRef` values, but it never registers an exact identity for the **rule content** and never proves that the rule hash is determined by those authorities.

   This is not theoretical. The model-rule class permits different rule material under the same model/walkback authority refs. The repository's positioned-subject courts construct different walkback rules under the same model/walkback authorities, and rule content participates in result identity. A rule-content change can therefore change the product identity without any changed graph determinant capable of invalidating the old product.

The second defect is also the remaining caller-assertion problem at the direct-authority lane: `AnalyticalProductRegistration.determinant_authority_refs` accepts AuthorityRefs directly and `build_graph()` emits `authority -> product` edges from them. `DeterminantOwnerEvidence` authenticates only `determinant_ownerships`; it does not authenticate the claim that a direct authority owns/binds the consumed model-rule content.

Because these are source-level authority defects, the commission's missing-runtime fallback does not control the terminal. The correct terminal is **AUTHORITY_OVERREACH**, not merely “blocked by missing exact evidence.”

## 2. Mandatory attack results

### 2.1 Total determinant classification

**PASS at the set of exact refs HQ225 registers.**

`AnalyticalDependencyRegistry.build_graph()` calls `assert_complete_determinant_classification()`. A consumed `determinant_exact_ref` missing from `determinant_ownerships` raises `UNCLASSIFIED_DETERMINANT_REFUSED`.

The actual fresh runner calls the same complete-census helper and passes its returned exact refs plus ownership rows into `AnalyticalProductRegistration`.

This closes HQ224 defect 001 at the exact-ref registration layer.

### 2.2 Complete consumed-determinant census

**PARTIAL / FAIL at model-rule identity.**

The candidate now accounts for:

- empirical query;
- predicate;
- consumer query;
- condition-binding witness;
- source universe;
- upstream producer `EmpiricalFact`;
- C11 release ref;
- consumer subject/target;
- conditioner subject-fact / empirical-coordinate refs;
- risk-set, measure-basis, response-state, target-domain replay and operator-semantics refs;
- witness preimage / predicate-leaf / pairing-ground-truth refs;
- query and predicate replay roots;
- direct model/walkback/proxy authority refs.

That is substantially stronger than HQ223.

However the provider's own identity binding also consumes **`model_rule_hash`**, and the downstream result identity contains the same rule hash. There is no exact model-rule determinant, no rule-hash dependency object, and no authenticated proof that the model rule's full semantic material is frozen by the direct authority refs.

Therefore the candidate's statement that the consumed determinant census is complete is false.

### 2.3 Owner-authentic ownership evidence

**PASS for `ExactDeterminantOwnership`; FAIL for direct model-rule authority binding.**

For rooted exact determinants, `DeterminantOwnerEvidence` now requires:

- the exact determinant ref;
- material whose semantic hash equals that ref's content hash;
- an allowed determinant-specific owner relation path;
- declared owner refs exactly equal to the refs found at that path.

The “foreign authority existing elsewhere” hostile is no longer a global-union test and is materially sound.

But `determinant_authority_refs` remain bare caller-provided AuthorityRefs. They do not carry analogous evidence proving those refs bind the model-rule content consumed by the product.

### 2.4 Real sealed successor snapshot

**PASS for the query court; FAIL for the actual runner lifecycle.**

The query court now does the right thing:

- candidate -> APPROVED adjudication -> `seal_revision`;
- successor from the seal;
- exact sealed snapshot via public `resolve_historical_exact(successor)`;
- semantic-body-to-authority-ref check via `assert_authority_snapshot_body_matches_ref`;
- recomputation under that actual snapshot.

The actual fresh runner does something different. Its lifecycle is a model-authority transition:

- initial owner state is seeded from `fx.model_authority_snapshot(direction)`;
- that snapshot is not body/ref authenticated;
- after sealing the revision, the runner returns `revision.proposed_authority_ref`, not the resolved sealed successor snapshot;
- product recomposition receives only the bare successor `AuthorityRef` and constructs a new `PositionedSubjectPossibilityModelRule` from it.

Thus the actual runner does not satisfy the final-review requirement that recomputation consume the actual sealed/selected successor snapshot.

### 2.5 Family-safe replacement

**PASS by source inspection.**

Both determinant and product recompilation go through `_assert_replacement_family()`. A predicate-to-query replacement now raises `REPLACEMENT_FAMILY_MISMATCH`.

The repaired positive query witness returns:

- query -> query;
- predicate -> predicate;
- upstream fact -> fact;
- N10E product -> N10E product.

### 2.6 Actual graph reachability

**PASS for registered rooted exact determinants; FAIL for model-rule content.**

The graph now contains real two-hop paths such as:

- query authority -> query -> N10E product;
- query authority -> predicate -> N10E product;
- source authority -> universe -> N10E product;
- relevant authority closure -> upstream fact -> N10E product.

The direct model and walkback authority refs also emit `authority -> product` edges.

But no graph node represents `model_rule_hash`. A semantic rule-content mutation under unchanged authority refs is not reachable.

### 2.7 Selective invalidation

**Source-level mechanics are substantially repaired but not adoptable.**

The edge-deletion hostiles are meaningful:

- deleting owner -> determinant removes seeding;
- deleting determinant -> product removes downstream product reachability;
- the explicit nonconsumer remains unaffected by the query-authority change.

Currentness resolution still delegates to the accepted owner, so object/cache presence does not restore a recorded noncurrent artifact.

The missing model-rule determinant means “all and only consumers of D” is still unproved for D = model-rule semantic identity.

### 2.8 Positive product path

The source path remains present and unchanged:

`provide_empirical_possibility_slice -> compose_positioned_subject_possibility -> producer-derived PossibilitySliceEvidence -> evaluate_positioned_subject_possibility`.

HQ225 did not mutate provider, analytical composition or positioned-subject consumer semantics.

However the commission requires executed fresh-process evidence for adoption. No exact N10E execution was available or observed in this review.

### 2.9 Residual owner limitations

The candidate classifies the named inherited limitations accurately:

- `C11LogicalRelease`: unowned lifecycle ref / upstream owner-contract gap;
- comparability: recorded/rooted but installed fixture material is not a full stageable authority snapshot;
- walkback: directly consumed/rooted but fixture-only authority material is not stageable;
- affected-but-identical recomputation: accepted owner contract cannot represent same-ref replacement.

Those are not local defects merely because they remain unresolved.

The **model-rule identity/authority mismatch is different**: it is part of the actual N10E product identity and current runner lifecycle, so it is a local closure defect and may not be reclassified as one of those upstream limitations.

## 3. Runtime evidence

The commission requires a lawful exact run of:

- targeted N10E court;
- directly dependent owner/provider courts;
- hostile witnesses for all five HQ224 repairs.

No such execution exists on the candidate branch:

- GitHub Actions returns no workflow runs for `agent/rabochii-pyat-hq225-n10e-owner-authentic-lifecycle-repair-r1`;
- the generic pull-request workflow executes `.rabochii/court_spec.json`;
- that spec lists unrelated FIABC tests and does not include the N10E court or its direct owner/provider regression set.

This reviewer did not mutate workflow or court-spec terrain and does not claim any pytest count.

If the source defect above did not exist, the absence of exact runtime evidence would force
`N10E_OWNER_AUTHENTIC_FINAL_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`.

Because a source-level authority defect **does** exist, runtime absence is secondary to the rejection.

## 4. Exact source anchors

Candidate blobs:

- `rawlsing_next/pre553_analytical_replay_dependency.py` — `230bd7efed04a8fecc573812d7fbacb6dd93f86f`
- `rawlsing_next/tests/n10e_provider_replay_lifecycle_runner.py` — `a146874238d04bd705509066da0520af77f9f521`
- `rawlsing_next/tests/test_pre553_n10e_provider_replay_lifecycle_court.py` — `40d61205dc9692c9d867fe1e68c88ce08687d8a5`

Independent supporting blobs:

- `rawlsing_next/tests/c1_at18_at19_fixture.py` — `cc0015ce9c7e05224ec499f66e893a7ffda1bbe3`
- `rawlsing_next/pre553_authority_maintenance.py` — `547e6bf20354f38179a0e2600de64c7cb2260ea0`
- `rawlsing_next/pre553_empirical_authority.py` — `ca65a7fd4d52f0c44447434559b1d09412e7aa39`
- `rawlsing_next/pre553_empirical_objects.py` — `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- `rawlsing_next/pre553_empirical_possibility_provider.py` — `23167aa25291fb148b1e3cf210ac33fe7769b783`
- `rawlsing_next/source_backed_positioned_subject_possibility.py` — `62e5eced47b64512f47b004e3e13a6ef3fe21de7`
- `rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py` — `c48342fc5b9d7ae6701b5399c656d3c300cc407a`

## 5. Required next repair

A lawful successor repair must at minimum:

1. make the actual runner's baseline model authority body/ref authentic, or refuse it;
2. resolve and consume the actual sealed successor **snapshot** in the actual model-authority recomposition path, not only its AuthorityRef;
3. represent the consumed model-rule semantic identity as an exact lifecycle determinant or prove an exact cryptographic contract that the entire rule material is determined by an authenticated owner authority;
4. add a hostile showing that changing rule material while authority refs remain unchanged cannot silently leave the old product CURRENT;
5. only then rerun the exact N10E and dependent owner/provider courts on a lawful execution surface.

**TERMINAL:** `N10E_OWNER_AUTHENTIC_LIFECYCLE_AUTHORITY_OVERREACH`
