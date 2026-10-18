# Ghana EE12 / N8E — exact pending owner record (no measured trend issued)

**Worker terminal:** `HOLD_SOURCE_RELEASE_METHOD_STATISTICS_AND_EE12_ISSUER` (inherited N03 state, unchanged)
**Claim:** `N8E_GHA_R5Q43_R9Q31_DSAT_R1`, graph edge `TEMP_SRC02_SRC03`
**Role limit:** this source-free worker does not issue EE12/C7, does not read original respondent files, does not compute a Ghana number and does not install N8E into N9.

## 1. What N03 already established (documentary only)

N03 at `d2475e630e6f32a83c6fa4a35983259049d179f9` established a positive bounded **documentary** correspondence:

- Ghana R5 2012 English questionnaire finalized 19 April 2012, Q43 at PDF index 8 / printed p.9, asks satisfaction with how democracy works in Ghana; categories 4/3/2/1/0, where `0` is the substantive respondent judgment “Ghana is not a democracy”;
- Ghana R9 2022 English indigenized questionnaire revised 30 March 2022, Q31 at PDF index 12 / printed p.13, asks the same intended concept with the same visible category topology; DK `9`;
- R5 Q42 and R9 Q30 immediately precede the satisfaction item with a “how much of a democracy” question;
- published target class Ghanaian citizens 18+, independent cross-sections, national `n=2400`, PPPS clustered/stratified design class, field periods 2012-05-08..27 and 2022-04-04..20;
- merged-codebook refusal conventions R5 `998`, R9 `8`; missing `-1`; DK `9`;
- `0` is not a missing code and not a surrogate for dissatisfaction.

This is **not** proof of the original merged release, actual Ghana selector/routing in the retained private bytes, fielded translation, design weights/PSU/strata, variance, comparability or any trend.

## 2. The exact null state that remains

The frozen N03 expected record is reproduced by `runtime/n8e_sourcefree_comparator.py::ghana_n03_state()` and is exercised by the test suite. Its result fields are all null:

| field | value |
|---|---|
| `actual_result_state` | `HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE` |
| `wave_sample_and_weight_design_receipts` | `[null, null]` |
| `wave_five_category_weighted_distributions` | `[null, null]` |
| `wave_asked_valid_and_typed_nonresponse_receipts` | `[null, null]` |
| `weight_PSU_stratum_variance_authority` | `null` |
| `independent_scientific_decision` | `null` |
| `positive_EE12_relation_and_snapshot` | `null` |
| `source_run_authority_and_product_receipts` | `[null, null]` |
| `N8E_implementation_commit_blob` | `null` |
| `delta_proportion` | `null` |
| `design_variance` | `null` |
| `design_standard_error` | `null` |
| `confidence_or_compatibility_interval` | `null` |
| `inferential_classification` | `null` |
| `N9_product_family_and_target_use_permission` | `null` |
| `actual_N9_consumer_receipt` | `null` |
| `asof_replay_invalidation_receipt` | `null` |
| `N8S_structural_rule_and_fact_refs` | `null` |

The frozen input material for any future competent operation remains:

