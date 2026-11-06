# 01 — E r1 narrow diff and independent probe notes

## Exact diff

`git diff 15da2b8bf..7d1aadfd4 -- rawlsing_next/` is limited to:

- `pre553_field_forge_empirical_ingress.py` (+39): `_exact_fact_query` now
  compares:
  1. fact/query `condition_predicate_ref`;
  2. fact/query `measure_basis_ref`;
  3. fact `response_state_semantics_ref` vs query requested-output-grain;
  4. fact `source_scope_mode` vs query grain (missing/None rejected);
  5. fact `measure_kind` vs query grain (missing/None rejected).
- `test_pre553_field_forge_empirical_ingress.py` (+5 parametrized cases; 16
  total).

No owner file, producer function, bridge, structural-admission, guide, or shared
status file changed. No fixture expected response was inserted into production.

## Independent probe

`evidence/e_r1_fivecase_probe.json` constructs variants of the exact FF fixture
with a valid bound query but altered semantic fields. At repaired head:

- different condition predicate → `FieldForgeEmpiricalIngressError`
- different measure basis → `FieldForgeEmpiricalIngressError`
- different response-state semantics → `FieldForgeEmpiricalIngressError`
- null source scope → `FieldForgeEmpiricalIngressError`
- null measure kind → `FieldForgeEmpiricalIngressError`
- null condition / measure basis / response state → typed ingress error

Positive control returns `CONDITIONAL_SUPPORT_PROFILE`, counts `[3,3,0]`,
`structural_grant=false`, bridge typed refusal for the fixture scope, and the
same relation ref as a direct `produce_exact_conditional_support_profile` call.
The old five-case acceptance negative is preserved in
`evidence/old_negative_preserved.json`.

## Test-quality note (nonblocking)

The new author test parametrization uses `pytest.raises(Exception)` with a detail
substring. The implementation was independently verified to raise
`FieldForgeEmpiricalIngressError`; future test tightening to the exact exception
is recommended but does not block this scoped acceptance.

## Boundaries

- D authentic bind NOT_RUN.
- Native/all35 NOT_CLAIMED.
- Structural/science/actor NO_ISSUANCE.
- Protected receiving NONE.
- GT2 two-target RAW limit remains real.
