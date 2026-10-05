# EE-P2R6V — governed return

## Disposition

PASS.

`EE_P2R6V_PASS__WVS7_PROJECTION_MATERIALIZER_BINDER_RECURSION_REPAIRED__EXACT_R6S_AUTHORITY_IDENTITIES_PRESERVED__READY_FOR_HQ_SELECTIVE_FANIN`

## HQ authority

Live HQ resolved first to checkpoint `20260919T0330-0400` at immutable handoff `9540aba11d40fc749ffa59827e871c1ba00e7ec6`.

The checkpoint and manifest were verified:
- `CURRENT.md` blob `16169e29b9497b8bf9d9f3af09f2de61b72e3ff0`;
- `CURRENT.json` blob `a29c37146dc12b9c126561e956ea3bbe7395c89f`.

Controlling decisions:
- `HQD-2026-09-19-081`
- `HQD-2026-09-19-082`

P2X remained held at `ae8b1db9d8c3288e002950ac01123c70f3138320` throughout this commission.

## Exact production repair

Only the commissioned production file changed:

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

Prior blob:
`3a3e228843656e023673310c26acbd41ecdc1b3b`

Repaired blob:
`11b28416aac5a4899706150721f2f8ac8bb6ee43`

Production candidate commit:
`a500440ee904af98a14df72d1f1cb5a4b9f02728`

The exact production diff is two lines:
1. import accepted P2R1 `bind_governed_c11_projection` as `_bind_governed_c11_projection`;
2. preserve public `bind_exact_projection_fields` and replace its recursive self-call with exactly one call to the imported alias.

No WVS semantic authority, projection authority, country-coordinate law, Lock2 identity, routing law, or backend code changed.

## Frozen R6S identities

Qualified unchanged:
- projection identity: `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`;
- coordinate slot identity: `4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6`;
- coordinate authority: `9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d`;
- P2F2 / Lock2 tie-order identity: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`.

The qualification additionally proves the local public wrapper still performs every frozen guard before delegation.

## Hostile negatives

Six exact mutation / authority-substitution cases fail closed before the imported binder can be reached:
1. coordinate name substitution;
2. coordinate authority substitution;
3. projection authority substitution;
4. replay authority substitution;
5. Lock2 / tie-order substitution;
6. non-empty weight-slot substitution.

## Browser qualification

Governed Browser court:
- PR: `#416` (draft, unmerged);
- semantic candidate: `a500440ee904af98a14df72d1f1cb5a4b9f02728`;
- execution head: `97372c99a85595b3e4acc4a392215940c173a3bc`;
- workflow run: `35430213683`;
- job: `105863313092`;
- bounded R6V tests: **8 passed**;
- protocol self-tests: **20 passed**;
- artifact: `10580237771`;
- artifact name: `rabochii-court-receipt-35430213683`;
- artifact digest: `sha256:ed46169f4d3c53ce87417b08cde587b04adf6b9bac6ef88fa5173eccb3e4527a`.

The transient `.rabochii/court_spec.json` was absent at commission time, present only for governed Browser qualification, and restored to absence at commit `dc6721969c96a9b987e3aaf97b330935daf212df`.

No Library, WVS carrier, empirical outcome, measured P2X court, or performance data was accessed.

## Wake

Wake exactly:

`HQ_R6V_ADJUDICATION_ONLY__SELECTIVELY_FAN_IN_REPAIRED_WVS7_MATERIALIZER_BLOB_11b28416aac5a4899706150721f2f8ac8bb6ee43_TO_EXISTING_P2X__DO_NOT_RESUME_P2X_UNTIL_ALL_REQUIRED_REPAIRS_AND_LOCAL_RECONCILIATION_ARE_ADOPTED_AND_HQ_SEALS_RESUME`

Return to HQ.
