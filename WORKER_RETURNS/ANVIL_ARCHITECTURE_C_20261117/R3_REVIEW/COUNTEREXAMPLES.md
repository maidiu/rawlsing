# R3 claim-targeted counterexamples

These are exact source/claim failures, not cardinality objections.

## C1 — FF01 k>2 and reverse-distribution overclaim

**R3 claim:** `R3_ARCHITECTURE_DECISION.md` §6.4 says
`ExactConditionalSupportProfile` “already models conditional support” and
“the R3 contract extends the route to `P(Y1..Yk|D,U,W)` and reverse
`P(D|Y,U,W)` … ordinary/minority alternatives, role/position contrasts,
branch/recursive conditionals …”. `R3_CAPABILITY_ACCOMMODATION.tsv`
`R3-CAP-04` repeats `P(Y1..Yk|D,U,W)` and reverse and grades the route
`CONCEPTUALLY_ACCOMMODATED`.

**Actual code** (`rawlsing_next/field_forge_conditional_support.py`,
product `cea2d4d`):
- module header: “**Bounded FIELD FORGE conditional-support count relation for
  GT2**”; it “consumes an already-produced PRE553 I03 **two-target** joint
  EmpiricalFact”; it “**does not calculate ratios**” (lines 1–8).
- fixed roles `CONDITIONER_SOURCE_NATIVE_VARIABLE = "Q86B"`,
  `TARGET_SOURCE_NATIVE_VARIABLE = "Q86A"` (lines 34–35);
- `_query_component_material` requires exactly
  `[Q86B CONDITIONER, Q86A TARGET]` (lines 136–141);
- `ExactConditionalSupportProfile` has only `conditioner_ref`/`target_ref`,
  `conditioner_domain`/`target_domain`, and
  `conditional_count_profile` (lines 359–380);
- semantic projection fixes `"participant_cardinality": 2` (lines 432 and
  530);
- `produce_exact_conditional_support_profile` is the only producer (line 467).

**Failing route:** the existing function cannot produce a k>2 conditional,
a reverse `P(D|Y,U,W)` with its own risk basis, role/position contrasts, or
branch/recursive conditional support. A k>2 F1–F4 joint fact is not a
substitute for the missing FF01 derived product; the profile is a two-target
count relation, not a conditional distribution.

**Smallest correction:** split the claim into two artifacts and routes:
(a) `FF01-2` — the exact existing Q86B→Q86A two-target count profile, with
its real provenance/permission ceiling; (b) `FF01-k` — a versioned derived
conditional-support product contract that names the k-component joint fact,
role/key map, numerator/denominator rule, reverse risk basis, minority/
branch/recursion, uncertainty/coverage and first consumer. Until (b) exists,
grade k>2/reverse `CONDITIONAL_EXTENSION` or `OWNER_HELD`, not
`CONCEPTUALLY_ACCOMMODATED` via the existing function. Add a corresponding
falsifier and `R3-RES-*` entry.

## C2 — Source-observability overclaim: C11 does not itself preserve all listed native fields

**R3 claim:** `R3_ARCHITECTURE_DECISION.md` §6.1 says “C11 preserves native
item/option/form/routing/version, raw/canonical values, respondent/household
namespace, occurrence/rank/repeat, typed absent/unknown, weights/design and
source/time/authority.” `R3-CAP-01` requires original-language
item/option/form/routing/version and respondent/household namespace.
§6.3/§7 says C11 preserves “design” and “uncertainty material.”

**Actual persisted schema at `cea2d4d`:**
- `QuestionVariableBinding` (pre553_c11_integrity.py:201–209) has
  `empirical_universe_ref`, `native_question_ref`,
  `instrument_question_version`, canonical/component refs or typed absence,
  `semantic_authority_ref`, `topology_authority_ref`. It has no option,
  form, ballot or routing field.
- `RoutingEligibilityFact` (pre553_empirical_objects.py:548–555) has
  `question_or_target_ref`, `risk_set_ref`, `routing_rule_ref`,
  applicability/routing states, parent predicates and member-set replay.
  It preserves routing state/refs, not original-language option/form content.
- `EmpiricalUniverse` (pre553_empirical_objects.py:503–512) has
  `instrument_release`, `respondent_namespace`, `sampling_design_regime` and
  `target_population_and_sample_frame`. It has no household/roster namespace
  and no PSU/strata/variance field.
- `WeightMeasureFact` (pre553_empirical_objects.py:559–567) has weight value/
  state/source, `design_authority_ref`, `estimand_authority_ref`,
  normalization rule and effective scope. It has no PSU, strata, replicate
  weight or design-variance field.
