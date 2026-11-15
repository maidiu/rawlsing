# RAWLSING HQ CURRENT — FIABC I01/I02 SUCCESSION REPAIR ACCEPTED

Status: `RAWLSING_FIABC_I01_I02_SUCCESSION_REPAIR_ACCEPTED__PROTECTED_EXECUTION_REBOUND__MEASURED_SIX_CELL_RETRY_AUTHORIZED`

Checkpoint: `20260924T0058-0400`

## Governing decision

`HQD-2026-09-24-090`

## Accepted repair

Implementation head:
`ebb0da371f809a47bce68c6beb331208846573a9`

Source-free qualification head:
`bc832181b4284ac110d2be44fc83504e04de081e`

R4 qualification:
- 204 pytest tests PASS;
- 28 subtests PASS;
- current static cross-lane assertions PASS;
- live current-head succession producer PASS;
- live succession preflight PASS;
- candidate processes started = 0;
- candidate outputs seen = 0;
- exact cell order = LiTS A/B/C then WVS7 A/B/C.

The repair restores the omitted Wave-3 current owners:
- `rawlsing_next/pre553_diagnostics.py`
- `rawlsing_next/pre553_effective_n.py`

No measured driver/backend, T2/T5 contract, frozen oracle, or T3 bytes were modified by the implementation fan-in.

## Canonical integration

PRE-MAIN two-parent integration commit:
`c020a684c8547acf3c98a048c101f875a165339b`

HQ acceptance receipt:
`WORKER_RETURNS/PREMAIN-FIABC-W3-I01-I02-FANIN-R1/02_HQ_ACCEPTANCE.json`

Protected execution branch:
`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact protected execution head:
`bc832181b4284ac110d2be44fc83504e04de081e`

Promotion was fast-forward only.

## Frozen answer key remains unchanged

- LiTS oracle identity: `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`
- WVS7 live oracle identity: `e546c15533ba138be9995095059ea3b70b64a6d7b5765e3789935cff7342ef00`
- T3 SHA-256: `7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`
- PRE_CANDIDATE_STOP identity: `203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384`

## Deterministic launcher

Path:
`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Current launcher binding commit:
`590558a703107e492bd769715ec4531c2c82ce26`

Current launcher blob:
`852cffd259e2cd73092ae179a7cb6a5e0506e8aa`

Launcher qualification receipt:
`HQ_HANDOFF/launchers/FIABC_DISPOSITIVE_SIX_CELL_LAUNCHER_QUALIFICATION_R3.json`

The launcher now:
1. requires protected execution head `bc832181...`;
2. verifies source and frozen answer-key identities;
3. fetches exactly the three off-lineage immutable succession evidence commits:
   - `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
   - `76c73e5c15eb512fa0b3217bc9e313d2b54f9a2d`
   - `0c0dd1f23bc59017552afdbd5af2021f051d48f7`
4. uses scoped `python -B` only during premeasurement succession/preflight;
5. does not invoke `produce-lits` or `freeze-t3`;
6. invokes measured driver `--run` without `-B` or a global bytecode environment override.

## Earlier failed launch attempts

All earlier failed roots are pre-candidate control-plane stops.

Preserve them unchanged. Do not resume from them.

They are not A/B/C evidence and are not measured P2X evidence.

## Next lawful action

Run one fresh deterministic Terminal launch from a fresh clone of protected execution head `bc832181...` and a new persistent work root.

If preflight passes, do not intervene: allow the executable to enter and complete the serialized six-cell court.

If it stops, preserve the new work root unchanged and adjudicate the emitted evidence.

P2 HQ synthesis remains blocked until measured six-cell evidence exists.
