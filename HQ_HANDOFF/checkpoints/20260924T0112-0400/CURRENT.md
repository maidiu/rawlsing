# RAWLSING HQ CURRENT — FIABC PACKAGE-MODULE ENTRYPOINT REPAIR

Status: `RAWLSING_FIABC_DRIVER_ENTRYPOINT_REPAIRED__RUN1_PRE_CANDIDATE_STOP_BANKED__MEASURED_RETRY_AUTHORIZED`

Checkpoint: `20260924T0112-0400`

## Governing decision

`HQD-2026-09-24-091`

## RUN1 classification

RUN1 work root:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN1`

Observed state:
- immutable succession evidence fetch PASS;
- runtime/source/frozen answer-key gates PASS;
- succession producer PASS;
- direct succession preflight PASS;
- driver preflight failed before initialization;
- no T5 preflight receipt;
- no candidate process started;
- no candidate output seen.

Exact driver-preflight failure:

`ModuleNotFoundError: No module named 'rawlsing_next'`

Cause: launcher invoked the package-internal driver by file path rather than module entrypoint.

## Repair

Launcher path:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Repair commit:

`f102dccfe53ecd57d146b256900962705ef24c50`

Launcher blob:

`37d2a3c33eb2958c873cecc3ab083ffee2c0e144`

Qualification receipt:

`HQ_HANDOFF/launchers/FIABC_DISPOSITIVE_SIX_CELL_LAUNCHER_QUALIFICATION_R4.json`

Preflight invocation is now:

`python -B -m rawlsing_next.ee_p2x_darwin_court_driver --preflight ...`

Measured invocation is now:

`python -m rawlsing_next.ee_p2x_darwin_court_driver --run ...`

No `PYTHONPATH` is injected.

Measured `--run` receives no `-B`.

No protected execution Python file changed.

## Protected execution

Branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact head remains:

`bc832181b4284ac110d2be44fc83504e04de081e`

## Frozen answer key

T3:
`7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`

PRE_CANDIDATE_STOP:
`203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384`

## Next lawful action

Preserve RUN1 unchanged.

Use a fresh protected checkout and fresh persistent work root.

Use the current PRE-MAIN launcher at blob `37d2a3c3...`.

If driver preflight passes and the launcher prints:

`FIABC_DISPOSITIVE_PREFLIGHT_GREEN__STARTING_SIX_CELL_MEASURED_COURT`

the measured six-cell court has begun.

Do not intervene in a healthy measured run.
