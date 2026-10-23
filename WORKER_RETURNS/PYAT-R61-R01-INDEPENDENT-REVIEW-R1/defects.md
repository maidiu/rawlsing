# R01V independent defects — exact input, observed vs required, contract link

Verdict driver: **REVISE**. Ten independent probe failures below. Each has a
minimal exact input and a contract link. No candidate code or test was edited.

Evidence paths are relative to
`WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/`.

## Blocking R03 prerequisites

### D1. Typed bool and explicit-null condition domains are not representable

- Exact input: `Occurrence(key=OccurrenceKey("bool_condition"), domain=(True, False))`
  and `Occurrence(key=OccurrenceKey("null_condition"), domain=(None,))`.
- Observed: `ValueError: domain values must be exact non-float scalars`
  (`rawlsing_next/universal_grammar/types.py:148-150`). Both constructors reject.
- Required: `INPUTS/CONTRACTS.md` K requires tagged scalar types and explicit
  null versus absent; R01V requires bool/int/null/absent/order collision tests.
  `canonicalize()` already supports bool and None, so this is a candidate-side
  restriction, not an owner limitation.
- Probe: `test_DEFECT_bool_condition_domain_is_representable`,
  `test_DEFECT_explicit_null_condition_value_is_representable`.
- Rank: **blocking R03** (the frontier cannot state the required condition
  identity at all).

### D2. Operation identity does not bind source edition/wave/digest

- Exact input: two inventories with identical `inventory_id`, occurrences and
  policy, but `source_sha256="a"*64, wave="W1", edition="E1"` versus
  `source_sha256="b"*64, wave="W2", edition="E2"`.
- Observed: every operation `op_id` is identical across the two frontiers, while
  `inventory_hash` differs.
- Required: K binds source/dataset/wave/edition/digest. A changed source must
  change operation identity or be a typed refusal; a frontier-level hash is not
  enough because `ScientificOperation.identity_material()` binds only
  `source_inventory=inventory_id` (`types.py:448-464`, `types.py:524`).
- Probe: `test_DEFECT_operation_identity_binds_source_edition_and_digest`.
- Rank: **blocking R03** (cross-source/cold identity collision).

### D3. Operation identity does not bind estimand/weight/design/variance

- Exact input: same inventory identity and `MeasurePlan(measure_id="SAMPLE",
  kind="SAMPLE")`, but `estimand="estimand-one", variance_policy="UNCERTAINTY_ONE"`
  versus `weight_ref="WEIGHT-2", design_ref="DESIGN-2",
  estimand="estimand-two", variance_policy="UNCERTAINTY_TWO"`.
- Observed: all operation `op_id`s are identical. `make_operation()` copies only
  `measure.measure_id` and `measure.kind` (`types.py:518-519`); the operation type
  has no weight/design/estimand/variance fields.
- Required: K binds sample/population estimand, weight/design/uncertainty refs.
- Probe: `test_DEFECT_operation_identity_binds_estimand_weight_and_design`.
- Rank: **blocking R03**.

### D4. Operation identity cannot represent clocks or currentness

- Exact input: introspection of `ScientificOperation.__dataclass_fields__`.
- Observed: missing `observation_clock_ref`, `reference_clock_ref`, `as_of_ref`,
  `publication_clock_ref`, `current_selection_ref`.
- Required: K binds observation/reference/as-of/publication clocks and permitted
  comparisons; `current_selection` exists only on `SourceInventory`, not on the
  operation identity (`types.py:209-289`, `types.py:406-476`).
- Probe: `test_DEFECT_operation_type_carries_clocks_and_currentness`.
- Rank: **blocking R03**.

### D5. Eligibility, execution and result axes are collapsed into one enum

- Exact input: `rawlsing_next.universal_grammar.types.DISPOSITIONS`.
- Observed: `DISPOSITIONS = (ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD,
  UNKNOWN, UNSUPPORTED_RUNTIME, DEFERRED)`; there are no
  `ELIGIBILITY_STATES`/`EXECUTION_STATES`/`RESULT_STATES`; there is no result
  axis at all.
- Required: `INPUTS/CONTRACTS.md` Revision 2 says the three axes must remain
  separate and "a single enum that conflates these axes is forbidden."
- Probe: `test_DEFECT_eligibility_execution_result_axes_are_separate`.
- Rank: **blocking R03** (runtime unsupported/deferred cannot be conserved
  independently of eligibility).

