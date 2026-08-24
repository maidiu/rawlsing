# REC-03 — R10G Normative-Role Source Census

Status: `REC03_COMPLETE_CENSUS__SUCCESSOR_CANDIDATES_IDENTIFIED__SUCCESSORS_NOT_AUTHORED`

Exact launch HEAD: `e410799cc7afa95e758ebe774f141e053e2bb711`

Worker branch: `agent/vozhd-trii-rec03-r10g-normative-role-census`

## Scope

REC-03 enumerates the full current R10G semantic-unit class whose canonical semantic role is
`NORMATIVE_OR_POLICY_STANCE`. It does not reopen unrelated R10G driver/facet/domain/axis/target authority.

The full denominator is **594 unique semantic units**. This is distinct from R02's bounded T06 hostile
ledger; R02 explicitly did not claim a global R10G role census.

## Enumeration proof

The current R10G role count is independently recorded as `NORMATIVE_OR_POLICY_STANCE=594` in the
whole-machine input-contract audit. The exact denominator spine used here is
`T06_NORM_SHORE_ACCOUNTING_R2.csv`, which carries current R10G semantic-unit ids and source memberships.
Its 813 current normative-role source-membership rows collapse to exactly 594 unique semantic units.

## Source-evidence relation

`SOURCE_EVIDENCE_LEDGER.csv` defines the governed evidence relation used for every denominator row.
For each `semantic_unit_id`, exact proposition evidence is the complete set of rows in
`T06_NORM_SHORE_ACCOUNTING_R2.csv` where `sem__audit_unit_id == semantic_unit_id`. Those rows preserve
source family, wave, variable identity, exact question text, current predicate/target, and routing/accounting
context. Exact `(source_family, wave, source_variable_code)` joins to the governed P2 question-node catalog
supply response-authority/question-node binding for **811 / 813** source-membership rows. The two remaining
memberships retain the T06 source proposition and bounded R14 parent/stem evidence where available; no
missing proposition field is invented. R02 hostile rulings are reused only on exact matching units.

## Compact row-code contract

`R10G_NORMATIVE_ROLE_DENOMINATOR.csv` and `ROW_LEVEL_ROLE_CENSUS.csv` use:

- `P` = `PASS__CURRENT_ROLE_SOURCE_SUPPORTED`
- `S` = `SUCCESSOR_CANDIDATE__ROLE_MISCLASSIFIED`
- `L` = `SOURCE_LIMITED__CANNOT_RESOLVE`

`ROW_LEVEL_ROLE_CENSUS.csv` proposition-class codes are:
`NORM_MORAL`, `NORM_OBLIG`, `NORM_POLICY`, `NORM_OTHER`, `P_ACTOR_COMMIT`, `P_CAUSAL`, `P_FREQ`,
`P_EXTENT`, `REALIZED_STATE`, `P_ACCESS`, `DESC_BELIEF`, `AFFECT_CONCERN`, `SALIENCE`, `EVAL`,
`INTENT`, `EXPECT`, `P_POP_ATTR`, `UNRESOLVED`.

Its preservation codes mean:

- `P1`: current normative speech-act role is source-supported; preserve source actor/operator/target/object,
  condition, modality, timeframe/horizon, population/geography, parent/stem context and response topology.
- `S1`: exact actor/target/modality preservation and role-dependent replay requirements are stated in
  `SUCCESSOR_CANDIDATE_LEDGER.csv`; source condition/timeframe/population/geography and unrelated R03
  coordinates remain preserved unless a separate exact defect is proved.
- `L1`: proposition-defining dimensions remain UNKNOWN at the recovered evidence ceiling; do not infer them.

`SOURCE_LIMITED_ROWS.csv` uses:
- `NE1` = exact parent/stem/operator plus response frame/topology required to resolve the speech act.
- `PI1` = no keyword, moral-content, neighboring-wave, label, or convenience inference is permitted.

## Adjudication counts

- `PASS__CURRENT_ROLE_SOURCE_SUPPORTED`: **463**
- `SUCCESSOR_CANDIDATE__ROLE_MISCLASSIFIED`: **59**
- `SOURCE_LIMITED__CANNOT_RESOLVE`: **72**
- total: **594**

Successor candidates identify proposition-class defects only. They do not author a successor and do not
demote current driver/facet/domain/target authority. For every candidate the ledger names the exact
current assertion, exact source proposition, corrected proposition class, actor/target/modality
preservation requirements, and the role-dependent assertions requiring replay.

## Evidence ceiling

When the bounded source evidence does not recover enough proposition-defining parent/stem/operator or
response topology to distinguish a normative stance from an adjacent descriptive/evaluative/epistemic
speech act, the row is `SOURCE_LIMITED__CANNOT_RESOLVE`. REC-03 does not guess from labels, keywords,
neighboring waves, or moral/political content.
