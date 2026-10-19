# P41 — F8/N9/N10E/N10W status and coverage crosswalk (Atlas AT-linked)

Status vocabulary: `EXECUTED_GREEN` (sourcefree bounded grain), `TYPED_REFUSAL`
(deliberate, correct), `HELD` (authority missing), `NOT_RUN`.

| Element | State | Evidence |
|---|---|---|
| N10E computed slices from exact empirical products | EXECUTED_GREEN | `computed_progressive_conditioning_receipts.json` (routes N10E_PUBLIC_SINGLE / C1_PUBLIC_MULTI_BINDING; cells 32{14,18}→16{6,10}→8{2,6}) |
| N10W progressive conditioning (ordered, multi-conditioner) | EXECUTED_GREEN | E03 chain receipt + per-step F8 consumption (`EXACT_SUPPORTED` ×3); progressive identity changes per depth |
| N9 selected objective world (M4/M5 + catalog rules; clocks) | EXECUTED_GREEN (TEST_ONLY rule world) | `n9_world` blocks; rev2 fee6/exit8 publication-boundary matrix; early as-of selects rev1 |
| Actual original consumer effect (NONPARENT_OPTIONS) | EXECUTED_GREEN | `generic_consumer_values_read.json` with learned-release bindings per step |
| Learned-release read-through channel | EXECUTED_GREEN | same-step fact values with `learned_release_binding`; release severity witness in W3 |
| Actor firewall / sampling-unit firewall | EXECUTED_GREEN | `actor_firewall_receipt.json`; dyad refusal typed; no route probability |
| Current/historical/as-of + selective invalidation | EXECUTED_GREEN | `current_historical_serving_invalidation.json` |
| Cold deterministic replay | EXECUTED_GREEN | two fresh processes identical content hash (`test_p41_cold_replay.py`) |
| N10W global installation claim | NOT CLAIMED | requires N9+N10E positive jointly read and authorized for that consumer purpose |
| Original-source measured estate (F1–F7, 35 waves) | HELD | N03/C11 custodian chain; no current source warrant |
| Proposal/V3 C0 purpose | TYPED_REFUSAL (permitted) | `CONSUMER_PERMISSION_UNISSUED` + versioned contract |
| F6 cross-source transport | HELD | WV1 separation retained; not admitted here |

## Acceptance-case linkage

| AT | Case | Result |
|---|---|---|
| AT07 | bidirectional conditional arithmetic, common risk set | forward 18/32 and reverse A|Y 18/29 computed from the same exact source; unauthorized reverses (B, C) refuse |
| AT08 | attitude/joint conditioning identity | condition change changes query identity hash; three distinct progressive identities |
| AT10 | minority/counterpattern survival | depth-3 minority branch (2 of 8) retained; all cells > 0 preserved; no ranking collapse |
| AT13 | joint morphology/component scope | C1 multi-binding routes retained; no scalarization of heterogeneous authority |
| AT17 | computed possibility slices | provider computes from exact products; caller geometry rejected; no handwritten slice |
| AT18 | replay grade | `DETERMINISTIC_CONTENT_HASH_VERIFIABLE`; cold replay green; no claim beyond grade |
| AT19 | selective invalidation | structural revocation selective; source-permission revocation consumer-vs-producer channels distinct; historical retained |
| AT31 | world dependency closure (bounded) | dependencies list explicit; full cross-owner closure remains W41/A41 |
| AT32 | current and historical serving | as-of matrix + declared-no-current fresh refusal + archival receipt |
| AT33 | progressive possibility | known configuration updates alternatives using governed slices + world context; minority support retained |
| AT34 | sampling-unit firewall | individual possibility lawful; dyad claim refused without linkage authority |
| AT35 | actor wake threshold | correct refusals alone are not a wake; no personhood/route probability emitted; N11/N12 untouched |
