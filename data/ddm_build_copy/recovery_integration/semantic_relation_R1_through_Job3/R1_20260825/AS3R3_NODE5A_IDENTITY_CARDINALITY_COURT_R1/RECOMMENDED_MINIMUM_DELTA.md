# Recommended Minimum Delta — AS3R3 Node 5A Cardinality

## Required HQ act

Issue one bounded HQ authority that adopts **Disposition A** and corrects count language only.

Freeze:

`19_PREDICATE_SOURCE_ROLES__19_ROLE_TO_REF_ROWS__18_DISTINCT_CANONICAL_PREDICATES__SOLE_ALIAS_A000_A1RAPP`

The act should state:

1. Accepted AS3 remains exactly 19 predicate semantic source/role rows.
2. Accepted Node 4A remains exactly 19 complete predicate input records.
3. Node 5A invokes the frozen producer on all 19 records.
4. Node 5A freezes exactly 19 AS3-source/role-to-successor-ExactRef mapping rows.
5. Lawful distinct canonical `EmpiricalPredicate@1.0.0` cardinality is exactly 18.
6. The sole permitted predicate alias class is `{A000,A1RAPP}`; any additional duplicate is a blocker.
7. A000 and A1RAPP remain distinct semantic/candidate roles even though their accepted executable predicate semantics share one canonical ref.
8. The canonical object catalog serializes the shared predicate once; provenance/crosswalk artifacts preserve both roles.
9. Source IDs, source kinds, candidate-role labels, derivation wrappers, and old AS3R2 hashes may not be injected into canonical predicate identity merely to force uniqueness.
10. The 22-row succession crosswalk remains 22 rows. Its two A000/A1RAPP rows may cite the same future successor ref; row uniqueness remains by source identity and historical ref.
11. Node 4B resolves predicate use by source/role ID through the 19-row mapping rather than positional assumptions about 19 unique refs.
12. Independent hostile validation proves the alias class is exactly reproducible and behavior-preserving.
13. AS4I0 successor adaptation validates 19 predicate role mappings and 18 distinct canonical predicate representations.
14. Candidate count 82, exact candidate membership/order, K=18, J=2, depth=18, RAW-only measure, one risk partition, two topology partitions, no-pruning law, RNG NONE, support law, and common A/B/C terrain remain unchanged.

## Do not change

- `rawlsing_next/pre553_as3r3_runtime_producer.py`
- `rawlsing_next/pre553_as3r3_runtime_producer_contract.py`
- `rawlsing_next/pre553_empirical_objects.py`
- accepted Node 4A predicate semantic mappings
- AS3 candidate descriptors or candidate commitments
- AS3R2 historical artifacts
- accepted historical AS4I0
- Route A/B/C architecture

## Why this is minimum

The producer and canonical object law are behaving correctly. Changing them to manufacture a nineteenth identity would corrupt semantic identity. The contradiction lies in downstream count expectations that assumed a one-to-one correspondence between source roles and canonical objects.

After HQ adopts this count law, the next execution should be a bounded Node 5A replay/seal only. Query input freeze remains downstream.
