# RAWLSING HQ CURRENT — FIABC LAUNCHER R2 RETRY AUTHORIZED

Status: `RAWLSING_FIABC_LAUNCHER_SELF_CONTAMINATION_REPAIRED__MEASURED_RUN_ENVIRONMENT_UNCHANGED__FRESH_RETRY_AUTHORIZED`

Checkpoint: `20260923T2357-0400`

## Blocker classification

The first deterministic Terminal launch stopped before candidate execution because importing `rawlsing_next.fiabc_succession_producer` created `rawlsing_next/__pycache__/` before that producer enforced its clean-worktree precondition.

This is a control-plane launcher self-contamination defect.

It is not:
- Candidate A/B/C evidence;
- measured P2X evidence;
- source/oracle/T3 drift;
- a reason to reopen source truth.

No candidate cell started.

## Repair

Launcher:
`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Repair commit:
`d0838133148d89866fcbbeefaf31d5b64adf036a`

Launcher blob:
`43d250b36cc6dbba831b686a225b14497a2232e8`

Qualification:
`a5f91eb73809594ccbaa1f83df2e246f2dabb183`

Scoped bytecode suppression is applied only to:
- succession producer;
- succession preflight;
- driver `--preflight`.

The measured driver `--run` invocation remains unchanged and receives no `-B` and no global `PYTHONDONTWRITEBYTECODE`.

Protected execution head remains:
`b53ff08921af263b9db4d1ad038f35fbc12b990a`

T3 remains:
`7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`

PRE_CANDIDATE_STOP remains:
`203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384`

## Retry law

Preserve the failed work root unchanged.

Do not resume from it.

Use:
- a fresh or clean protected execution checkout at exact `b53ff089...`;
- a fresh persistent work root;
- the R2 launcher above.

The next lawful action remains the dispositive six-cell measured FIABC court.
