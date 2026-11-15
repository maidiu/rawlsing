# RAWLSING HQ CHECKPOINT — 20260919T0110-0400

Status: `R6S_ADOPTED_PASS__SELECTIVE_P2X_FANIN_READY__P2X_HELD`

Semantic PRE-MAIN:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

Controlling decision:

- `HQD-2026-09-19-075` — adopt EE-P2R6S PASS and exact qualified runtime fan-in set.

Adoption record:

`HQ_HANDOFF/EE_P2R6S_PASS_ADOPTION_20260919.md`

## Adopted R6S

Return head:

`48887a2b1523c9d20933e4d6c5e341e80d7a0ff6`

Terminals:

`EE_P2X_PRODUCTION_STAGE_BACKEND_READY__NO_EMPIRICAL_MEASUREMENT_PERFORMED`

`EE_P2R6S_PASS__WVS7_COUNTRY_COORDINATE_AND_COMPLETE_GOVERNED_PROJECTION_QUALIFIED__ORIGINAL_BE1_PRODUCTION_BACKEND_READY__READY_FOR_HQ_SELECTIVE_FANIN_TO_P2X`

WVS projection identity:

`838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`

Production backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

## Selective fan-in set

1. `rawlsing_next/ee_p2x_darwin_stage_backend.py`
   `ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

2. `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`
   `3a3e228843656e023673310c26acbd41ecdc1b3b`

3. `WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`
   `9406bacfd928393f6a159a46216aa1f7ec129f34`

4. `WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json`
   `e04e84b76f8b4eb53905276dd025938bf2e5f6fe`

Qualification-only tests and `.rabochii/**` are excluded.

R6S worker tree is not merged wholesale.

## P2X

Held branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Observed head:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

P2X remains held until exact fan-in is created, verified and sealed.

Terminal:

`R6S_ADOPTED__SELECTIVE_P2X_FANIN_READY__P2X_HELD`
