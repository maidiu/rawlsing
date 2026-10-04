# PYAT HQ197 — R9 candidate independent review — R1

Repository: maidiu/rawlsing

Role: independent source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq197-r9-broker-candidate-hostile-r1

Target candidate:
d5ce4ecff6acc25d199577a7859de7e98514e9fd

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ197-R9-CANDIDATE-INDEPENDENT-REVIEW-R1/
- /WORKER_RETURNS/PYAT-HQ197-R9-CANDIDATE-INDEPENDENT-REVIEW-R1/
- /rawlsing_next/

Do not clone the repository. Do not convert to a full checkout.

## Mission

Review the actual HQ196 candidate independently.

1. Confirm the governed decoder route performs one application-owned source-path open and passes file-like objects, not source path strings, to pyreadstat.
2. Confirm the file-object route remains on pyreadstat 1.3.6 and leaves the accepted interpreter/package identity unchanged.
3. Confirm DTA repeated reads use correct position-zero view/reset behavior over the same physical open.
4. Inspect SourceAccessBudget.reader_bytes. Determine whether the candidate really prevents bytes beyond the declared limit from being read. The review must distinguish a declared field from an enforced limit.
5. Reproduce the known pyreadstat callback behavior: an exception raised from the file-object read callback may not be a safe limit mechanism. Do not approve that mechanism unless it returns promptly and deterministically.
6. Measure selected-variable mode with and without usecols. Record returned columns and underlying read-call/byte counts. Do not decide the authority meaning of the word PHYSICAL; a separate lane owns that question.
7. Compare the two modified pre-existing tests against the exact freeze and judge whether their original guarantee was preserved.
8. Using the accepted 23-module C4 closure, verify there is no remaining pyreadstat call inside that closure that receives a source path string. The WVS7 projection materializer is outside this C4 closure and is not a blocker here.

## Exact R7 six-file court

Use:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<candidate sparse worktree root>

Use pytest with -p no:cacheprovider.

Exact files:
- rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
- rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py
- rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py
- rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
- rawlsing_next/tests/test_r35_i01_physical_metadata.py
- rawlsing_next/tests/test_pre553_source_backed_c11_facade.py

Run collect-only first. It must collect exactly 55 tests.
Then run the exact six files twice.
Record all exit codes. Do not hide or retry test failures.

## Allowed dispositions

- BROKER_CANDIDATE_PARTIAL__BYTE_CAP_REPAIR_REQUIRED
- BROKER_CANDIDATE_ACCEPTABLE_PENDING_SELECTED_AUTHORITY
- MATERIAL_COUNTEREXAMPLE__CANDIDATE_UNSOUND
- R7_REQUALIFICATION_FAILURE__CANDIDATE_NOT_ACCEPTABLE

## Return

Write only:
WORKER_RETURNS/PYAT-HQ197-R9-CANDIDATE-INDEPENDENT-REVIEW-R1/**

Commit, push, re-fetch, verify local == remote.

Terminal:
HQ197_R9_CANDIDATE_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED

No real survey-source access, locator work, warrant issuance, live C4, C7, or actor/person work.
