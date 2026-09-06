# OBL034 LEARNED-PRODUCT LIFECYCLE CANDIDATE R1

Status:

`CANDIDATE__NO_PROJECT_CURRENT_EFFECT__READY_FOR_SUB_VOZHD_B_ADJUDICATION`

Candidate contract:

`PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0`

Machine-readable rules blob:

`f73d9ca5903d1f243d2a904085a879777ca323a8`

Immutable B5 handoff:

`9bda4cb1ae425fd14e9483199f5a9aa7859d048c`

## 1. Jurisdiction

This candidate owns only learned-product lifecycle operations:

- immutable learned-product lifecycle registration;
- publication;
- explicit current-selection;
- supersession;
- withdrawal/invalidation;
- historical retention;
- replay/rebuild eligibility;
- optional-cache lifecycle classification;
- learned-product payload garbage-collection eligibility.

It does not own producer semantics, semantic-authority adjudication, source/carrier retirement, general comparability/portability, general composition, physical architecture selection, PRE553 topology selection, or V3/V2 causality.

Binding invariant:

`SEMANTIC OWNER != CARRIER OWNER != LIFECYCLE OWNER`

A lifecycle receipt may make a product available, current, noncurrent, invalidated, withdrawn, replayable, rebuildable, or payload-GC-eligible. It cannot change what the product means or who produced that meaning.

## 2. Physical-neutral semantic floor

Authority31 fixes the common logical theorem:

`SOURCE_AND_GOVERNED_AUTHORITY`
→ `EXACT_RECONSTRUCTIBLE_EMPIRICAL_INFORMATION`
→ `PRODUCER_OWNED_SEMANTIC_OBJECT_DAG`
→ learned products
→ shared release/replay graph
→ typed PRE-V3 publication/serving.

The resulting lifecycle constraints are:

- semantic stage identity does not require a separate physical stage;
- rebuildability does not make a semantic product disposable;
- canonical semantic identity does not require a permanent payload table;
- cache/materialization is not authority merely because it is persistent;
- direct producer reuse is preferred to semantic republishing for physical neatness;
- source retirement remains separate governance.

Therefore this candidate is neutral among persistent, source-backed virtual, and hybrid physical realizations.

## 3. Learned-product identity

The semantic learned-product identity is immutable and must bind at least:

- exact `product_ref`;
- exact producer owner and producer contract;
- semantic projection hash;
- exact AuthoritySnapshot refs used by the product;
- exact direct dependency refs;
- determinant-set hash;
- exact replay root;
- exact selection-scope ref;
- exact build/release receipt refs.

Publication, current-selection, supersession, withdrawal, invalidation, carrier relocation, cache loss, or payload garbage collection cannot rewrite that identity.

If changed semantic determinants change the semantic output, the rebuild creates a new exact product identity. The prior product becomes historical; it is not rewritten.

## 4. Orthogonal lifecycle state

The candidate deliberately avoids one overloaded lifecycle status. It tracks separate dimensions:

- publication: `UNPUBLISHED | PUBLISHED`;
- selection: `NOT_CURRENT | CURRENT_SELECTED`;
- validity: `VALID | INVALIDATED_REBUILD_REQUIRED | WITHDRAWN`;
- replay: complete or typed fail-closed replay blocker;
- rebuild: current rebuild eligible, historical replay eligible, blocked, or not requested;
- materialization class: mandatory retained capital, recomputable product payload, or optional cache/accelerator.

This prevents false equivalences such as:

`PUBLISHED == CURRENT`

`SUPERSEDED == INVALID`

`WITHDRAWN == ERASED`

`REBUILDABLE == DELETE_SOURCE`

`CACHED == AUTHORITATIVE`.

## 5. Publication and current-selection

Publication requires an exact lifecycle publication receipt binding:

- product identity;
- producer permission ceiling;
- exact authority-snapshot closure;
- determinant-set hash;
- replay root;
- publication authority/rule;
- parent lifecycle event.

