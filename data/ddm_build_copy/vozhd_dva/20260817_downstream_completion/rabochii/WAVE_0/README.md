# Rabochii Wave 0 — Downstream Reconnaissance and Safe Infrastructure

**Wave:** R0  
**Coordinator:** Vozhd Dva  
**Purpose:** make downstream requirements concrete enough to launch semantic implementation without serial-stage blindness or another open-ended architecture cycle.

## Wave law

All five assignments are bounded. Workers inspect actual `main` code and contracts, answer the specific cross-stage questions in their cell, and implement only the isolated work explicitly authorized there. They do not redesign neighboring stages to make local work convenient.

The five workers run concurrently. Their outputs are **inputs to Vozhd Dva adjudication**, not independent architecture authority.

## Branch and PR protocol

The launch base for all five workers will be the Wave-0 integration branch created by Vozhd Dva after these packets are committed to `main`.

Worker branch names:

- `agent/vozhd-dva-r0-01-v553-v554`
- `agent/vozhd-dva-r0-02-v555`
- `agent/vozhd-dva-r0-03-v556-attractor`
- `agent/vozhd-dva-r0-04-runtime-contract`
- `agent/vozhd-dva-r0-05-vertical-harness`

Target integration branch:

- `agent/vozhd-dva-wave0-integration`

Each worker must open a **draft PR** against that integration branch. No worker merges their own PR.

## Required report location

Every worker writes two report files in **its own cell on its worker branch**, alongside any code changes:

- `RESULT.md` — concise human-readable account for Vozhd Dva review.
- `RESULT.json` — machine-readable terminal report using `../REPORT_FORMAT.json`.

Cell paths:

- `rabochii/WAVE_0/R0_01_V553_V554/`
- `rabochii/WAVE_0/R0_02_V555/`
- `rabochii/WAVE_0/R0_03_V556_ATTRACTOR/`
- `rabochii/WAVE_0/R0_04_RUNTIME_CONTRACT/`
- `rabochii/WAVE_0/R0_05_VERTICAL_HARNESS/`

Paths are relative to this control-room root:
`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/`.

## Terminal statuses

Use exactly one:

- `COMPLETE`
- `COMPLETE_WITH_FINDINGS`
- `PARTIAL_AWAITING_CROSS_HOOK`
- `BLOCKED_BY_CANONICAL_DEFECT`
- `FAILED`

`COMPLETE` means the assigned scope is fully answered and any authorized implementation is tested. It does **not** mean Vozhd Dva has accepted the work.

## Cross-cutting discoveries

If a worker discovers a necessary change outside its write domain:

1. preserve evidence;
2. describe the exact producer/consumer mismatch;
3. complete all lawful in-domain work;
4. record it under `cross_hooks` in `RESULT.json`;
5. do not edit the neighboring domain;
6. return `PARTIAL_AWAITING_CROSS_HOOK` if the missing hook prevents terminal completion.

## Review path

Vozhd Dva reviews each worker in:

`reviews/WAVE_0/<worker_id>_REVIEW.md`

and synchronizes accepted cross-stage facts in:

`integration/WAVE_0_INTAKE_LEDGER.md`.

Worker self-report and Vozhd Dva acceptance are deliberately separate states.
