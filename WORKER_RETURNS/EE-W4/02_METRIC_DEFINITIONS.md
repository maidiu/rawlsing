# EE-W4 metric definitions

These definitions implement the accepted C09 parity-first measurement law without making a physical comparison. All metrics are recorded per `(candidate_id, universe_id, operation_id, phase)`; the harness never drops `universe_id` when aggregating. Missing measurements remain `null`/typed incomplete and are never silently converted to zero.

| Metric | Definition |
|---|---|
| `wall_ns` | Monotonic elapsed nanoseconds around the exact declared operation/action. |
| `cpu_user_ns`, `cpu_system_ns` | Child-process `wait4` user/system CPU converted to ns. |
| `peak_rss_bytes` | Linux `ru_maxrss × 1024`; native value/unit is retained. |
| `scratch_bytes_before/after` | Logical regular-file bytes under that candidate's isolated scratch root immediately before/after the step. |
| `peak_scratch_bytes_observed` | Maximum sampled logical scratch bytes while the candidate child is live, including boundary samples. |
| `peak_scratch_file_count_observed` | Maximum sampled regular-file count under isolated scratch. |
| `max_single_temp_object_bytes_observed` | Largest sampled regular scratch object. |
| `durable_bytes_before/after` | Logical regular-file bytes under that candidate's isolated durable root. |
| `durable_bytes_created_delta` | `after - before`; retained even when negative after cleanup. |
| `source_open_count` | Candidate-reported exact open count for the declared operation. Required for measurement-complete eligible candidate actions. |
| `source_decode_count` | Candidate-reported exact decode-pass count. Required for measurement-complete eligible candidate actions. |
| `bytes_read`, `bytes_written` | Candidate-reported values where observable; otherwise missing, not zero. |
| `temporary_spill_bytes_reported` | Candidate-reported spill accounting where observable; separate from sampled scratch. |
| `cache_index_bytes_created` | Candidate-reported persistent/regenerable cache/index creation. |
| `rewritten_bytes` | Candidate-reported bytes rewritten for rebuild/selective invalidation. |
| `semantic_oracle_status` | Exact SHA-256 equality against the frozen workload oracle. It gates performance eligibility. |
| `identity_oracle_status` | Exact equality for any workload-frozen deterministic/release/replay identities. |

The workload itself names cold, warm, replay, delete/rebuild, source-invalidation and semantic/routing-authority-invalidation steps in exact order. EE-W4 does not synthesize repeats because doing so would let the harness redefine EE-W1's equal-work denominator. It supports the required `cold`, `warm_1`, `warm_2`, `warm_5` schedule directly when those steps are frozen in the incoming profile.

No weighted or opaque composite score exists in EE-W4. A cell with failed semantic parity is performance-ineligible regardless of measured speed. An authority-limited cell is reported as typed ineligible/unresolved and is not counted as a candidate failure.
