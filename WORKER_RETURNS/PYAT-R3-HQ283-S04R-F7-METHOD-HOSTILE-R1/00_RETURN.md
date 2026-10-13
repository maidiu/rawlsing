# PYAT HQ283 — S04R independent F7 / EE12 temporal-method review

**Role:** Commissioned independent scientist/reviewer, **not** HQ, not an issuer.  
**Commission:** `WORKER_COMMISSIONS/PYAT-R3-HQ283-S04R-F7-METHOD-HOSTILE-R1/00_COMMISSION.md` read in full at **sealed** `28b2a7f048b8412c72fb549eda954654a1780449`.  
**Assigned reviewer branch:** `agent/reviewer-pyat-r3-hq283-s04r-f7-method-r1`. Initial remote `refs/heads/` direct GET confirmed **exactly** `28b2a7f048b8412c72fb549eda954654a1780449` before reviewer writes.  
**Frozen candidate inspected:** S04 `9ae87f2227384e0567190c6a2d5f3a33a60d4b4c`, with `rawlsing_next/s04_temporal_policy.py`, `rawlsing_next/tests/test_s04_temporal_policy.py`, `WORKER_RETURNS/PYAT-R3-S04-F7-TEMPORAL-SOCIOLOGY-R1/00_RETURN.md`, `01_METHOD_COMPARISON.json`, `02_MANIFEST.json`. Nothing in that frozen candidate or its acceptance assertions is modified.  
**Inherited historical V553 evidence:** `data/ddm_build_copy/ddm_v553_harmonization.py`, `ddm_v553_canonical_harmonization.py`, `ddm_v553_temporal_pressure.py` on remotely observed `main@25830fe7462bb9e29bc4087e6ae14f3f84cec377`; their Git blobs respectively `153f3dbeab19e6be15947f7bcbb5377dae1dfc8a`, `1951ada5cb7453108939eae9af91fcbfc90ad517`, `5304b70f9f6522c5ae3893eff215c1d445681983`. Main is an **inherited code comparator**, not independent source authority or permission to use original respondent data.  
**Additional exact grounding:** D07 `bab16899f4c2d7137aba95debbce5410ea0dd74d`; N03 `d2475e630e6f32a83c6fa4a35983259049d179f9`; Astra R3 `88d3c40def26d34ff202258171c256dfa9d17dbb` (`METHOD_REDISPOSITION.json` M08/M11).  
**Proof grade:** `DOCUMENTARY_AND_STATIC_CODE_REVIEW`, no respondent measurements or executable comparison. **No scientific claim of a temporal trend is issued.**

## 1. Independent verdict and scope

`S04R_F7_METHOD_VERDICT = SCIENTIFIC_ADMISSION_HOLD__SOURCE_FREE_POLICY_DEMONSTRATOR_ONLY`

The S04 functions are deterministic, source-free arithmetic and refusal prototypes. Their narrow existence is not in dispute. S04's own author reports 17/17 local tests at its candidate head; I inspected those tests and the author's manifest **but did not re-execute them**. The independent case suite at `rawlsing_next/tests/test_hq283_s04r_temporal_method.py` is newly written, source-free and **NOT_EXECUTED**. The negative cases are explicitly marked `xfail(strict=True)` as presently identified contract defects; a future authorized host can run them without changing S04's frozen oracles. They are proposed independent acceptance criteria, not successful pytest outcomes.

S04 **cannot** be accepted as the scientific F7 temporal estimator or a source-qualified EE12→N8E→N9 bridge merely because one synthetic method produces a number or a heuristic refusal. Both named methods operate on hand-supplied scalar anchors already marked `qualified`, without proving their construct, original response order, respondent risk, country, source version, weights, design, or comparison operation. Neither measures a real Ghana 2012→2022 change.

`nearest_anchor_backoff` can be retained, at most, as a **model-based nearest-anchor context carrier** where a competent future authority **explicitly** authorizes the exact scope, range, uncertainty meaning and downstream use. `linear_interpolation` remains an optional source-free comparative heuristic, not an inherited permission to fill unknown survey years. There is **no empirically defensible basis in the inspected artifacts** to select either as universally superior; a "better" error rate or successful coverage has not been measured.

