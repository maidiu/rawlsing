# PROGRAMMA PYAT universal35 — E ingress r1 linkage repair

**RESULT:** `E_INGRESS_R1_EXACT_FACT_QUERY_LINKAGE_REPAIR__AUTHOR_FOCUSED_PASS__OLD_HEAD_RED_REPRODUCED__REPAIRED_HEAD_REFUSES__INDEPENDENT_REREVIEW_PENDING`.

**Base/lineage:** base `d119045f4169439b4ba02d0870bc328f8beb3aaa`; previously
published E frozen head `15da2b8bf71d1ee61d6b3040996436f8be537e06`,
implementation `08138f52da1c32b62d28532b87b0cdce340c2bae`; independent reviewer
G `e714a5dd3628f3b60ab5b6bdcfeef036ecdabc8f` verdict
`REVISE_MATERIAL_NARROW`.

## Exact repair

Only `_exact_fact_query` in
`rawlsing_next/pre553_field_forge_empirical_ingress.py` was changed, plus matching
tests/evidence/return. Before delegation it now requires exact equality of:

1. `fact.condition_predicate_ref` == `query.condition_predicate_ref`
2. `fact.measure_basis_ref` == `query.measure_basis_ref`
3. `fact.response_state_semantics_ref` ==
   `query.requested_output_grain.response_state_semantics_ref`
4. `fact.source_scope_mode` == `query.requested_output_grain.source_scope_mode`
5. `fact.measure_kind` == `query.requested_output_grain.measure_kind`

Missing, `None`, malformed or mismatched values raise the existing typed
`FieldForgeEmpiricalIngressError`; they never acquire a support profile. Existing
arity/role/risk/universe/provenance/replay/null-weight checks, delegation,
bridge-evidence-only behavior and structural-grant-false remain intact. No
semantic owner or wider FIELD FORGE code was changed.

## Old-head RED and repaired-head result

The G five-case probe was reproduced against the old implementation
`08138f52` loaded unchanged from git:

- `evidence/old_head_defect_probe.json`: all five cases
  (`different_condition`, `different_measure_basis`, `different_response_state`,
  `null_source_scope`, `null_measure_kind`) returned
  `CONDITIONAL_SUPPORT_PROFILE` with a relation and empty refusal. RED reproduced.

At the repaired head, `evidence/repaired_head_linkage_probe.json` shows all five
cases are refused with the typed ingress error. The exact positive fixture still
returns the existing conditional support profile; real current N10E/I03
one-target facts still reach ingress and receive the two-target typed refusal.

## Commands and results

Runner unchanged: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`
(Python 3.11.3, PyArrow 22.0.0, DuckDB 1.5.2, macOS 13.7.8 x86_64). Passport:
`evidence/environment.json`.

```text
python3 -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/evidence/junit_ingress.xml \
  rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py
# 16 passed in 1.40s, exit 0

python3 -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/evidence/junit_regression.xml \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
# 25 passed in 0.27s, exit 0

python3 WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/run_ingress.py abi
python3 WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/run_ingress.py selftest
# exit 0 each
```

Focused coverage retained: positive exact profile; changed counts/denominator
change support; source-edition/provenance changes relation identity; true zero and
minority preserved; reversed role, 3+/one-target, missing joint, RAW weighted,
and five new linkage mismatches are typed refusals; dependency sever RED and
restore PASS; structural grant false; no GT12-D admission.

## Evidence

- `evidence/old_head_defect_probe.json` — G five-case old-head RED.
- `evidence/repaired_head_linkage_probe.json` — all five refused at repair.
- `evidence/junit_ingress.xml`, `logs/ingress-tests.log` — 16 tests.
- `evidence/junit_regression.xml`, `logs/ff-regression.log` — 25 tests.
- `evidence/ingress-selftest.json`, `evidence/interface-readback.json`,
  `evidence/test_run.json`, `evidence/result.json`,
  `evidence/source_manifest.json`, `evidence/environment.json`.

## Limits and grades

- Sourcefree/test-only; no original respondent bytes read by E.
- D authentic products: `NOT_RECEIVED_BY_E`; D bind remains separate.
- Native/all35: NOT_CLAIMED. Structural/science/actor: NO_ISSUANCE.
- GT2 two-target RAW single-universe remains the real existing owner limit.
- Independent rereview of the repaired exact head is required; this is not
  self-acceptance. No protected merge.

## Owner / next action

Distinct reviewer G or another nonauthor reviewer rechecks the exact repaired
commit and the five-case reproducer. D may bind authentic two-target RAW facts
only after that review; D numerical work is not blocked.

## Publication

Branch `codex/pyat-universal35-e-20261106-r1`. Exact repaired implementation
commit and final pushed head are in `PUBLICATION_RECEIPT.json`.
