# Rawlsing Engineering Control Plane R1

## Purpose

This control plane exists to make Rawlsing's already-governed architecture executable without creating a competing source of semantic truth.

It is an **index, state machine, verifier, impact analyzer, and receipt ledger** over existing authority. It must never decide what a survey item means, change routing truth, invent structural pressure, or upgrade generated material into evidence.

The control plane is deliberately small. Its job is to stop four recurring failures:

1. reconstructing project state from chat or historical filenames;
2. reopening upstream authority because a downstream implementation is inconvenient;
3. treating a successful process exit as semantic readiness;
4. losing hard-won failure cases instead of turning them into permanent regression law.

## Constitutional model

Rawlsing keeps five independent evidence shores separate:

1. typed semantic relation truth;
2. respondent-grounded empirical co-travel;
3. routing / respondent composability / applicability;
4. position / strata / Absolute-Horizon context;
5. support / design / uncertainty.

The control plane may track dependencies among these shores. It may not collapse them.

Other non-negotiable laws inherited from the governing R5/R6 authorities include:

- downstream vividness may not exceed upstream authority;
- empirical co-travel cannot create semantic truth;
- semantic absence, REJECT, or BLOCKED cannot erase lawful empirical co-travel;
- routing controls observability, not semantic truth;
- BLOCKED is terminal uncertainty, not negative authority;
- frozen releases are append-only; downstream defects create successor obligations;
- BLOCKED_LOCAL requires a genuine local routing/design/respondent-universe incompatibility;
- synthetic fixtures test logic only and cannot satisfy empirical acceptance;
- exact governed identities beat fuzzy matching;
- V550J does not reopen the respondent database;
- exit code 0 is not stage readiness.

## Source-of-truth order

The control plane does not copy authority into new prose and then govern from the copy.

1. **Pinned governing authority** remains in its original GitHub/Library artifact.
2. **Accepted execution receipts** record what was proved under those pinned authorities.
3. `control_plane/current.json` points to the latest accepted receipt and active frontier.
4. Derived status is computed from those objects.
5. Historical/scaffold artifacts are never promoted merely because they exist.

R5 remains the cumulative ontology/history root. R6 is the post-R5 forward-execution overlay through the M6 snapshot. The accepted Phase-D closeout receipt advances R6's active execution pointer; it does not rewrite R6's constitutional laws or M6 ancestry.

## State model: pointer + immutable receipts

There is intentionally no manually maintained monolithic `project_state.json`.

`control_plane/current.json` is a tiny mutable pointer:
- governing foundation;
- latest accepted receipt;
- active frontier.

Everything else is derived.

An accepted receipt is immutable. If a later change affects it, the old receipt remains historical provenance and is marked **stale for active use** by impact analysis; it is not edited retroactively.

Promotion model:

`DRAFT -> SHADOW_RUN -> DIFFERENTIAL_ACCEPTED -> PROMOTED`

Rollback moves the active pointer to the last accepted compatible receipt. It never deletes history.

## Typed execution graph

`control_plane/pipeline_graph.json` is not a semantic ontology. It is a typed execution/control graph.

Edge meanings are explicit:
- `EXECUTION_PRECEDES`
- `CONSUMES_OUTPUT_OF`
- `SCALE_REVALIDATES`
- `RUNTIME_GUARDED_BY`
- `MUST_NOT_REOPEN`

Only `EXECUTION_PRECEDES` defines the forward stage DAG. Other edge types cannot silently become execution or semantic dependency.

The live R6 order is:

`Phase-D closed -> V552 unchanged-first -> V552J -> bounded V553 -> V554 -> V555 -> V556 -> V557 -> V558 -> canonical 35-wave app/scale court -> runtime graft -> final repair-stack reconciliation`

The canonical 35-wave respondent-data run is **after bounded V552-V558 architecture acceptance**. It is the scale/universality proof, not the place to discover what those layers mean.

## Capability courts, not generic corpora

A dataset by itself proves nothing. Every run occurs under a named **court** in `control_plane/courts.json`.

Each court declares:
- entry gate;
- scope-selection law;
- required assertions;
- allowed claims;
- forbidden claims;
- privacy class;
- what it may unlock.

This prevents a small smoke, synthetic fixture, or subprocess-success run from being cited as stronger evidence than it actually provides.

Important courts:
- repo-static integrity;
- synthetic contract logic;
- bounded V552 reacceptance;
- bounded real multi-wave temporal vertical;
- V554-V558 vertical continuation;
- 35-wave capability preflight;
- canonical 35-wave APP-GATE release court;
- runtime graft court;
- final repair-stack reconciliation.

Exact real-wave selections for bounded courts must be frozen from authority/capability requirements **before respondent outcomes are inspected**. The control plane does not hard-code a convenient story-driven subset.

## Change classes and impact

All work is classified before mutation:

- `C0_IMPLEMENTATION`: semantics-preserving code/performance/serialization/test repair.
- `C1_INTERFACE`: schema or handoff shape change without semantic-authority change.
- `C2_AUTHORITY`: new or successor semantic/routing/measurement/strata authority.
- `C3_ARCHITECTURE`: changes layer ownership, gate meaning, inference ceiling, or jurisdiction.
- `C4_DATA_EXECUTION`: corrected extraction/input/scope execution under unchanged authority.

Impact is typed, not "rerun everything downstream" and never "reopen everything upstream."

A downstream failure may invalidate a **claim of readiness**. It does not by itself invalidate the upstream authority that supplied the input.

## Work economics

There is one active vertical frontier.

Parallel work is allowed only when it is:
- a proven upstream defect that blocks a named frontier acceptance predicate; or
- infrastructure that does not change authority.

Every task must name the acceptance predicate it advances. Work that cannot name one is not frontier work.

Ordinary implementation failures are fixed autonomously with regression/equivalence proof. Vozhd adjudication is required when proceeding would change semantic meaning, routing truth, scope for semantic reasons, missingness meaning, weights/support thresholds, validator predicate meaning, privacy boundary, or architecture.

## GitHub / Library boundary

GitHub contains:
- code;
- schemas/contracts;
- control-plane indexes;
- privacy-safe accepted receipts;
- regression law;
- CI that needs no respondent microdata.

Library/local trusted execution contains:
- immutable handoff packs;
- large/private execution artifacts;
- respondent microdata;
- privacy-safe bounded reproduction capsules where appropriate.

GitHub CI may prove **repo/control integrity and synthetic logic only**. It must never advertise empirical or runtime readiness from the absence of private data.

Trusted real-data executions produce hash-pinned, privacy-safe receipts that can be checked into GitHub.

## Commands

```bash
python3 control_plane/rawlsingctl.py status
python3 control_plane/rawlsingctl.py verify --tier repo
python3 control_plane/rawlsingctl.py next
python3 control_plane/rawlsingctl.py impact --node V552J_HANDOFF --class C1_INTERFACE
python3 control_plane/rawlsingctl.py court --id V552_BOUNDED_REACCEPTANCE
python3 control_plane/rawlsingctl.py task --stage V552_REACCEPTANCE
```

`verify --tier trusted --artifact-dir <dir>` additionally verifies pinned external R5/R6 archive hashes when those files have been materialized into a trusted local directory.

## R1 stopping rule

Do not keep expanding the control plane because more governance can be imagined.

R1 is sufficient when a fresh worker can:
1. identify the governing foundation and current frontier;
2. verify control integrity;
3. identify the exact court and claim ceiling;
4. know what it may fix autonomously;
5. know what requires central adjudication;
6. return an immutable receipt that advances or honestly blocks one gate.

From that point onward, build Rawlsing.
