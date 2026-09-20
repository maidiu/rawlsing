# CLOSED35-R1-GSS1972 — Qualification Test Protocol

Status:

`AUTHORED__NOT_EXECUTED`

This protocol defines the hostile source-specific semantic court that A/B/C must later pass.

It intentionally uses synthetic/frozen semantic fixtures and accepted physical facts. This worker did not open or execute `GSS1972.sav`.

## 1. Qualification order

For each candidate:

```text
canonical source identity
-> exact reader/config binding
-> applicable physical edge receipt [EC01, EC07, EC10, EC12]
-> GSS1972 realization-contract identity
-> route/occurrence projection tests
-> weight/design projection tests
-> negative-admission tests
-> candidate-neutral semantic digest comparison
```

A semantic pass cannot repair a failed physical receipt.

A physical pass cannot repair a semantic divergence.

## 2. T01 — Missingness cannot create routing

Fixture:

- target field physical state = SYSTEM_MISSING;
- documentary route prerequisites = respondent eligible.

Expected:

- eligibility = `ELIGIBLE_DOCUMENTED`;
- response may be missing/nonresponse;
- applicability must not become skipped/not asked.

Fail if:

`SYSTEM_MISSING -> NOT_ASKED`

without independent route authority.

## 3. T02 — Missingness cannot prove spouse absence

Fixture:

- spouse-target field missing;
- marital prerequisite is unavailable or unresolved.

Expected:

- do not infer nonmarriage;
- route state = `ROUTE_EVALUATION_UNRESOLVED` unless exact prerequisite authority resolves it.

Fail if missing spouse field is used as proof that the respondent is unmarried.

## 4. T03 — Documentary skip outranks missingness inference, not raw storage

Fixture:

- documented route says target is skipped;
- physical target cell is missing.

Expected:

- semantic applicability = `FILTERED_SKIPPED_DOCUMENTED`;
- raw physical missing state remains preserved independently.

The route comes from the questionnaire, not the missing cell.

## 5. T04 — Observed value cannot erase documentary contradiction

Fixture:

- documented route says target ineligible;
- target raw storage value is observed.

Expected:

- raw observed value preserved;
- documentary route preserved;
- audit state = `ROUTING_PHYSICAL_CONTRADICTION__RAW_PRESERVED`.

Fail if candidate deletes the raw value or silently marks the respondent eligible from observed incidence alone.

## 6. T05 — Q25 explicit not-asked state

Fixture:

- Q25 contains the instrument-defined `Not asked, inappropriate` response.

Expected:

`NOT_ASKED_DOCUMENTED:INAPPROPRIATE`

separate from physical null/missing vocabulary.

Fail if normalized to generic missing.

## 7. T06 — Q91 occurrence topology

Fixture has four role slots:

- respondent;
- father_or_substitute;
- mother_or_substitute;
- spouse_if_currently_married.

Expected:

four role-distinct occurrence identities.

Fail if:

- flattened into one anonymous repeated list;
- father/mother merged;
- spouse slot treated as universally applicable;
- parent route inferred from nonresponse instead of Q3.

## 8. T07 — Q17/Q18 target-person preservation

Two synthetic route cases:

A. respondent currently working → target role `respondent`.

B. married nonworking respondent with working spouse under the documented branch → target role `spouse`.

Expected:

same question family, different governed target-person occurrence.

Fail if target role is discarded.

## 9. T08 — Q19 aggregate topology

Fixture:

`Q19A = 1 person`.

Expected:

- Q19B-E/Q20 suppressed by documentary route;
- no repeated-person objects generated.

Fail if household count fields are converted to anonymous person occurrences.

## 10. T09 — Q51-Q81 omnibus exclusion

Fixture references a paper-instrument occurrence within Q51-Q81 without an independent retained-source/codebook admission.

Expected:

`EXCLUDED_NON_GSS_INSTRUMENT_BLOCK`.

Fail if realized merely because it exists in the omnibus questionnaire.

## 11. T10 — Later form/ballot assumptions rejected

Request:

- form assignment for 1972;
- ballot assignment for 1972.

Expected:

`NOT_APPLICABLE_1972`

for both.

Fail if:

- UNKNOWN;
- null-as-missing;
- later GSS form/ballot code synthesized.

## 12. T11 — Cross-release native identity rejected

Fixture:

two rows from different GSS releases share the same native `id`.

Expected:

no person join.

Each remains keyed by its own source SHA + row ordinal.

Fail if native `id` creates cross-release continuity.

## 13. T12 — WTSSPS / WTSSALL distinction

Case A:

declared intent = person-level population inference under current GSS 1972 guidance.

Expected selector:

`WTSSPS`.

Case B:

declared intent = explicit legacy adults-in-household weighting reproduction.

Expected selector:

`WTSSALL`.

Case C:

declared intent = raw descriptive counts with no population generalization.

Expected selector:

`NONE`.

Fail if one physical carrier is deleted, aliased to the other, or silently selected without analytical intent.

## 14. T13 — No modern variance pair fabricated

Request:

`MODERN_DESIGN_CORRECTED_VARIANCE`

Expected:

`UNSUPPORTED__NO_AUTHORIZED_1972_VARIANCE_PAIR`

with:

- no VPSU;
- no VSTRAT;
- no synthesized SAMPCODE;
- no phantom block-quota PSU/stratum pair.

This result must not be represented as UNKNOWN because the L2 documentary court issued a negative admission.

## 15. T14 — Later weight regimes rejected

Requests for:

- FORMWT;
- BALLOTFORMWT;
- BALLOTFORMWTNR;
- WTSSNR;
- WTSSNRPS;
- OVERSAMP.

Expected:

`NOT_APPLICABLE_1972` or the exact frozen negative state from the realization map.

Fail on fallback to a same-name later GSS convention.

## 16. T15 — Candidate-neutral semantic convergence

Provide A/B/C with:

- identical canonical source identity;
- physically equivalent EC01/07/10/12 evidence;
- identical GSS1972 authority pack;
- identical declared analytical intent.

Expected:

identical governed semantic projection.

Candidate IDs, cache layout, streaming strategy, or internal data structures must not enter the semantic preimage.

Fail if any candidate produces a different:

- route;
- occurrence role;
- weight selector;
- support/rejection state;
- respondent identity.

## 17. T16 — Physical survival remains prerequisite

A candidate supplies semantically correct route outputs but:

- drops WTSSALL;
- changes replay identity;
- drops routing-carrier evidence;
- or fails its R35 physical receipt.

Expected:

qualification failure.

Semantic agreement is insufficient to erase physical divergence.

## 18. Required qualification evidence

Later A/B/C court must record:

- canonical source SHA;
- reader/config identity;
- R35 physical-equivalence receipt;
- derivative parentage receipt where non-direct;
- GSS1972 realization-contract identity;
- candidate semantic projection identity;
- each T01-T16 verdict;
- explicit unsupported/not-applicable states without coercion to UNKNOWN.

## 19. Current execution boundary

This protocol is authored only.

No canonical GSS1972 source was opened.

No source processing was executed.

No A/B/C test run was performed.

No measured P2X was run.
