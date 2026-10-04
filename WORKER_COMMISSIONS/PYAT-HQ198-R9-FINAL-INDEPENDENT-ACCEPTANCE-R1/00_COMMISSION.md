# PYAT HQ198 — R9 repaired-candidate final independent acceptance — R1

Repository: maidiu/rawlsing

Role: independent source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq198-r1

Review target branch tip:
4b6335ca5fc485108b0ffb1d682a29a02e1eee51

Code-bearing repair commit:
a483cb6619a84c4785296e923a8571447041ffa5

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ198-R9-FINAL-INDEPENDENT-ACCEPTANCE-R1/
- /WORKER_RETURNS/PYAT-HQ198-R9-FINAL-INDEPENDENT-ACCEPTANCE-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Do not clone the repository. Do not create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Independence order

Before reading the HQ197 physical-selected worker return at:
d43c7f8647a28da13e05bdd264722d1d87b2cb29

independently reconstruct the meaning of:
- BOUNDED_FRESH_PHYSICAL_SELECTED_VARIABLE_READ
- BOUNDED_FRESH_PHYSICAL_READ_EXACT_VARIABLE
- selected_reads
- full_reads

from the exact C4B/C4/C3 authority chain.

Write your pre-comparison interpretation into the return packet first.
Only then read the worker's interpretation and compare.

## Candidate acceptance

Review the repaired candidate, not the pre-repair d5ce candidate.

Verify:
1. one application-owned source path open per governed C4 decoder scope;
2. no source path string reaches pyreadstat inside the accepted C4 closure;
3. DTA fresh-view/reset semantics are correct;
4. pyreadstat 1.3.6/file-object seam remains pinned and R7 interpreter/package identity is unchanged;
5. reader_bytes is now genuinely enforced:
   - no byte beyond the cap is consumed;
   - exactly-enough succeeds;
   - one-byte-short fails;
   - the file-object callback never raises as the limit mechanism;
   - failure is prompt and typed at the outer boundary;
   - reader byte accounting excludes application hash/header bytes;
6. selected-read mode remains honest about non-suppression of underlying bytes;
7. no unrelated production movement exists between d5ce and the repaired clean tip.

## Exact R7 qualification court

Use:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<review sparse worktree root>

pytest flag:
-p no:cacheprovider

Exact files:
- rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
- rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py
- rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py
- rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
- rawlsing_next/tests/test_r35_i01_physical_metadata.py
- rawlsing_next/tests/test_pre553_source_backed_c11_facade.py

Collect first: exactly 55 tests.
Run twice: target 55 passed / 55 passed.
Record every exit code. Do not retry away failures.

No symlink to the canonical WORKER_RETURNS tree is needed; the required fixture directories are in the sparse manifest.

## Candidate-specific courts

Run the broker/source-access court and independently exercise:
- reader-byte caps;
- DTA reset/view behavior;
- selected/full counters;
- selected-column negative cases;
- version pin;
- raw-path rejection.

The prior test-coverage advisory about chunk size is not itself blocking. Independently verify chunk_rows is honored on a carrier larger than one chunk and record the result.

## Physical-selected authority question

Determine independently whether the frozen term means:

A. PHYSICAL identifies the physical source/witness tier while SELECTED_VARIABLE_READ identifies the configured reader/output scope; or

B. it requires byte-level suppression of unselected-column data; or

C. another meaning / genuine ambiguity.

Use exact historical authority. Do not choose based on implementation convenience.

After recording your independent determination, compare with:
d43c7f8647a28da13e05bdd264722d1d87b2cb29

## Allowed dispositions

Exactly one:
- ACCEPT_REPAIRED_BROKER_CANDIDATE__PHYSICAL_SELECTED_A_CONFIRMED
- ACCEPT_REPAIRED_BROKER_CANDIDATE__PHYSICAL_SELECTED_AUTHORITY_STILL_OPEN
- REPAIRED_CANDIDATE_MATERIAL_DEFECT
- R7_REQUALIFICATION_FAILURE
- MATERIAL_AUTHORITY_CONFLICT

## Return packet

At minimum:
- 00_REVIEW.md
- 01_PRECOMPARISON_PHYSICAL_SELECTED_INTERPRETATION.json
- 02_REPAIRED_BYTE_LIMIT_REVIEW.json
- 03_R7_55_TEST_COURT.json
- 04_C4_CLOSURE_AND_BROKER_REVIEW.json
- 05_POSTCOMPARISON_AUTHORITY_REVIEW.json
- 06_FINAL_DISPOSITION.json

Commit, push, re-fetch, verify local == remote.

Terminal:
HQ198_R9_FINAL_INDEPENDENT_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED

No real survey-source access, locator discovery, warrant issuance, live C4, C7, or actor/person work.
