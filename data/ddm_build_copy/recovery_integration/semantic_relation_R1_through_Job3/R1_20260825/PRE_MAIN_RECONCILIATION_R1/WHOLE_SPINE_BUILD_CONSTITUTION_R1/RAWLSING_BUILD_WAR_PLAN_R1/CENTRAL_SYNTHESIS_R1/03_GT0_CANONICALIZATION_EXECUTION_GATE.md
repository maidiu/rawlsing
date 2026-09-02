# GT0 CANONICALIZATION REAL-CHECKOUT EXECUTION GATE R1

## Purpose

The repaired GT0 at `ed1482517e0eebe2228e838dc6a24b97db879fc9` passed the exact bounded hostile rereview at `19ea48a7f0742c721e28b4ac51e6c205d01f5497`.

The rereviewer identified no remaining material semantic/API defect but correctly refused to fabricate an actual pytest execution claim because its connected GitHub environment had no checkout executor or reusable CI workflow.

This gate is therefore **execution only**, not another semantic audit.

## Exact candidate

Start from:

`ed1482517e0eebe2228e838dc6a24b97db879fc9`

Do not substitute the audit-only commit for the candidate.

## Required execution

In a real repository checkout, run:

1. the focused GT0 protocol/bridge/integrated tests;
2. the three WSC002R repair regressions;
3. the smallest inherited regression subset for structural-admission/M1 no-bypass, V3 zero-positive guard, M6 actor-safe expression, and bounded rendering, following the exact rereview scope;
4. no unrelated broad test campaign unless a focused import/dependency failure requires the smallest additional diagnostic.

At minimum include:

- `rawlsing_next/tests/test_wsc_gt0_protocol.py`
- `rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py`
- `rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py`
- `rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py`
- `rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py`
- `rawlsing_next/tests/test_wsc002r_c_m6_render_authoritative_binding.py`
- the smallest directly relevant inherited tests for `pre553_structural_admission.py`, `m1_temporal_v554_admission_dedup.py`, `v3_psepf_zero_positive_guard.py`, `m6_actor_safe_expression.py`, and `render_bounded_expression.py`.

## Pass condition

- all required focused/relevant inherited tests pass;
- no candidate-caused import/type/signature failure;
- no repair is needed.

If PASS, return the exact command(s), environment/Python identity, counts, terminal output summary, and candidate SHA. This authorizes a separate central canonicalization/adoption act at the audited GT0 grain.

If FAIL, identify only the smallest candidate-caused defect. Do not reopen architecture, FIELD FORGE R2, or the whole project.
