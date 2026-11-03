# Owner limits — q101 code-99 correction

## Repaired

- q101 code 99 is reclassified from `SUBSTANTIVE_RESPONSE` to `REFUSAL` in an
  isolated in-memory configuration overlay.
- Exact response-option authority supports `special`, non-substantive, refusal,
  missing and `special_missing`.
- Corrected aggregate: 7129 valid, 204 explicit nonresponse, 4 missing, 7337
  source records; observed 7333.

## Not changed

- Other 41 selected fields remain at their historical classification.
- No production/config adoption.
- No historical receipt is rewritten.
- No routing, eligibility denominator or policy is inferred.
- No original source/respondent read or original workload.

## Classification owner

No dedicated response-state classifier exists in the current owners for this
metadata overlay. The exact response-option authority fields are used directly:

```text
option_group=special, is_substantive=False, is_refusal=True,
is_missing=True, response_kind=special_missing
```

The source-configuration schema owner validates the overlay; no new policy or
classifier is invented.

## Remaining routing hold

All 42 selected routing entries remain `ROUTING_UNKNOWN`; all 42 risk-set refs
remain unresolved. Affirmative routing evidence is absent. The first routing
question remains `q101` with unresolved rule/risk refs.

## Scope

TEST_ONLY metadata/aggregate evidence. No production edit, CI, merge or adoption.
Distinct focused review is required.
