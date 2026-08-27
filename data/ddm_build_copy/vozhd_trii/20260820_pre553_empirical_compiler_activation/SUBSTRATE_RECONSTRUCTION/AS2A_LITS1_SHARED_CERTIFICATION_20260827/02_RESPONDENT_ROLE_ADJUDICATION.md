# AS2A LiTS-I Respondent-Role Adjudication

Status: `PART_A_PASS__GSR08R2_LITS1_RESPONDENT_ROLE_BRIDGE_CLOSED_FOR_BOUNDED_RAW_PROVING_RELEASE`

Source: `LiTS_I.dta`  
Source SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Respondent-role bridge identity:  
`urn:rawlsing:pre553:as2a:lits1:respondent-role-bridge:sha256:1d4249a2bdbd373503c68f60b3c83882428ca3c2b3f3e37cb5178ad76e4f0d80`

Respondent-role bridge hash:  
`1d4249a2bdbd373503c68f60b3c83882428ca3c2b3f3e37cb5178ad76e4f0d80`

## Frozen holding

`ONE_PHYSICAL_ROW != ONE_SEMANTIC_RESPONDENT_FOR_EVERY_SLOT`

The questionnaire positively assigns Sections 1–2 to the household head or another knowledgeable household member, Sections 3–7 to the selected respondent with no substitutions, and Section 8 to the interviewer.

For the bounded proving release, one role-scoped selected-respondent identity is bound to each source row:

`selected_respondent_ref = source_sha256 + one_based_row_ordinal + selected_respondent_role`

This is a release-scoped replay/subject identity only. It does not promote native `id`, Table-2 IDs, or Table-3 IDs into durable identity.

Sections 1–2 never inherit that selected-respondent ref as self-report. Household roster/housing material remains exact source-preserved nonparticipating material. The 12-member roster topology remains preserved.

## Bounded proving release

Positive projection is intentionally bounded and exact:

- 65 unconditional selected-respondent Section-3 slots (Q3.01–Q3.14 excluding conditional Q3.15) → `RespondentEvent`;
- `country` and `tablec` → source-scoped `EmpiricalCoordinateFact`;
- `weight_0`, `weight_1`, `weight_2` remain distinct but produce no `WeightMeasureFact` under RAW/unweighted scope;
- every other source slot is explicitly preserved but nonparticipating.

Response binding consumes exact LiTS response-option authority `e696eb5084458cb5424a53f96c9461cdf8ec3da8e5eb47dc0a4458b413a2f867`:
- `certified` value authority may bind authorized canonical semantics;
- `preserved_not_certified` or absent value authority remains raw with `INVALID_UNRESOLVED`;
- physical missingness alone never becomes a semantic response state.

The LiTS-2006 FQRA/QSM authority remains in the closure as a governed input but does not self-assign C11 object-family ownership.

## Ledger legend

- `PROJECT_EVENT`: selected-respondent `RespondentEvent` in bounded proving scope.
- `PROJECT_COORD`: source-scoped `EmpiricalCoordinateFact`.
- `PRESERVE_HH_REPORTER`: household/head-knowledgeable-member material, never selected-respondent self-report.
- `PRESERVE_SELECTED_OUTSIDE_SCOPE`: selected-respondent material retained outside this bounded certification projection.
- `PRESERVE_ID_PROV`: source identity/selection/derived provenance only.
- `PRESERVE_INTERVIEWER`: interviewer-only material.
- `PRESERVE_WEIGHT_RAW`: distinct weight surface preserved, no default/estimand claim.

## Pass

`UNACCOUNTED_LITS1_SOURCE_SLOT = 0`

`UNRESOLVED_RESPONDENT_ROLE_REQUIRED_FOR_PROVING_SCOPE = 0`

`UNRESOLVED_ROUTING_APPLICABILITY_REQUIRED_FOR_PROVING_SCOPE = 0`

The four Authority-82 unknowns remain frozen and nonblocking for this RAW single-release proving scope.
