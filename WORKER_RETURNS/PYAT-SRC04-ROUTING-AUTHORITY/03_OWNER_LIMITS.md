# Owner dependencies and limits

## Exact unresolved routing/eligibility premise

For all 42 selected SRC04 fields, the existing configuration interface has:

```text
typed_state = ROUTING_UNKNOWN
routing_rule_ref = unresolved
risk_set_ref = unresolved
row_selector = ALL
```

`row_selector=ALL` is not treated as eligibility authority. No exact item-specific
skip/routing rule or eligible denominator exists in the examined source config,
codebook or exception ledger.

**Owner:** ARAB lane / P3 integration owner named in the SRC04 exception ledger.

**Required artifact:** exact per-item questionnaire skip/routing rule plus the
risk-set/eligibility denominator handoff. No observed counts may be used to infer
it.

## 14 held refusal entries

The following remain `HELD_UNCERTIFIED`:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

Exact missing premise: item-specific competent response-semantics certification
for the code-99 option row; the current exact option authority is
`preserved_not_certified`.

**Owner:** ARAB lane / P3 integration owner; later competent source-semantics
authority.

Their `eligible`/`routed_out` state remains `UNKNOWN`.

## 28 certified refusal entries

The accepted certified overlay remains preserved. This authorization does not
convert refusal certification into route or eligibility certification.

## Downstream

Exact R03 `GrammarPolicy`/authorized direction grant remains absent; owner: R03
policy/direction owner.

## Limits

No original source/respondent rows, original workload, scientific issuance,
production/config adoption, universal code assumption, policy, merge or CI.
Distinct focused review is required.
