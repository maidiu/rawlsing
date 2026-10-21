# R30G material scenarios and source faults

Frozen assertion: `r30g.assertion.p01` / `R30G-GM01-C12-A0-A2-P01`.

A positive requires all of the following at the real product:

- A0 `status=OK` and `ARRIVAL` claim;
- GM01 material start `tools_for_a=1`;
- A action admitted, tool consumed;
- A completed units +1, material remaining -1;
- B other units 4 with `OFFSCREEN_NO_CHANGE`;
- the GM01 receipt hash is stored in the material start;
- the corrected C12 verifier is `ok=true`.

| Scenario | GM01 result | A tools | A completed | B units | A2 offscreen | P01 |
|---|---|---|---|---|---|---|
| B share + A E2 | `OPPORTUNITY_CHANGED_BY_INDEPENDENT_B` | 1→0 | 4→5 | 4 | `OFFSCREEN_NO_CHANGE` | **PASS** |
| B refuse + A E2 | `DENY_ACTION_WITHOUT_MATERIAL` | 0→0 | 4 | 4 | `OFFSCREEN_NO_CHANGE` | false |
| B share + A omit | `OPPORTUNITY_CHANGED_BY_INDEPENDENT_B` | 1→1 | 4 | 5 | `OFFSCREEN_REPAIR` | false; separate lawful no-effect |
| B refuse + A omit | `OPPORTUNITY_UNCHANGED` | 0→0 | 4 | 4 | `OFFSCREEN_NO_CHANGE` | false |
| B share + contrary + A omit | `UNCERTAIN_CONTRADICTORY_PROJECTS` | 1→1 | 4 | 5 | `OFFSCREEN_REPAIR` | false; competing preserved |
| forged E2 before E1 | `DENY_E2_NOT_LATER` | 0→0 | 4 | 4 | `OFFSCREEN_NO_CHANGE` | false; denied |
| revoked GM01 source | `DENY_REVOKED` | 0 | 4 | 4 | `OFFSCREEN_NO_CHANGE` | false; denied |

Source cuts and restoration in `tests/test_r30g.py`:

- positive B share/A E2 → refusal → restore share: P01 true → false → true.
- B share/A E2 → A omission: P01 false while the option remains available and B acts.
- forged E2, reversed clock, revocation and contrary project all fail closed without acquiring a trait or target.

The GM01 resource reports `psyche_delta={}`, `v3ms_created=0`, `rule_t_result=NO_CHANGE`, `rule_t_grant=None` in every case.
