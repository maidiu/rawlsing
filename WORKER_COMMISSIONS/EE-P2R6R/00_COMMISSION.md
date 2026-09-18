# EE-P2R6R — F02 SOURCE-SCAN VERIFIER CONTRACT REPAIR

Repository: `maidiu/rawlsing`

## Execution surface

**BROWSER**

## Library access

**NO**

Do not access Library files, LiTS/WVS carriers, source bytes, empirical outcomes, or performance measurements.

Exact branch:

`agent/rabochii-prev3-ee-p2r6r-source-scan-verifier-contract-repair-r1`

Exact base:

`a2122c1d06f9ff7aa52ddcbc18f813200ceb314f`

Before any work, resolve live canonical HQ through `HQ_HANDOFF/LATEST.json` and verify its immutable checkpoint packet.

## Trigger

Local EE-P2R6L performed the exact authorized R5B driver/verifier path and stopped at first failure with:

`EE_P2R6L_BLOCK__F02_SOURCE_SCAN_ROOTS_COUNTS_MISMATCH`

No repair, rerun, carrier mutation, or branch mutation occurred.

The four generated JSON outputs remain locally present but uncommitted.

HQ independently confirmed a deterministic repository-level verifier-contract defect:

1. R5B driver blob  
   `b819fdff50470a71f1c570aa8021e28b361fa986`
   computes:
   `source_scan = f02_module.scan_records(...)`
   and immediately requires:
   `f02_module.verify_real_source_summary(source_scan)`.

2. Frozen F02 selector producer blob  
   `7b45b277164fa90c3da739aab26b516f7a8cb8dc`
   defines each exact source-scan entry as:
   - `counts`
   - `row_semantic_root_sha256`
   - complete `selector_roots` for `1,2,3,MISSING`

   and `verify_real_source_summary` requires exact equality with that full structure.

3. R5B verifier blob  
   `348c533a3dff477c3ea0c2f19b41a4e131ef3d3f`
   defines `EXPECTED_SCAN` with only:
   - `counts`
   - `row_semantic_root_sha256`

   then executes:

   `if scan.get("source_scan") != EXPECTED_SCAN: fail("F02 source scan roots/counts mismatch")`

Therefore any correctly emitted full frozen F02 source scan necessarily fails the R5B verifier because the verifier truncated the expected schema by omitting `selector_roots`.

This commission must independently re-prove that diagnosis before repair.

## Exact grain

`R5B_F02_SOURCE_SCAN_VERIFIER_SCHEMA_COMPLETENESS_REPAIR__PLUS_R6B_PIN_REFRESH_ONLY`

This is a verifier/receipt-contract repair.

It is not source execution and not semantic redesign.

## Controlling exact source-scan authority

Frozen F02 exact expected source replay:

### q310

Counts:

- 1: 12340
- 2: 7511
- 3: 9085
- MISSING: 66

Row semantic root:

`a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`

Selector roots:

- 1: `0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2`
- 2: `0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83`
- 3: `b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d`
- MISSING: `810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348`

### q311

Counts:

- 1: 16582
- 2: 4548
- 3: 7826
- MISSING: 46

Row semantic root:

`af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`

Selector roots:

- 1: `bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869`
- 2: `43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f`
- 3: `642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837`
- MISSING: `847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb`

These identities come from the frozen F02 producer and may not be recomputed from invented data.

## Mission

Repair the verifier contract so the exact full F02 source-scan object emitted and already prevalidated by the R5B driver is verified against the exact frozen F02 source-scan authority **without weakening any check**.

Then refresh the R6B post-local issuer/verifier chain so it pins and invokes the repaired exact R5B successor-release verifier.

The repair must support re-verification of the already-produced R6L output JSONs without rerunning the LiTS carrier.

## Required repair law

### A. Diagnose first

Prove exactly whether the failure is:

`EXPECTED_SCAN_SCHEMA_TRUNCATION__SELECTOR_ROOTS_OMITTED_FROM_VERIFIER_EXPECTATION`

If not, BLOCK with the smallest exact alternative defect.

### B. Corrected source-scan verification

The repaired verifier must require the **full** exact frozen F02 source-scan structure.

Preferred law:

`observed_source_scan == exact frozen REAL_SOURCE_SCAN`

including:

