# RABOCHII B19Q2 — AS4I ROUTE A ADAPTER FULL QUALIFICATION R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-as4i-route-a-adapter-qualification-q2-r1`

Exact starting HEAD:
`764cd0ecb39c6bf9663e42667b52cbcf5a7c5d79`

Qualification-only court. NO CODE EDITS.

PASS:
`AS4I_ROUTE_A_ADAPTER_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

Blocker:
`AS4I_ROUTE_A_ADAPTER_QUALIFICATION__EXACT_BLOCKER_PROVED`

Binding adjudication:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/43_B19R_B20IR_ADJUDICATION_AND_Q2_FULL_QUALIFICATION_AUTHORIZATION_R1.md`

Exact frozen inputs:
- Route-A implementation:
  `rawlsing_next/pre553_r5_source_backed_adapter.py`
  blob `d4915e7e6755ba1850756aebff72f982f73a332b`;
- repaired qualification test:
  `rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`
  blob `25e905868a21bb36035269065b7bc3640201b7d8`.

## Required execution

Run exactly:

`python -m pytest -q rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

twice in genuinely independent fresh Python processes with distinct temp/pycache state.

Each run must report:
- 8 collected;
- 8 passed;
- 0 failed;
- 0 errors;
- 0 skipped;
- 0 xfailed/xpassed masking.

Bind exact:
- Python version;
- pytest version;
- command;
- exit code;
- stdout/stderr SHA-256;
- implementation blob;
- test blob.

If either run fails:
- preserve exact failure;
- do NOT patch code;
- return blocker.

## Required outputs

Write only under:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B19Q2_AS4I_ROUTE_A_ADAPTER_QUALIFICATION_R1/`

Required:
- `00_RETURN.md`
- `01_INPUT_IDENTITY_RECEIPT.json`
- `02_RUN1_PYTEST_RECEIPT.json`
- `03_RUN2_PYTEST_RECEIPT.json`
- `04_CROSS_RUN_PARITY_RECEIPT.json`
- `05_COMMON_HARNESS_INTAKE_HANDOFF.json`
- `CHANGED_FILES.txt`

Hard stops:
- no code edits;
- no C09/WVS7;
- no benchmark/ranking;
- no common harness implementation;
- no OBL037 / architecture selection / positive V3.

Return to SUB-VOZHD B.