The positive real product does **not** require imposing either interpolation policy on a two-wave observed comparison. It requires separately measured wave-specific estimates with design-aware uncertainty and an exact positive comparison authorization.

## 2. Inherited V553: actual method and authority distinction

S04 describes `linear_interpolation` as "inherited V553 (gap-insensitive, no drift uncertainty)" and `nearest_anchor_backoff` as the selected improvement. That historical comparison is **materially incomplete and partly inaccurate**.

In `ddm_v553_temporal_pressure.py` on the identified main:
- `_interp` (around line 199) and `_build_interpolated_pressure_rows` (606–672) implement an elementary **pressure-component interpolation helper**, not a source-intrinsic survey trend law.
- `_build_interpolation_policy_ledger` (850–886) records authorized or refused interpolation and its own *heuristic* confidence penalty. S04's new drift value is not calibrated in that ledger.
- `_authorize_v553_multi_wave_key` (750–849) requires harmonization readiness, same comparable grain, resolved dimensions, packet provenance, minimum two eligible distinct waves, and proper authority. One anchor is `PROBE_ONLY_TEMPORAL_KEY`, not positive comparability.
- `_build_v553_interpolation_segment_index` (2675–2729) expressly sets `unknown_gap_preserved`, `interpolation_method="none"`, `interpolation_allowed=False` and `no_survey_observation_preserve_unknown` even when sparse temporal key authority exists. `_build_v553_temporal_gap_and_absence_index` (2772–2805) separately marks `value_inference_allowed=False`.
- `_build_v553_temporal_pressure_field_contract` (2837–2947) preserves **null** unknown-year pressure levels and `allowed_downstream_use=False`, while separating authorized structural anchors from probe-only material.
- `_build_v553_cross_wave_delta_index` (2596–2674) distinguishes `authorized_structural_delta_value`, `probe_delta_value`, `delta_interpretation_permission`. It is not a design-adjusted national opinion difference estimator.

In `ddm_v553_harmonization.py` (519–985), comparability requires one explicitly identified source family and country, multiple waves, shared semantic/directionality/position structure and wave-level authority; a "column overlap" score alone is not exact item/estimand equivalence. `ddm_v553_canonical_harmonization.py` enforces published V552J artifact identity, manifest/schema/integrity distinctions (not-present, valid-empty, corrupt and unauthorized) before consumption. These are **inherited safeguards**, not a positive Ghana EE12.

S04's own `linear_interpolation` is also **not literally gap-insensitive**: it refuses bracketing gaps above `max_gap_years`; before the first anchor it uses that gap limit, and after the last anchor it enforces `max_horizon_years`. Its author comparison table therefore understates an existing guard. The meaningful contrast is **straight-line interpolation versus nearest-observation carry**, each under incomplete source/method authorization.

**Scientific consequence:** `ANALYTIC_INTERPOLATION != OBSERVED_SURVEY_RESULT != QUALIFIED_ESTIMATED_TEMPORAL_DELTA != STRUCTURAL_PRESSURE_FIELD`. Current authorized V553 gap-preservation semantics must not be silently displaced by a newly selected S04 method.

## 3. Bounded review findings — exact failure mechanisms

### 3.1 Five primary scientific blockers

**F01 — `0.05 / year` is not uncertainty estimated from samples.** In `nearest_anchor_backoff`, `drift_uncertainty=round(gap*0.05,6)`; in `linear_interpolation`, the value is scaled by interval length and fractional position. No source, measured volatility, standard error, loss/coverage calibration, probability model, unit/metric, or design-based variance justifies `0.05`. Ten years yields 0.5 on a nominal 0–1 synthetic scale, not an empirically certified interval. Exact-year `0.0` means no *constructed* drift penalty, not zero survey sampling/nonresponse/measurement uncertainty. Defensible alternatives: report qualitative/typed temporal uncertainty; use a **source-qualified and preregistered/calibrated** sensitivity envelope after actual observational evidence; use survey design variance for two-wave measured Δ independently. Until then any output `drift_uncertainty` must be visibly `UNCALIBRATED_MODEL_HEURISTIC`, never SE/CI or an issued accuracy claim.