Repository presence is not publication authority.

Currentness is a separate explicit pointer keyed by exact `selection_scope_ref`. It exists only through an exact selection receipt containing the selected product, prior current product if any, selection rule, and attestation.

The following never select current:

- newest timestamp;
- newest file;
- newest branch;
- repository order;
- highest version string;
- `latest`;
- `default`;
- fuzzy/nearest/semver fallback.

If current evidence is missing or conflicting, the result is `UNKNOWN_CURRENTNESS` or `CONFLICTING_CURRENT_SELECTION`, not an inferred winner.

## 6. Supersession and withdrawal

Supersession is an explicit predecessor→successor relation plus an exact current-selection transition. It is non-destructive.

The predecessor keeps:

- immutable identity;
- lifecycle history;
- exact historical authority refs;
- determinant closure;
- replay root;
- historical audit/replay status.

Withdrawal prohibits current serving in the governed scope but does not erase history.

If a current product is withdrawn or invalidated, the current pointer must either:

1. move by exact receipt to another already-lawful product; or
2. become explicitly empty / no current selection.

There is no implicit rollback to “the previous one.”

## 7. Replay after supersession or withdrawal

Historical replay pins historical authority id/version/hash and exact historical determinants.

A newer AuthoritySnapshot may not reinterpret an older product merely because it is current now.

This follows the current replay inspectorate and the current AuthoritySnapshot maintenance contract, both of which reject latest/default/fuzzy substitution and preserve historical identities.

The mandatory historical retention floor is:

- product identity;
- lifecycle event journal;
- publication/current-selection/supersession/withdrawal/invalidation/rebuild receipts;
- exact historical AuthoritySnapshot refs;
- exact determinant closure;
- replay/reconstruction root and instructions;
- required source/upstream refs;
- governance/adjudication evidence needed to explain what was built and why.

Payload bytes may be recomputable. This floor is not.

## 8. Dependency-driven invalidation

The candidate generalizes a determinant-graph rule:

`CHANGED EXACT DETERMINANT`
→ directly dependent learned products
→ transitive exact learned-product dependency closure.

Unrelated products remain valid.

Determinants include exact semantic authority, producer contract, source/release/universe, query/predicate/discovery/validation rule, upstream learned product, publication governance, replay protocol, and any executor/schema identity that is semantically determinant rather than merely operational.

This rule has two supporting grains:

1. current `PRE553_AUTH40_SEMANTIC_AUTHORITY_MAINTENANCE@1.0.0` already computes exact authority-changed dependent closure;
2. Chetiri C08 independently holds that minimum lawful recompilation is changed determinant scope plus transitive exact dependency closure.

C08 final reconciliation is still pending. Therefore B5 constitutes this only as the OBL034 lifecycle **candidate rule**, not as a claim that C08 has finally closed.

Optional cache loss is not a semantic determinant and does not semantically invalidate learned products.

## 9. Rebuild eligibility

A product is rebuild-eligible only if the exact required reconstruction inputs exist:

- source or exact upstream product;
- exact semantic authority closure;
- exact producer contract;
- exact replay/reconstruction rules;
- required dependency closure;
- governed execution mechanism.

Historical replay uses historical determinants.

Current rebuild after a changed determinant uses the new lawful determinant set and creates a new product identity if semantics differ.

Missing authority/source/upstream/replay material yields a typed rebuild blocker. The lifecycle owner may not manufacture substitutes.

## 10. Optional caches

A cache or accelerator is non-authoritative when its loss changes performance only.

Examples include:

- warm source-backed C11 session releases;
- deterministic indexes;
- R4-style execution representations;
- other bounded regenerable accelerators.

A cache may be dropped and rebuilt without changing product semantic identity/currentness.

If someone wants cache material itself to carry learned semantic meaning, it must be separately published as a governed learned product. Persistence alone cannot promote it.

## 11. Garbage-collection eligibility

