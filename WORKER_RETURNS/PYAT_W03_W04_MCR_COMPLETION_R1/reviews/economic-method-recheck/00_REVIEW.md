# 00_REVIEW — W03/W04 economic method recheck at `dec934dde`

**Status:** `REVISE_METHOD` — the corrected benchmark method is **not yet ready for the pinned full-scale run**. This is not whole-economic or 12-ID acceptance.

**Reviewer role:** original independent economics/method receiver; not the implementation author.

**Review turn:** `opencode-go/deepseek-v4.1-flash#max` (unchanged).

**Review branch / exact head:**

- branch `review/pyat-w03-w04-economic-method-recheck-r1`
- head `dec934dde93ffa9e087d5648678d1bb7854ff015`
- review lease: `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economic-method-recheck/`

**Governing and source refs:**

- original review: `8992151d0150185d5ed4ffe5bb866329fb924b2b`; its old `RED` is preserved.
- frozen commission: `PYAT_W03_W04_MCR_C_Commission.md` (sha256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`)
- frozen 12-ID TSV: `WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv` at source `5a891a311c70f4cb8c09864008b33405362f7c7c`, blob `b17c63cea9706f50a0d9c0f0ce064e967da4c8eb`, sha256 `5de8d68207de353926bd2d42095a8c8c44a36b06ac4038a7c9b16a1b6173428e`.
- author repair: `1d7007a34fdf9cb7cdd30ec581e7d94523047da7`
- integrated exact source: `dec934dde93ffa9e087d5648678d1bb7854ff015`
- actual caller: `07f37e47893fdbc956766cea7d3ef550f064d8c7`
- cold-order source pin: `f9aedf8e2b570174881cef627dc6a24b78031ed7` (independent cold-order review; not reopened here)
- frozen PR895: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
- protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`

**Exact benchmark code/test blobs at `dec934dde`:**

- `1789450f9a2f3cdf79265478c4103920a8e2f2bc  rawlsing_next/bench_w03_w04_physical.py`
- `1ca91502a30ea6af2bb983a71e465dd613cdbf1a  rawlsing_next/tests/test_bench_w03_w04_physical.py`
- `git diff 1d7007a..dec934dde -- rawlsing_next/bench_w03_w04_physical.py rawlsing_next/tests/test_bench_w03_w04_physical.py` is empty; the exact source carries the repaired method.

## 1. What was read and run

- Read the full repair docs and the `ECONOMIC_R3` correction matrix, evidence summary, raw 64-row current/baseline receipts, `warm_restarts_3.json`, cap falsifier, no-baseline gate, and the exact source diff.
- Ran only bounded checks:
  - `13 passed in 21.97s` for the focused benchmark test file.
  - In-memory 64-row gate audit from the author raw receipts.
  - gate falsifiers for a >10% other-profile regression, missing baseline events/commands/hash, and cap absence.
  - clean cold 16-row vs inherited-policy cold 16-row; same-size/same-mtime derived corruption; raw warm-clock audit.
- Did not run 100k, the final 100k matrix, original data, native workload, or any production/test/workflow edit. Did not touch the independent cold-order or MCR-validator work.

## 2. Per-finding disposition

### ECON-M1 — `PARTIAL_REVISE`: root-level cold no-persist is corrected, but inherited policy can still write a governed cache and contaminate the cold measurement

The repaired `_worker` sets `build_root` only for `full-matrix`/`warm`/`reopen` (`bench_w03_w04_physical.py:591`), and the new cold test observes zero `derived_cache_files` and no canonical files. That clean path is corrected.

However, the production facade `build_source_backed_c11_repository` calls `attach_governed_cache` for an `ExactPhysicalCellStream` (`pre553_source_backed_c11_facade.py:1288-1296`), and `attach_governed_cache` reads the host `RAWLSING_C11_ACCELERATOR_POLICY` (`_pre553_w03_cold_compact.py:236`). The benchmark's cold `_run_child` copies the parent environment and does not clear the policy/legacy environment. My bounded probe with a valid inherited policy produced a real derived file while the benchmark reported:

```text
clean cold 16:        cold_metric 56,971,264; process 56,983,552; derived_cache_files 0
inherited-policy 16:  cold_metric 102,768,640; process 102,780,928; derived_cache_files 0
                      derived_cache_status NO_GOVERNED_DERIVED_CACHE_WRITE
                      actual policy cache file: env_policy/derived-accelerator/c11-events-f.parquet (22,412 bytes)
```

This is a hidden cache-write/cold-cache contamination exactly in the W03 negative direction. The clean test is insufficient; the cold child must explicitly clear `RAWLSING_C11_ACCELERATOR_POLICY` and `RAWLSING_C11_ACCELERATOR_DIR`, or the benchmark must detect the actual policy root and reject/record any write. Add an inherited-policy cold test.

**Exact evidence:** `PROBE/clean_cold_16.json`, `PROBE/env_cold_16b.json`, `PROBE/env_policy_cache_observation.txt`, `PROBE/method_probe_summary.txt`.

### ECON-M2 — `CORRECTED`: stage current RSS and process cumulative high-water are now separated

The repaired `_stage` records entry/exit current RSS from OS `ps`, a sampled current-RSS stage peak at 50 ms, and process `ru_maxrss` separately (`bench_w03_w04_physical.py:115-141`). Aliases are explicitly labelled combined rather than reported as zero; `cold_combined` is an honest combined public boundary. The 13 focused tests pass, including the post-highwater allocation test. Both arms use the same sampler. No method residual is required for this item at the current method boundary; the true 100k sampling behavior remains a final-scale obligation, not a reason to reopen this repair.

### ECON-M3 — `PARTIAL_REVISE`: parent kill monitor works at 8 MiB, but acceptance does not require cap enforcement/peak and the monitor is not a hard bound

The parent `_run_child` now starts the child with `Popen`, samples RSS, and kills above `--cap-bytes` (`bench_w03_w04_physical.py:706-785`). The 8 MiB falsifier returns `BLOCKED_EXACT_DEPENDENCY`, `cap_enforced=true`, with a sampled peak of `15,986,688` bytes above the 8 MiB cap. That is a real bounded falsifier.

But the acceptance gate contains no cap field or check. The 64-row gate and identity probes expose `gate_keys` with no `cap_enforced`/`cap_peak_sampled_bytes`/`cap_bytes`, and a synthetic result can pass the economic gate without any cap evidence. On a successful run, `cap_enforced` is set to `sampled` (at least one RSS sample), not proof that the required bound was enforced. The 8 MiB falsifier is not a 100k guarantee. The final gate must require an active monitor, sampled cap evidence, and no overshoot beyond the declared authorized bound; if the monitor cannot enforce the bound, the run must be `BLOCKED_EXACT_DEPENDENCY`, not a whole PASS.

**Exact evidence:** `EVIDENCE_AUTHOR_R3/cap_falsifier.json`, `PROBE/gate_identity_and_cap_probe.txt`, `PROBE/method_probe_summary.txt`.

### ECON-M4 — `PARTIAL_REVISE`: null-safe baseline and identity checks are corrected, but the gate still has three contract deviations

Corrected parts: `_baseline_section` is null-safe; a cold-only baseline no longer crashes; the gate checks schema, protected source head `4f3413`, rows, profiles, repetitions, and host; the cold `--acceptance-gate` returns 2 with no baseline; the 64-row current/baseline gate reports cold improvement `0.389853`, warm ratio `1.447120`, `final_shape=false`, `pass=false`, and `DO_NOT_RETAIN__NONBENEFICIAL_OR_REGRESSION_OR_MISMATCH`.

Residuals:

1. **Universal >10% regression ban.** `_acceptance_gate` sets `pass_all = ... and not regressions` (`bench_w03_w04_physical.py:1029-1031`), and the regression loop adds every cold/full-matrix profile with >10% RSS/wall regression. The frozen W03 positive requires other profiles and wall regressions to be explicitly reported, with any >10% regression requiring justified correction — not an automatic universal pass ban. My synthetic other-profile 20% regression probe makes the gate `pass=false` even with the selected cold-wide/warm-repeat gates satisfactory. The gate should record `REGRESSION_...` and require an explicit correction/justification, rather than silently inventing a stricter universal acceptance rule.
2. **Warm clock is not startup-to-first-consumer.** The gate uses `median_parent_wall_seconds` for both current warm and protected cold (`:1010-1015`). The current warm child runs `_consumer` first and then `canonical_reopen`/canonical consumer (`:641-669`). In the 64-row repeat warm raw receipt: current parent `2.723282 s`, `firstconsumer` `0.122029 s`, `canonical_reopen` `0.687796 s`; baseline cold parent `1.881863 s`, firstconsumer `0.125453 s`. The 1.447 ratio therefore includes work after the first consumer, contrary to the correction matrix's statement that the comparison is not canonical reopen. The measured RED may still fail after a conservative correction, but the frozen W34 metric is restart-to-first-consumer; the gate must measure that exact clock and keep canonical validation separate.
3. **Baseline identity is incomplete.** The gate checks source head/rows/profiles/repetitions/host/schema, but it has no `actual_event_counts`/event-parity, command, or expected baseline-file hash check. A synthetic baseline with the same five identity fields but no event counts, commands, or hash passes the gate (`pass=true`) when selected metrics are satisfactory. The raw `warm_restarts_3.json` and parity files contain actual event counts and fingerprints, but the gate does not bind them. Add exact event-count/fingerprint parity, the protected baseline file sha256, and the exact command to the identity gate.

The 64-row cold-wide improvement is `0.389853 = 38.99%`; the warm repeat ratio is `1.447120 = 144.7%`; the retention is `DO_NOT_RETAIN`; `final_shape=false`. This is diagnostic RED, not a 100k PASS; it is not a reason to optimize production before the final scale.

### ECON-M5 — `PARTIAL_REVISE`: explicit source-open N/A, three fresh warm PIDs, and separate derived/canonical evidence are corrected; write amortization and derived-hit truth are not

Corrected parts: `source_opens` is explicit `NOT_APPLICABLE__SOURCEFREE_SYNTHETIC_EXACT_PHYSICAL_CELL_STREAM`; `warm_restarts_3.json` has three distinct PIDs on one persisted root, all derived and canonical hits true; derived and canonical files are separate; the 64 full-matrix shows derived miss/write cold and derived/canonical hits warm with consumer fingerprint parity.

Residuals:

1. **Amortization excludes the derived write.** `cache_write_amortization` is `canonical_persist_wall_seconds_total / len(warm_runs)` (`bench_w03_w04_physical.py:931-942`), e.g. `0.204367/3 = 0.068122` in `warm_restarts_3.json`. The derived cache write is part of the W34 cache-write cost; no derived-write wall time is separately measured. The reported amortization is therefore incomplete, even though canonical write timing is real.
2. **Same-size/same-mtime derived corruption is reported as a hit.** `_derived_state` reads an envelope, but `derived_hit` is only `before_keys == after_keys` (name, size, mtime); the status is `HIT_EXACT_ENVELOPE_AND_MTIME`. My bounded probe corrupted one byte while preserving size and mtime; `_build_release` returned `derived_hit=True`, `derived_write=False`, status `HIT_EXACT_ENVELOPE_AND_MTIME`, with the same release ref and event count. That is not proof of a valid envelope/body hit. The existing test only shortens the file (changes size); it does not cover same-size/same-mtime corruption. The method must validate the envelope/content identity, not only metadata, and the final cache-hit metric must not count a corrupted slot.

**Exact evidence:** `PROBE/derived_envelope_probe.txt`, `EVIDENCE_AUTHOR_R3/warm_restarts_3.json`, `PROBE/method_probe_summary.txt`.

## 3. Diagnostic small result matches the author record — and remains non-final

- Focused benchmark tests: **13 passed**.
- 64-row gate: `cold_pass=true`, `cold_rss_improvement=0.389853...` (wide), `warm_pass=false`, `repeat_wall_ratio=1.447120...`, `retention=DO_NOT_RETAIN...`, `final_shape=false`, `pass=false`.
- Cap 8 MiB falsifier: `BLOCKED_EXACT_DEPENDENCY`, `cap_enforced=true`, sampled peak `15,986,688 B`; this proves the monitor can kill a small process, not that a 100k run is bounded.
- Three warm PIDs: `78863, 78906, 78951`; derived hits `true,true,true`; canonical hits `true,true,true`; amortization `0.068122...` is canonical-only.
- Clean cold 16: `56,971,264 B` cold metric; inherited-policy cold 16: `102,768,640 B` with a hidden 22,412-byte derived file and `derived_cache_files=0` reported.
- Same-size/same-mtime derived corruption: `derived_hit=true`, `derived_write=false`, `HIT_EXACT_ENVELOPE_AND_MTIME`.

The author's small record (`cold wide 38.99%`, warm repeat ratio `1.447`, `DO_NOT_RETAIN`, `final_shape false`) is confirmed. It is diagnostic RED, not a pass, and not a reason to optimize production before the final scale.

## 4. Decision

**`REVISE_METHOD` — not `METHOD_READY_FOR_PINNED_FULL_SCALE`; not `BLOCKED_DEPENDENCY`.**

There is no proven irreducible host restriction in this bounded review. The five original counterexamples are materially improved, and ECON-M2 is corrected. However, the exact residuals above change the actual acceptance semantics: inherited policy can contaminate the W03 cold measurement; the cap is not part of the acceptance gate; the warm economic clock includes work after first consumer; the gate invents a universal >10% regression ban and lacks event/command/hash identity; and M5's write amortization and derived-hit truth are incomplete.

The owner should fix the method before the pinned full-scale run:

1. Clear policy/legacy env in cold children, or detect and reject actual policy writes; add inherited-policy cold test.
2. Require cap monitor evidence in the final gate; reject unmonitored or over-cap runs; keep the 8 MiB falsifier as a falsifier, not a guarantee.
3. Replace the universal regression ban with report + explicit justified-correction semantics; retain the frozen 15% cold and 90% repeat thresholds.
4. Measure and gate startup-to-first-consumer separately from canonical reopen/consumer; do not include canonical post-first-consumer work in the W34 repeat clock.
5. Bind baseline actual events/fingerprints, exact command, and baseline file sha256 into identity; null-safe cold lookup is already fixed.
6. Measure derived-write amortization and validate same-size/same-mtime derived content before claiming a hit; add tests.
7. Then freeze the exact candidate and run the 100k, three-repetition, three-profile matrix against the protected 4f baseline at the same host/method; final independent receiving must inspect raw receipts and full 12-ID coverage.

## 5. Final obligations (not this review)

- Final 100k × 3-repetition × narrow/wide/repeat matrix; no downsizing and no 64-row PASS.
- Same HQ-frozen SHA for engineering and economic receiving.
- External SHA-bound MCR evidence block, `--verify-return`, all 12 IDs, all engineering/science/authority courts.
- CI/proof CC-F03/F04 and any separate MCR-validator/cold-order results remain independent and pending.
- Original35, source, SAV/DTA/DB, native, science, actor, FF/N11/Sorok, protected merge held.

No production/test/workflow edit, no source/respondent/native execution, no merge, no new worker/model/provider/effort switch, no full matrix or 100k run in this review.