- `SRC02` SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`, R5 Ghana Q43, field dates 2012-05-08/2012-05-27;
- `SRC03` SHA-256 `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`, R9 Ghana Q31, field dates 2022-04-04/2022-04-20;
- substantive codes `0,1,2,3,4`; numerator codes `3,4`;
- typed special codes R5 `{dk:9, refused:998, missing:-1}`, R9 `{dk:9, refused:8, missing:-1}`.

No value in this table is a measurement. Missing does not mean zero, and lack of evidence does not mean `NONCOMPARABLE`.

## 3. Source-free comparator / admissibility exercise (hypothetical only)

`runtime/n8e_sourcefree_comparator.py` implements the **specification** the N03 future product must satisfy. It accepts only receipts whose claim id begins `HYPOTHETICAL_` and whose `ghana` field is false. A full positive hypothetical receipt yields a weighted arithmetic check; every incomplete or hostile receipt yields a typed state:

| condition | typed state |
|---|---|
| no positive exact EE12 relation/snapshot/target use | `HOLD_EE12_ISSUER` |
| no independent estimand/weight/design/variance decision | `HOLD_SCIENCE` |
| no design-based variance authority | `UNQUANTIFIED_DESIGN_UNCERTAINTY` |
| IID binomial or headline-`n` variance | `REFUSED_IID_OR_HEADLINE_VARIANCE` |
| dependent waves without covariance | `HOLD_COVARIANCE` |
| zero weighted denominator | `ZERO_SUPPORT` (delta null) |
| interval includes zero | `INCONCLUSIVE_WITH_INTERVAL` (never `NO_CHANGE`) |
| predeclared no-change margin satisfied | `NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION` |
| positive necessary-condition conflict with exact negative issuer | `SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND` |
| missing category `0` or a changed five-category topology | `CATEGORY_TOPOLOGY_MISMATCH` |
| special codes not separated/typed | `SPECIAL_CODE_LAUNDERING` |
| source version superseded | `STALE_SOURCE_INVALIDATED` |
| missing required receipt fields | `MISSING_SOURCE` |
| non-hypothetical or Ghana-labelled input to the exercise | `REFUSED_NON_HYPOTHETICAL_OR_GHANA_CLAIM` |

The comparator only computes `p_t = Σ w_ti 1[response∈{3,4}] / Σ w_ti` over the five substantive categories, with `Δ = p_B - p_A`; it uses provided design variances and, where independence is false, a provided covariance. It never derives an IID interval from `n=2400` or a headline MOE. The one arithmetic positive in this return is explicitly hypothetical (`p_A=0.5`, `p_B=0.7`, `Δ=0.2`, SE `0.07810249675906655`, interval `[0.04691910635222957, 0.35308089364777046]`) and is not a Ghana or N8E result.

## 4. Historical V553 method evaluation

`data/ddm_build_copy/ddm_v553_temporal_pressure.py` and `ddm_v553_harmonization.py` are real sealed historical implementations. They were imported and executed against empty input:

- `validate_v553_temporal_pressure_readiness({})` returns 45 typed structural readiness errors (packet path, year-indexed pressure, harmonization evidence, source wave anchor, cross-wave delta, comparability audit, score fields, etc.);
- `build_v553_wave_harmonization_report(pd.DataFrame())` returns `STATUS: V553_WAVE_HARMONIZATION_SCAFFOLD_ONLY_SINGLE_WAVE`, `comparability_status=comparability_limited`, `comparison_authority_status=insufficient_multi_wave_authority`, `multiple_waves_present=false`, `wave_count=0`, `blocking_conditions=[at_least_two_waves, one_explicit_survey_family_and_country, shared_semantic_directionality_and_position_signal_columns, wave_specific_certified_authority_rows]`.

**Verdict:** V553 is a structural temporal-pressure/harmonization candidate. It does not consume respondent rows, five-category satisfaction, design weights/PSU/strata or produce a survey-wave delta. It cannot substitute for N8E and creates no Ghana authority. Reuse is structural-only.

## 5. Exact owners and stop order

The N03 docket `GHANA_Q43_Q31_EXACT_RETAINED_RELEASE_NATIONAL_DESIGN_ESTIMAND_BRIDGE_R1` remains the single binding request, with five distinct authorities:

1. **Afrobarometer Data Management / CDD-Ghana** — authenticate the original official **merged-round** R5/R9 release, version/correction date, Ghana Q43/Q31 field/routing, substantive and special codes, fielded language/forms, national design/weights/PSU/strata, variance and response/nonresponse documentation. A public Ghana-only dataset or generic TIF is not a binding to the private merged bytes.
2. **Separately source-read-authorized Rawlsing custodian** — verify at actual physical roots the frozen SRC02/SRC03 SHA-256, map them to the official merged release/version, and provide exact Ghana selector/routing/column/weight/design bindings. The custodian may not certify unseen private bytes, and no source file is opened by this worker.
3. **Independent survey measurement/statistics owner** — decide the eligible/asked/substantive adult-citizen estimand, response transform, five-category preservation, missingness, design-based variance, independent-cross-section covariance or its refusal, and the uncertainty ceiling. If design uncertainty cannot be supported, return `UNQUANTIFIED_DESIGN_UNCERTAINTY` or `HOLD_METHOD`, not a spurious interval.
4. **Competent exact EE12/C7 issuer** — after 1–3, issue an authentic positive relation/snapshot over the exact source-product identities, Ghana scope, value meanings, target estimates, reference time, target use `EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY` and revocation/falsification conditions. A public questionnaire, code fixture or alias is insufficient.
5. **Separate per-wave execution and N9 product-family owner** — issue exact source-use/operation authority, produce two native five-category wave facts, independently qualify/adopt the N8E comparator, and permit only an as-of-bounded historical CONTEXT in N9. N9 must show exact dependency/as-of/replay/invalidation; it must not place N8E attitude into V553 active causal structure or N10W person selection. N8S needs independently admitted objective N5/N6 fields and its own rule.

Stop order: missing official release or private byte match → `HOLD_CUSTODY`; missing Ghana selector/weight/design → `HOLD_SOURCE_METHOD`; unresolved measurement/population/design → `HOLD_SCIENCE` or an explicit limited scope; absent authentic EE12 snapshot → `HOLD_EE12_ISSUER`; absent per-wave facts/current comparator/permitted N9 consumer → `HOLD_PRODUCTION_CONSUMER`. Only a competent positive necessary-condition conflict may yield `NONCOMPARABLE_FOR_EXACT_ESTIMAND`.

## 6. Explicitly forbidden in this state

- Any Ghana numeric change, direction, trend, uncertainty interval or `NO_CHANGE` claim.
- Any “measured no-change” inferred from absence, a null delta, a non-significant result or a failed search.
- Any claim of original weight/design comparability, release-byte identity, respondent-level linkage or national representativeness.
- Any N8E product, N9 installed historical context, N8S structural interpretation, persona input or actor use.
- Any opening of the private SRC02/SRC03 files, SAV/DTA rows or original respondent files without the exact source-and-host permission.

The required next actual return is a competent, separately signed owner decision under the docket above. Until it exists, the correct product is this typed HOLD, not a fabricated number.
