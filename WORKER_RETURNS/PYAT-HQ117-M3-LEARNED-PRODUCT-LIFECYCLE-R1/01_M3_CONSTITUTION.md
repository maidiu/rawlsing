# M3 CONSTITUTION — LEARNED-PRODUCT LIFECYCLE / CURRENT-SELECTION

Contract name proposed for adoption:

LEARNED_PRODUCT_LIFECYCLE_CONTRACT@1.0.0

## 1. Purpose

M3 governs the lifecycle of already-existing immutable M2 learned-product releases.

Its purpose is to answer only:
- what happened to an exact release in lifecycle terms;
- what exact release, if any, is current for one exact selection jurisdiction;
- what historical selection state existed at an exact replay point;
- what exact dependents must be reconsidered when a governed determinant changes.

M3 is not a producer of learned semantic truth and is not a consumer-permission service.

## 2. Constitutional noncollapse

Freeze:

SEMANTIC_PRODUCT_IDENTITY != M2_RELEASE_IDENTITY

M2_RELEASE_IDENTITY != M3_LIFECYCLE_EVENT_IDENTITY

M3_LIFECYCLE_EVENT_IDENTITY != CURRENT_SELECTION_IDENTITY

CURRENT_SELECTION_IDENTITY != CONSUMER_PERMISSION_IDENTITY

CURRENT_SELECTION_IDENTITY != STRUCTURAL_ADMISSION_IDENTITY

RELEASE_PUBLICATION != CURRENT_SELECTION

RECERTIFICATION != CURRENT_SELECTION

CORRECTION != CURRENT_SELECTION

SUPERSESSION != CURRENT_SELECTION

WITHDRAWAL != DELETE_HISTORY

REOPEN != ACCEPT

ONTOLOGY_EXPANSION != UNIVERSAL_OLD_TRUTH_INVALIDATION

## 3. Inputs

M3 accepts only exact refs to already-governed objects.

Required upstream inputs are:
- exact M2 learned-product release ref;
- exact semantic-product ref carried by that release;
- exact product-family/lifecycle-domain ref;
- exact release determinant/dependency closure supplied by M2;
- exact lifecycle authority/adjudication or attestation refs for the proposed event;
- exact selection key when currentness is affected.

M3 must fail closed if the referenced release, determinant closure, or event authority cannot be resolved exactly.

Repository presence alone is not permission to lifecycle-promote or current-select.

## 4. Outputs

M3 produces only lifecycle/currentness artifacts:
- LearnedProductLifecycleEvent;
- CurrentSelectionKey;
- CurrentSelectionReceipt;
- NoCurrentReceipt;
- LifecycleInvalidationReceipt;
- RebuildLinkReceipt;
- LifecycleCheckpoint / replay receipt.

These are governance facts about releases, not substitute learned products.

## 5. Lifecycle event vocabulary

Required event kinds:

CURRENT_SELECT
NO_CURRENT
RECERTIFIES
CORRECTS
CHANGES_SCOPE_EXPLICITLY
SUPERSEDES
WITHDRAWS
REOPENS
ONTOLOGY_OR_FAMILY_EXPANDS
INVALIDATION_DECLARED
REBUILD_LINKED

For compatibility with accepted P2 vocabulary, a SUPERSEDES event may carry a typed supersession_class including COMPLETENESS_ONLY.

Events may be compound only by explicit composition of separate typed records. A CORRECTS event does not silently imply CURRENT_SELECT; a SUPERSEDES event does not silently imply WITHDRAWS; a WITHDRAWS event does not silently imply NO_CURRENT outside the exact selection keys named by the event.

## 6. Identity layers

### Semantic product

Owned upstream.

It represents producer-owned learned meaning or typed disposition.

M3 never hashes lifecycle state into semantic-product identity.

### M2 release

Owned by M2.

It immutably binds the semantic product to release/publication preimage, exact dependencies/determinants, replay/reconstruction material, explanation lineage, and lawful resolution/service metadata.

M3 never mutates an M2 release.

### Lifecycle event

Owned by M3.

It is an immutable, content-addressed statement that a typed lifecycle event occurred over exact subject refs under exact authority, scope and predecessor context.

### Current selection

Owned by M3.

It is the current state of one exact SelectionKey produced only by explicit CURRENT_SELECT or NO_CURRENT events.

### Consumer permission

