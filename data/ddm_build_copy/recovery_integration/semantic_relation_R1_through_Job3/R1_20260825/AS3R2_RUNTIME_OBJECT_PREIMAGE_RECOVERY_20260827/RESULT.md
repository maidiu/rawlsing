# AS3R2 Runtime-Object Preimage Recovery

Disposition: **FAIL CLOSED**

Return token:

`AS3R2_RUNTIME_OBJECT_PREIMAGE_RECOVERY_FAIL_CLOSED__AS3R2-B01__AUTHORITATIVE_RUNTIME_OBJECT_PRODUCER_UNREACHABLE_AND_CANONICAL_PREIMAGES_UNSERIALIZED`

## Scope

This cell was executed only as canonical identity recovery for the 19 frozen `EmpiricalPredicate` refs and 3 frozen `EmpiricalQuerySpec` refs sealed by accepted AS3R2 at `aae978928d2416c23d6b1562e7ac559b106b2cf7`. No LiTS-I run, candidate execution, I05 semantic change, AS3R2 authority change, AS4I0 change, or route ranking occurred.

## Positive recovery

The accepted AS3R2 runtime binding manifest positively preserves exactly 19 predicate runtime refs and 3 query runtime refs. Those 22 identities are reproduced exactly in the two failure catalogs and the crosswalk in this directory.

The production identity law is also recoverable from `rawlsing_next/pre553_empirical_objects.py`: identity is SHA-256 over the canonical semantic projection containing `schema_id`, `schema_version`, `typed_state`, canonical `authority_snapshot_refs`, canonical `dependency_refs`, `producer_replay_locator_or_reference_root`, and complete normalized family `semantic_fields`.

## Exact blocker

The accepted AS3 atom/query catalogs do not serialize that complete runtime projection. They preserve descriptive AS3 semantics and AS3 identities, while AS3R2 preserves the resulting runtime refs. The missing bridge is the exact construction invocation/material that produced those refs.

The AS3R2 construction lineage records the producer as:

- commit `b0ed3d1509421011816f5ac694f9d1ec875c5bf5`
- path `rawlsing_next/pre553_late_run_evidence.py`
- recorded file SHA-256 `17852eb0e8369550f629375e0fcc03053dfe77b2ae4faa1728cf4cf8e1c019fb`

That commit is not reachable/resolvable in the current repository graph, and that file is not present at the accepted AS3, AS3R1, or AS3R2 heads examined. Reachable `pre553_discovery_exact.py` consumes and verifies already-instantiated runtime objects; it does not regenerate their constructor preimages. AS3R1 preserves the 19/3 catalogs and changes the support rule; it does not serialize these preimages.

Therefore the exact values of the identity-bearing closure fields cannot be proved for any of the 22 objects. Reconstructing them from atom names, descriptions, AS3 semantics, or target hashes would violate the governing rule:

`SEMANTIC_EQUIVALENCE != IDENTITY_RECOVERY`

No such reconstruction was attempted.

## Frozen invariants

- predicate count: 19
- query count: 3
- predicate aggregate hash: `8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293`
- query aggregate hash: `f76ddf2b8a99e6a05884d503aa7a5da8fbf1fb3b07fbcd4cc93597457defa423`
- DiscoveryAuthority: `98d52062a0acc04a1949053a8f83397621e810950ff70ceff0260b68d17fd28c`
- official frontier: `84349595622ed6eec5bd6af60de5b74df26ae6752ae64e40d7595fd7560b7d67`
- candidate count: 82
- candidate executions: 0

The aggregate hashes above are verified as unchanged sealed anchors, **not** claimed as hashes reproduced from recovered canonical preimages.

## AS4I0 handoff status

Not ready. The failure catalogs intentionally are not production-instantiable AS4I0 runtime catalogs. They preserve the exact frozen IDs while marking `canonical_preimage = null`; making them instantiable without the missing historical construction evidence would manufacture identity.
