# Rawlsing V550–V552J Issue Register — Execution Procedure

## Purpose

This directory is the execution authority for the confirmed V550–V552J repair set frozen on 2026-08-15. It is a task register, not semantic authority. Use it to prevent confirmed defects from being lost, duplicated, reopened without evidence, or silently replaced by a new redesign.

The governing issue-set fingerprint is:

`5004f95a7f2505b109b9ffe1aebc34693e44407c8d2bf2d54dc422aaf816c0f6`

## Source precedence

For files in this repair closure, do **not** assume GitHub `main` is the best implementation merely because it is `main`.

Use this order:

1. Explicit governed semantic/measurement authority and later owner rulings.
2. The newest actual August runtime implementation (`data/ddm_build_copy` lineage represented by Desktop snapshot `e2afe02...`, plus later V551 stamp-gate work through `9838527...`) as the default implementation baseline.
3. Accepted late-July packages as regression oracles: they prove previously accepted properties, but are not automatically newer or better than the August runtime.
4. GitHub `main` as the integration destination; preserve main-only improvements after file-by-file reconciliation.
5. Historical output packages only when a disputed behavior, hash, or regression cannot be resolved from the above. Do not start a broad archaeology project by default.

For V551 specifically, the accepted July core SHA-256 is `1339fb9197a622c130d64e256c396be43e02c9742424a9c8ec5629b161d2972c`; the August runtime copy is essentially that implementation plus a small later response-family fallback. Do not restore the July file wholesale: preserve useful later work, remove proven regressions, and fix defects shared by both.

## Register classes

- `issues_*.json`: mandatory confirmed defects. Every entry must receive a terminal resolution before this repair program is complete.
- `deferred.json`: confirmed risks explicitly outside the current mandatory repair boundary. Do not expand them into required work unless a mandatory fix or regression test proves they block correctness.
- `closed.json`: findings already resolved, disproven, or determined not to be current runtime defects. Do not reopen them without new concrete evidence.
- `file_hashes.json`: known byte-level anchors for touched or compared files.

The frozen issue shards are evidence. **Do not edit them in place to mark progress.** Record implementation progress in a separate resolution ledger so the original finding remains immutable.

## Operating rule

The objective is to **make the pipeline we have work**, not to reconstruct Rawlsing from historical packages and not to redesign unrelated stages.

For every touched behavior, classify the state as one of:

- `KEEP_CURRENT`: later runtime behavior is valid and must survive.
- `REMOVE_REGRESSION`: later behavior violates accepted/governed semantics.
- `FIX_SHARED_DEFECT`: defect exists in both accepted checkpoint and current runtime.
- `IMPLEMENT_NEW_REQUIREMENT`: required architecture/contract does not yet exist in either.
- `DEFER`: real issue, outside current repair boundary and not blocking the mandatory closure.

Never replace an entire file with an older accepted copy merely because that copy passed an earlier acceptance run.

## Preflight before editing

1. Read `index.json`.
2. Read the issue shard(s) for the stage being changed.
3. Read `closed.json` so disproven findings are not reintroduced.
4. Read relevant entries in `deferred.json` to understand boundaries without expanding scope.
5. Confirm the current Git `main` commit and the relevant runtime/donor file hashes before editing.
6. For each touched file, record: current-main hash, August-runtime hash, accepted historical hash if known, and the chosen baseline/rationale.
7. If a hash differs from the register, stop only long enough to determine whether the file legitimately advanced; do not assume corruption and do not revert automatically.

## Required implementation order

Work in dependency order unless a test-only change is needed earlier:

