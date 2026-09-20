# FIABC-W3-I06A — Test and Execution Protocol

## Browser-worker execution status

No tests were executed in this commission.

Reason: the worker was restricted to GitHub/browser repository tools. There is no Python/OS execution surface in that constraint, and the tests deliberately exercise real subprocess identity, process-local RSS history, inherited environment, filesystem isolation, and process termination. No result is fabricated.

No measured P2X was run.

## Focused hostile test command

From the repository root on a Python environment capable of subprocess execution:

    python -m pytest -q rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py

Expected test count from this worker: 9.

The command is deterministic and does not require the real LiTS/WVS source files. It uses only the hostile probe backend.

## Hostile coverage

### Candidate A state cannot appear in B

test_candidate_a_session_process_and_rss_history_cannot_enter_candidate_b

The test creates an A session, allocates A heap memory, then terminalizes A and opens B. It requires A stages to share one PID only where explicitly authorized, B to have a different PID, B session registry to start empty, B envelope to contain no prior-candidate RSS field, and both stop receipts to state process-local RUSAGE_SELF scope.

### Live cross-candidate process reuse is impossible

test_live_candidate_process_cannot_be_reused_for_another_candidate

A remains alive for an explicitly authorized same-cell transition. An attempted B stage through that A process must raise CrossCandidateReuseError.

### Warm state requires explicit lifecycle permission

test_same_cell_process_retention_requires_explicit_lifecycle_authorization

Even A→A process retention fails if no exact warm transition token exists.

### Scratch/durable state does not cross candidates

test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails

A writes scratch state. B's root cannot see it. A foreign candidate owner marker in C's root fails closed.

### Cold means candidate-owned cold

test_cold_run_fails_if_candidate_owned_warm_state_already_exists

Pre-existing candidate durable state makes the default cold run fail. No global OS-cache claim is made.

### Same-candidate retained state requires explicit resume

test_same_candidate_warm_state_requires_explicit_resume_hook

A matching prior cell marker plus explicit resume authorization admits same-cell retained state and records that the start is not cold.

### Candidate-specific initialization cannot be moved before start

test_candidate_specific_backend_import_before_measurement_start_is_detected

The test pre-imports the inner backend in the parent. Candidate start must fail with PreStartContaminationError.

### Candidate-neutral upstream capital can be shared

test_candidate_neutral_freeze_is_shared_without_becoming_candidate_state

A and B bind the same freeze receipt SHA and C0 classification while the receipt remains outside all candidate roots.

### Child process attribution is exact

test_descendant_child_process_is_attributable_to_exactly_one_candidate_cell

A backend-spawned descendant must inherit the exact source, candidate, cell key, and freeze identity, and its PPID must be the sealed candidate process.

## Integrated pre-measurement wiring

After fan-in supplies the current driver/backend plus I06B/I06C and the independent upstream freeze receipt, set only the exact governed permissions.

Illustrative wiring shape:

    export RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT=/absolute/path/to/frozen-candidate-neutral-receipt.json
    export RAWLSING_EE_P2X_INNER_BACKEND=rawlsing_next.ee_p2x_darwin_stage_backend
    export RAWLSING_EE_P2X_EXPLICIT_RESUME_CELLS='SOURCE/CANDIDATE,...'
    export RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS='FROM_STAGE>TO_STAGE,...'

    python rawlsing_next/ee_p2x_darwin_court_driver.py \
      --preflight \
      --continuation-map /absolute/path/to/frozen-continuation-map.json \
      --work-root /absolute/path/to/new-court-work-root \
      --repo-root /absolute/path/to/rawlsing \
      --lits-path /absolute/path/to/frozen-lits-source \
      --wvs-path /absolute/path/to/frozen-wvs-source

For an executable non-measured qualification run, the driver must additionally select:

    --backend-module rawlsing_next.ee_p2x_process_isolated_backend

The exact --run/--resume command and lifecycle allow-lists must come from the integrated fan-in qualification packet. This worker does not manufacture them from the old court state.

## I06B verification expectations

I06B should reject an accounting receipt when:
- cell PID attribution is missing;
- process start/stop hooks are missing for a terminal cell;
- a child resource observation cannot be bound to one cell;
- a candidate's process-local resource basis is replaced by the long-lived parent driver's RSS history;
- arithmetic infers a metric that I06A emitted only as raw observation.

## I06C verification expectations

I06C should reject lifecycle reuse when:
- SAME_CELL_RESUME_EXPLICIT is present without lifecycle authority;
- a warm process-retention token is not in its exact governed lifecycle;
- a cold cell contains candidate-owned state;
- an ACTIVE interrupted marker is silently treated as clean;
- lifecycle recovery attempts to move state between candidates.

## Measured P2X prohibition

Do not run measured P2X from this branch.

This return is ready for fan-in and premeasurement hostile qualification only.
