# HQ270 U01 — dictionary-only future requirements, bounded candidate estimand and non-adoption

## Court disposition

**QUALIFIED_CANDIDATE_FOR_NARROW_SOURCE_DOCUMENT_AND_DICTIONARY_COURT__SCIENTIFIC_HOLD_ON_PAIR_USE.** Original Uganda R5 *country* codebook and R5 contemporaneous published Q7 report recovered; full R5 administered instrument not recovered. R9 original Uganda English instrument, codebook and TIF located, with indexed pages but required visual screenshots failed due cache miss. This improves historical R5 multinational-only evidence materially; it does **not** establish national-sample/weight/source-file equivalence or issuance of an empirical or semantic use grant.

## ONE bounded candidate scientific estimand

Let `U_t` be the **noninstitutional Ugandan citizen aged >=18 in the respective wave's national survey coverage frame**, not the supplemental districts/cities and not a fixed person cohort. Let `Y_t=1` iff eligible respondent answers native substantive code **2**, and `Y_t=0` iff answers code **1**.

**Candidate `Delta = P_R9(Y=1 | Q3∈{1,2}, U_R9) − P_R5(Y=1 | Q7∈{1,2}, U_R5)`.**

The operation—once separately authorized—estimates the *change in the probability of calling Uganda's overall direction “right” among respondents offering a binary substantive judgement, under each wave's own national sampling/weighting design*. It is repeated cross-sectional **2011–12 vs January 2022**, not longitudinal within-person change and not objective policy performance. Denominator restriction can introduce selection bias if don't-know/refusal differs; report the design-weighted non-substantive proportions separately **and** a pre-specified all-eligible or uncertainty-sensitive diagnostic. No substantive result is implied or calculated here.

R5 `{1 wrong,2 right,9 DK,998 refused,-1 missing}`; R9 `{1 wrong,2 right,8 refused,9 DK,-1 missing}`. Do not code `998->8` silently without an explicit tagged recode mapping; retain original and harmonized fields with traceable provenance. Keep `-1` as missing, not as a negative answer. No neutral category and no generic R5 `997` “not asked” may be projected into these specific question domains without exact evidence.

**Primary uncertainty:** valid national-only design-weighted proportions and a 95% CI for the difference, with independent wave-specific PSU/strata/weight designs and respondent-level item-missing diagnostics. Small-cell and subgroup use would demand separate variance and support qualifications; no “±2% per wave” substitute for difference-of-design-based-S.E. and no population causal inference.

## Required chain (all held, none granted)

### D0 Original and prompt/country/original instrument proof

1. Recover **fielded/indigenized Uganda R5 2011–12 questionnaire** Q7 in English and actual interview languages and adjacent lead-in; request from Afrobarometer Data Management and R5 Wilsken Agencies historical national custodians. June 2012 country codebook and summary are not its manuscript.
2. Obtain rendered page-image/screenshot custody for official R5 codebook printed pp. 2 and 9–10, R5 2012 national summary Q7, R9 Dec 28 2021 questionnaire pp. 2–6, R9 codebook pp. 8 and 67–68, R9 TIF printed p. 4. In this review the PDF page text index was accessible but all web page screenshots returned **cache miss**; no visually certified original pages. Confirm whether 2021 R9 manuscript was final as actually administered and how revisions/languages map.
3. Adjudicate the R9 framing expansion versus R5 short introduction as a **comparability uncertainty**; same end response labels are insufficient evidence of question-level invariance.

### D1 Source dictionary/retention identity proof: allowed only by **fresh narrower separate HQ scope**

