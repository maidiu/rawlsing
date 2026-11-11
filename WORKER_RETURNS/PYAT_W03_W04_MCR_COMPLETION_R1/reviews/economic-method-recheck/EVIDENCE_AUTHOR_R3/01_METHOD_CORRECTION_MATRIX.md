# ECON-M1..M5 correction matrix

| ID | Status | Exact code/behavior | Test/evidence |
|---|---|---|---|
| ECON-M1 | CORRECTED | `_worker` passes no policy root for `cold`/`cells-and-hash`; `full-matrix` uses policy. `cold` metric is max of normal streaming cold and first-consumer stage peaks; canonical persistence only full-matrix. | `test_cli_cold_small_writes_machine_readable_json`; 64-row parity current cold derived files 0; full-matrix cold coverage in raw |
| ECON-M2 | CORRECTED | `_RssSampler` samples current RSS at 50 ms; `_stage` reports entry/exit current, sampled stage peak, and separate process `ru_maxrss`; aliases are explicitly combined, not zero. | `test_stage_peak_tracks_post_highwater_allocation`; raw stage keys |
| ECON-M3 | CORRECTED | Parent `_run_child` monitors `ps` RSS from process start, kills above `--cap-bytes`; child profile starts only after Popen/monitor; `cap_enforced` added by parent. | `test_small_cap_refuses_over_limit_without_host_stress`; `cap_falsifier.json` |
| ECON-M4 | CORRECTED | `_baseline_section` null-safe; baseline source head/rows/profiles/repetitions/host/schema checked; gate thresholds and regressions; `--acceptance-gate` returns 2 on failure. | `test_acceptance_gate_requires_baseline_and_is_nonzero`; `test_acceptance_gate_threshold_and_identity_falsifiers`; 64 baseline/current |
| ECON-M5 | CORRECTED | Source opens explicit N/A; actual derived/canonical hits/writes; 3 fresh-process warm restarts on one persisted root; actual amortization; explicit retention. | `test_full_matrix_three_fresh_warm_restarts_share_persisted_root`; `warm_restarts_3.json` |

## Deliberate boundaries

- `projection`, `objectconstruction`, `canonicalhash`, `i02validation`, `seal`, `compact` are labelled combined inside the normal current build; no invented split stages.
- `decode` is `NOT_APPLICABLE__EXACT_PHYSICAL_CELL_STREAM__NO_SOURCE_DECODE`, not a fake measured cost.
- Canonical `ParquetC11Carrier` and governed derived `c11-events-*.parquet` are separate namespaces/stages; canonical file counts are not cache hits.
- `repeat` warm comparison is to the protected **cold no-acceleration** normal path, not in-process warm or canonical reopen.
