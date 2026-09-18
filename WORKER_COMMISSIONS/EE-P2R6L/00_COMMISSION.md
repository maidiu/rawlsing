# EE-P2R6L — LiTS-I ACCEPTED I02 SUCCESSOR RELEASE MECHANICAL EXECUTION

Repository: `maidiu/rawlsing`

## Execution surface

**LOCAL-MACHINE CODEX**

## Maximum model intelligence required

**LUNA**

Do not use a higher intelligence tier unless execution is impossible at Luna for a purely tooling reason. This commission contains no authorized semantic judgment or redesign work.

## Library access

**EXACT_ONLY**

Authorized carrier only:

`LITS-2006-data.dta`

Required SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Expected shape:

- 29,002 rows
- 1,198 variables

Do not inspect, enumerate, or open any other Library/source carrier.

Exact branch:

`agent/rabochii-prev3-ee-p2r6l-lits-i02-successor-release-local-execution-r1`

Exact base / prepared package head:

`648a39ad5bed42f66e066410af5869604d29c12d`

Prepared R5B package:

`WORKER_RETURNS/EE-P2R5B/`

Before execution, resolve live `HQ_HANDOFF/LATEST.json` and verify the immutable checkpoint packet.

Proceed only if HQ has adopted EE-P2R5A realization authority and still authorizes this exact local execution grain.

## Mission

Perform **only** the fully prepared R5B source-backed I02 successor-release execution.

Do not investigate.

Do not redesign.

Do not patch the driver or verifier if execution fails.

The only allowed substantive source-side act is running the exact prepared driver against the exact authorized LiTS-I carrier and then running the exact prepared verifier.

## Prepared driver

`WORKER_RETURNS/EE-P2R5B/03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py`

Git blob:

`b819fdff50470a71f1c570aa8021e28b361fa986`

Prepared verifier:

`WORKER_RETURNS/EE-P2R5B/05_SUCCESSOR_RELEASE_VERIFIER.py`

Git blob:

`348c533a3dff477c3ea0c2f19b41a4e131ef3d3f`

Prepared local packet:

`WORKER_RETURNS/EE-P2R5B/06_LOCAL_EXECUTION_PACKET.json`

Receipt schema:

`WORKER_RETURNS/EE-P2R5B/04_SUCCESSOR_RELEASE_RECEIPT_SCHEMA.json`

## Runtime

Accepted baseline:

`Python 3.11.3`

Prepared exact package requirements:

- `pyreadstat==1.3.2`
- `pandas==2.3.1`
- `numpy==2.3.2`
- `pyarrow==22.0.0`
- `duckdb==1.5.2`

Use the existing environment only if it satisfies the prepared packet exactly enough for the driver to run under its own checks.

If exact dependencies are missing, an isolated environment may be created and only the exact required packages installed.

Do not alter repository source code to accommodate dependency drift.

Network is not required for execution itself. If package installation is impossible, STOP and return the exact environment blocker.

## Source location

Locate only the authorized file by exact filename and SHA.

Do not inspect other Library carriers.

Before execution prove:

- filename is the authorized LiTS carrier or a lawful materialization thereof;
- SHA-256 exactly matches;
- no other empirical carrier is opened.

## Output directory

Use a new dedicated empty directory under:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/`

Before running, ensure it does not contain stale output files.

Do not overwrite a prior run and call it fresh evidence.

## Exact execution

Run the prepared driver exactly in substance:

`python WORKER_RETURNS/EE-P2R5B/03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py --source <EXACT_AUTHORIZED_LITS_PATH> --output-dir WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT`

Do not add semantic flags.

Do not edit the driver.

The expected outputs are exactly:

- `successor_release_receipt.json`
- `successor_release_replay_manifest.json`
- `successor_release_m01_m18.json`
- `successor_release_extension_scan.json`

Then run:

`python WORKER_RETURNS/EE-P2R5B/05_SUCCESSOR_RELEASE_VERIFIER.py --receipt WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_receipt.json`

## PASS criteria

PASS requires all of the following:

1. exact source SHA/shape checks pass;
2. accepted base projection identity reproduces exactly:
   `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
3. accepted base candidate identity reproduces exactly:
   `7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c`;
4. accepted base I02 release reproduces exactly:
   `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
5. accepted base ReplayManifest reproduces exactly:
   `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`;
6. frozen F02 q310/q311 source replay counts/roots reproduce exactly;
7. exact row relation `f02_row = i02_physical_row - 1` proves across the full source;
8. all required extension refs/authorities close;
9. accepted I02 returns `ACCEPTED_C11_LOGICAL_RELEASE`;
10. complete M01-M18 closes;
11. `C11Repository.resolve_release_exact(result.release_ref)` succeeds;
12. prepared verifier exits 0;
13. no realization/equality claim is made between `bf305...` and the new I02 runtime release.

The future successor runtime release hash is **unknown before execution**. Report exactly what I02 mints.

## Failure law

On any failure:

**STOP.**

Do not patch.

Do not change source bytes.

Do not change decoder configuration.

Do not change vendored support.

Do not weaken a check.

Do not rerun with altered semantics.

Do not infer the intended fix.

Return the exact first blocker with:

- command;
- exit status;
- stderr/error;
- stage;
- environment identity;
- any files produced before failure.

A failed run is evidence, not permission to repair.

## R5A boundary

HQ adoption of R5A authorizes the **relation schema**, not a concrete binding before this run.

This worker must not issue a `ReleaseRealizationBinding`.

The new I02 release ref and receipts are facts for a later Browser issuer/adjudication step.

Do not:

- claim new runtime release == `bf305...`;
- rewrite the frozen selector release ref;
- modify selector identities;
- emit a concrete realization binding.

## Required governed return

On PASS, keep the four exact output files under:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/`

Also write:

`WORKER_RETURNS/EE-P2R6L/00_RETURN.md`

and:

`WORKER_RETURNS/EE-P2R6L/01_LOCAL_EXECUTION_RECEIPT.json`

The execution receipt must bind:

- exact source path/materialization identity;
- source SHA;
- Python and package versions;
- exact driver/verifier blobs;
- commands and exit statuses;
- all four output-file SHA-256 values;
- exact I02-minted runtime release ref;
- no realization binding issued;
- no P2X/BE1 activity.

Commit only governed receipts/output JSON.

Never commit source carrier bytes.

## PASS terminal

`EE_P2R6L_PASS__ACCEPTED_I02_SUCCESSOR_RELEASE_MINTED_AND_VERIFIED__READY_FOR_CONCRETE_REALIZATION_BINDING_ISSUANCE`

## BLOCK terminal family

`EE_P2R6L_BLOCK__<EXACT_FIRST_MECHANICAL_FAILURE>`

Do not convert BLOCK to repair work.

## Hard forbidden

- no source carrier except exact LiTS-I;
- no WVS access;
- no semantic interpretation;
- no code repair;
- no selector remint;
- no R5A binding issuance;
- no production evaluator/I05 change;
- no D02/F02 workload mutation;
- no P2X or BE1;
- no Candidate-C repair;
- no Lock1/Lock2 mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch.

Commit the governed return on this exact branch and report final branch tip, PASS/BLOCK, exact runtime release ref if PASS, output hashes, environment identity, and verifier disposition.

Return to HQ.