**F02 — the `qualified=True` bit cannot authorize measurement.** `Anchor` has `year, value, population, polarity, qualified, evidence_mode, source_ref, category_semantics`; it has no bound country/original field/eligible asked risk/release version/weight/PSU/stratum/measurement design/authority snapshot. `_qualify` checks string equality and boolean only. A changed population definition may retain the same string; different Ghana domain/other-country facts may be mixed; a value could be a model prior. Nominal year is not the fieldwork window. Before any scientific or N8 use, each per-wave factual scalar must descend from a source-qualified national estimate and a positive exactly scoped relation/operation.

**F03 — numeric `3x` and polarity string are not qualified structural or instrument break detectors.** `_find_breaks` compares consecutive anchors in the **unfiltered entire input**. Unqualified records and another population can cause a break refusal inside a legitimately filtered adult series. It refuses when raw polarity strings differ or `abs(curr-prev)/abs(prev)>3` (except prior=0); this is scale-dependent, ignores a 0→large jump, and may call a genuine large observed social change a "method break". It does not inspect instrument wording, translation, response-category meaning, field method or changed sampling frame. Restrict any change-point diagnostic to a certified same-series source and keep `METHOD_HOLD`, `MODEL_WARNING`, `SOURCE_PROVEN_NONCOMPARABLE`, and `TRUE_MEASURED_CHANGE` distinct. A ratio heuristic **cannot adjudicate** original source equivalence.

**F04 — source-native ordinal order and evidence plane can silently change.** `category_semantics` is never used; only nominal `polarity` equality is checked. Identical `high_good` strings can mask reversed original scale/collapsed DNR cells or shifted category interpretation. On exact year, both functions always force `MEASURED` with drift=0 even if anchor is `TRANSFORMED`, `INFERRED` or `PRIOR`. For interpolation/backoff they force `INFERRED` irrespective of source grade; that is a new estimated value **conditional on** the underlying evidence, not permission to upgrade low-grade support. Original observational claim, transformed response mapping, inferred model value, broad prior and analyst structural interpretation all need separate typed provenance and authorized ceilings.

**F05 — no survey support or sample-design calibration.** The model never sees source denominator, effective n, population/stratum/domain variance, cluster/PSU, weights, nonresponse or covariance. It cannot recognize wave-specific support deficiencies; wrong design cannot be rescued by more restrictive time extrapolation. An observed weighted Δ should use a competent independent complex-survey estimate and variance under a declared cross-section covariance assumption. Without it, `UNQUANTIFIED_DESIGN_UNCERTAINTY`, not a fabricated interval, IID/SRS convenience bound, `NO_CHANGE`, or synthetic `drift_uncertainty`.

### 3.2 Additional execution/identity defects

**F06 — one anchor is not a temporal trend.** The nearest policy extrapolates from one within `max_gap_years`; `linear_interpolation` falls back to nearest at edges. A one-wave value may be a historical anchor or unissued prior conditioning; it does not provide evidence of temporal change. At default `max_gap=10` and `max_horizon=20`, the nearest policy tests `gap>max_gap` **before** `gap>max_horizon`: `HORIZON_REFUSAL` is unreachable at the defaults. Conversely the two linear edge policies are asymmetric. A 20-year inter-anchor interval can be carried near either endpoint if nearest is within 10 years despite the full segment's evidence absence. No method paper or owner rule supports these defaults or conditions.

**F07 — replay/input identity is under-specified.** `content_hash` omits `source_ref`, `category_semantics`, `evidence_mode`, `allow_interpolation`, `allow_backoff`, `allow_prior`, full operation identity/version and positive authority. Two semantically different per-wave inputs can hash identically. Exact-year conflicting duplicate anchors are resolved by first insertion order without ambiguity refusal. A candidate readout can be deterministic given an arbitrary list without being source-identical or replay-auditable under a real release replacement.

