# N03 — frozen first actual N8E empirical change/no-change product and N9 consumer contract

**Status:** `PROPOSED_EXACT_FUTURE_OPERATION__NOT_EXECUTED_OR_ISSUED`. The full result record below is an **expected shape with null result fields**, **not an observed result**. Freeze scientific operation and output prior to inspecting any raw row or observed sign. No EE12 comparison authority is created by defining this contract.

## Precise population, response, measure, temporal interpretation

- Claim ID `N8E_GHA_R5Q43_R9Q31_DSAT_R1`. Graph `TEMP_SRC02_SRC03`; subject class **Ghanaian citizens age 18+**, separate probability cross-section respondents in the nation at R5 Ghana field period **2012-05-08..27** and R9 Ghana **2022-04-04..20**. **Not a panel**, not objective democratic performance and not an individual psychological trajectory.
- Per-wave original native field `Q43` (R5) vs `Q31` (R9) in correct official country-eligible **retained merged** releases; 0='Ghana is not a democracy', 1='not at all satisfied', 2='not very satisfied', 3='fairly satisfied', 4='very satisfied'. Preserve all five categories as separate substantively answered classes with native labels and weighted shares. R5 missing `9/DK, 998/refused, -1/missing`; R9 `9/DK, 8/refused, -1/missing`; zero is never a code for missing or a surrogate for dissatisfaction. Explicit `NOT_ASKED` remains typed if source routing establishes it. Verify any additional native special codes before running; never infer a zero denominator.
- Primary **design-weighted national descriptive** estimand: in wave `t` the finite-population ratio `p_t = [Σ_{eligible, asked, substantive 0..4} w_{ti} 1(R_{ti}∈{3,4})] / [Σ_{eligible, asked, substantive 0..4} w_{ti}]`, using authorized source-native Ghana national selection weight and correct nationally representative selection. `Δ = p_2022 - p_2012`; signed change in share measured in proportion or percentage points, sign fixed as later minus earlier. Report per-wave raw counts only as **sample diagnostics**, not replace weighted Ghana population estimator.
- Also report `p_t(k)` **for all five k=0,1,2,3,4**, the eligible/asked/substantive raw counts and survey-weighted denominators, DK/refused/missing counts, national inclusion proof, and field/release/provenance. If standardization to an identical age/sex or geography population is necessary, that is a **new prespecified and independently issued estimand**, not a silent after-the-fact manipulation; do not interpret different 2010/2021 frames as an observed causal change.
- Design uncertainty: independent complex clustered/stratified/PPPS surveys; method owner certifies named PSU, stratum, calibration weights/replicate weights or suitable alternative. With independent samples and valid comparable p estimators, `Var(Δ)=Var(p_2022)+Var(p_2012)`; if independence or shared calibration fails, **include authorized covariance**; choose survey df, test/interval and nonresponse sensitivity by signed statistician. **Do not** use IID SRS binomial `sqrt(p(1-p)/2400)`, headline ±2% national MOE, or ignore unavailable design effect. Missing design authority → null SE/interval with `UNQUANTIFIED_DESIGN_UNCERTAINTY`, and not a scientific positive inferential no-change finding.

## Exact negative and null decision logic

- `MEASURED_INCREASE` / `MEASURED_DECREASE`: observed signed weighted Δ plus applicable uncertainty, **only** when original-source measurement, design and EE12 permission are positive and an actual comparison executed. Direction and inference should be separately typed; a positive numerical delta not different from zero with uncertainty is not assertively 'increased population share'.
- `MEASURED_EXACT_ZERO_POINT`: numerically equal computed p only after actual qualified execution, not an inferred zero from no evidence.
- `NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION`: **only** if the independent science owner predefines a valid interval, equivalence/no-change threshold or decision rule and actual data meet it. Merely failing to reject 0 is **not** proof of no change. `INCONCLUSIVE_WITH_INTERVAL` is distinct.
- `ZERO_SUPPORT`: an authenticated item/domain count or denominator is actually zero for a supported scoped operation, with typed base/eligibility; no fake 0-share for not-asked/unknown rows. This does **not** mean Δ=0.
- `UNQUANTIFIED_DESIGN_UNCERTAINTY` / `UNISSUED_EE12` / `MISSING_SOURCE` / `HOLD_METHOD` / `HOLD_CONSUMER` are not empirical outcomes. `SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND` requires independent positive necessary-condition conflict and competent negative issuer, not a 404 archive or unavailable private row.
- Report result field `null` with typed explanation until permission/execution. Independently documented response change is not automatic measurement change. No choice of favorable category threshold after seeing empirical direction.

## Expected exact **N8E product record** (placeholders not evidence)

