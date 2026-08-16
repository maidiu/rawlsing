# Rawlsing V550–V552J Repair — Worker Execution Guide

This guide operationalizes the **same** issue register in this directory. It does not create a second issue universe.

Canonical machine plan: `WORKER_PLAN.json`  
Issue-register revision: `b89bffbde1ece404c6a21af218764654bab3b034b75951339d1b16d116c3aa72`

## Before any worker starts

Read, in order:

1. `index.json`
2. `PROCEDURE.md`
3. `WORKER_PLAN.json`
4. this guide
5. the issue shards containing that worker's assigned issue IDs
6. `closed.json` and relevant `deferred.json` entries

The worker plan assigns **67/67 active mandatory issues exactly once**. Do not claim another worker's issues merely because a cross-cutting contract touches your stage.

All workers obey the frozen contracts `CF-001` through `CF-010` in `WORKER_PLAN.json`. In particular: exact run/scope identity, typed integrity/evidence/permission state, producer-declared artifact hashes, Parquet as the governed machine output for this repair, stale-safe publication, V551-only signed projection, and the closed 35-wave universe.

## Git model

No worker pushes directly to `main`.

All repair work converges through:

`agent/v550-v552j-repair-integration`

Each **phase** starts from the current integration-branch gate commit. A later phase uses a new branch from the post-gate integration commit; do not keep extending an old Wave-1 branch after the pipeline contract has moved.

Every phase opens a draft PR against the integration branch. Vozhd reviews ownership, reconciliation, tests and cross-stage contract closure before merging.

## Concurrency / release order

### G0

Launch concurrently:

- W01-A — source authority + Section85 path repair
- W02-A — V550
- W03-A — V550J
- W05-A — lineage/orchestration infrastructure
- W06-A — extraction/QA preparation

### G1A

As soon as exact V551 scale authority (`SRC-002`) and W02-A V550 work are merged, launch **W04-A**. Do not wait for unrelated W03/W05 work.

### G1B

W03-A plus `SRC-004` establishes the V550J side needed later by V551J.

### G2

When W04-A has delivered the new canonical V551 contract, launch **W02-B (V552)** and **W03-B (V551J)** concurrently. W01/W05/W06 can simultaneously adapt their consumers to the frozen V551 contract.

### G3A / G3B

V552 and V551J complete independently.

### G4

Only after both are ready does W06-B finalize V552J. W01 and W05 then finish Section85/lineage consumers against the actual final producer contracts.

### G5

Run 35-wave acceptance, Section85, EVS 1999/Iceland, downstream typed-absence checks, and close `SRC-001`. Only then merge integration to `main`.

## Worker ownership

### W01 — source authority + Section85

Primary issues: `SRC-002`, `SRC-004`, `ORCH-002`, `ORCH-003`, `ORCH-009`, `ORCH-010`.

Phase A may write only authority/registry bytes and `section85/**`. Do not regenerate semantic authority. Restore exact governed bytes where pinned, or make the dependency explicitly external and fail-closed.

Phase B makes Section85 consume typed producer state rather than nonzero rows, obsolete booleans, or mere readiness-document presence.

### W02 — V550, then V552

Phase A owns `V550-001/002/003/005/006` and the V550 applicability/raw/provenance boundary.

Phase B owns `V552-001` through `V552-007` after G2. V552 must consume canonical V551 signed/coverage semantics, not re-solve scale geometry.

Do not edit V551 semantic files.

### W03 — V550J, then V551J

Phase A owns `V550J-001` through `V550J-003`: actual threshold provenance, governed lane publishability, and draft/executable coherence.

Phase B owns `V551J-001` through `V551J-005` after G1B + G2. Preserve useful runtime compatibility adapters unless all consumers move atomically to a new versioned artifact set.

Do not mutate governed family-registry semantics merely to make tests pass.

### W04 — sole V551 semantic owner

Primary issues: `SRC-003` + `V551-001` through `V551-017`.

