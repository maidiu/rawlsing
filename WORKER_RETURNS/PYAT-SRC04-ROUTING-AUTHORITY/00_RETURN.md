# SRC04 routing/eligibility authority — 42 fields

**Base:** `ddc85dd298d36d4825d42cd4931a0cac5d91cb73`
**Branch:** `agent/pyat-pdev01-gap007-sourcefree-r1`
**Mode:** TEST_ONLY sourcefree metadata/authority trace; no respondent read.

## Verdict

**`HOLD_ROUTING_ELIGIBILITY_AND_14_HELD__28_CERTIFIED_PRESERVED`**

No exact item-specific routing/skip rule or eligible denominator is evidenced for
the accepted 42 SRC04 fields. Routing remains `ROUTING_UNKNOWN`; no `row_selector=ALL`
placeholder was promoted into eligibility authority.

## Accepted overlay preserved

The accepted certified-refusal overlay remains intact:

- 28 certified refusal entries
- 14 held/uncertified entries
- Aggregate retained replay:
  - valid `275397`
  - explicit nonresponse `23422`
  - refusal `2185`
  - missing `9335`
  - source records `308154`
  - observed `298819`
- q101: `7129` valid, `204` explicit nonresponse, `4` missing, `7337` total.

## Routing interface trace

Existing source-configuration interface:

```text
source_configuration.data.SRC04.source.config.json:routing[]
fields: typed_state, routing_rule_ref, risk_set_ref, row_selector
```

For all 42 selected fields:

- exact routing bindings: **0**
- typed-unknown/held routing: **42**
- exact eligibility denominators: **0**
- unresolved eligibility denominators: **42**
- `eligible`: `UNKNOWN`
- `routed_out`/ineligible: `UNKNOWN`
- ineligible inferred from observed counts: **false**

Every selected routing entry has `ROUTING_UNKNOWN`; the rule and risk-set refs
are unresolved. The first field is q101:

```text
urn:rawlsing:r157:original:SRC04:q101:unresolved
```

## Codebook/source authority check

- Codebook: 181 rows, SHA `8ad1af17b782d1ff3beb84c2d2331977195ac3bb48dbcc94a94a08ca725b288f`
- Source exception ledger: 6 entries
- Relevant unresolved source fields:
  - `routing.typed_state` — `UNKNOWN`
  - `supported_scope.supported_form_slice` — `UNKNOWN`
- Codebook term scan found one substantive phrase, `q221: "unconditional"`; this is question text, not a routing rule. No `skip`, `filter`, `ask all`, `routing`, or eligibility rule was found.

**Missing premise:** exact item-specific questionnaire skip/routing rule and
risk-set/eligibility denominator.

**Owner:** ARAB lane / P3 integration owner named in the SRC04 exception ledger.

## Remaining 14 held entries

The 14 uncertified refusal entries remain held because the exact option-authority
row is `preserved_not_certified`; no competent item-specific certification exists:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

For each, the exact missing premise is item-specific competent response-semantics
certification; `routed_out` and eligibility remain `UNKNOWN`. No speculative
certification or correction was applied.

Downstream unresolved owner: R03 `GrammarPolicy` / authorized direction grant.

## Distinct states preserved

- `EXPLICIT_NONRESPONSE` is retained separately from substantive answers.
- `UNKNOWN_ROUTED_OUT_OR_INELIGIBLE` is not populated from counts.
- No route probability, selection weight or population claim is created.

## Tests

`test_routing_authority.py`: **5 passed** in 0.03s.

## Limits

No original SAV/DTA or respondent rows were read. No original workload, scientific
issuance, production/config adoption, policy, merge or CI was created. The
aggregate replay uses retained counts only.

**Distinct focused review and owner action on the named dependencies are required.**
