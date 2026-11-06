# PROGRAMMA PYAT — Universal35 E independent empirical-ingress review

**Verdict:** `REVISE_MATERIAL_NARROW` — thin delegation and the reviewed tests
pass, but the ingress does **not** enforce several exact fact↔query semantic
linkages it is supposed to gate. A self-consistent fact with a different
condition predicate, measure basis, response-state semantics, source scope, or
measure kind is accepted and produces a conditional-support profile instead of a
typed refusal.

## Identity / scope

- Reviewed frozen head: `15da2b8bf71d1ee61d6b3040996436f8be537e06`
- Implementation/test commit: `08138f52da1c32b62d28532b87b0cdce340c2bae`
- Base: `d119045f4169439b4ba02d0870bc328f8beb3aaa`
- Branch: `codex/pyat-universal35-e-review-20261106-r1`
- Reviewed files: `rawlsing_next/pre553_field_forge_empirical_ingress.py`,
  `rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py`, E
  `D_INPUT_CONTRACT.json`, `INTERFACE.json`, `run_ingress.py`; reused current
  `field_forge_conditional_support.py` and `gt12_c_to_d_relation_bridge.py`.
- G did not author E/tests; no product/test repair; no source/structural/science
  issuance, protected merge, original-data read, or self-review.
- D authentic products: **NOT_RUN / NOT_RECEIVED_BY_E**. Native/all35: not claimed.

## What passes

- **Actual owner delegation:** `ingest_empirical_fact` calls
  `field_forge_conditional_support.produce_exact_conditional_support_profile`
  and then only `gt12_c_to_d_relation_bridge.bridge_gt12_c_relation_to_d_evidence`.
  It never calls `admit_gt12_c_relation`, `pre553_structural_admission`, or a
  replacement statistics implementation.
- **No fixture-expected implementation:** fixture counts/expected values occur
  only in tests; production code contains no hardcoded Q86 counts, source IDs, or
  target values.
- **Arity/target limits:** one-target and real current 3-target facts are typed
  refusals; the GT2 two-target limit is preserved as a real consumer limitation,
  not generic F4/N10E/all35 completion.
- **Reversed role / incomplete cells / RAW weighted input:** typed refusals.
- **Two-target RAW GT2-compatible fixture:** existing owner profile with true zero
  and minority counts; structural grant always false; structural state withheld.
- **Dependency sever/restore:** severed joint cell → RED typed refusal; restored
  exact fact → PASS with the same relation ref.
- **Current N10E producer:** actual current provider fact reaches ingress and is
  typed-refused for one-target FF arity; `n10e_provider_state =
  EXACT_SUPPORTED_SLICE_PRODUCED`, route `DIRECT_I03_TO_POSITIONED_SUBJECT`.
- **Default permission tuple:** it is a caller-owned ceiling passed to the
  existing owner, not independent source authority; relation ceiling may narrow
  only. No source grant follows.

## Defect (consequential)

`_exact_fact_query` checks fact/query object types, content hashes, and
`fact.empirical_query_spec_ref == query.ref`. The existing FF owner then checks
risk-set, universe, RAW/null-weight, authorities, replay, provenance, target
domain/topology. Neither layer compares the remaining exact semantic fields that
`D_INPUT_CONTRACT.json` requires:

- `fact.condition_predicate_ref` vs `query.condition_predicate_ref`
- `fact.measure_basis_ref` vs `query.measure_basis_ref`
- `fact.response_state_semantics_ref` vs
  `query.requested_output_grain.response_state_semantics_ref`
- `fact.source_scope_mode` vs `requested_output_grain.source_scope_mode`
- `fact.measure_kind` vs `requested_output_grain.measure_kind`

Consequence: a caller can supply a self-consistent `EmpiricalFact` that binds the
right query ref but carries a **different conditioner/measure/response/scope
semantics**, and E returns `CONDITIONAL_SUPPORT_PROFILE` with a relation ref. That
is a false semantic linkage at the ingress boundary, not a new cryptographic
court: these are already exact typed fields in the D contract and current owner
inputs.

Independent reproducer:
`evidence/e_ingress_defect_probe.json`. It constructs five variants with the
same bound query:

| Variant | Observed |
|---|---|
| different `condition_predicate_ref` | `CONDITIONAL_SUPPORT_PROFILE`, refusal empty |
| different `measure_basis_ref` | `CONDITIONAL_SUPPORT_PROFILE`, refusal empty |
| different `response_state_semantics_ref` | `CONDITIONAL_SUPPORT_PROFILE`, refusal empty |
| `source_scope_mode=None` | `CONDITIONAL_SUPPORT_PROFILE`, refusal empty |
| `measure_kind=None` | `CONDITIONAL_SUPPORT_PROFILE`, refusal empty |

