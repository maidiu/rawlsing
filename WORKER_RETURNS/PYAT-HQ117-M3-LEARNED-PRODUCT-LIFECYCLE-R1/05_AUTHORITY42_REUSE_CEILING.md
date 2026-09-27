# AUTHORITY42 REUSE CEILING

## 1. Holding

Authority42 A03 proves a current semantic-authority maintenance lifecycle.

It does not prove generic learned-product lifecycle ownership.

Freeze:

AUTHORITY42_A03_SEMANTIC_AUTHORITY_LIFECYCLE != M3_LEARNED_PRODUCT_LIFECYCLE_OWNER

M3 may reuse mechanics only where the subject ontology remains correct.

## 2. Exact Authority42 A03 precedent

Authority42 A03 admits, at semantic-authority maintenance grain:

evidence -> candidate -> adjudication -> revision -> promotion/release -> supersession/rollback -> invalidation/recompile -> restart/replay

Current code on the HQ117 base implements:
- immutable AuthoritySnapshot history;
- exact AuthorityRef resolution;
- explicit promotion/rollback receipts;
- exact selection receipt requirement;
- no latest/default/fuzzy lookup;
- SemanticDeterminantGraph;
- affected/unaffected invalidation receipts;
- append-only maintenance events;
- deterministic checkpoint/restart;
- replay verification.

These are strong mechanical precedents.

## 3. Lawful direct reuse

The following patterns are jurisdiction-compatible:

### Exact immutable refs

All lifecycle subjects, receipts, events, determinants and checkpoints must be exact-ref addressable.

### Explicit selection

Current selection changes only by exact receipt/event.

No inferred latest/default path.

### Historical exact resolution

Later current selections never reinterpret historical exact subjects.

### Append-only journal

Lifecycle event history is append-only and parent-linked.

### Determinant graph

Explicit exact determinant edges may compute direct/transitive impact after a governed change has already been classified.

### Selective invalidation

Affected and unaffected dependent sets remain distinguishable.

### Checkpoint/restart/replay

A serialized lifecycle state may be checkpointed, restored and replay-audited for exact identity.

### Exact rollback target

Rollback/current reselection must cite an exact prior lawful release/selection state, not merely an old-looking subject.

## 4. Forbidden semantic reuse

The following are not lawful M3 shortcuts:

### AuthoritySnapshot as learned product

Forbidden.

AuthoritySnapshot is semantic authority, not learned empirical/product meaning.

### AuthorityRef as M2 release identity

Forbidden.

An authority ref and learned-product release ref answer different identity questions.

### authority_id as SelectionKey

Forbidden.

M3 currentness must bind product family + exact scope + exact purpose + optional consumer-context partition.

### AuthorityReleaseReceipt as generic M3 receipt

Forbidden as-is.

A03's release receipt selects AuthoritySnapshot revisions by authority identity and supports PROMOTION/ROLLBACK.

M3 needs learned-product lifecycle events including NO_CURRENT, withdrawal, recertification, correction, scope change, supersession classes, reopen, ontology/family expansion and historical current-as-of.

### A03 adjudication semantics as product semantics

Forbidden.

An APPROVED semantic-authority candidate does not mean a learned product is validated, released, current, consumer-authorized or structurally admitted.

### A03 recompiler as learned-product producer

Forbidden.

M3 may coordinate invalidation/rebuild linkage but cannot synthesize semantic successors.

### A03 correction_kind as generic learned-product correction truth

Forbidden unless a separately governed learned-product event authority supplied that classification.

The dependency/lifecycle engine must not infer product meaning.

## 5. Required implementation strategy

Two lawful implementation paths exist.

### Path A — product-specific M3 owner

Implement a dedicated learned-product lifecycle executor using exact refs and the constitution in this return.

### Path B — extract a lower-level neutral lifecycle core

Refactor/extract generic mechanics from A03 only if the extracted core is neutral over subject type.

A neutral core may know:
- exact subject refs;
- exact event refs;
- selection keys;
- determinant edges;
- invalidation/rebuild refs;
- checkpoints/replay.

It may not know AuthoritySnapshot-specific meaning.

The semantic authority maintenance executor and learned-product lifecycle executor would then be separate typed adapters over the common neutral core.

## 6. Anti-alias law

No type alias may make these appear equivalent:

AuthoritySnapshot == LearnedSemanticProduct
AuthorityRef == LearnedProductReleaseRef
AuthorityReleaseReceipt == CurrentSelectionReceipt
authority_id == CurrentSelectionKey
APPROVED_AUTHORITY == VALIDATED_PRODUCT
PROMOTED_AUTHORITY == CURRENT_PRODUCT

Any implementation that relies on such equivalence fails M3 constitution even if tests pass mechanically.

## 7. What M3 binds from existing replay law

M3 adopts the existing PRE553 replay discipline:

- exact historical refs only;
- no selector fallback;
- repository presence is not permission;
- provenance is not permission;
- supersession does not reinterpret history;
- pinned replay identity must match exactly.

M3 extends those mechanics to learned-product lifecycle/currentness without widening semantic authority.

## 8. Boundary result

Authority42 is sufficient precedent to show that the required mechanics are technically coherent.

It is insufficient authority to close the generic learned-product owner gap by identity reuse.

Therefore M3 is required, but it need not reinvent the mechanical substrate.
