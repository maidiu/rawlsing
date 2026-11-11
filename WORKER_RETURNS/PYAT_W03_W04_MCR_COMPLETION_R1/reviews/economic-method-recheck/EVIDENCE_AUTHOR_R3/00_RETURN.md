# Bench ECONOMIC_R3 — residual method repair

**Author status:** `DELIVERED_PENDING_RECEIVING` for the bounded method repair; whole MCR and economics remain `INCOMPLETE`.
**Source head observed:** `07f37e47893fdbc956766cea7d3ef550f064d8c7`
**Branch:** `agent/pyat-w03-w04-mcr-bench-integrated-r2`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2`

Prior RED `c44cf09f` and the normal-caller/derived-vs-canonical repair at `07f37e4` are preserved. This is the second benchmark-boundary repair; no final 100000 matrix or production/ABI change.

## Finding dispositions

| Finding | Correction | Small evidence |
|---|---|---|
| ECON-M1 | `cold`/`cells-and-hash` are no-policy/no-persist; full-matrix owns governed derived cache and canonical carrier separately. Cold threshold uses `cold_to_firstconsumer_stage_peak_rss_bytes`, never retained compressed-file size. | current 64 `cold` parity has zero derived files; full-matrix cold writes derived; warm hits derived; canonical files separate |
| ECON-M2 | `_stage` records entry/exit current RSS, sampled current-RSS stage peak, and process `ru_maxrss` separately. Combined public boundaries are explicitly labelled; later allocation test passes. | `evidence_summary`/raw stages; 13 benchmark tests pass |
| ECON-M3 | Parent starts child, then samples child RSS and kills over-limit; cap is active before profile data completes; `cap_enforced` only when monitored. No RLIMIT_AS claim on Darwin. | 8 MiB falsifier: `BLOCKED_EXACT_DEPENDENCY`, `cap_enforced=true` |
| ECON-M4 | cold-only baseline lookup is null-safe; baseline binds protected 4f3413, rows/profiles/repetitions/host/schema; gate enforces 15% cold stage-RSS, 90% repeat no-acceleration restart wall, >10% RSS/wall regressions, retention, and nonzero failure. | 64-row gate: cold pass, warm fail, final_shape false; no-baseline gate exits 2; identity/threshold falsifiers tested |
| ECON-M5 | source opens are explicit `NOT_APPLICABLE__SOURCEFREE_SYNTHETIC_EXACT_PHYSICAL_CELL_STREAM`; actual derived/canonical reads/writes; 3 fresh warm PIDs on one persisted root; amortization uses actual warm restarts. | 3 warm PIDs distinct; all derived/canonical hits true; no in-process warm |

## Small run result

- `40 passed` selected tests; `13 passed` benchmark tests.
- Three-source 64-row parity: narrow 128 events, wide/repeat 384 events; full consumer fingerprints equal across current 07f, frozen 46b and protected 4f.
- Current 64 full-matrix: derived miss/write cold, derived hit + canonical reopen hit warm, fingerprint parity true; `final_matrix_eligible=false`.
- Acceptance gate at 64 rows is diagnostic, not a pass. Current cold wide stage peak shows 38.99% improvement vs protected in this small run, but repeat no-acceleration restart wall ratio is `1.447` (>0.90); retention is `DO_NOT_RETAIN`. No threshold PASS is claimed.

## Limits

No 100000 × 3-repetition matrix was launched. Final candidate/economic receiving must use the corrected method at one HQ-pinned final SHA. All 12 MCR obligations, independent review/receiving, external block, protected merge and original35/native/science/actor rights remain outside this lane. No source/respondent/native effect, no new engine/reader, no install, no subworker/model change. Quota `UNKNOWN`; goal checks paused.
