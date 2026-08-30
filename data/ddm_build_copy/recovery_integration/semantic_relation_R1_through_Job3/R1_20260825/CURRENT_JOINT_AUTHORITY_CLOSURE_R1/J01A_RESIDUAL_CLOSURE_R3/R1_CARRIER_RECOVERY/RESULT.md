# J01-A R3 — FROZEN R1 CURRENT-CARRIER BYTE RECOVERY

## Terminal status

`BLOCKED__EXACT_FROZEN_R1_CARRIER_BYTES_NOT_RECOVERABLE_FROM_AUTHORIZED_VISIBLE_STORAGE_PATHS`

This byte-identity/transport court exhausted the authorized visible recovery paths for the two frozen J01-A R1 current-only carriers and did **not** recover either carrier byte-for-byte.

## Frozen authority

Git authority: J01-A R1 commit `085dcb9d7d92d427038b634c55b8b4f3ce5235da`, `CARRIER_MANIFEST.json`.

- `CURRENT_SOURCE_STRUCTURE_UNIVERSE.csv`: 299 rows; 253,503 bytes; SHA-256 `47913a300402b65e4fd92197220ced0195b6b50704679e3cc088d15604d4b7ad`; frozen Library ID `libfile_f4d6104cdc64819184fed7938f603239`; frozen backing ID `file_00000000f50881f7b9569c40882e37b9`.
- `CURRENT_J_CANDIDATE_UNIVERSE.csv`: 257 rows; 216,925 bytes; SHA-256 `3fe61d274c4b0d78c9b1ba142709125831a4c7d8e3418e0a69fc257879b743f9`; frozen Library ID `libfile_9338d56ded208191ae1583a5f0de9977`; frozen backing ID `file_00000000050481f79dcbc99e80c39912`.

## Executed recovery findings

1. Direct materialization and direct read by both frozen backing IDs fail because those backing objects are not currently visible to the Files/Library surface.
2. The frozen stable Library IDs still resolve, but they now point to different backing objects and different bytes:
   - source alias -> `file_000000009dc881f79b5040c56f61e6d3`, 394,454 bytes, 439 data rows, SHA-256 `de4a097b1059be2c398ed0eef5876f308a37e38c0fc315d936b42213d1ba8ba7`;
   - candidate alias -> `file_00000000ddec81f79f81bf65c27cbe04`, 288,879 bytes, 328 data rows, SHA-256 `329840cc555b791c1cebca8328a317009d5ce201c4b60e72edec1900923ac550`.
   Both are rejected by frozen byte/hash/row-count identity.
3. Version probes `0` and `1` on both stable Library IDs materialize the same current mutated bytes; neither exposes the frozen bytes.
4. Exact Library searches by frozen hash, frozen backing ID, stable Library ID, filename, path, and expected byte count found no exact immutable duplicate.
5. A complete Library namespace listing for the exact R1 bind interval 2026-08-29 20:30Z–20:50Z found no visible file objects of any type. A complete Aug. 29 current-day CSV listing likewise contained no carrier at either frozen byte size.
6. The original R1 Git branch remains exactly at `085dcb9d7d92d427038b634c55b8b4f3ce5235da`. Its transport record explicitly says the exact carriers were stored in ChatGPT Library and only a hash manifest was Git-tracked; the carrier bytes themselves are absent from Git.
7. Git branch/search inspection found no J01-A R1 temporary carrier/transport branch or hash-matching Git copy.

## Constitutional disposition

No semantic row was reconstructed, inferred, repaired, or copied from any later carrier. No historical J inventory was consumed. Content inspection was limited to transport metadata, raw byte hashes/sizes, and CSV record counts needed to reject nonmatching aliases.

Because neither frozen carrier was recovered exactly, no new immutable Library copy was created and the success token `J01A_R3_FROZEN_R1_CARRIER_BYTES_RECOVERED_PASS` is **not emitted**.

## Required SUB-VOZHD action

The remaining blocker is storage-layer recovery, not semantic adjudication. Recovery requires either direct restoration/version-history access to frozen backing objects `file_00000000f50881f7b9569c40882e37b9` and `file_00000000050481f79dcbc99e80c39912`, or another immutable copy that independently matches the frozen hash + byte + row-count identities. Do not regenerate the R1 semantic carriers from later work to satisfy this court.
