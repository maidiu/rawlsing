# PRE-MAIN FINAL GATE SPEC R1

## Purpose

This specification defines the minimum evidence-backed gate stack that a future `integration/pre-main-reconciliation-r1` candidate must pass before it can replace `main`.

This worker did not validate such a candidate. None existed at the dispatch point. The work is forensic: it maps the validation law present at exact starting HEAD `0777a34e50221bde6801dbaca26c058a7350c9e8` and converts that law into a future admission procedure.

The central rule is: **do not manufacture a single omnibus test that the repository does not possess.** Rawlsing currently has strong executable stage/boundary tests, frozen authority checks, targeted runtime checks, and binding semantic/manual courts. Pre-main admission must compose those layers and report their different evidentiary strengths honestly.

## Starting-head findings that govern this specification

1. The tracked tree contains no GitHub Actions workflow, and the prior resolution ledger says no GitHub status checks were reported at final integration.
2. The root `README.md` explicitly calls the repository a curated source transfer and says it is not a claim that every included stage passed a full production run. Runtime data and database state are external.
3. The prior G5 gate explicitly disclosed that respondent-backed EVS end-to-end and generated real-data `CLOSED_35` sweeps were not executable. A future pre-main gate may not convert that historical limitation into an inherited PASS.
4. The R1 question-relation authority has strong immutable evidence: `SHA256SUMS.csv`, an exact 18,518-row target, exact status counts, 4,886 hostile QA checks with zero failures, and current tests that recalculate checksums.
5. The current V550 through V552J boundary stack has extensive fail-closed tests for artifact bytes, schema/compiler versions, run/scope identity, typed evidence state, downstream permission, row counts, upstream manifest hashes, and stale-safe publication.
6. The whole-machine architecture court is binding but explicitly distinct from implementation conformance. The seam court requires semantic harnesses and says artifact/readiness tests are not substitutes.
7. No literal repository-wide cold-validation or zero-loss executable exists at this starting HEAD. No-loss is therefore a composed admission property, not a fake one-command check.

## Evidence classes

Every final gate result must label each piece of evidence as one of:

- `EXECUTED_CANDIDATE_CHECK`: actually run against the candidate.
- `FROZEN_HASH_VERIFICATION`: immutable artifact/hash/count verification rerun against candidate bytes.
- `MANUAL_SEMANTIC_COURT`: adjudication against binding law with exact evidence paths.
- `TARGETED_RUNTIME_CHECK`: requires an external DB/microdata/runtime substrate.
- `HISTORICAL_PRECEDENT_ONLY`: useful context but never a candidate PASS.
- `NOT_RUN_EXTERNAL_LIMITATION`: explicitly not run because the required external substrate is unavailable.

No PASS may cite only `HISTORICAL_PRECEDENT_ONLY` or `NOT_RUN_EXTERNAL_LIMITATION` evidence.

## Gate 1 — Git / reachability integrity

### Why it belongs

Rawlsing integration law requires synchronized accepted cross-prong facts, and prior courts preserve exact accepted heads/merges. Pre-main cannot be legitimate if an accepted worker return is present only as copied files or if an unadjudicated branch is silently incorporated.

### Executable checks

At minimum:

```bash
git status --porcelain
git diff --check
git fsck --full
git merge-base --is-ancestor <declared-integration-base> <candidate>
```

For every SHA in the HQ accepted-commit ledger:

```bash
git merge-base --is-ancestor <accepted-sha> <candidate>
```

Also compare the candidate diff/tree to the adjudicated integration ledger. A clean object graph is necessary but not sufficient: the accepted-commit ledger is the authority for which branches belong.

### PASS

- candidate identity is fixed by SHA;
- declared base is an ancestor;
- every accepted commit is reachable;
- no required accepted commit is missing;
- no unadjudicated integration commit is present unless explicitly listed as an HQ integration commit;
- `git fsck` and `git diff --check` pass;
- validation evidence itself is committed and reachable.

### FAIL

Any missing accepted SHA, unknown integrated SHA, object corruption, unresolved conflict marker, or inability to produce the accepted-commit ledger is blocking.

## Gate 2 — Accepted-authority completeness

### Why it belongs

The current repository treats authority as immutable, versioned, hash-pinned material. R1 question-relation tests recalculate package checksums and exact denominators; response semantics uses exact inherited contract identities rather than recomputation. Architecture law says missing authority stays missing and cannot be replaced by heuristics.

### Candidate checks

Required frozen baselines at the starting head include, at minimum:

- R1 full question-relation package `SHA256SUMS.csv` verification;
- exact 18,518 active R1 rows;
- exact 35 active waves with Asian Barometer W6 excluded;
- exact 20-row Latinobarómetro 1995 legacy residual when loading the runtime union;
- R1 authority-status counts preserved unless a later accepted authority explicitly supersedes them;
- response-scale registry hash identity;
- V550/V551 exact binding identity: 236 active bindings, 145 distinct certified response-semantic contract hashes, 700 source-validation rows.

