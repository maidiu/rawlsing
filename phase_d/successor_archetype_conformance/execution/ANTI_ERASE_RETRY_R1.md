# Phase-D successor anti-erase retry R1

## Purpose

Repair only the response-option input gap exposed by the blocked successor run, then rerun the frozen anti-erase ladder. The blocked run at commit `cb0445eacb9b27b7a2628b4241887d93d58d7373` remains immutable ancestry.

## Frozen inputs

- Candidate-order SHA-256: `5ae32c7cdfd68d3e0c1816abd85fc6f77387f65a383e5b860d2ab9cf814235b2`
- Encoded projection SHA-256: `650ea4da5c687f692f8abae51094e312de2f7add2e31cc204e41b54e82620d97`
- Materialized projection CSV SHA-256: `d9bcc4e9cf80c6e70fdf38d7fd260c5b60f4f8a4696fbea0c8e6d4fbff5ee1f7`
- Projection shape: 69 data rows covering 12 frozen variables.

Read `../authority/RESPONSE_SEMANTICS_PROJECTION_PROVENANCE_R1.md` before execution.

## Preflight

1. Verify the frozen candidate-order SHA unchanged.
2. Verify the encoded sidecar SHA.
3. Materialize the sidecar with the local Python standard library into a temporary CSV.
4. Verify the materialized CSV SHA and exact 69-row shape before any database access.
5. Confirm that the projection is used as an additive, bounded response-option input for the frozen anti-erase slices only. Do not modify the canonical response-option authority in place.
6. If the local V550 loader cannot consume the projected rows without changing semantic meaning, routing truth, validator semantics, or architecture, stop and report the exact interface mismatch.

## Empirical retry

- Reuse the same governed local respondent substrate and the same V550/V550J execution law as the first successor run.
- Execute only the anti-erase ladder, in exact frozen rank order.
- Stop at the first lawful anti-erase instantiation or after rank 11 is lawfully exhausted.
- Do not reorder, replace, add, or delete candidates.
- Do not infer response labels from respondent values.
- Do not promote empirical co-travel into typed semantic authority.
- Do not begin V552, V552J, V553+, or the 35-wave rebuild.

The already-instantiated GSS local-block archetype from the blocked run is carried forward as immutable evidence and is not re-executed.

## Return construction

Create a fresh successor return descended from the blocked return:

- preserve the frozen ladder and M6 ancestry;
- carry forward the prior local-block instantiated row without changing its semantic or routing claims;
- replace the prior anti-erase NOT_INSTANTIATED execution rows with the new bounded retry rows;
- write a fresh no-outcome-selection attestation and privacy scan for this retry;
- package only aggregate/governed artifacts, never respondent-level rows or direct identifiers.

Run the existing successor validator unchanged:

`phase_d/successor_archetype_conformance/validation/validate_phase_d_successor_archetype_return.py`

Valid terminals remain exactly:

- `PHASE_D_GATE_CLOSED`
- `BLOCKED_SUCCESSOR_ARCHETYPE_CONFORMANCE`

If the gate closes, stop. Do not begin V552 in the local execution worker.
