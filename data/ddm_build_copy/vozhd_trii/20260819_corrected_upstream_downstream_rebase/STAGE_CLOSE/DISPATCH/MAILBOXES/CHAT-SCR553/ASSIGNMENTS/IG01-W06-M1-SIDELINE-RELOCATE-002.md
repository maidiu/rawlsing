# Worker #6 — IG_M1_SIDELINE_RELOCATION

Permanent chat: `CHAT-SCR553`  
Most recent submitting agent: `IG_M1_IMPLEMENTATION`  
Worker class: **SUB-VOZHD**

Mission branch: `agent/vozhd-trii-ig-m1-sideline-relocation`  
Exact base: `0777a34e50221bde6801dbaca26c058a7350c9e8`

Binding activation control: `agent/vozhd-trii-implementation-activation-control@e99722b560b2f2df9dd354d5865d32c85f52db2f`.

Use `agent/vozhd-trii-ig-m1-temporal-v554-admission-dedup@0bdb74ff541ff3c976d76492a959ba7e74f29ceb` only as implementation evidence. Do **not** merge/cherry-pick its legacy-tree paths.

## Mission

Transpose the already-returned IG-M1 runtime and tests into the clean sideline machine with no semantic redesign.

Write **only**:

- `rawlsing_next/m1_temporal_v554_admission_dedup.py`
- `rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`

No new runtime or executable tests under `data/ddm_build/**` or `data/ddm_build_copy/**`. No imports from legacy runtime modules there. Mechanical import/path changes required for relocation are allowed; semantic behavior changes are not.

Run the relocated test file. Verify base→HEAD contains only the two allowlisted paths.

If the old implementation itself contains a semantic defect, fail closed instead of repairing it under this relocation assignment.

Return exactly one token:

- `IG_M1_SIDELINE_RELOCATION_COMPLETE`
- `BLOCKED_RELOCATION_SEMANTIC_DEFECT_FOUND`
- `BLOCKED_RELOCATION_EXECUTION_ENVIRONMENT`

Return exact HEAD SHA with the token.
