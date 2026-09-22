# FIABC-T3 — Process Envelope Binding

## Atomic execution laboratory

The process key is:

`source_id × candidate_id`.

One child process belongs to exactly one such key for its entire lifetime.

A different source or candidate cannot enter that process.

## Parent/child split

The long-lived court driver may import only:

`rawlsing_next.ee_p2x_process_isolated_backend`.

That neutral adapter imports the process-envelope controller, not the actual candidate implementation.

The actual backend named by `RAWLSING_EE_P2X_INNER_BACKEND` is imported only after:

1. the frozen upstream receipt has validated;
2. the exact cell root has validated;
3. cold/explicit-resume state has validated;
4. the parent candidate boundary timestamp has been taken;
5. the exact cell owner marker has been written;
6. a fresh child process has started.

The default inner backend remains:

`rawlsing_next.ee_p2x_darwin_stage_backend`.

## Exact child attribution

The child inherits and verifies:

- `RAWLSING_EE_P2X_CELL_SOURCE`;
- `RAWLSING_EE_P2X_CELL_CANDIDATE`;
- `RAWLSING_EE_P2X_CELL_KEY`;
- `RAWLSING_EE_P2X_UPSTREAM_FREEZE_SHA256`.

The child handshake records:

- PID / PPID;
- pre-backend-import timestamp;
- post-backend-import timestamp;
- process-local CPU/RSS snapshots;
- session-registry-empty assertion;
- exact attribution environment.

Descendants inherit the same attribution unless a later governed subprocess explicitly replaces it.

## State non-crossing law

The following may not cross source×candidate boundaries:

- candidate backend module state;
- candidate owner instances;
- `_SESSIONS`;
- heap/RSS history;
- scratch roots;
- durable roots;
- candidate logs/receipts;
- same-cell warm state.

A live A process cannot become B. A LiTS process cannot become WVS. Foreign session keys at process stop fail closed.

## Root law

The only candidate root is:

`work_root/cells/<source>/<candidate>`.

Its `scratch`, `durable`, `logs`, and `receipts` children must resolve under that exact root and may not be symlinks.

The candidate-neutral freeze receipt must live outside `work_root/cells/`.

## Cold and same-cell retention

Default start mode is:

`COLD_REQUIRED`.

This means no candidate-owned accelerating state. It does not claim a globally flushed host OS page cache.

Pre-existing same-cell state requires:

- exact matching process-owner marker;
- explicit same-cell resume authorization;
- later lifecycle/accounting proof that retention is lawful.

Keeping one process alive across stages in the same cell also requires an exact transition token:

`FROM_STAGE>TO_STAGE`.

T3 enforces the hook but does not mint lifecycle permissions. That remains the later lifecycle/accounting layer's burden.

## Oracle interaction

The process envelope treats source/authority/workload/oracle freeze as shared upstream capital.

It does not build the oracle, materialize source semantics, or mount oracle-created caches into a candidate.

At every candidate stage the production backend binds the already-frozen source-local oracle identity. Candidate-local S03 cannot rewrite or replace it.

## Direct backend bypass

The T3 driver rejects measured/run execution unless the selected backend is exactly:

`rawlsing_next.ee_p2x_process_isolated_backend`.

This closes the prior path where the long-lived parent could import and execute the candidate backend directly.
