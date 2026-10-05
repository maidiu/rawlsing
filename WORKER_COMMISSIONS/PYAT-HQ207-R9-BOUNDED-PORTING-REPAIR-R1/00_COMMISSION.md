# PYAT HQ207 — R9 bounded porting repair — R1

Repository: maidiu/rawlsing
Role: bounded source-free repair worker — Space Bunny High

Branch:
agent/rabochii-pyat-hq207-r9-repair-r1

Exact repair base:
dfdf5659fd78e9bc996b07383349094059a5553d

Independent adjudication:
7a5cf25ab3fb98fe5311e0a394b4432a498f6546

HQ207 adjudication:
cfe648bd462ddf6fc1252182c5e784ec43bf4405

Checkout:
SPARSE_REQUIRED

## Mission

Perform ONLY the bounded repair authorized by HQ207.

Do not modify accepted R9 production runtime blobs.

### Repair 1 — SR06 test port

Adopt the accepted-lineage test blob:

rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py
blob:
dfd063227e4a0897

paired with accepted decoder:
b406d45fae419c02

This is a test port, not a test retirement.

Preserve the still-binding invariants:
- source identity is hashed before reader decode;
- normal decode follows the accepted chunked route;
- compatibility route follows the accepted full-read route.

The stale read_file_in_chunks helper assertion may be replaced by the accepted revision.

Do not modify the decoder to satisfy the old seam name.

### Repair 2 — R7 gate attribution

Update the fan-in return/gate receipts so they state truthfully:

- the canonical 55-test six-file R7 denominator is qualification of the accepted C4C3 lineage;
- it is NOT a current-control obligation;
- current-control fan-in acceptance uses:
  1. current-control sanctioned court set;
  2. the reachable R7 subset present on current control;
  3. the accepted R9 focused courts.

Do NOT import missing C3 production modules/courts merely to manufacture 55 collected on control.

### Repair 3 — governed environment rerun

Use exactly:

/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

and preserve the pyreadstat 1.3.6 pin.

Re-run:
- execution-binding court: 34 expected;
- source-session court: 15 expected;
- broker court: 20 expected;
- current-control reachable R7 subset: 25 expected;
- updated SR06 test.

Record exact package versions and interpreter path.

Also rerun the same current-control regression slice that previously exposed the two SR06 failures and prove the two regressions are gone without new failures.

## Prohibitions

No decoder changes.
No production C3 backport.
No test retirement.
No environment reconstitution.
No raw source access.
No warrant.
No live C4.
No C7.
No actor/person work.
No self-adoption.

## Output

00_RETURN.md
01_SR06_PORT_RECEIPT.json
02_R7_GATE_ATTRIBUTION.json
03_GOVERNED_ENVIRONMENT_COURT_RECEIPT.json
04_REGRESSION_RECEIPT.json
05_FINAL_DISPOSITION.json

Allowed:
- R9_BOUNDED_PORTING_REPAIR_COMPLETE__READY_FOR_FINAL_ACCEPTANCE
- R9_BOUNDED_REPAIR_INCOMPLETE__NAMED_DEFECT
- R9_GOVERNED_ENVIRONMENT_QUALIFICATION_FAILURE
- MATERIAL_NEW_COUNTEREXAMPLE

Commit, push, re-fetch, verify.

Terminal:
HQ207_R9_BOUNDED_PORTING_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED
