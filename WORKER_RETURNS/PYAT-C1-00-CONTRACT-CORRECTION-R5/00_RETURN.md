# PYAT C1-00 — CONTRACT CORRECTION R5 — AT07 PREIMAGE COMPLETION RETURN

## Disposition

`PREIMAGE_UNDERDETERMINED__CONTRACT_CORRECTION_REQUIRED`

The four requested historical preimages cannot be reconstructed lawfully from the accepted C1 fixture/owner material without guessing identity-bearing caller inputs and testing those guesses against the already-frozen SHA-256 outputs.

This is not a hash mismatch. It is a preimage-specification failure.

## Exact governing inputs inspected

- R2 condition/value relation oracle and witness schema.
- R3 exact AT07 universe/release/query-authority synchronization.
- R3 noncircular evidence preimages and exact identity spine.
- R4 independent rereview/recomputation artifacts.
- current active C1 analytical contract and fixture oracle.
- current public `ConditionerBinding.material()` and `PositionedSubjectPossibilityQuery.material()` owner at blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7`.
- frozen C1-01 production implementation blob `5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`.

## Why the forward/reverse query preimages are underdetermined

The owner hashes all of these fields:

- `contract`;
- `query_id`;
- `purpose`;
- `subject_ref`;
- `target_ref`;
- `source_universe_ref`;
- `release_ref`;
- full sorted `conditioner_bindings`;
- `requested_projection`.

The accepted packet fixes contract/purpose, target, source, release, binding id, subject-condition fact ref, empirical coordinate, and comparability authority.

It does **not** freeze:

1. `query_id`;
2. query-level `subject_ref`;
3. `requested_projection`;
4. `ConditionerBinding.effective_time_or_interval`.

The public owner does not derive those values. It only validates them:
- `query_id` must be a nonempty non-fuzzy string;
- `subject_ref` must be an `ExactRef`;
- `requested_projection` need only canonicalize;
- binding effective time need only canonicalize.

No accepted C1 artifact supplies an equality rule that determines those four values. In particular, the frozen R2 `subject_condition_preimage_ref` is the binding's `subject_fact_ref`; it is not declared to be the query-level `subject_ref`.

The frozen query hashes therefore cannot be used as a semantic selector without doing the prohibited operation: inventing candidate labels/refs/projections/times and testing them against SHA-256.

## Why the witness preimages are underdetermined

R2 requires the full witness to bind:

- `consumer_query_ref`;
- full `consumer_binding_material`;
- `consumer_binding_fingerprint`;
- subject preimage ref/material;
- producer query ref;
- producer predicate ref;
- `producer_predicate_hash`;
- producer normalized leaf ref/projection;
- pairing ref/authority;
- source/release/effective-time;
- binding mode.

The accepted packet does not freeze:

1. the binding's exact `effective_time_or_interval`, so the full binding material and binding fingerprint are not reconstructible;
2. the exact producer `predicate_hash` field required by the witness; only the outer `EmpiricalPredicate.ref` and normalized value-bearing leaf ref/projection are frozen;
3. an exact closed witness field set. R2 names `required_fields`, not an exact no-extra-field identity schema.

Thus even with the already-frozen `consumer_query_ref`, the full historical witness preimage is not uniquely specified.

## Important distinction

The accepted forward/reverse evidence preimages remain fully frozen and independently hash-reproducible because they contain the already-frozen witness **refs**, not the missing witness preimages.

Nothing in R5 disputes:

- forward evidence hash `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`;
- reverse evidence hash `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`;
- forward arithmetic `54/60`;
- reverse arithmetic `54/62`;
- R2/R3/R4 history.

## Minimum correction required

A competent correction authority must newly freeze—not claim to recover historically—the exact intended source-free AT07 values for:

- forward/reverse query `query_id`;
- forward/reverse query-level `subject_ref`;
- forward/reverse `requested_projection`;
- forward/reverse binding `effective_time_or_interval`;
- forward/reverse exact producer `predicate_hash` used by the witness;
- exact witness identity field set/material.

After those inputs are normatively frozen, the resulting hashes must be recomputed. If they do not equal the old four frozen hashes, the old hashes must be superseded by an explicit later correction rather than reverse-engineered.

No historical R2/R3/R4 artifact was edited.