### D6. Native receipt anti-join checks only `rule_id`/count, not condition semantics

- Exact input: actual I05 run with six supported rules. Baseline
  `native_receipt_anti_join` returns `no_drop_ok=true`. Then mutate the predicate
  behind one condition atom from `q_beta=0` to `q_beta=1` while keeping the same
  `rule_id`, re-issue a valid discovery authority and execute the real
  `execute_exact_bounded_discovery`.
- Observed: the mutated run returns the same rule ids/counts;
  `native_receipt_anti_join` returns
  `{'expected_rule_count': 6, 'actual_rule_count': 6, 'missing_rule_ids': (),
  'unexpected_rule_ids': (), 'count_mismatches': {}, 'no_drop_ok': True}`.
- Required: verify requested and returned target, conditions **and values**;
  targeted condition/refutation/restoration must fail the same consumer
  assertion (`INPUTS/CONTRACTS.md` Revision 2; R01V requirement 4). The current
  join reads only `receipt.candidate_identity["rule_id"]`
  (`native_map.py:462-487`).
- Probe: `test_DEFECT_native_receipt_antijoin_binds_conditions_not_just_rule_id`.
- Rank: **blocking R03** (a semantically changed native rule passes no-drop).

### D7. `LoweringRecord` cannot represent the contract fields required for R03

- Exact input: introspection of `LoweringRecord.__dataclass_fields__`.
- Observed: missing `lowering_version`, `discovery_authority_ref`,
  `batch_unit_refs`, `evidence_grade_ceiling`, `typed_refusal`; refusals are a
  free-text `reason` string.
- Required: CONTRACTS 3 defines `LoweringRecord = operation_ref + exact
  predicate/query/DiscoveryAuthority refs + expected candidate/query-role keys +
  Batch unit refs + lowering version + typed refusal + evidence-grade ceiling`.
- Probe: `test_DEFECT_lowering_record_has_required_contract_fields`.
- Rank: **blocking R03 interface** (R03 cannot bind/issue from this record
  without inventing fields).

### D8. Native target cells silently coerce int/bool to string

- Exact input: one target occurrence with `domain=(1, "1")`, one `DIST`
  operation, a catalog with a valid query ref.
- Observed: lowered `rule["target_cells"] == ["1", "1"]`; the declared int 1 and
  string "1" become the same native cell. `_native_cell()` stringifies
  `int`/`bool` (`native_map.py:67-72`).
- Required: tagged scalar identity, no float/string coercion
  (`INPUTS/CONTRACTS.md` K). If current I05 cannot express both types, the
  lowerer must return a typed refusal, not a colliding rule.
- Probe: `test_DEFECT_native_target_cells_preserve_typed_int_vs_string`.
- Rank: **blocking native semantic lowering**.

## Local later proof / declared-limitation candidates

### D9. Topology support is hardcoded before any catalog is consulted

- Exact input: target occurrence `topology="MULTI_SELECT_SET"`; a `NativeCatalog`
  that declares `supported_topologies=("SCALAR_SINGULAR", "MULTI_SELECT_SET")`
  and supports `DIST`.
- Observed: the frontier pre-classifies the operation
  `UNSUPPORTED_RUNTIME` (`enumerate.py:136-137`), so `lower_operation` returns
  `NOT_ELIGIBLE` / `FRONTIER_DISPOSITION_UNSUPPORTED_RUNTIME`, never
  `SUPPORTED`.
- Required: existing capability must not be declared missing solely because the
  enum/native map lacks a branch (R01V requirement 4). If current I05 genuinely
  lacks MR/rank/repeat expressions, this may be a declared limitation, but the
  gate must then cite that owner contract rather than precede catalog lookup.
- Probe: `test_DEFECT_catalog_supported_topology_can_promote_operation`.
- Rank: **later proof / conditional limitation**, not the only reason for
  REVISE.

### D10. `lower_operation` trusts a forged disposition/direction

- Exact input: a real eligible `DIST` operation replaced with
  `direction_ref="FORGED-DIRECTION"` while remaining `ELIGIBLE`; lower with a
  well-formed catalog.
- Observed: returns `SUPPORTED`. `lower_operation` accepts `policy` but never
  uses it (`native_map.py:184-190`), so direction/role grants and frontier
  provenance are not revalidated.
- Required: explicit direction/role identity and semantic target/condition query
  roles. R03 admission may independently protect this boundary; rank as a
  defensive gap, not yet a blocker by itself.
