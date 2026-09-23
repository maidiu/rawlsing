# Court 2 — I03 Runtime-Catalog Jurisdiction

## Result

**PASS**

The integrated execution chain implements the jurisdiction law required by Worker A.

## Actual runtime catalog origin

LiTS runtime materialization constructs the current `RuntimeObjectCatalog`.

Its actual catalog identity is computed by:

`catalog.receipt()["catalog_identity"]`

The LiTS runtime materializer verifies that computed identity against the adopted R6O identity before returning runtime material.

The oracle producer independently reconstructs the catalog from the runtime documents and again verifies:

`catalog.receipt()["catalog_identity"] == LITS_RUNTIME_CATALOG`

This is the identity of the exact authorities, predicates, queries and discovery authority actually used.

## Runtime binding

`RuntimeBinding` contains:

`runtime_catalog_identity: str | None`

`bind_runtime(..., runtime_catalog_identity=...)`:

- requires a lowercase 64-hex SHA when supplied;
- stores it in the active runtime binding.

The LiTS neutral execution binds:

`runtime_catalog_identity=catalog.receipt()["catalog_identity"]`

There is no ambient/default catalog substitution in this chain.

## I03 successor resolution

When historical I03 authority is not directly sufficient, the query path invokes:

`authorize_i03_operation_successor(..., runtime_catalog_identity=runtime_binding.runtime_catalog_identity, ...)`

The generic resolver:

- requires exact catalog identity text;
- checks exact SHA shape;
- requires `contract.runtime_catalog_identity == runtime_catalog_identity`;
- requires exact parent authority ref;
- exact successor operation;
- exact query ref;
- exact universes;
- exact object family;
- unique exact successor;
- exact historical parent adopted and positive.

Absence of the catalog identity therefore fails when fallback is invoked.

## Parent operation

After the exact successor contract is selected and its historical parent resolved, the resolver explicitly requires:

`contract.parent_operation in historical_parent_snapshot.governed_operations`

Failure raises:

`I03 successor parent operation is absent from exact historical authority`

## Generic law

The generic resolver does not contain a LiTS runtime catalog constant. Source-specific catalog identity is data inside the LiTS successor authority record and is passed from the actual runtime execution context.

## Hostile negatives

The integrated test helper:

`_rehashed_successor_record(...)`

mutates identity material and then recomputes `authority_content_hash = semantic_hash(identity_material)`.

The integrated runtime helper explicitly adopts the recomputed successor hash.

### Wrong catalog

The hostile record changes only `runtime_catalog_identity` to another valid SHA-domain value, rehashes it, and adopts it.

Other jurisdiction dimensions remain lawful.

The call supplies the live catalog identity.

Failure therefore occurs because no exact successor matches the live catalog—not because the authority hash is stale or unadopted.

### Wrong parent operation

The hostile record changes `parent_operation`, rehashes it, and adopts it.

Catalog/query/universe/object-family/snapshot/successor operation remain lawful.

Selection succeeds because parent operation is intentionally checked against the parent after contract matching.

The test requires the exact failure:

`parent operation is absent from exact historical authority`

Thus this negative reaches the intended predicate.

## Holding

Worker A's original jurisdiction defect is closed in the integrated tree.
