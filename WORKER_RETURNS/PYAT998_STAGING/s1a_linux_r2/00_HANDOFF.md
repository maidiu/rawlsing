# PYAT998 — S1-A incorporation and Linux S2-B compatibility

## Status

**`S1A_INCORPORATED__LINUX_S2B_COMPAT_PASS__OWNER_ACK_AND_PHASE2_HOLDS`**

Same staging branch, same worktree, parent return
`a9407f08f7e0efed32b4dba7f654b3906cbfb18a`. Integration remains **UNMERGED**. No
joined S01–S05, no independent G5, no production CURRENT, no original35 and no
protected merge is claimed.

## S1-A

Accepted review: `c900cf463694a8b21af7f3f8bd8da6a6b23d1d82`
(`ACCEPT_SCOPED@S1A_SOURCEFREE_SEMANTIC_CACHE`), candidate
`6286ea700a253ff142104f2e3ee62c9352a07644`.

Exact accepted blobs added:

| Path | Accept blob | Current staged blob |
|---|---|---|
| `pre553_source_backed_c11_facade.py` | `f29247b3…` | `f29247b3…` |
| `test_c1_agent_b_cache_differential.py` | `d9494634…` | `d9494634…` |
| `pyat-c1-agent-b-cache-proof.yml` | `f740e6a1…` | `f740e6a1…` |

Supplement: `provenance_supplement.json` (3 entries; total staged files 39).
The parent 36-file manifest and all prior return files were preserved.

S1-A semantic cache key, race guards and existing source-backed/native behavior
are retained.

## Compatibility results on this composed cut

| Suite | Actual |
|---|---|
| S1-A focused 34 | **34 passed in 3.21s** |
| S1-A preservation 136 | **136 passed in 105.79s** |
| World-binding literal 18 | **18 passed in 275.24s** |
| S2-C | **31 passed in 5.73s** |
| S2-D | **31 passed in 14.08s** |
| S2-E | **22 passed in 20.86s** |
| Imports after S1-A | **PASS** |
| S2-B Linux direct/external/semantic | **81 passed in 37.99s** |

The 32 Darwin `/proc` failures are closed on Linux, not waived:

- existing `limactl` **s2b** Running, vz/x86_64, 2 CPU, 4 GiB;
- existing venv `/Users/matthewsmith/s2b-work/rawlsing-s2b-r5-local/.venv`;
- unique proofcopy `/Users/matthewsmith/s2b-work/pyat998-s1a-linux-r2-20261113T154623`;
- guest had no active pytest/rawlsing process before the run;
- host/guest SHA-256 and git blobs matched for the tested files;
- no VM/provider/runner/harness change, no other worker scratch, no skip or
  `/proc` fallback.

This is current composed-cut compatibility, not a rerun of the prior S2-B G5.

## Frozen owner handoff — S2-E method

`rawlsing_next/pre553_issued_workload.py`:
`NativeWorkloadResult.exact_s2e_output_census`

- current blob `5879c2b6690deb01c9442061bca9d9691988281f`
- S2-D source blob `b02810677ae66231e5e59b09aefe9bd63a31aaa3`
- S2-E method source blob `6356d6639a5af65b9e4e7f86f4e3b495905e9d2c`
- exact minimal 15-line delta: `evidence/s2e_method_delta.patch`
- owner session `ses_e3120ba7affeNBHUoX1HIP3G4r`
- **owner ACK not claimed; file frozen; no new edit**

Prior ancestry is not treated as owner permission.

## S2-A remains a real REVISE

`VerifiedDirectEstate.select_events` still undercounts the poisoned target
locator in the accepted review. No S2-C edit, no adapter and no local
authorization is made. See `s2a_hold.json`.

## Holds

- S2-E method owner ACK: **PENDING**.
- #997 source-to-saved/fate bridge: **EXTERNAL HOLD**.
- S2-A owner decision and G5: **PENDING**.
- Joined vertical: **HOLD_DEPENDENCY_997_S2A_OWNER_ACK**.
- 1001 full 100k/6 GiB: **NOT_RUN**; prior prep remains author-prepared only.
- Protected merge / production CURRENT / original35: **NONE**.

## Self-critique

- S1-A is incorporated source, but this author cannot accept the integrated
  packet.
- Linux compatibility is scoped to the named S2-B suites on the proofcopy.
- The S2-E method composition is still unaccepted pending owner ACK.
- S2-A and #997 are real external blockers; no green is fabricated.
- No heavy benchmark or full 202 court was run.
