# V01 — T02 PREDECESSOR-LINEAGE FAIL-CLOSED REPAIR R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w20-v01-t02-predecessor-lineage-repair-r1`

Commission tip: `acc37ce514af887a5f5918fab454c7d28d90305d`

Commission base / HQ authority: `43aafdae67d7b56da13e3e0d0695e36731fe18e7`

Exact grain:

`SDTF_R4_GENERIC_BATCH_ADAPTER_PREDECESSOR_LINEAGE_FAIL_CLOSED_REPAIR_R1_ONLY`

Library: `NOT USED`

## Terminal

**PASS**

`T02_PREDECESSOR_LINEAGE_DEFECT_REPAIRED__FRESH_INDEPENDENT_QUALIFICATION_REQUIRED`

This is a bounded repair PASS only. It is not independent qualification and does not authorize generic R4 batch production use.

## Repaired implementation

Artifact:

`rawlsing_next/sdtf_r4_generic_batch_adapter.py`

Repaired Git blob:

`f6427a42524086194ed6fca9ba2387561ff00891`

Producer implementation blob replaced:

`c1a495c7a23d4ebee086fd5410d9627f4aefb695`

The repair is confined to predecessor closure inside `adapt_generic_r4_batch(...)`.

For generation `N > 0`, syntax-only predecessor identity is no longer enough. The frozen S03 interface exposes no separate immutable lineage resolver at this grain, so a successor now receives lawful predecessor proof only from a co-present predecessor row whose **full supplied exact ref equals its computed row ref**, including the content hash. The successor's `predecessor_row_ref.key` must match one of those identity-valid co-present exact refs.

If the prior snapshot is absent, carries a forged hash, or is represented by a stale/mismatched supplied ref that does not equal the row's computed identity, the adapter adds the existing `PREDECESSOR_CHAIN_INVALID` failure and projection remains closed.

The existing local lineage shape law is unchanged:

- generation `0` requires null predecessor;
- generation `N > 0` requires non-null predecessor;
- predecessor kind must be `SDTF_R4_GENERIC_BATCH_CANDIDATE_ROW`;
- predecessor object id must be exactly the same namespace/candidate id at generation `N-1`.

No registry, resolver, selector, new lineage architecture, S03 redesign, or R4 redesign was introduced.

## Tests

The producer test artifact is preserved byte-for-byte:

`rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter.py`

Git blob:

`7b4190601757fa69352d1a990c27242c67226cae`

V01 adds one bounded repair-regression artifact:

`rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter_predecessor_lineage_repair.py`

Git blob:

`a8fcb9f4f0d260f4660b89df0a74493c6dffda8e`

Exact V01 regression identities:

1. `test_forged_predecessor_hash_with_prior_absent_fails_closed`
2. `test_exact_predecessor_copresent_is_lawfully_accepted`
3. `test_wrong_predecessor_hash_with_prior_copresent_fails_closed`
4. `test_matching_supplied_ref_from_identity_invalid_prior_does_not_prove_lineage`
5. `test_generation_zero_with_nonnull_predecessor_fails_closed`
6. `test_generation_positive_with_null_predecessor_fails_closed`
7. `test_lineage_failure_is_row_local_and_unrelated_valid_row_still_projects`
8. `test_exact_lineage_repair_does_not_change_row_or_batch_identity_law`
9. `test_repair_does_not_weaken_existing_non_lineage_boundaries`

The ninth regression reuses the unchanged producer tests for exact duplicate idempotence, same-key/same-generation conflict quarantine, silent N/A rejection, candidate-only projection closure, currentness/evidence closure, and no invention of authority/ref/body/currentness.

## U01 blocker closure

U01 blocker:

`PREDECESSOR_CHAIN_INVALID_NOT_FAIL_CLOSED_FOR_UNPRESENTED_PRIOR_SNAPSHOT`

U01 counterexample after this repair:

- successor generation `1`;
- predecessor kind/object id syntactically correct;
- predecessor content hash forged;
- prior snapshot absent.

The forged predecessor key is not present in the identity-valid co-present predecessor-ref set, so the successor receives `PREDECESSOR_CHAIN_INVALID` and cannot project.

The co-present wrong-hash case also fails because the actual prior row contributes its real exact ref, not the forged predecessor ref.

A co-present row with a stale supplied ref also cannot prove lineage, because only rows with `supplied_ref == computed_ref` contribute to the predecessor-proof set.

## Identity and boundary preservation

The repair does not alter candidate-row identity material, batch identity material, receipt shape, determinant grammar, package partition, duplicate deduplication, same-generation conflict quarantine, authority semantics, N/A laws, value-mode/calibration laws, currentness laws, or the adopted R4 projection constructor.

The producer test artifact remains exactly `7b4190601757fa69352d1a990c27242c67226cae`.

No source/question semantics were adjudicated. No authority was issued. No concrete rule was minted. No rule currentness was selected. No actor/entity fact was materialized. No topology was constructed. No V3/person state or OBL063 semantics were entered. MAIN and PRE-MAIN were not mutated.

## Execution status

No fresh independent qualification is claimed by this return.

The commission explicitly permits HQ to bank the repaired candidate while actual-repository execution remains behind the neutral-smoke execution gate. The repaired implementation and both test artifacts are committed for the required fresh independent qualification when that execution gate is available.

`REPAIR_PASS != INDEPENDENT_QUALIFICATION`

## Successor gate

PASS wakes exactly one fresh independent qualification of the repaired T02 adapter.

Only that successor may decide whether the repaired adapter is independently qualified for HQ adoption/closure. Generic R4 batch production use remains dormant until that successor passes.