These are starting-head baselines, not a claim that no later accepted reconciliation authority may supersede them. The final pre-main candidate must additionally consume an HQ-issued accepted-authority ledger generated by the reconciliation campaign. If that ledger says a baseline is superseded, the supersession record must be exact and reachable.

### PASS

Every accepted/current authority entry exists at the canonical path, matches its declared hash/schema/count, and has exactly one terminal disposition: retained, superseded-by exact successor, intentionally blocked, or intentionally non-inference/negative authority.

### FAIL

Missing accepted authority, hash drift without accepted successor, duplicated competing current authority, silent blocker deletion, or absent accepted-authority ledger.

## Gate 3 — Semantic / architectural consistency

### Why it belongs

Architecture closure is binding; present implementation is not automatically conformant. Gate discipline explicitly rejects artifact-exists or exit-code-only admission. The seam court binds semantic continuity laws.

### Executable component

Run the current semantic regression suites, especially:

- V550/V551 applicability and direction transport;
- V551 atom/conservation/adjudication;
- V552 measurement-state and denominator regression;
- exact V552J join behavior;
- vertical semantic-continuity fixture;
- post-G5 V552J-to-V553 canonical consumer behavior.

### Manual court component

For every changed semantic seam, answer with exact evidence:

1. What accepted upstream meaning enters?
2. What exact operation is authorized here?
3. What identities/roles/cardinality/order/provenance/negative states must survive?
4. What new meaning, if any, is uniquely owned here?
5. What downstream meaning is explicitly not owned here?
6. Which closed noncollapse distinction could this change accidentally violate?
7. Which seam-hardening items apply?
8. Does any behavior rely on a superseded legacy shape?

The court must preserve the architecture-closure burden: architecture is reopened only by concrete starvation, irreducible semantic duplication, genuine jurisdiction contradiction, or impossible producer/consumer contract. Implementation inconvenience is not reopening evidence.

### PASS

All executable semantic regressions pass and the manual court has no unresolved material conflict with closed architecture, noncollapse law, or seam hardening.

## Gate 4 — Runtime / build correctness

### Why it belongs

The current stage graph has strong typed producer/consumer contracts and extensive tests. The root README also makes clear that runtime data and DB state are external, so a source-only gate must not fake a production-data run.

### Source-only candidate suite

The final integrator should execute, in a clean documented Python environment from repository root:

```bash
python -m pytest -q data/ddm_build_copy section85/tests
```

If environment-specific tests are intentionally excluded, record each exclusion by exact test path and reason. A broad unexplained skip count is not a PASS.

In addition, exercise current producer-manifest verifiers and any changed command-line entrypoints. Syntax/import checks are required for changed Python modules.

### Targeted runtime suite

When a compatible external database and respondent-level substrate are available, run the governed `CLOSED_35` smoke/preflight path and relevant readiness/database checks. Preserve the result separately from source-only PASS.

### PASS

- all source-only mandatory tests pass;
- no canonical producer/consumer manifest contract fails;
- no changed import/CLI/schema is broken;
- targeted runtime checks pass when their required external substrate is part of the release environment;
- if runtime substrate is unavailable, the result is `NOT_RUN_EXTERNAL_LIMITATION`, never PASS by inference.

## Gate 5 — Empirical denominator / provenance integrity

### Why it belongs

Current tests explicitly protect neutral mass in denominators, repair debt from renormalization, observed zero from unresolved, exact row counts, file hashes, manifest hashes and run identity. Whole-machine closure further requires deterministic replay/provenance and forbids mutable `latest`, hidden filesystem order, hidden network/raw-stage lookup and unnamed randomness from altering causal truth.

### Required checks

- R1 frozen counts and package hashes.
- V551 distribution conservation.
- V552 neutral-denominator and repair-debt behavior.
- Artifact `row_count` equals inspected serialized row count.
- Artifact SHA256 equals manifest declaration.
- Nested upstream manifest hashes match.
- Run/scope identity is exact.
- Evidence bundle records candidate SHA, invocation command, executable/environment, current working directory, script path, input documents and stable hashes for all materially consumed files.
- For later V3/V2-capable candidates, replay evidence must cover the TD-R07 minimum tuple: producer/repository bundle IDs/hashes, resolver rule versions, queries/generated bindings, selection receipts, V3 rules/models, named randomness, admitted events, event/checkpoint hashes, accessibility boundary, V2 render versions/session cursor, render artifact hash and V3 admission/rejection receipts.

The existing `ddm_run_provenance.py` helper captures invocation metadata but does not itself hash input documents. A final evidence recorder must supply those hashes rather than overclaiming what the helper proves.