**F08 — method fallback is silently permissive.** `evaluate_temporal(..., method="unrecognized")` runs `nearest_anchor_backoff` instead of refusing unknown method. `allow_prior` and `PRIOR_BROAD` are exposed, but S04 does not implement a qualified prior source/selection; an empty anchor set still returns `MISSING_ANCHOR`. This is preferable to inventing a prior, but it disproves the author's suggestion of an implemented "historical priors" path. A previous-source `POLARITY_DRIFT` enum likewise is not positive semantic-adjudication logic.

**F09 — research-generic geography/irregular waves.** The S04 request has no explicit Ghana country or frame/field period, and irregular wave spacing is reduced to nearest numeric year. A changed survey population/territory/design is not recognized. Source identity, item identity and cross-wave estimand are separate than string-level population and polarity. A later multi-wave curve would require its own tested model, not merely more anchors.

**F10 — test proof ceiling.** S04 reports `python3 -m pytest rawlsing_next/tests/test_s04_temporal_policy.py -v` exit 0, 17 pass in the authored return and manifest. That is **author-reported**, not independently observed at this review host. The original tests are synthetic interface cases and do not prove original-source measurement, survey design, ordinal category stability, properly separated proof grades, full replay hash, or empirical calibration. Newly committed source-free independent cases exercise these omission points but remain unrun. No purported `pytest` success is included in S04R.

### 3.3 Stress-case interpretation table

| Case | What S04 code can do | Competent disposition |
|---|---|---|
| Reversed source-native ordinal coding but same nominal polarity | Accepts value; `category_semantics` unused | `HOLD_SCALE_EQUIVALENCE`, preserve native cells and required transformation |
| Changed eligible respondent target with stable `population` string | Accepts silently | `HOLD_ESTIMAND_POPULATION`, prove asked/routing/domain/denominator |
| Different instrument/mode/translation or frame | Can refuse only if arbitrary scalar change/polarity detected | `HOLD_METHOD_INVARIANCE`; do not pronounce noncomparability on heuristic |
| Ratio shift >3x or prior zero | Ad hoc break or missed break | `MODEL_DIAGNOSTIC_ONLY`, separate true social change from source incompatibility |
| Long/irregular inter-wave gap | Numeric backoff or interpolation if configurable distance passes | `UNKNOWN_GAP` unless exact calibrated model/operation grant |
| Missing PSU/strata/weight/national domain | Input has no fields to check | `UNQUANTIFIED_DESIGN_UNCERTAINTY`; not 0 error or sample-size shortcut |
| Same native item but different geography | No geography guard | `HOLD_COUNTRY_DOMAIN` and exact source selector |
| Mixed observed/inferred/prior anchors | Exact branch turns every grade into `MEASURED` | Preserve per-source and output evidence labels separately |
| Single qualified anchor | Returns source-free backoff in bounded window | Historical context only, never measured trend |
| No anchors or invalid method | Missing anchor or silently defaults nearest | Exact missing / unknown method fail-closed; no fabricated prior |

These are code-derived expected paths and reviewer-normative acceptance standards; **none** is reported as an executed fixture or an empirical incompatibility finding.

## 4. First real positive EE12 → N8E → N9 path (do not generalize the hold)

**Nearest candidate:** Ghana Afrobarometer **Round 5 (2012) Q43** to **Round 9 (2022) Q31**, graph edge `TEMP_SRC02_SRC03` and proposed claim `N8E_GHA_R5Q43_R9Q31_DSAT_R1`. This is the D07/N03 **documented candidate**, not an issued `EE12` relation. D07 directly recovered the country-original English R5 instrument (PDF index 8, printed p.9) and R9 (PDF index 12, printed p.13). Both concern reported satisfaction with democracy **in Ghana**. Public Ghana TIF fieldwork: 2012 May 8–27 and 2022 April 4–20, independent nationally sampled Ghanaian adults 18+, with important census frame/mode/nonresponse changes. Public materials do not by themselves authenticate the **private retained merged-round bytes** or design fields.

