# D r11 evidence and commands

## Focused tests

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_produces_two_target_fact_for_cold_e \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 2 passed in 2.88s
```

## Actual asymmetric joint probe

Controlled sourcefree SAV with deliberately asymmetric conditional counts:

- plan F2 target `fixture.B`, conditioner `fixture.A`;
- engine result: 3 facts, arities `{1:2, 2:1}`, 4 joint cells,
  raw numerator/denominator 12/12;
- cold E: `CONDITIONAL_SUPPORT_PROFILE`;
  condition B=0 denom 8 target A `{0:6,1:2}`;
  condition B=1 denom 4 target A `{0:0,1:4}`.
- expected requested F2 P(B|A): condition A=0 denom 6 target B `{0:6,1:0}`;
  condition A=1 denom 6 target B `{0:2,1:4}`.
- API with explicit correct roles (`conditioner=A,target=B`): `TYPED_REFUSAL`;
  API with reversed roles (conditioner=B,target=A): profile. The envelope query
  target order `[B,A]` prevents recovering the requested direction.

## Joint refusal / preservation

- Missing permission, tampered replay fact ref, and tampered joint cell all
  refuse in the accepted E codec.
- 1-target envelopes remain exact `FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED`
  refusals; `structural_grant=false`.
- Changed source cell changes fact refs; exact restore returns original refs
  (focused R11 test).
- Prior R10 artifact publication/decision ordering remains unchanged; the joint
  helper consumes a qualified bundle and performs no new source admission.

## Limits

Actual original facts, authentic E handshake, A/C scale, all35/native/S3/
science and protected acceptance remain NOT_RUN. No original data, 650 s or
full-estate run, source read, code repair, or A/C/E/guide/progress/controller
edit. E codec blob `6acba005…` exact.
