# I2 M2 — VIRTUAL / MATERIALIZED PARITY RECEIPT

## Holding

Release semantic identity is representation-neutral.

`SAME_RELEASE_CORE + DIFFERENT_EXACT_REPRESENTATION -> SAME_RELEASE_ID + DIFFERENT_PUBLICATION_BINDING_ID`

## Materialized witness

A `CONTENT_ADDRESSED_MATERIALIZATION` representation binds:
- exact release ref;
- exact resolved producer-subject ref;
- exact producer-contract ref;
- exact resolver/locator ref;
- exact representation-integrity ref.

## Virtual witness

A `GOVERNED_VIRTUAL_REBUILDER` representation is admitted only if the release's replay closure declares:

`EXACT_DETERMINISTIC_REBUILD`

and the rebuilt exact subject ref plus producer contract exactly match ReleaseCore.

A mismatch fails with:

`REBUILD_SEMANTIC_MISMATCH`.

## Governed tests

- `test_08_virtual_rebuild_parity_and_mismatch_detection` — PASS.
- `test_09_materialized_virtual_semantic_parity` — PASS.
- `test_03_physical_relayout_changes_binding_not_release_core` — PASS.

The materialized and virtual witnesses resolve:
- the same exact ReleaseCore;
- the same exact producer-owned subject;
- different PublicationBinding identities.

The implementation therefore gives retained bytes no extra semantic authority and gives a virtual resolver no exact-replay claim without the required replay grade.

Disposition:

`M2_MATERIALIZED_VIRTUAL_PARITY_SOURCE_FREE_GREEN`