4. Identify exact physical stored `data/Data/Afro Barometer Round 5.sav` and `data/Data/Afro Barometer Round 9.sav`, reconfirm their SHA-256 against the upstream HQ269 **documentary-only** recorded hashes: R5 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` (49,689,458 bytes), R9 `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` (70,621,348 bytes). This worker **did not access or hash those SAVs**. The cited values are previous custody receipts, not newly verified.
5. Under separate authorization **dictionary-only (no respondent-row iteration or survey execution)** enumerate both retained files' codebook metadata **Q7/Q3 labels and code/value/missing metadata, country variable and Uganda country code, version or file producer, national-vs-supplement designation variable or manifest, eligibility, stratum, PSU, primary design weights `withinwt` / `withinwt_ea` / `withinwt_hh`, adult count, respondent-ID string; file-level national inclusion/distribution documentation**. Confirm actual presence/meaning via external owner declarations, not by asserting from PDF alone.
6. Prove how `R5 6,200` country respondent-ID span maps to **2,400** official national probability interviews and the **3,800** USAID targeted supplemental interviews, and how `R9 3,392` maps to **2,400** national plus **992** city specials. The count of the archived country file is **not established in this worker**. If a retained file is national-only, obtain the exact producer/release note and identity; otherwise require explicit flags/record inclusion lists. Neither `RESPNO` range nor `URBRUR` alone establishes this.
7. Reconcile Afrobarometer Uganda R5 country codebook **June 2012**, multinational merged R5 codebook **July 2015**, Uganda R9 original questionnaire **28/29 Dec 2021**, R9 codebook cover **April 2023** hosted 2024, R9 World Bank catalog `UGA_2022_AFB-R9_v01_M` and the 2,400-case November 2023 updated file, versus exact Rawlsing asset. Preserve divergences in weighting/observations as release-specific facts, not automatic errors. Confirm whether release country codebooks cover special oversamples while public national releases exclude them.

### D2 National design and estimation competence

8. From producer/custodian: exact R5 and R9 national selection probability frame, urban/city/region-stratum construction, PPPS EA units, PSU IDs, household walks/card vs tablet choice, oversample sampling overlap, substitutions and excluded strata; verify national weights **for selected release**, whether `withinwt` R5 blank TIF is merely omitted vs unknown, whether R9 `withinwt_hh` (with ADULT_CT) is authoritative vs `withinwt_ea`, and whether city supplemental records have distinguishable weights. Do **not** infer authority because fields exist.
9. Prespecify independent sample complex-survey variance method, lonely PSU handling, design degrees-of-freedom, alternative weighting sensitivity, effective sample size/design effect, DK/refusal/missing behavior, translation and frame changes, and country nationally valid weighting after city/district supplemental exclusion. Use national-only **2,400** as intended national reference in *each* wave, subject to source lineage. No unauthorized observed counts/estimates.
10. Only then propose (not self-issue) an **exact Uganda R5 Q7↔R9 Q3 comparable-measurement warrant** with target population, exclusion, concept, code mapping, temporal endpoints, source-byte/release IDs, permitted analyses and uncertainty/limits. Distinct EE12/C7 pair use must be formally adopted by owner/HQ; historical **51** response/question continuity edges are merely lineage, not a substitute. Downstream objective-world/F6/N7/N9/EE14 serving needs its separate consumption permission and actual evidence; the actor/V3 firewall stays intact.

## Hard scientific refusals

- No recovered **original R5 interview manuscript**, no visually verified official PDF pages; country codebook Q7 and 2012 summary only.
- No evidence permitting **6,200** R5 or **3,392** R9 all-case files as national samples.
- No exact producer-issued national-only **record selector**, weight-and-PSU tuple or verified archive-to-release mapping.
- No demonstrated **measurement invariance** for changed R9 preamble or translations.
- No design-based trend, wave difference, marginal or uncertainty computation; no row processing.
- No pair/use permissions, EE12/C7 grant, T2 or PRE-V3 service result.

## Supporting exact documentary URLs

- R5 Uganda **country** codebook: https://www.afrobarometer.org/wp-content/uploads/2022/02/uga_r5_codebook.pdf
- R5 Uganda summary: https://www.afrobarometer.org/wp-content/uploads/2022/02/uga_r5_sor.pdf
- R5 34-country later merged codebook: https://afrobarometer.org/wp-content/uploads/migrated/files/data/round-5/merged_r5_codebook.pdf
- R9 Uganda original English questionnaire: https://www.afrobarometer.org/wp-content/uploads/2023/06/UGA_R9.Indigenized-questionnaire_29Dec21-Final.docx.pdf
- R9 Uganda country codebook: https://www.afrobarometer.org/wp-content/uploads/2024/05/UGA_R9.Codebook_16Apr24.final_.pdf
- R9 Uganda summary and Technical Information Form: https://www.afrobarometer.org/wp-content/uploads/2023/08/UGA_R9_Summary-of-results_Afrobarometer-9aug23.pdf
- R9 public country release: https://microdata.worldbank.org/catalog/6756/data-dictionary/F1
- Official Afrobarometer sample and weight guidance: https://www.afrobarometer.org/surveys-and-methods/sampling/
- Prior HQ269 scientific candidate docket: `WORKER_RETURNS/PYAT-HQ269-S01-EXACT-MEASUREMENT-STRUCTURAL-AND-TEMPORAL-COMPETENCE-R1/03_DISPOSITION.json @ c2170891fdb1d3713beaeac4c52dfc105de6ff78`.

**Terminal scientific court:** `CANDIDATE_BOUNDED__NATIONAL_COMPARABILITY_HOLD__NEEDS_ORIGINAL_R5_INSTRUMENT_AND_EXACT_NATIONAL_SOURCE_DESIGN_WARRANT`.