- Probe: `test_observation_lowerer_trusts_operation_disposition_and_direction`.

### D11. Empty `risk_set_refs` are silently treated as unconstrained

- Code path: `role_disposition` intersects only non-empty risk sets
  (`enumerate.py:121-127`). An occurrence that declares no risk set is dropped
  from the intersection instead of making the common-risk state unresolved.
- Required: applicability/risk identity and common risk sets
  (`INPUTS/CONTRACTS.md` K); R01V requires changed risk to be challenged.
- Rank: **medium**, needs an explicit policy decision (empty = unconstrained vs
  unknown); currently undocumented.

### D12. Held inventory entries are free-text, not structured owner reasons

- Code path: `SourceInventory.held: tuple[str, ...]` (`types.py:226`) and
  `inventory_ledger` emits the generic reason
  `"OCCURRENCE_HELD_BY_INVENTORY"` (`enumerate.py:47-48`).
- Required: held semantics need a structured owner reason bound to the affected
  occurrence/operation; free-text held labels do not authorize exclusion.
- Rank: **medium**.

### D13. Recursion/baseline is not independently enumerated

- Code path: `D` is only compared with `branch_depth` (`enumerate.py:152-153`);
  `branch_depth` is set to `depth-1` only for `FORK` (`enumerate.py:366-378`).
  There is no recurrence chain beyond conditioner depth and no baseline-ref
  field in `ScientificOperation`.
- Required: R01V requirement 2 includes recursion/baseline bounds and exact
  identity. If R01 defines recursion only as FORK-over-K conditioners, this must
  be stated; the current types cannot carry a baseline identity.
- Rank: **declared-limitation / clarification**, not the primary verdict driver.

### D14. There is no serialized cold-restore ingress

- Observed: the reviewer cold probe recomputes from the same frozen inventory in
  a subprocess and gets identical content hash, partition root, operation ids,
  disposition counts and pending ids. There is no `from_material`/deserialize
  path, so "cold replay" is deterministic recomputation, not custody restore.
- Required: partition/cold restore must conserve exact operation identities and
  held/unknown/unsupported/pending sets. R04 owns authenticated custody; mark
  this NOT_REACHED at R01 rather than claiming restore.
- Probe: `test_budget_partition_and_cold_recompute_conserve_identity_sets`.

### D15. `native_grammar()` always sets `allow_empty_frontier: False`

- Code path: `native_map.py:424`. A complete inventory with zero eligible
  operations yields no supported rules but still advertises
  `allow_empty_frontier=False`.
- Required: a valid complete empty frontier must be `VALID_EMPTY`, not an
  invented positive/filler. Low severity if I05 ignores this field; clarify.
- Rank: **low / later proof**.

### D16. Author all-missing test is vacuous

- `test_all_missing_observations_do_not_shrink_eligible_frontier` enumerates the
  same inventory twice and asserts an empty local tuple; it admits the
  enumerator has no observation parameter. This does not exercise an all-missing
  observation store or a native missing result. The structural property (no
  values input) is true, but the test does not prove the claimed all-missing
  invariance.
- Rank: **proof gap**, not a separate code defect.

## Independently confirmed strengths

- Ordered target identity: all 4 ordered target tuples for two targets appear;
  `(alpha,beta)` and `(beta,alpha)` are distinct.
- Ordered typed condition identity: all 13 ordered condition tuples for
  K=2 over two int domains appear; order is semantic.
- Exact operation-pair coverage: hand oracle 4 target orders x 5 condition
  orders = 20 pairs matched exactly.
- Duplicate qualified occurrence key refused before construction.
- `NOT_ADMINISTERED` HELD, administration UNKNOWN retained, administrative role
  PROHIBITED, complete admin-only inventory gives `e_pre_count=0` with a root,
  incomplete inventory gives `e_pre=None` plus a cause.
- Budget 3 keeps the full operation set/E_pre and yields exact pending ids;
  bounds are unchanged.
- Count-preserving substitution is rejected by `conservation_report`.
- Direction grants are exact ordered role tuples; reverse direction is
  PROHIBITED until explicitly granted.
- Form/repeat keys stay distinct; MR/rank remain typed runtime-unsupported
  obligations in the ledger.
- Risk-set/measure-kind changes alter `op_id` (the content gap is D3/D4, not
  absence of these two labels).
- Occurrence-order permutation leaves the logical frontier unchanged.
- Author suite replay: 11 passed, 0 failures/errors/skips under reviewer JUnit
  with actual imports.
