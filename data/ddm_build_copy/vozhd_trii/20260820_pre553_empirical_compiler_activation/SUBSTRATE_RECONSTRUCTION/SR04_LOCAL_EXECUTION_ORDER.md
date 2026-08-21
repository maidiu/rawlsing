# SR04 — PHYSICAL CARRIER BAKEOFF — BOUNDED LOCAL CODEX CELL

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Mission

Implement the single benchmark harness authorized by:

`18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`

then execute the bakeoff exactly under that contract and return the small metrics/receipt package.

This cell is mechanical benchmark implementation + execution. It has **no authority** to choose semantic architecture, reinterpret source meaning, change the candidate set, alter budgets, or modify accepted runtime code.

## Read first

1. `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
2. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
3. `16_SR03_R3_ADJUDICATION.md`
4. `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`
5. accepted reference code only as needed to understand file-neutral C11/query shapes:
   - `rawlsing_next/pre553_c11_repository.py`
   - `rawlsing_next/pre553_c11_ingest.py`
   - `rawlsing_next/pre553_empirical_query.py`
   - accepted I03/I05 test fixtures under `rawlsing_next/tests/`

Reference files are READ ONLY.

## Sole permitted repository write

You may create/modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No other repository file may change.

## Local source bytes

Use exact hash-matched sources under the local Rawlsing source root, normally:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data`

Required exact source hashes are frozen in the contract and `SOURCE_BYTE_INVENTORY.csv`.

Do not substitute files.

## Implementation preflight

Before full execution:

- verify exact Git HEAD from HQ;
- verify only the permitted harness path is dirty after implementation;
- syntax-check the harness;
- run a tiny harness self-test if implemented, confined to the disposable work root;
- verify the harness itself rejects wrong source hashes and unsafe disk conditions;
- verify it never connects to `DATABASE_URL` for the PostgreSQL candidate;
- verify the PostgreSQL candidate creates only a disposable local cluster;
- verify candidate cleanup is confined to the SR04 disposable root.

## Harness publication

After the harness passes the preflight:

1. commit **only** `SR04_CARRIER_BAKEOFF.py` with message:
   `Implement frozen SR04 carrier bakeoff harness`
2. push the control branch;
3. record the resulting exact commit SHA;
4. execute the full bakeoff from that exact committed harness.

Do not commit local result data, virtualenvs, staging files, candidate databases, stdout/stderr, `.DS_Store`, or other artifacts.

## Full execution

Run the committed harness against the exact local source root and a fresh disposable work root under `/private/tmp`.

The command-line interface may be chosen mechanically by the harness implementation, but the final return must include the exact command. Recommended form:

`python <ORDER_ROOT>/SR04_CARRIER_BAKEOFF.py --source-root /Users/matthewsmith/Desktop/Rawlsing/data/Data --output-dir SR04_CARRIER_BAKEOFF_RESULTS`

The frozen contract controls all candidate/layout/query/disk/time semantics regardless of CLI spelling.

## Required return to HQ

- starting exact HQ launch HEAD;
- committed harness execution HEAD;
- harness path and SHA-256;
- exact full execution command;
- exit code;
- full `SR04_CARRIER_BAKEOFF_RESULTS/` small result package;
- deterministic result ZIP byte size + SHA-256;
- candidate dispositions;
- provisional selection;
- success token presence;
- final `git status -sb`;
- pushed branch HEAD.

Required success token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Fail closed

Do not improvise around a contract failure.

Return exact failure for:

- source hash mismatch;
- fixture oracle mismatch;
- disk reserve violation;
- candidate budget/time violation;
- missing PostgreSQL server binaries;
- benchmark dependency failure after the explicitly authorized isolated-temp dependency path;
- contract ambiguity.

Never delete user files to make space. Never alter the live Rawlsing database. Never relax the candidate correctness gate.
