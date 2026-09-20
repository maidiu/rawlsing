# GSS 1973 — Weight, Design, and Income-Rename Authority

Canonical carrier: `GSS1973.sav`  
Canonical SHA-256: `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2`

This document is documentary authority only. It does not assert that a field exists in the canonical SAV until the later source-specific realization observes that field in the exact carrier.

## A. 1973 design

### A1. Sample design

Official GSS Appendix A identifies the 1972–1974 surveys as **block-quota** samples:

- multistage area-probability selection through PSU / block-or-segment stages;
- quota sampling at the block/segment level;
- quota controls based on sex, age, and employment status.

The historical cumulative codebook reports 1,504 completed interviews in 1973 and identifies 1973 with the 1970 sample frame / block-quota design.

This design is not interchangeable with the full-probability design introduced on split halves in 1975/1976 and used thereafter.

### A2. Experimental-form assignment inside the 1973 design

GSS Methodological Report 36 is controlling for the X/Y assignment.

For the block-quota surveys 1973, 1974, and 1976:

- experimental form was randomized **within the quota types**;
- quota assignment sheets told interviewers whether to administer X or Y;
- when two interviews of a quota type were assigned, the first completed interview of that type received X and the second Y;
- once a respondent had actually been selected, form administration was not at interviewer discretion.

Thus the form coordinate is a producer-designed experimental assignment, not a missingness pattern that Rawlsing may reconstruct from observed responses.

## B. Weight authority

### B1. Historical household-size weighting exists, but is not a 1973 form adjustment

GSS Methodological Report 3 documents standardized household-size weights for the 1973 probability-with-quotas sample. Appendix A later describes `WTSSALL` as applying the adults-in-household adjustment to pre-2004 years.

This is historical sample-weight authority. It is **not** authority to identify or repair X/Y form assignment.

### B2. No 1973 FORMWT

GSS Methodological Report 36 locates the defective form-randomization procedure in the later full-probability surveys, specifically the affected 1978–1985 period. The modern GSS weight documentation names form-error corrections for 1978, 1980, 1982, 1983, 1984, and 1985.

1973 is not in that correction set.

Therefore:

- do not apply `FORMWT` to 1973;
- do not apply `BALLOTFORMWT` to 1973;
- do not manufacture an equal-form rescaling;
- preserve the actual FORM-specific denominator.

The fact that 1973 used two forms does not itself create authority for a form weight.

### B3. Current producer-authorized default: WTSSPS

Current NORC authority is explicit.

The GSS FAQ states that:

- weighted analysis is recommended;
- `WTSSPS` is recommended for most analyses;
- `WTSSPS` spans 1972–2024;
- `WTSSNRPS` is available only for 2004–2024.

Release notes document the extension of post-stratification weights back through 1972–1987. Methodological Report 137 describes the construction of the historical post-stratification weights and recommends the new weight for future GSS analyses.

This is explicit 1973 applicability, so it is lawful under the CLOSED35 rule against importing later assumptions merely by analogy.

### B4. Binding for source-specific realization

For a person-level cross-sectional estimate from the 1973 source:

1. require exact source identity `GSS1973.sav` / canonical SHA;
2. require the exact carrier to expose the producer-authorized `WTSSPS` field;
3. use `WTSSPS` as the current producer-recommended general weight;
4. for `CLASS` or `CLASSY`, first restrict to the producer-authorized FORM-eligible risk set; weighting does not make the complement form eligible;
5. do not stack `FORMWT`, `BALLOTFORMWT`, or `WTSSNRPS`;
6. if the canonical carrier does not expose the authorized field, fail closed rather than synthesize a weight.

Legacy `WTSSALL`/household-size weighting remains documented historical authority, but it is not the current NORC default where `WTSSPS` is available.

### B5. Variance / design binding

Methodological Report 137 states that **strata and clustering are not used for survey estimation in 1972, 1973, and 1974 because quota sampling was used**.

