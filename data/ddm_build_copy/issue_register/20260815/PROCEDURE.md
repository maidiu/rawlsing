# Rawlsing V550–V552J Issue Register — Execution Procedure

## Purpose

This directory is the single execution register for the confirmed V550–V552J repair closure. It is a task register, not semantic authority.

Base issue-set fingerprint:

`5004f95a7f2505b109b9ffe1aebc34693e44407c8d2bf2d54dc422aaf816c0f6`

Exhaustive-audit revision fingerprint:

`b89bffbde1ece404c6a21af218764654bab3b034b75951339d1b16d116c3aa72`

`index.json` is the canonical entrypoint. Read it before doing any work.

## How to load the register

1. Read `index.json`.
2. Read this procedure.
3. Load **every** `issues_*.json` file listed by `index.json`, including numbered continuation shards such as `issues_src_2.json` and `issues_v551_3.json`.
4. Apply the supersession maps in `index.json` before calculating active work.
5. Read `closed.json` so disproven findings are not reintroduced.
6. Read `deferred.json` for boundary awareness, excluding any entry promoted/superseded by `index.json`.
7. Use `file_hashes.json` and pinned hashes in `index.json` as byte-level anchors.

The original issue shards are immutable evidence. Numbered continuation shards are **not a separate audit or authority**; they extend this same register after further hostile review. Do not create a parallel issue universe.

## Governing objective

The objective is to **make the pipeline we have work**.

Do not reconstruct Rawlsing from historical output packages. Do not redesign unrelated stages. Do not assume that an older accepted checkpoint is globally better than later runtime code. Do not assume that either current GitHub `main` or the August runtime donor is globally better than the other.

### Source/integration precedence

Use this order:

1. Explicit governed semantic/measurement authority and later owner rulings.
2. For every touched implementation file, compare current `main` and the August runtime lineage file-by-file and function-by-function.
3. Preserve every proven improvement from either lineage unless it conflicts with higher authority.
4. Use accepted late-July packages as regression oracles: they prove previously accepted properties but are not automatic restore targets.
5. Search historical outputs only when a disputed behavior/hash cannot be resolved above.
6. **Never wholesale-copy either `main` or the runtime donor over the other.**

Known preservation requirements from the exhaustive reconciliation include:

From current `main`, preserve unless specifically superseded:
- shared V550/V550J respondent-substrate machinery;
- bounded V550J governed-authority/prepared-substrate validation;
- the stricter rule that `draft` is not silently executable authority;
- main-only V550 response-relation/shared-substrate/registry-contract modules;
- current-contract smoke adapters where they are aligned with live producers.

From the August runtime lineage, preserve unless specifically superseded:
- the governed `CLOSED_35_WAVES` scope and Asian Barometer W6 exclusion;
- QRA/authority-receipt work;
- accepted scale-v5 V551 and the exact response-scale registry/manifest;
- low-support handling fixes;
- V551J signed-component and compatibility-adapter work;
- V551 directionality-stamp helper after fixing its contaminated applicability denominator.

For V551 specifically, the accepted July core SHA-256 is:
`1339fb9197a622c130d64e256c396be43e02c9742424a9c8ec5629b161d2972c`

The August runtime V551 is the same core lineage plus a small later response-family fallback. Do not restore the July file wholesale: preserve useful later work, remove proven regressions, and fix defects shared by both.

## Register classes

- `issues_*.json`: mandatory confirmed defects. Every active entry must receive a terminal resolution.
- `deferred.json`: confirmed risks outside the current mandatory boundary unless promoted by `index.json` or proven blocking.
- `closed.json`: disproven/resolved/non-defect findings. Do not reopen without new concrete evidence.
- `file_hashes.json`: byte-level comparison anchors.

Do **not** edit issue records in place to mark progress. Record implementation progress in a separate machine-readable resolution ledger keyed by issue ID + fingerprint. The issue universe remains frozen evidence.

## Per-file classification before editing

For every touched file/behavior, classify the delta as:

- `KEEP_MAIN`
- `KEEP_RUNTIME`
- `REMOVE_REGRESSION`
- `FIX_SHARED_DEFECT`
- `IMPLEMENT_NEW_REQUIREMENT`
- `DEFER`

Record current-main hash, August-runtime hash, accepted historical hash when known, chosen implementation source, and rationale.

## Required implementation order

Work in dependency order unless a test-only patch is needed earlier:

1. **Source/integration closure**
   - reconcile touched main/runtime files;
   - restore or explicitly externalize exact governed dependencies;
   - repair default lineage dependency closure;
   - enforce governed 35-wave scope.
2. **V550 boundary**
   - separate pure directional applicability from promotability;
   - preserve raw coordinates and upstream authority/provenance;
   - remove canonical signed-projection ownership from V550.
