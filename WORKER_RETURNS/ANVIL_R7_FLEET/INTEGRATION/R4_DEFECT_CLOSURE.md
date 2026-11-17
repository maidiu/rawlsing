# R4 ONE-DEFECT CLOSURE — state/claim binding

**Target:** R3 `9fe1fd3842ee1c1c76da0188150467e4799079cc`; R3 recheck `0d87a5643d0bb515dad5c7431ab5b581ffb2ce0c`. **Status:** `PENDING_SAME_C_RECHECK`. Not self-accepted; no reviewer launch.

## Repair

The existing typed/narrative binding now includes readiness-bearing state fields:

- Identity narrative hash covers `disposition`, `status_assertion`, `evidence_grade` as well as source meaning/negative/effect/consumer/witness. A held/future identity cannot become `PRESENT_PRESERVED` without a changed authorized state binding.
- Requirement-disposition hash covers `disposition`; `FUTURE_NONPRECLUDED` cannot silently become `PRESENT_PRESERVED`.
- Boundary narrative hash covers `claim_grade`, `grade`, `actual_first_reader_verified`; `ACTUAL_PROVED` additionally requires an authorized reader witness (`reader_abi`, exit 0, trusted custody). No trusted custody is currently authorized, so `ACTUAL_PROVED` refuses.
- No target blacklist: the same rule applies to P4R-R01/R02, all requirements, and T4/T6/T7.

## Actual witness (inside lease: `R4_WITNESS/`)

| Case | Result |
|---|---|
| P4R-R01 `EXACT_OWNER_HOLD`→`PRESENT_PRESERVED` | DECISION RED, C RED |
| REQ-FIELD-FORGE `FUTURE_NONPRECLUDED`→`PRESENT_PRESERVED` | DECISION RED, C RED |
| T4 `SOURCE_STATIC_CONSERVED`→`ACTUAL_PROVED`, flag true | C RED (`ACTUAL_PROVED_WITHOUT_AUTHORIZED_READER_WITNESS`, narrative mismatch) |
| Analog P4R-R02 promotion | DECISION RED, C RED |
| Analog REQ-SEAM-WORLD-ACTOR promotion | DECISION RED, C RED |
| Analog T6 actual-proof promotion | C RED |
| Exact baseline restore | FRAME/DECISION/C all PASS |

`R4_WITNESS/OUT/R4_RESULT.json`: `all_refused=true`, `restore_pass=true`.

## Preserved

Source identity 118/26 NOT_ADOPTED/14 HELD; W1/W2 typed/prose; W5 graph fates/edges; W3 no conditional admit; D5 projections; D6 literal cold; D7 machine freeze; lawful changed proposal route. Existing changed-scope suites: 29/29 and 11/11 OK. Final ZIP cold literal inventory/29/11/gates/six-projection verify pass.

**Still held:** same-C recheck, protected H1, native 100k/6 GiB/1-10-100, actual native/actor/science, source rights, F26 caller/invalidation. No architecture selection.
