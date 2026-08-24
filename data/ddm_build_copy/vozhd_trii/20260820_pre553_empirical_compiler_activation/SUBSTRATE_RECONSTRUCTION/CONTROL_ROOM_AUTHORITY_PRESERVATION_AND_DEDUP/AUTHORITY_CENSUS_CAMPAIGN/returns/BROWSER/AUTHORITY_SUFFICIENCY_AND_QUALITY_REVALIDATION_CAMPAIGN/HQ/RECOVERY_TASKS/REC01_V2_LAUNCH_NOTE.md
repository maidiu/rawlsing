# REC-01 V2 Relaunch

Status: `AUTHORIZED__FRESH_BRANCH_REQUIRED__FIRST_BLOCKER_PRESERVED`

Relaunch branch:

`agent/vozhd-trii-rec01-tir014-wvs7-fd-v2`

The exact start HEAD is the control HEAD that contains:

- `REC01_TIR014_WVS7_FD_EXECUTION_TASK.md`;
- `REC01_IMMUTABLE_SIBLING_INPUT_ACCESS_PATCH.md`;
- `REC01_BLOCKER_DISPOSITION.md`;
- `REC02_IMMUTABLE_SIBLING_INPUT_ACCESS_PATCH.md`;
- `REC02_PRELAUNCH_PATCH_DISPOSITION.md`.

The v2 worker must not cherry-pick, merge, copy, or treat the first blocked REC-01 return as source evidence. It may read the blocker disposition only to understand why v2 exists.

All substantive execution begins fresh from P0.
