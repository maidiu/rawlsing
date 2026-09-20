# FIABC-W3-I06B — Implementation Diff Inventory

## Added production component

### `rawlsing_next/fiabc_telemetry_semantics.py`

New dedicated telemetry/accounting component implementing:

- `CellIdentity`: exact source/source-SHA/candidate/workload/authority cell key.
- `ObservationContext`: exact source/candidate/phase/process/cost-class provenance for every observation.
- `ProcessEnvelopeReceipt`: I06A integration contract using cumulative start/stop process counters, explicit `PROCESS_SELF_ONLY` CPU scope, and `CANDIDATE_PROCESS_LOCAL` RSS scope.
- `LifecycleActionReceipt`: I06C integration contract for lifecycle-scoped metrics.
- `TelemetryLedger`: one source×candidate immutable metric ledger.
- candidate-grain and lifecycle-grain write-once metric slots;
- process-envelope CPU/RSS/wall aggregation;
- per-phase CPU counter-delta recording;
- child-process CPU inclusion exactly once;
- lifecycle-bound fresh-process replay CPU materialization;
- observed source event counters;
- observed I/O event accounting with rewrite lineage;
- excluded C0/C4 event visibility;
- included C1/C2/C3 event charging;
- scratch high-water accounting;
- typed-null missing/unavailable metric states;
- stable metric-definition manifest + SHA-256;
- telemetry receipt preserving the input semantic disposition unchanged.

## Added hostile tests

### `tests/test_fiabc_telemetry_semantics.py`

Deterministic standard-library `unittest` coverage:

1. duplicate immutable metric rejected;
2. later cold-I03 cannot overwrite canonical cold field;
3. missing metric stays typed null;
4. cumulative CPU counters become phase deltas;
5. nested phase CPU cannot inflate candidate-total CPU;
6. process-global RSS rejected;
7. endpoint directory size cannot populate `bytes_written`;
8. hardcoded `bytes_rewritten=0` rejected;
9. scratch endpoint cannot masquerade as scratch peak;
10. Candidate-A observation cannot enter Candidate-B/A-mismatched cell;
11. missing exact phase identity fails closed;
12. C0 common production excluded while C1 common-input access is counted;
13. metric-definition hash identical across A/B/C;
14. child CPU included once and RSS uses max, not sum;
15. child/self+children cumulative CPU scope rejected;
16. fresh-replay child CPU requires exact lifecycle binding;
17. cold and warm canonical fields remain distinct;
18. successful telemetry does not upgrade semantic failure.

## Existing production files intentionally not modified

The assigned base `56697a27e94eb9603dfa412a15ab8f1feb819b0c` does not contain the audited historical/current P2X backend path:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

That backend was inspected at `617c9c9426db12a3c0f7fea6b68a582c10759553` because B03 identifies it as the implementation whose metric arithmetic is noncompliant. This worker does not transplant or reconstruct that backend onto the Wave-2 fan-in base. Integration belongs to fan-in with I06A/I06C and whichever current execution carrier HQ admits.

## No ownership drift

No source, semantic, routing, parity, empirical, candidate, process-policy, or lifecycle-policy ownership was changed.

No measured P2X state was created.
