# Jurisdiction Holding

## Question presented

Whether the adopted LiTS-I `I03OperationSuccessorContract` may be consumed when its already-declared `runtime_catalog_identity` and `parent_operation` are not independently executed by the generic successor resolver.

## Holding

No. Both fields are jurisdictional, fail-closed predicates.

The successor is now consumable only if all of the following are simultaneously true:

1. the active runtime binding supplies a non-null exact lowercase SHA-256 catalog identity;
2. that supplied identity equals `contract.runtime_catalog_identity` exactly;
3. the contract's `parent_authority_ref` and `runtime_snapshot_content_hash` exactly match the supplied current/historical query authority snapshot as already governed;
4. the runtime authority set contains the exact adopted historical parent snapshot named by `contract.parent_authority_ref`;
5. the historical parent snapshot is positive `PREDICATE_GRAMMAR` authority;
6. `contract.parent_operation` is an exact member of that snapshot's `governed_operations`;
7. `contract.successor_operation` still equals the requested successor operation exactly;
8. query ref, source universe, object family, and exact query-authority parentage all continue to match.

Failure of any predicate rejects the successor.

## LiTS-I application

The LiTS-specific authority module supplies, rather than generic code inventing:

- runtime catalog: `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`;
- parent authority ref: `urn:rawlsing:pre553:as2b:lits1:authority:i03_query`, version `AS2A-BANKED-1.0.0`, content hash `6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d`;
- parent operation: `AS2B_LITS1_I03_QUERY`;
- successor operation: `PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`.

The historical parent snapshot is reconstructed from the accepted banked AS2B builder law. Its authority hash was minted from the builder's pre-canonical material, whose family sequence is exactly:

```text
EmpiricalPredicate@1.0.0
EmpiricalQuerySpec@1.0.0
EmpiricalFact@1.0.0
```

That sequence is preserved for the historical preimage; `AuthoritySnapshot` may canonicalize its set-like public field afterward. No hash was rewritten and no authority identity was relaxed.

## Negative law

The repair does not permit:

- version fallback;
- catalog aliases;
- adjacent-catalog equivalence;
- same-object/same-query catalog substitution;
- source-name dispatch inside the generic resolver;
- substring or alias matching for operations;
- successor-operation substitution for parent-operation authority;
- inference of operation from authority kind;
- globally mandatory catalog identities where no adopted I03 successor is being consumed.

Absent runtime authority context retains predecessor behavior. A runtime context that carries an adopted I03 successor but omits catalog identity fails closed when that successor is required.
