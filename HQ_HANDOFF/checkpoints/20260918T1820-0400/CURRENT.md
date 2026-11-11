# RAWLSING HQ CHECKPOINT — 20260918T1820-0400

Status: `R6I_CANDIDATE_QUARANTINED__ZERO_ACTIVE_BINDINGS__R6B_TO_R6A_BINDING_ALIGNMENT_READY__AB_DORMANT__P2X_HELD`

Semantic PRE-MAIN:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

Controlling decision:

- `HQD-2026-09-18-058` — supersede the active-runtime effect of HQD-057 because R6I candidate identity_material does not satisfy the exact R5A/R6A production binding contract.

Correction record:

`HQ_HANDOFF/EE_P2R6I_RUNTIME_COMPATIBILITY_CORRECTION_20260918.md`

## R6I status

R6I return remains governed PASS evidence at:

`f1941fc7e9291a17860475dc14edc9ef1bc32eff`

R6B candidate:

`fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0`

Disposition:

`QUARANTINED__R6B_INTERNAL_PASS__NOT_R5A_R6A_RUNTIME_CONSUMABLE`

It must not be supplied to R6A as `ACTIVE_POSITIVE`.

## Exact defect

R6A production runtime blob:

`2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`

requires exact R5A `future_binding_required_fields` inside active binding `identity_material`.

R6I places only 4/17 required fields there under the exact required names.

The remaining required facts are elsewhere in the envelope and/or differently shaped.

This is a producer/consumer contract mismatch.

## Current binding registry

Current corrective registry snapshot:

`HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T1820-0400.json`

Snapshot hash:

`209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56`

Active positive binding count:

`0`

The R6I candidate is recorded as quarantined evidence.

Historical snapshots remain immutable.

## Next lawful work

`R6B_TO_R6A_ACTIVE_BINDING_CONTRACT_ALIGNMENT_AND_REISSUANCE`

The successor must:

- preserve R5A/R4A/R6L semantics;
- construct binding identity_material in the exact R5A/R6A shape;
- derive a new deterministic binding identity;
- verify the proposed active record directly through exact R6A production runtime;
- remain inactive pending HQ adoption.

## Wake graph

A/B owner-seam requalification: `DORMANT`

Backend fan-in: `DORMANT`

P2X: `HELD`

Terminal:

`ZERO_ACTIVE_BINDINGS__R6J_READY__AB_DORMANT__P2X_HELD`
