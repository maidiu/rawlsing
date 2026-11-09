# VMESTYE P0 S2 STAGE-AWARE VALIDATOR

## Purpose and scope
This is a separate versioned validator for the corrected Phase 0 assembly. It does not replace or modify `validation/validate_vmestye.py`, which remains the historical pre-dispatch bootstrap at Git blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f`.

The validator executes at local structural S2 only. It does not claim original-native execution, S3, scientific meaning, actor authority, source issuance or P0 acceptance.

## Test assembly
- Protected source: `2162d85db5e6822707e5cdff7aac2656ebef4761`.
- ZL-00: `11047708a6e4b4050da351f4b6cc35f03cb8269b`.
- ZL-01 corrected: `353adc216a832a6c41ccc99f77cb3b53651af64e`.
- Reviewer R3: `caefb06bb73e1bc58033794184069337c6847e71`.
- Assembly: protected VMESTYE tree plus the 9 ZL-00 and 9 ZL-01 changed files, with 18 hash-pinned rows in `P0_S2_ASSEMBLY_MANIFEST.tsv`.
- No candidate path overlap; `ESTATE_COVERAGE.tsv` is the only modified protected control file. The assembly is disposable and is not a protected merge.

## Checks
- **A. Census/source identity:** exact 25-column, source-derived 6,125-row census; unique census IDs and full composite identity; every source key re-derived from the exact source blob at the claimed commit/path; 110 anti-join rows; 111 coverage receipts; exact 2,416 Pyat and 1,314 Sorok SR-01 key sets.
- **B. RM:** 30 frozen `AJ-RM01`..`AJ-RM30` mappings, exact `RECENT_CAMPAIGN30` + `source_exact_id` selectors, one retained negative each, 56 requirement rows.
- **C. D02–D07:** 23 exact per-file selectors, grouped estate plus exact source path, source-key/ordinal grain, retained negatives, source-derived 369 source-file rows. D05 raw-source qualification is checked separately.
- **D. G4:** original 82-row source, exact 82 edge IDs/requiredness/predicates/G2 kind/condition, 26 IF predicates preserved, 82 predicate receipts.
- **E. Stage:** exact stage progression, no acceptance without independent review at the exact candidate head, no protected adoption for an unaccepted candidate, local S2 runner ceiling and no S3.
- **F. P1:** five literal `VMESTYE_P1_PRONG_TABLES_V1` headers, foreign-key/unjoin law and 13 distinct ZL-02–ZL-14 leases.

## Result
The historical bootstrap passed on a clean extracted copy of the protected cut. The stage-aware baseline passed cleanly against the corrected ZL-01 head: 49 checks PASS, 0 FAIL, 0 HOLD, exit 0. The eight deliberate negative controls were rerun on that clean baseline and all eight detected their intended error IDs.

## D05 qualification
`AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv` contains 11 exact keyed rows `D05-F01..F11`. Two rows, `D05-F06` and `D05-F11`, have malformed CSV quoting and parse to five fields rather than eight. Their raw identities and line hashes are exact; ZL-01's `P0_D05_RAW_SOURCE_QUALIFICATION.tsv` records the strict-CSV failure and field-semantic HOLD for those rows. The validator verifies that qualification artifact and does not assert the missing field meanings.

## Limitations
- The validator uses local Git object reads for source bytes and exact source-key extraction. All 59 census source files and the SR/G4 sources were available.
- External locator checks for issue/PR-only RMs use the protected `RECENT_CAMPAIGN30` census row and retained negative, not a re-fetch of GitHub issue bodies.
- The run is local structural S2; no original respondent/native data, no scientific or actor issuance, no protected write and no merge.
- The actual model is `opencode-go/deepseek-v4.1-flash`; reasoning effort was not exposed by the runtime and is not claimed as I3+/HIGH.
