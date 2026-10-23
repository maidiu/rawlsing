# R61-R01 R5 author return — authenticated recurrence lineage and issue chain

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 remains
NOT_STARTED. R4 artifacts remain immutable.

## Exact identity

- Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`
- R5 startup: `5c77413365b9d45375b25dbaa29cb3da497bcb10`
- Contract amendment commit (before code): `63fe9ebf110e76326a07b9d0badf0ab7b208af6f`
- R5 code commit: `c9cd59536e9323e6f48f1818bd41204cc6ae6095`
- Independent defect review: `634ee0dac4ef87347d6f334f6c8c1abc97b24d01`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01`

## Whole-function repair

### Receipt-bound parent resolution

A `RecurrenceParentResolver` is now the declared trusted-coordinator seam. It is
constructed from the existing `load_recursive_handoff_bundle` loader or from an
in-process tuple of canonical `RecursiveBranchHandoff` objects. Before issue and
again before execution, each receipt-bound parent must resolve by exact
`replay_binding_ref`; predicate, receipt ref, handoff ref, canonical parent id,
source releases and execution releases must match. The actual owner
`replay_recursive_branch_membership` evaluator is called against the real
repository/registry/releases before I05 child execution. Missing, severed,
altered, cross-source, stale or fabricated bindings are typed
`RecurrenceRefusal`s at the same N+1 consumer. Exploratory parents remain
explicitly receipt-free; root parents remain root-only.

Trust boundary: this is a declared trusted resolver/catalog. It proves
consistency under that assumed resolver, not a protected issuer, signing
service, global durable uniqueness or R09 enforcement.

### Generation continuity

One versioned convention is implemented: `RecurrenceParent.generation` is the
generation that **produced** the parent. Root is generation 0. Generation 1
requires exactly one root parent; generation G>1 requires only non-root parents
with producer generation G-1. Mixed, duplicate, root-relabelled, skipped or
stale plans refuse. `activate_next_generation` records the producer generation,
not the next label. Persisted parents carry that convention.

### Issue-chain accounting

Each immutable plan binds its actual predecessor plan ref/count, own cumulative
count, policy hash, root predicate ref, generation, exact expected operation
ids and state (`ISSUED`/`STOPPED_BUDGET`). The predecessor plan object is
validated for generation, policy, root and count consistency. Per-generation
and remaining total caps are checked before large materialization. Exhaustion
returns `STOPPED_BUDGET` with explicit unissued entries; execution of a no-work
plan raises the typed `RECURRENCE_PLAN_HAS_NO_ISSUED_WORK`, not an untyped crash
or fabricated empty success. The law is trusted coordinator append-only
accounting at this module grain; R04/R09 service-level durability/unique-fork
enforcement is NOT_REACHED.

## Successor attacks B1–B7

| Review attack | R5 successor behavior/test |
|---|---|
| B1 severed receipt/binding | resolver lookup + handoff/receipt/predicate/source checks refuse |
| B2 root-only generation 2 | `ROOT_PARENT_NOT_ALLOWED_AFTER_GENERATION_ONE` |
| B3 understated total budget | `UNBOUND_TOTAL_ISSUED_BEFORE_REFUSED`; predecessor plan is required |
| B4 malformed profile | existing typed policy refusals retained |
| B5 receipt-bound without receipt/handoff | `PARENT_RESOLVER_REQUIRED` / binding missing refusal |
| B6 distinct root/parent comparator views | retained, with independent arithmetic expected-state assertions |
| B7 exhausted total budget | `STOPPED_BUDGET` plan with explicit unissued entries; no native call |

## Native qualification

- 26 author tests pass, including three actual generations through unchanged
  I05 and `execute_exact_bounded_discovery_with_handoffs`, exact per-generation
  anti-join, persisted handoff bundle loaded in a fresh subprocess with the
  predecessor plan ref, protected nonwinning exploration, hidden internal
  differentiation, K/D/cap refusals, source-release mutations, generation
  relabel refusal and rule-drop mutation/restoration.
- Comparator arithmetic is independently computed from the frozen synthetic
  rows for parent-relative and root-relative support states.
- Recurrence chain measured separately: 3 generations, 12 issued operations,
  `0.325s`, peak RSS about 31 MB.
- Python `3.11.3`, pytest `9.0.2`, pyreadstat `1.3.2`.

## Commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r5/junit.xml -o addopts=''
```

Exit `0`; `26 passed`, `0 failed/errors/skips`; `10.74s`. JUnit `junit.xml`,
log `pytest.log`.

## Exact changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `017c925fdb339894e682c8a5a9f2f1cabc5255e9` |
| `rawlsing_next/tests/test_universal_grammar.py` | `49cc9ad92367c90a0f6a0a08a1077d89234eabaa` |

Report artifacts are SHA256-listed in `manifest.json`, which excludes itself.

## Boundary

No R03/U43/Batch, R04 custody, R05 grades, original 35/1890, global F6/F7/F8,
N11/N12, Sorok, production/CI or J52/W52. The reference profile is TEST_ONLY
synthetic engineering, not original science. A fresh distinct reviewer must
qualify this exact pushed candidate; no self-adoption.
