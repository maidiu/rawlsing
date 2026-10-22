# Defects found — return to same R00E implementer

`evidence/defect_probes.json` records 8 defects. All tests below were executed through the public evaluator with the independently verified canonical pin.

| # | Failing input | Actual | Required secure behavior |
|---|---|---|---|
| D1 | `request.claim_kind="EXECUTED_NATIVE"` with full 18 operations, no native evidence | ALLOW_LOCAL_POLICY_CONSISTENT | HOLD_TRUSTED_NATIVE / REFUSE_FORGED_EVIDENCE / REFUSE_AUTHORITY |
| D2 | One operation `execution=COMPLETED, result=SUPPORTED, proof_source=TEST_ONLY_HAND_DERIVED`, no native evidence | ALLOW_LOCAL_POLICY_CONSISTENT | HOLD/REFUSE; local policy may not assert supported execution |
| D3 | PROHIBITED operation set `eligibility=ELIGIBLE, execution=COMPLETED, result=OBSERVED_ZERO` with denominator/numerator | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_STATUS |
| D4 | Change one operation’s `direction_ref` and add a benign status edit for the same operation ID | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_FRONTIER; status edits must not suppress exact semantic comparison |
| D5 | `request.claim_grade="MADE_UP"` | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_AUTHORITY/STATUS/PIN |
| D6 | Duplicate `submitted.occurrence_objects` (same qualified key) | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_FRONTIER |
| D7 | `PinnedPolicyHandle.policy.contract_id="OTHER"` (same-process constructed handle) | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_PIN/IDENTITY |
| D8 | ELIGIBLE operation disposition-edited to HELD | ALLOW_LOCAL_POLICY_CONSISTENT | REFUSE_STATUS |

D1–D6 and D8 are candidate-input paths. D7 is within the stated trusted-supervisor assumption; it shows the gate does not verify the handle’s contract identity even when the handle is supplied in-process.

## Why this blocks acceptance

The frozen contract separates eligibility, execution and result, and requires exact operation identity before any claim transition. The gate currently lets a candidate:

- claim native execution without evidence;
- mutate an operation’s semantic identity while masking the mismatch with a status edit;
- move PROHIBITED operations into completed observed-zero;
- supply unknown claim grades;
- ignore submitted occurrence objects;
- change ELIGIBLE to HELD;
- use an in-process handle whose policy contract identity does not match.

The 36 oracle cases do not exercise these paths. The author’s 36/36 pass is therefore insufficient for the generic policy/claim gate claim.
