# RABOCHII B20R — ROUTE C QUALIFICATION-DRIVER REFERENCE NORMALIZATION REPAIR R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-as4i-route-c-qualification-driver-reference-normalization-repair-r1`

Exact starting HEAD:
`74053daed81e660b5b22db8bdaa26186442b6fca`

Repair-only mission.

PASS terminal:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

Blocker terminal:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR__EXACT_BLOCKER_PROVED`

## 1. Binding adjudication

Read:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/39_B20Q_BLOCKER_ADJUDICATION_AND_B20R_DRIVER_REPAIR_AUTHORIZATION_R1.md`

## 2. Frozen implementation

DO NOT MODIFY:

`rawlsing_next/pre553_route_c_accelerators.py`

Frozen implementation blob:
`ed249de09b15b1b948d9e79bd3056e58967d2e66`

Frozen implementation SHA-256:
`d949394ad18c89e1956ec317d43993d36477d9ef4ebe1c3bdb1f5f12d4a8aa17`

## 3. Exact driver to repair

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B20_AS4I_ROUTE_C_CACC1_CACC2_PARITY_ADAPTER_R1/01_ROUTE_C_IMPLEMENTATION_QUALIFICATION.py`

Pre-repair driver blob:
`366d83ca9f08d93637dcdbd5b555913a18d2943a`

Pre-repair driver SHA-256:
`a5a69d59d768675b2dd14ad5fb257e2943e569131b253cf5f7243af6a6e0200c`

## 4. Exact proved defect

At `_route_c_fixture()`, the driver builds an allowed set of exact question refs and filters routing facts with:

`fact.question_or_target_ref in allowed_qrefs`

At runtime:
`fact.question_or_target_ref`
is canonical mapping material, so set-membership attempts to hash a dict and raises:

`TypeError: unhashable type: 'dict'`

This failure is reproduced twice in clean worktrees.

## 5. Authorized repair

Use the repo-native converter:

`rawlsing_next.pre553_empirical_objects.exact_ref`

Authorized conceptual change:

`exact_ref(fact.question_or_target_ref, "routing question_or_target_ref") in allowed_qrefs`

Add only the import and exact normalization needed for this comparison.

Do NOT:
- convert to fuzzy/string identity;
- compare only object_id;
- compare only content_hash;
- mutate routing facts;
- change the allowed question set;
- alter fixture semantics.

## 6. Commit-before-smoke law

The repair MUST be committed before any validating smoke execution.

Record:
- repaired commit SHA;
- repaired driver Git blob;
- repaired driver SHA-256;
- exact textual/semantic diff.

## 7. Smoke boundary

After repair commit, run the minimum real process needed to prove the old failure is removed.

Preferred:
- execute the repaired driver until at least successful completion of `_route_c_fixture()` and entry into the first CACC1 build;
- or run the full driver if that is the simplest available invocation, but do NOT use such a run as B20Q2 qualification authority.

The smoke result may establish only:
`FORMER_UNHASHABLE_ROUTING_REF_FAILURE_REMOVED`.

If a new, independent driver defect appears:
- preserve it exactly;
- stop;
- do not patch it in B20R unless it is strictly the same representation-normalization issue.

## 8. Required outputs

Write only under:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B20R_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR_R1/`

Required:
- `00_RETURN.md`
- `01_PRE_REPAIR_IDENTITY_RECEIPT.json`
- `02_REPAIR_DIFF_RECEIPT.json`
- `03_REPAIRED_DRIVER_IDENTITY_RECEIPT.json`
- `04_POST_REPAIR_SMOKE_RECEIPT.json`
- `05_B20Q2_HANDOFF.json`
- `CHANGED_FILES.txt`

## 9. PASS consequence

PASS authorizes only a new full qualification court:

`B20Q2_ROUTE_C_FULL_QUALIFICATION_ON_REPAIRED_DRIVER`

B20R itself MUST NOT claim:

`AS4I_ROUTE_C_CACC1_CACC2_PARITY_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

## 10. Hard stops

Do NOT:
- modify Route-C implementation;
- modify common semantic/query/discovery code;
- claim full qualification PASS;
- execute real C09;
- execute WVS7;
- benchmark/rank;
- implement common harness;
- launch OBL037;
- select architecture/topology;
- enter positive V3.

Return to SUB-VOZHD B.
