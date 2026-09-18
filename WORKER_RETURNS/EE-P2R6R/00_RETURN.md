# EE-P2R6R — F02 SOURCE-SCAN VERIFIER CONTRACT REPAIR — GOVERNED RETURN

Disposition: **PASS**.

Terminal:

`EE_P2R6R_PASS__F02_FULL_SOURCE_SCAN_VERIFIER_CONTRACT_REPAIRED__R6B_VERIFIER_CHAIN_REFRESHED__EXISTING_R6L_OUTPUTS_READY_FOR_NO_CARRIER_REVERIFICATION`

Grain:

`R5B_F02_SOURCE_SCAN_VERIFIER_SCHEMA_COMPLETENESS_REPAIR__PLUS_R6B_PIN_REFRESH_ONLY`

## Authority and scope

Canonical HQ remained sealed at checkpoint:

`20260918T1642-0400`

immutable handoff:

`28e0af7fd90dd2ed90923ec3f8bd1aa0e4e1fed4`

through final qualification and return preparation.

Execution surface: **BROWSER**.

Library access: **NO**.

No Library files, carrier bytes, source bytes, empirical outcomes, or performance measurements were accessed. The LiTS carrier was not reopened and the source driver was not rerun.

## Static defect independently reproduced

Exact R5B driver Git blob:

`b819fdff50470a71f1c570aa8021e28b361fa986`

was preserved unchanged.

The driver obtains the q310/q311 summary through frozen F02 `scan_records(...)` and immediately calls frozen F02 `verify_real_source_summary(...)` before writing output.

Frozen F02 producer Git blob:

`7b45b277164fa90c3da739aab26b516f7a8cb8dc`

requires exact equality with the complete `REAL_SOURCE_SCAN`, including counts, row-semantic roots, and all four selector roots for q310 and q311.

Old R5B verifier Git blob:

`348c533a3dff477c3ea0c2f19b41a4e131ef3d3f`

omitted `selector_roots` from `EXPECTED_SCAN` while comparing the whole observed source-scan object to that truncated expectation.

Therefore the old verifier necessarily rejected an exact valid complete F02 source scan.

Classification:

`EXPECTED_SCAN_SCHEMA_TRUNCATION__SELECTOR_ROOTS_OMITTED_FROM_VERIFIER_EXPECTATION`

No independent driver or source-replay defect was proved.

## Repaired successor-release verifier

Path:

`WORKER_RETURNS/EE-P2R6R/02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py`

Git blob SHA-1:

`e7752c558c7fb407852ef7377f45eca775d3b86b`

The repaired file is the exact old R5B verifier with only the complete frozen `selector_roots` added to `EXPECTED_SCAN`. Whole-object equality remains the governing check, so missing fields, changed values, and unexpected keys all fail closed. Every non-scan R5B verification check remains byte-for-byte unchanged.

## Refreshed R6B chain

Refreshed issuer:

`WORKER_RETURNS/EE-P2R6R/03_REPAIRED_R6B_BINDING_ISSUER.py`

Git blob SHA-1:

`8fd59bc69cd549c39b81bef7d44bb96c1bc0b7c6`

It is the adopted R6B issuer with only the R5B verifier path/blob pin changed to the repaired verifier.

Refreshed binding verifier:

`WORKER_RETURNS/EE-P2R6R/04_REPAIRED_R6B_BINDING_VERIFIER.py`

Git blob SHA-1:

`94d4b6a500925b62fd016b57870083f4d41fc85d`

It is the adopted R6B binding verifier with only the issuer path/blob pin changed to the refreshed issuer.

Authority epoch is preserved exactly:

`30815cfb20f4f66140cee8f6a2b5e5cafd5e20fb4d1b0c607bad1e3699fae2ff`

No actual `ReleaseRealizationBinding` was emitted.

## Existing R6L output re-verification

Prepared packet:

`WORKER_RETURNS/EE-P2R6R/05_EXISTING_R6L_OUTPUT_REVERIFY_PACKET.json`

The future local act is verification-only:

- execution surface: **LOCAL-MACHINE CODEX**
- maximum intelligence: **LUNA**
- Library access: **NO**
- do not reopen `LITS-2006-data.dta`
- do not rerun the driver
- run the repaired verifier against the already-existing `successor_release_receipt.json`
- on PASS, hash and seal all four already-existing R6L JSON outputs
- write the governed R6L PASS return and local execution receipt
- commit and push
- on any later verification failure, stop exactly there.

Exact wake:

`HQ_ADOPT_R6R_REPAIR__THEN_LOCAL_MACHINE_CODEX_LUNA__LIBRARY_NO__RUN_REPAIRED_VERIFIER_AGAINST_EXISTING_R6L_SUCCESSOR_RELEASE_RECEIPT__ON_PASS_HASH_AND_SEAL_FOUR_EXISTING_JSON_OUTPUTS_AND_WRITE_GOVERNED_R6L_PASS__DO_NOT_REOPEN_LITS_2006_DATA_DTA__DO_NOT_RERUN_DRIVER`

## Governed Browser qualification

Final qualifying semantic candidate:

`81ee5b5aa60cc03d2948d27b0f7ace6989db7f1c`

Evidence execution:

`ee2001bcce84f71f22af9954c2c1bfd4fa237fd6`

Transient PR:

`#406` — closed unmerged.

PR synthetic SHA:

`793b0026d07dd12ccfd74798ea879989d98eb4a2`

Workflow/run/job:

`350748047 / 35393995830 / 105758519925`

Qualification:

- protocol self-test: **20/20 passed**
- bounded court: **42/42 passed**
- Python: **3.12.14**
- pytest: **9.1.1**

Artifact:

- ID: `10566572777`
- name: `rabochii-court-receipt-35393995830`
- size: `608` bytes
- digest: `sha256:6086a658a6073ff75336f493c2884859853ed4254adae2556f885aaa3670d5dd`

Qualification receipt:

`WORKER_RETURNS/EE-P2R6R/06_BROWSER_QUALIFICATION_RECEIPT.json`

Git blob SHA-1:

`b5ad8b903b6a8a37d09a1770636e4cedeadd30fa`

The court proved the exact complete frozen scan matches the repaired expectation; missing selector roots, one changed selector root, one changed count, one changed row root, and an unexpected source-scan key fail exact equality; the old truncated expectation rejects the exact valid full scan; all other R5B checks are preserved; the refreshed issuer/verifier pin chain is exact; authority epoch is preserved; and no actual binding is emitted.

Two earlier qualification-only attempts are preserved as non-authoritative audit history in the qualification receipt: PR #404 failed court-spec path validation before bounded tests ran; PR #405 reached bounded tests and exposed a Git-blob helper bug in the qualification test itself. Neither changed product bytes. Both were closed unmerged and superseded by the green R3 court.

## Hard-scope audit

Not performed:

- Library or carrier access
- source-driver execution or rerun
- source-scan weakening
- selector remint
- D02/F02 workload mutation
- concrete realization binding issuance
- P2X or BE1 execution
- Candidate-C repair
- Lock1/Lock2 mutation
- MAIN or semantic PRE-MAIN modification
- rebase or replacement branch.

All net repository changes from the commissioned head are confined to:

`WORKER_RETURNS/EE-P2R6R/`

## Successor wake

PASS wakes **HQ adjudication only**:

`HQ_ADJUDICATE_REPAIRED_VERIFIER_AND_AUTHORIZE_NO_CARRIER_R6L_REVERIFICATION`

R6L carrier execution remains forbidden. Existing outputs are ready for no-carrier verification after HQ adopts this repair.
