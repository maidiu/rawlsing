# Owner limits — certified refusal overlay

## Certified

- 28 selected response fields have exact per-item authority rows with
  `response_semantics_status=certified`.
- Code-99 values in those fields are moved from `SUBSTANTIVE_RESPONSE` to
  `REFUSAL` in the isolated overlay.
- The normal source-configuration schema owner validates the corrected
  configuration.
- Aggregate retained counts conserve 308154 source records; certified refusal
  count is 2185; q101 remains 7129 valid / 204 explicit nonresponse / 4 missing.

## Held

The following 14 fields are explicitly `HELD_UNCERTIFIED` because their
authority rows are `preserved_not_certified`, even where the option fields
describe refusal/special missing:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

They retain their historical `SUBSTANTIVE_RESPONSE` mapping. No speculative
correction was applied.

## Authority join

The overlay uses exact per-item allowlist rows plus exact option-authority rows.
It does not apply a universal code-99 semantic. The 14 held entries are not
promoted.

## Routing

Routing remains unknown for all 42 selected fields; 42 risk-set refs remain
unresolved. No eligibility denominator or policy is inferred.

## Limits

No original source/respondent read, original workload, production/config
adoption, policy, merge or CI. Distinct focused review is required.
