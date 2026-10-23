# R61-R01V R2 independent defects — exact input, observed vs required

Verdict driver: **REVISE**. R03 remains **NOT_STARTED**. Candidate code/tests
were not edited. Probes/mutants live only under this return root.

Evidence paths are relative to
`WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/`.

## A1 (blocking R03): conditional JOINT / CO_TRAVEL is lowered SUPPORTED while
## its exact condition value is silently dropped from native execution

- Exact input: the candidate's own TEST_ONLY fixtures, but the reviewer selects
  every eligible SAMPLE `JOINT`/`CO_TRAVEL` operation on ordered targets
  `(q_alpha, q_beta)` with exactly one condition from `q_gamma ∈ {0,1}`
  (`_policy(j=2,k=1,d=0)`). The frontier contains four such eligible operations
  (both classes x both condition values).
- Observed (`evidence/conditional_joint_repro.txt`): for each operation
  `lower_frontier(...).records[0]` returns:
  - `status=SUPPORTED`, `family=PAIR_RESPONSE_COTRAVEL`,
    `form=JOINT_DEPENDENCE`, `expected_candidate_count=1`;
  - `rule_keys=[baseline_atom_id, family, form, joint_template_id,
    marginal_template_ids, rule_id, validation]`;
  - `coverage_roles=('JOINT','MARGINAL_0','MARGINAL_1')`;
  - the exact condition atom (`ATOM-782202...` for `q_gamma=1`,
    `ATOM-7b9f94...` for `q_gamma=0`) is present in `record.atoms` but is
    referenced by neither the rule nor any expected query role;
  - every expected query role's `predicate_ref` is the all-response baseline
    atom `ATOM-d738f6...`, not the condition atom;
  - the two condition values produce the same executed query roles; only the
    `rule_id` (derived from the operation canonical hash) differs.
- Required: `INPUTS/CONTRACTS.md` Revision 2 says the receipt/consumer binding
  must verify requested **conditions and typed values**, not just rule id,
  count, or operation hash. R01V R2 commission item 4 requires the anti-join to
  bind semantic exact targets/conditions/typed values; item 5 requires a sound
  pre-execution `LoweringRecord` for R03. A many-to-one template requires an
  explicit adequate coverage witness. `JOINT`/`CO_TRAVEL` with conditions is
  eligible under the candidate's own policy, so silently mapping it to an
  unconditional joint/marginal query is a false semantic binding. It is not
  enough to put the unused condition atom in `record.atoms`.
- Why it blocks R03: R03 would issue and execute a joint-dependence candidate
  for an operation that requested a conditioned joint distribution. The
  resulting facts/validation would be for a different scientific operation.
  The defect is in R01's lowering, not in R03 issuance/Batch or R04 custody.
- Minimal probe: `probes/test_r01v_r2_reviewer.py::test_conditional_joint_condition_has_native_semantic_role`
  (fails as required; `replay/own_probes.log`).