The accepted relation ref is recomputed from the forged fact, so content-hash
checks alone cannot catch it.

## Precise narrow repair recommendation (not applied)

In `rawlsing_next/pre553_field_forge_empirical_ingress.py::_exact_fact_query`,
before delegation, compare the exact fields:

```python
grain = query.requested_output_grain  # already a mapping by owner contract
if exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref") != \
   exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref"):
    raise FieldForgeEmpiricalIngressError("fact condition predicate does not bind query")
if exact_ref(fact.measure_basis_ref, "fact.measure_basis_ref") != \
   exact_ref(query.measure_basis_ref, "query.measure_basis_ref"):
    raise FieldForgeEmpiricalIngressError("fact measure basis does not bind query")
if exact_ref(fact.response_state_semantics_ref, "fact.response_state_semantics_ref") != \
   exact_ref(grain["response_state_semantics_ref"], "query.response_state_semantics_ref"):
    raise FieldForgeEmpiricalIngressError("fact response semantics do not bind query")
if fact.source_scope_mode != grain["source_scope_mode"]:
    raise FieldForgeEmpiricalIngressError("fact source scope does not bind query")
if fact.measure_kind != grain["measure_kind"]:
    raise FieldForgeEmpiricalIngressError("fact measure kind does not bind query")
```

Add focused negative tests for each mismatch (expected ingress error or typed
refusal, consistently), plus a positive control. Do not relax the existing arity,
role, incomplete-cell, weighted, provenance/replay, or structural-withheld tests.
A narrower alternative is to add the same equality checks to the existing FF
owner `_validate_common_closure`, but that changes an existing owner contract;
the E precheck is the smallest lawful repair for this new facade.

## Separate grades

| Grade | Result |
|---|---|
| Sourcefree engineering | `REVISE_MATERIAL_NARROW`; delegation/refusals mostly pass but exact semantic linkage missing |
| Sourcefree RAW two-target fixture | Owner profile PASS on reviewed fixture; dependent on missing linkage gate |
| Native / D authentic bind | **NOT_RUN**; D products not received |
| Original35/all35 | **NOT_CLAIMED** |
| Scientific/structural/actor | **NO_ISSUANCE**; structural grant always false, no GT12-D admission |
| Protected receiving | **NONE**; branch-only review |

## Exact independent test receipts

- `test_pre553_field_forge_empirical_ingress.py`: **11 passed in 0.76 s**
- `test_field_forge_conditional_support.py` + `test_gt12_closure_b_c_to_d_bridge.py`:
  **25 passed in 0.27 s**
- Sever/restore test: **1 passed in 0.34 s**
- `run_ingress.py abi`: exit 0; interface readback pass
- `run_ingress.py selftest`: exit 0; GT2 profile and N10E typed refusal
- Defect probe: FAIL (E accepts forged semantic variants) — evidence file above

No whole-estate/full-regression run. No source edits.

## PROGRAMMA_DELTA (ordinary return)

- Identity: E ingress `PRE553_FIELD_FORGE_EMPIRICAL_INGRESS@1.0.0`, reviewed at
  `15da2b8bf71d1ee61d6b3040996436f8be537e06`, implementation
  `08138f52da1c32b62d28532b87b0cdce340c2bae`.
- Function: exact fact+query → existing FIELD FORGE conditional support profile or
  typed refusal; bridge evidence only.
- Input→output: currently accepts some contradictory fact/query semantic fields
  → relation; required narrow fix adds exact equality refusals.
- Root/schema/clock/permission: no new root/clock; caller permission ceiling only.
- Actual first consumer: existing FF owner; N10E current one-target typed refusal;
  no structural admission.
- Affected IDs: `W08`, `W09`, `P07`, `P08`, `S-F1F4`, `N10E` first-reader seam;
  no 62/82/49 rewrite.
- Conditional unlocks: after fix, D authentic two-target RAW facts can bind; D
  authentic bind remains NOT_RUN now.
- Next action: E author applies narrow linkage precheck + tests; independent
  re-review; no protected merge.

## Limits

- Sourcefree/test-only; no original respondent bytes or native facts.
- GT2 two-target/RAW/single-universe remains the real existing owner limitation;
  this review does not declare F4/N10E/all35 completion.
- Structural admission/GT12-D admission was not invoked; structural grant false.
- D authentic products not present; no native acceptance.
