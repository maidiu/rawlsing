# R27P seven actor-source fault trials

All baseline/restored roots are fresh; the same `stable_actor_binding.assert_stable` is used. Receipt: `evidence/seven_faults_receipt.json`.

| Edge | Baseline | RED | Restored | Same A0/A2 assertion? |
|---|---|---|---|---|
| `ACTOR_SOURCE_GENESIS` | PASS | `BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8` | PASS | No — product construction |
| `A_OWN_OMISSION` | PASS | `R27P_TARGET_NOT_BOUND_TO_ACTOR_HISTORY` | PASS | **Yes** |
| `B_INDEPENDENT_ACT` | PASS | `R27P_TARGET_NOT_BOUND_TO_ACTOR_HISTORY` | PASS | **Yes** |
| `ADP010_ENCOUNTER` | PASS | `MATERIAL_PAYMENT_OUTSIDE_SOURCE_SCHEDULE` | PASS | No — source refusal |
| `E1_C8_PROOF` | PASS | `AnchorUnavailable:ANCHOR_WATERMARK_MAC_INVALID` | PASS | No — construction |
| `A_T_TARGET_GRANT` | PASS | `BP2_RULE_T_AUTHORIZATION_ABSENT` | PASS | No — construction |
| `INDEPENDENT_E2` | PASS | `R27P_PRACTICE_TOOL_MISSING` | PASS | **Yes** |

Thus `all_proved=true` under the trial harness, but **only 3/7** meet the strict same-final-A0/A2 assertion requirement. This is the primary engineering REVISE gap.
