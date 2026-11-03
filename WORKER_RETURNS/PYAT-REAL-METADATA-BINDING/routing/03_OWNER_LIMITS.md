# Routing/denominator owner limits

## Accepted at this scope

- 42-slot SRC04 slice, 2 coordinate slots, single SAV/source-interview-row.
- `form_id=None`, `repeat_id=None` for that bounded slice only.
- Prior D1 observed-sample tally and focused review are accepted at their
  descriptive grade.
- Source-record/event denominators and response-state categories are available:
  valid answer, explicit nonresponse, missing/unobserved.
- The accepted tally/replay refs and consumer API are preserved.

## Not proven

- No exact questionnaire skip/routing rule is present for any of the 42 selected
  fields.
- No eligibility/risk-set denominator is accepted.
- No routed-out category can be resolved.
- The observed counts must not be used to infer eligibility or routing.
- No R03 GrammarPolicy/authorized direction grant exists.

## First exact missing artifact

- Artifact: exact routing/skip rule and risk-set/eligibility denominator handoff
  for the accepted 42-slot SRC04 slice.
- First question: `q101`.
- Fields: `routing[].typed_state`, `routing[].routing_rule_ref`,
  `routing[].risk_set_ref`, `risk_set_refs`.
- Owner: ARAB lane / P3 integration owner named in the SRC04 exception ledger.

## Consequences

- The normal Pyat metadata consumer can resolve the accepted slice, form/repeat
  null shape and descriptive response categories.
- It cannot distinguish eligible from routed-out, and it cannot produce an
  eligibility-conditioned denominator or R03 policy.
- Any route-conditioned or denominator-conditioned claim remains held until the
  exact rules are supplied. No routing was inferred from observed counts.

## Boundaries

No original source/respondent rows, workload issuance, production edit, policy
fabrication, merge or CI. Distinct nonauthor review is required.
