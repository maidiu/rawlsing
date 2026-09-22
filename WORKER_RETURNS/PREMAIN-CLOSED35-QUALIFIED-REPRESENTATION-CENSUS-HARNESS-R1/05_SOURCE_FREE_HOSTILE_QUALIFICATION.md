# Source-Free Hostile Qualification

Qualified code head: `11704fbfa16797fbdd55dadc7929aaad729c9454`

Status: **GREEN**

This qualification is source-free. It opened no CLOSED35 raw survey source and did not invoke candidates, measured P2X, P3, or architecture selection.

## Frozen material

| material | exact blob |
|---|---|
| census harness | `b667f7198349486cec32d8168ddc2de1ed0427a8` |
| hostile tests | `bc54bd3ef0f8e7537f448593f77d2c5ca1336a10` |
| 35-source registry | `1b15ce03e337d156c9b9da6d3d60a7a8d1b23591` |
| 38-surface registry | `f3c2c1915c4f3bf379e5233ce9dc4137a841f9e8` |

The frozen test module contains **32 hostile test functions**.

## Commission qualification matrix

1. **35 registry entries:** PASS — ordered source IDs 01..35; 31 SAV + 4 DTA.
2. **Canonical SHA validity:** PASS — all 35 lower-case SHA-256 fields validated and source/surface joins agree exactly.
3. **Decoder/config lanes:** PASS — all 35 resolve to SAV/DTA readers; no `auto`, `guess`, or fallback lane; declared BIG-5/WINDOWS-1252 gaps remain explicit.
4. **Governed-surface authority:** PASS — 38 surfaces resolve; Section85 enumeration is exhaustive at 26/26; LiTS-I, WVS7, Afro R5/R9 and historical Arab W2/W5 authority blob pins resolve exactly.
5. **Output schemas:** PASS — per-source and all six aggregate schema/validator paths are frozen; deterministic aggregate rewrite is hostile-tested.
6. **Classification reachability:** PASS — all six required enums are present and hostile-tested.
7. **Exact R5 codec lanes:** PASS — current codec blob is pinned and hostile surfaces exercise typed token production.
8. **int/float/Decimal noncollapse:** PASS — frozen hostile tests require int ≠ float ≠ Decimal and preserve Decimal exponent identity.
9. **missing-state/declaration noncollapse:** PASS — physical binding keys include exact R5 raw token, physical state, and exact source declaration; hostile tests cover state/declaration changes.
10. **historical dependency-origin audit:** PASS — current successor and historical LiTS key-producing blobs were recovered exactly; ambient-current origin is rejected.
11. **source-local failure continuity:** PASS — harness persists a BLOCKED source receipt and continues to later sources unless the failure is global integrity.
12. **deterministic rerun/resume:** PASS — identical immutable receipts resume without re-observation; input drift fails globally.
13. **no Candidate A/B/C path:** PASS — exact-head import/runner audit finds no candidate execution import or dispatch.
14. **no measured P2X path:** PASS — exact-head import/runner audit finds no measured-P2X execution import or dispatch.

## Exact dependency recovery

Current successor pins:

- R5 codec `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`;
- typed physical binding `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- physical decoder `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`;
- WVS7 representation authority `220c646df5b85eb927af70961c5d05be97edfb73`.

LiTS historical pins at `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`:

- legacy facade `7c509c2098d0030f253344eb3f682471378812a8`;
- canonicalize/semantic-hash dependency `a61365b994e5c3c50de0f598fcf40e90abf757b6`;
- physical-missing-state dependency `13aa733b511dc23e00bfcdf288c5b920e3f09983`.

## Qualification execution note

The preparation environment could not DNS-resolve github.com for a direct git checkout, so this turn did not invoke `pytest` from a cloned worktree. Instead, qualification was performed against the exact committed blobs through GitHub reads plus independent source-free hostile assertions reproducing the registry, authority, dependency, execution-boundary, and determinism obligations above.

This limitation does **not** weaken the authoritative runtime gate and does not authorize source observation in the preparation cloud.

## Holding

`SOURCE_FREE_HOSTILE_QUALIFICATION_GREEN__QUALIFIED_CODE_HEAD_11704fbfa16797fbdd55dadc7929aaad729c9454`
