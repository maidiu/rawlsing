# PYAT HQ254 E01 — A048 measurement, population, estimand and uncertainty court — R1

**DISPOSITION:** `SCIENTIFICALLY_PLAUSIBLE_DESCRIPTIVE_PAIR__NOT_YET_QUALIFIED_FOR_TEMPORAL_INFERENCE`  
**TERMINAL:** `HQ254_E01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`

No raw survey opened. No numerator, denominator, estimate, difference, sign, p-value or confidence interval is calculated here.

## 1. Measurement court

HQ253 already established the source-level fact pattern and E01 does not re-fetch the question texts. The two Austrian field instruments have the same substantive target clause and approve/disapprove direction, but their respondent presentation is not identical: 1990 is visibly interviewer-read in the national block, while 2008 explicitly introduces Liste 53 and also reads the row aloud. The 1990 integrated/master representation additionally references Card Z. Repo witness: `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ253_R01_R02_INDEPENDENT_INTAKE_AUSTRIA_PRIMARY_SCAN_AND_T0_FIRST_TEST_R1.md @ 85f2835dc5b26735ed9ed36a6cb52ee11fc5abea`, blob `db045dff5d4340faa9abe604ef6e0cc8fe1f2c9e`, lines 26–38.

**Court result:**  
`SAME_TARGET_SEMANTICS__SAME_SUBSTANTIVE_DIRECTION__DISPLAY_AND_INSTRUCTION_EQUIVALENCE_UNPROVED`.

That difference can affect response process through visual anchoring, battery context, respondent burden, satisficing or social-desirability dynamics. E01 has no validation study quantifying such an effect, so it may not assume either “zero effect” or “fatal break.” The measurement difference is a **non-sampling comparability uncertainty** that ordinary survey standard errors do not capture.

The EVS Trend File `ZA7503 v3.0.0` is an official harmonization product, but harmonization is a data-engineering/semantic correspondence layer, not a randomized administration experiment. It cannot by itself certify measurement invariance. GESIS current source: https://www.gesis.org/en/european-values-study/data-and-documentation/evs-trend-file-1981-2017.

## 2. Population court

### Native 2008 universe

Primary Austria-2008 method documentation defines the universe as persons **18+ resident in private households regardless of nationality/citizenship/language**. Source: https://access.gesis.org/dbk/17933, PDF p.13, extracted lines 341–345.

### What is known for 1990

GESIS's current 1990 wave description says adult population 18+, but its public wave summary does not provide the Austria-specific citizenship/residence/private-household boundary. Source: https://www.gesis.org/en/european-values-study/data-and-documentation/2nd-wave-1990.

The later AUSSDA Austria 1990–2018 longitudinal metadata describes its universe as eligible **Austrian citizens**, older than 18 at survey start, with registered residence in a private household in Austria. Source: https://data.aussda.at/dataset.xhtml?persistentId=doi:10.11587/C4YBOT, metadata lines 285–290. This is highly relevant national-series evidence, but because it is metadata for the combined longitudinal product it does not by itself prove the exact 1990 source frame or resolve the apparent “18+” versus “older than 18” boundary.

### Defensible common target candidate

If later documentary/source verification confirms the necessary variables and frame, the strongest conservative common population candidate is:

> Austrian citizens in the verified common lower-age domain, registered/resident in Austrian private households, who were eligible for and actually exposed to the exact A048 source item in the relevant wave.

This is intentionally an **intersection target**, not an assertion that the two native samples had identical universes. Because 2008 explicitly includes non-citizens, a common-citizen estimand would require a verified 2008 citizenship restriction; because 1990's exact frame is not yet primary-qualified, the same restriction must be source-grounded there too. The inclusive age boundary (18+ vs strictly older than 18) must be resolved from wave-specific primary metadata before execution.

If those restrictions cannot be verified without changing the substantive target, then the lawful product is **two native-wave descriptive population quantities with explicit universe labels**, not a single same-population temporal difference.

## 3. Candidate estimands — definitions only

### A. Source-native unweighted descriptive quantity

For each wave separately: among respondents in the verified country/item-risk set who were actually eligible/exposed and have a substantive valid response, report the **unweighted sample proportion approving**.

Status: `DESCRIPTIVE_SAMPLE_QUANTITY_ONLY`. It must not be called a nationally representative population estimate and carries no automatic design-based interval.

### B. Weighted population descriptive quantity

For each wave separately: among the verified common-target or explicitly native-target analytic population, report the **weighted proportion approving among substantive valid responses**, using exactly one source-qualified weight whose construction corresponds to that target.

1990: official ZA4460 documentation establishes `weight_g` as gender/age calibration and shows Austria is not in the no-weight group. Source: https://access.gesis.org/dbk/50678, PDF p.24, lines 763–770.

2008: official national report describes the EVS `weight` as gender×age calibration and separately says Austria has an additional country-specific original weight. Source: https://access.gesis.org/dbk/17933, PDF p.21, lines 629–656.

