# 00_REVIEW — PYAT W03/W04 MCR-C — Independent Economic/Memory Methodology

**Review status:** `EARLY_METHOD_FINDINGS_RETURNED` — **not a final receiving**, **not an acceptance**, and **not a complete 12-ID review**.

**Reviewer role:** independent economic/memory methodology and resource-evidence receiver; not the bench or cold author.

**Review turn:** `opencode-go/deepseek-v4.1-flash#max` (unchanged; no provider/model/account/effort switch).

**Review branch / head:**

- branch `review/pyat-w03-w04-mcr-economics-r1`
- head `16fd5f7b97a5b798b475ad99a61406afff236830`
- review lease: `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/`

**Contract and source refs:**

- contract: `PYAT_W03_W04_MCR_C_Commission.md`
- 12-ID source: `5a891a311c70f4cb8c09864008b33405362f7c7c`, obligations blob `b17c63cea9706f50a0d9c0f0ce064e967da4c8eb`
- PR895 exact: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
- protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`
- bench draft branch: `agent/pyat-w03-w04-mcr-bench-r1`, base `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`
- live completion worktree observed at `dcd00620d43b69039c63e51260dc878eac7ffe98`; it is not the review intake and not a frozen final candidate.

## 1. What was actually read and run

- Read the full MCR-C commission, the frozen 12-ID TSV and the W03/W34/engineering-R6 acceptance text.
- Snapshotted the live **initially uncommitted** bench code/test/workflow from `pyat-w03-w04-mcr-bench-r1`; live hashes matched the snapshot at the first read-consistency check. The exact snapshot and hashes are in `BENCH_DRAFT_SNAPSHOT/`. It is marked `UNCOMMITTED_DRAFT_AT_READ`; it is **not** commit-grade proof and no same-SHA final claim is made.
- The live author lane later advanced during this review to `c44cf09fb9ca5cbc235763d8bd5df9b0074de289` (`Add W03 W04 physical economy benchmark and paired baselines`). I snapshotted the exact committed c44 files in `BENCH_LIVE_C44_SNAPSHOT/`. The bench implementation hash is unchanged (`b00cf324...`); the test file added one `cells-and-hash` case. Neither snapshot is a final integrated candidate.
- Snapshotted the author's live partial bench metrics/return in `AUTHOR_PARTIAL_METRICS_SNAPSHOT/`. They were untracked at first read and are now part of the c44 author commit; they remain `NOT_FINAL_AUTHOR_PARTIAL` and are **limits**, not whole acceptance.
- Compared the bench draft's imports/call path against protected `4f3413fc` and PR895 `46b73256`. The protected baseline imports and a bounded 16-row protected cold probe ran.
- Ran only bounded probes:
  - 7 focused bench test cases at c44 (3 profile-parametrized cases plus 4 functions): `7 passed in 9.91s`. The earlier 6-case snapshot had `6 passed in 10.16s`.
  - candidate 16-row cold (review-head `16fd5f7b`, not PR895; method probe only); protected 4f3413fc 16-row cold; candidate 24-row full-matrix.
  - a cold-only baseline-pairing attempt, which failed as recorded below.
- Did **not** run a 100k benchmark, the full matrix, the full 43-case/12-ID suite, or any original source/respondent/native workload. The author's separate 100k receipt was read as an author partial, not reproduced.

## 2. Bounded readiness that did pass

- The draft harness uses the real current C11/I03/I05 path: `ExactPhysicalCellStream` → `project_c11_candidate_from_physical_cells` → `validate_c11_source_release` → `_compact_public_objects` → `C11Repository` → `CarrierNeutralResearchExecutor.execute_i03/execute_i05`. It is not a hand-built C11 object or a candidate-statistics oracle. The physical cell stream is a sourcefree synthetic fixture, which is the authorized S2 input for this obligation.
- The protected `4f3413fc` API contains the same imported facade/compact symbols; the protected 16-row cold probe completed with a `SUPPORTED` fact.
- The bench's release/consumer path returned actual `C11LogicalRelease`/internal records and actual I03/I05 facts in the bounded tests.
- The initial live bench snapshot was byte-identical to the live files at the first read-consistency check. The live branch later advanced to author commit c44cf09f; the c44 bench implementation hash is unchanged, its test added the cells-and-hash case, and the exact c44 snapshot is recorded separately. These are point-in-time snapshots only; neither is a frozen final candidate.

These are bounded readiness facts, not W03/W34 acceptance.

## 3. Actionable method findings

### ECON-M1 — The W03 `cold` scenario includes W04 cache persistence, so the W03 peak is contaminated by the cache write

**Status:** method defect; blocks W03/W34 receiving.
**Scope:** W03-COLD-HIGHWATER, W34-RESOURCE-ECONOMY.

Evidence in the snapshot:

- `_worker` persists whenever `args.worker_scenario in {"cold", "full-matrix"}` and a root is supplied: `bench_w03_w04_physical.py:519-525`.
- `_run_scenario` always supplies a root and passes `worker_scenario="cold"` for the `cold` scenario: `bench_w03_w04_physical.py:638-653`.
- The W03 check command is exactly `--scenario cold` (`PYAT_W03_W04_MCR_C_Commission.md:45`), and the W34 matrix is a separate full-matrix check (`:53`).
- The reported aggregate is `metrics.rss_peak_bytes` (`bench_w03_w04_physical.py:534-540`), aggregated in `_aggregate` (`:597-618`) and compared in `_compare` (`:622-635`). It includes the `persist` stage.

The bounded 16-row probe shows the contamination directly (not 100k evidence):

| stage | candidate cold 16 | protected 4f3413fc cold 16 |
|---|---:|---:|
| aggregate peak | 103,653,376 B | 104,046,592 B |
| `i02_validation_seal` peak / delta | 42,455,040 / 0 | 40,001,536 / 0 |
| `compact` peak | 64,471,040 | 99,053,568 |
| `firstconsumer` peak | 64,802,816 | 99,500,032 |
| `persist` peak / delta | 103,653,376 / 38,850,560 | 104,046,592 / 4,546,560 |

The candidate's compact stage is materially lower, but the `cold` aggregate is essentially unchanged because `persist` dominates it. The draft's aggregate threshold can therefore move for a W04/cache-body reason while the W03 I02-to-first-I03 peak is unchanged; that is the explicitly forbidden direction in the W03 negative. The 16-row probe is too small to decide the 100k outcome, but it demonstrates the attribution defect in the harness.

**Minimal owner action:** make `--scenario cold` a no-persist cold build, or capture and use a pre-persist peak through first I03/I05. Keep W04 persistence in `full-matrix`/a separate stage and report the two peaks separately. Add a test that `cold` does not call `ParquetC11Carrier.persist` (or that the W03 threshold uses only the pre-persist peak) and that a compact-only change with unchanged pre-persist peak cannot pass W03. Then rerun the exact 100k obligation.

### ECON-M2 — Stage RSS is process high-water, not a stage peak; projection/object/hash are not actually instrumented

**Status:** method defect; W03 stage-allocation evidence is inadequate.
**Scope:** W03-COLD-HIGHWATER stage evidence.

Evidence:

- `_stage` records `rss_peak_bytes` from `resource.getrusage(RUSAGE_SELF).ru_maxrss` after the stage and `rss_peak_delta_bytes = max(0, after_peak - before_peak)`: `bench_w03_w04_physical.py:84-98`. Once a prior stage has raised the process high-water mark, later stages report delta `0` even if they allocate memory; the reported `rss_peak_bytes` is not the stage's peak.
- `_build_release` labels the projection as built before the stage and then writes a post-hoc high-water value (`:332-371`); `objectconstruction` and `canonicalhash` share wall time and have no RSS values; `i02validation`/`seal` duplicate the same stage; `firstconsumer` is another cumulative high-water snapshot (`:422-423`).
- The bounded candidate cold 16 output has `i02_validation_seal` delta `0`, `firstconsumer` delta `307,200`, and no RSS for object construction/canonical hash. The 24-row full-matrix cold output has `i02_validation_seal` delta `0` and `firstconsumer` delta `335,872`.
- The commission requires stage peaks, not only compressed retained bodies (`PYAT_W03_W04_MCR_C_Commission.md:45`, R2/R6 at `:77-78`). The negative explicitly forbids a compact-only retained-body fall masking an unchanged/rising cold I02 peak.

The draft is honest that object construction/canonical hashing are combined at the public boundary, but combining them does not turn a cumulative process high-water mark into a stage peak.

**Minimal owner action:** record current RSS at stage entry and exit and sample/track a true per-stage peak (or run a stage in an isolated child where necessary); report `process_ru_maxrss` separately from `stage_current_rss_peak`. Measure the actual projection construction, or report it explicitly as combined with profile setup. Add a regression test that a known allocation in a later stage changes its stage peak even when the process high-water mark was already set. Do not claim a stage allocation unless the stage-specific peak is measured.

### ECON-M3 — The 6 GiB cap is installed after profile/cell construction; the 100k author receipt says `cap_enforced: false`

**Status:** method defect; scale safety and the required BLOCKED behavior are not established.
**Scope:** W03-COLD-HIGHWATER, W34-RESOURCE-ECONOMY, R6.

Evidence:

- `_worker` calls `_profile(args.worker_profile, args.worker_rows)` before the `resource.setrlimit(RLIMIT_AS, 6 GiB)` attempt: `bench_w03_w04_physical.py:438-461`; `MAX_CHILD_BYTES` is declared at `:49`.
- The profile constructs the 100k respondents, row bindings and routing before the cap, and the `profile_setup` stage is recorded before `cap_enforced` becomes true. A profile that exceeds the intended cap can be killed before the bench can emit an exact `BLOCKED_EXACT_DEPENDENCY`.
- The author's own partial 100k narrow receipt records `"cap_enforced": false` in `proof_02_resource_comparison.json`, while the return/02 text says a 6 GiB child cap is used. The author's 100k peak is 5,923,426,304 B; it completed under 6 GiB, but the cap was not enforced.
- R6 says: if 100000 events exhaust authorized memory, mark exact `BLOCKED_EXACT_DEPENDENCY`; never downsize and declare a full pass (`PYAT_W03_W04_MCR_C_Commission.md:78`).

**Minimal owner action:** set the limit before profile/cell construction, ideally in a small launcher immediately after process start before the bench imports/constructs data. Record cap enforcement as a precondition of every measured run; if the platform cannot enforce it, emit `BLOCKED_EXACT_DEPENDENCY` rather than a memory result. Add a low-cap test that proves an over-limit allocation is refused.

### ECON-M4 — Cold-only baseline pairing crashes; baseline identity and the W03/W34 thresholds are not enforced

**Status:** method defect / incomplete economic gate.
**Scope:** W03-COLD-HIGHWATER, W34-RESOURCE-ECONOMY, R6.

Evidence:

- The required W03 check is `--scenario cold` (`PYAT_W03_W04_MCR_C_Commission.md:45`). A cold-only baseline result has `"warm": null`. `_run_scenario` does:
  `(baseline_for or {}).get("warm", {}).get("aggregate")` at `bench_w03_w04_physical.py:684`.
  When `warm` is present but `null`, this dereferences `None` and raises `AttributeError: 'NoneType' object has no attribute 'get'`.
- I ran the exact bounded pair with a protected cold-only baseline:
  `--scenario cold --profiles narrow --rows 16 --repetitions 1 --baseline-json protected_cold_16.json`.
  It failed with that traceback and produced no candidate JSON. The traceback is preserved in `SMALL_PROBE/paired_cold_16.stderr`.
- `--baseline-json` accepts an arbitrary JSON (`:725-727`); `_compare` only returns baseline/candidate/ratio and `status=OBSERVED|NO_BASELINE` (`:622-635`). It does not bind the baseline to protected `4f3413fc`, exact rows/profile/host, the command, or process isolation. It does not compute a >=15% RSS PASS, a <=90% warm restart wall PASS, or a >10% RSS regression check.
- `regressions` only emits a wall regression above 10% (`:685-691`); it does not check RSS regressions or apply the required conditional retention. `_run_scenario` can return without any baseline and `main` still exits 0.
- The author's partial 1000-row matrix has one process per section, not three process-isolated repeats; the author's 100k narrow is one narrow cold measurement, not the required wide/repeat 3-repeat matrix. The author explicitly reports the 100k narrow RSS ratio as `1.1303` (a +13.0% regression versus protected; target is >=15% improvement), and does not claim PASS. That is a limit, not the final matrix.

**Minimal owner action:** fix the cold-only lookup; require a protected baseline run with the same exact rows/profiles/repetitions/host and bind its source SHA, command, and output hash into the candidate result; compare stage and aggregate values; hard-fail (nonzero) on `NO_BASELINE`, missing/mismatched baseline, or unmet thresholds; add the >10% RSS regression and explicit retention decision; test cold-only baseline, no baseline, wrong rows/host, and threshold failure. Final receiving must inspect the raw 100k 3-repeat receipts at the same frozen HQ SHA; a copied/edited baseline must not count.

### ECON-M5 — Source-open and repeat/retention economics are asserted rather than measured

**Status:** method gap; W34 repeat/amortization/retention is not yet proven.
**Scope:** W34-RESOURCE-ECONOMY, R6, conditional retention.

Evidence:

- `source_opens` is hard-coded to `0`: `bench_w03_w04_physical.py:540`. For the sourcefree `ExactPhysicalCellStream`, zero source opens may be a legitimate N/A, but it is not measured and the harness does not label it as N/A; the W34 requirement asks for source-open counts and R6 asks for source opens/restore cost (`PYAT_W03_W04_MCR_C_Commission.md:53`, `:78`).
- `cache_write_amortization` is only `persist.wall_seconds / profile["repeat_count"]` (`:541-544`). The `repeat` profile repeats `_consumer` on the same release in the same child process (`:424-427`); it does not perform repeated fresh-process warm restarts from one persisted cache. The benchmark therefore does not measure the repeat-heavy persistent workload's amortized restart/first-consumer cost; it estimates it with a repeat count.
- The draft's `limits` note says sourcefree and no source decode, but it does not provide an explicit `N/A`/`NOT_MEASURED` distinction for source opens, and it does not implement a conditional-retention decision for a nonbeneficial persist case.
- The W34 positive requires at least one qualified repeat-heavy persistent workload with median restart-to-first-consumer wall <=90% of no-acceleration baseline, report write amortization and any regression, and apply explicit conditional retention (`:53`).

**Minimal owner action:** either instrument actual source opens or emit an explicit `NOT_APPLICABLE__SOURCEFREE_SYNTHETIC_STREAM`; count actual cache reads/writes and perform at least two fresh-process warm restarts from the same persisted cache, with the restart-to-first-consumer metric; compute amortization from actual uses and bytes; add a nonbeneficial persist case that must be retired/not retained; add an explicit retention decision to the output and test it.

## 4. Current author partial measurement (limit, not acceptance)

The author's `00_RETURN.md` and `02_resource_economy.md` in `AUTHOR_PARTIAL_METRICS_SNAPSHOT/` state `INCOMPLETE` and report:

- 100k narrow cold, current `46b73256` vs protected `4f3413fc`: wall 777.53 s vs 997.04 s (ratio 0.7798), peak RSS 5,923,426,304 B vs 5,240,467,456 B (ratio 1.1303, **+13.0% RSS regression**), `cap_enforced: false` for both.
- The target is >=15% cold median RSS improvement; the author's own partial result does not meet it.
- Because the `cold` command persists (ECON-M1), the author's 100k cold RSS is a cache-inclusive partial, not an isolated W03 I02-to-first-I03 peak. It must not be compared to the W03 target without separating the pre-persist peak.
- 100k wide/repeat and the final three-repetition candidate matrix were not run; 1000-row matrix used one process per section, not three repeats.
- The author's return claims 7 focused benchmark tests. The live c44 test file has 7 collected cases; my bounded run of it was `7 passed in 9.91s`. The earlier 1b0c8dc4 snapshot had 6 cases. The author's 50 selected-test count is not the full 43-case/12-ID acceptance and was not independently run here.
- The separate "41 universal / 37 pass / 2 skip R157" clause in the dispatch is not a W03/W04 bench claim in the inspected refs, and this lane did not verify it. If that candidate is still active, it needs its own exact-SHA review; it is not used as W03/W04 evidence here.

This is a **partial author measurement**, not an independent final result, and not a PASS or FAIL of the final integrated candidate.

## 5. Bounded examined readiness and unresolved boundary

Ready for the next step only in the sense that the bench harness is a real sourcefree C11/I03/I05 path and its focused tests pass at small scale. It is **not ready for W03/W34 receiving** because the findings above are method-level, not cosmetic.

Not assessed / held:

- full 12-ID coverage and all 12 claim-specific outputs;
- 100k wide/repeat, 3 process-isolated repeats, median/range;
- per-stage true peaks, CPU/wall/disk/files/source-opens/cache-write amortization;
- actual required raw receipts, exact commands, process isolation, cap enforcement;
- full W03/W04 suite and all engineering/science/authority courts;
- original35, source, SAV/DTA/DB, native, science, actor, FF/N11/Sorok, protected merge, CI waiver, new worker/engine/query/authority registry.

No final receiving was attempted. The final economic receiving must be resumed at the **same HQ-frozen SHA as the engineering review**, after the bench owner's repair and a frozen same-candidate matrix. It must inspect the actual raw receipts and full 12 IDs, not this early review.

## 6. Exact-scope verdict and least necessary owner repair

**Verdict:** `EARLY_METHOD_FINDINGS_RETURNED`; **W03/W34 bench draft NOT RECEIVABLE**; **whole W03/W04 remains INCOMPLETE**; **author ceiling remains DELIVERED_PENDING_RECEIVING / INCOMPLETE**, not accepted. No merge, no protected adoption, no science/source/authority issuance.

**Least necessary owner repair:** implement ECON-M1 through ECON-M5 in the bench harness and tests, then rerun the bounded tests and the exact 100k 3-repeat matrix against protected `4f3413fc` at the same host/process conditions; preserve exact candidate/protected hashes, commands and raw outputs; freeze the final integrated SHA; then resume independent final receiving. Do not use the author's 100k narrow +13.0% RSS result as a W03 PASS, and do not treat the 256-row CI smoke or the 1000-row single-run matrix as 100k acceptance.
