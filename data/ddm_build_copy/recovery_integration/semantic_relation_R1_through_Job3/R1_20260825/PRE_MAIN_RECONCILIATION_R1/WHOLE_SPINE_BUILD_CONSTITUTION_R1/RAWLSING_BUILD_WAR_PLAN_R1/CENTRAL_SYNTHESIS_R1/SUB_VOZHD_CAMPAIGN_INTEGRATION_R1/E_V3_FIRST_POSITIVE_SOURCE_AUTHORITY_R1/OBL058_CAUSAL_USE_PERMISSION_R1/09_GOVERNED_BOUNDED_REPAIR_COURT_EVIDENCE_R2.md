# OBL058 — CAUSAL_USE_PERMISSION — GOVERNED BOUNDED REPAIR COURT EVIDENCE R2

Status: `GREEN_PRODUCER_REPAIR_COURT__NOT_INDEPENDENT_REVIEW__NOT_ADOPTED`

## Exact frozen repaired candidate

- candidate freeze: `f735c85393280557284b3a309cafc0847fb48aec`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0`
- candidate definition: `08_FROZEN_REPAIRED_CANDIDATE_AUTHORITY_R2.md`

The frozen candidate was not modified after `f735c85393280557284b3a309cafc0847fb48aec`. Court tests, wrapper, and court-spec plumbing are later evidence commits only.

## Governed execution

- workflow: `Rabochii Governed Bounded Court`
- execution-only PR: `#275`
- PR state after evidence capture: `CLOSED_UNMERGED`
- governed run: `34189967948`
- governed job: `101945838419`
- exact evidence execution SHA: `4f8b37358ef721a6a259b7795f2483231aea0f27`
- PR synthetic merge SHA: `dbec3355fe3593479fa2b6ce352ea84b1d7e8ba5`
- Python: `3.12.14` / `CPython`
- determinism mode: `EXACT`
- court-spec SHA-256: `290504f0963e95e323bc79a55801b5781cb7c126eb6e60cd11a2bf1740549726`

## Results

- protocol self-tests: `20 passed in 0.11s`
- governed court-spec validation: `PASS`
- bounded repair court: `26 passed in 0.08s`
- court receipt result: `PASS`
- receipt exit code: `0`
- receipt semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`

## Artifact

- artifact name: `rabochii-court-receipt-34189967948`
- artifact ID: `10041842927`
- artifact size: `617 bytes`
- artifact ZIP SHA-256: `9326196e16ed503fdcdae6e501a03d3be706d5f5f05c517e4351e0791d969f03`
- artifact expiry reported by GitHub: `2026-12-07T05:15:57Z`

Exact receipt payload recorded from the artifact:

```json
{"determinism_mode":"EXACT","elapsed_seconds":0.304518,"env":{"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONHASHSEED":"0"},"evidence_execution_sha":"4f8b37358ef721a6a259b7795f2483231aea0f27","exit_code":0,"implementation":"CPython","pr_synthetic_merge_sha":"dbec3355fe3593479fa2b6ce352ea84b1d7e8ba5","python":"3.12.14","result":"PASS","schema_id":"RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0","semantic_candidate_sha":"f735c85393280557284b3a309cafc0847fb48aec","spec_sha256":"290504f0963e95e323bc79a55801b5781cb7c126eb6e60cd11a2bf1740549726","tests":["rawlsing_next/tests/test_subv_e_obl058_causal_use_permission_bounded_repair_r2_court.py"]}
```

## What the 26 repair checks cover

The producer repair court verifies that the repaired candidate:

- permits the one registered noncurrent-synthetic positive basis on its exact scope;
- carries revised authority/schema identity and explicit basis-binding proof fields;
- denies arbitrary unregistered basis IDs;
- rejects whitespace basis IDs;
- removes caller-supplied permission booleans and caller-supplied basis-kind selection;
- rejects plain/reconstructed mappings as source-issued receipts;
- rejects rewritten-and-rehashed denial-to-permit constructions;
- exposes read-only issued receipt mappings;
- prevents reuse of the registered basis across actor, world, subject, time, and transition changes;
- rejects project-current-shaped actor, world, subject, time, and transition identifiers;
- rejects the exact current first-canary subject identifier on the bounded synthetic surface;
- rejects a direct `PROJECT_CURRENT` fixture label;
- rejects wrong expected scope;
- has no public basis-registration API.

## Non-evidence preliminary run

Run `34189908642` / job `101945667377` failed before executing the bounded repair tests because the first court spec pointed directly to the lane-local test file, while the execution protocol requires a `rawlsing_next/tests/*.py` court entry. Protocol self-tests were green (`20 passed`); court-spec validation correctly failed with:

`tests[0] must be a rawlsing_next/tests/*.py path`

No candidate change was made. The plumbing was repaired by adding an approved wrapper and rebinding the court spec, producing the green governed run above. The failed preliminary run is not the evidence execution.

## Boundary

This green court is producer-side repair verification only. It is not the commissioned fresh distinct independent review and must not be counted as one.

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`HQ_ADOPTION_CLAIMED = NO`

The repaired candidate remains frozen and awaits a separate independent reviewer.
