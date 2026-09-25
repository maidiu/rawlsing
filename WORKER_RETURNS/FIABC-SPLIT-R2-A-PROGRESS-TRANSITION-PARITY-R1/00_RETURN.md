# FIABC SPLIT R2 — Worker A return

Terminal:

`PASS__SPLIT_R2_A_PROGRESS_TRANSITION_PARITY__READY_FOR_FANIN`

## Provenance

- Worker branch: `agent/rabochii-fiabc-split-r2-a-progress-transition-parity-r1`
- Exact common base: `e1b82095c83dd15a64b409dba0e4ae7d4f4460c6`
- Commission: `64affcb34c1ec2c7823a9fc9238b3e4cf7fb9c62`
- Protected execution: `3d8f2ad62600b6777dcb23a28404a067502e77a0` — unchanged
- Dedicated fan-in: `agent/vozhd-fiabc-split-r2-fanin-r1`
- Fan-in commission: `a11d3f6d264ff6d0cc6c3e4eadfd2791baa07966`
- **Implementation head:** `36315c423f824be0308d7995d405a1139a08299c`

## Closure

The RUN5 LiTS failure is a cursor/scope mismatch in the inherited full-court progress plan: protected `ManifestProgressPlan` starts its governed address universe at `LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD`, while a fresh split LiTS root must reconstruct mechanical `LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY`. Emitting that S00 through the inherited plan therefore throws before candidate execution.

Worker A closes the class rather than suppressing the string. The split driver retains the protected `ProgressReporter` but installs a 51-row selected-source plan (3 cells, 44 executable rows) containing neither the other source nor COURT/S17. LiTS/A/S00 is now materialized during source-local preflight, with no progress emission, matching joined `bind_initial_manifest_prefix()`.

The exact protected manifest contains 102 cell-stage rows. Joined all-PASS behavior is:

- preflight prefix: LiTS/A/S00 only;
- source traversal: 50 LiTS rows;
- source traversal: 50 WVS rows;
- then COURT/S17.

The only manifest row not visited by the joined all-PASS pass graph is `WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY`, because WVS/B/S16 points directly to WVS/C/S01. Split terminal completeness still needs C/S00. Worker A therefore admits exactly that one extra split materialization and fail-closes unless it remains `DONE__PRESERVE`, source-free, non-physical, and non-backend-executable. Candidate backend address/order remains identical: 44 READY rows per source.

Common-source blocker propagation now retains the protected global next edge for telemetry/adjudication while the source-local runner still stops at the source cut; it never dispatches the other source or S17.

## Qualification

A dedicated source-free test was added at:

`rawlsing_next/tests/test_fiabc_split_r2_a_progress_transition_parity.py`

It uses the actual protected StateMachine, StageSpec, StageLedger, ProgressReporter, candidate-stop, and source-stop mechanics when supplied the exact protected checkout. It covers all-pass; A/B/C failure at S01/S05/S16; common-source blockers early/middle/late; common-court blockers early/middle/late; prefix placement; exact progress universes; and source/S17 exclusion.

This connector session could not execute a local protected checkout, so I do **not** claim that Python test as executed here. Fan-in must execute it before integrated qualification. The checked-in exact-manifest static artifacts are complete and source-free.

## Source-free telemetry

Raw source opens: **0**. Source hash passes: **0**. Decoder calls: **0**. Candidate launches: **0**. Candidate outputs: **0**. Measured execution: **false**.
