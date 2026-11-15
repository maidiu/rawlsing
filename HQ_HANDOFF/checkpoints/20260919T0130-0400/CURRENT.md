# RAWLSING HQ CHECKPOINT — 20260919T0130-0400

Status: `P2X_BLOCK_ADOPTED__R6T_PATH_REF_REPAIR_READY__P2X_HELD_AT_LITS_A_S02`

Semantic PRE-MAIN:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

Controlling decision:

- `HQD-2026-09-19-077` — adopt exact P2X LiTS AS2A pinned-authority path-ref blocker.

Adoption record:

`HQ_HANDOFF/EE_P2X_LITS_AS2A_PATH_BLOCKER_ADOPTION_20260919.md`

## Governed P2X stop

P2X branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Current stopped head:

`d0187a01f21959f4834a7f774f92d06187f1efb3`

Terminal:

`EE_P2X_LITS_I_A_S02_C11_REACHABILITY__COMMON_COURT_AUTHORITY_FAILURE`

Resume stage after repair:

`LITS_I/A/S02_C11_REACHABILITY`

No candidate measurement or WVS execution occurred.

## Exact blocker classification

Backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

Pinned authority commit:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

Backend requested missing canonical-name directory:

`AS2A_LITS1_SHARED_CERTIFICATION_20260827`

Pinned commit contains exact accepted authority under:

`banked_as2a`

with exact blobs:

- ledger `c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`
- package `174b931e8aa89111086e3d46159b47154bed7f16`

These exact blobs are later vendored under the canonical-name directory.

Classification:

`EXACT_AUTHORITY_PATH_REF_MISMATCH__NO_AUTHORITY_CONTENT_CHANGE_REQUIRED`

## Wake

EE-P2R6T exact backend path-ref repair is ready to commission.

P2X remains held until R6T PASS is adopted and the repaired backend is selectively fanned into the same P2X branch.

Terminal:

`R6T_READY__P2X_HELD_AT_LITS_A_S02`
