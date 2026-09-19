# FIABC-W2-B03 — Equal-Work Accounting / Measurement Court

Status: `COMPLETE__ACCOUNTING_CONSTITUTION_PROVED`

Worker: `FIABC-W2-B03`

Branch: `agent/rabochii-premain-fiabc-w2-b03-equal-work-accounting-r1`

Base SHA: `dfdae1dfcef5e3061094935312c3db2cc0fde2f0`

Return path: `WORKER_RETURNS/FIABC-W2-B03/`

## Holding

The Wave-1 B03 accounting defects can be closed at constitutional/specification grain without changing semantic ownership or inventing a new execution architecture.

The equal-work court compares **candidate-owned physical realization / persistence / regeneration / reuse** over one invariant source-local logical workload. The accounting boundary therefore separates four things that the current P2X backend partially mixes:

1. immutable candidate-neutral authority/oracle production;
2. candidate-local access to those frozen inputs;
3. candidate-owned physical realization and the exact I03/I05/lifecycle work it enables;
4. court administration and evidence serialization.

Only (2) and (3), plus the actual common logical output production performed through each candidate, belong in candidate cost. Candidate-neutral authority/oracle production is prepared once and reused; post-stop court administration is excluded.

## Exact candidate-local boundary

For each `source × candidate` cell, the comparison unit is source-local. No WVS/LiTS pooling is permitted.

The candidate cost envelope begins only after exact source identity, Lock1/Lock2 authority identities, fixed workload identities, and candidate-neutral parity-oracle material have been verified/materialized and frozen. It begins with the first candidate-specific process/action needed to realize, open, reconstruct, regenerate, or access that candidate's physical path for the frozen workload. It ends after the last required candidate lifecycle/recovery/replay/audit operation and final governed output identity are complete, before court-level verifier/fan-in/commit/report serialization.

A fresh candidate process is required per cell for candidate-local memory accounting. No previous candidate `_SESSIONS`, imported candidate owner objects, candidate scratch, or candidate durable state may survive into the next candidate. Within a candidate, lawful warm state may persist only where the frozen workload explicitly calls for warm/repeated work.

## Preserved work adjudication

- Immutable common authority, source-identity law, Lock1/Lock2 workload authority, runtime/query/discovery authority, and independently frozen parity-oracle production are candidate-neutral upstream capital. They are reused and are not re-produced merely for symmetry. If a candidate execution itself reads/deserializes/attaches those frozen objects, that candidate-local access is counted.
- The current LiTS-A P2X first-build receipt may be reused only for telemetry it directly observed and only if the final verifier confirms the receipt satisfies this constitution's exact manifest/runtime/fresh-state/isolation bindings. Missing fields may not be inferred from it.
- The preserved LiTS-B cacheless C11 receipt proves semantic/identity work but explicitly captured no numeric telemetry. It receives **no numeric cost credit** and no zero substitute. Any future numeric B construction cost requires a separately authorized measured execution; this return does not authorize one.
- The older pre-P2/R10L A build remains calibration-only because Lock1 expressly says it is not a dispositive P2 first-build sample.
- Authorized-stop receipts remain valid stop evidence; every unreached metric is typed null, never numeric zero.

## Metric constitution

The metric ledger in `02_METRIC_DEFINITION_LEDGER.csv` fixes the accounting semantics. Key non-negotiable points are:

- CPU is candidate-total and per-phase, accumulated from non-overlapping process/child-process deltas; a later stage may not overwrite earlier CPU.
- RSS is candidate-process-local. Darwin `ru_maxrss` is bytes under the accepted R8B law, but process lifetime must be one candidate cell, not the whole A→B→C court.
- observed I/O bytes are event counters from actual candidate-local reads/writes/rewrites; final directory size is a state-size metric, not an I/O substitute;
- scratch peaks are high-water observations, not one end-of-stage directory sample;
- cold/warm metrics are separate immutable fields. Canonical cold I03 is the first candidate I03 invocation from the frozen candidate-owned cold state that is compared against the pre-frozen independent oracle. If verification has already warmed that exact query/session, the cold metric is invalid until the frozen cold state is re-established;
- invalidation/rebuild/recovery metrics require actual governed lifecycle actions. Formula-assigned recomputation units, law-string hashes, or generic scratch-file creation do not count as observed work;
- candidate-neutral semantic/output truth remains common even where a candidate pays the physical work needed to realize or access it.

## Current implementation implication

`rawlsing_next/ee_p2x_darwin_stage_backend.py@617c9c9426db12a3c0f7fea6b68a582c10759553` does not satisfy this constitution. The exact defects and required mechanical changes are enumerated in `04_CURRENT_METRIC_DEFECT_TO_REQUIRED_CHANGE.csv`.

This finding is deliberately narrower than a P2X execution judgment:

- it does **not** repair Candidate C reachability/portability;
- it does **not** define B02's independent semantic oracle contents;
- it does **not** authorize measured P2X resume;
- it does **not** claim any current source×candidate cell already has a constitution-complete terminal vector.

What is proved here is the **accounting law HQ can mechanize and test** without moving semantic ownership.

## Terminal

`FIABC_W2_B03_EQUAL_WORK_ACCOUNTING_CONSTITUTION_PROVED`