1. **Source/integration contract** — reconcile `main` with the August runtime for files actually touched; restore exact governed authority files required by runtime contracts.
2. **V550 boundary** — separate pure directional applicability from promotability; preserve raw response coordinates and exact upstream authority/provenance; remove downstream semantic ownership that belongs to V551.
3. **V551** — make V551 the canonical directional adjudication/projection boundary; eliminate forbidden inference; preserve neutral raw values; produce typed candidate adjudication, clean promotable atoms, distribution coverage, and run integrity.
4. **V551J** — consume the new V551 producer contract; distinguish known V551 repair debt from unexplained missing atoms; retain valid neutral and low-support review semantics; enforce producer hashes/versions.
5. **V552** — modify only the effective/live builder first; consume canonical V551 signed projection instead of re-solving scale semantics; separate intentional selected-surface partiality from unresolved adjudication debt; split integrity, evidence state, and downstream permission.
6. **V552J** — remove synthetic unknown objects and absence-to-zero aggregate scoring; preserve typed absence.
7. **Lineage/orchestration/Section85/smokes** — replace `nonempty == valid` and status-substring gates with artifact integrity, producer contract, typed evidence state, and operation-specific sufficiency.
8. **Downstream regression** — verify V553–V558 do not collapse `OBSERVED_ZERO`, `NO_APPLICABLE_EVIDENCE`, and `APPLICABLE_BUT_UNRESOLVED`. Patch only proven leaks.

Do not start the next semantic stage while producer/consumer contract versions are internally inconsistent.

## V551 design invariant

The governing architecture is:

> V551 adjudicates candidates; atoms are individually promotable; distributions carry completeness; the run carries integrity.

Keep these grains separate.

The canonical V551 surfaces should be no more than necessary:

- directional candidate adjudication (one row per applicable candidate; outcome, reason, provenance),
- clean relation-evidence atoms (promotable only),
- directional distribution coverage/completeness,
- run manifest/integrity.

Legacy diagnostics may remain as compatibility views only where a real consumer still exists. Do not create multiple authoritative artifacts that encode the same decision independently.

## Core semantic invariants

### Neutral

Certified neutral means:

- preserve raw/source `response_intensity` exactly (including midpoint coordinates such as `0.5`, or missing if the source has no numeric coordinate),
- canonical signed side = `neutral`,
- canonical signed intensity = `0.0`,
- neutral counts as represented mass,
- neutral contributes zero signed pressure,
- neutral is valid relation evidence and must not become +/- pressure.

Do not infer neutral from missing directionality.

### Missing/unresolved

Never convert these into authoritative numeric zero:

- no applicable directional evidence,
- applicable evidence with unresolved authority/projection,
- missing structural/pressure observation,
- no V552J constraint observations.

`OBSERVED_ZERO`, `NO_APPLICABLE_EVIDENCE`, and `APPLICABLE_BUT_UNRESOLVED` are distinct states throughout the chain.

### Projection authority

- V551 owns canonical signed projection.
- Load and validate the governed response-scale registry/manifest once per run.
- Use exact response-semantics-contract authority.
- No response-family fallback, generic midpoint inference, raw-sign inference, or fabricated +/- magnitude.
- V552 consumes the V551 signed representation and does not independently reinterpret raw scale geometry.

### Applicability vs promotability

Directional applicability must be authority-defined upstream and immutable. It must not be overwritten by row-level response-map success, structural completeness, support, review state, or V551 promotability.

Use typed outcomes rather than overloaded booleans:

- `APPLICABLE_BY_AUTHORITY`
- `NOT_APPLICABLE_BY_AUTHORITY`
- `APPLICABILITY_UNRESOLVED`

Candidate adjudication likewise must distinguish at least:

- `PROMOTABLE`
- `NONPROMOTABLE_REPAIRABLE`
- `NOT_APPLICABLE`

Run-integrity failure is a separate level.

### Completeness

Keep two dimensions separate:

- selected/source surface completeness (`COMPLETE_SELECTED_SURFACE` vs intentional selected-category partiality),
- directional adjudication completeness (`COMPLETE`, `PARTIAL_UNRESOLVED`, `NO_PROMOTABLE_DIRECTIONAL_EVIDENCE`, `NOT_APPLICABLE`).

A lawful intentionally partial selected surface may retain conditional normalization. Unresolved adjudication debt must never be silently renormalized away.

Enforce conservation at exact distribution grain:

`directionally_applicable = promotable + nonpromotable_directional`

