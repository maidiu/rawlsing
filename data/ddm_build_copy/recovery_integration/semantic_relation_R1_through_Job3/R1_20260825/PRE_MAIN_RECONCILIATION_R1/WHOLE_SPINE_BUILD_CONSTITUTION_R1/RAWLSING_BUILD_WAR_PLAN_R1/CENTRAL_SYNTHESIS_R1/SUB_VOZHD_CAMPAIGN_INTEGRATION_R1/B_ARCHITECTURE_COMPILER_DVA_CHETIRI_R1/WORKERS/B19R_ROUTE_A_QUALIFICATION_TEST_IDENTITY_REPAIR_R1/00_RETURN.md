# B19R RETURN — ROUTE A QUALIFICATION TEST IDENTITY REPAIR R1

Terminal:

`B19_ROUTE_A_QUALIFICATION_TEST_IDENTITY_REPAIR_COMPLETE__READY_FOR_B19Q2_FULL_QUALIFICATION`

Branch:
`agent/rabochii-subv-b-as4i-route-a-qualification-test-identity-repair-r1`

Starting HEAD:
`0ec9db44496563f6b18a063b66b3a8644df7aac6`

Handoff:
`304956409268a4bed50d72754f21ce2cf4a8cd40`

Current flight-state:
`68971da943275a4365ed656b1f660c4f960fbd3f`

Repair commit:
`8103a70b43dc657a41d2f42401eef9dfadcd3c1f`

## Repair

Only:
`rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py`

was changed.

Pre-repair test blob:
`2a274e7e6e65e269ff9edcf93a1bb1951186b2e6`

Post-repair test blob:
`25e905868a21bb36035269065b7bc3640201b7d8`

Route-A implementation blob remained:
`d4915e7e6755ba1850756aebff72f982f73a332b`

The repaired test preserves two distinct target directories (`left`, `right`) while giving both builds one shared governed release identity:

`shared_identity = _identity(fx, tag="replay")`

No equality assertion was weakened or removed.

## Commit-before-smoke proof

The repair was committed at `8103a70b43dc657a41d2f42401eef9dfadcd3c1f` before smoke execution.

The post-repair smoke checkout reproduced the committed repair tree:
`604d7b8d976627ec56847211701ed76e1b273fb2`

and repaired test blob:
`25e905868a21bb36035269065b7bc3640201b7d8`.

## Required smoke

Command:

`python -m pytest -q rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py::test_two_independent_bounded_r5_builds_replay_to_identical_c11_identities`

Result:

- exit code 0
- 1 passed
- 0 failed
- 0 errors
- 0 skipped
- elapsed reported by pytest: 0.26s

The formerly failing identity/parity test is repaired.

B19R does not claim Route-A qualification PASS. A separate B19Q2 must execute all 8 tests twice in fresh processes.

Return to SUB-VOZHD B.
