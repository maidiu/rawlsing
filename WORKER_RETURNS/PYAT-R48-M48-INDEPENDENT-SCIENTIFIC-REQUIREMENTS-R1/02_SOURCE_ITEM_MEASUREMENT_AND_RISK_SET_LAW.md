# Measurement, administration and risk-set law

Proposed objects below are decision-ready contracts, not issued source facts. Distinguish three uses of U: `U_item` (administered item-instance inventory), `U_unit` (sampled respondent/household units), and `U_app(i)` (units applicable to occurrence i). Never use one integer for all three. A frame population is neither the achieved sample nor the valid-response denominator.

`SourceScope` must bind family_uid, wave_uid, release/edition digest, country, fieldwork interval, language/form/ballot/module, shard partition and overlap rules, unit schema and source codebook identity. Family-scoped aliases are references, never authority to select the newest release. Country/year fields can be scope coordinates without being attitude targets. Wave is not a single interview date.

`ItemOccurrence` binds scope, native item and option codes, source wording reference, unit/role, battery/member/loop/rank identity, administered form and route expression, response topology/domain, state map, semantic use/disposition, authority/current-selection refs, and evidence locations. Repeated household members remain separate occurrences or a governed array with an explicit unit transform. A household proxy report is not a second selected-adult self-report. Multiple-response selections use set incidence; ranks use ordered alternatives and tie rules; repeated occasions retain order and dependence. Do not turn option slots into independent people or a rank number into attitude intensity.

State map must distinguish substantive response, DK, refusal, item nonresponse, not asked by design, routed inapplicable, structural omission, unavailable/undecoded and invalid value. Special states may be scientifically interesting **as special-state targets** if approved; they do not become substantive agreement. Numeric code order, negative sign, blank, and textual similarity cannot determine state/polarity or equivalence. V550 retains governed response semantics and explicitly declines to mint a row contract from an arbitrary map hash [V550_RESPONSE/V550_DIST].

For operation o with targets T and conditioners C, define:

```
A_o(r) = frame_membership(r) AND form_assignment(r)
         AND each applicable_route(r, i), i in T union C
R_o(r) = A_o(r) AND authorized_unit_linkage(r) AND authorized_state_policy(r,T,C)
D_o(r) = R_o(r) AND predicate_C(r)
```

All predicates use three-valued logic: TRUE/FALSE/UNKNOWN. Unknown administration is not false and is never coerced into unconditional. Contradictory source decisions raise an integrity/authority conflict. Logical route impossibility is a pre-execution disposition with proof; an observed empty cell is a post-execution outcome. Store both the administration base and complete-response denominator, with losses by state. A composite target normally uses the **intersection** of component-applicable units, but whether that estimand is meaningful must be decided; intersection alone is not a scientific argument. Domain variance may need full design records with domain indicators even when numerator/denominator use only domain members.

`MeasurePlan` binds descriptive achieved-sample or population target, weight basis, household/person/ballot/subsample role, calibration and nonresponse corrections, design strata/PSU/replicate weights, variance method and degrees-of-freedom/lonely-PSU rule. Generic software may evaluate supplied masks, weighted sums and design formulas; it may not choose a weight by spelling or substitute unit weights under a population claim. Missing weight/design can leave a separately authorized **sample description** executable while the population/uncertainty variant is held. No automatic rescue by renaming the estimand after seeing results.

For a governed nonnegative-weight descriptive ratio:

`p_hat(y|C,R) = sum_r w_r 1[D_o(r)] 1[Y(r)=y] / sum_r w_r 1[D_o(r)]`.

Zero denominator gives no probability. Zero numerator with positive eligible denominator is an observed zero, not impossibility. Invalid/missing weights retain affected membership and reason; never silently fill them with zero. Replicate-weight negative values require the source's specific variance procedure; do not apply a generic nonnegative analytic-weight rule to all replicate systems. Kish `(sum w)^2/sum(w^2)` is weight concentration, not a substitute for full design variance or a universal sample-size threshold [EFFECTIVE_N].

Survey-method owner must decide finite fields: exact frame/unit, form/module and route code semantics, nonresponse estimand/treatment, weight/design role and population target, allowed aggregation/recodes, unit-link meaning, and evidentiary ceilings. Code derives route dependency closure, feasible code combinations, mask intersections, contradictions and counts **from** those decisions. Semantic judgments are not required anew per generated query when an accepted rule already covers it.

Historical grounding [W47/PREMAIN/P10]: 18,276 implementation accounting includes 14,386 typed unresolved routing dispositions at that historical cut; 2,104 affirmative source bindings never implied full routing closure. Source grouping and J candidacy are distinct. Q86B→Q86A retained F5 has context-only permission [F43]. LiTS history includes no-weight UNAVAILABLE outcomes [S44]. These are actual adjudicated examples, not invented instrument facts. Household/split-ballot/MR/rank cases in 06 are declarative canaries grounded in required type classes and existing fixture topology; no claim that a specific uninspected original item has those properties.

External methodological check: [CDC variance tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx) distinguishes weighting from design variance and describes domain estimation. It corroborates the general distinction; NHANES guidance does not issue methods or rights for this estate.
