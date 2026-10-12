# Ghana R5 Q86A — original source vs exact retained metadata court

## Disposition

**Exact retained physical Q86A dictionary: prior M01 witness positive and HQ272 evidence-credited; original Ghana item: official primary-document positive; country-specific source-row mapping / edition / scientific operation: HELD.**

### 1. Three distinct source objects, not one falsely matched release

| Object | Identifying evidence | What it does *not* establish |
|---|---|---|
| 2012 national **Ghana fielded English instrument** (final 19 April 2012) | Ghana p20 Q86A asks citizenship opinion for Ghana-born person with one Ghanaian/non-Ghanaian parent; one randomly selected Ghanaian citizen adult 18+ in common questionnaire | Actual physical file's respondents/translation variants, any true row exposure |
| Published Ghana R5 *country-specific* dataset and IHSN `GHA_2012_AFB-R5_v01_M` | IHSN data dictionary enumerates Q86A and RESPNO; **2,400 cases / 354 variables**; original public use + version documentation | File byte equality to Rawlsing's merged R5 archive, 2,400 valid Q86A denominator |
| Rawlsing retained R5 *merged* SAV | M01 on second Mac previously hashed **49,689,458 bytes SHA256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`**, metadata header **51,587 × 348**, stored `Q86A` with exact six categories | Any Ghana row/subject subset, release-edition version match, unique (COUNTRY,RESPNO), accepted RAW unary permission |

The **354 vs 348** difference is not a proof of contradiction, but proves we cannot identify country and merged release byte objects merely by survey label. Neither published source carries a verified counterpart byte SHA in the examined original-document chain.

### 2. Actual physical dictionary and original semantics

M01 source-data-neutral readback in `01_FILE_SHA_DICTIONARY_AND_NATIONAL_SAMPLE_METADATA.json` (blob `742af5e5be98cf604d04aac56ae0c6116c54744f`) reports **`Q86A` present** in the same exact merged R5 SHA. Native retained label: *Q86a. Right to be citizen: born in country with one non-citizen parent*. Stored code labels: `0 No`, `1 Yes`, `9 Don't know`, `997 Not asked`, `998 Refused`, `-1 Missing`. No SPSS user-missing ranges or user-missing values were defined in the returned dictionary (empty objects); thus explicit *source-semantic typed missingness* is essential, and SPSS missing declarations alone must **never** select substantive risk.

Independent Ghana official English questionnaire is more specifically Ghana-focused than the retained *merged* label. Their corresponding Q86A item location and code categories are documentary grounds for a **candidate exact field-semantic mapping**, not a silently adopted equivalence for translated and nationally fielded responses.

M01 reports physical `RESPNO` present but **no uniqueness proof**; physical `COUNTRY` and `COUNTRY_ALPHA` are present (numerical coding). `COUNTRY_ALPHA3` is absent from the SAV; inherited `wave1_r5_q86_c11_projection.py` used a *derived* `COUNTRY_ALPHA3` coordinate. Official merged codebook reports Ghana `COUNTRY_ALPHA=11` and RESPNO range `GHA0001–GHA2400`, not a physical observed country selector or validated member set. A separate authority-approved country crosswalk and **real respondent bindings** are required.

The header has `file_label: null`; a matching retained SHA establishes the historical file identity, **not its official published edition**. M01 on an authorized second Mac previously found the SAV; separate HQ262 E01 on another Mac had `ABSENT`, and those are host-specific observations rather than conflict or universal disappearance.

### 3. Field-equivalence matrix at each necessary grain

| Grain | Verdict | Evidence / unresolved owner |
|---|---|---|
| Original Ghana Q86A item administered, native text and 0/1 semantic response | **DOCUMENT_POSITIVE** | HQ273 S01 original national questionnaire + official merged codebook |
| Exact retained merged R5 bytes and native `Q86A` column | **PRIOR_PHYSICAL_METADATA_POSITIVE** | M01 SHA and dictionary read on different Mac, credited by HQ272; no new A03H read |
| M01 Q86A metadata inspection's legal source-science scope | **COMPETENT_RATIFICATION_HOLD** | HQ262 explicitly foregrounds Ghana Q43/R9 Q31 while broadly allowing some column labels; HQ272 left Q86ABC inspection applicability undecided |
| Public country-data `Q86A` → retained merged column Q86A | **CANDIDATE_DOCUMENTARY_BRIDGE** | Corresponding labels/codes; no official version and form/recode/permutation byte crosswalk |
| Ghana country selector and individual person reference | **HELD_REAL_ROW_BOUND** | COUNTRY / COUNTRY_ALPHA / RESPNO column presence, no eligible-row or uniqueness evidence |
| Per-respondent Q86A routing / selected-adult eligible, asked and substantive risk | **HELD_REAL_ROW_BOUND** | Original common-form expected question is not an actual `RoutingEligibilityFact` |
| Design/weights for population inference | **HELD_NOT_NEEDED_FOR_RAW** | RAW restricted descriptive; `withinwt` presence is not an estimator or variance warrant |
| Ghana source-read/I03 operation/use/consumer | **NO_POSITIVE_GHA_GRANT_FOUND** | frozen GT1 19,210 excludes Ghana; separate issuer required |

### 4. No false metric/semantic transposition

A response in `Q86A=9` is **DK**, not a Yes vote; `997` is *not asked*, `998` refused, `-1` missing. Numeral equivalence does not allow importing `Q97=9` (postgraduate) or `Q8A=9` (DK). This country-only qualitative opinion is not the state of Ghana citizenship law, not an objective material causal force, and not weighted Ghana adult opinion prevalence without a separate design warrant.

**Source evidence manifest:** A03G `01_PRIMARY_RELEASE_PHYSICAL_FIELD_AND_RESPONDENT_WARRANT.json`, HQ273 S01 original Ghana report (blob `8b6fd01af4dde339cd35eb7faa241e4935a63363`), official [Ghana questionnaire](https://www.afrobarometer.org/wp-content/uploads/2022/02/gha_r5_questionnaire.pdf), official [merged R5 codebook](https://afrobarometer.org/wp-content/uploads/migrated/files/data/round-5/merged_r5_codebook.pdf), [IHSN country dictionary](https://catalog.ihsn.org/catalog/8848/data-dictionary/F1), plus M01 primary previously executed metadata return. Original PDFs **not newly reopened by A03H**, PDF byte hashes not invented.
