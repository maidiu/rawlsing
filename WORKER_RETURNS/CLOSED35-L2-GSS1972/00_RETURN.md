# CLOSED35-L2-GSS1972 — GSS 1972 Documentary Form / Routing / Weight Authority Closure

Status: `PASS__DOCUMENTARY_ROUTING_WEIGHT_AUTHORITY_CLOSED`

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-premain-fiabc-s35-fanin-r1`  
Base tip: `770d95c1a604ea1f47ac2971b923673c14c42984`  
Branch: `agent/rabochii-closed35-l2-gss1972-authority-r1`

Canonical source: `GSS1972.sav`  
Canonical SHA-256: `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`

## 1. Execution boundary

This worker performed documentary research only. It did **not** open the canonical SAV, decode source bytes, execute source processing, or run measured P2X.

Physical facts below are inherited only from the accepted SR09-PRE R05 / PREP71 R05 / PREP72 R10 estate. New semantic authority comes only from official NORC/GSS documentation.

## 2. Inherited L2 burden

The accepted S35 estate classifies GSS1972 as native SAV with source-local row identity, routing/applicability, and weight/design burdens still requiring documentary binding. Accepted prior evidence fixes:

- 1,613 rows / 216 variables in the canonical current year-slice;
- native `id` complete and injective within this exact snapshot but restarting in other GSS releases;
- `sample=1` on all rows, labeled `1960 sample frame, block quota`;
- no `form`, `ballot`, `VPSU`, or `VSTRAT` variable in this exact source;
- exact source weight candidates are `wtssall` and `wtssps`;
- hard replay identity remains source SHA-256 + zero-based source-row ordinal.

This return does not re-measure any of those facts.

## 3. Documentary holding

### 3.1 Controlling 1972 instrument

NORC's official 1972 questionnaire is the source-native routing authority for respondent-facing GSS items. The questionnaire explicitly states that the 1972 GSS was embedded in an NORC omnibus and that questions 51-81 are **not GSS questions and are not included in the cumulative GSS file**.

The instrument contains explicit `IF`, `ASK`, `SKIP`, `GO TO`, substitution, and repeated-person instructions. Therefore:

`missingness != routing authority`

A released source state may be classified as not-asked / inapplicable only when the exact 1972 instrument, or a 1972-explicit GSS codebook entry for a derived/technical field, supplies that applicability rule.

### 3.2 Form / ballot / module applicability

Official NORC design summaries identify 1972 as:

- block-quota (`BQ`) sample;
- no item rotation;
- no experimental forms;
- no topical module;
- no international module.

The accepted source is congruent: no `form` or `ballot` coordinate is present. A form/ballot route must therefore **not** be synthesized for 1972.

### 3.3 Sampling-frame applicability

Appendix A identifies 1972-1974 as modified-probability samples with quota selection at the block level. The 1972 questionnaire itself directs the interviewer to find the person needed to fill the quota. Appendix A documents the multi-stage area selection down to blocks/segments, followed by sex/age/employment quotas at the block level.

MR056 further identifies 1972 as the only GSS using the 1960 NORC sample frame. The inherited exact-source `sample=1` carrier is therefore lawfully bound as a **design-classification coordinate**, not as an analytical weight.

### 3.4 Occurrence and routing

The official questionnaire closes the documentary occurrence grammar needed for realization:

- parental substitution: Q3 controls whether Q4 and the father/mother columns of Q91 occur;
- respondent work history: Q9 routes into Q10-12;
- spouse occurrence: Q13-16 occurs only through marital/work-status conditions;
- Q17-18 selects respondent versus working spouse according to current work/marital state;
- one-person households skip the household-composition subitems after Q19A;
- Q25 contains an explicit `Not asked, inappropriate` response category, proving that "not asked" may be a documented instrument state rather than generic missingness;
- Q82 is asked only if the respondent is currently employed;
- Q91 is a repeated-person matrix over respondent, father, mother, and spouse, with spouse occurrence conditional on current marriage and parent occurrence governed by Q3;
- household/person repetition inside omnibus Q51-81 is outside the GSS and must not be materialized as a GSS1972 occurrence merely because it appears in the paper instrument.

The 1972-2018 cumulative codebook may supplement the questionnaire only when its field entry or appendix explicitly identifies 1972. It may not overwrite exact 1972 wording/routing with a later-year convention.

## 4. Weight and design holding

### 4.1 `WTSSALL`

NORC's historical weighting documentation defines `WTSSALL` as the weight that extends the adults-in-household adjustment to years before 2004. MR003 documents the early GSS household-size problem and 1972-specific probability-with-quotas individual weights.

For this canonical current year-slice, `WTSSALL` is therefore admitted as a **later cumulative historical person-weight construct attached to 1972 cases**. It is not to be represented as an original 1972 fielded weight.

### 4.2 `WTSSPS`

MR137 explicitly says that:

- `WTSSPS` is available for 1972 onward;
- for 1972-1998 its input weight is `WTSSALL` (or an explicitly adjusted version in affected years);
- the post-stratified weight is produced by raking to population controls;
- NORC recommends `WTSSPS` as the default weight for analyses covering 1972 onward.

For **person-level population inference from this 1972 current-release slice**, `WTSSPS` is the producer-authorized default analytical weight.

This does not make `WTSSPS` native to the 1972 field period. It is a later cumulative-file construct whose 1972 applicability is explicit.

### 4.3 Negative design bindings

The following later constructs are not lawful 1972 defaults:

- `WTSS`, `WTSSNR`, `WTSSNRPS`: 2004+ nonresponse/subsampling regime;
- `FORMWT`: form-assignment correction for later named years, not 1972;
- `BALLOTFORMWT` / `BALLOTFORMWTNR`: later ballot/form corrections;
- `OVERSAMP`: 1982/1987 Black oversamples;
- `VPSU` / `VSTRAT`: NORC's public design-variable documentation begins with 1975, and accepted exact-source evidence says they are absent in GSS1972.

The cumulative codebook also states that `SAMPCODE` is blank for all 1972 cases. Appendix A contains a legacy statement about a 1972 "sampling error code"; that historical statement does not authorize synthesizing a current-release `SAMPCODE`, `VPSU`, or `VSTRAT` carrier.

Thus the documentary court closes with a **negative variance-design binding**: the exact public GSS1972 source does not lawfully support a modern `VPSU/VSTRAT` complex-sample variance specification. Any downstream analysis requiring design-corrected sampling variance must fail closed unless a separate producer-authoritative 1972 variance-design carrier/method is supplied.

### 4.4 No phantom block-quota weight

MR056 documents historical attempts to correct block-quota artifacts and the 1960-frame race imbalance. Those historical methods are documentary context, not permission to invent a third weight variable. Accepted exact-source evidence exposes only `wtssall` and `wtssps` as weight candidates. Realization must not synthesize a `BQWT`, race weight, form weight, or other unnamed carrier.

## 5. Identity holding

The GSS cumulative codebook calls `ID` the "Original ID Number." That does not establish cross-release person continuity. Accepted exact-source evidence proves that `id` is injective only within this exact file and restarts in other selected releases.

Lawful hard identity is therefore:

`(canonical_source_sha256, zero_based_source_row_ordinal)`

Native `id` is preserved as a source-local attribute / check only. It may not be used to join respondents across releases.

## 6. Documentary-source hierarchy for realization

For GSS1972:

1. exact canonical source physical facts inherited from accepted source courts;
2. exact official 1972 questionnaire for direct-item wording, occurrences, filters, substitutions, and skips;
3. 1972-explicit entries in the official cumulative codebook / appendices for derived or technical variables and source-year notes;
4. official GSS methodological reports for sampling/weight construction and historical defects;
5. later cumulative conventions only when NORC explicitly states 1972 applicability.

Later conventions without explicit 1972 scope are inadmissible.

## 7. Closure

No named documentary document remains missing for the L2 admission burden. The remaining work is **source-specific realization**: bind released fields to the now-frozen documentary rules without inferring route from missingness and without inventing unavailable design carriers.

Unsupported analysis classes (for example, modern `VPSU/VSTRAT` variance estimation from this exact source alone) are explicit negative admissions, not unresolved unknowns.

Terminal:

`CLOSED35_L2_GSS1972_DOCUMENTARY_ROUTING_WEIGHT_AUTHORITY_CLOSED__READY_FOR_SOURCE_SPECIFIC_REALIZATION`
