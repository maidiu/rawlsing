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

## Source evidence

`SOURCE_EVIDENCE_LEDGER.csv` preserves the exact source-reference set for every denominator unit.

- 811 / 813 source-membership rows join exactly to the governed P2 question-node catalog.
- 2 / 813 retain exact current source membership but did not recover an exact P2 join; no source fields were invented.
- R02's exact source-backed RR_NORM hostile rulings are reused only where they match the exact semantic unit.
- No classification is based on moral/political keywords alone.

Proposition class codes in `ROW_LEVEL_ROLE_CENSUS.csv`:
`NORM_MORAL`, `NORM_OBLIG`, `NORM_POLICY`, `NORM_OTHER`, `P_ACTOR_COMMIT`, `P_CAUSAL`, `P_FREQ`, `P_STATE`, `P_ACCESS`, `DESC_BELIEF`, `AFFECT_CONCERN`, `SALIENCE`, `EVAL`, `INTENT`, `EXPECT`, `P_POP_ATTR`, `OTHER_NONNORM`, `UNRESOLVED`.

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