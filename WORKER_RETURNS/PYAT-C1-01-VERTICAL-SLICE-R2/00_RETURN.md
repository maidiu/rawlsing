# PYAT C1-01 — VERTICAL SLICE R2 RETURN

## Disposition

`PREIMAGE_UNDERDETERMINED__CONTRACT_CORRECTION_REQUIRED`

The commissioned continuation did not lawfully reconstruct the four missing AT07 canonical preimages.

The previous C1-01 production implementation remains frozen at blob:

`5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`

and was not edited.

## Exact finding

The old blocker was phrased as “preimages not exposed.” R5 sharpens it:

The accepted material does not merely fail to *publish* a recoverable object. It fails to *determine* several identity-bearing caller inputs required by the current public consumer owner.

For each `PositionedSubjectPossibilityQuery.material()`, the accepted packet does not freeze:

- `query_id`;
- query-level `subject_ref`;
- `requested_projection`;
- binding `effective_time_or_interval`.

For each witness, the accepted packet additionally does not freeze:

- exact `producer_predicate_hash` required by R2;
- an exact closed witness identity-material field set.

The owner accepts multiple lawful values for these dimensions. Therefore multiple semantically distinct query/witness constructions satisfy the accepted structural constraints. The frozen SHA-256 values cannot be used to choose among them without inventing candidate material and hash-testing it, which this commission expressly forbids.

## Consequence

The red missing-preimage test was **not** replaced, because successful replacement requires actual exact R5 preimages.

Forward/reverse full composition tests were **not** completed, because doing so would require manufacturing query/witness material.

No current active C1 contract/oracle file was changed. R2/R3/R4 history was untouched.

## What remains valid

- public producer → banked adapter → public consumer code path is still banked;
- AT07 producer arithmetic remains 54/60 forward and 54/62 reverse;
- evidence projection schema remains unchanged;
- forward/reverse frozen evidence hashes remain unchanged;
- no supplied/prebuilt final slice was introduced.

## Required next correction

HQ must choose between two honest paths:

1. **Normative completion:** explicitly freeze the intended missing caller-defined query/binding/witness inputs now, then compute new exact query/witness/evidence identities and supersede any hashes that change; or
2. **Historical evidence recovery:** supply an already-existing accepted artifact that contains the exact historical canonical materials. Merely supplying the four digest strings again is insufficient.

C1-02 was not started.
