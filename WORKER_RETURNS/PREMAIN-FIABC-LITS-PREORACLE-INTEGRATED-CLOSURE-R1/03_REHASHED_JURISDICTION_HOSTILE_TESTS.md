# Rehashed I03 Jurisdiction Hostile Tests

The independent audit required negatives that cannot pass merely because a mutated authority record has an invalid identity hash.

## Wrong executing catalog

The test:
1. clones the accepted successor authority record;
2. changes only `runtime_catalog_identity`;
3. recomputes `authority_content_hash = semantic_hash(identity_material)`;
4. adopts the new hash in a fresh `Pre553RuntimeAuthoritySet`;
5. retains the accepted historical parent snapshot;
6. executes authorization under the real accepted LiTS runtime catalog.

The constructor accepts the internally valid hostile authority. Authorization then fails because the executing catalog and contract catalog do not match.

Result: **PASS**.

## Wrong historical parent operation

The test:
1. clones the accepted successor authority;
2. changes only `parent_operation` to `OTHER_PARENT_OPERATION`;
3. recomputes and adopts the authority hash;
4. retains the accepted runtime catalog, query, universe, family, snapshot, and successor operation;
5. supplies the exact adopted historical parent snapshot.

The constructor accepts the hostile authority. Authorization then fails because the hostile parent operation is absent from the exact historical parent's governed operations.

Result: **PASS**.

These are distinct from the retained ordinary tamper/hash-rejection tests.
