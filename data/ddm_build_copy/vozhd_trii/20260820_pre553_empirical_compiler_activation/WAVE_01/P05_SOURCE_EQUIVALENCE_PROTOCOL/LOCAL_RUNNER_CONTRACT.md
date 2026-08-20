# LOCAL RUNNER CONTRACT — POPULATED SOURCE→C11 CERTIFICATION

## Role

The local Codex/exact-checkout runner is an evidence executor. Data access does not grant semantic authority. The runner executes this frozen protocol against one deliberately bounded source/release/universe lane and returns immutable evidence.

It may return `CERTIFIED`, `FAILED`, or `BLOCKED`. It may not repair contracts, invent mappings, infer missing semantics, alter authority, pool sources, tune semantic truth conditions to one source, or delete/retire source snapshots.

## Required launch inputs

Before execution, bind exact:

- repository and Git HEAD;
- clean working-tree proof;
- protocol file identities/hashes;
- exact source/release/instrument/universe IDs;
- immutable source snapshot file/object IDs and hashes;
- accepted C11 ingest authority ID/version/hash;
- exact C11 target universe/partition identity;
- source-native semantic/codebook authority IDs/hashes;
- response-topology authority IDs/hashes;
- routing/applicability authority IDs/hashes;
- weight design/basis authority IDs/hashes;
- normalization/crosswalk authority IDs/hashes;
- query/replay authority IDs/hashes;
- code/config/fixture hashes;
- exact runner command/environment identity sufficient for replay.

No `latest`, default branch, unpinned dependency, mutable lookup, fuzzy discovery, or wall-clock-derived semantic identity is allowed.

## Execution sequence

### L01 — Preflight integrity

1. Verify exact Git HEAD.
2. Verify clean working tree.
3. Verify all required protocol/authority/source identities.
4. Record runner platform/runtime versions as execution provenance only.
5. Refuse execution if a required semantic dependency can only be resolved by `latest`, guessing, or fuzzy matching.

### L02 — Source-native inventory

Inventory the exact native source before any C11 equivalence claim:

- source/release/instrument/wave/country/sample identities;
- respondent identities;
- question/component identities;
- event/multiplicity/topology surfaces;
- routing/skip/applicability surfaces;
- typed response states;
- native empirical coordinates;
- weight variables/design/bases;
- questionnaire/codebook/crosswalk files;
- immutable source snapshot hashes.

Return exact counts by typed state and identity class, but label these `DIAGNOSTIC_ONLY__NOT_EQUIVALENCE_PROOF`.

### L03 — C11 target inventory

Inventory the populated C11 lane for the same exact source/release/universe:

- EmpiricalUniverse identity;
- respondent identities;
- RespondentEvent incidence;
- EmpiricalCoordinateFact incidence;
- RoutingEligibilityFact incidence/rule refs;
- WeightMeasureFact incidence;
- AuthoritySnapshot refs;
- relation/overlap/linkage authority where applicable;
- semantic content/replay manifests.

Record counts of rejected/defaulted/coerced rows or fields. Unauthorized defaulted/coerced count must be zero for certification.

### L04 — Source-native diagnostics

Compute native diagnostics without treating canonical normalization as already valid:

- exact respondent sets;
- event multiplicity distributions;
- topology classes;
- routing/applicability typed states;
- risk-set member sets for selected governed fixtures;
- typed missing/DK/refusal/IAP/not-asked/inapplicable counts;
- raw support;
- weight presence/status/basis;
- native coordinate identity/value/unit/taxonomy/time coverage;
- branch/joint configuration identity where applicable.

### L05 — Bounded ingest prerequisite

Only after the campaign's accepted ingest prerequisite is satisfied, ingest one bounded source/release lane into C11 under exact accepted authority. No repair-on-the-fly is permitted.

If ingest cannot proceed because authority or source semantics are missing, return `BLOCKED` with exact blocker identities.

