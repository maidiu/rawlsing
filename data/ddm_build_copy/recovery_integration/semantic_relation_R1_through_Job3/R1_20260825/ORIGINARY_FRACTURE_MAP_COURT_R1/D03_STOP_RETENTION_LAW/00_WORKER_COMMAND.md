# D03 — FRACTURE-MAP CONTINUATION / STOP / RETENTION LAW RECOVERY R1

Repository: maidiu/rawlsing
Worker branch: agent/verkhovod-fracturemap-d03-stop-retention-law-r1
Parent HQ ref at branch creation: 80843fc92b79bf591f57b22bae7ccc4db0db1ac3

## Mission
Recover the exact law for when a discovered fracture-map branch is retained, recursively continued, reported-only, or stopped. Documentary/authority work only. No production code. Do not consume still-running L02/L03.

## Read first
- Authority 35 and 36A.
- L01 RESULT.
- L04 RESULT at `agent/verkhovod-fracturemap-l04-multilabel-residual-stoplaw-r1`.
- G01 historical implementation RESULT.
- G02/G05 current-controller audits.
- Existing typed-state/support/measure authority in current PRE553.

## Required distinctions
Adjudicate exact semantics for:
- supported branch retained + eligible to recurse;
- supported branch retained but not eligible to recurse;
- stable minority;
- split/multimodal branch;
- valid-empty;
- underpowered/insufficient support;
- low support/exploratory-only if lawful;
- residual/none/category-failure;
- missing/unavailable/unresolved/noncomparable;
- max depth;
- no meaningful split/no gain;
- unstable branch;
- no remaining eligible predictors/questions.

For each, state whether the branch itself survives as learned empirical evidence even when recursion stops.

## Threshold discipline
The originary examples 50/25/10 are illustrative, not universal law. Recover parameter existence, owner/governance source, and which quantities must be measured. Do not invent thresholds.

## Anti-collapse
`STOP_RECURSION != DELETE_BRANCH`
`UNDERPOWERED != VALID_EMPTY != MISSING`
`NONE_OF_THESE != MISSING/DK/REFUSAL/NOT_APPLICABLE`

## Return
Under `.../ORIGINARY_FRACTURE_MAP_COURT_R1/D03_STOP_RETENTION_LAW/` produce:
RESULT.md, RESULT.json, STOP_STATE_LATTICE.csv, RETENTION_VS_CONTINUATION_MATRIX.csv, THRESHOLD_AUTHORITY_LEDGER.csv, MINIMUM_HQ_LAW_GAPS.md, CHANGED_FILES.txt.

Success token:
`D03_FRACTURE_MAP_STOP_RETENTION_LAW_R1_COMPLETE`
