# D07 selected first EE12 source, target, estimand and issued-or-held gate

**Status: PRE-RESULT FROZEN PROPOSAL, NOT SOURCE EXECUTION, NOT EE12 ISSUANCE.**  
**Selector:** Ghana, Afrobarometer `TEMP_SRC02_SRC03`; R5 `Q43` (May 8–27, 2012) -> R9 `Q31` (April 4–20, 2022); country adult Ghanaian citizens, 18+; independent repeated cross-sections.

## Two original administered-form witnesses recovered/verified at documentary-text level

- **R5 Ghana English, finalized 19 April 2012:** https://www.afrobarometer.org/wp-content/uploads/2022/02/gha_r5_questionnaire.pdf. Cover p1 PDF index0. Q42/Q43 at PDF index8, printed p9. Q43 satisfaction item plus `4 Very satisfied`, `3 Fairly satisfied`, `2 Not very satisfied`, `1 Not at all satisfied`, `0 Ghana is not a democracy` (do not read), `9 Do not know` (do not read). Main prompt is in interview language while the noun *democracy* is English unless the respondent cannot understand. Generic interviewer instruction near PDF index2: write “refused” on firm refusal. 2012 card selection / Ghana-citizen 18+ appears index1–2.
- **R9 Ghana English, revised 30 March 2022:** https://www.afrobarometer.org/wp-content/uploads/2023/06/GHA_R9.Indigenized-Questionnaire-_30mar22-FINAL.docx.pdf. Q30/Q31 at PDF index12 / printed p13. Same intended concept `4/3/2/1/0` with DK9; `0` explicitly “Ghana is not a democracy” (do not read). Same localized prompt / English “democracy” rule. Some punctuation and accept/read instruction differences. R9 tablet-selected household citizen 18+; languages and forms near PDF index3.
- **Confidence ceiling:** Both original PDFs' text passages were directly opened and searched. Repeated tool screenshot requests for the relevant page indexes returned *Internal Error*, so no successfully reviewed page images are claimed. Public official file + page-index text is an original-document documentary witness, **not visually certified field deployment, original translation corpus, release-byte identity or administered-response equivalence**.

The exact R5 country original materially upgrades HQ260's merged-codebook-only position. It does **not** resolve released-source identity: Ghana 2012 separately linked national SAV is an official resource, but Rawlsing's retained SRC02 is a frozen *merged* round SAV; matching by year/item and a different country-only download is not a cryptographic proof. Likewise SRC03. Preserve version/as-of identity and country-specific selection in each retained source.

## Measure, semantics, routing and target

Object: **population distribution of reported satisfaction with democracy**, *not* institutional quality, democracy's objective state, causal effects or current national political stability. Eligible universe in both technical forms: Ghanaian citizens age 18+, independently selected; confirm retained release includes only eligible Ghana respondents, proper asked-item routing and weights. Non-substantive refusal R5 `998` vs R9 `8` in respective merged codebooks; DK `9`; missing `-1`; keep types and count separately. No DK/refusal/missing is a zero or “Ghana is not a democracy.” All original substantive `0,1,2,3,4` are kept separately in output and in denominator; `0` is a substantive *self-report* in a separate response class, not the investigator's diagnosis.

Preselect the exact claim:
```text
A = Ghana adult citizens >=18 in SRC02 R5 May 2012;
B = Ghana adult citizens >=18 in SRC03 R9 April 2022;
S_t = individually eligible, administered exact Q43/Q31 and response ∈ {0,1,2,3,4};
p_t = (Σ_{i∈S_t} w_ti · 1[response_i∈{3,4}]) / (Σ_{i∈S_t} w_ti);
Δ = p_B − p_A;
```

Report independently weighted original five-category proportions, unweighted/weighted asked/valid base, DK/refused/missing and availability/routing, frame/inclusion and per-wave design uncertainty. Use the **two independent, complex survey designs**, verified strata/PSUs/calibration/missingness and independent-wave covariance treatment. If the effective variance cannot be supported from retained public-use releases, produce a typed **UNQUANTIFIED_DESIGN_UNCERTAINTY / method HOLD** rather than an IID/Wald CI. Do not describe “no statistically significant difference” as observed equality. Calculate nothing until original-source operation and affirmative pair authority are independently issued.

**Freeze target-use:** `N8E_GHANA_CITIZEN_DEMOCRACY_SATISFACTION_SHARE_R5_R9_DESCRIPTIVE@1`; intended N9 product family `EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY`, *conditionally* if N9 owner permits this exact temporal survey context. Never supply N8S STRUCTURAL_DELTA or a causal rule. The intended marginal share among five substantive answers is not a selected empirical result; all p, Δ, SE, CI fields are `null: NOT_RUN`.

## Material original comparisons, not declarative equivalence

