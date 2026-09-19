# EE-P2R6T COMMISSION — 2026-09-19

Status: `R6T_BROWSER_LITS_AS2A_PATH_REF_REPAIR_ACTIVE__P2X_HELD_AT_S02`

Decision:

`HQD-2026-09-19-078`

HQ commissions:

- id: `EE-P2R6T`
- branch: `agent/rabochii-prev3-ee-p2r6t-lits-as2a-path-ref-repair-r1`
- exact base: `d0187a01f21959f4834a7f774f92d06187f1efb3`
- commission tip: `f325ef8b6502e38d1a811a5da2ae4dcfb357a3b7`
- execution surface: `BROWSER`
- Library access: `NO`
- grain: `EXACT_LITS_AS2A_PINNED_AUTHORITY_PATH_REF_REPAIR_ONLY`

The worker must repair only the production backend's exact pinned AS2A path reference from the non-existent canonical-name directory to the existing `banked_as2a` directory at the unchanged pinned commit `3ce639e1...`.

The exact authority bytes are immutable:

- ledger blob `c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`
- package blob `174b931e8aa89111086e3d46159b47154bed7f16`

No semantic authority change, source/carrier access, measured execution, fallback lookup, backend redesign or P2X movement is authorized.

PASS terminal:

`EE_P2R6T_PASS__LITS_AS2A_PINNED_AUTHORITY_PATH_REF_REPAIRED__EXACT_BANKED_AUTHORITY_BYTES_PRESERVED__READY_FOR_HQ_SELECTIVE_BACKEND_FANIN_AND_P2X_RESUME`

PASS wakes HQ adjudication only.

P2X remains held at `LITS_I/A/S02_C11_REACHABILITY`.