```json
{
 "schema":"N8E_GHA_DEMOCRACY_SATISFACTION_DELTA@1",
 "proof_grade":"FROZEN_EXPECTATION_ONLY",
 "claim_id":"N8E_GHA_R5Q43_R9Q31_DSAT_R1",
 "graph_edge":"TEMP_SRC02_SRC03",
 "country":"Ghana",
 "target_population":"adult citizens age >=18 in each independent field period",
 "source_refs":[
  {"SRC":"SRC02","root_sha256":"c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651","wave":"R5","item":"GHA:Q43","field_dates":"2012-05-08/2012-05-27","release_version":null,"per_wave_fact_ref":null},
  {"SRC":"SRC03","root_sha256":"3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8","wave":"R9","item":"GHA:Q31","field_dates":"2022-04-04/2022-04-20","release_version":null,"per_wave_fact_ref":null}
 ],
 "native_substantive_labels":{"0":"Ghana is not a democracy","1":"not at all satisfied","2":"not very satisfied","3":"fairly satisfied","4":"very satisfied"},
 "substantive_valid_codes":[0,1,2,3,4],
 "positive_numerator_codes":[3,4],
 "typed_special_codes":{"R5":{"dk":9,"refused":998,"missing":-1},"R9":{"dk":9,"refused":8,"missing":-1}},
 "denominator":"eligible national citizens, asked and valid one of 0..4",
 "estimand":"weighted p2022(3,4)-p2012(3,4)",
 "wave_sample_and_weight_design_receipts":[null,null],
 "wave_five_category_weighted_distributions":[null,null],
 "wave_asked_valid_and_typed_nonresponse_receipts":[null,null],
 "weight_PSU_stratum_variance_authority":null,
 "independent_scientific_decision":null,
 "positive_EE12_relation_and_snapshot":null,
 "source_run_authority_and_product_receipts":[null,null],
 "N8E_implementation_commit_blob":null,
 "delta_proportion":null,
 "design_variance":null,
 "design_standard_error":null,
 "confidence_or_compatibility_interval":null,
 "inferential_classification":null,
 "actual_result_state":"HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE",
 "N9_product_family_and_target_use_permission":null,
 "actual_N9_consumer_receipt":null,
 "asof_replay_invalidation_receipt":null,
 "N8S_structural_rule_and_fact_refs":null
}
```

## Actual owner candidate and missing N8E positive producer

**Native/authority:** `rawlsing_next/pre553_empirical_authority.py` for exact kinds `ROUTING_RISK_SET`, `WEIGHT_DESIGN_ESTIMAND`, `UNCERTAINTY_METHOD`, `SOURCE_EQUIVALENCE`, `TEMPORAL_EVIDENCE`; `rawlsing_next/pre553_source_relations.py` `SOURCE_SEMANTIC_EQUIVALENCE` relation + positive immutable `AuthoritySnapshot`; `pre553_analytical_composition.py` source-authorized same-scope product grammar. Those are **existing pieces, not a positive original survey EE12 issuance**. D07 cites independent HQ214 repaired `pre553_temporal_comparability.py` at `a93352512aa9290112bff1eb680c54d43345078f`; absent N03 sealed tree (verified). An adopted survey-design-aware N8E comparator must be identified/independently reviewed for this exact claim or minimally implemented in a separately permitted owner commission. `m1_temporal_v554_admission_dedup.py` is structural V554 ingress and does not compute Ghana 2012/2022 respondent-backed Δ.

**Acceptance intended:** N8E `wave_comparability_manifest.json`, `empirical_temporal_product.json`, `temporal_consumer_receipt.json`; [AT29](https://github.com/maidiu/rawlsing/blob/87e74b18570a11ee29b1e0c78edd31d33f3a8561/PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/AT29.md) and [AT30](https://github.com/maidiu/rawlsing/blob/87e74b18570a11ee29b1e0c78edd31d33f3a8561/PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/AT30.md) require positive source/product and real producer→consumer. No such Ghana outputs exist at current verified claim grain; proof state **NOT EXECUTED**.

## First N9 consumer and separate N8S route

**Proposed first N9 query:** `WORLD_GHA_HISTORICAL_ATTITUDE_SATISFACTION_CONTEXT__R5_R9`, consuming **only a provenance-labeled, as-of-bounded report of adults' 2012/2022 reported satisfaction**, with five native cells and uncertainty, **not** country's objective democracy score, structural pressure, institutional causal change, raw individual changes or present-day forecast. The N9 owner at `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/nodes/N9.md` must affirm that an `EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY` N8E product family is permitted in a declared world snapshot, before a direct path is claimed. Existing `rawlsing_next/m4_v557_v558_publication_repository.py` supports V557 publication/V558 resolution for bounded `V553/V554/V555/V556` structural roots. Existing `prev3_objective_position_v557_v558_publication.py` is one **BEN0002 Q73A original-position-context** owner grant; it does not grant Ghana Q43/Q31 temporal facts. Existing `objective_non_event_publication_serving_adapter.py` covers another bounded structural non-event serving path; do not reuse either to launder new EE12/temporal/world permissions. Thus **N9 product-family adapter or explicit authorized world-serving route is currently an identified composition gap**, not an automatic callable that consumes arbitrary N8E.

**Future real N9 receipt must show:** exact issued source/estimand/model-use if applicable, both per-wave hashes/product refs, positive EE12 and comparison implementation identity, producer-signed N8E product, N9 selection/publication authority, actual query parameters, receipt/result, dependency graph with field dates and effective/as-of semantics, one changed release or revocation/replacement showing selective invalidation and replay, negative/refusal cases. Historical context is the maximum *candidate* claim even if licensed. N9 actual product and consumer receipt: **null / NOT_RUN**.

**N8S is separate:** independently admitted original-material institutional/objective fields N5/N6, their matched structural effective dates/temporal rule and competent N8S structural interpretation, accepted V553 fact/delta and replay. Self-reported democracy satisfaction is not an institution, governance quality or causal material determinant simply by differencing. Do not place N8E attitude Δ into V553 V557 active-causal, a persona model or N10W without explicit new warrants.
