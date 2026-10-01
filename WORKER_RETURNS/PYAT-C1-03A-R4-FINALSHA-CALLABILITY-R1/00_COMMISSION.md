# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — R4 FINAL-SHA CALLABILITY CORRECTION — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq156-c1-03a-r4-finalsha-callability-r1`

Exact base / returned R4:
`3bd481163ac1b2b1e30817b2704e89341099a960`

R4 worker disposition:
`PASS_C1_03A_REFUSAL_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

HQ intake found a direct final-SHA defect:

`OwnerStateProjection.from_empirical_integrity_refusal`

is decorated with **two consecutive `@classmethod` decorators**.

In Python, that produces a bound method whose wrapped object is itself a `classmethod`, so calling it raises:

`TypeError: 'classmethod' object is not callable`.

This contradicts the returned claim that the exact final SHA passed 208 tests including genuine integrity-refusal projection.

## Mission

Perform the smallest possible final-SHA correction.

Required:
1. remove exactly the duplicate `@classmethod` decorator so the method has one;
2. do not change refusal semantics, witness semantics, provenance, route law, AT15, AT16, or any owner module;
3. add/retain an explicit hostile that directly calls:
   `OwnerStateProjection.from_empirical_integrity_refusal(witness=<genuine witness>)`
   and proves it returns `INTEGRITY_FAILURE`;
4. directly call the blocked-authority sibling too and prove `BLOCKED_REQUIRED_AUTHORITY`;
5. rerun the exact ten-file R4 court on the **final commit** and report exact counts;
6. verify the final commit itself (after all return-packet edits) still passes the court;
7. return the exact final SHA and branch head.

Do not rewrite or broaden anything else.

## Write terrain

Only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py` only if an explicit final-SHA callability court is needed;
- `WORKER_RETURNS/PYAT-C1-03A-R4-FINALSHA-CALLABILITY-R1/**`

Do not modify fixture unless absolutely necessary. Do not modify any owner module.

## Return

Required:
- `00_RETURN.md`
- `01_FINAL_SHA_CALLABILITY_RECEIPT.json`
- `02_EXECUTION_RECEIPT.json`
- `03_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03A_R4_FINALSHA_CALLABILITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `UNEXPECTED_BROADER_DEFECT__HQ_ADJUDICATION_REQUIRED`

No merge/self-adoption.

Terminal:
`C1_03A_R4_FINALSHA_CALLABILITY_RETURNED__HQ_ADJUDICATION_REQUIRED`
