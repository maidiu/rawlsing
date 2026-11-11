# Exact diagnosis and obligation mapping

## CI failure

Exact failing node:

`rawlsing_next/tests/test_bench_w03_w04_physical.py::test_stage_peak_tracks_post_highwater_allocation`

Observed Linux values:

```text
process_ru_maxrss_after_bytes = 290,238,464
stage_peak_current_rss_bytes  = 290,365,440
difference                     = 126,976 bytes
```

Both are normalized byte values. The former is `getrusage(RUSAGE_SELF).ru_maxrss` (Linux KiB -> bytes); the latter is a sampled current RSS from `ps -o rss=`. They are distinct counters and no cross-counter ordering is guaranteed. The old test asserted an unrelated ordering.

## Obligation preserved

Required: actual stage current RSS distinguishes a later allocation after an earlier process high-water; process cumulative high-water is separate and never falsely labelled stage peak.

New assertions:

```text
value length == 8 MiB
stage_peak_current_rss_bytes >= stage_entry_current_rss_bytes
stage_peak_current_rss_bytes - stage_entry_current_rss_bytes >= 4 MiB
process_ru_maxrss_after_bytes >= process_ru_maxrss_before_bytes
rss_peak_bytes == process_ru_maxrss_after_bytes
```

Deterministic counter-falsifier:

```text
_rss_peak_bytes fixed at 123456
=> process_ru_maxrss_before/after = 123456
=> stage_peak_current_rss_bytes remains independently observed (> 123456)
=> old cross-counter ordering is false
```

This is not a tolerance or mirror; it fails if `_stage` aliases the cumulative counter into the stage metric.
