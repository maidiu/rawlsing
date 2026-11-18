# ANVIL R2 — aligned phase audit

All numbers are derived from frozen `R2_PILOT/baseline.json`, `prepared.json`,
and `FIRST_PAIR_RESULT.json` at 495796e5. No measurement rerun.

| Phase | Baseline | Prepared as-run | Prepared aligned positive |
|---|---:|---:|---:|
| Wall | 80.6244 s | 78.0472 s | **63.2445 s** = total - negative 14.8027 |
| S = index build | 14.3780 s | 5.4978 s total | **2.7261 s** = total - negative 2.7718 |
| Q = native evaluator/fact | 65.4039 s | 72.1034 s total | **60.1765 s** measured ops |
| O = export serialization | 0.0191 s | 0.0173 s | 0.0173 s |
| H = admission (outside wall) | 0.2726 s | 0.2874 s | 0.2874 s |

Derived exploratory alignments:

- wall saving: baseline 80.6244 - prepared positive 63.2445 = **17.3799 s**
- S saving: 14.3780 - 2.7261 = **11.6519 s**
- Q saving: 65.4039 - 60.1765 = **5.2274 s**
- prepared positive wall model: S 2.7261 + Q 60.1765 + O 0.0173 + overhead 0.3247 = 63.2445 s
- Q share of prepared positive wall: **95.15%**
- S share of prepared positive wall: **4.31%**

`H` is measured before the wall starts, so it is not added to wall. `S` is
outside the Q timer: baseline `DirectEstateI03Session.__enter__` builds before
`execute_empirical_query`; the prepared context builds before the five timed
operations. `Q` includes native fact construction/hash. `O` is post-call
serialization and is not added to Q. There is no Q/S/O double count in the
positive phase.

The headline `prepared 78.05 vs baseline 80.62` compares different work:
prepared 78.05 includes the negative/restore phase 14.8027. The aligned
exploratory positive wall is 63.2445 vs 80.6244. This is a one-pair sourcefree
mechanics observation, not a qualified speedup.

Unavailable aligned fields:

- CPU: negative phase has no separate CPU fields; use aggregate only, not a
  matched positive comparison.
- Process-tree RSS: prepared aggregate includes negative/restore; no aligned
  positive RSS.
- Row-group reads: prepared aggregate includes negative/restore; no aligned
  positive reads.
- Peak staging: only `scratch_peak_component_bytes` 23,269,376 B is available;
  external supervision sampled 30,368,896 B; no separate staging peak.
- Process-tree peak is 0.25 s sampled plus `ru_maxrss`, not continuous.

Geometry and payload claims are exact:

- 16 respondents, 600 native question bindings, 8,622 RespondentEvent,
  9,600 RoutingEligibilityFact, 16 weights, 7,099,520 retained bytes.
- Added 595 slots / 9,520 cells: 7,616 valid (80%), 952 MISSING (10%),
  952 NOT_ASKED (10%); 8,568 added events, 54 base, 8,622 total.
- Five distinct operations target base A/B/C/MR roles; 600 added slots are not
  600 queried operations and are not a dense all-600 result.
- Full semantic/identity/refs/member/replay parity is true for all five.
- Old ref-only 1,885-byte smoke was correctly superseded by full semantic
  35,256 B (selected) / 148,727 B across five, identity and member refs
  separately; O is not Q.