3. **V550J**
   - preserve main's stricter authority-status semantics;
   - resolve the shipped-draft/default contradiction;
   - bind governed association lane publishability and actual statistical thresholds;
   - restore conditional association registries or explicit external dependency contract.
4. **V551**
   - sole canonical directional adjudication/projection boundary;
   - remove forbidden inference;
   - preserve neutral raw values;
   - fix stratified distribution identity/deduplication;
   - emit typed candidate adjudication, clean promotable atoms, coverage, and run integrity.
5. **V551J**
   - consume V551 producer manifest + atoms + adjudication/coverage;
   - distinguish known repair debt from unexplained missing atoms;
   - preserve neutral and low-support review semantics;
   - preserve/replace required compatibility adapters atomically.
6. **V552**
   - modify only the effective/live builder first;
   - consume canonical V551 signed projection;
   - distinguish selected-surface partiality from unresolved adjudication debt;
   - split integrity, evidence state, and downstream permission;
   - remove ghost/dead V552 contract requirements from consumers.
7. **V552J**
   - no synthetic unknown object;
   - no absence→0 aggregate scores;
   - hard scope identity before structural matching;
   - producer-bound inputs only.
8. **Lineage/orchestration/Section85**
   - replace `nonempty == valid`, free-text substring readiness, and path-exists gates;
   - bind all stages to one coherent producer-run graph;
   - repair Section85 path rebasing;
   - make all-wave scope authority-derived and joint stages applicability-scoped;
   - make serialization contract truthful and stale-artifact-safe.
9. **Downstream regression only**
   - verify V553–V558 do not collapse `OBSERVED_ZERO`, `NO_APPLICABLE_EVIDENCE`, and `APPLICABLE_BUT_UNRESOLVED`;
   - patch only proven leaks.

Do not start the next semantic stage while producer/consumer contract versions are internally inconsistent.

## V551 design invariant

> **V551 adjudicates candidates; atoms are individually promotable; distributions carry completeness; the run carries integrity.**

Keep those grains separate.

Canonical V551 authority should reduce to:
- directional candidate adjudication: one row per applicable candidate, outcome/reason/provenance;
- clean relation-evidence atoms: promotable only;
- directional distribution coverage/completeness;
- run manifest/integrity.

Legacy diagnostics may remain only as derived compatibility views where a real consumer still requires them.

## Core semantic invariants

### Neutral

Certified neutral means:
- preserve raw/source `response_intensity` exactly, including midpoint coordinates such as `0.5`, or missing if source coordinate is absent;
- canonical signed side = `neutral`;
- canonical signed intensity = `0.0`;
- neutral counts as represented mass;
- neutral contributes zero signed pressure;
- neutral remains valid relation evidence;
- never infer neutral from missing directionality.

### Missing / unresolved

Never convert these into authoritative numeric zero:
- no applicable directional evidence;
- applicable evidence with unresolved authority/projection;
- missing structural/pressure observation;
- no V552J constraint observations.

`OBSERVED_ZERO`, `NO_APPLICABLE_EVIDENCE`, and `APPLICABLE_BUT_UNRESOLVED` are distinct throughout the chain.

### Projection authority

- V551 alone owns canonical signed projection.
- Validate exact response-scale registry + manifest once per run.
- Exact `response_semantics_contract_hash` authority only.
- No response-family fallback, midpoint inference, raw-sign inference, or fabricated +/- magnitude.
- V552 consumes V551 signed fields and does not independently reinterpret scale geometry.

### Applicability vs promotability

Directional applicability is immutable authority-defined upstream state and must not be overwritten by response-map success, structural completeness, support, review state, or V551 promotability.

At minimum:
- `APPLICABLE_BY_AUTHORITY`
- `NOT_APPLICABLE_BY_AUTHORITY`
- `APPLICABILITY_UNRESOLVED`

Candidate adjudication at minimum:
- `PROMOTABLE`
- `NONPROMOTABLE_REPAIRABLE`
- `NOT_APPLICABLE`

Run-integrity failure is a different level.

### Completeness

Keep these independent:
- selected/source-surface completeness;
- directional-adjudication completeness.

Intentional selected-category partiality may use conditional normalization only when adjudication inside the selected surface is complete. Unresolved repair debt must never be renormalized away.

Enforce:
`directionally_applicable = promotable + nonpromotable_directional`

Preserve weighted and unweighted unresolved mass explicitly.

### Identity and scope

Before any semantic or fuzzy structural match, require exact producer/scope identity appropriate to the contract:
- producer run ID;
- source;
- wave;
- country/shard;
- exact empirical/distribution identity where applicable.

A semantic score may never bridge a failed scope-identity check.

Stage `--run-id` is not proof of lineage. Embedded producer identity and producer manifest must agree with the output/run identity.

### Producer boundary

