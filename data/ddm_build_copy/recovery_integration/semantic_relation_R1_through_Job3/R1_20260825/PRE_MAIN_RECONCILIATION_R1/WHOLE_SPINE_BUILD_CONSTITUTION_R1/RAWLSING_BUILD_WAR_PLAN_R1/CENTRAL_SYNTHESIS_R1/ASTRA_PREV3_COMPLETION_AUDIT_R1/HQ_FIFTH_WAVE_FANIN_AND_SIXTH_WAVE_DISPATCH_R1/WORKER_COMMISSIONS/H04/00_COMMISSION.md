# H04 — D05 currentness compatibility implementation R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w6-h04-nonevent-currentness-implementation-r1`

Commission/start parent: `f0c463860a23f0d159cb5cc814f4541f998de547`

HQ fifth-wave fan-in authority: `f0adc9db42277669bbd359adb14da795f998135b`

Execute only:

`PREV3_D05_CURRENTNESS_COMPATIBILITY_IMPLEMENTATION_R1_ONLY`

## Mission

Implement the adopted G04 contract:

`PREV3_D05_NON_EVENT_CURRENTNESS_COMPATIBILITY@1.0.0`

Repair the D05 non-event adapter so a CURRENT serving path validates the actual content-addressed D05-specific currentness receipt object required by G04.

The implementation must recompute/validate receipt identity and bind the exact D05 resolution/selection/producer/world/currentness-authority/basis/effective-time tuple. Only exact state `CURRENT` may support CURRENT service. STALE, REFRESH_REQUIRED, INVALID, malformed, mismatched, or ref-only inputs fail closed; historical material remains historical.

## Hard ceiling

Do NOT modify or widen M4 or M5.

Do NOT relabel the D05 receipt as an M5 receipt.

Do NOT mint currentness truth, use wall-clock/latest/default/fuzzy selection, widen producer family, create publication authority, or touch V3/person state/OBL063.

This is implementation/repair only. You may run targeted/regression tests, but you may NOT claim independent qualification of your own repair.

## PASS / blocker law

PASS if the adopted contract is implemented exactly with targeted/regression evidence and the E05 stale-currentness laundering defect is eliminated at the G04 ceiling.

If implementation cannot be completed without violating G04/HQ authority, return the smallest exact blocker.

## Return

Write governed return under:

`.../HQ_FIFTH_WAVE_FANIN_AND_SIXTH_WAVE_DISPATCH_R1/SIXTH_WAVE_WORKER_RETURNS/H04/`

Include canonical `00_RETURN.md`, exact production/test blob identities, targeted stale/mismatch results, and successor gate for separate independent requalification.

Commit and report final branch tip.
