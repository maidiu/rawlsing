# MX01 R2 — COMMON CONTRACT DELTA

## Authorized seam

Only this seam is changed:

`DISCOVERED_CHILD -> CANONICAL_REUSABLE_PARENT_FOR_NEXT_DISCOVERY_GENERATION`

No general discovery redesign is performed.

## Before R2

I05 could compile and evaluate a `RECURSIVE_SUBGROUP_FORK` and could emit a `DiscoveryResultReceipt` containing an exact `winning_predicate_ref`. The common substrate also already contained `DiscoveryBranchReplayBinding`, including semantic slots for parent branch and winning predicate.

The irreducible gap was operational persistence and reuse:

1. the exact compiled child `EmpiricalPredicate` was not exposed as a persisted/reloadable N+1 input;
2. the existing replay binding was not materialized for the discovered recursive child;
3. immediate-parent role was therefore not available as a persisted role-bearing handoff;
4. process exit severed the direct path from an actually discovered child to a later discovery invocation unless caller knowledge reconstructed the predicate;
5. the bounded depth-two proof could therefore not be executed through a public/common persisted handoff.

## After R2

### 1. Reuse of existing semantic carrier

The implementation materializes the existing `C11Internal:DiscoveryBranchReplayBinding` with `state=PRESENT` for supported `RECURSIVE_SUBGROUP_FORK` results.

No new public PRE553 semantic-object family is created.

`RecursiveBranchHandoff` is a runtime/operational handle over:

- the existing replay binding;
- the exact persisted compiled `EmpiricalPredicate`;
- exact source release refs;
- discovery-authority/frontier refs;
- hash-bound replay side material required to validate the binding after process exit.

### 2. Exact child predicate resolution

The handoff wrapper consumes the normal I05 `DiscoveryResultReceipt`, canonicalizes its `winning_predicate_ref` through `exact_ref(...)`, and resolves exactly one governed compiled predicate from the authority-frozen grammar and exact predicate catalog.

Resolution is identity-based. A non-unique or non-matching result fails closed.

N+1 does not receive or reuse an in-memory `_Candidate` object and does not call private `_compile_frontier` to reconstruct its parent.

### 3. Explicit immediate-parent role

The materialized `DiscoveryBranchReplayBinding.parent_branch_ref_or_typed_absence` carries the exact baseline predicate ref as the immediate parent.

This is semantically distinct from unordered ancestry. `RecursiveBranchHandoff.immediate_parent_branch_ref` exposes the exact role.

### 4. Hash-bound replay closure

The handoff binds exact material for:

- source release / universe scope;
- risk-set scope;
- topology scope;
- measure scope;
- predicate grammar authority;
- same-respondent binding semantics;
- discovery authority;
- evaluated frontier;
- I05 query execution contract;
- coverage/pruning contract;
- deterministic parameters;
- winning predicate and immediate parent.

Each persisted side payload is content-addressed and checked against the ExactRef stored in the replay binding.

### 5. Persistent bundle

`write_recursive_handoff_bundle(...)` writes a canonical content-addressed bundle containing the replay binding, exact compiled predicate projection, and hash-bound replay side material.

`load_recursive_handoff_bundle(...)` reconstructs the objects and verifies exact identities. Bundle tampering fails closed.

### 6. Deterministic membership replay

`replay_recursive_branch_membership(...)` evaluates the persisted winning predicate against the exact sealed release and authority registry. It returns canonical respondent ExactRefs.

The N+1 caller does not provide guessed member labels or a reconstructed predicate.

### 7. Public/common N+1 consumption

`recursive_parent_atom(...)` converts the persisted winning predicate into an exact governed atom entry for a later I05 authority grammar.

The hostile proof therefore executes:

`PARENT -> discovered CHILD -> persisted CHILD -> fresh process -> discovered GRANDCHILD`

with GRANDCHILD's immediate parent equal to the persisted CHILD predicate ref.

## Exact proof identities

- PARENT predicate: `e542a2679d5043c6f94785253fe4f00c4df513ae45bab92a2d9863e20bb9d037`
- CHILD predicate: `1532ba19dbedefd796711cf3ec5b60795d1d8771a6640efbc8a145f6ed50faf1`
- CHILD replay binding: `ed0b6a38a44cd02900ead97f48ce6506916cb06eefe6b238c056aee5299eb696`
- CHILD persisted bundle: `b4c26c33f508019b63e583133e5d643e0fa77932ce39f48b62a39db9dbf6001b`
- GRANDCHILD predicate: `231c9fc7381ed00b5971dcb4cab4bb1af835baec99097a5a3b2f3298ce5f1c9e`
- GRANDCHILD replay binding: `b88880158a7e051aa9fc09c52386174ee960d089955984723cc631937101f86d`
- GRANDCHILD persisted bundle: `b6a58a204238a98a7216c093a00ff3b5177fc8891143d7d0c5a575f4092fa718`

## Preserved laws

R2 does not change:

- `rawlsing_next/pre553_discovery_exact.py`;
- I05 exact-frontier compilation law;
- support thresholds;
- authority-before-search law;
- diagnostic nonauthority;
- query semantics;
- A/B/C carriers;
- V3;
- downstream architecture.

Existing I05 tests remained green in the targeted verification run.

## Production file delta

### `rawlsing_next/pre553_recursive_handoff.py`

New bounded common runtime module.

Semantic reason: expose the already-existing replay-binding semantics as an exact persisted recursive handoff and make a discovered child usable by a later governed discovery generation without caller reconstruction or hidden compiler-state dependence.

## Negative ceiling

This delta proves depth > 1 through one exact persisted common handoff. It does not claim an unbounded recursive search engine, recursive architecture selection, adaptive frontier growth, or generalized downstream structural admission. Any such extension remains outside MX01 R2 authority.
