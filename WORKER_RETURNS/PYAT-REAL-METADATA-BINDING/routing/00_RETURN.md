# SRC04 routing/denominator metadata trace — focused correction

**Base:** `c8e0215f6f222eb7b09ef0a8d198b23f0780dac2`
**Review:** `bdeace786` in sibling `pyat-pdev01-gap007-review`
**Mode:** TEST_ONLY sourcefree metadata trace; no original respondent read.

## Verdict

**`HOLD_ROUTING_AND_DENOMINATOR_NOT_ACCEPTED`**

The accepted 42-slot SRC04 slice is a single-SAV/source-interview-row shape.
For that bounded slice, `form_id=None` and `repeat_id=None` are the accepted
null shape; no form identifier is fabricated. The first genuinely unresolved
source input is routing/eligibility and the risk-set/denominator handoff.

## Accepted prior slice and tally

Read-only prior artifacts:

- Release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- Slice selection: 42 response slots, 2 coordinate slots
- Tally product: `d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0`
- Tally ref: `87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022`
- Replay ref: `8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f`
- Focused recheck: **PASS**, `D1_OBSERVED_SAMPLE_DESCRIPTIVE_TALLY_ACCEPTED`
- Consumer API: `rawlsing_next.pre553_carrier_execution.materialize_public_object`

## Routing result

- Config routing entries: 178
- Selected 42 routing entries: 42
- Selected `ROUTING_UNKNOWN`: 42
- Selected risk-set refs unresolved: 42
- Exact questionnaire skip rules found: 0
- Accepted routing binding: **false**
- Source-record/event denominator accepted: **true**
- Eligibility/risk-set denominator accepted: **false**
- Routing inferred from observed counts: **false**

The first exact question is `q101`; its unresolved rule and risk-set refs are:

```text
urn:rawlsing:r157:original:SRC04:q101:unresolved
```

The same unresolved state applies to all 42 selected fields.

## Consumer probe

The accepted descriptive tally can distinguish response outcomes for `q101`:

- Valid answer: `7162`
- Explicit nonresponse (DK/source-specific special): `171`
- Missing or unobserved: `4`
- Source-record/event denominator: `7337`
- Eligible: **unknown**
- Routed-out: **unknown**
- Routing rule exact: **false**

It cannot distinguish eligible from routed-out because no exact questionnaire
skip rule or eligibility denominator is present. Observed counts were not used
to infer routing, and no policy was manufactured.

## Response-option authority

The accepted 42-slot slice maps to 367 response-option authority rows (12,160
rows total). Response option classification is available; it does not supply
routing/denominator authority.

## Exact missing artifact

**Artifact:** exact questionnaire routing/skip rule and risk-set/eligibility
denominator for the accepted SRC04 42-slot slice.

**Fields:** `routing[].typed_state`, `routing[].routing_rule_ref`,
`routing[].risk_set_ref`, `risk_set_refs`.

**Owner:** ARAB lane / P3 integration owner named in the SRC04 exception ledger.

**Consequence:** only source-record/event denominators and response-state
categories are available. No eligible denominator, routed-out category,
route-conditioned query or R03 policy can be claimed. The downstream missing
artifact is an exact R03 `GrammarPolicy`/authorized direction grant, owned by
the R03 policy/direction owner.

## Tests

`test_routing.py`: **5 passed** in 0.03s.

## Limits

- No original SAV/DTA or respondent rows were read.
- No original workload was issued.
- No production edit, policy, routing rule, form identifier, merge or CI.
- The accepted D1 tally remains a bounded descriptive product, not an I03
  `EmpiricalFact`.

**Distinct nonauthor review is required.**
