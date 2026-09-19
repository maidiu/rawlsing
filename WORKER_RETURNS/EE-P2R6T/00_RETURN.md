# EE-P2R6T — governed return

## Disposition

PASS.

`EE_P2R6T_PASS__LITS_AS2A_PINNED_AUTHORITY_PATH_REF_REPAIRED__EXACT_BANKED_AUTHORITY_BYTES_PRESERVED__READY_FOR_HQ_SELECTIVE_BACKEND_FANIN_AND_P2X_RESUME`

## HQ authority

Live HQ resolved first to checkpoint `20260919T0132-0400` at immutable handoff `9aa2cd5053e88f1b3bc7b25e20793e80702a54b1`.

Controlling decisions:

- `HQD-2026-09-19-077`
- `HQD-2026-09-19-078`

P2X remained held at `LITS_I/A/S02_C11_REACHABILITY` throughout this commission.

## Exact production repair

Only the permitted production source was changed:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

The exact semantic change is:

`LITS_AS2A: AS2A_LITS1_SHARED_CERTIFICATION_20260827 -> banked_as2a`

Prior backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

Repaired backend blob:

`fb30167ebc060939e17eb15c71b93c000033eb4f`

The backend contract remains:

`RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0`

The pinned authority commit remains:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

No fallback, fuzzy, latest, or alternate authority lookup was introduced.

## Exact pinned authority resolved

Ledger:

- Git blob: `c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`
- SHA-256: `65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`

Package:

- Git blob: `174b931e8aa89111086e3d46159b47154bed7f16`
- projection-material semantic hash: `9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`

Builder:

- Git blob: `c51b56779ab9d79126619b7733d41f5253c8150f`
- exact `read_banked_authority()` function accepted the deployed exact ledger/package bytes.

LiTS source identity remained:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

No Library or source-carrier bytes were accessed.

## Hostile court

All exact hostile cases failed closed:

1. missing exact `banked_as2a` path -> `CourtAuthorityStop: immutable path unavailable`;
2. substituted ledger bytes -> `RuntimeError: Part-A slot ledger SHA mismatch`;
3. substituted package projection material -> `RuntimeError: Part-A projection authority content hash mismatch`.

The 17-stage production dispatch set and handler coverage remain unchanged.

## Browser qualification

Governed Browser court:

- PR: `#415` (transient, unmerged)
- semantic candidate: `5bacfb54e8968ee3a8867b3111d6771068a76855`
- execution head: `14f6fcb980c861d8520551392eae750856798486`
- run: `35424699308`
- job: `105848513942`
- bounded tests: **6 passed**
- protocol self-tests: **20 passed**
- artifact: `10579135204`
- artifact name: `rabochii-court-receipt-35424699308`
- artifact digest: `sha256:3a4dce583165ae90ee18002da1ada4e513b4d9e4de25173fc22995c1b0b5f00c`

No measured P2X court execution, empirical outcomes, performance measurements, or source carriers were touched.

The transient `.rabochii/court_spec.json` was absent at the commissioned head, present only for the governed Browser court, and restored to absence at commit `93e3856c6a54768cf93311f5539348292db6f3b1`.

## Wake

Wake exactly:

`HQ_REPAIRED_BACKEND_ADJUDICATION_ONLY__SELECTIVELY_FAN_IN_BACKEND_BLOB_fb30167ebc060939e17eb15c71b93c000033eb4f_TO_EXISTING_P2X__SEAL_RESUME_AUTHORITY__THEN_WAKE_P2X_AT_LITS_I_A_S02_C11_REACHABILITY`

P2X must not resume before HQ adoption and selective backend fan-in.

Return to HQ.
