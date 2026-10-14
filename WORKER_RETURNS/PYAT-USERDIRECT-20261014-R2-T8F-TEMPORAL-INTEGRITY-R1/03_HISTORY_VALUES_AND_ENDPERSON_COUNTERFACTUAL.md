# History Values and End-Person Counterfactual

## Numerical wave changes propagate

- Changed 21/220 -> 23/220 delta propagates to consumer `selected_numeric_temporal_value`
- Data-plane read hash changes with numerical change
- Unrelated input (variance) does not change delta

## Historical consumer

`consume()` returns `STANDALONE_HISTORICAL_ASOF_TEST_READER__NOT_REAL_N9` with:
- `values_read_digest` (content-addressed)
- `selected_numeric_temporal_value` (delta)
- `historical_intervening` (UNKNOWN_UNOBSERVED_GAP for 2017)

## End-person counterfactual

No same-person inference. No respondent movement. Independent cross-sections only. No V3 actor.