**Forbidden shortcuts:**
- do not multiply EVS and Austria-original weights absent explicit source instruction;
- do not substitute cross-country equalization/population weights for a within-Austria target;
- do not infer a probability/inclusion weight merely because a variable is named “weight”;
- do not use national n=1460 or n=1510 as the A048 denominator;
- do not collapse unasked/not-applicable/don't-know/no-answer into the substantive denominator without an adopted missingness rule.

S03's earlier candidate had the correct high-level grain: wave-specific Austrian adults eligible and asked A048, substantive valid responses, correct design/weight, repeated cross-sections rather than a panel. Repo witness: `WORKER_RETURNS/PYAT-HQ250-S03-EVS-ONE-CONSTRUCT-COMPARABILITY-R1/EXACT_TWO_WAVE_LINEAGE.json @ d7c529a2aaa424e558137daeb0f81ea678955928`, blob `b21613ce1e46ec730a5d8003658b75d40f70db22`, lines 153–154. E01 narrows it by requiring exact population-overlap and weight provenance before temporal use.

## 4. Missingness / item-risk court

The denominator must be the source-specific **item-risk + substantive-valid** set, not the whole national sample. Distinguish at minimum:
- not asked / source absence;
- not applicable / routed out;
- don't know;
- no answer/refusal;
- other/system missing;
- substantive approve/disapprove.

Harmonized `-1..-5` trend codes cannot be presumed to preserve every native pathway without the source-specific bridge. The exact retained-source column/value lineage therefore remains a prerequisite before executing SRC12/SRC14.

## 5. Uncertainty court

### 1990

The public primary documentation recovered here establishes a calibration weight, but not the Austria-specific frame, PSU/strata, inclusion probabilities or exact selection rule. Therefore:

`1990_DESIGN_BASED_SE_CI = NOT_QUALIFIED`.

An iid/SRS confidence interval applied merely because `weight_g` exists would manufacture precision. If an authoritative country method later confirms a probability sample and the necessary cluster/stratum information is available or reconstructable, a design-consistent variance method (e.g. Taylor linearization or source-appropriate replicate resampling) may be commissioned. If the primary method instead proves quota/non-probability selection, probability-design intervals are invalid; uncertainty must be explicitly model-based/sensitivity-based, and selection bias remains a separate identification problem.

### 2008

The 2008 design is explicitly stratified and clustered with election-unit PSUs and 375 sample points. A valid design-based variance requires the analysis-accessible PSU/stratum structure and the chosen weight/inclusion logic. The age×sex calibration weight by itself is insufficient. Source: https://access.gesis.org/dbk/17933, PDF pp.18,21.

### Any later temporal contrast

The waves are repeated independent cross-sections, not a person panel. If pair authority is later adopted, uncertainty for a difference must propagate both wave-specific sampling/weight uncertainty and keep the administration/protocol difference visible as **measurement-comparability uncertainty**, rather than pretending the latter is contained in a sampling CI.

## 6. Qualification/disproof matrix

| Gate | Current E01 result | What would disprove/stop it |
|---|---|---|
| Same construct target | `DOCUMENTARY_SEMANTIC_PASS` | Primary source shows materially different target/response meaning |
| Same administration | `NO__DIFFERENCE_CONFIRMED` | N/A; difference already observed |
| Difference tolerable for target use | `UNPROVED` | Validation/source evidence shows material response-process break |
| 1990 probability design | `SECONDARY_CORROBORATED__PRIMARY_UNPROVED` | Primary country method shows quota/non-probability or non-reconstructable selection |
| 1990 national calibration | `PRIMARY_DOC_PASS` | Official corrected release supersedes or negates documented `weight_g` |
| Common population | `CANDIDATE_ONLY` | 1990 frame or 2008 restriction cannot support a defensible intersection |
| Source byte/version binding | `UNPROVED` | Public checksum/version evidence mismatches retained SRC12/SRC14 identities |
| Design-based 1990 uncertainty | `BLOCKED` | Only unblocked by primary design + sufficient variance inputs |
| Temporal pair authority | `ABSENT` | Must be separately issued/adopted; E01 cannot self-grant |

## 7. Smallest next scientific/documentary action

**Owner:** GESIS/EVS archival methodology custodian + AUSSDA/University of Vienna Austrian-series custodian for source facts; independent survey statistician for inferential qualification; HQ/EE12 owner for any later pair relation.

**Single next lawful action:** bank one fixed, non-raw Austria-1990 method/version packet that resolves sample type/frame/stages/person selection/weight construction and, if available, checksum/release lineage to the frozen SRC12/SRC14 identities; then independently adjudicate the common target and variance method.

Until that occurs, the most accurate state is:

`A048_AUSTRIA_1990_2008_DOCUMENTARILY_PLAUSIBLE__DESIGN_VERSION_AND_MEASUREMENT_QUALIFICATION_INCOMPLETE__PAIR_NOT_READY`.

`HQ254_E01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`
