# SUCCESSION / INVALIDATION / REBUILD LAW

## 1. Central law

Lifecycle authority determines what changed.

Dependency machinery determines what exact dependents are affected.

Freeze:

DEPENDENCY_ENGINE_EXECUTES_CONSEQUENCES__DOES_NOT_INFER_LIFECYCLE_MEANING

M3 must never infer CORRECTS, RECERTIFIES, SUPERSEDES, WITHDRAWS, or ONTOLOGY_OR_FAMILY_EXPANDS from changed hashes, changed refs, chronology, lexical similarity, or graph position.

## 2. Determinant model

Every M2 release must expose or exact-bind its immutable determinant/dependency closure.

M3 treats determinants as exact opaque refs.

Examples of determinant classes may include:
- semantic product ref;
- validation/disposition ref;
- source/replay refs;
- authority refs;
- scope refs;
- ontology/family refs;
- explanation refs;
- selection-state refs where a downstream product explicitly depends on currentness.

M3 does not reinterpret determinant meaning.

## 3. Selective invalidation

Given a set of governed changed determinant refs:

1. find direct dependents whose recorded determinant closure contains those refs;
2. traverse explicit dependency edges to transitive dependents;
3. preserve all non-reachable dependents;
4. emit an exact LifecycleInvalidationReceipt;
5. do not fabricate rebuilt successors.

The invalidation receipt must identify:
- changed determinant refs;
- direct affected refs;
- transitive affected refs;
- unaffected refs for the inspected closure when enumerable;
- event/ref that governed the determinant change;
- derivation/checkpoint ref;
- invalidation state.

No family-wide invalidation is permitted without exact dependency reachability or a separately governed family-level determinant.

## 4. Rebuild linkage

Invalidation != rebuild.

M3 records rebuild obligations and later exact producer-owned results.

Required RebuildLink row states:

REBUILT
REBUILD_REQUIRED
REBUILD_BLOCKED
REBUILD_NOT_REQUIRED
REBUILD_OUT_OF_SCOPE

REBUILT must bind old exact ref -> new exact ref plus exact producer/rebuild receipt.

M3 may not create the new semantic product or M2 release itself.

## 5. Event consequence matrix

### CURRENT_SELECT

Semantic product:
unchanged.

M2 release:
unchanged.

Potential invalidation:
only dependents that explicitly use the current-selection receipt/key as a determinant.

Typical effect:
serving/dispatcher/cache state may change; historical semantic descendants do not change merely because current pointer changed.

### NO_CURRENT

Semantic product:
unchanged.

M2 release:
unchanged.

Potential invalidation:
current-dependent services/dispatchers for the exact SelectionKey.

Historical products remain replayable.

### RECERTIFIES

If release preimage unchanged:
lifecycle-event-only; invalidate only consumers that explicitly depend on certification event/current eligibility.

If authority/determinant/explanation changes M2 preimage:
new release, same semantic product if meaning unchanged; invalidate release-dependent descendants only.

### CORRECTS — semantic

Requires:
new semantic product + new M2 release.

Invalidate:
every exact dependent whose determinant closure reaches the corrected semantic product/release at affected scope.

No unrelated family member is invalidated by name alone.

### CORRECTS — release preimage only

Requires:
new M2 release; semantic product may remain same.

Invalidate:
dependents that bind release identity or changed determinant, not dependents that bind only unchanged semantic-product identity.

### CHANGES_SCOPE_EXPLICITLY — semantic scope

Normally:
new semantic product + new release.

Invalidate:
intersection of descendants with the changed semantic scope.

### CHANGES_SCOPE_EXPLICITLY — selection scope

May be event/current-key only.

Invalidate:
selection-dependent consumers for old/new keys only.

### SUPERSEDES — general

Successor release must exist exactly.

Predecessor remains historical.

Invalidation follows exact changed determinants and supersession scope.

No automatic current selection.

### SUPERSEDES — COMPLETENESS_ONLY

Old ordinary edge/relation truth can survive.

Invalidate/narrow:
completeness, absence, frontier-complete, exhaustive-coverage, or ontology-bounded consumers whose determinant closure depends on the old completeness universe.

Do not invalidate ordinary local truth unless it also depends on the changed completeness determinant.

### WITHDRAWS

No semantic rewrite.

Invalidate:
current-dependent consumers and any consumer whose contract requires release lifecycle eligibility.

Require explicit CURRENT_SELECT replacement or NO_CURRENT for affected current keys.

### REOPENS

Eligibility/court state only.

No semantic product is made positive.

No automatic rebuild or current selection.

### ONTOLOGY_OR_FAMILY_EXPANDS

Old local semantic truth may survive.

Invalidate:
completeness/absence/exhaustiveness products dependent on the old ontology/family boundary.

New expanded products are producer/M1/M2 work, not M3 work.

## 6. New semantic product vs new release vs event-only

### New semantic product mandatory when

- proposition/claim meaning changes;
- relation semantics change;
- semantic subject/object/scope constitutively changes;
- corrected product no longer makes the same semantic claim.

The producer/M1 owns this classification subject to exact authority.

M3 records the governed result; it does not make the semantic judgment.

### New M2 release mandatory when

- semantic product ref changes;
- release dependency/determinant closure changes;
- replay/reconstruction closure changes;
- explanation lineage changes;
- publication/resolution/service binding changes;
- other M2 immutable preimage field changes.

### Lifecycle event only sufficient when

- current pointer changes;
- NO_CURRENT is declared;
- withdrawal is recorded without changing release preimage;
- reopen is recorded;
- recertification is an external lifecycle fact and M2 preimage is unchanged;
- selection partition changes without semantic/release change;
- a historical succession relation is appended without modifying immutable releases.

## 7. Nondestructive supersession

Supersession is an edge between exact immutable releases/events.

It never mutates predecessor bytes or predecessor semantic projection.

Historical queries must continue to resolve predecessor release and determinant closure exactly.

A successor event may mark predecessor operationally noncurrent or ineligible at an exact scope, but cannot erase it.

## 8. Determinant-change authority

The determinant graph never decides that two refs are semantically equivalent, corrected, superseded, or recertified.

Those are upstream governed facts.

The graph only answers:

IF exact determinant X has a governed changed-state event, WHICH exact dependents recorded X directly or transitively?

This is the maximum lawful genericism.

## 9. Rebuild completion

An invalidated dependent returns to a positive current/servable state only when:
- its owning producer emits a lawful rebuilt semantic object/product as required;
- M2 emits a lawful immutable release if reusable publication is required;
- M3 records exact rebuild linkage;
- M3 explicitly CURRENT_SELECTs that release if currentness is required;
- downstream consumer permission independently passes.

No one step implies the next.
