# Requalification matrix

| R00V defect | Independent reviewer assertion | Result |
|---|---|---|
| D1 executed native no evidence | `decision == HOLD_TRUSTED_NATIVE` | PASS |
| D2 supported status no evidence | `decision == HOLD_TRUSTED_NATIVE` | PASS |
| D3 prohibited completed zero | `decision == REFUSE_STATUS` | PASS |
| D4 semantic mutation + status edit | `decision == REFUSE_FRONTIER` | PASS |
| D5 unknown grade/kind | `decision == REFUSE_AUTHORITY` | PASS |
| D6 duplicate occurrence objects | `decision == REFUSE_FRONTIER` | PASS |
| D7 handle contract mismatch | `decision == REFUSE_PIN` | PASS |
| D8 eligible→held | `decision == REFUSE_STATUS` | PASS |

Also executed:

- 36/36 policy cases with independent Git pin.
- Valid subsets 1/5/17 and reverse order → local ALLOW.
- Valid full occurrence transport → local ALLOW; semantic/unsupported occurrence transport → REFUSE.
- Unknown submitted kind/native claim → REFUSE.
- Semantic mutation masked by disposition edit → REFUSE_FRONTIER.
- Handle version/contract mismatch → REFUSE_PIN.
- Invalid status values/unknown edit IDs → REFUSE_STATUS.
- Simultaneous faults cannot return local ALLOW.
- Same-assertion dependency fault: ALLOW → REFUSE_FRONTIER → cold restore ALLOW.

Receipts: `reviewer_replay.json`, `defect_requalification.json`, `junit/r00v_r2.xml`, `dependency_fault.json`.