- exact counts;
- exact row semantic root;
- exact four selector roots for each q310/q311.

Do not "fix" by ignoring extra fields.

Do not compare only a subset.

Do not permit unknown keys.

Do not derive expected values from the receipt itself.

The repair should strengthen the verifier to the full already-governed F02 contract.

### C. No driver change unless strictly necessary

The R5B driver already calls `verify_real_source_summary` before writing outputs.

Do not modify the driver unless repository proof shows a separate deterministic defect.

If the only defect is verifier truncation, preserve driver blob:

`b819fdff50470a71f1c570aa8021e28b361fa986`

exactly.

### D. Existing-output re-verification support

Prepare an exact verification-only packet for the already-existing R6L outputs.

That packet must require **no carrier access and no driver rerun**.

Future local action should be only:

1. run repaired verifier against existing `successor_release_receipt.json`;
2. if PASS, hash/seal all four existing output JSONs;
3. create governed R6L PASS return/receipt;
4. commit and push;
5. no source reopening.

If repaired verification fails at a later check, stop there. Do not rerun carrier or repair locally.

### E. Refresh R6B chain

Current adopted R6B issuer blob:

`c83058ec51ef731166bde06465a3b72c022c9c47`

pins the old R5B verifier blob:

`348c533a3dff477c3ea0c2f19b41a4e131ef3d3f`

and current R6B binding verifier blob:

`641f1e50af416441cba7650956123aa1d32f9b59`

pins the issuer.

Produce successor copies under this repair lane that:

- pin the repaired R5B verifier blob;
- preserve all R6B binding semantics and authority epoch;
- introduce no other behavioral change;
- remain inactive candidate issuers pending exact R6L receipts and HQ adoption.

Do not mutate historical R6B return artifacts in place.

### F. Regression / hostile checks

Prove at minimum:

- exact full frozen scan passes;
- scan missing selector_roots fails;
- one changed selector root fails;
- one changed count fails;
- one changed row root fails;
- unexpected extra scan key fails;
- old truncated expectation is demonstrated to reject exact valid full scan;
- repaired verifier preserves every non-scan R5B check;
- repaired R6B issuer invokes/pins repaired verifier;
- repaired R6B verifier pins repaired issuer;
- no actual realization binding emitted.

## Library / empirical boundary

Library: **NO**

No real source bytes.

No generated surrogate empirical evidence.

Structural fixtures may reproduce the already-governed exact scan object only for verifier qualification.

## Required outputs

Write only under:

`WORKER_RETURNS/EE-P2R6R/`

At minimum:

1. `00_RETURN.md`
2. `01_STATIC_DEFECT_PROOF.json`
3. `02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py`
4. `03_REPAIRED_R6B_BINDING_ISSUER.py`
5. `04_REPAIRED_R6B_BINDING_VERIFIER.py`
6. `05_EXISTING_R6L_OUTPUT_REVERIFY_PACKET.json`
7. `06_BROWSER_QUALIFICATION_RECEIPT.json`

If needed, vendor exact immutable support under `WORKER_RETURNS/EE-P2R6R/SUPPORT/`.

## PASS terminal

`EE_P2R6R_PASS__F02_FULL_SOURCE_SCAN_VERIFIER_CONTRACT_REPAIRED__R6B_VERIFIER_CHAIN_REFRESHED__EXISTING_R6L_OUTPUTS_READY_FOR_NO_CARRIER_REVERIFICATION`

PASS wakes HQ adjudication only.

## BLOCK terminal

Use the smallest exact proved blocker if the mismatch is not solely the verifier-contract truncation or if repaired verification cannot be defined from already-adopted authority.

## Hard forbidden

- no Library/carrier/source access;
- no driver rerun;
- no driver semantic mutation unless a separate exact defect is proved;
- no source-scan weakening;
- no invented expected roots/counts;
- no actual realization binding;
- no P2X/BE1;
- no Candidate-C repair;
- no selector remint;
- no D02/F02 workload mutation;
- no Lock1/Lock2;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch.

Run the governed Browser qualification court.

Commit and push the governed return on this exact branch.

Report PASS/BLOCK, final tip, repaired verifier/issuer blobs, qualification run/job/artifact identities, and exact no-carrier local re-verification wake.

Return to HQ.
