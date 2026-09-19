# FIABC-B03 — First Common Output Candidates

This note distinguishes an **interface convergence point** from a **full equal-work comparison cut**. They are not the same thing in the current A/B/C design.

## Candidate 1 — validated C11 logical release

Strong evidence supports `C11Repository` + `C11LogicalRelease` as the earliest common logical interface.

### A

`rawlsing_next/pre553_r5_source_backed_adapter.py` reopens the accepted R5 carrier, reconstructs an `ExactPhysicalCellStream`, and then calls:

`build_source_backed_c11_repository(stream, projection, cache=None)`

The adapter explicitly states that it is mechanical and assigns no new semantics.

### B

`rawlsing_next/pre553_source_backed_c11_facade.py` takes exact `PhysicalSourceIncidence` (or an exact physical-cell stream), applies the explicit `GovernedC11Projection`, validates the C11 source release, and returns `C11Repository((release,)), release`.

### C

`rawlsing_next/pre553_route_c_accelerators.py` converts CACC1 back into an exact physical-cell stream, then `build_route_c_repository` calls the same `build_source_backed_c11_repository` facade.

### Why this is a real common point

At this point candidate-specific source transport is hidden behind the same governed logical families and release contract. For LiTS, the accepted A first-build receipt and B cacheless-C11 receipt both bind the same projection cache identity and the same C11 logical release:

- projection: `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`
- C11 logical release: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`

This is the best repository-supported **earliest semantic convergence point**.

### Why it is not sufficient as the full P2 equal-work cut

Candidate C's accepted physical meaning includes CACC2, which is explicitly an I03/I05-side coverage/preflight accelerator. CACC2 is not exhausted merely by reaching C11. Therefore a court stopping at C11 would fail to exercise the full accepted C physical treatment.

The frozen P2 manifest also requires I03, I05/learned empirical production, provenance, warm/cold work, lifecycle/rebuild/invalidation, fresh-process replay, and recovery. A C11-only cut would compare only part of the candidate treatment.

## Candidate 2 — exact I03 query result

All accepted candidate designs are intended to converge on the unchanged exact I03 engine and exact identity-bearing empirical facts.

Route C's own module states that CACC2 is only a coverage/preflight accelerator and that the unmodified exact I03 engine remains the sole semantic oracle.

This is a later and stronger semantic comparison point than C11, but it still does not include the representative I05 workload that is expressly part of the physical-carrier decision.

## Candidate 3 — governed I05 learned empirical product + semantic/replay identity

This is the strongest repository-supported candidate for the **full first common pre-Field-Forge comparison output** because:

1. the final P2 manifest requires actual I05 / learned empirical production as part of every qualifying source×candidate workload;
2. LiTS freezes exact 50-candidate / 77-role learned work and exact product/replay identities;
3. WVS freezes an exact 46-candidate frontier;
4. Route C's accepted CACC2 surface exists specifically on the exact-bounded discovery path, so the candidate treatment is not fully exercised until I05-side work has happened;
5. the deletion law requires B/C to regenerate execution state while reproducing the same governed empirical product, semantic identity, and replay identity.

In current backend terms, S05 stores:

- `product_identity`
- `semantic_identity`
- `replay_identity`
- `exact_output_identity`

These are the closest present implementation objects to the post-treatment logical convergence that the court actually wants to compare.

## Current proof status

The current executable graph cannot establish Candidate 3 across A/B/C:

- LiTS-C stops at `S02_C11_REACHABILITY` because the frozen CACC1 stream omits q310/q311 required by the F02 composite projection.
- WVS-C has no backend execution path.
- `_bind` explicitly composes only A and B.

Therefore:

- `C11LogicalRelease` is **proved as the intended earliest common logical interface** from owner implementations;
- `I05 learned empirical product + semantic/replay identity` is the **best-supported full-court comparison-output candidate**;
- the exact equal-work pre-Field-Forge cut is **not executable/proved across all three candidates in the current graph**.

No repair or new boundary is proposed here.
