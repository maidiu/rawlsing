# R61-R01 R4 author return — bounded adaptive native recurrence

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 remains
NOT_STARTED. A4 is implemented in this candidate; its qualification remains with
a distinct reviewer.

## Exact identity

- Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`
- R4 startup: `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`
- Profile freeze commits: `e8034e3ed9da38d9b46acd7810860ddf1d53e3c6`,
  corrected before code at `f3601f418d79c83d467ce8dd0ed1c0113c31d7e8`
- R4 code commit: `009dc5119ae21cd1bc943eeb49019cd25e22eaa6`
- Settled basis: R61L `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`;
  R61M user approval `37dba2837c94ddb71287ffbc18260d051fc9765a`.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01`

## What was delivered

A source-independent, versioned TEST_ONLY recurrence policy and finite adaptive
issue mechanism now reuses the actual PRE553 I05 exact discovery and recursive
handoff owners. It issues generations 1..D from active parents, freezes each
generation's exact expected operation set before execution, and records a
separate activation/queue ledger.

- Receipt-bound parents resolve through the existing
  `execute_exact_bounded_discovery_with_handoffs` and
  `DiscoveryBranchReplayBinding`; no private candidate state or ad-hoc
  membership is used.
- Root and immediate-parent comparators are separate issued operations and
  receipts with exact baseline predicate refs.
- A valid nonwinning exploratory parent is constructed from the source/risk
  predicate plus exact condition predicates; it never claims a winner receipt.
- D counts actual generations; K counts ancestor conditions under the explicit
  `ANCESTOR_CONDITIONS_COUNT_TOWARD_K` convention. A profile that would exceed K
  refuses with a typed limit.
- Per-generation and cumulative test budgets cap issued operations; unissued
  work is explicit with a reason.
- Every issued rule has an exact operation id/rule id and is anti-joined to
  actual receipts. Cold persisted parents are loaded in a fresh subprocess for
  N+1.

## Reference and transformed profiles

`CONTRACT_AND_TEST_PROFILE.md` and `test_profile.json` were committed before
code. Reference: J=2, K=3, D=3, breadth 2, followup 2, protected exploration 1,
per-generation cap 4, total cap 12. Transformed: different names/namespace,
D=2, breadth 1, per-generation 3, total 6. The parameters are TEST_ONLY
demonstration values, not global or original-source defaults.

## Native qualification evidence

Committed test `test_bounded_adaptive_recurrence_three_generations_actual_native`:

- Three actual generations through unchanged I05 and recursive handoff:
  12 issued operations, 12 actual rule receipts, exact anti-join at every
  generation.
- Gen2 contains a child whose root-relative and parent-relative receipt states
  differ; both are separately identified.
- A neutral aggregate parent is retained and a protected nonwinning exploratory
  parent is activated with reason `PROTECTED_NONWINNING_EXPLORATION`.
- Gen3 contains hidden internal differentiation under that neutral parent, with
  parent-relative supported and root-relative different evidence.
- Persisted `DiscoveryBranchReplayBinding` handoffs round-trip and a fresh
  subprocess loads them, runs generation N+1, and reproduces exact refs/no-drop.
- Renamed/transformed source and smaller profile also execute natively.
- D=2 stops generation 3 with `D_REACHED`; K=2 refuses a third ancestor
  condition with `EXCEED_K`; tight issuance leaves explicit `unissued` records.
- Dropping an issued recurrence rule fails exact anti-join; restoring the
  original plan passes. Invalid exploratory parent claiming a receipt and
  authority/grammar mismatch are typed refusals.

The suite also preserves all R3 conditioned JOINT/CO_TRAVEL semantics and prior
typed identity/axes tests.

## Commands and counts

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r4/junit.xml -o addopts=''
```

- Exit `0`; `24 passed`, `0 failed/errors/skips`; `10.31s`.
- JUnit: `junit.xml`; log: `pytest.log`.
- Recurrence chain measured separately: 3 generations, 12 issued operations,
  `0.4083s`, peak RSS about 31 MB.
- Python `3.11.3`, pytest `9.0.2`, pyreadstat `1.3.2`.
- Imported current owner blobs:
  - `rawlsing_next/pre553_empirical_objects.py` = `a61365b994e5c3c50de0f598fcf40e90abf757b6`
  - `rawlsing_next/pre553_discovery_exact.py` = `905f24d114419dbdd93879ad2bee5b59dd2f23af`
  - `rawlsing_next/pre553_recursive_handoff.py` = `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`
  - test helpers `test_pre553_discovery_exact.py` and
    `test_pre553_empirical_query.py` are recorded in `proof_witness.json`.

## Exact changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `c21d896d0c25a4352f379fe32fca0c1546e1a88d` |
| `rawlsing_next/tests/test_universal_grammar.py` | `2b15177a7c60499c81c506245a5899055f63bfe3` |

Report artifacts are SHA256-listed in `manifest.json`, which explicitly excludes
itself and claims no hash for any future file/commit.

## Boundary

No R03 issuance/wake, R04 custody, original respondent/source science,
U/E_pre, F6/F7/F8, N11/N12, Sorok, production/CI, or J52/W52. The reference
profile is synthetic engineering, not original science. A fresh distinct
reviewer must qualify this exact pushed candidate; the author does not adopt it.
