# R38 WG0RI — Phase A prefreeze (before candidate-dependent execution)

**Role:** fresh independent I2 source-free custody reviewer, not WG0R/WG0I author,
Pyat HQ, source-semantic issuer or original E_pre issuer.

**Branch:** `agent/reviewer-pyat-r38-wg0ri-exact-disposition-repair-r1`
**Sealed base:** `68873526efe5a39a0849aa401666ac997870f156`
**Author target:** `86c13ea6cea813fa2f87dca92396646305e3742c`
**Prior independent WG0I:** `44eac9021db23267448a6fc151e6bbe8374a868f`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/wg0ri`

## Artifact expectations (fixed before running the author court)

| Artifact | Expected |
|---|---|
| Original frozen disposition payload | 18,276 bytes, SHA-256 `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98` |
| Exact P2 identity master | 18,276 unique implementations, SHA-256 `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6` |
| Original Git preimage | commit `b44596d880425f6984f208bfa14daee2f15d3f90`, blob `c93945d158198871f5cc6692a6bed25aeef44028`, 24,972 bytes, SHA-256 `c1d5a9a9b2905f7ed783a21f43eeef91bc173d6e5e077751a67f7025408ee7ad` |
| Original malformed decoded payload | 18,387 bytes, SHA-256 `3bee6f0ec5cae74c112f2896b517b23ab7e880c9400bf019d1df6d0b3157edee`, 2,114 reserved-bit violations (WG0I RED; to be re-verified and preserved) |
| Surviving shard | original Git blob `3a9b5bde2fc479c6fc10280561fe715686e39dd4`, 1,000 rows + header, 11,944 bytes, SHA-256 `e9fff20e06fabbd90fff6552f73811e93caeb8c0d998cb96add5d472d8892a67` |
| Shard manifest | 19 shards, 18,276 rows; part-000 listed SHA-256 `e2f5f13ade61…` differs from the surviving Git shard `e9fff20e…`; the manifest cannot be assumed to be the survivor's manifest and must be typed, not used as a substitute |
| Repaired carrier | `sources/recovered_disposition/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv`, one `P2_ORDINAL_BYTEPACK_V1` row, declared 18,276 bytes / `64a43ba2…`, code map `0=SEM;1=TOP;2=POS;3=END;4=CTX;5=SCX;6=ADM;7=REJ;8=CPC;9=BLK`, bits0-3 use / bit4 hard_fail / bit5 route_predicate_required / bits6-7 zero |
| Recovery inputs | S00 `d0fc960f…`, O06 `91379e9a…`, O07 `4b9b4a54…`, O08/O09 `2daebfe1…`, O04 `8da69f98…` projection SHAs as declared in custody; archive/member provenance retained |
| O07 boundary | diagnostic candidate projection only; it may not issue use/disposition meanings; any change to its non-diagnostic fields must leave the recovered payload unchanged; any change to its diagnostic held input must change only held bits and must fail the frozen payload SHA unless every other accepted input matches |
| Original historical malformed artifact | preserved unchanged, still fails the repaired reader closed; the repaired carrier is a separate versioned path |
| Author 90-test court | 90 passed / 0 failed / 0 error / 0 skip natively and in the relocated cold court; two fresh processes produce identical payload/receipt identity |

## Frozen evidence-chain checks

1. The original Git preimage blob is exactly `c93945d1…`; its Git publication
   commit is `b44596d8…`; it is not silently repaired or replaced.
2. The surviving shard is exactly the original Git blob `3a9b5bde…`; each of its
   1,000 rows decodes to the corresponding recovered payload byte (ordinal,
   use code, hard_fail, route flag).
3. The recovered payload is a single 18,276-byte ordinal bytepack with zero
   reserved bits; every byte's use code is in the frozen code map.
4. The repaired reader binds the payload to the exact P2 master, declared byte
   length, hash, format, code map and packed-byte legal range; a corrupt copy
   fails closed.
5. The accounting output has 18,276 rows, 35 waves, 9 families; no row carries
   `DISPOSITION_CARRIER_REQUIRES_EXACT_REPUBLICATION`; governed use/hard-fail/
   route flags are all non-null; the 76 P10/G1A held accounting states remain 76
   within the 65,354-unit census.
6. The recovered carrier does **not** become a source/operation permission: the
   full original35 eligible item/operation frontier remains HOLD. WG0I's
   P2/O35E crosswalk concern (18,276 vs 18,259; 26 P2-only hashes; 9 O35E
   blocked-identity rows; 17 net delta; 19 measurement candidates) and the full
   frontier HOLD are preserved.

## Frozen independent hostile cases

Byte/hash corruption; P2 identity substitution; ordinal duplication, omission
and reordering; reserved-bit violations; disposition code-map change; dropped or
silently converted holds; forged historical provenance; false reconstruction
from aggregate counts; mismatched surviving shard/manifest; replay nonidentity;
and a correctly preserved historical malformed artifact failing closed. Each
must produce a typed refusal or a detectable mismatch, never a silently accepted
new disposition meaning.

## Chronology statement

This prefreeze was written from the launch, the original Git preimage/survivor,
the exact P2 identity hash and the prior WG0I return, before executing the
author's `recover_disposition_payload.py`, `account_current35.py` or 90-test
court. The author's claimed class/hard-fail/route counts are not imported as
oracle; they are recomputed from the recovered payload and cross-checked against
the independent shard/custody evidence.
