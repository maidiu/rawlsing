# M3 IMPLEMENTATION CONTRACT

Status: documentary contract only. No implementation authorized by this worker.

## 1. Minimum runtime surface

A future implementation should expose a typed owner equivalent to:

LearnedProductLifecycleStore / LearnedProductLifecycleExecutor

It operates on exact M2 release refs and exact lifecycle receipts.

It must not require raw source access.

## 2. Required immutable records

At minimum:

LearnedProductLifecycleEvent@1.0.0
CurrentSelectionKey@1.0.0
CurrentSelectionReceipt@1.0.0
NoCurrentReceipt@1.0.0
LifecycleInvalidationReceipt@1.0.0
RebuildLinkReceipt@1.0.0
LifecycleCheckpoint@1.0.0
LifecycleReplayReceipt@1.0.0

All records are canonicalized and content-addressed.

## 3. Required state indexes

Implementation may maintain efficient indexes, but authoritative state derives from immutable records.

Required indexes:

selection_key_ref -> exact current receipt OR explicit NO_CURRENT receipt

release_ref -> ordered exact lifecycle event refs

determinant_ref -> direct dependent refs

dependent_ref -> determinant refs

invalidation_ref -> rebuild-link rows

event_ref -> exact parents

Indexes are rebuildable and nonauthoritative.

## 4. Required write operations

record_recertification(...)
record_correction(...)
record_scope_change(...)
record_supersession(...)
record_withdrawal(...)
record_reopen(...)
record_ontology_or_family_expansion(...)

select_current(selection_key_ref, release_ref, authority_refs, attestation_refs, ...)

declare_no_current(selection_key_ref, authority_refs, attestation_refs, ...)

declare_invalidation(changed_determinant_refs, governing_event_ref, ...)

link_rebuild(invalidation_ref, old_ref, new_ref_or_typed_state, producer_receipt_ref, ...)

Every write returns an exact immutable receipt/ref.

No operation mutates an existing release or event.

## 5. Required read operations

resolve_release_lifecycle_exact(release_ref)

resolve_current_exact(selection_key_ref, current_receipt_ref)

resolve_current_as_of(selection_key_ref, as_of_event_or_checkpoint_ref)

list_selection_history(selection_key_ref)

list_release_history(release_ref)

resolve_invalidation_exact(invalidation_ref)

resolve_rebuild_status(invalidation_ref, dependent_ref)

export_checkpoint()

restore_checkpoint_exact(checkpoint)

audit_replay()

## 6. Forbidden resolver APIs

No implementation may offer semantically authoritative behavior equivalent to:

resolve_latest
resolve_default
resolve_nearest
resolve_best_version
resolve_semver_fallback
resolve_current_without_receipt
select_successor_automatically
auto_promote_on_release
auto_promote_on_recertify
auto_promote_on_supersession

Convenience UI methods may sort historical objects for display, but display order cannot become lifecycle authority.

## 7. M2 interface

M3 requires from M2 an exact release object or adapter exposing at least:

release_ref
semantic_product_ref
product_family_ref
release_scope_ref
determinant_refs / dependency closure ref
replay/reconstruction refs
explanation lineage ref
publication/resolution binding refs
typed release state

M3 must not infer these from file path or repository layout.

If M2 chooses a virtual/rebuildable physical representation, M3 still operates on the durable logical release ref and exact durable release preimage.

Physical carrier identity is not currentness identity.

## 8. M1 interface

M3 never validates discovery evidence.

If an M2 release wraps an M1 typed learned-empirical disposition, M3 treats the semantic product ref as opaque and exact.

M3 may not turn provenance/support into ACCEPTED or VALIDATED state.

## 9. Dispatcher/consumer interface

Downstream dispatch receives:
- exact selection key;
- exact current receipt;
- exact selected M2 release ref or NO_CURRENT;
- exact lifecycle eligibility state.

Downstream must separately prove:
- consumer permission;
- claim-family applicability;
- structural admission where required;
- comparability/composition/measurement premises where required.

M3 does not collapse those gates.

## 10. Determinant engine interface

The implementation may reuse/extract existing determinant traversal mechanics if generalized over ExactRef.

Required function shape is semantically equivalent to:

derive_affected(changed_exact_refs, determinant_graph) -> direct_affected, transitive_affected, unaffected

The function must not classify the lifecycle event.

Its output is mechanical only.

If rebuild cannot execute in M3 jurisdiction, the invalidation receipt records REBUILD_REQUIRED instead of fabricating a new object.

## 11. Current selection state machine

Per SelectionKey:

UNKNOWN_BEFORE_SELECTION_HISTORY
  -> CURRENT_SELECTED via CURRENT_SELECT
  -> CURRENT_SELECTED via later CURRENT_SELECT
  -> NO_CURRENT via NO_CURRENT
  -> CURRENT_SELECTED via later CURRENT_SELECT

A WITHDRAWS event does not itself move the state machine unless paired with explicit selection-state event(s).

A SUPERSEDES event does not itself move the state machine.

A RECERTIFIES event does not itself move the state machine.

Conflicting event ancestry moves to CONFLICTING_CURRENT_SELECTION until reconciled.

## 12. Selection transaction law

For one SelectionKey, selection update must be atomic:

1. exact target/NO_CURRENT validated;
2. exact prior selection receipt captured if present;
3. event sealed;
4. current receipt sealed;
5. selection index advanced to the exact receipt;
6. checkpoint/replay state updated.

Crash/restart may not expose a half-selected state.

## 13. Historical replay

Checkpoint payload must include enough immutable refs to reconstruct:
- all lifecycle events;
- all selection receipts;
- all NO_CURRENT receipts;
- selection indexes;
- determinant graph state;
- invalidation/rebuild refs;
- parent-event graph.

Replay must produce the same canonical checkpoint hash.

Later currentness must not alter historical resolution.

## 14. Implementation ceiling

A future implementation may optimize storage/cache/indexing freely if:
- canonical logical identity is unchanged;
- append-only history survives;
- exact historical replay survives;
- explicit current receipts survive;
- fail-closed conflict/no-current states survive.

No physical architecture choice is implied by this constitution.

## 15. Qualification gate

Before generic use, implementation must pass the hostile plan in 08_HOSTILE_LIFECYCLE_TEST_PLAN.md.

A green implementation still does not make any particular product current without product-specific CURRENT_SELECT authority.
