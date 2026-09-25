# FIABC T5 JOINED FAILURE-SEMANTICS REPAIR — R1

You are **FIABC T5 JOINED FAILURE-SEMANTICS REPAIR — R1**.

Repository:

`maidiu/rawlsing`

Branch:

`agent/rabochii-fiabc-t5-joined-failure-semantics-repair-r1`

Exact base:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

This base is the current protected execution head. Your branch is an isolated repair branch. Do NOT mutate the protected execution branch itself.

## SOURCE / EXECUTION LAW

SOURCE-FREE / CANDIDATE-FREE repair only.

Do not open, hash, decode, inspect, or infer from raw LiTS/WVS files.
Do not launch Candidate A/B/C.
Do not run measured P2X.
Do not modify frozen candidate-owner implementations.
Do not modify T2 manifest unless you prove the manifest itself is defective and stop for HQ adjudication.
Do not mutate prior measured roots.

## PROVED BLOCKER

Worker C proved at exact protected head:

`BLOCKED__PREEXISTING_JOINED_T5_FAILURE_PATH_DEFECT`

Return branch:

`agent/rabochii-fiabc-split-r2-c-t5-process-failure-parity-r1`

Return head:

`640724ef289a45953d8b25b96717bd4bad07616f`

Read:

- `WORKER_RETURNS/FIABC-SPLIT-R2-C-T5-PROCESS-FAILURE-PARITY-R1/00_RETURN.md`
- `12_PROCESS_LIFECYCLE_DIFFERENTIAL.json`
- `13_T5_SOURCE_LOCAL_DEPENDENCY_AND_FAILURE_PATHS.json`
- `15_SOURCE_FREE_FORENSIC_HARNESS.json`

Exact defect:

If A or B has a candidate-local failure before or at S05, there is no
`fiabc_t5_candidate_observation.json` for that candidate.

When C later passes S05, `admit_post_i05_oracle_match()` unconditionally loads A/B/C observations for the same source to construct the three-way gate. Missing A/B observation raises `LiveTerminalControlError`.

That exception occurs after `backend.run_stage()`, outside the driver's typed candidate/common-blocker catch, producing an untyped orchestration failure.

This defect exists in the canonical joined runner and both sources.

## MISSION

Repair the JOINED runner's complete candidate-failure semantics, not merely the observed C/S05 stack trace.

First derive the intended failure law from:

- current six-cell execution manifest;
- T5 current court contract;
- candidate-local failure continuation edges;
- T4/T5 contracts;
- final S17 verifier requirements.

Do not fabricate missing successful observations for failed candidates.

### F1 — C/S05 same-source three-way gate

Define and implement a lawful typed outcome when C itself passes S05 but A and/or B lacks a passing S05 observation because of an already-recorded candidate-local failure.

Requirements:

- C's own independent oracle match may be retained only if current law supports it;
- missing failed-candidate observations may never be synthesized;
- three-way A/B/C parity may never be claimed PASS without three actual passing observations;
- no untyped exception;
- later-stage continuation must follow an explicit governed disposition.

Determine whether the correct disposition is:
- candidate-local;
- common-source blocker;
- court blocker;
- or another already-governed typed state.

Do not invent a new semantic class unless existing law is genuinely insufficient; if insufficient, stop and return the exact law gap.

### F2 — FINAL S17 FAILURE PATH

Audit what happens after ANY candidate-local failure anywhere in A/B/C.

A failed candidate generally lacks a passing S16 cell terminal. The current S17 final verifier expects all six passing terminal bundles.

Prove and repair the joined court so candidate-local failure cannot later become an untyped missing-file/orchestration crash at S17.

The court must terminate with a typed governed non-PASS disposition/evidence state, never:
- fabricate a PASS cell;
- fabricate a terminal bundle;
- silently skip failure evidence;
- crash on missing files.

### F3 — ALL FAILURE POSITIONS / BOTH SOURCES

Source-free actual-object tests must cover both LiTS and WVS:

- A failure S01
- A failure before S05
- A failure at S05
- A failure after S05
- A failure S16
- B same positions
- C same positions
- common-source blocker early/middle/late
- common-court blocker early/middle/late

At minimum distinguish failures:
- before candidate observation exists;
- after observation/oracle match exists;
- after cell terminal exists.

### F4 — PROCESS LIFECYCLE

Preserve the already-proved good ProcessIsolationController law.

Do not weaken:
- fresh process per source×candidate cell;
- no cross-cell warm state;
- authorized same-cell transitions;
- stop on non-PASS;
- S15 fresh replay child law.

### F5 — T5 SOURCE LOCALITY

Preserve:
- A/B individual matches source-local;
- C three-way dependency same-source only;
- no cross-source live dependency before S17.

### F6 — TYPED EXCEPTION SURFACE

Audit every T4/T5 post-backend hook called after `backend.run_stage()`.

No expected governed failure condition may escape as an untyped orchestration exception merely because the hook is outside the backend catch.

Do not broadly catch programming errors. Add narrow typed handling for governed conditions only.

### F7 — S17 PASS PATH NO DRIFT

All-six-PASS behavior must remain byte/semantic compatible with current T5 final verification.

No weakening of:
- independent oracle requirement;
- telemetry completeness;
- six-cell terminal completeness;
- no self-replay-as-truth law.

### F8 — SPLIT COMPATIBILITY

The repaired semantics must be reusable by the alternate split runner through the same protected helper interfaces. Do not add split-specific behavior into protected T5 logic.

## QUALIFICATION

Source-free qualification only.

Must prove:
- raw source opens 0
- source hash passes 0
- decoder calls 0
- candidate process launches 0
- candidate outputs 0
- measured execution false

Use actual protected StateMachine/T5 objects where possible.

Bank exact implementation head separately from later return/docs commits.

## OWNERSHIP

You may modify only the minimum protected-control surfaces required, expected to be among:

- `rawlsing_next/fiabc_live_terminal_control.py`
- `rawlsing_next/ee_p2x_darwin_court_driver.py`
- directly relevant source-free tests

Do not modify candidate owner code or physical decoder/carrier semantics.

## RETURN

Return under:

`WORKER_RETURNS/FIABC-T5-JOINED-FAILURE-SEMANTICS-REPAIR-R1/`

Required:
- 00_RETURN.md
- RETURN.json
- failure-semantics matrix
- C/S05 three-way adjudication
- S17 non-PASS terminal adjudication
- post-backend typed-exception audit
- source-free test output
- protected-base no-unrelated-drift table
- exact implementation head

Success terminal:

`PASS__FIABC_T5_JOINED_FAILURE_SEMANTICS_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED`

If law is insufficient or any failure path remains untyped:

`BLOCKED__FIABC_T5_JOINED_FAILURE_SEMANTICS_REMAINS`
