# RAWLSING HQ CURRENT

Checkpoint: `20260916T2201-0400`
Prior sealed checkpoint: `20260916T2049-0400`
Semantic PRE-MAIN: `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## Material transition

R8 partial fan-in is adopted without imposing an all-lanes barrier. EE-R8A and ASTRA-D11 have returned. ASTRA-FF01 remains active and is not superseded or fan-in adopted before its governed return exists.

### EE-R8A — adopted exact blocker

- return tip: `4ff8f012f4b09ab488cdb59e6f0f62db6db8c4ca`;
- final package remains `18/18 READY`, zero pending, and A/B/C physical readiness remains `27/27`;
- exact `pyreadstat==1.3.6` and `pyarrow==25.0.1` were co-located on Darwin x86_64;
- exact WVS7 and LiTS-I sources both decoded successfully in real child processes with exit code 0;
- no candidate was executed because the unchanged qualified W4 harness returns required `peak_rss_bytes=null` on Darwin;
- proved cause is only W4 `rusage_metrics`: Linux `ru_maxrss` is normalized from KiB to bytes, while every non-Linux platform is emitted as `platform_native` and leaves `peak_rss_bytes=null`;
- this is a common execution-surface portability defect, not a candidate, semantic, routing, owner, workload, lifecycle, or architecture failure.

### EE-R8B — active local-machine Codex successor

Exact commission authority: `6cdd1015ac1ac889c5133cd8b0db559e5709e6f9`.

Branch: `agent/rabochii-prev3-ee-r8b-darwin-rss-normalization-final-bakeoff-r1`.

R8B may repair only the `rusage_metrics` platform-unit normalization so that the already-required `peak_rss_bytes` metric is represented in bytes on Darwin while preserving Linux behavior and fail-closed unknown-platform behavior. It must independently qualify that portability seam and, in the same commission, run the complete already-ready final A/B/C bakeoff. No repair-only interstitial round is authorized.

R8B is explicitly suitable for local-machine Codex and should reuse the exact functioning Darwin runtime/source layout proved by R8A where available.

### ASTRA-D11 — PASS adopted

- return tip: `a89b7ebd608742a87557395e2359291a32b62302`;
- exact qualified M10-M01 rule is selected `CURRENT_ACCEPTED` at rule-currentness grain;
- exact current-selection evidence and disposition are bound;
- no application/world fact, realization, witness, topology, encounter, person, or V3 state is created;
- SDTF remains noncritical to the empirical/structural research path.

### ASTRA-FF01 — still active

FF01 remains the active D04 learned-product -> Field Forge ingress/structural-use worker. HQ does not interpret intermediate branch movement as a governed return. Its result will be fan-in reconciled when the commissioned return is complete.

## Broad-view project law

Research remains:

`source/data grounding + semantic authority -> Trii empirical production -> Field Forge structural inference -> Dva temporal/pressure-world synthesis -> sociologically processed PRE-V3 artifacts -> V3`.

Carrier benchmarking is orthogonal physical realization. The FF01 research lane does not wait for R8B, and R8B does not wait for FF01.

## Current priorities

1. finish the final A/B/C comparison locally through the narrowly authorized Darwin RSS normalization;
2. let FF01 complete actual empirical-to-structural progression without interference;
3. bank D11 rule-currentness closure; do not spawn gratuitous SDTF work merely because a successor may exist;
4. no broad architecture review;
5. no all-lanes barrier;
6. local execution defects remain local.
