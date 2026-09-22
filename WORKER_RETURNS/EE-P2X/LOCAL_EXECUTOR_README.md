# EE-P2X local Darwin executor — driver-bound receipt/verifier surface

Status: `PROPOSED_FOR_HQ_ADOPTION__NOT_OPERATIVE_AUTHORITY`

This surface makes the remaining local court mechanical around the **qualified Darwin driver**. The preparation packet itself opens no empirical carrier and contains no candidate outcome or performance value.

Exact controlling execution interfaces:

- adopted continuation map: `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json`
  - Git blob `e06e95dd370a4fd44235932088308c3372522ed4`
  - SHA-256 `ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`
- qualified driver: `rawlsing_next/ee_p2x_darwin_court_driver.py`
  - Git blob `c3a368270f6f7a6f613efb78e31972e64a092c88`
- qualified P2X fan-in head: `6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`
- driver-binding contract: `WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`

The older normalized receipt packet remains in force for the evidence semantics it already defined. The driver-binding layer does not replace it; it proves that those normalized receipts came through the actual driver ledger and per-stage receipt interface.

## Mechanical local sequence

The driver owns stage order and resumability. Do **not** hand-maintain a parallel stage ledger.

Use the exact driver modes:

- `--preflight`
- `--status`
- `--run`
- `--resume`
- `--verify-only`

The adopted reducer fixes source order as:

`LITS_I -> WVS7`

and candidate order within each source as:

`A -> B -> C`.

The first unfinished stage is exactly:

`LITS_I/A/S02_C11_REACHABILITY`.

The local supervisor supplies the exact local source paths only to driver modes that require them. The receipt/verifier preparation code does not discover, open, substitute, or synthesize source carriers.

## Driver ledger is primary execution evidence

The driver writes:

`<work-root>/ee_p2x_stage_ledger.json`

with schema:

`RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0`.

Each terminal stage is bound to:

- exact stage/source/candidate;
- exact input-identity hash;
- exact terminal disposition;
- exact per-stage receipt path and SHA-256;
- exact output-artifact locators and SHA-256;
- verifier-completion state;
- exact next stage.

Per-stage receipts live under the driver's work root, ordinarily:

`cells/<SOURCE>/<CANDIDATE>/receipts/<stage>.json`.

The driver-bound verifier consumes those exact fields and schemas. It does not infer execution from a prose summary or from the existence of normalized files.

## Backend-to-normalized evidence bridge

For an actually executed `READY__RUN_LOCALLY` stage, the driver writes:

`RAWLSING_EE_P2X_DARWIN_STAGE_RECEIPT_ENVELOPE@1.0.0`.

The backend's `measured_payload` may bind normalized evidence through:

`evidence_artifacts`.

Allowed roles are:

- `cell_receipt`
- `failure_receipt`
- `learned_receipt`
- `deletion_receipt`
- `persistence_receipt`

Every declared path must be repository-relative under
`WORKER_RETURNS/EE-P2X/LOCAL_COURT/` and must also appear in that **same stage ledger entry** as
`repo:<path>` with the exact SHA-256. A normalized receipt that merely exists in the tree but is not bound by the actual driver stage is not admissible as fresh execution evidence.

Minimum stage bindings:

- successful `S05_I05_LEARNED_PRODUCTION` -> `learned_receipt`;
- successful `S09_DELETION_REGEN_OR_A_PERSISTENCE`
  - A -> `persistence_receipt`;
  - B/C -> `deletion_receipt`;
- successful `S16_TERMINAL_METRIC_VECTOR_COMPLETENESS` -> `cell_receipt`;
- any actually attempted backend terminal failure -> both `cell_receipt` and `failure_receipt`.

For a stopped attempted cell, metrics not reached by the lawful stop are typed
`NOT_REACHED_AUTHORIZED_STOP` with null value and a reason. They are never replaced by zero.

## Manifest synchronization

The pre-existing seeder remains byte-identical:

`WORKER_RETURNS/EE-P2X/11_seed_ee_p2x_local_receipts.py`.

It may be used once to create empty normalized receipt skeletons before local execution. It does not constitute execution evidence.

After driver stages have produced evidence, synchronize the normalized manifest mechanically with:

`WORKER_RETURNS/EE-P2X/11A_sync_ee_p2x_driver_manifest.py --driver-work-root <work-root>`.

That synchronizer derives only facts recoverable from the driver ledger and its bound evidence artifacts:

- attempted cells;
- actually executed reducer stage addresses;
- six-row coverage state;
- receipt pointers;
- physical-host identity from bound cell receipts;
- exact driver/map/ledger identities.

It does not fill measurements.

## Repetition-forbidden and frozen-law stages

`DONE__PRESERVE` is non-executable. The driver-bound verifier rejects a backend execution envelope on such a stage.

In particular, do not repeat:

- the LiTS-A qualifying first build;
- the LiTS-B standalone cacheless C11 preparatory stage.

Their exact banked evidence is consumed through the driver's
`RAWLSING_EE_P2X_PRESERVED_STAGE_BINDING@1.0.0` receipts.

Frozen-law skips use:

`RAWLSING_EE_P2X_FROZEN_LAW_SKIP@1.0.0`.

Candidate-local and common-source propagation receipts are also non-execution terminalization. They must point backward to the actual typed blocker stage.

A metric genuinely absent from a repetition-forbidden historical stage may use
`NOT_CAPTURED_PRESERVED_STAGE` with null value plus reason. Nothing is rerun merely to rectangularize the metric vector.

## WVS Candidate C

WVS7/C is not executed.

The exact driver path is:

- S00: preserved preflight binding;
- S01: `RAWLSING_EE_P2X_PRESERVED_CANDIDATE_LOCAL_FAILURE@1.0.0`
  with `WVS7_C__CURRENT_PORTABILITY_FAILURE`;
- S02-S16: frozen-law skips.

There is no Candidate-C fallback, no WVS accelerator, and no Candidate-C backend source path. The normalized preserved failure remains:

`WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json`.

## Supervisor tokens

After every actually executed stage whose reducer tuple requires physical-host measurement, the driver prints one:

`RAWLSING_LOCAL_SUPERVISOR_ACTION {...}`

token with schema:

`RAWLSING_EE_P2X_LOCAL_SUPERVISOR_ACTION@1.0.0`.

Capture the JSON object exactly under:

`WORKER_RETURNS/EE-P2X/LOCAL_COURT/supervisor_tokens/<stage-address-with-slashes-replaced-by-__>.json`.

The driver-bound verifier checks the stage, receipt hash, branch, observed head and token schema. The token's `ledger_sha256` is the **historical post-stage ledger hash emitted at that moment**; do not replace it with the eventual final-ledger hash.

The driver does not commit or push automatically. The supervisor token is the mechanical handoff for the bounded commit/push step on the existing P2X branch.

## Pre-outcome identities vs measured values

The normalized packet still requires pre-outcome binding of:

- physical-host identity;
- governed projection identity;
- exact RuntimeObjectCatalog identity;
- accepted candidate-provider identity;
- candidate-neutral oracle identity.

Parity/oracle completion must precede performance admission.

Actual local execution alone may supply:

- source open/decode/reread counts;
- bytes read/written/rewritten;
- wall/CPU/RSS/scratch measurements;
- durable authoritative/regenerable bytes;
- cold/warm I03;
- I05 learned-production wall time and throughput;
- repeated-research reread/redecode;
- delete/rebuild evidence;
- invalidation recomputation units;
- stale/corrupt persistent-state behavior;
- interruption/session recovery;
- fresh-process replay;
- audit time;
- removable-with-zero-information-loss bytes;
- moving-parts count;
- fresh execution output/product/semantic/replay identities.

The preparation packet contains none of those measured values.

## LiTS learned-product law

Every qualifying LiTS cell must produce fresh execution evidence for exactly:

- 50 candidates;
- 77 independently executed roles;
- 49 `EVALUATED_SUPPORTED` + 1 `EVALUATED_VALID_EMPTY`;
- product SHA-256 `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`.

Historical learned product may serve as oracle/reference authority only.
`historic_product_substitution` must remain false.

## WVS learned-product law

The normalized verifier binds:

- Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- replay `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- DiscoveryAuthority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- exact candidate grammar;
- 46 canonical candidate hashes;
- 11 predicate hashes;
- 3 query hashes;
- family shape `10/1/10/25`.

The frontier must be frozen before outcome access and unchanged afterward. No synthetic fallback is admitted. If both WVS A and B qualify, their governed product/semantic/replay identities must match.

## Deletion/regeneration and Candidate A persistence

For a qualifying B or C cell:

- delete P4 optional cache;
- delete P5 transient compiler state;
- retain P1 source;
- retain P2 governed semantic/learned products;
- retain P3 replay/provenance determinants;
- prove C11/I03/I05 reachability;
- regenerate in a fresh process;
- require exact before/after product, semantic and replay identities.

For Candidate A, keep three questions separate:

1. information authority;
2. operational persistence value;
3. rebuild cost.

`expensive_to_rebuild_used_as_authority_basis` must be false.

## Typed stops

The older normalized packet recognizes candidate/source/interruption/parity stops. The qualified driver adds one exact orchestration disposition that predates that vocabulary:

`COMMON_COURT_BLOCKER -> BLOCKED_BY_COMMON_COURT_AUTHORITY`.

The driver-binding contract normalizes that only as:

`COMMON_COURT_AUTHORITY_FAILURE`

with scope:

`COURT_UNTIL_RESUME`.

The driver-bound verifier validates its actual stage envelope and bound failure receipt, returns that exact disposition directly, and does **not** force it through the older normalized verifier as a different failure kind.

Candidate-local failures do not suppress later lawful cells. Common-source authority blockers stop that source and remain final blockers even though later sources may lawfully proceed. Common-source and common-court failure receipts are candidate-neutral (`candidate: null`) so one exact common-scope receipt can cover later unattempted positions without falsely attributing the common defect to another candidate. No failure authorizes synthetic completion.

## Final verification

The canonical final receipt check is now:

`WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py --driver-work-root <work-root>`.

It performs, in order:

1. exact qualified-driver and reducer identity checks;
2. exact driver-ledger and per-stage receipt verification;
3. exact output-artifact binding verification;
4. exact supervisor-token verification for executed measured-host stages;
5. WVS-C/preserved/skip/propagation-law verification;
6. deterministic normalized-manifest synchronization;
7. the unchanged normalized verifier `12_verify_ee_p2x_local_court.py`.

It writes:

- legacy normalized receipt: `LOCAL_COURT/90_FINAL_VERIFICATION_RECEIPT.json`;
- driver-bound receipt: `LOCAL_COURT/91_DRIVER_BOUND_FINAL_VERIFICATION_RECEIPT.json`.

The only successful terminal is:

`PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE`.

Otherwise it returns the deterministic exact blocker/failure disposition.

If the verifier is invoked as the S17 backend, S00-S16 must already be terminal; S17 itself need not yet exist because the driver writes that terminal entry only after the backend returns. After `--run`/`--resume` returns, execute the driver's `--verify-only` mode and retain its exact PASS output. That final pass revalidates S17 as well.

No score, ranking, winner, selection, recommendation or cross-universe metric pool is permitted.