### L06 — P01–P20 dimensional comparison

For each proof dimension record:

- proof ID;
- applicability decision and authority;
- source object ref/hash;
- C11 replay object ref/hash;
- exact comparison key;
- expected equality;
- allowed normalization authority if any;
- source diagnostic hash;
- C11 diagnostic hash;
- state `PASS|FAIL|BLOCKED|NOT_APPLICABLE`;
- exact mismatch/blocker details;
- evidence bundle refs/hashes.

`NOT_APPLICABLE` requires a positive exact frontier/source rule. Missing information is never `NOT_APPLICABLE`.

### L07 — M01–M18 information closure

Prove that every D13 C11 information class required for this source/frontier is physically retained or immutably/exactly dereferenceable. A missing required class is `BLOCKED` if source evidence/authority is unavailable, or `FAILED` if the source evidence exists and C11 lost it.

### L08 — T01–T18 hostile/frontier replay

Run the source-applicable retained replay frontier, including topology/routing/weights/identity/joint/branch/coordinate/lineage cases. Preserve exact member identities and typed zero/blocked states.

Do not certify from selected aggregate parity.

### L09 — Determinism

Repeat the complete semantic proof under identical governed inputs. Canonical semantic dimension states, evidence identities, query results, and logical semantic projection must be identical.

Processing order may be permuted for unordered collections to prove P20. Explicit rank/sequence order must remain semantic.

### L10 — Receipt and postflight

1. Compute logical semantic integrity hash only after dimensional proof.
2. Freeze exact final certification state.
3. Record all failed and blocked dimensions even when `FAILED` precedence determines the terminal state.
4. Compute replay root over the immutable receipt/evidence manifest.
5. Verify source snapshots remain present/addressable.
6. Verify clean working tree after execution.
7. Return exact pytest/validation command output and exit statuses.

## Terminal decision

Use this deterministic precedence:

1. If any mandatory dimension has an observed semantic mismatch, terminal state = `FAILED`.
2. Else if any mandatory dimension is unresolved, terminal state = `BLOCKED`.
3. Else if every mandatory applicable dimension and retained replay obligation passes, terminal state = `CERTIFIED`.

A diagnostic warning cannot downgrade a fully proven certificate unless it corresponds to a mandatory proof failure. Conversely, a successful count/schema/hash diagnostic cannot upgrade a blocked or failed source.

## Required receipt envelope

Each local run returns one immutable receipt containing at least:

- `receipt_schema_id/version`;
- `certification_state`;
- exact source/release/universe identity;
- source snapshot manifest hash;
- Git HEAD;
- protocol and authority identities;
- code/config/fixture hashes;
- source-native inventory hash;
- C11 inventory/content identity;
- P01–P20 result array;
- M01–M18 result array;
- T01–T18/frontier result array;
- rejected/defaulted/coerced counts;
- deterministic replay comparison;
- pytest/validation output hashes and statuses;
- clean-worktree-before/after attestations;
- logical semantic projection hash;
- replay root;
- exact failed dimensions;
- exact blocked dimensions;
- source-snapshot-retention proof.

## Explicit prohibitions

The local runner must fail closed rather than:

- infer source topology from cardinality;
- infer routing from row absence;
- treat blank/null as a typed source state without authority;
- default a missing weight to `1.0`;
- deduplicate legitimate repeated/multiselect/ranked events;
- resolve conflicting scalar duplicates by first/last/modal choice;
- collapse raw source/wave/country identity into a canonical alias;
- use fuzzy labels or nearest matches;
- pool source universes because labels harmonize;
- infer source equivalence from counts/aggregates/schema/hash;
- promote empirical coordinates into structural/generated position;
- alter accepted contracts to make the source pass.

## Source retention

The runner MUST preserve and return a retention proof for the original source/native snapshot set. This contract never authorizes source deletion, replacement, destructive compaction, or retirement, even after `CERTIFIED`.
