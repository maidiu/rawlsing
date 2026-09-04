# GT12 R4A — I03 SCALE-EQUIVALENCE REPAIR R1

## Exact jurisdiction

Repository: `maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-r4a-i03-scale-equivalence-repair-r1`

Exact working ancestry:

`0446710569c7b471c5d2e449628edadb396b45b4`

This repair is a bounded execution-representation repair for the existing PRE553 I03 evaluator only.

It is NOT:
- a new empirical algorithm;
- a GT2-specific semantic fast path;
- permission to change query/fact/replay identity law;
- permission to alter PRE553 public schemas;
- permission to use aggregate receipts in place of exact runtime objects;
- permission to acquire new source data;
- permission to execute PRE-V3/M1/M4/V3 E2B;
- permission to move PRE-MAIN or main.

## Established diagnosis

R4A has already proved on the exact accepted governed substrate:

- A1 C11 release hash:
  `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- A1 replay manifest:
  `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- exact risk-set cardinality: `19,210`
- current GT2 predicate:
  `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- current GT2 query:
  `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- release-index construction is not the bottleneck.

The remaining constrained-process slowdown occurs inside genuine-scale I03 evaluation.

## Concrete duplicated work already identified

In `rawlsing_next/_pre553_query_eval.py::_evaluate_index_group`:

1. each target routing fact is resolved and authority-validated in the per-target loop;
2. the same target routing fact is then resolved and authority-validated again by `_risk_membership`;
3. duplicate used objects and authority refs accumulate in append-only lists until end-of-evaluation canonical deduplication.

The final semantic outputs are already set-like/canonicalized:
- `used_objects` by exact `obj.ref.key`;
- `used_authority_refs` by exact authority identity;
- risk/denominator member refs canonically sorted;
- fact provenance canonically sorted;
- replay material canonically hashed.

Therefore the repair may remove duplicate intermediate work ONLY if final exact canonical material is unchanged.

## Required repair

Implement the smallest general I03 evaluator repair that:

1. resolves each respondent/target routing fact at most once per evaluation pass;
2. reuses those exact resolved routing states for membership determination;
3. preserves every existing routing conflict/unresolved/unknown-state failure;
4. reduces duplicate intermediate `used` / `used_auth` retention, preferably by exact-key deduplication during evaluation rather than only at the end;
5. preserves the exact final `used_objects` and `used_authority_refs` sets and canonical ordering;
6. preserves all weighted-query behavior even though GT2 is RAW;
7. remains generic PRE553 I03 code, with no Afrobarometer/Q86/GT12 branch inside the evaluator.

A small helper such as membership-from-prevalidated-routing-states is acceptable.
A special-case GT2 shortcut is forbidden.

## Identity / semantic invariants

Do not change:

- `EmpiricalPredicate` construction;
- `EmpiricalQuerySpec` construction;
- `EmpiricalFact` fields;
- `_make_execution_replay_ref` material;
- `_cell_projection`;
- target-domain order;
- Q86B -> Q86A component order;
- risk-set semantics;
- denominator semantics;
- typed response-state handling;
- authority scope law;
- public object schemas;
- canonical JSON/hash algorithms.

For any pre-repair fixture that completes successfully, post-repair execution MUST yield identical:

- query ref;
- predicate ref;
- fact ref;
- replay ref;
- risk-set member refs;
- denominator-member refs;
- complete cells;
- source empirical provenance refs;
- authority snapshot refs;
- typed state and execution detail.

## Required hostile tests

Add focused tests proving at minimum:

1. one routing lookup/validation per respondent/target in the normal path, not two;
2. conflicting routing facts still fail closed;
3. unresolved routing still fails closed;
4. target-specific common-risk disagreement still fails closed;
5. duplicate intermediate observations cannot alter final provenance;
6. authority closure is identical to the pre-repair semantic baseline;
7. replay/fact identity is identical on representative positive fixtures;
8. weighted behavior is not silently weakened or bypassed.

Do not weaken existing tests to make this pass.

## Required regression

Run at least:

`rawlsing_next/tests/test_pre553_empirical_query.py`

`rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py`

`rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py`

plus any new focused repair test file.

Run the smallest additional inherited PRE553 query/authority tests touched by the implementation.

## Real-scale boundary

This worker does NOT need Library or the accepted FFP014/FFP017 bytes.

After this repair passes its equivalence court, R4A proper will apply/integrate the repair into its exact checkout and rerun the accepted 19,210-member GT2 execution.

Only that real R4A run may establish the required current canonical EmpiricalFact:

`540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`

The repair worker MUST NOT issue the R4A transport-seal PASS.

## Return

Write one bounded return artifact under:

`.../R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/I03_SCALE_EQUIVALENCE_REPAIR_R1/00_RETURN.md`

Include:
- exact start SHA;
- terminal SHA;
- exact production/test files changed;
- before/after semantic-equivalence evidence;
- test commands/results;
- exact explanation of removed duplicate work;
- explicit statement that no query/fact/replay semantic identity law changed.

### PASS terminal

`PASS__GT12_R4A_I03_SCALE_EQUIVALENCE_REPAIR_GREEN__NO_SEMANTIC_IDENTITY_DRIFT`

### BLOCK terminal

`BLOCKED__GT12_R4A_I03_SCALE_EQUIVALENCE_REPAIR_CANNOT_PROVE_IDENTITY_PRESERVATION`
