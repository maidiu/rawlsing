# R29P seven same-observable actor/source faults

The frozen observable is `r29p.runner.observable`: one product API call sequence returning A0 claims/others/self-history/tools and A2 clock/offscreen other-actor units. Every fault uses this same function. No constructor exception is counted as a behavioral RED; construction refusals are not used for any of the seven.

Baseline in `evidence/r29p_seven_faults.json`:

```text
status=OK  claims=["ARRIVAL"]  others=["B"]  tools=1
a2_clock=40  a2_other_units=5  a2_offscreen=["MOVE","OFFSCREEN_REPAIR"]
self_history=f5406fb8ba26473d9ea7fd1fa1c9d805e9e76078a89283a2b6d51c81bf43d053
```

| # | Edge cut | Baseline | Actual downstream fault observation | Restore |
|---|---|---|---|---|
| 1 | A genesis/history | OK, history `f5406f…` | OK, history `0a2cf6…`; same A0/A2 product constructs and reads a different A0 self history | OK, baseline history |
| 2 | A performed/omitted action | OK, history `f5406f…` | OK, history `c9b69b…`; A omission removed from source history changes A0 self history | OK, baseline history |
| 3 | B independent performed action | OK, A2 other units 5 | OK, A2 other units 3; B's own state is materially lower | OK, A2 other units 5 |
| 4 | ADP010 encounter/contact | OK, A0 others `["B"]` | OK, A0 others `[]`; B is not co-present, A2 has no MOVE | OK, A0 others `["B"]` |
| 5 | C8/E1 proof | OK, A0 claims `["ARRIVAL"]` | HELD `BP3_PROOF_INVALID`; A0 cannot read the occurrence | OK, A0 claims `["ARRIVAL"]` |
| 6 | CAN008 A / CAN011 T target/grant | OK, tools 1 | HELD `C9_TARGET_PREIMAGE_UNSEALED`; A0 cannot read the practice target | OK, tools 1 |
| 7 | Later independent E2 | OK, tools 1, other 5, `OFFSCREEN_REPAIR` | OK, tools 0, other 4, `OFFSCREEN_NO_CHANGE`; no practice, no independent repair | OK, tools 1, other 5, `OFFSCREEN_REPAIR` |

Every row has `baseline_pass=true`, `fault_changed_or_refused=true`, `restored_pass=true`, `stable_restore=true` and `proves=true` in `evidence/r29p_seven_faults.json`.

## Why these are behavioral, not constructor passes

Faults 1-4 and 7 construct the product and return an A0/A2 observation. The difference is in the observed actor history, A2 other-actor units, A0 participants, A0 tools or A2 offscreen event kind. Faults 5-6 construct the product and return an A0 `HELD` from the real C10 read, not a producer or constructor error. The restore for faults 5-6 is a fresh product over the restored artifacts and returns to the baseline observation.

## Rival interpretation

The same results are compatible with H1 (a bounded sourcefree enacted activity), H2 (B-mediated availability) and H3 (contradictory/omitted action). They are also compatible with H0: the simulator, role fixtures and selected source data can produce the result without any empirical psychological acquisition. R29P does not choose among H1-H3. It proves the software receiver distinguishes the seven source edges; it does not prove human psychogenesis.

The B and encounter cuts are product-world/sourcefree input cuts, not observed human contact. The A/T and C8 cuts use the exact TEST_ONLY owned rules and journal. No native CAN008/CAN011/ADP rule is implied.