- Exact finite repair options (choose one, in R01 scope):
  1. Typed-refuse `JOINT`/`CO_TRAVEL` operations with non-empty conditions until
     the current catalog/owner exposes exact conditioned joint/marginal refs
     and objects (smallest safe repair; keeps the scientific operation eligible
     but runtime-unsupported with a typed reason).
  2. Extend `NativeCatalog` with conditioned joint/marginal refs keyed by the
     ordered condition tuple and use those refs in the rule.
  3. Compose a derived exact predicate from the current I05 predicate
     primitives (`make_empirical_predicate` / the owner's combine operation),
     use it as the `JOINT` role baseline and marginal condition, and add its
     exact ref/object to the grammar.
  Do not claim current I05 supports conditional joint by adding an unused atom.

## A2 (medium/high, R03 interface hardening): lowering accepts a forged
## operation `op_id` that is not its canonical identity

- Exact input: a real eligible SAMPLE `DIST` operation, replaced with
  `op_id="urn:r61:op:forged-identity"`; all other fields unchanged; a
  well-formed catalog.
- Observed: `lower_operation(...)` returns `status=SUPPORTED`, `reason=None`.
  `_policy_revalidated` checks source/measure/policy/role/direction/risk/unit/
  form/topology/scope/administration but never checks
  `operation.op_id == "urn:r61:op:" + operation.canonical_hash`.
- Required: the commission asks lowering to validate operation/frontier
  identity, not only direction; R03 will bind planned Batch units and receipts
  to operation IDs. A forged frontier ID is not the canonical operation.
- Probe: `test_forged_operation_id_is_not_accepted_as_exact_identity` (fails).
- Rank: not the sole verdict driver (normal R01 output has canonical IDs), but
  it should be fixed in the same repair because it is a one-line identity
  revalidation and prevents an unsound R03 binding boundary.

## A3 (medium): an unsupported-only scientific frontier is advertised as a
## valid empty native frontier

- Exact input: one eligible target operation, a catalog with
  `supported_claims=()`; `lower_frontier` yields unsupported operation IDs.
- Observed: `plan.native_grammar()["allow_empty_frontier"] is True`
  (`lower_frontier` sets `allow_empty_frontier = not bool(supported_operation_ids)`).
- Required: D15/VALID_EMPTY must mean an independently complete empty frontier,
  not "all operations happened to be unsupported". Unsupported scientific
  obligations must remain explicit; they may not be conflated with a valid
  empty native grammar.
- Probe: `test_unsupported_only_frontier_is_not_declared_valid_empty` (fails).
- Rank: medium; R03 has the unsupported ID list, but the flag is misleading and
  should be `allow_empty_frontier = (no frontier operations and no unsupported
  operations)` (or an explicit three-way flag).

## A4 (medium/declared-limitation): recursion/baseline is still conditioner
## depth under new field names

- Exact input: policy `J=1, K=3, D=3` (and separately
  `recursion_relation_ref="REC-1"`, `baseline_policy_ref="BASE-1"`), three
  binary conditioners.
- Observed (`evidence/recursion_diagnostic.txt`): every `FORK` row has
  `branch_depth == recursion_depth == len(conditions)-1`; no FORK exists at
  condition depth 0/1; `baseline_ref` is the parent operation's `op_id`; the
  policy `baseline_policy_ref` never appears as an operation field; the maximum
  enumerated recursion depth is `K-1`, so `D=3` is not independently exercised.
- Required: R01V R2 commission item 6 / D13 asks for declared
  recursion/baseline identities and finite issued bounds without equating
  conditioner depth with recursion. The new fields are carried, but the
  enumeration still aliases the two depths and does not consume a recursion
  relation or baseline policy as a separate axis.
- Rank: medium. If R01's declared grammar defines FORK recursion as exactly
  FORK-over-K conditioners, state that limitation explicitly and do not claim
  D13 "PASS"; otherwise enumerate the separate recurrence/baseline chain.
  This is not used to inflate the verdict beyond A1.

## D1–D8 replay status (independent)

The prior reviewer's probe file was retained as history and adapted only for
the R2 public schema/behavior changes and its path-derived cold helper
(`probes/prior_test_r01v_independent.py`; adapted REPO_ROOT and three obsolete
assertions: topology now lowers by catalog lookup, forged direction now
refuses, MULTI_SELECT_SET is eligible at the frontier). Result: **20 passed**,
exit 0 (`replay/adapted_prior_probes.log`, `...junit.xml`).

- D1 typed bool/null domains: pass.
- D2 source/dataset/wave/edition/digest in operation identity: pass.
- D3 estimand/weight/design/variance in operation identity: pass.
- D4 clocks/current-selection fields and identity: pass.
- D5 separate eligibility/execution/result axes: pass (structural and budget
  PENDING).
- D6 CONDITIONAL/DIST receipt anti-join binds condition semantics: pass in the
  reviewer native case below; condition mutation fails, restoration passes.
- D7 LoweringRecord required fields: pass.
- D8 typed native cells/int-vs-string and non-injective codec refusal: pass.

## D9–D16 disposition at R01 grain

- D9 topology pre-gate: repaired; catalog can promote MULTI_SELECT_SET.
- D10 forged direction: repaired for direction/roles/risk/unit/form/topology/
  scope/administration; A2 shows canonical op_id is still unchecked.
- D11 empty risk sets: explicit `UNKNOWN` default vs `UNCONSTRAINED` policy.
- D12 structured held reasons: `HeldRecord` + authority; free text is UNKNOWN.
- D13 recursion/baseline: A4, not genuinely independent of conditioner depth.
- D14 serialized cold restore: **NOT_REACHED** (R04 owner). Deterministic cold
  recompilation passes; no serialized ingress is claimed.
- D15 valid empty: repaired for a truly empty frontier; A3 shows unsupported-only
  conflation.
- D16 all-missing: vacuous test removed; current synthetic I03 all-missing
  response is a typed integrity refusal before I05; positive all-missing native
  result remains NOT_REACHED and is not claimed.

## Independently confirmed strengths

- Author suite replay: 18 passed, 0 failures/errors/skips under reviewer JUnit
  with actual imports (`replay/author_suite.log`).
- Exact ordered target/condition identity sets, duplicate refusal, admin
  false/unknown, structured holds, budget pending IDs, partition/cold
  recomputation, count-preserving substitution refusal (adapted prior suite).
- Typed bool/int/string/null/absent identities and typed native cells; explicit
  injective codec; non-injective refusal.
- Actual I05 `execute_exact_bounded_discovery` with synthetic C11/I03: baseline
  positive, condition-atom mutation with same rule id fails the reviewer-owned
  exact candidate/query-role join and the candidate anti-join, restoration
  passes, and a cold subprocess reproduces the same case
  (`replay/native_positive.log`; `probes/test_r01v_r2_reviewer.py`).
- Direction grants, source/measure/clock identity, and axes conservation.
