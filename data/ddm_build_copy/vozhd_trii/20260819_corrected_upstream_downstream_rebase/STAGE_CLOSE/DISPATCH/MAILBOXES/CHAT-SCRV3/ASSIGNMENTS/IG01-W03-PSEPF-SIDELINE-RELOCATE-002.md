# Worker #3 — IG_PSEPF_SIDELINE_RELOCATION

Permanent chat: `CHAT-SCRV3`  
Most recent submitting agent: `IG_PSEPF_ZERO_POSITIVE_GUARD`  
Worker class: **SUB-VOZHD**

Mission branch: `agent/vozhd-trii-ig-psepf-sideline-relocation`  
Exact base: `0777a34e50221bde6801dbaca26c058a7350c9e8`

Binding activation control: `agent/vozhd-trii-implementation-activation-control@e99722b560b2f2df9dd354d5865d32c85f52db2f`.

Use `agent/vozhd-trii-ig-psepf-zero-positive-guard@ad032a4d7820d4eada2a5577e1c3dab2a46b9872` only as implementation evidence. Do **not** merge/cherry-pick its legacy-tree paths.

## Mission

Transpose the already-returned zero-positive guard and tests into the clean sideline machine with no semantic redesign.

Write **only**:

- `rawlsing_next/v3_psepf_zero_positive_guard.py`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`

No new runtime or executable tests under `data/ddm_build/**` or `data/ddm_build_copy/**`. No imports from legacy runtime modules there. Mechanical import/path changes required for relocation are allowed; semantic behavior changes are not. The default accepted positive transition registry must remain empty.

Run the relocated test file. Verify base→HEAD contains only the two allowlisted paths.

If the old implementation itself contains a semantic defect, fail closed instead of repairing it under this relocation assignment.

Return exactly one token:

- `IG_PSEPF_SIDELINE_RELOCATION_COMPLETE`
- `BLOCKED_RELOCATION_SEMANTIC_DEFECT_FOUND`
- `BLOCKED_RELOCATION_EXECUTION_ENVIRONMENT`

Return exact HEAD SHA with the token.