Every semantic consumer must verify:
1. producer run-integrity PASS;
2. exact supported producer contract/schema version;
3. exact producer-declared **artifact-file SHA-256** for consumed bytes;
4. exact producer run/scope identity;
5. artifact readability/schema validity.

Shape alone, path existence, self-hashing, or nonblank contract fields are insufficient.

Distinguish logical/DataFrame hashes from serialized artifact-file hashes with different field names.

Required producer status that is missing, malformed, wrong-format, or unknown fails closed.

### Serialization and filesystem integrity

Choose one real contract:
- either Parquet is mandatory for governed pipeline execution, or
- consumers discover and verify the producer-declared artifact format/path/hash.

Do not advertise modes the immediate consumer cannot read.

Run publication must be transactional/fresh or stage-owned stale artifacts must be removed before publication. Reusing a run ID may never leave an older disabled-format artifact visible as current.

## Per-issue execution protocol

For each active mandatory issue:

1. Load the issue record and verify its fingerprint.
2. Confirm the cited behavior still exists in the working baseline.
3. Classify it under the per-file categories above.
4. Make the smallest coherent producer + schema + validator + immediate-consumer change.
5. Run the issue's minimum tests and neighboring contract tests.
6. Record in the resolution ledger:
   - issue ID and issue fingerprint;
   - terminal status;
   - files changed;
   - before/after SHA-256;
   - commit SHA;
   - tests run/results;
   - intended identity/hash changes;
   - dependent issue IDs resolved by same patch.
7. Mark complete only when producer, consumer, validator, and tests agree.

One code change may resolve multiple IDs; record that rather than duplicating implementation.

## Git discipline

- Use a dedicated implementation branch when semantic repairs begin.
- Do not mechanically merge disconnected histories.
- Preserve main-only and runtime-only improvements unless superseded by authority.
- Commit coherent dependency slices rather than half-contract changes.
- Inspect each diff for unrelated source transfer.
- Acceptance evidence must point to Git commit + exact governed authority/artifact hashes.
- A ZIP in `outputs/` is not an installed implementation.
- Do not mutate governed semantic registries merely to make tests pass.

## Test order

At minimum:

1. unit/contract tests for changed IDs;
2. compile/import checks;
3. source/dependency closure tests;
4. V550 applicability and neutral/missing projection-boundary tests;
5. V550J governed-lane publishability and dynamic-threshold tests;
6. V551 neutral, missing-direction/intensity, authority mismatch, sibling survival, stratum identity, and conservation tests;
7. V551J neutral/low-support/repair-debt/run-coherence/producer-hash tests;
8. V552 neutral mass, true zero, unresolved-not-zero, selected-partial vs repair-partial, producer-hash tests;
9. V552J typed absence and wrong-source/wave/country structural-match rejection;
10. lineage malformed-readiness fail-closed, same-run coherence, valid-empty vs corrupt tests;
11. Section85 tests from a clean checkout with no old path alias or Desktop outputs;
12. governed **35-wave** differential using existing upstream shards where possible;
13. EVS 1999/Iceland canary;
14. broader V550→V552J smoke with joint stages applicability-scoped;
15. V553–V558 typed-state preservation regression.

Do not require a full V550 rebuild merely to validate V551 if existing governed V550 shards are sufficient.

## Stop conditions

Stop semantic execution only for unsafe conditions such as:
- missing required governed authority;
- authority/manifest hash mismatch;
- missing/corrupt producer schema;
- producer integrity failure;
- incompatible contract version;
- exact run/scope identity contradiction;
- unresolvable duplicate identity conflict;
- invalid emitted clean-atom contract;
- compiler invariant failure.

A bad candidate, zero promotable atoms, zero review rows, zero certified packets, or zero V552/V552J evidence rows is **not by itself** a failed run.

## Explicit supersessions in revision 2

- `V550-004` is inactive: the runtime V550 registry loader is already cached. See `CLOSED-007`.
- `WATCH-004` is no longer deferred: its integrated current-main/runtime form is mandatory `V550J-003`.

## Non-goals

Unless a mandatory issue proves otherwise:
- no wholesale historical-output archaeology;
- no redesign of run-coupled semantic IDs beyond enforcing coherent producer identity;
- no full-survey expansion of bounded question authority;
- no broad V553–V558 redesign;
- no cleanup of every dead/duplicate helper unrelated to effective execution;
- no resurrection of historical `data/ddm_build/`.

## Completion condition

Complete only when:
- all **effective mandatory** IDs from `index.json` have terminal resolution records;
- no closed finding is reintroduced;
- deferred findings remain deferred or are promoted with evidence;
- producer/consumer versions reject incompatible old/new mixing;
- the bounded differential/smoke suite passes under typed integrity/evidence semantics;
- all intentional identity/hash changes are explained;
- final Git commits and exact authority/artifact hashes are in the resolution ledger.

Do not rewrite frozen issue history to make it look cleaner.
