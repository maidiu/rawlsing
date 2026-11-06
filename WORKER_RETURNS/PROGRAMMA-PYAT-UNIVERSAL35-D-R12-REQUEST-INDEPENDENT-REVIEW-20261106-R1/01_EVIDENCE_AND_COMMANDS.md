# D r12 evidence and commands

## Focused tests

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 2 passed in 2.88s
```

## Actual asymmetric engine/cold probe

Controlled sourcefree SAV with asymmetric counts; actual requested F2 IDs.

- B|A: targets `[A,B]`; cold profile A=0 denom 6 B `{0:6,1:0}`, A=1 denom 6
  B `{0:2,1:4}`.
- A|B: targets `[B,A]`; cold profile B=0 denom 8 A `{0:6,1:2}`, B=1 denom 4
  A `{0:0,1:4}`.
- 3 facts, arities `{1:2,2:1}`, 4 joint cells, raw 12/12; both requests `OK`;
  cold CLI state `CONDITIONAL_SUPPORT_PROFILE`.

## Conditional-value gap

Two explicit F2 IDs sharing target/conditioner but with conditioner values
`("0",)` and `("1",)` both return `status=OK` with the same joint fact ref
`f311ac09…` and same query ref; neither result contains `conditioner_values` or
selected E profile rows. `_joint_frontier_for_pair` uses `conditions=()`.
This is the unresolved conditional-request realization gap.

## Preserved / refusal evidence

- Unknown operation ID -> typed `REQUESTED_OPERATION_NOT_IN_PLAN`; invalid
  request list fails closed; ineligible/weighted F2 handling is explicit.
- Missing permission, tampered replay, and tampered joint cell refuse in E.
- Changed source cell changes joint/profile; exact restore passes in the focused
  test.
- R10 final-decision/artifact ordering and permission/no-drop proofs untouched;
  joint helper consumes qualified bundle and performs no new source admission.
- E codec blob `6acba005…` exact.

## Limits

Actual original facts, authentic E handshake, all35/native/S3/science and
protected acceptance remain NOT_RUN. No original data, full-estate, 650 s run,
code repair, or A/C/E/guide/progress/controller edit.