Therefore the 1973 realization must not import later-year `VPSU`/`VSTRAT` complex-sample variance treatment merely because such fields exist in other GSS years.

This does not convert the original block-quota sample into a simple probability sample; it states the producer's current analysis instruction for these quota years.

## C. Income variable history

### C1. Exact producer chronology

Official GSS repeated-item documentation states:

- `INCOME72` — 1972;
- `INCOME` — since 1973;
- `INCOME77` — 1977–1980;
- `INCOME82` — 1982–1985;
- `INCOME86` — 1986–1990;
- `INCOME91` — 1991–1996;
- `INCOME98` — 1998–2004;
- `INCOME06` — 2006 onward in that documentation generation.

It explicitly says differences among these measures reflect expansion of the income ranges over time.

### C2. 1972 → 1973 change is substantive source history, not a harmless rename

Appendix N states that income response categories were revised **between 1972 and 1973**, and that the resulting groupings are treated as **separate questions and variables**.

The 1973 questionnaire Q101 asks:

- total **family** income;
- from all sources;
- in the prior year, 1972;
- before taxes;
- using the 1973 category scheme.

Therefore the lawful identity relation is:

`INCOME72@GSS1972 != INCOME@GSS1973`

at source-variable identity and response-dictionary grain.

The documentary record proves chronology. It does **not** prove lossless response-level semantic equivalence.

### C3. Allowed and forbidden transformations

Allowed only with separate producer authority:

- producer-defined recodes such as `REALINC` / `CONINC`;
- an explicitly documented harmonization with its own assumptions and target units.

Forbidden:

- renaming `INCOME72` to `INCOME` and treating the raw categories as identical;
- joining categories because labels appear similar;
- carrying a 1972 response code directly into the 1973 response dictionary;
- using raw-variable identity as if it were a longitudinal construct identity.

## D. Source authorities

1. 1973 GSS Questionnaire  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/quex/1973%20GSS%20Quex.pdf

2. Appendix A — Sampling Design and Weighting  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/A.pdf

3. Appendix N — Changes in Question Wording, Response Categories, and Format  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/GSS_Codebook_AppendixN.pdf

4. Appendix P — Experimental Forms  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/GSS_Codebook_AppendixP.pdf

5. GSS Methodological Report 3 — Weighting the General Social Surveys  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR003.pdf

6. GSS Methodological Report 36 — Problems in Form Randomization  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR036.pdf

7. GSS Methodological Report 137 — Post-stratification Weights for GSS 1972–2022  
   https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR137%20Poststratification%20Weights.pdf

8. GSS FAQ — current weight recommendation  
   https://gss.norc.org/faq.html

9. Repeated Items in the General Social Survey  
   https://gss.norc.org/Documents/codebook/Replicating%20Core_0707.pdf

10. Release Notes GSS 1972–2022 Release 2  
    https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/Release%20Notes%207222.pdf

## E. Governing realization constants

```text
SOURCE = GSS1973.sav
SOURCE_SHA256 = 59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2

DESIGN = BLOCK_QUOTA__1970_FRAME
FORM_ASSIGNMENT = RANDOMIZED_WITHIN_QUOTA_TYPE
FORM_1 = STANDARD__X
FORM_2 = Y_VARIANT__Y

GENERAL_WEIGHT_CURRENT = WTSSPS
GENERAL_WEIGHT_LEGACY = WTSSALL__DOCUMENTED_BUT_NOT_CURRENT_DEFAULT
FORM_WEIGHT_1973 = NONE_AUTHORIZED
NONRESPONSE_POSTSTRAT_WEIGHT_1973 = NOT_WTSSNRPS
STRATA_CLUSTER_VARIANCE_1973 = NOT_USED_PER_MR137

INCOME_1972_ID = INCOME72
INCOME_1973_ID = INCOME
INCOME72_EQ_INCOME = FALSE__NO_SOURCE_EQUIVALENCE_AUTHORITY
```
