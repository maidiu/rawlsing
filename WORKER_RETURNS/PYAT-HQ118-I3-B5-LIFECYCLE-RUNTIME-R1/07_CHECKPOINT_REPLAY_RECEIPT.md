# PYAT HQ118 I3 — Checkpoint / Replay Receipt

## Runtime contract

Checkpoint schema:

`PRE553_B5_LEARNED_PRODUCT_LIFECYCLE_CHECKPOINT@1.0.0`

Lifecycle contract:

`PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0`

The executor exposes:

- `export_checkpoint()`
- `LearnedProductLifecycleExecutor.from_checkpoint(...)`
- `audit_replay()`
- `resolve_current_as_of(...)`

## Checkpoint contents

The deterministic checkpoint binds:

- staged exact lifecycle subjects;
- exact registered-release set;
- append-only lifecycle event journal;
- exact SelectionKey objects;
- CurrentSelectionReceipt objects;
- NoCurrentReceipt objects;
- exact current/no-current selection index;
- publication state;
- validity state;
- replay state;
- rebuild state;
- materialization class;
- payload-materialization state;
- determinant graph;
- invalidation receipts;
- rebuild-eligibility receipts;
- rebuild-link receipts;
- GC-eligibility receipts;
- exact releases whose recomputable payload GC was recorded.

The checkpoint hash is:

`semantic_hash(checkpoint_payload)`

No timestamp, Git order, filesystem order, newest release, or implicit currentness participates.

## Replay validation

`from_checkpoint` verifies:

1. checkpoint payload hash;
2. checkpoint schema and B5 contract id;
3. exact lifecycle subject reconstruction;
4. exact registered-release coverage;
5. lifecycle event identity/content hash;
6. append-only ordinal sequence and exact parent linkage;
7. exact SelectionKey identities;
8. exact selection/no-current receipts;
9. exact selection-index state;
10. state-map coverage of the exact registered set;
11. exact invalidation/rebuild/GC receipt identities;
12. reconstructed determinant graph equality;
13. final exported checkpoint hash equality.

Any mismatch fails closed with `LearnedProductLifecycleConflict`.

## Current-as-of law

Historical currentness is resolved from:

- an exact lifecycle event ref; or
- an exact lifecycle checkpoint.

It is not resolved from:

- wall-clock time;
- commit time;
- filename order;
- semantic version;
- repository newest;
- filesystem newest.

A historical event walk replays only selection/no-current receipts whose exact lifecycle events are at or before the requested event ordinal.

## Governing hostile proof

I3 test:

`test_h22_checkpoint_restart_and_replay_identity_are_exact`

constructs a lifecycle containing:

- registration;
- publication;
- exact current selection;
- recertification;
- explicit NO_CURRENT.

It then proves:

`checkpoint_hash(original) == checkpoint_hash(restored)`

`events(original) == events(restored)`

and:

`audit_replay().original_checkpoint_hash == audit_replay().replayed_checkpoint_hash`

with:

`replay_state = REPLAY_VERIFIED`

Historical-as-of is separately proved by:

`test_h11_historical_current_as_of_uses_exact_event_not_git_time`

## Atomic failure proof

I3 also proves checkpoint identity is unchanged after rejected operations:

- unpublished product selection;
- stale/concurrent selection;
- current withdrawal missing explicit transition;
- current invalidation missing explicit transition;
- withdrawn product self-replacement;
- invalidated product self-replacement.

These are crash/atomic-selection hostile witnesses: validation occurs before lifecycle mutation.

## Repository-native qualification

Final narrow governed court:

- PR: temporary qualification PR `#458` (never for merge)
- exact workflow run: `36326914249`
- run head: `7c181e6c05532e6d7a4308ce5077d032e61f5b75`
- semantic candidate pinned by temporary court spec: `700dff473978fd241fe97fb68502a295a55de63e`
- protocol self-test: `20 passed in 0.11s`
- governed bounded court: `60 passed in 0.61s`
- court composition: 38 I3 lifecycle tests + 22 Authority42 maintenance non-regression tests
- artifact: `rabochii-court-receipt-36326914249`
- artifact id: `10933214853`
- artifact digest: `sha256:72d4527202693805aa9f0600935d63c686acff404cf3b1004bf693e5512f7996`

The temporary court spec was restored after qualification to the exact sealed-HQ118 blob:

`67eb1c668c6d03a31f678d6b09db3288bd1ef810`

Restoration commit:

`2343aa6e73fdfc0a2567693db5bf7993995f701f`

## Receipt ceiling

No raw survey/source file was opened.

No real-source I03/I05 execution occurred.

No M1/M2 sibling runtime was imported.

No Field Forge path was mutated.

No source/carrier retirement was performed.

## Terminal

`I3_CHECKPOINT_REPLAY = EXACT_HASHED_RESTART_GREEN__HISTORICAL_CURRENT_AS_OF_EXACT_EVENT_OR_CHECKPOINT__NO_CHRONOLOGICAL_CURRENTNESS`
