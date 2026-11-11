# FIABC FINAL LOCAL LAUNCH PACK — R1
## Integrated static hostile audit

Integrated head audited: `858b3b52674044e020b85f8697c5f2c61ce15371`

This audit is source-free. No LiTS/WVS carrier was opened, no Candidate A/B/C process was started, no measured P2X ran, and no GitHub Actions workflow was triggered.

## Integrated seam verdict

| Surface | Holding | Evidence in integrated code |
|---|---|---|
| 35-metric telemetry registry | PASS | `fiabc_telemetry_semantics.METRIC_DEFINITIONS` = 35; backend `METRICS` = 35; final telemetry producer manifest = 35. |
| I/O/scratch/fresh-child accounting | PASS structurally | Final telemetry closure remains present in backend/live-accounting/telemetry blobs. |
| Six-cell topology | PASS | Current manifest order is LiTS-I/A,B,C then WVS7/A,B,C; all six current capabilities are `CURRENT_EXECUTABLE`. |
| WVS7/C sixth cell | PASS | Current loader requires C S01/S02 READY on WVS7 and S12/S13 are exact zero-accelerator N/A skips. Historical WVS7/C failure is rejected as current law. |
| LiTS-I/A current entry | PASS | Current entry is `LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD`; S01 requires source + physical-host measurement. No current preserved-S01 numeric credit. |
| Manifest-derived failure ordering | PASS with authority defect below | Backend `_current_manifest_cell_order()` loads the current six-cell manifest and `_cell()` indexes failures from it; no five-cell hard-code is used for sequence order. |
| Progress vs stdout | PASS | `ProgressReporter` emits human/progress telemetry to stderr; the CLI machine result remains the final JSON printed to stdout. |
| Process isolation | PASS | Driver refuses direct candidate backend and requires exactly `rawlsing_next.ee_p2x_process_isolated_backend`; process envelope remains fresh-cell isolated. |
| Candidate-local stop sequencing | PASS structurally | Candidate-local failure advances according to the manifest and does not suppress later lawful cells; after all cell work, S17 success verifier is not run if candidate-local failures exist. |
| Candidate A typed N/A | PASS | Final telemetry emits `delete_rebuild_wall_ns = NOT_APPLICABLE_BY_FROZEN_COURT` for A; terminal completeness has the same special expectation. |
| Terminal completeness vs telemetry | **BLOCK** | Telemetry/backend registry is 35; `FROZEN_DISPOSITIVE_METRICS` is 29. Six live metrics are absent from S16/S17 completeness law. |
| WVS oracle current constitution | **BLOCK** | Runtime package/T2/T5 use successor Lock2, but `pre553_independent_parity_oracle.py` still exports predecessor Lock2/replay/DiscoveryAuthority and T5 `_court_constitution()` consumes those predecessor constants. |
| Frozen WVS oracle live schema | **BLOCK** | Accepted R1M oracle is `FIABC_LM2_R1M_FRESH_WVS_ORACLE@1.0.0`; live T5 requires `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0` and calls `verify_frozen_oracle()`. No exact adapter/launcher is committed. |
| Current failure authority metadata | **BLOCK** | Backend `_cell()` still reads `WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json`, whose Lock2/DiscoveryAuthority are predecessor `8e5842... / 245916...`, while current WVS court uses successor `5e2a53... / 3aee360...`. |
| LiTS current oracle materialization | **BLOCK: missing producer** | HQ boundary proves 50 candidates/77 roles and accepted product/replay, but explicitly lacks current constituent-I03 refs, current closure identity, and current observation-shaped exact-ref manifest. `build_lits_i_oracle()` is a library function only; no current local neutral producer CLI exists. |
| T3 frozen-upstream receipt | **BLOCK: missing producer** | `load_frozen_upstream_receipt()` validates/consumes `RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`; no committed final producer/launcher builds the two-source receipt. |
| Current-head I07 inputs | **BLOCK: missing producer** | `fiabc_succession_preflight.py` has an evaluator CLI, but no committed producer emits the real current-head frozen succession manifest plus P10 lifecycle/failure-scope context. |
| Driver execution branch binding | Requires exact launch setup | Driver/current manifest still require branch `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`. Remote tip `617c9c9...` is an ancestor of integrated `858b3b5...`, so this can be satisfied by a lawful fast-forward of the existing execution branch to the eventual final launch head; do not create a substitute branch or rebase. |
| Variable-width narrowing | NON-BLOCKING | Full-width decode is accepted by commission for this run. |

## Exact 29 -> 35 completeness delta

The six telemetry metrics missing from `fiabc_terminal_completeness.FROZEN_DISPOSITIVE_METRICS` are:

- `source_reread_count`
- `source_release_invalidation_wall_ns`
- `source_release_invalidation_bytes_rewritten`
- `semantic_authority_invalidation_wall_ns`
- `semantic_authority_invalidation_bytes_rewritten`
- `fresh_process_replay_cpu_ns`

Required lifecycle bindings already exist in telemetry law:

- source invalidation wall/rewrite -> `S10_SOURCE_RELEASE_INVALIDATION`
- semantic invalidation wall/rewrite -> `S11_SEMANTIC_AUTHORITY_INVALIDATION`
- fresh replay CPU -> `S15_FRESH_PROCESS_REPLAY`
- `source_reread_count` is candidate-cell source-event accounting, not a lifecycle action.

The live-accounting finalizer independently refuses `MEASUREMENT_NOT_CAPTURED`, so this mismatch does not authorize missing telemetry. It does mean the independent S16/S17 completeness constitution is not definition-identical to the frozen 35-metric surface.

## Exact WVS successor split

Current runtime/T2/T5 successor court:

- DiscoveryAuthority: `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`
- Lock2: `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`
- Lock2 replay: `9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a`
- accepted R1M oracle identity: `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`
- accepted R1M truth payload: `eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405`

Live independent-oracle module still freezes predecessor:

- DiscoveryAuthority: `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`
- Lock2: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`
- Lock2 replay: `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`

The successor constants declared in `fiabc_live_terminal_control.py` are not used by `_court_constitution()`; that function consumes the predecessor constants imported from the oracle module.

## Import-cycle / stale-code holding

No active top-level import cycle was found between driver, isolated backend, process envelope, backend, and T5 terminal control. Backend imports driver/T5 only inside stage functions where needed. The process-isolated adapter remains the only driver-admitted execution backend.

There is historical dead/compatibility code with stale assumptions (including old preserved-WVS-C helpers and old normalized verifier files), but the current manifest loader rejects historical Candidate-C failure dispositions. The launch-critical stale dependencies are the active oracle constants and active `_cell()` frozen-expectation read described above.

## T5 preservation-anchor note

`WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json` retains pre-final-closure T4 preservation anchors. Some are explicitly historical (`pre_t5_driver_blob`, `pre_t5_backend_blob`), so they are not treated here as a standalone launch blocker. A final repaired launch seal should nevertheless bind the actual post-repair head through the current-head succession manifest, as `run_live_succession_preflight()` requires.

## Conclusion

The integrated topology is substantially correct, but **measured launch is blocked before Candidate A**. None of these blockers requires variable pruning or semantic redesign.
