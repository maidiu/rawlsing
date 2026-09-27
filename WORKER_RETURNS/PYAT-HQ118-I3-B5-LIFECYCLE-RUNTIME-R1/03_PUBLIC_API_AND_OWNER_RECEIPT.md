# PYAT HQ118 I3 — Public API and Owner Receipt

## Governed owner

Current semantic owner implemented here:

`PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0`

Adoption status inherited from the sealed HQ118 base:

`OBL034 = CLOSED_AT_EXACT_LIFECYCLE_ECONOMICS_GRAIN`

This worker installs runtime mechanics for that already-adopted authority. It does not create a replacement lifecycle authority.

## Runtime surface

Implementation:

`rawlsing_next/pre553_learned_product_lifecycle.py`

Runtime schema:

`PRE553_B5_LEARNED_PRODUCT_LIFECYCLE_RUNTIME@1.0.0`

Checkpoint schema:

`PRE553_B5_LEARNED_PRODUCT_LIFECYCLE_CHECKPOINT@1.0.0`

Primary public types:

- `LearnedProductLifecycleSubject` — B5-side opaque exact product/release view; not an M2 ReleaseCore.
- `LearnedProductReleaseProtocol` — narrow adapter protocol for later I2/M2 integration.
- `SelectionKey` — exact family + scope + purpose + optional consumer-partition namespace.
- `LearnedProductLifecycleEvent` — immutable B5 event with exact parent, authority, rule, evidence and content hash.
- `CurrentSelectionReceipt` — exact explicit current-selection receipt.
- `NoCurrentReceipt` — exact explicit no-current receipt.
- `InvalidationReceipt` — determinant-local direct/transitive invalidation result.
- `RebuildEligibilityReceipt` — typed rebuild eligibility or blocker.
- `RebuildLinkReceipt` — exact old/new rebuild relationship without semantic synthesis.
- `GCElegibilityReceipt` — recomputable learned-product payload GC eligibility with source/carrier-retirement firewall.
- `LearnedProductDeterminantGraph` — subject-neutral product determinant traversal.
- `LifecycleReplayReceipt` — exact checkpoint/restart replay identity.
- `LearnedProductLifecycleExecutor` — append-only B5 runtime owner.

Primary executor operations:

- `stage_release`
- `stage_protocol`
- `register_product`
- `publish_product`
- `record_recertification`
- `selection_key`
- `select_current`
- `declare_no_current`
- `resolve_selection_exact`
- `supersede_current`
- `withdraw_product`
- `declare_invalidation`
- `record_rebuild_eligibility`
- `link_rebuild`
- `record_cache_materialized`
- `record_cache_dropped`
- `attest_gc_eligibility`
- `record_payload_gc`
- `release_history`
- `resolve_current_as_of`
- `export_checkpoint`
- `from_checkpoint`
- `audit_replay`

## B5 ownership boundaries

The runtime owns lifecycle facts only.

It does **not** own or infer:

- producer semantic truth;
- M1 learned-empirical validation/adjudication;
- M2 release-core construction or publication-binding semantics;
- AuthoritySnapshot production/currentness;
- source semantics;
- source-universe composition or measurement comparability;
- Field Forge structural admission;
- PRE-V3 target-use permission;
- V3/actor knowledge or causal permission;
- source/carrier retirement;
- physical architecture selection.

Freeze:

`SEMANTIC_OWNER != CARRIER_OWNER != LIFECYCLE_OWNER`

`REPOSITORY_PRESENCE != PRODUCT_REGISTERED`

`PRODUCT_REGISTERED != PRODUCT_PUBLISHED`

`PRODUCT_PUBLISHED != CURRENT_SELECTED`

`CURRENT_SELECTED != CONSUMER_PERMISSION`

## Current-selection law

Currentness exists only as an exact receipt under an exact `SelectionKey`.

The runtime has no latest/default/newest/semver/file-order selection API.

A selection update uses an exact expected prior receipt. A stale expected receipt fails with typed `CONFLICTING_CURRENT_SELECTION` before mutation.

`NO_CURRENT` is explicit through `NoCurrentReceipt`.

Different selection purposes or consumer-context partitions can hold distinct exact current selections without conferring permission.

## B5 supersession law

Because B5 is controlling where M3 differs, `supersede_current` implements the B5 rule:

- exact current predecessor;
- exact successor;
- explicit supersession basis;
- explicit selection attestation;
- one nondestructive `CURRENT_SUPERSEDED` event;
- exact new `CurrentSelectionReceipt`.

The predecessor remains immutable historical capital.

## Withdrawal and invalidation atomicity

If a product is current, withdrawal or determinant invalidation cannot leave an implicit current pointer.

The operation must provide, for every affected exact `SelectionKey`:

- an exact replacement release; or
- explicit `NO_CURRENT`.

Self-replacement by the withdrawn/invalidated product is rejected before mutation.

## Authority-change determinant law

B5 LCR-009 is implemented without importing Authority42 lifecycle semantics.

Exact `AuthorityRef` values are converted into neutral content-addressed `B5Lifecycle:AUTHORITY_DETERMINANT` keys solely for product invalidation traversal.

This means an exact authority change can invalidate the exact direct/transitive learned-product closure while `AuthoritySnapshot` lifecycle ownership remains external.

## Physical neutrality

No database, filesystem, object store, cache layout, source carrier, or endpoint is selected.

A staged exact release is not lifecycle-registered merely because a repository can see it.

Cache materialization/loss is explicitly performance-only for `OPTIONAL_CACHE_ACCELERATOR`.

Payload GC is limited to `RECOMPUTABLE_PRODUCT_PAYLOAD` after exact reconstruction/history/serving/no-byte-dependency/source-retention proofs.

## Terminal owner receipt

`B5_CURRENT_OWNER_IMPLEMENTED__DEDICATED_LEARNED_PRODUCT_RUNTIME__NO_AUTHORITY42_ALIAS__NO_M1_M2_FIELD_FORGE_OR_SOURCE_RETIREMENT_WIDENING`
