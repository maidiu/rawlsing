# FIABC-LM3 — R6X Stopped-Ledger Reconciliation

## Terminal

`FIABC_LM3_R6X_STOPPED_LEDGER_RECONCILED__READY_FOR_LOCAL_FANIN`

## Exact checkout

- Repository: `maidiu/rawlsing`
- Base: `7e33b76c7d46dcee31dd3be7b3b0230f3c18a152`
- Branch: `agent/rabochii-premain-fiabc-lm3-r6x-ledger-reconciliation-r1`
- Return directory: `WORKER_RETURNS/FIABC-LM3/`

## Scope result

This return applies the accepted R6X protocol to the real stopped local ledger at `/private/tmp/ee-p2x-exec-r3` in audit-only mode. The work root was already reconciled; no second mutation was attempted.

R6X identity is exact:

- pre-reconciliation ledger SHA-256: `7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`
- post-reconciliation ledger SHA-256: `4d0c412df4844906df78a94fbd0b3f6dff40412ca695e76137d3309cf1aaedd6`
- R6X receipt SHA-256: `cd346db0623ce1f138bd0f14d9a81f8edf45b62c576c4f35910241b98edc7b26`
- audit result: `AUDIT_ONLY__ALREADY_RECONCILED`
- removed historical ledger addresses: `62`
- retained post-R6X ledger addresses: `41`
- source-carrier access by reconciliation: `false`
- empirical measurement by reconciliation: `false`
- candidate roots deleted: `false`
- next stage recorded by R6X: `LITS_I/A/S02_C11_REACHABILITY`

The 62 removed entries are preserved as historical rows in `01_R6X_RECONCILED_LEDGER.csv`; they are not treated as erased history. R6X removed the four accepted infrastructure blocker entries, their mechanically propagated stops, and the orphan S17 state, plus failed-attempt-local mutable state. LiTS-C and WVS-C historical evidence remains preserved.

## Current T1–T6 disposition

All 103 historical ledger items are accounted for:

- `PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`: 10
- `NOT_REACHED`: 72
- `NOT_APPLICABLE`: 21
- `EXECUTED_NOW`: 0
- `LAWFULLY_PRESERVED_MEASURED_WORK`: 0
- current numeric credit: `0`

The zero `EXECUTED_NOW` and zero `LAWFULLY_PRESERVED_MEASURED_WORK` counts are intentional. This commission did not run candidate execution. T4-preserved LiTS-A historical telemetry remains non-creditable until exact generic parentage and field-wise workload/runtime/state/isolation/operation/metric compatibility are proved. LiTS-B remains semantic-only with no captured telemetry. Missing or unreached telemetry is typed null, never zero.

The historical LiTS-C and WVS-C failures and WVS-C downstream frozen-law skips are explicitly marked as obsolete current-capability law where applicable. Current T2/T5 identity binds six admitted cells: LiTS-I/WVS7 × A/B/C, with current Candidate-C law preserved and no invented accelerator.

## Identity binding

Surviving evidence is bound to the current:

- source roots: LiTS-I `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`; WVS7 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- candidate owners: A `d4915e7e6755ba1850756aebff72f982f73a332b`, B `7c509c2098d0030f253344eb3f682471378812a8`, C `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`;
- workloads: LiTS-I D04-R2 50-candidate/77-role; WVS7 Lock2 46-candidate frontier;
- runtime: Darwin x86_64, CPython 3.11.3, pyreadstat 1.3.6, pyarrow 25.0.1, `ru_maxrss` in bytes;
- authority: T2 HQ checkpoint `20260918T0210-0400`, handoff `10c91b1e03285b50cae7a39ab1458826712c52b5`, Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`, and the exact T3–T6 binding blobs recorded in the JSON input receipt;
- replay/terminal: fresh process per source×candidate cell, one candidate-neutral oracle, and the T5 governed I05 terminal identity.

## Fresh work still required

`04_FRESH_EXECUTION_REQUIREMENTS.csv` records the bounded next work. It includes current LiTS-A/B continuation, current LiTS-C and WVS-A/B/C source-backed qualification, fresh S17 final verification, generic parentage/oracle/physical materialization, field-wise T4 admission, and measured P2X only as the final separately authorized gate.

No LiTS-I raw source, WVS7 raw source, candidate execution, measured P2X, ranking, selection, source certification, or semantic adjudication was performed here.

## Artifacts

- `01_R6X_RECONCILED_LEDGER.csv` — 103-row post/reconciled historical ledger disposition.
- `02_HISTORICAL_TO_CURRENT_DISPOSITION.csv` — artifact-level historical-to-current map.
- `03_PRESERVED_WORK_ACCOUNTING_INPUTS.json` — exact T4 accounting inputs with current metric values kept null.
- `04_FRESH_EXECUTION_REQUIREMENTS.csv` — fresh materialization/execution requirements.
- `05_COMMAND_LEDGER.csv` — truthful command and boundary ledger.
- `RETURN.json` — machine-readable return.

Input/output hashes for the five tabular/JSON payloads:

- `01_R6X_RECONCILED_LEDGER.csv`: `1024ef42268b1c38c07497be1c15820a38019294b7e6f1e58e1877e9acb96926`
- `02_HISTORICAL_TO_CURRENT_DISPOSITION.csv`: `e0017ca233b94a4269621da351e2e313bf5b0233b26ab2435f7066d118ee1edd`
- `03_PRESERVED_WORK_ACCOUNTING_INPUTS.json`: `076679f906152b88dfc079205ebfc245e99669bd9ba9c529fb43c8680acca04a`
- `04_FRESH_EXECUTION_REQUIREMENTS.csv`: `7fefc27786cea97e0ef16be75803567705e72258203f9b91b8c156091a01c6d4`
- `05_COMMAND_LEDGER.csv`: `7a0a0d4ef236e43123c9dc327faa8ffb90bd69537f61d8a7bca35248bd30c96d`
