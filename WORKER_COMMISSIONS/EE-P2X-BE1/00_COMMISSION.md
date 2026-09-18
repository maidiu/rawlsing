# EE-P2X-BE1 — PRODUCTION DARWIN STAGE BACKEND IMPLEMENTATION

Status: `COMMISSIONED__BROWSER_IMPLEMENTATION_AND_QUALIFICATION_ONLY__NO_EMPIRICAL_CARRIER_ACCESS`

Repository:

`maidiu/rawlsing`

Exact branch:

`agent/rabochii-prev3-ee-p2x-be1-production-stage-backend-r1`

Exact base:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

This worker exists because the qualified Darwin orchestration driver requires a production implementation of:

`RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0`

but the current P2X tree contains only test doubles and no production backend module.

## Controlling sealed authority

Resolve canonical HQ through `HQ_HANDOFF/LATEST.json` before work.

Expected commissioning checkpoint:

`20260918T0455-0400`

Do not rely on that expectation if `LATEST.json` has advanced.

Underlying measured-court branch is:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

at commissioning base:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

## Mandatory existing interfaces

Consume, do not redesign:

- `rawlsing_next/ee_p2x_darwin_court_driver.py`
- `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json`
- `WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json`
- `WORKER_RETURNS/EE-P2X/10_LOCAL_COURT_RECEIPT_CONTRACT.json`
- `WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`
- `WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py`
- `WORKER_RETURNS/EE-P2X/LOCAL_EXECUTOR_README.md`
- adopted P2R1 seam `rawlsing_next/pre553_carrier_execution.py` blob `e7cda773e6a2426bfa12b22790fd8e005fe75153`
- accepted owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
- existing EE-P2X banked LiTS-A/LiTS-B evidence;
- P2R1 exact runtime-catalog, adapter-matrix, LiTS-C binding, and WVS-C adjudication returns.

## Mission

Implement the missing **production stage backend** used by the already-qualified Darwin driver.

Required module:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

It MUST export exactly:

`BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"`

and:

`run_stage(context, services)`

returning either the driver's accepted mapping shape or `BackendResult` semantics.

The backend is not a second orchestrator. The existing driver owns:

- stage ordering;
- preserved/skip stages;
- WVS-C terminal preservation;
- source/candidate progression;
- stop propagation;
- durable ledger;
- supervisor-token emission;
- resume law.

The backend owns only the actual work of each `READY__RUN_LOCALLY` stage.

## Required production coverage

Implement every executable stage in the adopted continuation map:

- `S01_CANDIDATE_PREPARATION_BUILD` where runnable;
- `S02_C11_REACHABILITY`;
- `S03_PARITY_ORACLE_GATE`;
- `S04_I03_EXECUTION`;
- `S05_I05_LEARNED_PRODUCTION`;
- `S06_PROVENANCE_AUDIT`;
- `S07_COLD_RESEARCH`;
- `S08_WARM_REPEATED_RESEARCH`;
- `S09_DELETION_REGEN_OR_A_PERSISTENCE`;
- `S10_SOURCE_RELEASE_INVALIDATION`;
- `S11_SEMANTIC_AUTHORITY_INVALIDATION`;
- `S12_STALE_CACHE_OR_PERSISTENT_STATE` where applicable;
- `S13_CORRUPT_CACHE_OR_PERSISTENT_STATE` where applicable;
- `S14_INTERRUPTION_RECOVERY`;
- `S15_FRESH_PROCESS_REPLAY`;
- `S16_TERMINAL_METRIC_VECTOR_COMPLETENESS`;
- `COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION`.

Do not implement stages classified by the reducer as `DONE__PRESERVE`, `SKIP__NOT_APPLICABLE_BY_FROZEN_LAW`, or `TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE`; the driver already terminalizes those mechanically.

## Source/candidate composition law

For each executable source×candidate cell, use the exact already-accepted physical owner and exact source-specific governed authority.

Candidate owners are fixed:

- A: `rawlsing_next/pre553_r5_source_backed_adapter.py` at owner commit `0b96b8de...`
- B: `rawlsing_next/pre553_source_backed_c11_facade.py` at owner commit `0b96b8de...`
- C: `rawlsing_next/pre553_route_c_accelerators.py` at owner commit `0b96b8de...`

Use `services.accepted_repository_builder(candidate)` and `services.compose_p2r1_binding(...)` rather than importing or reproducing owner logic independently.

The backend must locate and consume exact previously accepted source-specific projection/runtime-catalog/workload authorities already present in repository history/returns. It may add deterministic deserialization/binding glue, but MUST NOT invent source semantics, infer missing projection fields, hash-invert refs, or define a second semantic workload.

### LiTS-I

Preserve:

- source SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- 50-candidate / 77 independently executed role workload;
- expected product SHA-256 `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`;
- Candidate-C exact CACC1+CACC2 closure only;
- no repetition of LiTS-A qualifying first build;
- no repetition of LiTS-B standalone cacheless-C11 preparatory milestone.

