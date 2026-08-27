# AS4I0 Route-B bounded implementation scope

Status: bounded implementation committed; real-source C05R2B execution NOT performed.

This directory banks only the exact accepted inputs needed by the Route-B driver:
- AS3R2 frontier authority, runtime binding, DiscoveryAuthority, grammar, official frontier, replay closure, and final seal;
- the accepted AS2B LiTS-I source-backed construction script;
- the accepted AS2A slot ledger and source-specific projection authority package.

The implementation validates the frozen cross-checks before any source execution:
- DiscoveryAuthority: 98d52062a0acc04a1949053a8f83397621e810950ff70ceff0260b68d17fd28c
- official frontier: 84349595622ed6eec5bd6af60de5b74df26ae6752ae64e40d7595fd7560b7d67
- candidate count: 82
- predicates/query templates: 19 / 3
- pre-candidate fairness blockers: 0
- pruning: NONE_EXACT_EVALUATE_ALL
- minimum_raw_denominator: 0

Fail-closed blocker discovered in the exact accepted AS3R2 artifacts:
AS4I0-B01__AS3R2_RUNTIME_CATALOG_CANONICAL_OBJECT_PREIMAGES_NOT_SERIALIZED.

The AS3R2 seal contains the exact 19 EmpiricalPredicate refs and 3 EmpiricalQuerySpec refs, but no full canonical object projections (including producer replay roots). The existing I05 executor requires actual immutable EmpiricalPredicate / EmpiricalQuerySpec objects and verifies semantic_projection hashes. A SHA-256 ref is not an invertible serialization, and guessing replay identity material would manufacture authority/identity. The driver therefore requires those exact 22 canonical object payloads and validates every supplied object against the sealed refs before delegating to execute_exact_bounded_discovery.

No transformed empirical payload is banked here. The accepted AS2B builder reconstructs C11 from the exact LiTS-I source in memory; RouteBSourceSession.close() releases those references. Receipts emitted by the runner contain hashes, counts, states, and resource/session-boundary metadata only.

Later lawful production work after AS4I0-B01 is cured:
1. supply the exact canonical serialized preimages for all 19+3 sealed runtime objects from the authoritative construction that produced AS3R2;
2. run the one-command production entry point in a fresh process with exact LiTS-I SHA 7cac43e2...;
3. rebuild the accepted AS2B C11 release/repository from source;
4. invoke existing execute_exact_bounded_discovery exactly once;
5. require executed frontier 843495... and 82/82 terminal coverage;
6. emit execution/replay/resource/session-boundary receipts and terminate the process.
