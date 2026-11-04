# Owner dependencies and limits

## Exact routing/eligibility premise — 42 fields

The Wave 1 questionnaire has exact item citations for response semantics, but it
contains no explicit skip, filter, routing, ask-all or go-to instruction. The
existing source configuration therefore remains:

```text
typed_state = ROUTING_UNKNOWN
routing_rule_ref = unresolved
risk_set_ref = unresolved
row_selector = ALL
```

`row_selector=ALL` is not eligibility authority. The config was validated by the
normal schema owner with `valid=true`; it was not changed. Exact supported route
bindings: **0**.

**Owner:** ARAB lane / P3 integration owner named in the SRC04 exception ledger.

**Required artifact:** exact per-item questionnaire skip/routing rule and
risk-set/eligibility denominator handoff. The questionnaire's `if`/`only` phrases
on pages 6, 7, 10, 14, 18, 20, 21 and 7, 11, 18, 24, 28, 29 are substantive
question prose, not routing rules.

## 14 held refusal entries

Exact questionnaire evidence exists for every held field: the item block states
`99 = Decline to Answer`. PDF page and line citations are in
`evidence/RESPONSE_AUTHORITY_14.csv`.

The authority rows still say:

```text
response_semantics_status = preserved_not_certified
is_refusal = True
```

Fields:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

No correction was applied. Exact missing premise: competent item-specific
authority certification of the code-99 semantics; exact source evidence alone
does not change the authority status.

**Owner:** ARAB lane / P3 integration owner; later competent source-semantics
authority. Their eligible/routed-out state remains `UNKNOWN`.

## 28 certified refusal entries

The accepted 28-entry overlay remains preserved. Response evidence in the
original questionnaire is compatible with the existing certified entries; no
new correction or promotion is made here.

## Science and production

- Science: **HOLD**, absent the original execution grant. No empirical claim was
  made from the questionnaire or retained aggregate receipt.
- Authority: **HOLD**, production and issuance not granted. No production config
  was edited or adopted.
- Exact R03 `GrammarPolicy` / authorized direction grant remains absent; owner:
  R03 policy/direction owner.

## Limits

No original source/respondent rows, original workload, universal code rule,
scientific issuance, production/config adoption, policy, merge or CI. The only
reads are questionnaire/codebook metadata and retained aggregate counts.
Distinct focused review is required.
