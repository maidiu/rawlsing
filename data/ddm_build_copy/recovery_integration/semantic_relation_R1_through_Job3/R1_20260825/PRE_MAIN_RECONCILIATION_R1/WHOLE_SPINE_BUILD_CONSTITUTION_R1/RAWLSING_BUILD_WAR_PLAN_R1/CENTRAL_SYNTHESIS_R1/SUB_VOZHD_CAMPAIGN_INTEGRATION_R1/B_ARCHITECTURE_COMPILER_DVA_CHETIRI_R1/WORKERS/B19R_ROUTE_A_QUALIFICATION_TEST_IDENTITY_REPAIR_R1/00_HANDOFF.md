# RABOCHII B19R — ROUTE A QUALIFICATION TEST IDENTITY REPAIR R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-as4i-route-a-qualification-test-identity-repair-r1`

Exact starting HEAD:
`0ec9db44496563f6b18a063b66b3a8644df7aac6`

PASS terminal:
`B19_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR_COMPLETE__READY_FOR_B19Q2_FULL_QUALIFICATION`

Blocker terminal:
`B19_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR__EXACT_BLOCKER_PROVED`

Repair-only mission.

## Exact defect

The frozen qualification test:

`test_two_independent_bounded_r5_builds_replay_to_identical_c11_identities`

creates two physically distinct carriers using names `left` and `right`. The helper defaults identity tag to `name`, so the two carriers receive different:
- decoder_receipt material;
- compiler_contract_digest;
- c11_authority_digest.

The compact carrier correctly includes full release identity in the material hashed into `physical_root_id`.

Thus the test asserts physical-root equality after deliberately changing a physical-root identity determinant.

## Authorized repair

Modify ONLY:

`rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

Preserve two distinct target directories/build roots.

Give both carriers one shared governed release identity.

Preferred repair:

`shared_identity = _identity(fx, tag="replay")`

then:
- `left = _reader(tmp_path, fx, name="left", identity=shared_identity)`
- `right = _reader(tmp_path, fx, name="right", identity=shared_identity)`

Do not:
- weaken/remove any equality assertion;
- compare only logical stream digest;
- alter Route-A implementation;
- alter R5 runtime code;
- alter carrier hashing law;
- alter C05R2A semantics.

## Commit-before-smoke

Commit the test repair before executing validation.

Record:
- pre/post test blob;
- repair commit;
- exact diff.

Smoke:
- run the formerly failing test alone from a real checkout.

If it passes, stop and return repair PASS.

A separate B19Q2 must still run all 8 tests twice fresh.

## Outputs

Write only under:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B19R_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR_R1/`

Required:
- `00_RETURN.md`
- `01_PRE_REPAIR_TEST_IDENTITY_RECEIPT.json`
- `02_REPAIR_DIFF_RECEIPT.json`
- `03_REPAIRED_TEST_IDENTITY_RECEIPT.json`
- `04_POST_REPAIR_SMOKE_RECEIPT.json`
- `05_B19Q2_HANDOFF.json`
- `CHANGED_FILES.txt`

Hard stops:
- no Route-A implementation edits;
- no full qualification PASS claim;
- no common harness;
- no C09;
- no WVS7;
- no ranking/selection;
- no OBL037 / positive V3.

Return to SUB-VOZHD B.