| Dimension | Ghana R5 2012 | Ghana R9 2022 | Consequence |
|---|---|---|---|
| Country original question | Q43, April 19 final English | Q31, March 30 revised English | Direct country-text correspondence now evidenced |
| Prompt context | Q42 how much of a democracy immediately before | Q30 how much of a democracy immediately before | Similar immediate concept priming; broader sections/mode still need review |
| Labels | 0..4, DK9 printed | 0..4, DK9 printed | Refusal conventions 998/8 from codebooks, not item card |
| Target | Citizens 18+ | Citizens 18+ | Intent aligned, coverage implementation and source-release risk pending |
| Frame/mode | 2010 adjusted frame; card selected person | 2021 census frame; computer/tablet selected person | Exact design/weight and nonresponse effects unresolved |
| Date/response | May 8–27 2012; 72.9% reported response | Apr 4–20 2022; 94.23% reported response | No naive change test from headline n or MOE |
| Sampling | 2,400 nationally, PPPS clusters | 2,400 nationally, PPPS clusters | Original TIF gives design *class*, not archive fields/variance proof |
| Original release | SRC02 retained merged, SHA256 c9200ba3… | SRC03 retained merged, SHA256 3afcecd0… | Need official accession, exact Ghana scope columns and typed valid denominator |

## The exact first competent external method/issuer request

**One bounded missing return:** `GHANA_Q43_Q31_EXACT_RETAINED_RELEASE_NATIONAL_DESIGN_ESTIMAND_BRIDGE_R1`. Afrobarometer Data Management and CDD-Ghana survey custodian authenticate (a) retained SRC02/SRC03 SHA mapped to correct original merged official accession/revision, not just country-SAV names, (b) GH country scope and eligible ask-domain, Q43/Q31 native fields, missing/response handling, translated/deployed item if available, (c) PSU/stratum, PPS household/person inclusion, R5 and R9 national within-country weights, calibration and finite-population/inference guidance, (d) actual field administration and original method departures. Independent authorized survey-method statistician evaluates the proposed p and Δ, sample design and instrument comparability including effective design uncertainty. Return affirmative contract or **one exact refused field and custodial source path**. Neither a public English questionnaire nor worker inspection is an issuer.

**Follow-on gates, all **separately** unissued:** approved source reads of exact retained files → two actual native per-wave respondent-backed facts → genuine claim-specific EE12/C7 positive source-universe/measure/population/estimand/comparison target authority → authorized N8E comparator (existing owner only if actually adopted; HQ214 candidate absent sealed) → N9 bounded context-service positive owner + dependency/as-of/replay receipt. Any step can refuse. A positive instrument correspondence finding does not self-authorize later steps.

## Primary and internal witnesses

- Original Ghana R5 questionnaire: https://www.afrobarometer.org/wp-content/uploads/2022/02/gha_r5_questionnaire.pdf (cover PDF index 0: finalized 19 April 2012; Q43 PDF index 8 / printed p.9, R5 Q42 immediately preceding).
- Original Ghana R9 questionnaire: https://www.afrobarometer.org/wp-content/uploads/2023/06/GHA_R9.Indigenized-Questionnaire-_30mar22-FINAL.docx.pdf (cover PDF index 0: revised 30 March 2022; Q31 PDF index 12 / printed p.13, R9 Q30 immediately preceding).
- Afrobarometer merged R5 codebook: https://www.afrobarometer.org/wp-content/uploads/2022/02/merged_r5_codebook_2.pdf (Q43, PDF index 23 per HQ260; this merged file is NOT the original country questionnaire).
- Afrobarometer R9 merged codebook: https://www.afrobarometer.org/wp-content/uploads/2024/10/AB_R9.MergeCodebook_25Jun24.final_.pdf (Q31, PDF index 22 per HQ260; generic merged text cannot replace Ghana field text).
- Ghana R9 published country summary/TIF: https://www.afrobarometer.org/wp-content/uploads/2022/10/Summary-of-results-Ghana-Afrobarometer-R9-21oct2022-1.pdf (PDF index 3 / printed p.4, target/design/field dates).
- HQ260 E01 scientific ranking: https://github.com/maidiu/rawlsing/blob/5da99d15aeb83ab8d83f22128523e6a1be67209b/WORKER_RETURNS/PYAT-HQ260-E01-TEMPORAL-PAIR-METHOD-SELECTION-R1/02_ONE_TEMPORAL_ESTIMAND_READINESS_CHOICE.md
- D03 source science at f5173776412e4b93eaa82af291a6dcabafef32e9: https://github.com/maidiu/rawlsing/tree/f5173776412e4b93eaa82af291a6dcabafef32e9/WORKER_RETURNS/PYAT-HQ280-PV3-D03-EE12-COMPARABILITY-SCIENCE-R1/
- Ghana R5 public country data accession (last updated July 2015): https://www.afrobarometer.org/survey-resource/ghana-round-5-data-updated-july-2015/ ; the accession is not SHA256 identity proof for Rawlsing's merged retained SRC02.
