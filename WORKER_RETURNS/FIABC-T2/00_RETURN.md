# FIABC-T2 — Candidate-C / Six-Cell Execution Binding

Branch: `agent/rabochii-premain-fiabc-t2-candidate-c-six-cell-binding-r1`

Base / exact FIABC-T1 live-transposition tip:

`86daba6838d72c70b1452db4178c338185e6e377`

Implementation tip before this return packet:

`b1697105c80294341fc8c6fee91e0caef3d6e9b6`

## Disposition

PASS — bounded current-contract implementation complete.

No measured P2X was run. No merge was performed.

## Current six-cell contract

The live P2X execution line now carries a separate current execution manifest:

`WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json`

It admits exactly:

- LiTS-I × A
- LiTS-I × B
- LiTS-I × C
- WVS7 × A
- WVS7 × B
- WVS7 × C

The historical continuation map was not edited. Its exact frozen identity remains recorded in the new manifest as `IMMUTABLE_HISTORY_ONLY__NOT_CURRENT_CAPABILITY_LAW`.

The live driver now consumes the current six-cell manifest through `load_current_execution_manifest(...)`. The old historical loader remains present only for historical compatibility/audit and is no longer the current CLI execution contract.

## Candidate C live binding

Candidate C remains:

`SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS`

The accepted Wave-3 Candidate-C production binder was transposed byte-for-byte into the live lineage.

For current LiTS-I F02:

- CACC1/CACC2 remain the only permitted accelerator identities;
- neither is asserted fully applicable to the exact current F02 workload;
- q310/q311 and all uncovered exact material are retained and execute through exact source-backed fallback;
- no CACC3 exists or is admitted;
- exact source-backed realization remains Candidate C and does not substitute Candidate-B identity.

For WVS7:

- accelerator inventory is exactly empty;
- execution is exact source-backed;
- no WVS-specific CACC exists or is admitted;
- Candidate C remains Candidate C.

The live backend retains Candidate-C physical/provenance evidence beside the common repository-builder binding receipt.

## Source-root equality

Canonical roots are fixed court-wide:

- LiTS-I: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- WVS7: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

All A/B/C realizations for one source must close to that same root.

For preserved/prebuilt R5 carriers, the backend now validates the embedded `source_artifact_ref` before allowing the derivative to stand in for reopening raw source bytes. The current manifest separately requires lawful preserved-work accounting classification before any numeric credit can attach to such a derivative.

No alternate edition, export, cleaned source, or source substitution is admitted.

## Historical failures

The historical LiTS-C and WVS-C failure receipts remain immutable evidence, including:

- `WORKER_RETURNS/EE-P2X/05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json`
- `WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json`

The historical continuation map remains frozen at SHA-256:

`ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`

Those artifacts no longer function as current Candidate-C capability law.

## Live code changes

- `rawlsing_next/ee_p2x_darwin_court_driver.py`
  - adds current-manifest validation;
  - requires exactly six executable cells;
  - binds source-root equality and historical/current separation;
  - current S17 readiness requires terminal PASS for all six cells.
- `rawlsing_next/ee_p2x_darwin_stage_backend.py`
  - removes the historical LiTS-C q310/q311 hard stop;
  - removes the historical WVS-C no-path hard stop;
  - binds current Candidate C through the accepted source-backed production binder;
  - validates R5 canonical-source provenance.
- `rawlsing_next/pre553_candidate_c_production_binding.py`
  - transposed unchanged from accepted Wave-3 I03.
- focused Candidate-C and T2 current-contract tests are present.

T1's stable runtime packaging assets were not altered.

## Qualification boundary

Source-independent qualification commands are recorded in `04_TEST_COMMANDS.md`.

They were not executed on this GitHub/browser worker surface. No test result is fabricated. Real-source execution and measured P2X were not performed.

Terminal:

`FIABC_T2_CURRENT_SIX_CELL_EXECUTION_CONTRACT_IMPLEMENTED__READY_FOR_NEXT_LAYER`