and preserve weighted/unweighted unresolved mass explicitly.

## Per-issue execution protocol

For each mandatory issue ID:

1. Load the issue record and verify its fingerprint.
2. Confirm that the cited behavior still exists in the current working baseline.
3. Classify it as `REMOVE_REGRESSION`, `FIX_SHARED_DEFECT`, or `IMPLEMENT_NEW_REQUIREMENT` (or document why it is already fixed by a prior issue in the same patch).
4. Make the smallest coherent producer/consumer change that resolves the defect without reintroducing a closed finding.
5. Run the issue's minimum acceptance tests plus relevant neighboring contract tests.
6. Record the resolution in a separate machine-readable resolution ledger with:
   - issue ID and issue fingerprint,
   - resolution status,
   - files changed,
   - before/after SHA-256,
   - commit SHA,
   - tests run and result,
   - intended ID/hash changes,
   - any dependent issue IDs resolved by the same change.
7. An issue may be marked complete only when its required producer/consumer contract and acceptance tests agree.

If one code change resolves several issue IDs, record that explicitly; do not duplicate code to create one patch per issue.

## Git discipline

- Do semantic implementation on a dedicated working branch based on the chosen integration base; do not mechanically merge disconnected historical lineages.
- Preserve main-only improvements unless they directly conflict with governed semantics.
- Commit coherent dependency slices (producer + schema + validator + immediate consumers) rather than isolated half-contract changes.
- Before each commit, run focused tests and inspect the diff for unrelated source transfer.
- Acceptance evidence must point to the Git commit and relevant artifact/authority hashes. A ZIP in `outputs/` is not an installed implementation.
- Do not update governed semantic/authority registries merely to make tests pass.

## Test order

At minimum:

1. unit/contract tests for the changed issue IDs,
2. compile/import checks,
3. V550/V551 neutral, missing-direction, missing-intensity, authority-mismatch, and sibling-survival tests,
4. V551 coverage/conservation tests,
5. V551J neutral/low-support/repair-debt/local-packet tests,
6. V552 neutral-mass, true-zero, unresolved-not-zero, selected-partial vs repair-partial tests,
7. V552J no-input typed-absence tests,
8. lineage/smoke/Section85 valid-empty and valid-nonempty tests,
9. bounded 35-wave differential using existing upstream shards where possible,
10. EVS 1999/Iceland regression canary,
11. broader V550→V552J smoke,
12. V553–V558 regression for typed evidence-state preservation.

Do not require a full V550 rebuild merely to validate V551 if existing governed V550 shards are sufficient.

## Stop conditions

Stop semantic expansion and report a blocker only for conditions that make safe adjudication impossible, such as:

- missing required governed authority,
- authority/manifest hash mismatch,
- missing required producer schema,
- corrupt or contradictory identity authority,
- unresolvable duplicate identity conflict,
- invalid emitted clean-atom contract,
- compiler invariant violation.

A bad candidate, zero promotable atoms, zero review rows, zero certified packets, or zero V552/V552J evidence rows is **not by itself a failed run**.

## Non-goals for this repair

Unless a mandatory issue proves otherwise, do not expand scope into:

- wholesale historical-output archaeology,
- redesign of run-coupled IDs,
- re-governance of the V550J draft family registry,
- full-survey expansion of the bounded question authority,
- broad V553–V558 redesign,
- cleanup of every duplicate/dead helper unrelated to effective execution,
- resurrecting historical `data/ddm_build/`.

## Completion condition

This repair program is complete when:

- every mandatory issue ID has a terminal resolution record,
- no closed finding has been reintroduced,
- deferred issues remain explicitly deferred or are promoted with documented evidence,
- producer/consumer versions reject incompatible old/new mixing,
- the bounded differential and smoke suite pass according to typed integrity/evidence semantics,
- all intentional identity/hash changes are explained,
- the final Git commit(s) and exact authority/artifact hashes are recorded in the resolution ledger.

At that point, update the machine-readable resolution ledger; **do not rewrite the frozen issue shards to make the history look cleaner.**
