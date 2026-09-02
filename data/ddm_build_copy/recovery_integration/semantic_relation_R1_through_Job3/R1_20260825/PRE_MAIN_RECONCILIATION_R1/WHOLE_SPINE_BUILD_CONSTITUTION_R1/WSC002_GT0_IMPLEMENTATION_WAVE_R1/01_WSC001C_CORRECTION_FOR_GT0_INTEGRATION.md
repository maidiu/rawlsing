# WSC002 GT0 INTEGRATION CORRECTION — WSC001C SECOND-PASS R1

Binding correction evidence for central WSC002 integration:

`WSC001C_SECOND_PASS_REVIEW_AND_REPAIR_R1`

## Applies to WSC002 D and central integration

The current PRE553 I04 implementation accepts exact `EmpiricalQuerySpec + EmpiricalFact`; it is not a direct consumer of a FIELD FORGE relation object.

The current M1 direct basis grammar accepts `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` or V553 temporal material; it is not yet a direct FIELD-FORGE-relation basis.

Therefore WSC002 integration MUST reject any candidate implementation that:

1. wraps GT0 FIELD FORGE receipt/relation as `EmpiricalFact` merely to call I04;
2. fabricates a `StructuralEmpiricalAdmission` from FIELD FORGE relation/reference material;
3. feeds a FIELD FORGE relation directly into current M1 as though it were `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION`;
4. infers substantive PRE-V3 structure from the GT0 F0 source-structure/current-candidacy fact.

## Correct GT0 baseline behavior

For bound F0, WSC002 D should:

- accept the exact producer-preserving FF-stage receipt;
- validate exact upstream references, permission, typed state, dependency/replay closure and information-loss declaration;
- determine that the requested substantive PRE-V3 structural assertion is outside the lawful information/semantic type of the object;
- return `UNDEFINED_FOR_OBJECT` or the narrower exact blocker;
- preserve all upstream references and replay closure;
- produce no `StructuralEmpiricalAdmission`, V554 basis, V555 route, or actor state;
- allow `ZERO_V556_OBJECTS`.

A local GT0 wrapper/bridge may encode that blocker. It owns no new social meaning and creates no new semantic authority.

## Future positive path

Positive FIELD FORGE relation -> PRE-V3 execution remains an explicit implementation/compatibility gate requiring a separately governed FIELD-FORGE-relation admission surface plus an M1-compatible basis adaptation/extension.

Do not solve that generalized positive gate inside GT0 baseline implementation.

Terminal integration rule:

`GT0_BLOCKED_PATH_PASS != POSITIVE_FIELD_FORGE_TO_PREV3_COMPATIBILITY_CLOSURE`.
