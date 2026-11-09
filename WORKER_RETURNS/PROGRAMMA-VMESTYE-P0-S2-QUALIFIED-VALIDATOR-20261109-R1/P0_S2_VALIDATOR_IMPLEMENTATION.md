# VMESTYE P0 S2 STAGE-AWARE VALIDATOR

## Purpose and scope
This is a separate versioned validator for the corrected Phase 0 assembly. It does not replace or modify `validation/validate_vmestye.py`, which remains the historical pre-dispatch bootstrap at Git blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f`.

The validator executes at local structural S2 only. It does not claim original-native execution, S3, scientific meaning, actor authority, source issuance or P0 acceptance.

## Test assembly
- Protected source: `2162d85db5e6822707e5cdff7aac2656ebef4761`.
- ZL-00: `11047708a6e4b4050da351f4b6cc35f03cb8269b`.
- ZL-01: `3590b223c1c04df10d78b0c1df3fc2dfa2e32618`.
- Reviewer R2: `a71fa746a733e9f33e220516c2a530893be8a088`.
- Assembly: protected VMESTYE tree plus the 9 ZL-00 and 8 ZL-01 changed files, with 17 hash-pinned rows in `P0_S2_ASSEMBLY_MANIFEST.tsv`.
- No candidate path overlap; `ESTATE_COVERAGE.tsv` is the only modified protected control file. The assembly is disposable and is not a protected merge.

## Checks
- **A. Census/source identity:** exact 25-column, 6,120-row census; unique census IDs and full composite identity; every source key re-derived from the exact source blob at the claimed commit/path; 110 anti-join rows; 111 coverage receipts; exact 2,416 Pyat and 1,314 Sorok SR-01 key sets.
- **B. RM:** 30 frozen `AJ-RM01`..`AJ-RM30` mappings, exact `RECENT_CAMPAIGN30` + `source_exact_id` selectors, one retained negative each, 56 requirement rows.
- **C. D02–D07:** 23 exact per-file selectors, grouped estate plus exact source path, source-key/ordinal grain, retained negatives, source-file row counts.
- **D. G4:** original 82-row source, exact 82 edge IDs/requiredness/predicates/G2 kind/condition, 26 IF predicates preserved, 82 predicate receipts.
- **E. Stage:** exact stage progression, no acceptance without independent review at the exact candidate head, no protected adoption for an unaccepted candidate, local S2 runner ceiling and no S3.
- **F. P1:** five literal `VMESTYE_P1_PRONG_TABLES_V1` headers, foreign-key/unjoin law and 13 distinct ZL-02–ZL-14 leases.

## Result
The historical bootstrap passed on a clean extracted copy of the protected cut. The stage-aware baseline did **not** pass: it found a real source no-drop defect in the corrected ZL-01 candidate.

`D05_SOURCE_PACKAGE` contains 6 census rows from `AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv`, while the exact source file at `b7dd1bce667651c88ddd71c17c065f2b33ec38ec` contains 11 keyed function rows. Missing exact keys are:

- `D05-F07` source row ordinal 8
- `D05-F08` source row ordinal 9
- `D05-F09` source row ordinal 10
- `D05-F10` source row ordinal 11
- `D05-F11` source row ordinal 12

The candidate per-file selector claims 6 rows; the actual source file has 11. The grouped D05 source total is therefore 29, not the claimed 24; 369 per-file source rows, not 364. This is a ZL-01 source no-drop defect, not a validator failure or a missing source byte.

## Limitations
- The validator uses local Git object reads for source bytes and exact source-key extraction. All 59 census source files and the SR/G4 sources were available.
- External locator checks for issue/PR-only RMs use the protected `RECENT_CAMPAIGN30` census row and retained negative, not a re-fetch of GitHub issue bodies.
- The run is local structural S2; no original respondent/native data, no scientific or actor issuance, no protected write and no merge.
- The actual model is `opencode-go/deepseek-v4.1-flash`; reasoning effort was not exposed by the runtime and is not claimed as I3+/HIGH.
