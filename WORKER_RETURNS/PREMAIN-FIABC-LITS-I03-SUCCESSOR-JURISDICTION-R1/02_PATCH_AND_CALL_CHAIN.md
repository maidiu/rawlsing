# Patch and Call Chain

## Call chain after repair

```text
LiTS RuntimeObjectCatalog.receipt()["catalog_identity"]
  -> bind_runtime(..., runtime_catalog_identity=<exact hash>)
  -> RuntimeBinding.runtime_catalog_identity
  -> I03 empirical-query authority fitness
  -> Pre553RuntimeAuthoritySet.authorize_i03_operation_successor(
       runtime_catalog_identity=...,
       historical_parent_snapshot=...
     )
  -> exact contract.runtime_catalog_identity equality
  -> exact adopted historical parent snapshot resolution
  -> exact contract.parent_operation membership
  -> existing exact successor/query/universe/family checks
```

The final LiTS oracle producer binds the catalog identity only after it has independently rebuilt the `RuntimeObjectCatalog` and checked that its receipt equals the frozen LiTS catalog identity.

## File-by-file patch

### `rawlsing_next/pre553_runtime_context.py`

Adds optional `runtime_catalog_identity` to `RuntimeBinding` and `bind_runtime()`, validated as an exact lowercase 64-hex SHA-256. Threads the value through runtime I03 and bounded-discovery wrappers. No global requirement is added for callers that do not consume an adopted successor.

### `rawlsing_next/pre553_runtime_authority.py`

Extends `authorize_i03_operation_successor()` with:

- exact `runtime_catalog_identity`;
- exact `historical_parent_snapshot`.

Contract selection now includes exact catalog equality. After selection, the resolver requires the supplied historical parent to equal the exact adopted runtime snapshot for `contract.parent_authority_ref`, requires positive predicate authority, and requires exact membership of `contract.parent_operation` in `governed_operations`.

All prior predicates remain in the same selection/validation path.

### `rawlsing_next/pre553_empirical_query.py`

Consumes the full current `RuntimeBinding`, not merely its authority set, and passes the binding's catalog identity plus the exact adopted historical parent snapshot into the successor resolver. With no runtime binding, predecessor failure behavior remains unchanged.

### `rawlsing_next/fiabc_lits_i_i03_operation_authority.py`

Adds a source-free reconstruction of the exact accepted AS2B `i03_query` parent authority. It preserves the banked builder's pre-hash family order and verifies the resulting semantic hash equals the already-frozen parent authority content hash before constructing the snapshot.

No LiTS constant is moved into generic runtime machinery.

### `rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`

Adopts the exact historical I03 parent snapshot and its already-frozen authority hash into the LiTS runtime authority set. The runtime catalog package itself is not modified; its catalog identity remains the frozen `5983d7...` value.

### `rawlsing_next/fiabc_final_oracle_freeze_producers.py`

After constructing the LiTS `RuntimeObjectCatalog` and checking its receipt against `LITS_RUNTIME_CATALOG`, binds that exact receipt identity into the runtime context used by the common I05/I03 path.

### `rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py`

Adds hostile jurisdiction tests for wrong/absent catalog identity, exact catalog passage, absent/different/exact parent operation, immutable-contract tampering, preexisting successor dimensions, absent runtime context, and WVS7 nonactivation.

## Genericity

Generic machinery knows only that an exact supplied catalog identity must equal the contract's exact catalog identity and that an exact adopted parent snapshot must authorize the contract's exact parent operation. It does not know the LiTS source name, LiTS catalog SHA, or LiTS operation names.
