# FIABC-W3-I06B — Test and Execution Protocol

## Browser commission execution status

No local command was executed.

No measured P2X was run.

No numeric runtime result is claimed by this return.

The committed tests are deterministic pure accounting tests and do not require source datasets.

## Deterministic syntax/import check

Run from repository root on the integrated tree:

```bash
python3 -m py_compile \
  rawlsing_next/fiabc_telemetry_semantics.py \
  tests/test_fiabc_telemetry_semantics.py
```

Acceptance:

- exit code 0;
- no syntax/import error.

## Deterministic hostile unit suite

```bash
python3 -m unittest discover \
  -s tests \
  -p 'test_fiabc_telemetry_semantics.py' \
  -v
```

Acceptance:

- all committed I06B tests pass;
- no test invokes measured P2X;
- no test requires LiTS/WVS source bytes;
- no test fabricates OS measurement output.

## Hostile acceptance matrix

| Requirement | Test |
|---|---|
| same immutable metric twice rejected | `test_same_immutable_metric_twice_is_rejected` |
| later cold-I03 cannot overwrite earlier cold | `test_later_cold_work_cannot_overwrite_earlier_cold_metric` |
| missing telemetry null not zero | `test_missing_telemetry_is_typed_null_never_zero` |
| cumulative CPU not phase delta | `test_cumulative_cpu_counter_is_converted_to_phase_delta` |
| nested measurement no double count | `test_nested_phase_cpu_cannot_double_count_candidate_total` |
| process-global RSS rejected | `test_process_global_rss_is_rejected` |
| endpoint size not bytes written | `test_endpoint_directory_size_cannot_masquerade_as_bytes_written` |
| hardcoded rewrite zero rejected | `test_hardcoded_zero_rewrite_cannot_satisfy_observed_accounting` |
| endpoint scratch size not peak | `test_scratch_endpoint_cannot_masquerade_as_peak` |
| A metric cannot become B metric | `test_candidate_a_metric_cannot_be_attributed_to_b` |
| missing candidate/source/phase identity fails | `test_metric_without_exact_phase_identity_fails_closed` |
| common upstream excluded; candidate access counted | `test_candidate_neutral_production_excluded_but_candidate_access_counted` |
| definitions stable A/B/C | `test_metric_definition_hash_is_identical_for_a_b_c` |
| child CPU once; RSS max not sum | `test_child_cpu_is_added_once_and_rss_uses_max_not_sum` |
| cumulative self+children CPU scope rejected | `test_cpu_scope_with_children_already_included_is_rejected` |
| fresh replay child CPU exact lifecycle bind | `test_fresh_replay_child_cpu_binds_exact_lifecycle_action` |
| cold/warm distinct | `test_cold_and_warm_are_distinct_immutable_fields` |
| telemetry cannot upgrade semantic failure | `test_telemetry_does_not_upgrade_semantic_failure` |

## Integrated I06A validation — deferred

After I06A is fanned in, the integrated test must prove with actual process receipts that:

1. each source×candidate cell supplies one exact MAIN envelope;
2. every required child supplies a unique CHILD envelope;
3. every envelope uses `cpu_scope=PROCESS_SELF_ONLY`;
4. every RSS sample uses `rss_scope=CANDIDATE_PROCESS_LOCAL`;
5. child process tokens/parents belong to the same exact cell;
6. candidate-total CPU equals main SELF delta plus each admitted child SELF delta exactly once;
7. candidate peak RSS equals max process-local peak, not historical/global RSS.

This is OS-level validation and is intentionally not fabricated here.

## Integrated I06C validation — deferred

After I06C is fanned in:

1. bind each governed lifecycle action through `LifecycleActionReceipt`;
2. record lifecycle wall/counter metrics only with that action ID;
3. route rewrite events with exact lifecycle action and rewrite lineage;
4. bind fresh replay child CPU through `seal_fresh_process_replay_cpu`;
5. leave unreached or uncaptured lifecycle metrics typed null;
6. do not infer lifecycle work from law strings, formulas, endpoint state, or receipt-writing time.

## Integrated backend hook order

For each exact source×candidate cell:

1. construct one `TelemetryLedger(CellIdentity(...))`;
2. emit exact candidate-local read/write/source/scratch observations during execution;
3. emit phase CPU start/stop counter observations as phases finish;
4. bind I06C lifecycle receipts before lifecycle-scoped metrics/events;
5. submit final I06A main/child process envelopes;
6. explicitly seal source-event, I/O, scratch, and process accounting only where observation is complete;
7. request the telemetry receipt with the semantic disposition supplied by the semantic court;
8. do not let telemetry receipt state alter semantic/parity/qualification state.

## Prohibited execution

This return does not authorize:

- measured P2X;
- Candidate-C scope redesign;
- lifecycle-policy invention;
- process-isolation-policy invention;
- semantic/parity/empirical adjudication;
- replacing missing observations with zero or estimates.
