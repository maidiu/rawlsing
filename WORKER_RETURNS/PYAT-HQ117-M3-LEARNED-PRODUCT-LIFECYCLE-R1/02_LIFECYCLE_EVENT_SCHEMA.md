# LIFECYCLE EVENT SCHEMA

Schema family proposed for adoption:

LearnedProductLifecycleEvent@1.0.0

## 1. Exact event identity

A lifecycle event is immutable and content-addressed.

Its event_ref is the project-native exact ref over the canonical semantic projection below.

The event identity MUST include every field that can change lifecycle meaning, selection consequence, invalidation consequence, or historical replay.

Required canonical fields:

contract_id
event_kind
event_class
product_family_ref
subject_release_refs
predecessor_release_refs
successor_release_refs
semantic_product_refs
selection_keys
selection_effect
event_scope_ref
selection_purpose_refs
consumer_context_partition_refs
event_authority_refs
attestation_or_adjudication_refs
evidence_refs
determinant_change_refs
invalidation_receipt_refs
rebuild_link_refs
parent_event_refs
effective_time_evidence_ref
event_state

All refs are exact immutable refs. Empty fields are explicit empty collections/nulls; omitted-vs-empty ambiguity is forbidden in canonical serialization.

## 2. Event-state vocabulary

Allowed terminal event states:

COMMITTED
CONFLICTING
REVOKED_BY_EXACT_SUCCESSOR_EVENT

REVOKED_BY_EXACT_SUCCESSOR_EVENT does not delete the event. It means only that a later exact lifecycle event supersedes its operational effect at a named scope.

Historical replay still returns the original event.

## 3. Event-kind rules

### CURRENT_SELECT

Required:
- exactly one target subject_release_ref;
- exactly one or more exact selection_keys;
- selection_effect = SELECT_EXACT_RELEASE;
- exact selection authority/attestation refs.

Forbidden:
- implicit selection of another release;
- latest/default/newest resolution;
- consumer permission grant.

### NO_CURRENT

Required:
- one or more exact selection_keys;
- selection_effect = CLEAR_CURRENT;
- exact authority/attestation refs.

Target release is absent by design.

NO_CURRENT is not withdrawal, rejection, semantic negation, or deletion.

### RECERTIFIES

Required:
- exact subject release(s);
- exact recertification authority/evidence;
- recertification class.

Allowed recertification classes:
- RELEASE_UNCHANGED;
- SAME_SEMANTIC_PRODUCT_NEW_RELEASE.

A semantic change may not be labeled recertification.

### CORRECTS

Required:
- predecessor release(s);
- successor release(s);
- correction class;
- correction scope;
- exact correction authority.

Allowed correction classes:
- SEMANTIC_PRODUCT_CORRECTION;
- RELEASE_PREIMAGE_CORRECTION;
- LIFECYCLE_RECORD_CORRECTION.

SEMANTIC_PRODUCT_CORRECTION requires predecessor and successor releases to carry different semantic-product refs.

RELEASE_PREIMAGE_CORRECTION may preserve semantic-product ref while changing M2 release identity.

LIFECYCLE_RECORD_CORRECTION corrects only lifecycle metadata and may not rewrite the original event; it appends a successor correction event.

### CHANGES_SCOPE_EXPLICITLY

Required:
- old scope ref;
- new scope ref;
- scope class.

Allowed scope classes:
- SEMANTIC_PRODUCT_SCOPE;
- RELEASE_PUBLICATION_SCOPE;
- CURRENT_SELECTION_SCOPE.

SEMANTIC_PRODUCT_SCOPE change normally requires a new semantic product and new M2 release.

CURRENT_SELECTION_SCOPE may be event-only when the release is unchanged.

### SUPERSEDES

Required:
- predecessor release(s);
- successor release(s);
- supersession class;
- exact scope.

Allowed supersession classes include:
- GENERAL_SUCCESSION;
- COMPLETENESS_ONLY;
- PUBLICATION_ONLY;
- CURRENTNESS_ELIGIBILITY_ONLY.

COMPLETENESS_ONLY may leave ordinary edge/relation truth unchanged while invalidating completeness/absence descendants.

### WITHDRAWS

Required:
- exact release(s);
- exact withdrawal scope;
- exact authority/reason refs.

Withdrawal preserves historical replay.

If withdrawn release is current for any affected SelectionKey, an explicit NO_CURRENT or CURRENT_SELECT must be committed for those keys. Withdrawal itself may not silently choose a replacement.

### REOPENS

Required:
- exact subject refs;
- exact reopened status/court eligibility scope;
- exact authority.

REOPENS does not mean accept, approve, select current, or restore a withdrawn release.

### ONTOLOGY_OR_FAMILY_EXPANDS

Required:
- prior ontology/family ref;
- expanded ontology/family ref;
- exact expansion authority;
- affected completeness/product-family scopes.

Expansion does not automatically invalidate local historical truth.

### INVALIDATION_DECLARED

Required:
- changed determinant refs;
- exact affected dependent refs;
- exact unaffected refs at the inspected closure when enumerated;
- invalidation derivation/ref.

This event records consequences only after a governed lifecycle/determinant fact exists.

### REBUILD_LINKED

Required:
- invalidation receipt ref;
- rebuild pairs or typed unresolved rebuild rows.

A rebuild row is one of:
- REBUILT: old_ref -> exact new_ref;
- REBUILD_REQUIRED: old_ref -> no new ref yet;
- REBUILD_NOT_REQUIRED;
- REBUILD_BLOCKED;
- REBUILD_OUT_OF_SCOPE.

M3 may record the producer-owned new ref but may not mint it.

## 4. Current-selection key schema

CurrentSelectionKey@1.0.0 fields:

product_family_ref
selection_scope_ref
selection_purpose_ref
consumer_context_partition_ref = optional

The key identity is the canonical content hash of those exact refs.

consumer_context_partition_ref is a namespace discriminator only. It carries zero use permission.

## 5. Current selection receipt schema

CurrentSelectionReceipt@1.0.0 fields:

selection_key_ref
selected_release_ref
current_select_event_ref
previous_selection_receipt_ref = optional
selection_authority_refs
selection_attestation_refs
determinant_snapshot_ref
receipt_state = CURRENT_SELECTED

The receipt is immutable.

A later selection creates a new receipt and leaves the prior receipt historical.

## 6. No-current receipt schema

NoCurrentReceipt@1.0.0 fields:

selection_key_ref
no_current_event_ref
previous_selection_receipt_ref = optional
selection_authority_refs
selection_attestation_refs
reason_ref
receipt_state = NO_CURRENT

## 7. Historical current-as-of

CurrentAsOfQuery@1.0.0 accepts:

selection_key_ref
as_of_event_ref OR as_of_checkpoint_ref

It returns:
- CURRENT_SELECTED + exact release ref; or
- NO_CURRENT; or
- CONFLICTING_CURRENT_SELECTION; or
- UNKNOWN_BEFORE_SELECTION_HISTORY.

It may not consult newest release, repository order, commit time, filesystem order, semantic version ordering, or label similarity.

## 8. Parent linkage

Every event after the first event in a lifecycle ledger must cite exact parent_event_refs.

For one SelectionKey, concurrent incomparable parents that both alter selection state create a conflict until explicitly reconciled.

Append-only history is mandatory.

No event update-in-place is permitted.