### WVS7

Preserve:

- source SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- replay `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- DiscoveryAuthority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- exact 46-candidate frontier and `10/1/10/25` family shape;
- exact 11 predicates and 3 queries;
- WVS-C has **no backend execution path**.

## Measurement law

Actual measurements occur only when this module later runs under the qualified driver on the authorized local Darwin host.

Browser qualification MUST NOT open real LiTS/WVS carriers or emit surrogate candidate performance.

When running locally, stage measurements must be obtained from real operations, using monotonic/high-resolution host facilities and the accepted Darwin RSS law. No pre-populated metric value or benchmark result may exist in repository code.

Any metric not reached due to a typed stop must remain governed by the receipt contract's nonmeasured states; do not substitute zero.

## Evidence outputs

Backend `measured_payload` must bind normalized evidence through `evidence_artifacts` exactly as required by:

`WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`

At minimum:

- successful S05 -> learned receipt;
- successful S09 -> A persistence receipt or B/C deletion-regeneration receipt;
- successful S16 -> source×candidate terminal receipt;
- any attempted terminal failure -> source×candidate receipt + typed failure receipt;
- S17 -> run/final evidence required by the driver-bound verifier.

All repository evidence paths must live under:

`WORKER_RETURNS/EE-P2X/LOCAL_COURT/`

and must be returned to the driver in `output_artifacts` so exact hashes are ledger-bound.

## Parity and oracle law

Freeze candidate-neutral oracle identity before candidate output.

No performance metric may be admitted before all required parity dimensions pass.

Historic products are oracle/reference material only; never substitute them as fresh execution.

Any common-source or common-court authority defect must use the driver's typed blocker semantics, not a candidate-local failure.

## Lifecycle law

Implement exact frozen candidate behavior rather than generic simulated cache tests:

- A: separately classify information authority, operational persistence value, and rebuild cost;
- B: no P4 optional cache exists; S12/S13 remain driver-level frozen-law skips;
- C: only authorized regenerable accelerators may exist;
- B/C S09 deletes P4 optional cache + P5 transient compiler state while retaining P1/P2/P3, then proves identity-equivalent regeneration;
- stale/corrupt tests must operate only on actually-existing governed persistent/optional state;
- interruption/recovery and fresh-process replay must use real subprocess/process boundaries during local execution.

## S17 law

S17 must call/compose the already-adopted driver-bound verification surface; do not create a second final verifier.

It may generate only the evidence artifacts needed for the existing verifier to operate, then return PASS iff the exact final verifier terminal is:

`PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE`

Otherwise return the exact typed blocker/failure.

## Browser qualification

Create:

`rawlsing_next/tests/test_ee_p2x_darwin_stage_backend.py`

and governed return evidence under:

`WORKER_RETURNS/EE-P2X-BE1/`

Use mocks/tiny fixtures/banked exact authority objects only.

Prove at minimum:

- contract/module loading;
- exhaustive handling of every reducer `READY__RUN_LOCALLY` stage;
- no backend path for reducer-preserved/skipped/WVS-C stages;
- exact services-based owner/P2R1 composition;
- source path required only where reducer says source access is required;
- no guessed projection/catalog/default authority;
- parity-before-performance;
- required normalized evidence role binding;
- typed candidate/source/court blocker mapping;
- B cache nonexistence respected;
- B/C deletion-regeneration class law;
- A persistence-information separation;
- interruption and fresh-process replay use actual subprocess boundary in fixture qualification;
- S17 delegates to the existing driver-bound verifier rather than duplicating it;
- no forbidden ranking/selection/cross-universe aggregation keys.

If implementation reveals an exact missing source-specific authority/preimage that cannot be lawfully recovered from accepted repository evidence, STOP with the smallest exact blocker. Do not manufacture it.

## Hard prohibitions

- no real carrier access in browser qualification;
- no Library carrier bytes;
- no actual P2 measurements in browser;
- no surrogate performance;
- no pre-populated measured values;
- no Lock1 or Lock2 mutation;
- no candidate/workload redesign;
- no new WVS accelerator;
- no third CACC;
- no golden path;
- no ranking/scoring/recommendation/selection;
- no cross-universe metric pooling;
- no P2X branch movement;
- no rebase;
- no replacement branch;
- no MAIN mutation;
- no semantic PRE-MAIN mutation.

## PASS terminal

`EE_P2X_PRODUCTION_STAGE_BACKEND_READY__NO_EMPIRICAL_MEASUREMENT_PERFORMED`

PASS wakes HQ adjudication and selective fan-in to the existing EE-P2X branch. Only after HQ fan-in and checkpoint sealing may the local Darwin runner resume with:

`--backend-module rawlsing_next.ee_p2x_darwin_stage_backend`