- `EmpiricalFact` (pre553_empirical_objects.py:696–706) has
  `uncertainty_method_or_typed_state` (a method/ref/state), not a numeric
  variance/interval.

**Failing route:** a reader cannot tell which requested meanings are C11
bytes, which are resolved through an external source/codebook/artifact, and
which are unavailable. `native_question_ref` may point to an external codebook,
but the R3 decision asserts C11 preservation. Household/roster identity is not
in the 13-family canonical body; design variance/PSU/strata are not in
`WeightMeasureFact`; numeric uncertainty is not in `EmpiricalFact`.

**Smallest correction:** add an exact `R3-RES-023` `INSPECTED_CODE` field map:
C11 native refs/version/routing state; external source edition/codebook/
questionnaire for original-language option/form/ballot content; typed absence/
source hold for household/roster unless a source-specific projection is
defined; `EmpiricalUniverse` design regime/frame labels and
`WeightMeasureFact` design/estimand authority refs only; PSU/strata/variance
and numeric uncertainty are external F6 inputs or explicit holds. Correct
§6.1/§6.3/§7 and `R3-CAP-01`/`R3-CAP-03` accordingly.

## C3 — Architecture decision does not cite research IDs

**Requirement:** the commission and addendum require the architecture decision
to cite the `R3-RES-*` findings actually relied upon, not a parallel ledger.

**Actual:** `R3_ARCHITECTURE_DECISION.md`, `R3_CAPABILITY_ACCOMMODATION.tsv`
and `R3_FALSIFIERS_AND_COST.md` contain **zero** `R3-RES-*` identifiers. The
22-entry ledger has `cross_refs` to `R3-CAP-*` and a `reuse_beyond_anvil`
field, and the synthesis cites R3-RES IDs; the decision does not.

**Failing route:** a reader of the decision cannot recover which research
finding supports which accommodation claim. The ledger is substantive but
parallel to the decision, contrary to the explicit custody requirement.

**Smallest correction:** add a `research_refs` column to the capability TSV
and explicit `R3-RES-*` citations in each decision section; add reverse links
from the FF01/source-field/access-view findings. No new research is required.

## C4 — Access-view claim is stronger than the research’s own grade

**R3 claim:** `R3-CAP-02`/`R3-CAP-06` grade the respondent-major and
question-major views as `CONCEPTUALLY_ACCOMMODATED`/`MODIFY` access
architecture; `R3_ARCHITECTURE_DECISION.md` §4.1 keys the respondent view by
`(universe, respondent, question/native, occurrence/rank/repeat)` and the
question-major view by selector/denominator roles.

**Actual research entry:** `R3-RES-021` is explicitly
`OPEN_CONDITIONAL_ACCESS_EXTENSION`, says the gain is unmeasured and depends
on Q dominance, and requires exact candidate streams to the existing
evaluator. The current `EmpiricalCoordinateFact` has
`native_coordinate_ref`/`effective_or_reference_time`; `WeightMeasureFact` has
`weight_basis_id`/`effective_scope_ref`; `RoutingEligibilityFact` has
`question_or_target_ref`/`risk_set_ref`. No exact join key or adapter to
`execute_empirical_query` is supplied.

**Failing route:** the view is a plausible direction but not a concretely
keyed/bound input contract; `CONCEPTUALLY_ACCOMMODATED` overstates an
`OPEN_CONDITIONAL_ACCESS_EXTENSION`.

**Smallest correction:** supply the exact per-family key/ref map and the
native-evaluator adapter contract, or downgrade the view-specific capability
to `CONDITIONAL_EXTENSION` while retaining the architectural direction.

## C5 — F6 design variance/PSU/strata are not named as external

**R3 claim:** §6.3/§7 says C11 preserves “source/frame/design/weight/
uncertainty material”; `R3-CAP-03` requires design/estimand variance but its
source column names `EmpiricalUniverse`, `QuestionVariableBinding` and
time/authority, not PSU/strata/variance.

**Actual:** `WeightMeasureFact` has design/estimand authority refs, no
variance/PSU/strata; `EmpiricalFact` has an uncertainty method/state, not a
numeric interval; `EmpiricalUniverse` has design-regime/frame labels.

**Failing route:** F6 is correctly owner-held, but the exact design hold is
not named; a reader may infer that `WeightMeasureFact` contains design
variance/PSU/strata.

**Smallest correction:** state explicitly that C11 preserves the design/
estimand authority refs and universe/frame labels, while PSU/strata/replicate
weights/design variance and numeric uncertainty must be supplied by the F6
owner or typed-absent; add this to the capability row and ledger.
