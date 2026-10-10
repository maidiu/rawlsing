# HQ272 R01 — Source-native true conditional denominator and executable owner court

**Disposition:** HOLD_TRUE_CONDITIONAL_UNPROVED at the existing GT12 frozen code grain. This is a **missing binding/permission/product** finding, not a proof that I03 lacks generic conditional capability or that source cannot support the question.

## 1. Correct symbolic experiment — no fabricated observed counts

Let each `r` be one uniquely scoped `(COUNTRY, RESPNO)` respondent on the exact same authenticated C11 release, not joined to another person. Let `E_i(r)` be independently proven eligible/applicable AND exposed for item `i`; `V_i(r)` mean an actually substantive native 0/1 answer for Q86A/B/C (do **not** treat 9 DK, 997 Not asked, 998 Refused or -1 Missing as substantive). Define `Y=Q86A`, `A=Q86B`, `B=Q86C`, with fixed values Y=1, A=0, B=0. Let `C` be the **independently proved** source-specific common eligibility/exposure cohort for all three—not automatically the current GT2 frozen 19,210 persons.

For a valid *same-base progressively nested comparison*, predeclare complete-case analysis scope:

`S = {r in C | V_Y(r) AND V_A(r) AND V_B(r)}`.

`R_1 = {r in S | A(r)=0}`; `N_1 = #R_1`; `K_1 = #{r in R_1 | Y(r)=1}`.

`R_2 = {r in S | A(r)=0 AND B(r)=0}`; `N_2 = #R_2`; `K_2 = #{r in R_2 | Y(r)=1}`.

Then the precise raw conditional probabilities are `q1=K_1/N_1 = Pr(Y=1 | A=0, r in S)` and `q2=K_2/N_2 = Pr(Y=1 | A=0,B=0,r in S)`. These denominators are **condition-specific**; `R_2 subseteq R_1 subseteq S subseteq C`. They are not in general the `|C|=19,210` baseline and cannot be substituted with a 3-cell numerator divided by that frozen cohort. `N_1=0` or `N_2=0` yields typed abstention/zero support, **not a numerical probability, not empirical null and not a supported reversal**. Small subgroup support and uncertainty must be typed and the lack of design-based uncertainty explicit.

If instead the natural two-item baseline uses `S_{YA} = C_{YA} ∩ V_Y ∩ V_A` and the three-item refinement uses `S_{YAB}= C_{YAB} ∩ V_Y ∩ V_A ∩ V_B`, then their denominators come from **different complete-case source populations**. They are individually potentially valid descriptions but comparing q1 to q2 as a purely `B`-conditioned change confounds the result with Q86C exposure/nonresponse restriction. Report both sample/denominator identities, or adopt the exact common-three-item S as above. Original 9/997/998/-1 must stay distinct in separate excluded-state ledgers; no silent dropping, coding equivalence or missingness correction.

An alternative exact joint-cell calculation could reconstruct the two conditionals from a complete three-item joint support table by summing cells: `N_1=sum_{y,b in {0,1}} n_{y,0,b}`, `K_1=sum_{b in {0,1}} n_{1,0,b}`, `N_2=sum_{y in {0,1}} n_{y,0,0}`, `K_2=n_{1,0,0}`; **ONLY** when all cells share one proved complete-case S, every cell is source-native/identity-valid, and a separately authorized projection/normalization consumer binds those exact sums and zero-state policy. Possessing a tuple of three ordered targets alone does not perform these projections.

## 2. Code-forensic court — what is actually executable today

**Generic PRE553 I03 executor supports real conditioning in principle.**
- `rawlsing_next/_pre553_query_predicate.py` blob `8590bacf464b2c61f319f581820a3af76ed1e60c`: `_leaf_match` 225–251 `SURVEY_RESPONSE_EVENT` typed exact response predicate, `ROUTING_APPLICABILITY_STATE` 253–271, and `_eval_predicate` 366–404 boolean `AND` evaluation *per same scoped respondent*; requires exact question/value/semantics and authority.
- `rawlsing_next/_pre553_query_eval.py` blob `f808dfcd2008cc71e9203de3cadf1abe14223974`: `_evaluate_index_group` 370–454 iterates one source's `RespondentIdentity`, checks **all target-specific routing**, then `_eval_predicate`, appends *only predicate-passing respondents* to `denominator_members`, with `raw_denominator=len(denominator_members)`, then exact target response cells. `_build_fact` 616–648 retains conditional predicate ref, denominator member refs, uncertainty, authority, risk/source and replay. Hence this engine is not intrinsically restricted to the unconditional 19,210 denominator.
- `rawlsing_next/pre553_empirical_query.py` blob `03facecf70890bfd13b80418620d274cbcd69d02`: `execute_empirical_query` 373–539 requires matching actual predicate/query refs, positive grammar and target-use authority and exact sealed release; yields one typed fact per single universe, not a model-use grant. `_pre553_query_common.py` blob `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92` `_parse_target_plan` 311–408 is arity-polymorphic in **target cell tensor**.
- `rawlsing_next/pre553_empirical_objects.py` `EmpiricalFact@1.0.0` maintains raw numerator ≤ denominator and typed zero/nonpositive claims. No design-weighted/uncertainty authority issued here.

