# 01 — Focused review of the early capacity-miss guard

## Identities

- New implementation/test head: `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`
- Capacity evidence commit: `2a41b4682cfbbdc2b5e12ba71d114adb431c670f`
- Published head: `ba5783cbc79ee6541194f6bed400af321250eb8a`
- Prior accepted implementation: `409be32f7e4b4b961a360be1c8f44a17b5c62173`
- Prior published reviews: `e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3` (P2) and
  `5dfef26d5ba25d2848d8e7a1b137e29c2d3b544d` (phase-3 compact assessment).

Production/test blobs are identical at `9a5c`, `2a41b4682`, and `ba5783cbc`:

| File | Blob SHA |
|---|---|
| `rawlsing_next/pre553_empirical_query.py` | `b72b469e6646b88e4e2ed4dbbf0f3c209557fd69` |
| `rawlsing_next/tests/test_pre553_i03_grouping.py` | `78683c4098f388eb72d686651b3282b9162e2ed2` |

`git diff --name-only 409be32..9a5c -- rawlsing_next/` contains only those two
files. Between `141df637` and `9a5c`, only those two files changed; the evidence
commit `2a41b4682` changed only C4 artifacts/tools; `ba5783cbc` changed only
`00_RETURN.md`.

## Isolated exact-head checkout

I obtained the exact head in a detached linked worktree:

```
git worktree add --detach \
  .local-logs/pyat-l03-r03/checkout-9a5c \
  9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3
```

The review branch remained at `5dfef26d...` throughout. I did not merge the author
source into the review branch, edit production, or treat the checkout as source
adoption. The detached worktree is under the assigned checkout’s `.local-logs`.
The independent gate and focused tests ran in that exact tree.

## New production delta

`rawlsing_next/pre553_empirical_query.py`:

- Adds `_miss_capacity_exhausted(cached_members)`:
  `len(cache) >= max_groups or cached_members >= max_cached_members`.
- Calls it on a cache MISS, after the HIT path, before
  `_evaluate_index_group_core`.
- Increments `capacity_fallbacks` and the new `early_capacity_fallbacks` on the
  early return.
- Retains the existing post-build check
  (`cached_members + len(core.denominator_members) > max_cached_members`) for an
  unknown prospective denominator.
- Does not add eviction/LRU/estimation, change defaults, or change close/error
  handling.

`rawlsing_next/tests/test_pre553_i03_grouping.py` adds four tests (15 total):

1. `test_grouped_scope_warm_hit_at_group_capacity_still_reuses`
2. `test_grouped_scope_capacity_miss_does_not_invoke_core_builder`
3. `test_grouped_scope_member_bound_unknown_prospective_keeps_honest_fallback`
4. `test_grouped_scope_member_capacity_hit_and_exhausted_miss`

## Focused checks and results

Focused suite at exact `9a5c`:

```
15 passed in 6.91s
```

Independent reviewer gate (`reproducers/early_miss_gate.py`, receipt
`evidence/early_miss_gate.json`):

- Fill at `max_groups=1`: builds 1, hits 0.
- Identical HIT at full group capacity: hits 1, early 0, capacity 0.
- Different-plan MISS with builder monkeypatched: builder calls 0; facts equal
  no-scope; attempts 1, builds 1, hits 1, early 1, capacity 1.
- Restored original HIT after the early miss: hits 2; early/capacity stay 1.
- Authority DENY on the full scope: `UNAVAILABLE` /
  `MISSING_REQUIRED_AUTHORITY`, equal no-scope, scope receipt unchanged.
- Unsupported topology on the full scope: `UNRESOLVED` /
  `UNSUPPORTED_RESPONSE_TOPOLOGY`, equal no-scope, scope receipt unchanged.
- W2 weight refusal after an actual early MISS: `UNAVAILABLE` /
  `MEASURE_UNAVAILABLE`, equal no-scope; early and capacity each increment by one;
  `core_build_attempts` does not increase.
- Member cap already exhausted: cached one-member core, larger new denominator
  early-falls back with zero builder calls; facts equal.
- Unknown prospective member size: guard does not fire; post-build fallback is
  used honestly (attempts 1/builds 0/early 0/capacity 1; repeat attempts
  2/builds 0/early 0/capacity 2).
- `close()`: `closed: true`, `open_groups: 0`.

The normal query/identity/permission checks occur in `execute_empirical_query`
before `_evaluate_index_group`; the DENY/unsupported/W2 checks confirm the
capacity-full fallback does not skip the normal authority/measure/refusal results.
Index attestation and per-operation authority/identity gates are upstream and were
not altered by this delta.

## Author capacity receipts: consistency review, not re-timing

`results/capacity_summary.json` at `2a41b4682` (N=200, 3 rounds):

| Side | Miss median | Attempts | Builds | Hits | Early | Capacity | Facts |
|---|---:|---:|---:|---:|---:|---:|---|
| before | 0.3383 s | 2 | 1 | 1 | 0 | 1 | equal |
| after | 0.2001 s | 1 | 1 | 1 | 1 | 1 | equal |
| no-scope | 0.1989 s | — | — | — | — | — | equal |

- The medians match the author’s stated 0.3383 / 0.2001 / 0.1989.
- The before/after counters are consistent with the guard effect.
- “before” is not a checkout of old `409be32`: it is the new code with
  `_miss_capacity_exhausted` monkeypatched to `False` (guard-disabled A/B). That
  correctly isolates the guard, but it is not an old-commit run.
- Capacity-case receipts are internally consistent across all three rounds
  (`capacity_receipt_consistency.json`).
- **No reviewer timed benchmark was run. No performance/timing claim is made.
  Author economics remain author-grade.**

## Evidence boundary

- The focused 15 tests were independently rerun at exact `9a5c`.
- The independent gate compares full `EmpiricalFact.as_dict()` for fill, hit,
  early miss, restored hit, DENY, unsupported, W2, member-exhausted, and
  unknown-prospective cases.
- The author capacity sidecars/full fact material were not re-materialized; the
  author receipts are reviewed for internal consistency and the driver’s `.as_dict()`
  comparison logic was inspected in the phase-3 review. The capacity receipt has
  booleans and counters, not a retained full-fact dump.
- No whole-estate, P41 rerun, N=1,000/3,000, original35, production, or
  cross-machine run was performed.

## NOT_RUN

- No reviewer timed benchmark or profiling.
- No whole estate or P41 rerun.
- No N=1,000/3,000 capacity or compact run.
- No source/test/guide/protected branch edit, merge, or default-policy change.
- No new architecture/design court.
