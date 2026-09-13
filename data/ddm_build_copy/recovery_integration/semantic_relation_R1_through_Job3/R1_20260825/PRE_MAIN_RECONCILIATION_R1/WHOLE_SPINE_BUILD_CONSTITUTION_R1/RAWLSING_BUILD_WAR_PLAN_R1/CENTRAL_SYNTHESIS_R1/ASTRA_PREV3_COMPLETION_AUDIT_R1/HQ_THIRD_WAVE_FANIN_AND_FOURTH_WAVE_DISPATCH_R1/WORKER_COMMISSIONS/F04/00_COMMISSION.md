# W4-F04 Commission — PREV3_NON_EVENT_ADAPTER_CURRENTNESS_RECEIPT_VALIDATION_REPAIR_R1_ONLY

Repository: `maidiu/rawlsing`
Branch: `agent/rabochii-prev3-w4-f04-nonevent-currentness-repair-r1`
Parent E05 return: `a00d9e71c1317163071f1d086f498d492589e078`
HQ fan-in authority: `3781860269c20006d82f9bec40df3a24b90861a0`

Execute only:
`PREV3_NON_EVENT_ADAPTER_CURRENTNESS_RECEIPT_VALIDATION_REPAIR_R1_ONLY`

Exact blocker to repair:
`E05_D05_STALE_CURRENTNESS_RECEIPT_REF_LAUNDERING`

Mission:
Repair the D05 non-event adapter so CURRENT serving cannot be authorized by mere non-null exact-ref presence. Bind and validate the referenced currentness receipt against the accepted M5 currentness contract: exact schema/type/content identity, correct resolution/object binding, authority/basis/effective-time compatibility, and `state == CURRENT`. STALE, REFRESH_REQUIRED, INVALID, unrelated, mismatched, malformed or unresolvable currentness must fail closed.

Preserve all D05 positive laws: lawful K1/K2/K4 objective non-event serving, objective actor indexing, producer identity, permission narrowing, K3/event/history rejection, person firewall, no fuzzy/latest/default repair.

Do not change world-root authority, M5 semantics, producer family, allowed use ceiling or PRE-V3/V3 boundary.
Do not claim independent qualification.

Run the inherited D05 tests plus targeted currentness hostile controls and relevant regressions. Freeze exact implementation/test identities.

Authorized write scope: smallest D05 adapter/tests needed for this blocker plus:
`.../HQ_THIRD_WAVE_FANIN_AND_FOURTH_WAVE_DISPATCH_R1/FOURTH_WAVE_WORKER_RETURNS/F04/`

Expected return:
- `00_RETURN.md`
- `01_CURRENTNESS_VALIDATION_REPAIR_RECEIPT.json`
- `02_TARGETED_STALE_MISMATCH_HOSTILE_RESULTS.json`
- exact production/test identities.

Library: `NO`.

PASS: exact blocker is repaired with local/current regressions green, or a smaller incompatible M5 contract blocker is proved. Independent qualification remains downstream.

Successor gate: `GATE-NON-EVENT-REQUALIFICATION`.