This candidate distinguishes garbage collection of **recomputable learned-product payload bytes** from retirement of source/carrier evidence.

A recomputable payload is GC-eligible only after exact proof that:

1. product identity and lifecycle history remain;
2. reconstruction/replay path is exact and available;
3. historical authority/determinant/replay roots remain;
4. current serving, if applicable, can lawfully reconstruct without those bytes;
5. no exact downstream dependency requires the materialized bytes rather than the logical product;
6. source/carrier dependencies remain retained unless separately retired by competent OBL029 authority;
7. a GC eligibility attestation records the proof.

Never GC-eligible under this candidate:

- semantic identity records;
- lifecycle event history;
- required AuthoritySnapshots;
- determinant closure;
- replay/reconstruction receipts/instructions;
- source/carrier material whose deletion would require OBL029.

## 12. Source/carrier retirement boundary

Current source→C11 equivalence certification explicitly returns:

- `source_snapshot_retention_required = true`;
- `source_retirement_authorized = false`;
- `cutover_authorized = false`.

Accordingly this lifecycle owner can say:

“this learned-product payload is reconstructible”

but cannot say:

“therefore delete the source/carrier.”

OBL029 remains a separate competent authority question.

The B5 economics model consequently gives **no storage credit** for assumed source/carrier deletion.

## 13. AuthoritySnapshot lifecycle boundary

`PRE553_AUTH40_SEMANTIC_AUTHORITY_MAINTENANCE@1.0.0` remains owner of:

evidence → candidate → adjudication → seal → current promotion/rollback → exact invalidation → append-only replay.

The learned-product lifecycle consumes those exact authority events as determinants.

It does not:

- create AuthoritySnapshots;
- choose semantic authority;
- widen semantic permission;
- reinterpret prior products under new authority.

`CURRENT PRODUCT` does not imply `CURRENT AUTHORITY`, and `CURRENT AUTHORITY` does not automatically make a learned product current.

Both require their own exact receipts.

## 14. Fail-closed states

The machine candidate explicitly recognizes:

- `AMBIGUOUS_PRODUCT_IDENTITY`;
- `MISSING_LIFECYCLE_AUTHORITY`;
- `MISSING_SEMANTIC_AUTHORITY`;
- `MISSING_REPLAY_CLOSURE`;
- `MISSING_DETERMINANT`;
- `CONFLICTING_CURRENT_SELECTION`;
- `UNKNOWN_CURRENTNESS`;
- `INVALIDATED_DEPENDENCY`;
- `WITHDRAWN_NO_CURRENT_REPLACEMENT`;
- `REBUILD_NOT_PROVED`;
- `GC_NOT_AUTHORIZED`;
- `SOURCE_OR_CARRIER_RETIREMENT_AUTHORITY_REQUIRED`;
- conditional comparability/composition authority blockers if a future claim actually requires those grains.

No missing state is repaired by chronology, storage presence, lexical similarity, or an architecture preference.

## 15. Economics connection

Lifecycle economics must compare physical candidates as equal-obligation vectors.

Mandatory dimensions are priced separately from optional ones:

- semantic/governance retained capital;
- replay retained capital;
- source/carrier retained capital unless OBL029 says otherwise;
- learned-product materialization;
- caches/accelerators;
- source/decode/query/discovery/validation execution;
- determinant-local invalidation/rebuild;
- fresh-process replay/recovery;
- publication/repository/resolution overhead;
- migration only when materially live and lawfully authorized.

No scalar score or invented weights are part of this candidate.

## 16. Adoption boundary

This document and `02_LIFECYCLE_RULES.json` are a campaign-local B5 candidate only.

They do not:

- close central OBL034;
- become project-current lifecycle authority;
- modify current production code;
- authorize source/carrier retirement;
- launch OBL037;
- choose architecture A/B/C;
- choose PRE553 topology.

Exact next governance step:

`READY_FOR_SUB_VOZHD_B_ADJUDICATION__THEN_VOZHD_HQ_IF_ACCEPTED`
