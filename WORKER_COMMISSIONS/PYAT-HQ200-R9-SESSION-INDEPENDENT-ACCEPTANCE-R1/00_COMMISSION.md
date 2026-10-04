# PYAT HQ200 — governed source-session independent acceptance — R1

Repository: maidiu/rawlsing

Role: independent source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq200-r1

Review target clean tip:
76970cfdfc8968e975595ea288cf44b448205e30

Code-bearing session candidate:
90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ200-R9-SESSION-INDEPENDENT-ACCEPTANCE-R1/
- /WORKER_RETURNS/PYAT-HQ200-R9-SESSION-INDEPENDENT-ACCEPTANCE-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Read HQ200 adjudication by exact Git object:
e7ce39dade6b169ab068f5f786b7a0dea06846dd:
PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ200_R9_SESSION_PLAN_ADJUDICATION_R1.md

Do not clone. Do not create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Mission

Independently attack the HQ199 governed source-session candidate.

Do not review the parallel HQ200 implementation branch.

Verify or falsify:

1. GovernedSourceSession is genuinely above one decoder call and owns one broker lifecycle for a caller-bound source entry.
2. decoder_invocations is a separate account and budget, not reader_invocations under another name.
3. max decoder_invocations=1 refuses a second entry before ANY source operation on the second entry.
4. On that refusal, all relevant source accounts remain unchanged.
5. METADATA_ONLY + non-null encoding performs metadata admission and zero selected/full/chunk row-data operations.
6. SELECTED performs metadata + selected and zero full.
7. FULL performs metadata + full and zero chunk.
8. CHUNKED_FULL performs metadata + chunk reads and zero full.
9. header_prefix_bytes=None gives zero prefix operations.
10. explicit 176 gives exactly one 176-byte prefix operation.
11. session receipt is live after later chunk activity.
12. session close is deterministic/idempotent on success and error.
13. no source-specific SRCxx policy is hard-coded in production.
14. no raw source path reaches pyreadstat on the governed session path.
15. accepted broker byte-limit behavior remains intact.

## Count semantics ceiling

Use HQ200's adjudication exactly:

For SRC27:
- full_route_passes = EXACT/MAX 1 — frozen.
- full_reads = FLOOR >=1, ceiling historically UNBOUND.
- decoder_invocations historical expected count = UNBOUND.
- decoder MAX 1 may be an implementation-policy ceiling.
- path_opens historical numeric value = UNBOUND.
- the one-open broker is compatible.

Do NOT adopt the earlier statement that frozen authority itself requires exactly one full read or exactly one decoder invocation.

## Exact R7 court

Use:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<review worktree root>

pytest:
-p no:cacheprovider

Exact six files:
- rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
- rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py
- rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py
- rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
- rawlsing_next/tests/test_r35_i01_physical_metadata.py
- rawlsing_next/tests/test_pre553_source_backed_c11_facade.py

Collect exactly 55, then run twice. Target 55/55 twice.
Record all exit codes. Do not retry away failures.

Also run:
- session court;
- broker court;
- targeted independent source-free exercises for the criteria above.

## Architectural boundary

The candidate is generic and may permit multiple plan runs when its budget does not forbid them.

That is not automatically a defect: the warrant-binding layer may supply max decoder_invocations=1.

Determine whether the generic owner is sufficient as a mechanism for a stricter bound execution layer, or whether a structural defect remains in the owner itself.

## Allowed dispositions

Exactly one:
- ACCEPT_GOVERNED_SOURCE_SESSION_MECHANISM__WARRANT_BINDING_LAYER_NEXT
- SESSION_MECHANISM_MATERIAL_DEFECT
- R7_REQUALIFICATION_FAILURE
- SESSION_OWNER_SCOPE_STILL_INSUFFICIENT

## Return

At minimum:
- 00_REVIEW.md
- 01_SESSION_LIFECYCLE_REVIEW.json
- 02_DECODER_ACCOUNT_REVIEW.json
- 03_PLAN_MODE_REVIEW.json
- 04_R7_AND_COURTS.json
- 05_GENERIC_OWNER_BOUNDARY.json
- 06_FINAL_DISPOSITION.json

Commit, push, re-fetch, verify local == remote.

Terminal:
HQ200_R9_SESSION_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED

No real source access, locator discovery, warrant issuance, live C4, production mutation, C7 or actor/person work.
