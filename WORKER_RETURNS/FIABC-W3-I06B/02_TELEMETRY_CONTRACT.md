# FIABC-W3-I06B — Telemetry Contract

Contract: `FIABC_W3_I06B_TELEMETRY_SEMANTICS@1.0.0`

Authority basis: FIABC-W2-B03 measurement constitution and metric-definition ledger, as adopted by Wave-2 HQ for IMP11.

## 1. Atomic cell

Every telemetry ledger is bound at construction to exactly one:

`(source_id, source_sha256, candidate_id, frozen_workload_id, frozen_authority_set)`

LiTS-I and WVS7 remain separate. Candidate identity is one of A/B/C.

No observation is accepted unless its source, source SHA, candidate, phase, and process token are exact and non-empty.

## 2. Metric states

Every absent or nonnumeric metric uses one of B03's exact states:

- `MEASURED`
- `NOT_APPLICABLE_BY_FROZEN_COURT`
- `NOT_REACHED_AUTHORIZED_STOP`
- `MEASUREMENT_NOT_CAPTURED`
- `INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH`

Only `MEASURED` may carry a numeric value.

Every other state carries `value = null`.

The default receipt representation for an uncaptured field is `MEASUREMENT_NOT_CAPTURED` with null value. Numeric zero is never used as a missing-value encoding.

## 3. Immutability and grain

The metric manifest fixes each field's grain.

Candidate-grain fields have one canonical slot per exact source×candidate cell even if multiple later phases attempt to emit the same field.

Lifecycle-grain fields have one slot per exact source×candidate×lifecycle-action identity.

Any second write to the same slot raises `TelemetryContractError`.

This is the mechanism that prevents:

- S07 or later work from overwriting canonical `cold_i03_latency_ns`;
- the last timing helper from overwriting candidate CPU;
- later receipt synthesis from replacing earlier observations.

## 4. I06A process-envelope interface

I06B does not choose process-isolation policy. It consumes an exact I06A receipt with:

- exact cell identity;
- phase ID;
- process token;
- PID;
- role `MAIN` or `CHILD`;
- parent process token for children;
- `cpu_scope = PROCESS_SELF_ONLY`;
- `rss_scope = CANDIDATE_PROCESS_LOCAL`;
- cumulative user CPU start/stop counters;
- cumulative system CPU start/stop counters;
- outer wall start/stop counters;
- candidate-process-local peak RSS;
- evidence ref.

### Candidate-total CPU

I06B computes:

`sum(main process SELF delta + each required child process SELF delta)`

for user and system CPU separately.

A `SELF_PLUS_CHILDREN`, `RUSAGE_CHILDREN`-precombined, or other cumulative scope is rejected because it can double count child CPU.

### Per-phase CPU

I06B separately accepts phase start/stop cumulative counters and stores the resulting phase delta.

Phase CPU is evidence; it is not summed to derive candidate-total CPU.

Therefore nested phase timers may overlap without inflating candidate total.

### RSS

Only `CANDIDATE_PROCESS_LOCAL` RSS is admissible.

Candidate peak RSS is:

`max(main peak, required child-process peaks)`

not the sum and not a whole-court/process-history peak.

## 5. I06C lifecycle interface

I06B does not decide which lifecycle action is required.

Lifecycle-scoped metrics must bind an I06C `LifecycleActionReceipt` containing:

- exact cell identity;
- action ID;
- action type;
- phase ID;
- process token;
- outcome;
- evidence ref.

A lifecycle metric whose action ID is absent, or whose phase/process differs from the bound receipt, fails closed.

Fresh-process replay CPU has a dedicated hook that materializes its metric from the exact I06A child process envelope while requiring the exact I06C lifecycle action.

## 6. Observed I/O accounting

`bytes_read`, `bytes_written`, and `bytes_rewritten` are derived-only fields.

No caller may assign them numerically.

The event hook records:

- READ or WRITE;
- exact byte count;
- logical object identity;
- optional rewrite lineage;
- exact cell/phase/process/lifecycle provenance;
- cost class;
- evidence ref.

After the event stream is explicitly sealed:

- `bytes_read` = included READ event bytes;
- `bytes_written` = included WRITE event bytes;
- `bytes_rewritten` = included WRITE bytes carrying exact rewrite lineage.

Endpoint directory size is never accepted as event accounting.

A hardcoded zero is never accepted as a substitute for a completed rewrite-event stream. Zero becomes lawful only when a completed event stream positively contains zero qualifying rewrite events.

## 7. Cost-class treatment

The event ledger preserves the B03 noncollapse:

`SEMANTIC_OWNER != COST_OWNER`

Cost classes:

- C0 `COMMON_UPSTREAM_PRODUCTION__EXCLUDED_FROM_CANDIDATE_COST`
- C1 `CANDIDATE_ACCESS_TO_COMMON_INPUT__INCLUDED`
- C2 `CANDIDATE_PHYSICAL_REALIZATION__INCLUDED`
- C3 `COMMON_LOGICAL_OUTPUT_EXECUTION__INCLUDED`
- C4 `COURT_ADMINISTRATION__EXCLUDED_FROM_CANDIDATE_COST`

I/O events in C0/C4 remain visible in the receipt but are marked `charged_to_candidate = false`.

Candidate-local reads/deserialization/access to frozen common material must be emitted as C1 and are charged.

Thus neutral production is not silently charged and candidate-local shared-input access is not silently made free.

## 8. Scratch high-water accounting

Scratch accounting is state-transition based.

Hooks record exact candidate-owned scratch-object current sizes and removals throughout the envelope.

I06B tracks:

- simultaneous scratch bytes high-water;
- simultaneous scratch file-count high-water.

The canonical peak fields can be sealed only after at least one high-water observation.

A one-time endpoint directory sample cannot populate a peak metric.

## 9. Cold and warm fields

`cold_i03_latency_ns` and `warm_i03_latency_ns` are separate immutable candidate-grain fields.

Duration hooks require:

- exact phase/process/cell provenance;
- monotonic start and stop;
- an exact cold/warm state predicate or lifecycle evidence ref.

A later cold-like phase cannot replace the canonical cold field.

I06B does not define the cold-state predicate; it records the predicate supplied by the governed execution/lifecycle layer.

## 10. Stable A/B/C metric definition

The module emits one deterministic metric-definition manifest and:

`METRIC_DEFINITION_HASH = SHA256(canonical metric-definition manifest)`

The manifest is independent of candidate identity.

A/B/C therefore use the same field names, units, kinds, and grains even where measured values or lawful typed states differ.

## 11. Semantic boundary

`TelemetryLedger.receipt(candidate_semantic_state=...)` requires semantic disposition as an input.

The receipt returns that value unchanged and sets:

`semantic_state_was_modified_by_telemetry = false`

The telemetry layer contains no path that converts cost evidence into semantic PASS, empirical truth, parity truth, or candidate qualification.

## 12. Fan-in obligations

I06A must call the process-envelope interface with candidate-local process evidence.

I06C must bind exact lifecycle receipts before lifecycle-grain metrics are recorded.

The integrated execution backend must route actual read/write/rewrite and scratch state-change events through these hooks rather than assigning terminal metrics from endpoint state.

No architecture or experimental-design decision is made by this contract.