Exact source root identifiers **from D07/N03**, not independently reopened here:
- `SRC02` R5 SHA256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- `SRC03` R9 SHA256 `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`.

Preserve original category topology: `0=Ghana is not a democracy` (valid distinct DNR substantive category, not dissatisfaction), `1=not at all satisfied`, `2=not very satisfied`, `3=fairly satisfied`, `4=very satisfied`. `9=don't know` is not valid substantive; refusal `998` R5 vs `8` R9 and source-missing `-1` require wave-specific typed treatment. Choose **before data observation** the common adult-citizen national eligible/asked valid `0..4` denominator and indicator `3|4` numerator; this defines **candidate** difference `p_2022(3|4)-p_2012(3|4)`. No direction, estimate, variance, interval or no-change inference is known.

**Smallest competent custody/issuance order, already docketed by D07/N03:**

1. Afrobarometer original **merged-release** authority (CDD-Ghana/Data Management) attests exact source release versions, fielded question and instrument/languages/mode, population/domain, category and special-code bindings, official national design/weights/PSU/strata/variance availability. Instrument text alone is not a source-version or administered-language guarantee.
2. Separately permitted Rawlsing **private retained-byte custodian** binds those official releases to SRC02/SRC03 exact hashes, Ghana national/respondent/risk selectors, the original field columns and survey design without leaking or opening unauthorized data. This commission grants **no** respondent read.
3. **Independent statistician** issues a prespecified cross-wave measurement and design decision: target population, unchanged semantic constructs or adequate transformed equivalence, complex-survey estimators/variance/covariance, missingness, selection and nonresponse sensitivity. If uncertainty cannot be quantified, say `UNQUANTIFIED_DESIGN_UNCERTAINTY`; a failed significance test is not proof of no change.
4. A **separately competent exact EE12/C7 issuer** grants positive comparison and temporal operation/use on the precise source identities, response transform, estimator, time, provenance/snapshot/variance policy and audience. An existing generic `SOURCE_EQUIVALENCE`, `TEMPORAL_EVIDENCE`, or S04 `qualified=True` is insufficient.
5. **Only after** these grants and actual source execution: two qualified per-wave native five-cell weighted distributions and independent complex-survey estimates, executed **N8E** measured difference plus typed uncertainty and provenance; no source-free numeric fill. A permitted **N9** product-family adapter may serve the historical attitudinal context with exact source/as-of/replay/invalidation receipt—never an objective Ghana democracy score, causal societal pressure or live prediction.

**N8S is a different route.** It requires independently issued objective/material-institutional data, structural effective-time and temporal rule, N8S interpretation and separate eventual consumption. It is not implied by, and cannot be directly filled from, respondent opinions about democracy.

This is a **positive narrow product plan** with a real original-instrument candidate and exact owner requests, not a universal F7 stop. Uganda R5/R9 remains secondary because of national versus city oversample and questionnaire lead-in/selection and first-wave original-script gaps; Austria EVS candidates remain historical because of original item/method/target uncertainties (D07 §candidate comparison). Missing documentation is `HOLD`, not a competent declaration of intrinsic noncomparability. The existing **35 sources / 63 syntactic within-family links** are neither 63 legitimate trends nor uniformly forbidden pairs.

## 5. Decision policy and falsification conditions

**Qualified observed relation** requires (i) positive exact source identity/measurement/risk/population comparability; (ii) independent appropriate sampling/design uncertainty; (iii) permission for this precise comparison/use; (iv) actual two-wave measured products. Observed increase/decrease is only reported with separated observed signed point Δ and an independently defined uncertainty/inference rule.

**Modeled historical change** may be useful as a separately identified prior/context sensitivity exercise, but requires independent modeling assumptions, validation/sensitivity and error characterization; it cannot be smuggled into missing survey years as observation, into N8S objective fields or into an unqualified world fact. No preselected global 0.05/year calibration exists in inspected evidence.