W04 owns the bottleneck. Do **not** split V551 among coding workers.

It must deliver: exact contract-hash projection authority; preserved raw neutral; signed neutral zero; no intensity-only direction inference; pure applicability denominator; pre-promotability candidate universe; clean atoms; position-safe deduplication; canonical adjudication and coverage; mass conservation; separate run integrity; cleaned provenance/hash grain; and an explicit new V551 contract version.

### W05 — lineage / orchestration / publication integrity

Primary issues: `SRC-005`, `LIN-001` through `LIN-011`, `ORCH-001`, `ORCH-005` through `ORCH-008`.

W05 owns lineage selection, paired-wave preflight, all-wave smoke, shared producer-manifest verification and stale-safe publication infrastructure. W05 does **not** edit stage semantic builders.

`LIN-007`, `LIN-008`, `ORCH-007`, and `ORCH-008` are cross-cutting. Stage workers implement their local hooks; W05 keeps them `PARTIAL_AWAITING_CROSS_HOOK` until every affected stage is merged and verified.

### W06 — QA, then V552J

Primary issues: `ORCH-004` + `V552J-001` through `V552J-004`.

Phase A owns extraction diagnostics and black-box regression preparation. It also tests deferred `WATCH-001`, `WATCH-002`, and `WATCH-006` without redesigning V553–V558.

Phase B begins only after G3A + G3B. V552J must emit typed absence instead of synthetic `unknown`, preserve null rather than absence→0, and require exact run/source/wave/country-or-shard identity before structural scoring.

Phase C runs EVS, 35-wave typed-state and downstream non-leakage regressions.

## Cross-cutting hooks

The following issues have one primary owner (W05) but require stage-local hooks:

- `LIN-007`
- `LIN-008`
- `ORCH-007`
- `ORCH-008`

W02/W03/W04/W06 should implement only the hook inside their owned stage. They must not invent a different boundary or serialization contract.

## Worker return

Every phase returns a machine-readable report with:

- worker ID and phase
- exact base commit and branch
- primary issue IDs
- per-issue status
- every changed file with before/after SHA-256
- main/runtime reconciliation classification for each touched implementation
- contract changes
- exact test commands/results
- cross-worker dependencies still outstanding
- commit SHA and draft PR
- explicit assertion that no unowned files were changed

Issue status is one of:

- `RESOLVED`
- `PARTIAL_AWAITING_CROSS_HOOK`
- `BLOCKED_BY_AUTHORITY`
- `NO_LONGER_REPRODUCES_WITH_EVIDENCE`

Reconciliation classification is one of:

- `KEEP_MAIN`
- `KEEP_RUNTIME`
- `MERGE_BOTH`
- `REMOVE_REGRESSION`
- `FIX_SHARED_DEFECT`
- `IMPLEMENT_NEW_REQUIREMENT`

Workers never edit the issue shards to mark completion. Vozhd records terminal resolution after reviewing the return.

## Standard launch prompt

> You are Rawlsing repair worker **{{WORKER_ID}}**, phase **{{PHASE_ID}}**. Work only from the canonical register at `data/ddm_build_copy/issue_register/20260815/`. Read `index.json`, `PROCEDURE.md`, `WORKER_PLAN.json`, and `WORKER_GUIDE.md` first. Your primary issues are **{{ISSUE_IDS}}**. Your branch is **{{BRANCH}}**, based on the gate commit supplied by Vozhd. You own only **{{WRITE_DOMAIN}}**. Do not edit register governance files or another worker's semantic files. Preserve proven improvements from both current `main` and the August runtime lineage; never wholesale-copy a donor file. Apply `CF-001` through `CF-010` where they touch your stage. Run the issue-specific and neighboring contract tests. Return the required machine-readable worker report, commit SHA, and draft PR against `agent/v550-v552j-repair-integration`. A partial or blocked result must be reported as such, never disguised as completion.
