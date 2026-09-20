# FIABC-W3-I06A — Process Isolation Contract

## 1. Atomic laboratory

The process-isolation key is:

source_id × candidate_id

A process may belong to exactly one such key for its entire lifetime.

The cell process is the containment boundary for candidate backend module state, imported candidate owner objects, backend session registries such as _SESSIONS, candidate-local heap/RSS history, candidate-specific environment, candidate-local scratch/durable roots, and same-cell warm state explicitly allowed by lifecycle law.

A different candidate never enters that process.

## 2. Candidate-neutral upstream capital

I06A accepts one immutable upstream freeze receipt with schema:

RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@1.0.0

Required fields:
- candidate_neutral: true
- frozen_before_candidate_execution: true
- source_identities
- authority_identities
- workload_identities
- oracle_identity

Candidate-specific top-level fields are forbidden. The receipt itself must live outside work_root/cells/.

For each non-court cell, the receipt's source SHA must equal the cell context's frozen source SHA.

This object is classified:

C0_SHARED_UPSTREAM__NOT_CANDIDATE_PRODUCTION_COST

I06A does not rebuild it for A, B, or C. Actual candidate-local access to the frozen capital remains available for I06B to classify as C1 where observed.

## 3. Start boundary

Before the start boundary I06A performs only candidate-neutral/precondition work: freeze-receipt validation, source-identity binding check, root topology and pre-existing-state inspection, and parent contamination checks.

The exact parent candidate boundary begins at parent_envelope_start_monotonic_ns, taken immediately before the first candidate-specific process-owner marker and before Popen.

After that boundary the candidate-specific owner marker is written, cell attribution environment is created, fresh process is spawned, actual inner backend is imported, and any candidate owner initialization performed by that backend is candidate-local.

I06A rejects a start if the actual inner backend was already imported in the parent or if an accepted-owner module with the P2X candidate-owner naming surface is already initialized there.

## 4. Child import boundary

The fresh child validates four inherited attribution values before importing the inner backend:

- RAWLSING_EE_P2X_CELL_SOURCE
- RAWLSING_EE_P2X_CELL_CANDIDATE
- RAWLSING_EE_P2X_CELL_KEY
- RAWLSING_EE_P2X_UPSTREAM_FREEZE_SHA256

The child records resource observations before and after backend import.

If the backend exposes _SESSIONS, it must be empty at this point.

Thus candidate-specific initialization cannot be silently moved before the lawful candidate envelope.

## 5. Root isolation

For cell S/C, the only valid root is:

work_root/cells/S/C

The root and its scratch, durable, logs, and receipts children must already exist as directories, may not be symlinks, and must resolve under the exact cell root.

A process-owner marker binds the root to one exact cell. A foreign marker fails closed. An interrupted ACTIVE marker is not silently resumed.

## 6. Cold state

COLD_REQUIRED is the default.

It means no candidate-owned accelerating scratch or durable state exists at the candidate boundary.

It does not mean the operating system page cache is globally flushed.

A default-cold cell with pre-existing scratch or durable files fails with ColdStateViolation.

## 7. Explicit same-cell resume

Pre-existing candidate-owned state is allowed only when all are true:

- the exact SOURCE/CANDIDATE key is in the explicit resume set;
- the cell root contains a matching prior process-envelope owner marker;
- that marker is not ACTIVE;
- no other candidate identity is present.

This is only a process/lifecycle hook. I06C remains responsible for proving the retained state is lawful to reuse.

## 8. In-process warm retention

Process survival from one stage to another inside the same cell is itself treated as possible warm-state retention.

Therefore same-cell retention is forbidden by default.

A transition may keep the process alive only when its exact token is present:

FROM_STAGE_ID>TO_STAGE_ID

I06C owns which tokens are lawful. I06A merely enforces the allow-list. Missing authorization raises WarmStatePolicyError and aborts the cell process rather than silently carrying state forward.

## 9. Cross-candidate session and RSS isolation

The controller permits at most one active cell process.

If a stage for B arrives while the active process belongs to A, execution is rejected.

Before a new cell begins, the prior cell process must have stopped or been fail-closed/aborted.

Because each candidate gets a fresh process:
- _SESSIONS cannot carry A objects into B;
- arbitrary module globals from A cannot carry into B;
- A heap allocations cannot set B's RUSAGE_SELF.ru_maxrss;
- parent candidate owner objects are forbidden;
- B may lawfully report lower RSS than A.

At child stop, any exposed _SESSIONS key for a foreign cell is an error.

## 10. Stop boundary

The child emits child_process_stop_monotonic_ns immediately before its clean process terminal.

The parent waits for process exit and then records parent_envelope_stop_monotonic_ns.

No later candidate may start before that stop completes.

Stage/cell receipt and HQ accounting logic outside this envelope are not reclassified by I06A. I06B/I06C must use the boundary hooks according to their own governing contracts.

## 11. Child-process attribution

All descendants inherit the cell attribution environment unless a later governed subprocess explicitly changes it.

I06A records cell process PID/PPID, stage process PID, freeze receipt SHA, exact environment attribution, and process-local raw resource snapshots.

A descendant therefore has an unambiguous parent cell. I06B may consume that identity for child CPU/RSS accounting without I06A deciding the arithmetic.

## 12. Receipt interface for I06B

Every isolated backend result adds:

measured_payload.process_envelope

Important fields:
- source
- candidate
- cell_key
- candidate_neutral_freeze.receipt_sha256
- candidate_local_boundary.parent_envelope_start_monotonic_ns
- cold_state_observation
- process.pid
- process.ppid
- process.child_pre_backend_import_monotonic_ns
- process.child_backend_import_complete_monotonic_ns
- process.pre_backend_import_resource
- process.post_backend_import_resource
- stage_process_pid
- resource_after_stage
- lifecycle_process_retention
- stop.child_process_stop_monotonic_ns when the cell stops
- stop.resource_at_stop
- stop.parent_envelope_stop_monotonic_ns

These are raw observations/hooks, not final metrics.

## 13. Interface for I06C

I06C supplies the lifecycle decisions that I06A intentionally does not own:

- exact same-cell resume permissions;
- exact warm process-retention transitions;
- deletion/regeneration state preparation;
- stale/corrupt/invalidation/interruption actions and recovery disposition.

Adapter inputs:
- RAWLSING_EE_P2X_EXPLICIT_RESUME_CELLS
- RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS

No lifecycle permission is inferred from candidate label, source label, prior success, or presence of state.

## 14. Driver integration

The existing P2X driver/backend contract is preserved.

Integrated invocation must choose:

    --backend-module rawlsing_next.ee_p2x_process_isolated_backend

The adapter then wraps the actual inner backend inside the sealed process. By default that inner module is rawlsing_next.ee_p2x_darwin_stage_backend.

This is an execution-envelope change only. It does not alter candidate semantics or owner identity.
