# VMESTYE P0 S2 RETURN

## Terminal disposition
`VMESTYE_P0_S2_VALIDATOR_EXECUTED__NEGATIVE_CONTROLS_EIGHT_OF_EIGHT_PASS__INDEPENDENT_RECEIVING_PENDING__NO_P1_RELEASE`

## Corrected cuts
- Protected PRE-MAIN: `2162d85db5e6822707e5cdff7aac2656ebef4761`.
- ZL-00: `11047708a6e4b4050da351f4b6cc35f03cb8269b`.
- ZL-01 corrected: `353adc216a832a6c41ccc99f77cb3b53651af64e`.
- Independent reviewer R3: `caefb06bb73e1bc58033794184069337c6847e71`.
- S2 branch/PR: `test/vmestye-p0-s2-qualified-validator-r1` / https://github.com/maidiu/rawlsing/pull/826.

## Actual execution
- Historical bootstrap: **PASS** on a clean `git archive` extraction of protected `2162d85d`; 18 historical `NOT_DISPATCHED` and nine `NOT_RUN` gates preserved.
- Stage-aware clean baseline: **PASS**, `49` checks passed, `0` failed, `0` held, exit `0`.
- Negative controls: **8/8 PASS** on that clean baseline, each producing its intended fail-closed error ID. They no longer inherit the D05 baseline failure.
- Validator unit tests: `5 passed`.

## Corrected D05 result
ZL-01 now contains all 11 exact source keyed records from `AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv` at `b7dd1bce667651c88ddd71c17c065f2b33ec38ec` (blob `bf77b70f1858697ce663f2eeec2e91e25aa6ac94`):

- D05 file rows: 11, not 6.
- Grouped D05 rows: 29, not 24.
- D02–D07 per-file rows: 369, not 364.
- Census rows: 6,125, not 6,120.

The validator confirms exact source key/ordinal equality, updated anti-joins and updated coverage receipts.

## Historical CSV qualification
`D05-F06` (source row 7) and `D05-F11` (source row 12) have malformed CSV quoting; strict CSV parses only five fields, while their raw identities are exact. ZL-01 added `P0_D05_RAW_SOURCE_QUALIFICATION.tsv` with 11 raw-line SHA256 receipts. The validator checks that sidecar and records the field-level boundary as an explicit HOLD inside the source qualification; it does not assert or fabricate field meaning. Historical source bytes were not rewritten.

## Status ceiling
- This is local sourcefree structural S2 evidence only.
- No P0 acceptance, no ZL-02–ZL-14 release, no protected merge.
- No original respondent/native/S3, scientific, actor or first-consumer promotion.
- The same independent ZL-P0R reviewer must re-receive both corrected heads and this clean-run evidence before any P0 decision.

## Evidence
Return directory: `WORKER_RETURNS/PROGRAMMA-VMESTYE-P0-S2-QUALIFIED-VALIDATOR-20261109-R1/`.

Includes the validator and test sources on the worker branch, assembly/stage manifests, the 11-row D05 raw-source qualification, baseline and historical bootstrap logs, all eight clean-baseline negative-control logs, execution receipt, environment manifest, and changed-file inventory. Exact PR head is the latest commit on PR #826; the execution-return issue comment records it.
