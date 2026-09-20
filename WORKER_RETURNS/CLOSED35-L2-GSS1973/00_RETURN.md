# CLOSED35-L2-GSS1973 — GSS 1973 Split-Form / Routing / Weight Documentary Authority Closure

Status: `PASS__DOCUMENTARY_AUTHORITY_CLOSED__REALIZATION_NOT_EXECUTED`

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-premain-fiabc-s35-fanin-r1`  
Accepted base tip: `770d95c1a604ea1f47ac2971b923673c14c42984`  
Worker branch: `agent/rabochii-closed35-l2-gss1973-authority-r1`

Canonical source: `GSS1973.sav`  
Canonical SHA-256: `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2`

## Holding

The source-specific documentary debt for GSS 1973 is closed to the level needed for a later source-specific realization court.

No raw source carrier was opened. No source processing was executed. No measured P2X was run.

The closure is documentary: it establishes the producer-authorized form topology, form-assignment mechanism, routing/missing-state law, 1973 sample design, lawful weight applicability, and income-variable history. A later realization must bind these authorities to the exact canonical bytes and fail closed on any mismatch.

## 1. Exact 1973 experimental-form authority

NORC Appendix P states that:

- the GSS used a split sample in 1973;
- `FORM=1` is the standard wording;
- `FORM=2` is the "y" variant wording;
- Appendix P Table P.1 is the exhaustive register of questions that differ in wording/order or appear on only one experimental form.

The 1973 questionnaire supplies the respondent-facing identity. At Q56 it commands:

> ASK THE "X" OR "Y" VERSION; DEPENDING ON THE LETTER ON THE COVER OF THIS QUESTIONNAIRE.

The X wording has four social-class response names: lower / working / middle / upper.  
The Y wording has five: lower / working / middle / upper-middle / upper.

The cumulative codebook independently identifies `CLASSY` as the Form-2 1973 variant of `CLASS`. The lawful mapping is therefore:

- questionnaire X / `FORM=1` / standard wording -> `CLASS`;
- questionnaire Y / `FORM=2` / y-variant wording -> `CLASSY`.

Do not collapse `CLASS` and `CLASSY`. The five-category Y wording has a distinct response space.

For all released variables not in the producer's form-difference register, form assignment is not itself authority to divide the denominator. Ordinary questionnaire filters and substantive nonresponse remain independent dimensions.

## 2. Form assignment and denominator law

GSS Methodological Report 36 gives the 1973 assignment mechanism.

For the block-quota surveys including 1973, form was randomized **within quota types**. The quota assignment sheet specified whether form X or Y was to be administered. Where two cases of the same quota type were assigned, the first completed respondent of that type received X and the second Y. Once the actual respondent had been selected, form administration was not subject to interviewer discretion.

Consequences:

1. `CLASS` and `CLASSY` have form-eligible denominators, not the full 1,504-case denominator.
2. The complement form is **form-not-administered**, not item nonresponse.
3. Common questions remain eligible on both forms unless an independent questionnaire route/filter says otherwise.
4. A later realization may compute exact realized form counts from `FORM`; this documentary worker does not infer those counts from cumulative frequencies.

The 1973 total sample is 1,504 cases; the historical design is the 1970-frame block-quota design.

## 3. Do not confuse FORM X/Y with Q105 Card X/Y

The 1973 questionnaire also contains a separate Q105 experiment instructing the interviewer to hand Card X or Y and later re-ask the card-dependent question for a routed subset.

No located NORC document establishes that Q105 Card X/Y is the same assignment coordinate as the questionnaire-cover FORM X/Y used at Q56.

Therefore:

- `FORM` X/Y and Q105 Card X/Y are separate documentary identities;
- no join or equivalence between them is authorized here;
- Q105 also has an independent route keyed to Q102 birth-year last digit;
- the machine-extracted scan contains an apparent digit-list inconsistency, so an executable Q105 digit-set rule must be visually verified against the source page before realization. This local scan ambiguity does **not** reopen the FORM/CLASS/CLASSY closure.

## 4. Routing / missing-state classification

A single physical missing code must never be used to infer why a value is absent.

The later realization must classify absence in this precedence order:

1. `FORM_NOT_ADMINISTERED` — producer form registry says the respondent's FORM was not eligible for that form-specific item.
2. `ROUTED_SKIP` — explicit questionnaire filter/skip makes the respondent ineligible.
3. `SUBSTANTIVE_NONRESPONSE` — the respondent was eligible and the instrument/codebook supplies a response-state such as don't know, no answer, or refused.
4. `PHYSICAL_MISSING_UNCLASSIFIED` — physical/system missingness with no documentary semantic cause. Preserve it; do not guess.

The modern SPSS cumulative release standardizes negative reserve codes, but those release encodings are not substitutes for the source-native eligibility proof above. Some legacy GSS variables also use combined missing categories; where producer documentation does not separate causes, the realization must preserve the combined state rather than fabricate decomposition.

## 5. Income history — chronology proven, equivalence rejected

Official GSS repeated-item documentation gives this family-income variable history:

- `INCOME72` in 1972;
- `INCOME` since 1973;
- `INCOME77` for 1977–1980;
- `INCOME82` for 1982–1985;
- `INCOME86` for 1986–1990;
- `INCOME91` for 1991–1996;
- `INCOME98` for 1998–2004;
- `INCOME06` from 2006 onward in that documentation generation.

Appendix N is stronger still: response categories were revised between 1972 and 1973 and the groupings are treated as separate questions and variables.

The 1973 questionnaire Q101 asks for total family income from all sources in **1972**, before taxes, using the 1973 response categories.

Therefore:

- `INCOME72` and 1973 `INCOME` remain distinct source-variable identities;
- this closure does **not** authorize semantic equivalence merely because both measure total family income;
- any cross-year harmonization must use an explicit producer recode/crosswalk (for example producer-created constant-dollar recodes) and remains a separate analytical operation.

## 6. 1973 sample design and lawful weights

### Historical design

Appendix A identifies the 1972–1974 surveys as multi-stage area probability samples through the block/segment level with quota selection at the block level. Quotas were based on sex, age, and employment status.

MR036 confirms that 1973 form X/Y was randomized within those quota types and was not subject to interviewer discretion after respondent selection.

### Form-specific correction

No 1973 `FORMWT` adjustment is authorized.

NORC's form-randomization repair concerns the defect affecting 1978, 1980, and 1982–1985. Modern post-stratification documentation likewise identifies form corrections for those years, not 1973.

Therefore do not import `FORMWT`, `BALLOTFORMWT`, or a later form-error correction into 1973.

### Current producer-authorized analytical weight

NORC now explicitly recommends `WTSSPS` for most GSS analyses and states that it spans 1972 through 2024. MR137 documents the historical post-stratification extension back through 1972–2018.

Thus `WTSSPS` has explicit producer authority for 1973 and is not an inference from a later-year name.

`WTSSNRPS` is only available for 2004–2024 and is not a 1973 weight.

For 1972, 1973, and 1974, MR137 states that strata and clustering are not used for survey estimation because quota sampling was used. Do not import later `VPSU`/`VSTRAT` variance assumptions into 1973.

Realization rule:

- if the exact canonical `GSS1973.sav` exposes the release-authorized `WTSSPS`, bind it as the general 1973 post-stratification weight;
- preserve FORM eligibility when analyzing `CLASS` or `CLASSY`; the weight does not turn a form-specific item into a full-sample item;
- do not synthesize a weight if the exact carrier does not contain the authorized field;
- no source-specific form adjustment is required or authorized by the located producer documentation.

## 7. Exact unknown set after closure

The documentary court intentionally leaves only realization-level or genuinely unproved items:

- exact realized X/Y case counts in the canonical SAV — compute later from exact bytes, not from cumulative aggregates;
- exact physical negative-code representation of each semantic missing state in this specific SAV — bind later from source metadata plus documentary semantics;
- exact Q105 Card-X/Y assignment relationship to respondent FORM — **not proven; preserve separate identities**;
- exact Q105 odd/even digit list from the scanned page — machine text is internally inconsistent and must be visually checked before executable use;
- any cross-release semantic equivalence for `INCOME72` and `INCOME` — **not authorized**.

None of these unknowns blocks the source-specific realization of the 1973 FORM / routing / weight authority because each has a fail-closed treatment.

## 8. Principal official sources

- 1973 GSS questionnaire: https://gss.norc.org/content/dam/gss/get-documentation/pdf/quex/1973%20GSS%20Quex.pdf
- GSS Appendix P — Experimental Forms: https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/GSS_Codebook_AppendixP.pdf
- 1972–2018 cumulative codebook: https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/GSS_Codebook.pdf
- GSS MR036 — Problems in Form Randomization: https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR036.pdf
- Appendix A — Sampling Design and Weighting: https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/A.pdf
- GSS MR137 — Post-stratification Weights: https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR137%20Poststratification%20Weights.pdf
- GSS FAQ — current weight recommendation: https://gss.norc.org/faq.html
- Repeated Items in the GSS: https://gss.norc.org/Documents/codebook/Replicating%20Core_0707.pdf
- Appendix N — Changes in Question Wording / Response Categories / Format: https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/GSS_Codebook_AppendixN.pdf

## Terminal

`CLOSED35_L2_GSS1973_SPLIT_FORM_ROUTING_WEIGHT_AUTHORITY_CLOSED__READY_FOR_SOURCE_SPECIFIC_REALIZATION`
