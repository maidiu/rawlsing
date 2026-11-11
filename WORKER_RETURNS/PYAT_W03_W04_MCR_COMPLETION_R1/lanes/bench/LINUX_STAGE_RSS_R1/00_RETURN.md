# Linux stage-RSS test repair

**Status:** `DELIVERED_PENDING_RECEIVING` for the exact Linux CI test failure; no economic/full-12 acceptance.

- **Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2`
- **Branch:** `agent/pyat-w03-w04-linux-stage-rss-repair-r1`
- **Base head:** `3337b7946c5ab345d86dc48321c9b06ac4b6810a`
- **CI evidence:** run `42984252993`, job `130401567393`, head `254ee5b8bf81a7c806fd95c3caf9f67e58c31edb`
- **CI result:** 99 tests; 98 passed, 1 failed; smoke skipped; missing smoke artifact secondary only.
- **Failure:** `test_stage_peak_tracks_post_highwater_allocation` asserted `process_ru_maxrss_after_bytes >= stage_peak_current_rss_bytes` on Linux:
  `290238464 >= 290365440` (failure by 126,976 bytes).
- **Production benchmark bytes:** unchanged. Only the test was edited; no threshold, cache, carrier, query, validator, workflow, dependency or contract change.

## Diagnosis

The old assertion compared two different counters:

1. `stage_peak_current_rss_bytes` — a current resident-set sample collected by `ps -o rss=` during the stage; it can reflect an allocation after an earlier process high-water.
2. `process_ru_maxrss_after_bytes` — the kernel's cumulative `getrusage(RUSAGE_SELF).ru_maxrss` high-water counter, normalized from Linux KiB / macOS bytes.

These counters are not ordered by a required invariant. Both Linux values are byte-normalized and internally consistent; the kernel high-water counter was 126,976 bytes below the separately sampled current-RSS peak. The test's cross-counter ordering assumption was invalid, not a demonstrated sampler unit/timing defect.

The required obligation is preserved: the stage current-RSS sampler must distinguish a later allocation after an earlier process high-water, while the process cumulative high-water remains separate and truthfully labelled.

## Repair

Replaced only the invalid cross-counter assertion with:

- a bounded real stage probe: hold 20 MiB, then allocate 8 MiB inside `_stage`; require `stage_peak_current_rss_bytes - entry >= 4 MiB`, preserving the post-high-water intent;
- truthful process-counter assertions: `ru_maxrss_after >= before` and `rss_peak_bytes == process_ru_maxrss_after`, without claiming cumulative high-water is an upper bound on stage samples;
- a deterministic counter-falsifier that fixes `_rss_peak_bytes` low and proves the stage peak remains independently observed, rather than aliased to the cumulative counter.

No old positive was silently dropped: the 8 MiB value check and stage growth check remain. No tolerance, clamping, rounding, Linux skip or economic-threshold change was used.

## Evidence

- `CI_RUN_42984252993_failed.log`, `CI_RUN_42984252993_run.json`, `CI_RUN_42984252993_junit.xml` — exact preserved failure.
- `tests_22_affected_file.out` — affected benchmark file: **22 passed** locally.
- `targeted_stage_tests.out` — exact two stage tests: **2 passed**.
- `stage_counter_severance.json` — deterministic proof: old cross-counter ordering **false**, separated stage/process assertions **true**.

No 99-suite, 256-row smoke or 100k matrix was run. HQ can rerun the actual Linux CI at the returned cut; no flaky retry was claimed.