### PASS

Every applicable frozen denominator and manifest relationship is exact, and provenance is sufficient to identify what bytes/rules/inputs produced the evidence.

## Gate 6 — No-loss preservation

### Why it belongs

No single global zero-loss script exists. The binding seam court instead enumerates the semantic invariants that implementation harnesses must prove.

### Required seam preservation ledger

For every changed seam, mark each applicable item PASS with executable evidence where available and manual evidence otherwise:

- exact producer association / no rematch;
- simultaneous-pressure cardinality preservation;
- structural direction separate from temporal delta;
- finite-strata and Absolute-Horizon multiplicity/distinction;
- canonical V554 F1/F2/B1-only authority;
- one affordance per V555 route;
- no truncation / all-seeds fanout;
- inherited V554 F2 reference-only behavior;
- direct V555 route reuse as V556 base edge;
- no implicit cross-route relation synthesis;
- genuine n-ary V556 F1 preservation;
- V556 F2 separate from V3 satisfaction;
- V557 per-root transitive role-preserving closure;
- monotone capability narrowing;
- standalone V558 resolution without raw producer directories;
- exact F2 `ResolvedStructuralContext` envelope;
- two-channel context refresh;
- generated-binding caller ownership;
- proxy evidence never laundered into lived exposure;
- exact route/context receipt replay into V3.

Also compare accepted-authority ledger counts/hashes before and after integration so that no accepted file/row/state disappears without a typed supersession.

### PASS

No changed seam has an unexplained loss, invented rematch, flattened negative state, widened permission, dropped provenance role, cardinality loss or silent truncation.

## Gate 7 — Canonical documentation / entrypoint integrity

### Why it belongs

The existing control room uses a designated current-state authority and an explicit synchronization law. Fresh sessions are expected to inherit work through a canonical handoff. Pre-main would be unsafe if code and authority are reconciled but the repository still directs readers into stale or contradictory state.

### Required canonical entrypoint

The pre-main candidate must expose one obvious current entrypoint that states:

- candidate SHA and base;
- current phase/status;
- authority hierarchy and exact read order;
- accepted-commit ledger path;
- accepted-authority ledger path;
- required gate-spec path;
- canonical active scope/denominators;
- exact source-only validation command(s);
- exact targeted runtime command(s);
- external-data limitations;
- known blocked/missing authority;
- explicit list or pointer for superseded/historical material;
- rule that old PASS records are precedent, not inherited candidate evidence.

### Mechanical checks

- every referenced path exists in candidate;
- no canonical-current document points to a missing path;
- search canonical entrypoints/status docs for contradictory current phase, canonical branch, active-wave count, or authority status;
- legacy/historical documents are labeled or routed so they cannot plausibly be mistaken for current authority.

### PASS

A single unambiguous read path leads from repository root to current candidate state and validation law.

## Gate 8 — Fresh-agent intelligibility

### Why it belongs

The repository already treats succession/handoff as an operating requirement. A whole-machine freeze must be intelligible without hidden conversation state.

### Method

Execute `FRESH_AGENT_TEST_SPEC.md` against a genuinely context-free agent. The tester receives only:

- repository identity;
- candidate SHA;
- instruction to begin at the canonical entrypoint.

The tester must not receive prior chat history or an oral explanation.

### PASS

The fresh agent answers every mandatory question with exact repository evidence, finds the validation commands and ledgers, distinguishes current from historical/superseded material, and does not invent missing authority.

## Final admission rule

`PREMAIN_FINAL = PASS` only if PM-G1 through PM-G8 are PASS.

A targeted external runtime check may be `NOT_RUN_EXTERNAL_LIMITATION` only when:

1. the release environment genuinely lacks the required external substrate;
2. the check is not needed to support a positive production-data claim being made;
3. the limitation is surfaced in the canonical entrypoint and final return;
4. all source-only and frozen-authority checks still pass.

Any `CURRENT_REQUIRED` source-only check that is not executed is `NOT_READY`, not PASS.

## Minimum PASS conditions for pre-main to replace main

1. One fixed candidate SHA with complete accepted-commit reachability and no unadjudicated integration.
2. One complete accepted-authority ledger with exact current/superseded/blocked dispositions and verified hashes/counts.
3. All current source-only authority, boundary, semantic, lineage and canonical-consumer regressions PASS.
4. No material closed-architecture or seam-hardening conflict.
5. Frozen empirical denominators, typed negative states, artifact hashes and lineage hashes remain exact.
6. Every changed semantic seam has explicit no-loss evidence.
7. Canonical current documentation is internally consistent and routes away from stale authority.
8. A context-free fresh agent can reconstruct the current machine and validation procedure without hidden state.
9. Any unexecuted external runtime validation is explicitly reported and does not support a stronger claim than the evidence permits.
