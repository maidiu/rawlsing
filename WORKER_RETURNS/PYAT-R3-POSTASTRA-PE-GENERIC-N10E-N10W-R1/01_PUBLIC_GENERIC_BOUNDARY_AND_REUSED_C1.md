# 01 — Generic public boundary and reused C1

**POST-ASTRA R3 PE candidate; TEST_ONLY source-free court.** Grade:
`CANDIDATE_TEST_ONLY__NOT_OPERATIVE_N9__NOT_SCIENCE__NOT_V3__NOT_SOURCE_OR_E_PRE_ISSUER__NOT_MODEL_USE_ISSUER__NOT_ADOPTION`.
No original survey, no real-source C11, no model/actor run, no N9 current, no
V3 wake, no canonical merge. Fractions are exact arithmetic on synthetic
fixture laws at their declared empirical grain only.

## 1. What was reused versus what is new

| Component | Status | Exact identity |
|---|---|---|
| C1 analytical composition `compose_positioned_subject_possibility` | REUSED UNCHANGED (accepted) | `rawlsing_next/pre553_analytical_composition.py` |
| C1 lower generic multi-binding law `_all_bindings` | REUSED UNCHANGED (accepted) | same module; `query.conditioner_bindings` |
| C1-02 multi-conditioner witness `ConditionValueBindingWitness` | REUSED UNCHANGED (accepted) | same module; `C1_CONDITION_VALUE_BINDING_WITNESS@2` |
| Public consumer `evaluate_positioned_subject_possibility` | REUSED UNCHANGED (accepted) | `rawlsing_next/source_backed_positioned_subject_possibility.py` |
| N10E public facade `provide_empirical_possibility_slice` / `_single_binding` | REUSED UNCHANGED (accepted) | `rawlsing_next/pre553_empirical_possibility_provider.py`; its accepted C1-01 single-conditioner grain is untouched |
| I03 empirical query/predicate builders | REUSED UNCHANGED (read-only) | `rawlsing_next/tests/test_pre553_empirical_query.py` helpers |
| C1-02 multi-binding witness builders | REUSED UNCHANGED (read-only) | `rawlsing_next/tests/c1_at08_at13_fixture.py` helpers |
| **Generic world-situated seam** | **NEW versioned candidate** | `rawlsing_next/pre553_postastra_pe_generic_world_possibility.py` — `POSTASTRA_PE_GENERIC_WORLD_SITATED_POSSIBILITY@1.0.0` |
| Source-free fixture + two independent laws | NEW test-only | `rawlsing_next/tests/test_postastra_pe_fixture.py` |

**No adopted owner code was modified.** The legacy public N10E schema is
unchanged and its existing suite still passes 43/43 (regression recorded in
`02_EXECUTED_CONSUMER_LAW_AND_RECEIPTS.json`).

## 2. The versioned generic boundary

`GenericWorldSituatedRequest` carries: opaque generic `subject_ref`, `target_ref`,
1..n `ConditionerBinding`s, a `role_direction`, `native_unit_ref` /
`analysis_unit_ref`, `denominator_basis_ref`, `operation_authority_ref`,
`model_use_ref`, an `N9WorldDependency` (immutable selected snapshot + as-of +
dependency IDs) and `request_time`. It derives the exact accepted public
`PositionedSubjectPossibilityQuery` and calls the accepted C1 composition — the
seam adds **no estimator**.

`GenericWorldSituatedReceipt` binds: the N9 world dependency IDs, the
`inference_lane`, the conditioner count/IDs, the native/analysis unit, the
denominator basis, model-use and model-rule hashes, producer query/predicate/fact
identity, the consumer result identity and exact geometry, a proxy-lane flag, and
the epistemic ceiling.

## 3. Role/target reversal law (P(A|D) is not P(D|A))

- `FORWARD_SUBJECT_TO_TARGET` / `MULTI_CONDITION_INTERSECTION`: conditioners bind
  subject coordinates; the target is a distinct coordinate. Multi requires ≥2
  conditioners intersected in one exact C1 condition predicate.
- `REVERSE_TARGET_VALUE_TO_SUBJECT`: the subject is fixed at a target-coordinate
  value and the target is a distinct coordinate. Requires an explicit positively
  scoped `role_reversal_authority_ref`; without it the seam returns
  `REVERSED_UNAUTHORIZED_ROLE`. Reversal needs its own valid target topology,
  risk set, denominator and operation/design authority — it is not a relabeling.
- Conditioning on the target coordinate itself is refused
  (`SELF_TARGET_CONDITIONING`).
- Reversal is demonstrated live: `P(POSITION | ANSWER=yes) = 3/4` on Law A while
  the forward multi-binding slice is `9/10`; the two directions carry distinct
  target topology and denominators.

## 4. Genericity: no parent nouns upstream

The request schema has no `is_father_query`, no parent/household/dyad noun and no
type/psyche field. Parent-flavored and conception-scenario usage appear only as
downstream TEST-ONLY `requested_projection` scenario labels
(`TEST_ONLY_FAMILY_CARE_CONTEXT_*`, `TEST_ONLY_FINITE_CONCEPTION_SCENARIO_*`).
A request whose projection smuggles parent-assignment or type tokens is refused
at construction (`ARTIFICIAL_PARENT_SAMPLING_REFUSED`). A new analysis unit
(household/dyad) is refused (`NEW_UNIT_NOT_AUTHORIZED`): same-respondent joint is
not household dependence and neither is a causal effect.

## 5. C1 reuse, not a new statistical estimator

The seam calls `compose_positioned_subject_possibility`, which already consumes
`_all_bindings` (the full conditioner tuple), verifies the multi-conditioner
custody witness, executes the exact empirical query and builds the generated
slice evidence. The public consumer `evaluate_positioned_subject_possibility`
then applies the governed exact-conditional-with-walkback model rule. The seam
never accepts a caller-supplied `PossibilitySliceEvidence`, never accepts
precomputed geometry, and never smooths/interpolates/extrapolates.

## 6. Inference-lane distinction (W10 carriage is not joint conditioning)

- `N10E_CONDITIONED_EMPIRICAL_INFERENCE` — an exact empirical slice was actually
  computed by C1 at the declared grain for the requested conditioner set.
- `WORLD_ONLY_ROUTE_ELIGIBILITY` — only world/dependency identity was bound; no
  empirical probability is produced.
- A receipt that carries both world premise and N10E slice declares the N10E lane
  for numeric content and labels world content as non-probabilistic carriage
  (`world_carriage_is_not_route_probability=True`); route probabilities are never
  produced and never multiplied across grains.

## 7. N9 world dependency (TEST_ONLY; never invented current)

Every request binds an immutable selected N9 snapshot ref, an immutable as-of
coordinate and declared selected/asof dependency IDs. The seam never resolves or
invents N9 current. `INVALIDATED` current yields a typed refusal; an as-of at or
after the request time yields `FUTURE_TIME_AVAILABILITY_REFUSED` (later
publication is not earlier knowledge).
