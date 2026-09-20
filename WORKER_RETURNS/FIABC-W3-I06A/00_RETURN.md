# FIABC-W3-I06A — Process Isolation / Execution Envelope

Status: COMPLETE__IMPLEMENTED__TESTS_AUTHORED_NOT_EXECUTED

Repository: maidiu/rawlsing

Branch: agent/rabochii-premain-fiabc-w3-i06a-process-isolation-r1

Base: agent/vozhd-premain-fiabc-wave2-fanin-r1

Base SHA: 56697a27e94eb9603dfa412a15ab8f1feb819b0c

Production implementation tip before return-package commit: dc5b8a249b197bacf5c94d9f2c14043ebee67e53

Return path: WORKER_RETURNS/FIABC-W3-I06A/

## Holding

The former IMP11 process-isolation burden is implemented without changing semantic authority, source meaning, candidate identities, Candidate-C law, comparison-terminal law, parity truth, or metric arithmetic.

The P2X backend seam is wrapped by a process-isolation adapter. The long-lived court driver may import only that neutral adapter. The actual candidate backend is imported after the candidate-local boundary inside a fresh child process assigned to exactly one source × candidate cell.

A candidate process may never be reused for another candidate. Candidate-local module/session/RSS history therefore dies with the cell process. Same-cell process retention is fail-closed unless an explicit lifecycle transition authorization is supplied by the lifecycle owner.

## Implemented guarantees

- Fresh OS process per executing source × candidate cell.
- Exact parent envelope start timestamp is taken before the first candidate-specific owner marker or process spawn.
- Actual candidate backend import and candidate owner initialization are forbidden in the parent before that boundary.
- Child handshake records PID/PPID, pre/post-backend-import process resource observations, and the exact cell attribution environment.
- Module-global _SESSIONS is required to be empty at child start when exposed by the backend.
- A child refuses any stage whose source/candidate does not equal its sealed cell.
- At stop, any exposed session key belonging to another cell fails closed.
- Candidate transition, candidate-local failure, source/court stop, or court terminal stops and waits for the child before another cell can begin.
- Candidate roots are exact work_root/cells/<source>/<candidate> roots; root, scratch, durable, log and receipt roots may not be symlinks or escape the cell.
- Cold is defined only as absence of candidate-owned accelerating state. It does not claim a globally flushed OS page cache.
- Default cold start fails if scratch or durable candidate state already exists.
- Pre-existing same-cell warm/durable state requires explicit same-cell resume authorization plus the matching process-envelope owner marker.
- Keeping one process alive across same-cell stages requires an explicit lifecycle transition token. No implicit “same candidate means warm is allowed” rule exists.
- Candidate-neutral source/authority/workload/oracle freeze is consumed through one immutable freeze receipt outside candidate roots. It is classified as C0 upstream capital and is not regenerated per candidate by this worker.
- Descendant processes inherit exact source/candidate/cell/freeze environment attribution, so I06B can bind child resource observations to one cell without guessing parentage.

## Scope conservation

This worker does not calculate candidate CPU totals, phase arithmetic, memory aggregation, I/O byte arithmetic, throughput, or preserved-work credit. Those remain I06B.

This worker does not decide deletion/regeneration/invalidation/stale/corrupt/interruption actions or which lifecycle transitions are entitled to preserve warm state. It exposes exact process-retention and same-cell-resume hooks for I06C and fails closed when those hooks are absent.

This worker does not produce or alter the independent semantic parity oracle. It consumes only an opaque candidate-neutral freeze receipt whose identity and source SHA are checked before a candidate begins.

## Production files changed

Added:
- rawlsing_next/ee_p2x_candidate_process_envelope.py
- rawlsing_next/ee_p2x_process_isolated_backend.py

No existing production file was modified.

## Tests added

Added:
- rawlsing_next/tests/fiabc_i06a_process_probe_backend.py
- rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py

The hostile suite contains nine focused tests covering cross-candidate session/process/RSS separation, live cross-candidate reuse rejection, explicit warm-transition authorization, scratch/durable isolation, cold-state rejection, explicit same-cell resume, pre-start candidate backend import detection, candidate-neutral freeze reuse, and descendant child-process attribution.

## Test execution

NOT_RUN.

Reason: this commission was constrained to GitHub/browser repository tools only. No Python/OS execution surface was used, and no test result is fabricated. The deterministic local command is recorded in 03_TEST_AND_EXECUTION_PROTOCOL.md.

No measured P2X execution was run.

## Integration hooks

I06B consumes raw process-boundary observations from measured_payload.process_envelope, including process identity, start/stop monotonic boundaries, process-local raw resource snapshots, and descendant attribution. I06B remains responsible for lawful metric definitions and arithmetic.

I06C supplies/validates exact warm-state lifecycle permissions through the same-cell process-retention tokens and explicit same-cell resume set. I06A does not invent those permissions.

The integrated court driver must select:

    --backend-module rawlsing_next.ee_p2x_process_isolated_backend

and must provide the pre-frozen candidate-neutral receipt path before candidate execution.

## Terminal

FIABC_W3_I06A_PROCESS_ISOLATION_AND_EXECUTION_ENVELOPE_IMPLEMENTED__READY_FOR_FANIN
