# PYAT R3 S04 -- Temporal and Historical Sociological Conditioning Return

**Commission:** PYAT-R3-S04-F7-TEMPORAL-SOCIOLOGY-R1
**Branch:** `agent/rabochii-pyat-r3-s04-f7-temporal-sociology-r1`
**Implementation base:** `7f29aec36d24f16da52d84f17c00f08db3a55434`
**Astra R3:** `88d3c40def26d34ff202258171c256dfa9d17dbb`

## What was built

`rawlsing_next/s04_temporal_policy.py` -- bounded temporal policy module with two interchangeable methods:

1. **linear_interpolation** (inherited V553): `left + ((right - left) * fraction)`, gap-insensitive, no drift uncertainty.
2. **nearest_anchor_backoff** (improved): nearest qualified anchor with explicit drift uncertainty (`gap_years * 0.05`), break-aware, gap/horizon limited.

Both are pure functions. No side effects. No invented survey waves.

## Method comparison

| Property | Linear interpolation (V553) | Nearest-anchor backoff (S04) |
|---|---|---|
| Gap sensitivity | None | `max_gap_years` refusal |
| Break awareness | None | Polarity change / 3x jump detected |
| Drift uncertainty | Absent | `gap_years * 0.05` disclosed |
| Horizon limit | None | `max_horizon_years` refusal |
| Population filter | Implicit | Explicit match required |
| Evidence mode | Always `INFERRED` | `MEASURED` or `INFERRED` |

**Selection:** `nearest_anchor_backoff` is the recommended default. Linear interpolation remains available for comparison and backward compatibility. One stronger method (e.g., weighted local regression) is not justified without observed empirical deficiency in held-out waves.

## Required positive tests (all pass)

- Changed qualified anchor affects the appropriate historical distribution: `test_changed_qualified_anchor_affects_result`
- Changed irrelevant anchor does not: `test_changed_irrelevant_anchor_no_effect`
- Break-aware fallback: `test_break_aware_fallback`
- Excessive gaps: `test_excessive_gap_refusal`
- Unsupported extrapolation: `test_unsupported_extrapolation_horizon`
- Wrong population: `test_wrong_population_refusal`
- Polarity changes: `test_polarity_change_detected`
- Missing anchors: `test_missing_anchors`
- Replay determinism: `test_replay_deterministic`
- Uncertainty distinction (measured vs inferred): `test_uncertainty_distinction`
- Unqualified anchors ignored: `test_unqualified_anchor_ignored`
- Provenance recorded: `test_provenance_recorded`

## Separation of concerns preserved

- Observed repeated-wave distributions: `OBSERVED` decision with `MEASURED` evidence mode
- Modeled historical change: `INTERPOLATED` / `NEAREST_BACKOFF` with `INFERRED` evidence mode
- Historical priors: `PRIOR_BROAD` decision (explicit `allow_prior` flag)
- Structural interpretation: out of scope for this module; not conflated with temporal values

## Test evidence

`python3 -m pytest rawlsing_next/tests/test_s04_temporal_policy.py -v` -- exit 0, 17/17 pass

## Not done (HOLD)

- Real-source F7 qualification: requires exact source/design/operation authority
- Held-out wave validation: requires empirical comparison permission
- Ghana democracy comparison: optional candidate, not a prerequisite
- V3 execution: not run; not imported

## Terminal

`PYAT_R3_S04_F7_TEMPORAL_POLICY_IMPLEMENTED_LOCAL_TESTS_PASS__AWAITING_SOURCE_QUALIFIED_REVIEW__NO_V3`
