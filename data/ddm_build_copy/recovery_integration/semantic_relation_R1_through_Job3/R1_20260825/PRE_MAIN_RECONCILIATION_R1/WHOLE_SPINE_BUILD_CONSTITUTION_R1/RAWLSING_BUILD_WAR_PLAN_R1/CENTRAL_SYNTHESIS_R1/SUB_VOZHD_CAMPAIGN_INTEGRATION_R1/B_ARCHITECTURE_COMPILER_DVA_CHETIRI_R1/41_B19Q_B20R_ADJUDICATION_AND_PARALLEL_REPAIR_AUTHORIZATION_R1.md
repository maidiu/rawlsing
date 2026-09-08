# SUB-VOZHD B — B19Q/B20R ADJUDICATION + PARALLEL REPAIR AUTHORIZATION R1

Status:
`B19Q_TEST_COURT_BLOCKER_ACCEPTED__B20R_DRIVER_REPAIR_PASS_ACCEPTED__B19R_AND_B20IR_AUTHORIZED_IN_PARALLEL__FULL_QUALIFICATION_STILL_REQUIRED`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Campaign tip before this adjudication:
`c173cf21a37720bb3aa0d26ecdc05f4b95ccc4f0`

## 1. B19Q accepted exact blocker

Branch:
`agent/rabochii-subv-b-as4i-route-a-adapter-qualification-r1`

Final tip:
`47ed7863fdaf94d58f36522a11f8bf4f14b742d6`

Campaign bank merge:
`d40978dfcfbaebcd86f1987c519ed2be21c800f3`

Terminal:
`AS4I_ROUTE_A_ADAPTER_QUALIFICATION__EXACT_BLOCKER_PROVED`

Two genuinely fresh executions of:

`python -m pytest -q rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

each produced:
- 8 collected;
- 7 passed;
- 1 failed;
- 0 skipped;
- 0 errors.

Repeated failing test:
`test_two_independent_bounded_r5_builds_replay_to_identical_c11_identities`

Repeated physical-root mismatch:
- left:
  `a4d45cc535ffa5553a62682e4217433ded9cb4cdbcfaa2ff2bcbbe89d0283235`;
- right:
  `acd27ebf58a033a323596ec02889a286faf5a2dc4100160f535a3ddae78c00f7`.

Accepted diagnosis:
the test creates carriers in distinct directories AND gives them distinct release-identity tags `left` and `right`; those tags flow into release identity material, and the compact carrier correctly includes release identity in `physical_root_id`.

Therefore the failing assertion compares physical roots that were intentionally assigned different identity determinants.

No Route-A implementation defect is proved by B19Q.

## 2. B20R accepted repair-scope PASS

Branch:
`agent/rabochii-subv-b-as4i-route-c-qualification-driver-reference-normalization-repair-r1`

Final tip:
`6afddfd93570f9d02a19e8806eea88425603610f`

Campaign bank merge:
`c173cf21a37720bb3aa0d26ecdc05f4b95ccc4f0`

Terminal:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

Repair commit:
`006dea7e1c715b0c6ceeac06d458b9ecfd62e2b2`

Repaired driver blob:
`5377c70b5b3b9110cfd719b62ae1c3e2ceb07843`

Repaired driver SHA-256:
`73d9d9efd5bf70a181a7ddac3d98a5e8f7a90277765945862c402b4656c67350`

Former fixture-filter TypeError is proved removed.

## 3. Newly exposed Route-C implementation defect class

B20R smoke entered first `build_cacc1()` and then failed in:

`rawlsing_next/pre553_route_c_accelerators.py::_routing_membership`

Current code constructs:

`pair = (fact.scoped_respondent_ref, fact.question_or_target_ref)`

and uses that pair as a dict key.

Both semantic fields are canonical mapping-form refs at runtime.

The same function later also constructs:

`{fact.risk_set_ref for fact in facts}`

which is the same representation class and would likewise attempt to hash mapping-form exact refs.

The repo-native law is to normalize exact mapping refs through:

`rawlsing_next.pre553_empirical_objects.exact_ref(...)`

before hash-key/set use.

This is one bounded representation-normalization defect class in `_routing_membership`, not permission to redesign Route C.

## 4. B19R authorized grain

Authorize exactly:

`B19_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR`

B19R may modify ONLY:
`rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

Exact repair intent:
- retain two physically distinct carrier directories/build roots;
- give the two logically equivalent carriers the SAME release identity determinant;
- preserve the test's intended claim: independent builds of the same governed release reproduce identical physical-root/C11/replay identities.

Preferred bounded form:

`shared_identity = _identity(fx, tag="replay")`

then build:
- left with `name="left", identity=shared_identity`;
- right with `name="right", identity=shared_identity`.

Do not weaken assertions.
Do not alter Route-A implementation/runtime code.

B19R must commit repair before smoke, then prove the formerly failing test passes.
B19R itself may not claim full Route-A qualification PASS.

PASS:
`B19_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR_COMPLETE__READY_FOR_B19Q2_FULL_QUALIFICATION`

## 5. B20IR authorized grain

Authorize exactly:

`B20_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_NORMALIZATION_IMPLEMENTATION_REPAIR`

B20IR may modify ONLY:
`rawlsing_next/pre553_route_c_accelerators.py`

and its own repair receipts.

Within `_routing_membership()` only, normalize exact semantic reference fields before hash-key/set use.

Required bounded normalization:
- `exact_ref(fact.scoped_respondent_ref, "routing scoped_respondent_ref")`;
- `exact_ref(fact.question_or_target_ref, "routing question_or_target_ref")`;
- `exact_ref(fact.risk_set_ref, "routing risk_set_ref")`.

Use normalized ExactRef values for:
- `by_pair` keys;
- pair lookup consistency;
- common-risk ref set.

Do NOT:
- compare object_id only;
- compare content_hash only;
- stringify refs;
- mutate routing facts;
- widen accepted routing state law;
- touch CACC1 layout;
- touch CACC2 masks;
- alter query/discovery semantics;
- touch the repaired B20 qualification driver.

B20IR must commit implementation repair before smoke.

Smoke must at least:
- pass the former `_routing_membership` unhashable failure;
- complete first CACC1 build if no new independent defect intervenes.

B20IR itself may not claim full Route-C qualification PASS.

PASS:
`B20_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

## 6. Full qualification still mandatory

After repair PASS:
- B19R -> separate B19Q2 full 8-test qualification, two fresh processes;
- B20IR -> separate B20Q2 full Route-C qualification using repaired driver + repaired implementation under pyarrow 25.0.1.

No common-harness intake until B19Q2 and B20Q2 both PASS.

## 7. External WVS7 dependency unchanged

`CROSS_CAMPAIGN_DEPENDENCY__SUB_VOZHD_B__REQUIRES__VOZHD_TRII_SOURCE_CERTIFICATION_PLUS_HQ__WVS7_D03_ROUTING_D11_EMPIRICAL_UNIVERSE_D12_GOVERNED_REPLAY_AND_FULL_GSR07_SOURCE_CERTIFICATION`

## 8. Hard stops

Neither repair worker may:
- claim route qualification PASS;
- execute C09;
- execute WVS7;
- benchmark/rank A/B/C;
- implement common harness;
- launch OBL037;
- select OBL001/002;
- enter positive V3;
- mutate central/PRE-MAIN/main.

Terminal:
`SUB_VOZHD_B_B19R_B20IR_PARALLEL_REPAIR_AUTHORIZED__B19Q2_B20Q2_REQUIRED_AFTER_REPAIR__COMMON_HARNESS_GATED`