**But actual frozen GT1/GT2 wrapper is *not* condition-capable for this question.**
- `rawlsing_next/wave1_gt12_i03_positive_facts.py` blob `067628dc6605f28be68bdcd86ef57b02a0db4348`, lines 530–569: `_predicate_for_members` always constructs **ONE `DERIVED_BRANCH_COHORT` leaf** over exact frozen common member refs. It contains **no Q86B=0 or Q86C=0 survey-response predicate**.
- lines 584–643: `_query_for_targets` dynamically allows `len(targets)` as *joint target arity*, with same `condition_predicate_ref=predicate.ref`, `risk_set_type=COMMON_ELIGIBLE_RISK_SET` and raw measure. This does **not** prove either q1 or q2 conditional selector.
- lines 646–692: only `build_gt1_q86a_i03_plan` unary Q86A and `build_gt2_q86a_q86b_i03_plan` ordered pair Q86B×Q86A are present. Frozen `R5Q86I03ExecutionBinding` lines 138–151 has no q86c or GT3 permission; routing/member validation lines 342–466 validates only Q86A/B.
- lines 695–734: `execute_gt12b_i03_plan` delegates to the generic exact I03 engine, returning one `EmpiricalFact` containing one complete cell projection; replay is real but **a one-fact 3D joint is NOT two actually emitted conditioned facts**. The GT2 use term “Q86B conditioner” is a downstream Field Forge relation-role name, not a `SURVEY_RESPONSE_EVENT` condition in I03.

**First exact missing executable edge:** an owner-native **conditional-query plan** on the accepted C11 release, with independently proved Q86C routing and exact respondent-value predicates, separate q1 and q2 query/predicate identities, distinct denominator closures and replay. The generic engine can provide its denominator operator **if** the missing predicate/operator semantics and target-use/grammar permission are formally bound. Alternately a separately typed, permissioned I03 joint-to-conditional projection can consume a qualified 3D table and preserve numerator/denominator ref closure. No source-backed implementation or actual C1 conditional-slice consumer is proven in the frozen GT12 code. Merely appending Q86C to `target_refs` and reusing `_predicate_for_members` **fails** q1/q2.

**Existing conditional C1/EE14 integration:** source-free C1/G1 analytical/serving owner work is acknowledged in HQ271–272, but this review finds **no demonstrated code-bound specific adapter** selecting `Q86B=0` then `Q86B=0 AND Q86C=0` from a real R5 admitted query into an actual C1 progressively conditioned result. Treat C1 generic source-free fixture competence as separate from R5 source-backed conditional occupancy. Need exact `C1` consumed input/output API and positive q1/q2 replay proof before granting application adequacy.

## 3. Preconditions and hostile test cases for a lawful successor

1. **Q86C routing is not proxied by Q86A/B answers or Q86 block common wording.** Demand one Q86C `RoutingEligibilityFact` per scoped respondent and `EXPOSED__PROVED` on any claimed member; prove/rehash resulting source-native 3-item coexposure set (which may differ from the GT2 set). `997` is not evidence of positive exposure.
2. **Conditional membership test:** two separately typed `EmpiricalPredicate` structures: `AND(S, Q86B EQ 0, Q86A/Q86B/Q86C substantive-valid policy)` and `AND(S, Q86B EQ 0, Q86C EQ 0, substantive-valid policy)`, both exact `EXACT_SCOPED_RESPONDENT` via one release. Ensure admissible `S` is already exactly defined/serialized.
3. **Positive witness and typed counterexamples** on permitted source-free fixture: q1/q2 positive with *different* selected `denominator_member_refs` and correct numerators; no leaked respondent from other countries; altered Q86C-only exposure or missing code triggers expected membership differences; zero denominator, zero cell, underpowered/unknown are not illicitly promoted.
4. **No denominator cloning:** any producer returning q1/q2 denominators as 19,210 for arbitrary value conditioning without exact member-equality proof must fail, as must dividing joint cell count by frozen common exposure count.
5. **No type/policy substitution:** non-substantive 9/997/998/-1 all preserved, eligibility and respondent response separate; zero denominator not a supported probability; weighted or pooled country inference not silently switched on.
6. **No fake C1:** fact-producing I03 ≠ actual progressive possibility serving; prove a typed C1 conditional consumer with source-backed input, permission, replay and alternative configurations or report it absent.

**Decision:** existing same-respondent target-tuple **capacity** is affirmative, but **`q(Y|A)`→`q(Y|A,B)` source-backed positive product is NOT DEMONSTRATED**; `HOLD_TRUE_CONDITIONAL_UNPROVED`.
