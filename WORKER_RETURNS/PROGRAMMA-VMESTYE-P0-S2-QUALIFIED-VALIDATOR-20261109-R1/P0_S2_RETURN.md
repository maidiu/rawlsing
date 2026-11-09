# VMESTYE P0 S2 RETURN

## Terminal disposition
`FAIL__VMESTYE_P0_S2_BASELINE_D05_SOURCE_KEY_LOSS__ZL01_OWNS_FIVE_OMITTED_AUTHORITY_MAINTENANCE_ROWS__NEGATIVE_CONTROLS_EIGHT_OF_EIGHT_PASS__INDEPENDENT_RECEIVING_PENDING__NO_P1_RELEASE`

## What actually ran
- Historical bootstrap: `PASS` on a clean `git archive` extraction of protected `2162d85d`. It preserved 18 historical `NOT_DISPATCHED`, nine `NOT_RUN` gates and the five frozen seed blobs.
- Stage-aware validator: `FAIL` on the corrected ZL-00/ZL-01 assembly. It found the D05 source-key omission below; all other implemented checks passed.
- Eight deliberate negative controls: **8/8 PASS**. Each produced its intended fail-closed error ID and exit code, not a crash.
- Unit tests for the new helper/constraint layer: `5 passed`.

## Exact blocking defect
The corrected ZL-01 census omits five source keys from:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/LONG_MEMORY_CURRENT_ZERO_LOSS_DELTA_R1/D05_MAINTENANCE_LIFECYCLE/AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv`

at commit `b7dd1bce667651c88ddd71c17c065f2b33ec38ec`, blob `bf77b70f1858697ce663f2eeec2e91e25aa6ac94`:

- `D05-F07` (source row 8)
- `D05-F08` (source row 9)
- `D05-F09` (source row 10)
- `D05-F10` (source row 11)
- `D05-F11` (source row 12)

The source file has 11 keyed rows; the candidate census and per-file anti-join claim 6. This makes the D05 source total 29 rather than 24, and the 23 per-file source total 369 rather than 364. The candidate’s claimed exact no-drop is therefore not true at the source file grain.

Responsible owner: ZL-01. The correction must add the five exact source keys to its own candidate census with exact source commit/path/blob/row ordinal/negative status, update the D05 per-file and grouped counts and receipts, and return a new immutable head for the same independent ZL-P0R reviewer. No protected edit was made here.

Falsifier: an independent source-blob reread of `AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv` that shows all 11 keyed rows and a candidate census that still claims only 6, or a candidate correction that adds the five keys with exact retained negatives and all derived counts changed consistently.

## Negative controls
All eight specified defects produced the intended typed failures:
1. SR-01 missing key.
2. RM alias/selector corruption.
3. G4 predicate corruption.
4. IF-to-MUST promotion.
5. D02 dangling source path.
6. RM retained-negative loss.
7. Forged acceptance without review.
8. P1 frozen-header corruption.

The baseline D05 failure is present in every copied fixture; the negative controls are still counted pass only because the named intended error ID appears. No control produced a Python crash or an unrelated setup failure.

## Review and release status
- P0 is **not accepted**.
- P1 ZL-02–ZL-14 is **not released**.
- No protected write, merge, native source run, scientific/actor issuance or current-machine zero-loss claim.
- The existing independent ZL-P0R reviewer (#799 / PR #821) must receive the failing baseline and negative-control logs and decide whether to require a ZL-01 correction.
- Historical bootstrap success is not current P0 acceptance.

## Evidence
Return directory: `WORKER_RETURNS/PROGRAMMA-VMESTYE-P0-S2-QUALIFIED-VALIDATOR-20261109-R1/`.

Includes assembly/stage manifests, baseline and bootstrap stdout/stderr, complete negative-control logs, validator/unit-test sources in the worker branch, and the changed-file inventory. PR/branch head are recorded after publication.
