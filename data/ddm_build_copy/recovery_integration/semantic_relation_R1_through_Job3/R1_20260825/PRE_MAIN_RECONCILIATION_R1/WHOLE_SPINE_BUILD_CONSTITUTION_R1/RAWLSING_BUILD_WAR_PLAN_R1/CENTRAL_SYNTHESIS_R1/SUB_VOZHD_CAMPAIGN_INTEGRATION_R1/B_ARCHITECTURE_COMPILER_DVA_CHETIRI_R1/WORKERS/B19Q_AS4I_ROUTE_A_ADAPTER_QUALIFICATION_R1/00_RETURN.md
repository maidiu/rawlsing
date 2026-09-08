# B19Q RETURN — AS4I ROUTE A ADAPTER QUALIFICATION R1

Terminal:

`AS4I_ROUTE_A_ADAPTER_QUALIFICATION__EXACT_BLOCKER_PROVED`

Branch:
`agent/rabochii-subv-b-as4i-route-a-adapter-qualification-r1`

Handoff:
`0adb463d97b9f4726eb4aad8cc112c9cc092ae13`

Campaign authorization:
`1c02ae8ce6f811a2e8a4fbf83f32acbf8003a5bf`

Current flight-state:
`6f17559c46f6ba0ed77a239b6136bf16575925da`

Frozen implementation commit:
`c935c7003c6081f699968ee4385d6a91bba5f13e`

## Qualification result

The exact committed court was executed twice in genuinely fresh Python processes:

`python -m pytest -q rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

Run 1: exit 1, 8 collected, 7 passed, 1 failed.
Run 2: exit 1, 8 collected, 7 passed, 1 failed.

Both runs fail the same committed test:

`test_two_independent_bounded_r5_builds_replay_to_identical_c11_identities`

at:

`rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py:130`

Exact repeated mismatch:

- left physical root: `a4d45cc535ffa5553a62682e4217433ded9cb4cdbcfaa2ff2bcbbe89d0283235`
- right physical root: `acd27ebf58a033a323596ec02889a286faf5a2dc4100160f535a3ddae78c00f7`

The failing assertion is:

`assert ldesc.physical_root_id == rdesc.physical_root_id`

No implementation, test, or recovered runtime code was modified.

## Frozen-code diagnosis

The committed test builds the two carriers with `name="left"` and `name="right"`. Its frozen `_identity(..., tag=name)` binds that tag into release identity material, including `decoder_receipt`, `compiler_contract_digest`, and `c11_authority_digest`. The frozen compact carrier includes the complete release identity in the unsigned root before hashing `physical_root_id`. Therefore the two deliberately different release identities produce different physical-root hashes even when their logical source row stream is identical.

This is recorded as diagnosis only. Qualification law forbids repair on this branch.

Common A/B/C harness intake remains gated.

Return to SUB-VOZHD B.
