# FIABC B07 producer contract

## Producer

Module:

`rawlsing_next.fiabc_succession_producer`

Producer schema:

`RAWLSING_FIABC_CURRENT_HEAD_SUCCESSION_PRODUCER@1.0.0`

P10 context schema:

`RAWLSING_FIABC_P10_LIFECYCLE_FAILURE_SCOPE_CONTEXT@1.0.0`

Optional receipt schema:

`RAWLSING_FIABC_CURRENT_HEAD_SUCCESSION_PRODUCER_RECEIPT@1.0.0`

## Inputs

Repository-local, source-free inputs:

- actual checked-out Git HEAD;
- clean-worktree state;
- `WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json`;
- `WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json`;
- `WORKER_RETURNS/FIABC-HQ-FINAL-PREFLIGHT-FANIN/RETURN.json`;
- current I07 schema/profile/evaluator;
- exact current implementation files named by the adopted succession function boundary;
- immutable L01/L02/profile refs already encoded by the governing profile;
- accepted immutable Candidate-A/B owners where the current driver itself binds those immutable owner blobs.

No survey file path is an input.

## Outputs

The caller chooses explicit output paths:

- `--manifest-output` → frozen current-head I07 manifest;
- `--lifecycle-output` → governed P10 context;
- optional `--receipt-output` → producer receipt.

The producer writes atomically only after:

1. current HEAD resolution;
2. clean-tree gate;
3. optional expected-head equality;
4. current required-file exact Git-object resolution;
5. T2/T5 topology/law validation;
6. current-head manifest/P10 construction;
7. zero candidate-state assertions;
8. existing I07 evaluator PASS;
9. embedded PASS re-evaluation.

## Manifest identity

`manifest_identity.generated_from_ref` and `manifest_identity.generated_from_commit_sha` are both the runtime checked-out commit.

`manifest_identity.frozen_before_candidate_execution = true`.

The existing I07 `seal_manifest()` computes the governed manifest content identity. The producer does not replace or fork that law.

## Function succession

The 29 preterminal function rows are taken from the current governing profile and require a current implementation owner at actual HEAD.

Accepted semantic authority stays L02 claim-scoped authority. Current implementation presence is evidence of owner/binding, not semantic jurisdiction.

F019 and F025-F030 retain the profile's `INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY` state.

## Capability ordering

Capabilities are emitted in T2 cell order, not set/cartesian iteration order:

`LITS_I/A → LITS_I/B → LITS_I/C → WVS7/A → WVS7/B → WVS7/C`.

A/B production realization refs follow the exact immutable owner commit already used by the current driver. Candidate C binds the current-head source-specific production-binding module.

## P10 failure scopes

Candidate-local failure:

- only current candidate cell is failed;
- T2 `candidate_local_failure_next` is copied exactly per cell;
- later lawful cells remain reachable.

Common-source failure:

- remaining governed stages for that source are common-source blocked;
- next source remains reachable;
- final source proceeds to final court gate;
- disposition remains `BLOCKED_BY_COMMON_SOURCE_AUTHORITY`.

Common-court failure:

- court halts until lawful resume;
- disposition remains `BLOCKED_BY_COMMON_COURT_AUTHORITY`.

## No-cache/current-S01 invariants

The producer refuses to instantiate if:

- Candidate B S12/S13 cease to be `PURE_B_NO_CACHE` frozen skips;
- WVS7/C S12/S13 cease to be `C_ZERO_ACCELERATOR_NO_CACHE` frozen skips;
- LiTS/A S01 ceases to be current measured `READY__RUN_LOCALLY` work requiring source access and physical-host measurement.

## Pre-candidate purity

Required exact zero values:

```json
{
  "candidate_processes_started": 0,
  "candidate_outputs_seen": 0,
  "candidate_owned_roots_consulted": [],
  "ranking_or_selection": false
}
```

Any nonzero/nonempty mutation is rejected by `assert_zero_candidate_state()`.