Owned elsewhere.

A consumer may be denied use of a product that is current. A consumer may also lawfully use a historical exact release where a separate contract allows historical/replay use.

## 7. Authority ceiling by event

CURRENT_SELECT:
- may bind an exact release to one exact SelectionKey;
- may not alter release semantics or grant use permission.

NO_CURRENT:
- may clear one exact SelectionKey;
- may not withdraw or negate the underlying release.

RECERTIFIES:
- records that an exact product/release remains eligible under explicit recertification authority;
- does not select it current unless a separate CURRENT_SELECT exists.

CORRECTS:
- classifies the correction relation;
- must identify whether correction is semantic-product-changing, release-only, or lifecycle-record-only;
- cannot infer corrected truth from chronology.

CHANGES_SCOPE_EXPLICITLY:
- records exact old/new scope relationship;
- semantic-scope change and selection-scope change are distinct.

SUPERSEDES:
- records predecessor/successor relation at an exact supersession class and scope;
- never deletes predecessor history.

WITHDRAWS:
- records release ineligibility/withdrawal at exact scope;
- historical resolution remains lawful;
- current pointers affected by withdrawal must be explicitly cleared or replaced.

REOPENS:
- reopens eligibility/court status only;
- creates no positive semantic truth and no current selection.

ONTOLOGY_OR_FAMILY_EXPANDS:
- records expansion of the lawful prerequisite/product family space;
- old local truth may survive;
- completeness/absence products may require selective invalidation.

INVALIDATION_DECLARED:
- records the mechanically derived affected/unaffected set after a governed determinant change;
- does not decide lifecycle meaning.

REBUILD_LINKED:
- binds an invalidated old dependent to an exact later rebuilt object/release or typed unresolved rebuild obligation;
- M3 does not construct the rebuilt semantics.

## 8. Change-classification law

A new semantic product is required when producer-owned meaning/proposition/claim content changes.

A new M2 release is required whenever the immutable M2 release preimage changes, including semantic-product ref, determinant/dependency closure, replay/reconstruction binding, explanation lineage, or publication/resolution binding.

A lifecycle-event-only change is lawful when neither semantic-product identity nor M2 release preimage changes and the event records only lifecycle/currentness state.

Examples:
- CURRENT_SELECT over an existing release: event only.
- NO_CURRENT: event only.
- withdrawal of an existing release: event only.
- recertification with unchanged M2 preimage: event only.
- recertification that changes M2 determinant/authority closure: new release, same semantic product if meaning is unchanged, then lifecycle event.
- correction of publication/replay packaging only: new M2 release, same semantic product, then CORRECTS.
- semantic correction: new semantic product + new M2 release + CORRECTS.
- selection-scope repartition only: event/current-key change only.
- semantic claim scope change: new semantic product + release.
- ontology expansion that only widens prerequisite universe: old local semantic products may survive; new completeness product/release and selective invalidation are required where completeness meaning changes.

## 9. Replay law

Lifecycle history is append-only and exact-ref addressed.

Historical replay must resolve:
- exact historical M2 releases;
- exact historical lifecycle events;
- exact historical determinant closures;
- exact historical selection receipts.

Later supersession, correction, withdrawal or current selection may not reinterpret a historical exact release.

Current-as-of is reconstructed from an exact lifecycle event/checkpoint ref, not Git time.

A wall-clock as-of query is lawful only if the event contract carries separately governed effective-time evidence. Commit timestamp is not semantic effective time.

## 10. Conflict law

One SelectionKey may not have two simultaneous unresolved current releases.

If two branches or event chains conflict for the same key, M3 returns CONFLICTING_CURRENT_SELECTION and no current release until an explicit governed reconciliation event resolves it.

Absence of a current receipt means NO_CURRENT / UNKNOWN_CURRENT according to whether explicit NO_CURRENT exists; it never means choose newest.

## 11. Success criterion

The M3 constitution is complete at documentary owner-contract grain when:
- exact event identity is frozen;
- exact selection-key identity is frozen;
- explicit CURRENT_SELECT and NO_CURRENT are required;
- semantic product/release/currentness/permission are separated;
- historical replay is nondestructive;
- determinant invalidation is selective and mechanically executable after event classification;
- Authority42 reuse is limited to mechanics;
- OBL034's HQD-117 generic lifecycle-provider debt has a competent owner contract.
