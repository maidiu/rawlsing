# FIABC-W3-I06B — Metric Instrumentation / Telemetry Semantics

Status: `IMPLEMENTED__READY_FOR_FANIN`

Worker: `FIABC-W3-I06B`

Branch: `agent/rabochii-premain-fiabc-w3-i06b-telemetry-semantics-r1`

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

Return path: `WORKER_RETURNS/FIABC-W3-I06B/`

## Holding

IMP11's measurement/telemetry-semantics burden is implemented as a dedicated candidate-bound telemetry component:

`rawlsing_next/fiabc_telemetry_semantics.py`

The component mechanizes the Wave-2 B03 accounting constitution without reopening process-isolation policy or lifecycle policy.

The implemented law is:

- canonical metric slots are immutable at their defined grain;
- every admitted observation carries exact source, source SHA, candidate, phase, process, cost-class, and optional lifecycle-action provenance;
- candidate-total CPU is derived from exact `PROCESS_SELF_ONLY` process counter deltas and includes child-process CPU exactly once;
- phase CPU is independently retained as counter delta evidence and is never summed into candidate-total CPU;
- candidate RSS accepts only `CANDIDATE_PROCESS_LOCAL` envelopes and candidate peak is the max over admitted main/child process peaks;
- observed I/O is an event ledger; `bytes_read`, `bytes_written`, and `bytes_rewritten` cannot be directly assigned;
- C0 common-upstream production and C4 court administration are explicitly recorded as excluded rather than silently charged;
- C1 candidate-local access to frozen common material is chargeable;
- scratch peaks are high-water values derived from state-change observations, never endpoint-size aliases;
- cold/warm canonical metrics are distinct candidate-grain write-once slots;
- missing/unreached telemetry is typed null and never coerced to numeric zero;
- lifecycle-grain metrics require an exact bound I06C `LifecycleActionReceipt`;
- process totals require exact I06A `ProcessEnvelopeReceipt` data; the telemetry layer does not choose process launch/isolation policy;
- the metric-definition manifest and hash are candidate-independent and therefore stable across A/B/C;
- telemetry receipts echo semantic disposition unchanged and explicitly record that telemetry did not modify it.

## Legacy defect closure

The component blocks the specific current-backend failure modes identified by B03:

- last-write CPU overwrite;
- cumulative CPU mistaken for phase delta;
- nested timing double count;
- process-global `ru_maxrss` reuse across candidates;
- endpoint directory size used as I/O;
- hardcoded rewrite zero;
- endpoint scratch sample mislabeled as peak;
- cold metric overwrite;
- cross-candidate attribution;
- metric records lacking exact candidate/source/phase identity;
- candidate-neutral producer work charged to candidates;
- candidate-local shared-input access hidden as free work.

The Wave-2 fan-in base does not contain `rawlsing_next/ee_p2x_darwin_stage_backend.py`; therefore this worker does not fabricate an edit to an absent production file. Instead it provides the dedicated integration surface that I06A/I06C and final fan-in must call.

## Tests

Hostile deterministic tests are committed at:

`tests/test_fiabc_telemetry_semantics.py`

They cover every hostile case required by the commission plus child CPU scope and semantic-boundary checks.

No test command was executed in this browser-only commission. No measured P2X was run.

See `04_TEST_AND_EXECUTION_PROTOCOL.md` for deterministic commands intended for integrated/local qualification.

## Semantic boundary

Telemetry remains execution-cost evidence only.

A telemetry receipt:

- does not create semantic authority;
- does not establish empirical truth;
- does not establish parity truth;
- does not qualify a candidate;
- cannot upgrade a semantic failure.

## Terminal

`FIABC_W3_I06B_TELEMETRY_SEMANTICS_IMPLEMENTED__READY_FOR_FANIN`
