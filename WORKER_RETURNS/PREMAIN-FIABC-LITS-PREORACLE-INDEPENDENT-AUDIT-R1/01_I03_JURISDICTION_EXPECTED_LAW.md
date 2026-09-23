# I03 Successor Jurisdiction — Independent Expected Law

## Baseline finding

At `4513eae0ec2c55c3252871c77cd52fc3dd0f07cd`, `I03OperationSuccessorContract` makes both requested fields part of the successor authority's content-addressed record:

- `runtime_catalog_identity`
- `parent_operation`

That documentary binding is not executable jurisdiction.

The generic resolver `Pre553RuntimeAuthoritySet.authorize_i03_operation_successor(...)` currently matches:

- parent authority ref == supplied snapshot authority ref;
- runtime snapshot content hash == supplied snapshot content hash;
- successor operation == requested operation;
- query ref is in the successor's frozen query set;
- source-universe refs match exactly;
- required object family is governed;
- snapshot is an ALLOW `PREDICATE_GRAMMAR`;
- parent authority is named by the query.

It does **not** receive or compare the active runtime catalog identity, and it does **not** require `contract.parent_operation` to be one of the supplied parent snapshot's governed operations.

## Exact minimum executable law

A successor may authorize an I03 operation **iff**, in addition to the existing exact checks:

1. the caller supplies the exact identity of the `RuntimeObjectCatalog` from which the executing query/predicate were resolved;
2. `contract.runtime_catalog_identity == executing_runtime_catalog_identity`;
3. `contract.parent_operation in snapshot.governed_operations`;
4. all pre-existing exact parent-authority, snapshot-hash, successor-operation, query, universe, family, authority-kind/state, and query-authority-ref checks continue to pass.

This is conjunctive law. Neither a correct catalog with a wrong parent operation nor a correct parent operation with a wrong catalog is sufficient.

## Execution plumbing

The identity source must be the exact execution catalog:

`CarrierNeutralResearchExecutor.runtime_catalog : RuntimeObjectCatalog`

whose canonical receipt already exposes:

`runtime_catalog.receipt()["catalog_identity"]`.

Expected plumbing:

`CarrierNeutralResearchExecutor.execute_i03 / execute_i05`
→ exact `RuntimeObjectCatalog` identity
→ `execute_empirical_query(...)`
→ `_require_exact_i03_authority_fitness(...)`
→ `Pre553RuntimeAuthoritySet.authorize_i03_operation_successor(..., runtime_catalog_identity=...)`.

The identity must not be inferred from a global default. It must not be reconstructed from `AuthorityRegistry` alone, because the catalog identity binds predicates, queries, and discovery authorities in addition to authority snapshots.

### Compatibility law

Direct I03 execution that succeeds under the parent snapshot without using a successor should not acquire an unrelated source-specific requirement. Catalog identity becomes jurisdictionally mandatory **when the successor fallback is being invoked**. Generic carrier-neutral executor paths can and should always supply it.

## LiTS exact declarations to remain unchanged

Accepted LiTS successor declaration:

- runtime catalog: `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`
- parent operation: `AS2B_LITS1_I03_QUERY`
- successor operation: `PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`
- source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- frozen workload: 50 candidates / 77 query-role executions.

The repair changes jurisdictional enforcement, not the LiTS declaration.

## Required hostile tests

A field-presence assertion is not enough. Minimum new hostile negatives:

### Wrong catalog, otherwise lawful

Construct/adopt an internally valid successor contract whose:
- parent authority/snapshot;
- parent operation;
- successor operation;
- query;
- universe;
- object family

all match, but whose `runtime_catalog_identity` differs from the catalog used by the executor. The exact I03 call must fail closed **because of catalog mismatch**.

The test must not rely on an invalid authority-content hash. Recompute the authority record identity and include it in the test runtime's adopted hashes so hash tamper detection cannot accidentally stand in for jurisdiction.

### Wrong parent operation, otherwise lawful

Construct/adopt an internally valid successor contract with a `parent_operation` not present in `snapshot.governed_operations`, while all currently enforced dimensions match. It must fail closed **because the declared parent operation is outside the supplied historical snapshot**.

Again, rehash/adopt the test authority so the negative reaches the jurisdiction predicate.

### Positive exact match

The accepted LiTS successor must still authorize all and only its frozen query set when exact catalog and exact parent operation match.

### Generic noninterference

WVS7 accepted current behavior must remain exactly `{"COVERAGE_LIMITED":46}`; see `05_WVS7_NONINTERFERENCE_REQUIREMENTS.md`.

## Current test adjudication

`test_lits_i03_operation_successor_record_is_exact_and_narrow` proves the record is exact/narrow and contains the catalog declaration. It does not prove the catalog field is consulted at execution.

`test_lits_frozen_catalog_is_unchanged_and_exact_successor_closes_i03_gate` proves the successor is necessary for the accepted LiTS path. It does not prove the resolver is catalog-jurisdictional or parent-operation-jurisdictional.

`test_lits_i03_successor_rejects_unadopted_or_tampered_record` proves immutable authority-content/adoption law. It does not prove that a valid newly hashed/adopted successor with the wrong catalog or wrong parent operation is rejected.

## WVS7 effect expectation

The repair is generic, but no LiTS-specific successor must leak into WVS7. If WVS7 resolves without this I03 successor, the new checks are dormant and its material must remain unchanged. If any WVS path invokes a successor, it must supply and satisfy its own exact catalog/parent law; no fallback to the LiTS catalog is permissible.
