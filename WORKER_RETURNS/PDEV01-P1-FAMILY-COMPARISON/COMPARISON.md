# P1 CONDITIONAL/JOINT vs R03 governed frontier and I03

## Disposition

**HOLD_MISSING_EXACT_P1_HANDOFF**

The accepted GAP007 P1 plan contains 210 CONDITIONAL and 210 JOINT planned
operations, but it supplies only prospective `SourceItem`/`EligiblePopulation`
refs and source codes. It does not supply the exact R03 `OccurrenceKey` operand
identities, risk-set/denominator refs, inventory/policy identity, direction/
form/scope identity, or current I03 query/predicate/joint/marginal refs.

The existing R03 sourcefree receiver executes its own exact conditional and
joint inputs successfully. It cannot execute the P1 conditional/joint entries
without a new exact handoff. No P1 predicates were invented.

## Exact comparison

### P1 entries

- P1 plan: `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`
- 840 operations, `TEST_ONLY_SOURCEFREE`
- CONDITIONAL: 210
- JOINT: 210
- Sample P1 CONDITIONAL and JOINT operations are `COMPILED`
- P1 `batch_job_ref` kind: `PROGRAMMA_PYAT_EPRE_OPERATION` (not
  `EmpiricalQuerySpec@1.0.0`)
- P1 item/conditioner/joint refs: `SourceItem`
- P1 eligibility ref: `EligiblePopulation`
- P1 route: `Route`; weight: `WeightDesign`
- No R03 `OccurrenceKey`, risk set, direction, form/scope, inventory/policy, or
  current query/predicate/joint/marginal refs.

### R03 exact inputs

Existing R03 test:
`test_r03_governed_frontier_joint_conditional_no_drop_and_cold` — **1 passed**.

- R03 CONDITIONAL lowering: `SUPPORTED`, family
  `BRANCH_CONDITIONED_DISTRIBUTION`
- R03 JOINT lowering: `SUPPORTED`, family `PAIR_RESPONSE_COTRAVEL`
- R03 execution: 150 operation receipts/fact refs, 330 facts, no-drop true
- Required target/condition operands: exact `OccurrenceKey` with item/option/
  form/repeat identity
- Required eligibility/denominator: `risk_set_ref` and `risk_set_refs`
  (`RISK-A` in the R03 fixture)
- Required policy/operation context: `direction_ref`, `form_scope`, `scope`,
  administration states, measure plan, source inventory and policy hash
- Required I03 inputs: current `EmpiricalPredicate@1.0.0` and
  `EmpiricalQuerySpec@1.0.0` refs; JOINT additionally requires joint and
  marginal query refs.

### What P1 actually supplies vs. what is required

- **Alias:** no exact alias. P1 `SourceItem` refs and `source_variable_code`
  strings do not equal R03 `OccurrenceKey` identities; P1 has no option/form/
  repeat identity.
- **Missing handoff:** yes. P1 lacks exact R03 occurrence, inventory/policy,
  risk-set/denominator, direction/form/scope/administration and current I03
  query/predicate/joint/marginal refs.
- **Unissued scientific intent:** yes. P1 conditional/joint operations are
  prospective TEST_ONLY operation classes with no current issued I03/I05
  binding and no sourced scientific result.
- **First missing input:** exact R03 `OccurrenceKey` for the P1 target and
  conditioner operands; after that, exact R03 inventory/policy/risk-set and
  current NativeCatalog query/predicate/joint/marginal refs.

## Prior accepted GAP007 result preserved

- Source SHA: `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- Release: `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`
- 210 DIST executed / 210 `SUPPORTED`
- 630 typed refusals: CONDITIONAL 210, JOINT 210, HETEROGENEITY 105,
  RECURSIVE_BRANCH 105
- 840 total
- Prior cold replay and review artifacts preserved.

## Exact commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  python3 WORKER_RETURNS/PDEV01-P1-FAMILY-COMPARISON/compare_p1_r03.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  python3 -m pytest rawlsing_next/tests/test_universal_workload.py::test_r03_governed_frontier_joint_conditional_no_drop_and_cold \
  -q -o addopts=''
```

## Scope

Sourcefree, TEST_ONLY engineering comparison only. No original data, source
rights, production edit, CI, merge, adoption or new engine. Candidate is
read-only. Only `WORKER_RETURNS/PDEV01-P1-FAMILY-COMPARISON/**` was written.
