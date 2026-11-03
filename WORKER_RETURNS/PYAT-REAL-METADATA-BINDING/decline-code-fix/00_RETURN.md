# SRC04 q101 code-99 Decline to Answer correction

**Base:** `a108e7dc7232b1f3487e71d4607f3e6ca3e9ebdf`
**Review read:** `routing-recheck/00_RETURN.md` at `9d3d42984`
**Mode:** TEST_ONLY sourcefree aggregate correction; no original respondent read.

## Verdict

**`Q101_CODE99_CORRECTED_AGGREGATE_REPLAY__ROUTING_HOLD`**

The accepted q101 tally is corrected only at the response-state mapping for
code 99. The exact response-option authority says code 99 is `special`,
`is_substantive=False`, `is_refusal=True`, `is_missing=True`, and
`response_kind=special_missing`.

## Old failure vs corrected aggregate

| q101 classification | Old accepted tally | Corrected |
|---|---:|---:|
| Valid answer | 7162 | **7129** |
| Explicit nonresponse | 171 | **204** |
| DK | 171 | 171 |
| Refusal | 0 | **33** |
| Missing/unobserved | 4 | 4 |
| Observed response | 7333 | 7333 |
| Source-record denominator | 7337 | 7337 |
| Identity | 7162+171+4=7337 | **7129+204+4=7337** |

The 33 code-99 responses were previously counted as `SUBSTANTIVE_RESPONSE`; they
are now classified as refusal/special-missing. The old classification failure is
preserved explicitly in the correction receipt.

## Isolated overlay

`02_Q101_CODE99_OVERLAY.json` contains only:

- question: `q101`
- native value: `99`
- from `SUBSTANTIVE_RESPONSE` / canonical `"99"`
- to `REFUSAL` / canonical `null`
- exact option-authority fields
- `production_config_adopted=false`

The corrected configuration was validated with the existing source-configuration
schema owner. It changes only this q101 value classification; the original
configuration and prior accepted receipts remain untouched.

## Same mapping defect in selected metadata

The original selected metadata maps code 99 to `SUBSTANTIVE_RESPONSE` in **all
42** selected response fields. Exact question IDs are recorded in
`01_CORRECTION_RECEIPT.json`.

Only q101 is corrected in this isolated overlay. The other 41 selected fields are
reported as `remaining_uncorrected=41`; no speculative change was made to them.

## Historical supersession

The accepted D1 tally remains historically preserved. It is superseded **only at
q101** by this correction; all other fields and prior receipts remain unchanged.
The supersession record is `03_SUPERSESSION.md`.

## Routing

Routing remains `ROUTING_UNKNOWN` for all 42 selected fields:

- 42 routing entries unknown
- 42 risk-set refs unresolved
- accepted routing binding: false
- eligibility denominator: false
- affirmative routing evidence: false

No routing was inferred from counts or the q101 correction.

## Tests

`test_decline_fix.py`: **5 passed** in 0.04s.

## Limits

No original SAV/DTA or respondent rows were read. No original workload was
issued. No production/config adoption, routing rule, policy, merge or CI was
created. The aggregate replay uses retained code counts, not source rows.

**Distinct focused review is required.**
