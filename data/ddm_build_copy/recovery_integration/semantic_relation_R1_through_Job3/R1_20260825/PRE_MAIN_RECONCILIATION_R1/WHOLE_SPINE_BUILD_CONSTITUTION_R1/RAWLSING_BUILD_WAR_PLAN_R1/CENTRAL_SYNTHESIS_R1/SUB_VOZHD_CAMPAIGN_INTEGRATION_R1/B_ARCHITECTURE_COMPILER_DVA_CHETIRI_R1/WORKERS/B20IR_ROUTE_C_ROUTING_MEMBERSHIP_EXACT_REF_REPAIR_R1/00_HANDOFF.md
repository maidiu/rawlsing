# RABOCHII B20IR — ROUTE C ROUTING-MEMBERSHIP EXACT-REF IMPLEMENTATION REPAIR R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-as4i-route-c-routing-membership-exact-ref-repair-r1`

Exact starting HEAD:
`0ec9db44496563f6b18a063b66b3a8644df7aac6`

PASS terminal:
`B20_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

Blocker terminal:
`B20_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_NORMALIZATION_REPAIR__EXACT_BLOCKER_PROVED`

Implementation-repair mission limited to one function.

## Frozen repaired qualification driver

Use the repaired B20 qualification driver already banked by B20R.

Do NOT modify it.

## Exact implementation defect

File:

`rawlsing_next/pre553_route_c_accelerators.py`

Function:

`_routing_membership()`

Canonical semantic object fields are mapping-form refs at runtime.

Current function uses:
- `fact.scoped_respondent_ref`
- `fact.question_or_target_ref`
as a tuple dict key;
and later:
- `fact.risk_set_ref`
as set material.

Mapping-form refs are unhashable.

## Authorized normalization

Within `_routing_membership()` ONLY, use repo-native:

`exact_ref(...)`

Normalize:
- scoped respondent ref;
- question/target ref;
- risk-set ref.

Required behavior:

`pair = (exact_ref(fact.scoped_respondent_ref, "..."), exact_ref(fact.question_or_target_ref, "..."))`

and common-risk ref collection from exact-ref-normalized `fact.risk_set_ref`.

Preserve all existing exact-equality/routing-state/common-risk logic.

Do not:
- stringify refs;
- compare only object_id;
- compare only hash;
- mutate routing facts;
- change qref construction;
- change CACC1 layout;
- change CACC2;
- change query/discovery semantics;
- change accepted routing-state conditions.

## Commit-before-smoke

Commit implementation repair before validation.

Record:
- pre/post implementation blob/SHA;
- exact diff;
- repaired commit.

Smoke from real checkout under:
- CPython compatible with prior court;
- `pyarrow==25.0.1`;
- pandas as required.

Minimum smoke boundary:
- repaired driver fixture completes;
- `_routing_membership()` completes;
- first CACC1 build completes.

If a new independent defect appears after this boundary:
- preserve exact failure;
- stop;
- do not patch outside this same normalization class.

B20IR may NOT claim full Route-C qualification.

A separate B20Q2 must run the full court.

## Outputs

Write only under:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B20IR_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_REPAIR_R1/`

Required:
- `00_RETURN.md`
- `01_PRE_REPAIR_IMPLEMENTATION_IDENTITY_RECEIPT.json`
- `02_REPAIR_DIFF_RECEIPT.json`
- `03_REPAIRED_IMPLEMENTATION_IDENTITY_RECEIPT.json`
- `04_POST_REPAIR_SMOKE_RECEIPT.json`
- `05_B20Q2_HANDOFF.json`
- `CHANGED_FILES.txt`

Hard stops:
- no changes outside `_routing_membership()`;
- no full qualification PASS claim;
- no C09/WVS7;
- no common harness;
- no benchmark/ranking;
- no OBL037 / architecture selection / positive V3.

Return to SUB-VOZHD B.
