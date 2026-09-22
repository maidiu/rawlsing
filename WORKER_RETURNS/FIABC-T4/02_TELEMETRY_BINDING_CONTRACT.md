# FIABC-T4 — Telemetry Binding Contract

Contract seam:

`T3 process envelope → FIABC-T4 live bridge → accepted I06B TelemetryLedger`

## Identity grain

Every live cell is bound to:

- source id;
- canonical source SHA-256;
- candidate A/B/C;
- frozen workload identity;
- frozen authority-set identity.

Every observation additionally carries:

- phase id;
- candidate-process token;
- cost class;
- lifecycle action id where applicable;
- evidence reference.

Cross-cell attribution fails closed.

## Cost classes

- **C0** — candidate-neutral upstream production: source/authority/workload/oracle freeze; excluded.
- **C1** — candidate access to common input; chargeable where executed.
- **C2** — candidate physical realization; chargeable.
- **C3** — common logical-output execution within the candidate process; chargeable.
- **C4** — court administration; excluded.

## CPU

The T3 main candidate process supplies cumulative process-self counters at the cell boundary.

T4 additionally records replay/recovery subprocesses as CHILD process envelopes.

Candidate total CPU is:

`Σ(non-overlapping process-self CPU deltas for MAIN + each CHILD exactly once)`

Per-phase CPU remains a separate series derived from consecutive main-process cumulative snapshots. It is not re-added to the candidate total.

Duplicate child tokens fail closed.

## RSS

Each process envelope is candidate-local.

Candidate peak RSS is:

`max(process-local peak RSS observations)`

Never sum.

## Wall

Candidate total wall is the outer T3 cell envelope from candidate-process start boundary to lawful process stop.

Lifecycle and phase timers remain separately named observations.

## I/O

Only explicit READ/WRITE events may support I/O accounting.

Endpoint file or directory size is not I/O.

The current live bridge records source READ events but deliberately does **not** seal the canonical I/O aggregate until all candidate-local write/rewrite sites are event-covered. Until then `bytes_read`, `bytes_written`, and `bytes_rewritten` remain typed null rather than misleading partial totals or synthetic zero.

## Scratch

The accepted I06B high-water API is live.

An endpoint scratch size is not a peak. Until full event-level scratch mutation observation exists, the canonical peak fields remain typed null.

## Cold / warm

Cold and warm remain distinct metric names. Warm values cannot overwrite cold slots.

Cold lifecycle admission additionally requires the T3 absent-state receipt to show no candidate-owned warm state at process start.

## Missing values

Uncaptured or unreached telemetry is represented by an explicit metric state with `value: null`.

Missing is never numeric zero.

## Immutability

Canonical metric slots, phase CPU observations, process envelopes, lifecycle receipts, and the final telemetry receipt are write-once.

A resume may re-read an identical stage journal entry. A changed observation for an already-written stage fails closed.

## Semantic non-interference

The telemetry layer receives semantic state from the existing court.

It emits:

`semantic_state_was_modified_by_telemetry = false`

and has no path to upgrade/downgrade semantic disposition.