**Null and negative outcomes** must be sharply separated:
- `SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND`: positive necessary-condition conflict certified by competent source/statistical owner, not a numeric break or absent release;
- `HOLD_SOURCE_RELEASE`, `HOLD_METHOD`, `HOLD_DESIGN`, `UNISSUED_EE12`, `HOLD_CONSUMER`: authority unavailable, *not* empirical findings;
- `INCONCLUSIVE_WITH_INTERVAL`: real estimated comparison that does not establish direction;
- `NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION`: only from a prespecified equivalence/no-change standard and actual evidence, never "not significant";
- `ZERO_SUPPORT`: actual authenticated eligible denominator zero, not change=0;
- `VALID_EMPTY` / `MISSING` / `DENIED`: preserve distinct source and pipeline states.

**Falsification of present S04 method adequacy** is already visible in code: a transformed/prior exact anchor becomes `MEASURED`; unrelated population may force break refusal; two category orderings can share polarity and be consumed; same-year duplicates resolve by list order; replay hash omits meaning-bearing fields. The independent source-free tests document these cases and future remediations must satisfy them **without editing frozen original acceptance oracles**. A later statistically supported comparison can reject both simplistic methods; an accepted original-wave source pair does not automatically favor either.

## 6. Execution custody, limits, and exact return

**Actually observed:** via connected GitHub tools: successful direct fetch of commission at sealed SHA, successful direct GitHub `refs/heads/` check of reviewer branch at exact sealed SHA, direct fetch of S04 candidate and original test/return artifacts, direct fetch of inherited main V553 code and relevant D07/N03/Astra documents, and GitHub text-file writes to the **assigned branch only**. No local machine or subprocess was instantiated. Connector success is **not** a local shell command exit code.

**Not executed:** `python`, `pytest`, source surveys, respondent-row inspection, empirical F7/E12 statistic, N8E/N8S/N9 runtime, protected CURRENT, V3/V2 actors, production merge, external issuer signatures, model-use API metering. The S04 author's `17 passed` is reported **as authored evidence only**; this reviewer makes **zero new test-pass claims**. The independent tests are review assets marked NOT_EXECUTED. External platform/account allowance and exact token/cost use: UNKNOWN. Model identity: GPT-6; **High requested**, actual user configuration/effort not independently attested by GitHub. Execution surface: ChatGPT remote GitHub connector only. Provider: OpenAI ChatGPT with the connected GitHub account; account-specific provider billing and workspace resources UNKNOWN.

**Changes permitted:** 
- `WORKER_RETURNS/PYAT-R3-HQ283-S04R-F7-METHOD-HOSTILE-R1/00_RETURN.md`
- `WORKER_RETURNS/PYAT-R3-HQ283-S04R-F7-METHOD-HOSTILE-R1/01_REVIEW_FINDINGS.json`
- `rawlsing_next/tests/test_hq283_s04r_temporal_method.py`

**No changes:** S04 code/oracles; original data or manifest identities; current Pyat control owner, canonical/main, V3/V2 or N8 owners. The test path is noncolliding and does not claim acceptance authority.

**Needed independent review after this reviewer:** a separate methods/statistics expert and competent source-release/custody/EE12 issuer for the real Ghana target; an implementation/test-run reviewer with an authorized execution environment for the unrun regression suite; independent N8E producer and N9 consumer acceptance when actual output exists. This reviewer **does not** self-adopt or sign the EE12 bridge.

**Terminal:** `HQ283_S04R_INDEPENDENT_STATIC_REVIEW_COMPLETE__F7_SCIENTIFIC_ADMISSION_HOLD__NARROW_GHANA_EE12_PATH_RETAINED__NO_ORIGINAL_SOURCE_EXECUTION__NO_V3`.

**Remote verification receipt** is supplied in the final chat return using the direct GitHub branch ref; do not infer return SHA from a file blob or author commit assertion alone.
