# SRC04 certified refusal overlay — 28 entries / 14 held

**Base:** `1110093f324fe591246c56bf8f2e742a57c9201e`
**Review read:** `decline-code-recheck` at `ad205744c` in sibling `pyat-pdev01-gap007-review`
**Mode:** TEST_ONLY sourcefree metadata/aggregate replay; no original respondent read.

## Verdict

**`CERTIFIED_REFUSAL_OVERLAY_VALIDATED__28_CORRECTED__14_HELD__ROUTING_UNKNOWN`**

The q101 correction is preserved and extended by exact per-item certified
allowlist entries. The overlay now corrects **28 certified response fields**;
**14 uncertified fields remain explicitly held**. The correction is not a
universal code-99 rule.

## Overlay

- Certified entries: **28** (q101 + 27 additional)
- Held/uncertified entries: **14**
- Selected fields partitioned: **42**
- Existing source-configuration schema owner: **valid**
- Only certified entries changed: true
- Held entries changed: false
- Production config adopted: false

The overlay is in `02_CERTIFIED_OVERLAY.json`.

## q101 retained check

| q101 | Before | Corrected |
|---|---:|---:|
| Valid answer | 7162 | 7129 |
| Explicit nonresponse | 171 | 204 |
| Missing | 4 | 4 |
| Source records | 7337 | 7337 |

This preserves the accepted q101 correction.

## Conserved aggregate replay

All 42 selected fields retain their source-record denominators. Certified
code-99 counts are moved from substantive to explicit refusal; the 14 held fields
are unchanged.

| Selected 42 | Old | Corrected |
|---|---:|---:|
| Valid answer | 277582 | **275397** |
| Explicit nonresponse | 21237 | **23422** |
| Refusal (certified code-99) | 0 | **2185** |
| Missing/unobserved | 9335 | 9335 |
| Observed response | 298819 | 298819 |
| Source records | 308154 | 308154 |

Identity:

```text
275397 + 23422 + 9335 = 308154
```

The aggregate correction moves exactly **2185** certified code-99 responses from
substantive answer to explicit refusal.

## Held entries — 14

The following fields are explicitly held at `HELD_UNCERTIFIED`, current state
`SUBSTANTIVE_RESPONSE`, because their response-option authority row is
`preserved_not_certified`, even though its code fields describe refusal/special
missing:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

No correction was applied to these fields. Exact code counts and reasons are in
`01_CERTIFIED_RECEIPT.json`.

## Routing

Routing remains unchanged and unknown:

- 42/42 selected routing entries `ROUTING_UNKNOWN`
- 42/42 risk-set refs unresolved
- accepted routing binding: false
- eligibility denominator: false

No routing was inferred from observed counts.

## Tests

`test_certified_fix.py`: **5 passed** in 0.03s.

## Limits

No original SAV/DTA or respondent rows were read. No original workload was
issued. No production/config adoption, routing rule, policy, merge or CI was
created. The replay uses retained aggregate code counts only.

**Distinct focused review is required.**
