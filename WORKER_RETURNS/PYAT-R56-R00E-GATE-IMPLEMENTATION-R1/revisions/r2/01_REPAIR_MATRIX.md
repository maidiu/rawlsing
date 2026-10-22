# Repair matrix (defect → general validator → evidence)

| Defect | General repair | Evidence |
|---|---|---|
| D1 EXECUTED_NATIVE | Allowed claim kinds/grades validated; local executed-native without trusted observation → HOLD_TRUSTED_NATIVE; active native flags/traces/attestations → REFUSE_FORGED_EVIDENCE. | `test_executed_native_without_evidence_holds`; `defect_matrix.json` |
| D2 SUPPORTED status | Status transition validator: COMPLETED/SUPPORTED without native evidence holds; only POLICY_STATUS_CHECK_ONLY hand-derived OBSERVED_ZERO/VALID_NULL/VALID_EMPTY/UNKNOWN values are local. | `test_supported_status_without_native_evidence_holds` |
| D3 PROHIBITED completion | Final eligibility must equal policy-owned eligibility; invalid transitions and non-eligible completed results refuse. | `test_prohibited_operation_cannot_be_completed_observed_zero` |
| D4 semantic masking | Immutable operation projection is always compared, excluding only dynamic execution/result/proof fields; status edits cannot exempt direction/roles/values/identity. | `test_semantic_mutation_not_masked_by_status_edit` |
| D5 unknown grade/kind | Allowed grades from pinned policy; allowed kinds explicit; unknown fails closed. | `test_unknown_claim_grade_and_kind_refuse` |
| D6 occurrence objects | Supplied occurrence objects are shape/semantic/qualified-key validated; unsupported transport explicitly refuses; duplicate/unknown refs refuse. | `test_duplicate_occurrence_objects_refuse` |
| D7 handle identity | Handle commit/root, blobs, policy, synthetic, freeze, expected IDs and full expected objects are checked against exact Git pin. | `test_policy_contract_mismatch_refuses` |
| D8 ELIGIBLE→HELD | Eligibility is policy-owned; disposition edits must preserve original eligibility except no lawful cross-unit relation → HOLD. | `test_eligible_to_held_disposition_refuses` |

Additional: invalid execution/result values, unknown edit IDs, unknown submitted kind/native claim, multiple simultaneous faults, subset/order/typed identity, policy dependency substitution and cold restore.
