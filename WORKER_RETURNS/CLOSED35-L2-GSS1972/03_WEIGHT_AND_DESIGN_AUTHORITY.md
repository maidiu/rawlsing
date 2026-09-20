# GSS1972 — Weight and Design Authority

Canonical source: `GSS1972.sav`  
SHA-256: `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`

This document binds producer-documented use to the exact weight/design carriers already observed by accepted predecessor courts. It does not re-open source bytes.

## A. Exact current-source carrier set inherited from accepted evidence

Accepted SR09-PRE R05 measured exactly:

- `sample` — source/design coordinate; for GSS1972 it is code 1 on all rows with label `1960 sample frame, block quota`;
- `wtssall` — source-carried weight candidate;
- `wtssps` — source-carried weight candidate;
- no `form`;
- no `ballot`;
- no `VPSU`;
- no `VSTRAT`.

The accepted weight/design burden row names only `wtssall;wtssps` as GSS1972 weight candidates.

## B. Sampling design

Official Appendix A identifies the 1972-1974 GSS design as a multi-stage area-probability sample down to block/segment, followed at block level by quota selection. Quotas were based on sex, age, and employment status. The 1972 questionnaire's doorstep instruction independently requires the interviewer to locate the person needed to fill the quota.

MR056 identifies 1972 as the only GSS using the 1960 NORC sample frame and notes a race-composition artifact in that frame.

Binding:

- `sample=1` is admitted as **design classification**: 1960 frame + block quota.
- It is not an analytical weight.
- 1972 must not inherit the full-probability respondent-selection semantics of later GSS rounds.

## C. `WTSSALL`

Producer authority:

- Appendix A says `WTSSALL` extends the adults-in-household adjustment to years before 2004.
- MR003 explains why early GSS person samples require household-size adjustment and gives 1972 probability-with-quotas individual weights by number of adults.

Classification:

`LATER_CUMULATIVE_HISTORICAL_PERSON_WEIGHT__EXPLICIT_1972_APPLICABILITY`

Lawful use:

- legacy/historical **person-level** weighting of 1972 cases where the analytical purpose is the historical adults-in-household adjustment documented by GSS;
- as the producer-documented input weight for the later `WTSSPS` construction.

Not lawful as:

- an original 1972 fielded weight;
- a household-level default without separately selecting the household estimand/method;
- a complex-design variance carrier;
- a cross-release identity or routing carrier.

## D. `WTSSPS`

Producer authority:

MR137 states that `WTSSPS` is available for 1972 onward. For 1972-1998, its input is `WTSSALL` or a specifically adjusted version in affected years. It is then raked to population controls. MR137 recommends `WTSSPS` as the default for analyses spanning the historical cumulative GSS; current GSS guidance likewise recommends `WTSSPS` for most analyses.

Classification:

`LATER_POSTSTRATIFIED_CUMULATIVE_PERSON_WEIGHT__PRODUCER_DEFAULT_FOR_1972_CURRENT_ANALYSIS`

Lawful use in Rawlsing source-specific realization:

- **default weight for person-level population inference from GSS1972** when the analysis claims representation of the historical GSS target adult population;
- retain exact raw values and producer provenance;
- record that this weight was produced later and back-applied to 1972.

Target-population boundary:

Current GSS documentation describes the historical target as adults 18+ living in U.S. households; in 1972 the survey was English-language only. `WTSSPS` does not authorize inference outside that target.

Not lawful as:

- evidence that the 1972 field operation itself used post-stratification;
- a form/ballot correction specific to 1972 (there was no 1972 form/ballot split);
- a household-level estimand without separate authority;
- a source-routing carrier.

## E. Later or non-1972 constructs — explicit exclusion

| carrier / family | 1972 binding |
|---|---|
| `WTSS` | not a GSS1972 source-carried default; modern two-phase weight regime is later |
| `WTSSNR` | not available before 2004 |
| `WTSSNRPS` | not available before 2004 |
| `FORMWT` | not a 1972 weight; correction applies to later named form years |
| `BALLOTFORMWT` / `BALLOTFORMWTNR` | not 1972; later ballot/form assignment corrections |
| `OVERSAMP` | not 1972; documented for 1982/1987 Black oversamples |
| `VPSU` / `VSTRAT` | not present in accepted GSS1972 source; public GSS design-variable document begins at 1975 |
| `SAMPCODE` | cumulative codebook says blank for all 1972 cases; not admitted as an executable 1972 variance carrier |
| unnamed BQ/race correction weight | forbidden unless an exact current-source carrier and producer binding are separately proven |

## F. Design-corrected variance

This is the hard negative boundary.

The public 2013 GSS design-variable document provides `VSTRAT` and `VPSU` for 1975-2012, not 1972. Accepted exact-source evidence independently says GSS1972 contains neither variable.

The 1972 block-quota section of Appendix A contains a historical statement that a "sampling error code" was included, while the cumulative codebook's `SAMPCODE` entry says `SAMPCODE` is blank for all 1972 cases because 1972 did not use the later 1970/1980/1990/2000/2010 frames. This is not a license to manufacture a variance coordinate.

Therefore:

`GSS1972_PUBLIC_SOURCE_DESIGN_VARIANCE_BINDING = NONE_AUTHORIZED`

A source-specific implementation may:

- use `WTSSPS` for producer-authorized person-level point estimation/generalization;
- retain `sample` as a design-classification fact;
- preserve any exact physical technical fields that exist.

It may **not** claim design-corrected standard errors by pretending that modern `VPSU/VSTRAT` apply to 1972.

If variance estimation beyond naive/non-design descriptive calculation is required, the analytical path must fail closed until separate producer-authoritative 1972 variance information/method is supplied.

## G. Historical BQ corrections are context, not phantom carriers

MR056 reports corrections developed from 1975/76 BQ-vs-full-probability comparisons and says 1972's 1960 frame overrepresented Black respondents, with historical weighting to CPS race figures. Those facts explain why early GSS estimates are methodologically special.

They do **not** expand the exact accepted source carrier set. The current canonical GSS1972 year-slice has only `wtssall` and `wtssps` as accepted weight candidates. Rawlsing must not synthesize a third "BQ weight," "race weight," or equivalent carrier from prose.

## H. Analytical binding table

| analytical use | admitted binding | status |
|---|---|---|
| exact source replay / semantic certification | no analytical weight required; preserve all carriers | ADMITTED |
| raw within-source descriptive counts with no population claim | unweighted allowed if explicitly marked non-generalizing | ADMITTED |
| person-level historical U.S.-adult population estimate under current GSS guidance | `WTSSPS` | ADMITTED_DEFAULT |
| legacy comparison reproducing historical adults-in-household weighting | `WTSSALL` with method provenance | ADMITTED_NONDEFAULT |
| household-level population estimate | no implicit default from this packet | FAIL_CLOSED_PENDING_SEPARATE_ESTIMAND_BINDING |
| modern complex-sample SE using `VPSU/VSTRAT` | none for GSS1972 | FORBIDDEN_FROM_THIS_SOURCE |
| form/ballot-specific weighting | none | NOT_APPLICABLE_1972 |
| 2004+ nonresponse-adjusted weighting | none | NOT_APPLICABLE_1972 |

This closes the L2 weight/design authority burden without pretending that every modern GSS inferential facility exists for 1972.
