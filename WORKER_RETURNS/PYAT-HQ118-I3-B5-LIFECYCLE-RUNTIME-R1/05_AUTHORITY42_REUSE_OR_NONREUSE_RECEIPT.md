# PYAT HQ118 I3 — Authority42 Reuse / Non-Reuse Receipt

## Holding

Authority42/A03 is **not** reused as the generic learned-product lifecycle owner.

The I3 runtime is a dedicated B5 implementation.

Freeze:

`AUTHORITY_SNAPSHOT_LIFECYCLE != LEARNED_PRODUCT_LIFECYCLE`

`AUTHORITY_RELEASE_RECEIPT != LEARNED_PRODUCT_CURRENT_SELECTION_RECEIPT`

`AUTHORITY42_MECHANICS_PRECEDENT != AUTHORITY42_OWNER_PROMOTION`

## What was not reused

The I3 runtime does not import:

`rawlsing_next.pre553_authority_maintenance`

It does not alias or subclass:

- `AuthorityMaintenanceExecutor`
- `AuthorityReleaseReceipt`
- `AuthorityInvalidationReceipt`
- `MaintenanceEvent`
- `MaintenanceReplayReceipt`
- `SemanticDeterminantGraph` from Authority42

It does not call Authority42 promotion/rollback methods.

It does not use AuthoritySnapshot current pointers as learned-product current pointers.

It does not infer product lifecycle state from authority lifecycle state.

## Neutral primitives reused

I3 reuses only repository-wide neutral exact-identity primitives from:

`rawlsing_next.pre553_empirical_objects`

Specifically:

- `ExactRef`
- `AuthorityRef`
- `exact_ref`
- `authority_ref`
- `canonicalize`
- `semantic_hash`

These are identity/canonicalization primitives, not Authority42 lifecycle ownership.

## AuthorityRef determinant bridge

B5 LCR-009 requires an authority change to be an explicit product determinant.

I3 therefore converts an exact `AuthorityRef` into a neutral content-addressed:

`B5Lifecycle:AUTHORITY_DETERMINANT`

The projection contains only:

- determinant class `SEMANTIC_AUTHORITY_REF`;
- the exact authority id/version/content-hash tuple.

This key participates only in B5 product invalidation traversal.

It does **not**:

- resolve the AuthoritySnapshot;
- change Authority42 currentness;
- promote/rollback an authority;
- reinterpret authority semantics;
- create a learned-product permission.

This is an identity bridge, not owner reuse.

## Anti-alias runtime guards

`LearnedProductLifecycleSubject` rejects learned-product release refs whose exact kind is:

- `AuthoritySnapshot`
- `AuthoritySnapshot@1.0.0`
- `AuthorityReleaseReceipt`
- `Maintenance:RELEASE`

The hostile suite directly proves the first three relevant noncollapse cases.

## Parallel non-regression proof

Final I3 governed qualification:

- workflow run: `36326914249`
- governed-court step: `60 passed in 0.61s`
- I3 lifecycle tests: 38
- existing `test_pre553_authority_maintenance.py` tests in the same court: 22
- protocol self-test: 20 passed
- artifact: `rabochii-court-receipt-36326914249`
- artifact id: `10933214853`
- artifact digest: `sha256:72d4527202693805aa9f0600935d63c686acff404cf3b1004bf693e5512f7996`

Thus the learned-product runtime is green **alongside** the current Authority42 executor rather than by replacing or mutating it.

## Final disposition

`AUTHORITY42_NONREUSE_CONFIRMED__NEUTRAL_IDENTITY_PRIMITIVES_ONLY__AUTHORITYREF_DETERMINANT_BRIDGE_ONLY__22_AUTHORITY42_TESTS_GREEN_WITH_I3`
