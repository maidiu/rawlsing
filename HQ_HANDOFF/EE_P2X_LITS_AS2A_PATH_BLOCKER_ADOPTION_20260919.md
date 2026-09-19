# EE-P2X COMMON-COURT AUTHORITY BLOCKER ADOPTION — 2026-09-19

Status: `P2X_COMMON_COURT_BLOCKER_ADOPTED__EXACT_LITS_AS2A_PATH_REF_REPAIR_AWAKE__P2X_HELD_AT_S02`

Decision:

`HQD-2026-09-19-077`

Semantic PRE-MAIN remains:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## Governed P2X return

P2X return head:

`d0187a01f21959f4834a7f774f92d06187f1efb3`

Terminal:

`EE_P2X_LITS_I_A_S02_C11_REACHABILITY__COMMON_COURT_AUTHORITY_FAILURE`

This return is adopted as an exact common-court authority blocker.

The branch remains the existing P2X execution branch and must resume from the same reducer stage after repair.

No candidate measurement, WVS execution, ranking, synthesis, source substitution, backend redesign or semantic fallback occurred.

## Exact blocker

The qualified backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

pins:

`LITS_BANKED_COMMIT = 3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

and currently requests:

`.../AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv`

plus the sibling authority package.

At the pinned commit, that directory name does not exist.

The exact accepted authority exists instead under:

`.../AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a/`

with:

- ledger Git blob:
  `c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`
- package Git blob:
  `174b931e8aa89111086e3d46159b47154bed7f16`

These are the same exact Git blobs later vendored under:

`WORKER_RETURNS/EE-P2R6K/SUPPORT/R5B/SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/`

Therefore the blocker is classified:

`EXACT_AUTHORITY_PATH_REF_MISMATCH__NO_AUTHORITY_CONTENT_CHANGE_REQUIRED`

This is not a new authority issuance and does not authorize changing the underlying ledger/package bytes.

## Required repair

Repair only the backend's pinned AS2A repository path reference so it resolves the exact accepted `banked_as2a` files at commit `3ce639e1...`.

The repair must preserve:

- pinned commit `3ce639e1...`;
- ledger blob `c24e0d6a...`;
- package blob `174b931e...`;
- Part-A projection authority content hash `9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`;
- slot ledger SHA-256 `65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`;
- all current R6S/R6O runtime authority.

No path fallback, fuzzy search, latest lookup or alternative authority content is authorized.

## Wake

Wake:

`EE_P2R6T_EXACT_LITS_AS2A_BACKEND_PATH_REF_REPAIR`

P2X remains held at:

`LITS_I/A/S02_C11_REACHABILITY`

until the repaired backend is Browser-qualified, selectively fanned into the same P2X branch, and HQ seals resume authority.

Terminal:

`P2X_BLOCK_ADOPTED__R6T_PATH_REF_REPAIR_AWAKE__P2X_HELD_AT_S02`
