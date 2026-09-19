# EE-P2X SELECTIVE R6S BACKEND FAN-IN + RESUME AUTHORIZATION — 2026-09-19

Status: `R6S_RUNTIME_SELECTIVELY_FANNED_IN__P2X_LOCAL_MEASURED_EXECUTION_AUTHORIZED`

Decision:

`HQD-2026-09-19-076`

Semantic PRE-MAIN remains:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## Selective fan-in

Existing P2X branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Prior held head:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

Selective fan-in commit:

`548d7ae9be4a8a624601b5d468fb2e19693ca597`

Parent:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

The commit is one fast-forward commit ahead and changes exactly four paths:

1. `rawlsing_next/ee_p2x_darwin_stage_backend.py`
   - blob:
     `ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

2. `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`
   - blob:
     `3a3e228843656e023673310c26acbd41ecdc1b3b`

3. `WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`
   - blob:
     `9406bacfd928393f6a159a46216aa1f7ec129f34`

4. `WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json`
   - blob:
     `e04e84b76f8b4eb53905276dd025938bf2e5f6fe`

No qualification test, transient court spec, R6S prose return, or unrelated worker artifact was fanned into P2X.

## Adopted runtime contract

Backend contract:

`RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0`

Qualified Darwin driver remains:

`rawlsing_next/ee_p2x_darwin_court_driver.py`

blob:

`c3a368270f6f7a6f613efb78e31972e64a092c88`

Adopted continuation reducer remains:

`RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0`

blob:

`e06e95dd370a4fd44235932088308c3372522ed4`

exact-byte SHA-256:

`ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`

The driver requires the original frozen P2X resume head:

`a954e2d6676843da8427ef2439b5d1ef33478359`

to be an ancestor of HEAD.

It does **not** require HEAD equality.

Therefore the selectively fanned-in head `548d7ae9...` is lawful under the existing driver repo gate.

## Resume point

First unfinished reducer stage remains:

`LITS_I/A/S02_C11_REACHABILITY`

Do not repeat reducer stages marked:

`DONE__PRESERVE`

In particular:

- do not repeat LiTS-A qualifying first-build stage;
- do not repeat LiTS-B standalone cacheless-C11 preparatory stage.

The driver owns stage order, stage terminalization, candidate-local propagation and resumability.

Do not hand-maintain a parallel stage ledger.

## Execution authorization

The prior HQ coordination hold on EE-P2X is lifted.

P2X is authorized to resume measured execution on:

`LOCAL-MACHINE CODEX`

on the qualifying Darwin x86_64 host.

Library/source access:

`EXACT_ONLY`

for exactly:

- `LITS-2006-data.dta`
  SHA-256:
  `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

- `WVS Wave 7.sav`
  SHA-256:
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Required runtime remains:

- Darwin x86_64;
- CPython `3.11.3`;
- `pyreadstat==1.3.6`;
- `pyarrow==25.0.1`;
- accepted Darwin RSS byte-normalization law.

No substitute carrier/runtime/parser.

## Mechanical execution sequence

Use:

`WORKER_RETURNS/EE-P2X/LOCAL_EXECUTOR_README.md`

and the exact driver CLI.

At minimum:

1. resolve/verify live HQ and require P2X HEAD `548d7ae9be4a8a624601b5d468fb2e19693ca597` before the first new measured stage;
2. verify source SHA identities;
3. run driver `--preflight`;
4. inspect `--status`;
5. run `--resume` from the existing first unfinished stage;
6. after every expensive completed stage, capture the exact supervisor token and commit/push bounded governed evidence as already required by the commission;
7. continue autonomously through every lawful next stage;
8. after stage completion, mechanically synchronize normalized manifest through:
   `WORKER_RETURNS/EE-P2X/11A_sync_ee_p2x_driver_manifest.py`;
9. run:
   `WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py`;
10. require:
    `PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE`;
11. run driver `--verify-only` after S17 is terminal;
12. commit/push final governed return.

## Current candidate law

LiTS A and B are lawful executable production paths.

LiTS C performs its lawful preparation and stops candidate-locally at exact S02 q310/q311 reachability nonqualification.

No C repair/fallback.

WVS A and B are lawful executable production paths through R6S projection + exact P2F2/Lock2 runtime authority.

WVS C remains the preserved portability failure with no backend path.

## Measurement law

This is the actual measured court.

Parity/oracle completion precedes performance admission.

No surrogate metrics.

No pre-populated measured zero.

No historic product substitution as fresh execution.

No ranking, scoring, winner, recommendation or selection.

No cross-universe metric pooling.

## Wake

EE-P2X is now:

`AUTHORIZED_TO_RESUME_LOCAL_MEASURED_EXECUTION`

Successful terminal remains:

`EE_P2X_PASS__FINAL_TWO_SOURCE_ABC_EQUAL_WORK_P2_EVIDENCE_COMPLETE__READY_FOR_HQ_MEASURED_SYNTHESIS`

Any lawful typed candidate/source/court stop must be preserved exactly under the existing driver/reducer law.

Terminal:

`P2X_R6S_BACKEND_FANNED_IN__LOCAL_MEASURED_EXECUTION_RESUMED`
