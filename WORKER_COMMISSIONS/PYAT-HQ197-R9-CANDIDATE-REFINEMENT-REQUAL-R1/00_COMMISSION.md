# PYAT HQ197 — R9 candidate refinement and exact requalification — R1

Repository: maidiu/rawlsing

Role: source-free implementation worker — Space Bunny

Branch:
agent/rabochii-pyat-hq197-r1

Implementation base:
d5ce4ecff6acc25d199577a7859de7e98514e9fd

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ197-R9-CANDIDATE-REFINEMENT-REQUAL-R1/
- /WORKER_RETURNS/PYAT-HQ197-R9-CANDIDATE-REFINEMENT-REQUAL-R1/
- /rawlsing_next/

Do not clone the repository. Do not convert to a full checkout.

## Mission

Refine the existing candidate only where HQ197 identified a concrete gap, then run the actual accepted R7 qualification court.

### 1. reader_bytes limit

The current candidate declares SourceAccessBudget.reader_bytes but does not check that limit inside the governed read path before bytes are consumed.

Implement a deterministic bridge-safe byte limit.

Requirements:
- never read a byte beyond the declared limit;
- do not raise through pyreadstat's file-object read callback if that behavior can hang;
- a limit reached before the reader is complete must fail promptly and loudly at the outer decode boundary;
- account the exact bytes actually read;
- add negative tests proving bytes_read never exceeds the limit;
- distinguish allowed partial final read from an excess read.

Do not change pyreadstat or the R7 environment.

### 2. preserve honest selected-route disclosure

Do not claim pyreadstat physically suppresses unselected-column bytes.
Keep selected/full operation counters and the physical-I/O disclosure separate.

Do not resolve the authority meaning of PHYSICAL_SELECTED_VARIABLE_READ in this lane.

### 3. exact R7 six-file court

Use:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<candidate sparse worktree root>

Use pytest -p no:cacheprovider.

Exact files:
- rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
- rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py
- rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py
- rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
- rawlsing_next/tests/test_r35_i01_physical_metadata.py
- rawlsing_next/tests/test_pre553_source_backed_c11_facade.py

First run collect-only. Exact denominator must be 55.
Then run the six-file court twice.
Record every exit code and duration.
Do not retry away a failure.

### 4. candidate-specific courts

Run the broker/source-access court after the refinement and include:
- one physical path open per governed scope;
- zero source path strings passed to pyreadstat on the C4 decoder route;
- DTA view/reset behavior;
- byte-limit negative cases;
- selected/full counters;
- missing/unexpected selected-column failures;
- version/seam pin.

### 5. exact C4 closure audit

Use the accepted 23-module closure from the R7 return.
Verify there is no pyreadstat reader call receiving a source path string inside that closure.

The WVS7 projection materializer is outside that closure. Do not edit it.

## Write terrain

Only:
- rawlsing_next/pre553_source_access_broker.py
- rawlsing_next/pre553_physical_decoder.py if strictly required
- rawlsing_next/tests/**
- WORKER_RETURNS/PYAT-HQ197-R9-CANDIDATE-REFINEMENT-REQUAL-R1/**

No other production files.

## Allowed dispositions

- CANDIDATE_REQUALIFIED__PENDING_SELECTED_AUTHORITY_AND_INDEPENDENT_ACCEPTANCE
- BYTE_LIMIT_REPAIR_INCOMPLETE
- R7_SIX_FILE_COURT_FAILURE
- MATERIAL_NEW_COUNTEREXAMPLE
- CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED

No self-adoption.

## Return

Commit, push, re-fetch, verify.

Terminal:
HQ197_R9_CANDIDATE_REFINEMENT_RETURNED__HQ_REVIEW_REQUIRED

No real survey-source access, locator work, warrant issuance, live C4, C7, or actor/person work.
