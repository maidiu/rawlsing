# B20R RETURN — ROUTE C QUALIFICATION-DRIVER REFERENCE NORMALIZATION REPAIR R1

Status: **PASS — REPAIR SCOPE ONLY**

Terminal:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

Branch:
`agent/rabochii-subv-b-as4i-route-c-qualification-driver-reference-normalization-repair-r1`

## Repair committed before smoke

Repair commit:
`006dea7e1c715b0c6ceeac06d458b9ecfd62e2b2`

The exact authorized two-line textual change was made in the B20 qualification driver:
- import `exact_ref` beside `ExactRef`;
- replace direct set-membership of canonical mapping material with:
  `exact_ref(fact.question_or_target_ref, "routing question_or_target_ref") in allowed_qrefs`.

No other file changed in the repair commit.

Repaired driver:
- Git blob: `5377c70b5b3b9110cfd719b62ae1c3e2ceb07843`
- SHA-256: `73d9d9efd5bf70a181a7ddac3d98a5e8f7a90277765945862c402b4656c67350`

Frozen Route-C implementation remained:
- Git blob: `ed249de09b15b1b948d9e79bd3056e58967d2e66`
- SHA-256: `d949394ad18c89e1956ec317d43993d36477d9ef4ebe1c3bdb1f5f12d4a8aa17`

## Post-repair smoke

The smoke checked out exact repair commit `006dea7e…` under CPython 3.13.15, `pyarrow==25.0.1`, pandas 3.0.5.

The repaired `_route_c_fixture()` completed successfully. The former driver failure:

`TypeError: unhashable type: 'dict'`

at:

`fact.question_or_target_ref in allowed_qrefs`

did **not** recur.

Execution then genuinely entered the first `build_cacc1()`, satisfying the B20R smoke boundary.

Therefore:

`FORMER_UNHASHABLE_ROUTING_REF_FAILURE_REMOVED`

is proved.

## Newly surfaced out-of-scope observation

The first CACC1 build then fails inside the frozen Route-C implementation at:

`rawlsing_next/pre553_route_c_accelerators.py::_routing_membership`

where:

`pair = (fact.scoped_respondent_ref, fact.question_or_target_ref)`

is used as a dict key and again contains canonical mapping material, producing:

`TypeError: unhashable type: 'dict'`

This is **not a new driver defect**. It is in the implementation file B20R is explicitly forbidden to modify. B20R therefore preserved it and stopped; no second repair was attempted.

B20R does **not** claim Route-C qualification PASS. B20Q2 remains the separately required full qualification court, with this implementation observation carried forward to SUB-VOZHD B.

Zero real C09, zero WVS7, zero ranking, zero common-harness entry, zero OBL037, zero architecture selection, zero positive V3.
