# 01 — Exact owner-integrity diff and test fix (Gate 1)

**Sealed startup (verified exact):** `ff859444355724658bf6b8b00a3ae3354abe0c9f`
**A04T parent:** `c1df9842b7531146f1d8e215f216915b9039e4d7`
**Sealed diff base (unchanged from the original test):** `b68de0dd35a9885efcb46bcd8ec9cbe41dabf500`

## 1. The defect (independently confirmed, then fixed)

`test_accepted_owners_a04_a04s_a05_untouched` asserted empty output from
`git diff --name-only b68de0dd -- rawlsing_next/`. That scope necessarily
contains A04T's own two explicitly permitted NEW files, so the assertion
could never pass on the committed branch. Baseline re-executed on the sealed
tree before any mutation: **43 passed, 1 failed** (`repro/logs/01_baseline_43of44.txt`,
25.51 s), the failure being exactly this test — matching A04TR's independent
43/44 at `db85d2b0`.

## 2. What the diff actually contained (evidence, not assumption)

`git diff --name-only b68de0dd HEAD -- rawlsing_next/` on the sealed tree
returned exactly:

```
rawlsing_next/pre553_original_workload_v2_verifier_candidate.py
rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py
```

Both are A04T's own additions (blobs `996c8e90…` / `5799900d…`, matching the
commission's pins). Every protected owner below was byte-identical between
the sealed base and HEAD.

## 3. The corrected check (only `.../test_pre553_original_workload_v2_verifier_candidate.py` modified)

Four separate properties, each with its own failure message:

- **(A) exact diff allow-list.** Every `rawlsing_next/` path changed since the
  sealed base must be inside `permitted_changed` = the V2 candidate, its test,
  and the new A04TU hostile test. Any other changed or added path fails.
  No accepted owner is whitelisted.
- **(B) pinned protected blobs.** Eight files asserted byte-equal to their
  sealed-base blobs (full SHAs in the test source):

  | File | Pinned blob |
  |---|---|
  | `pre553_original_workload_binder_candidate.py` (A04 owner) | `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5` |
  | `tests/test_pre553_original_workload_binder_candidate.py` (A04 test) | `6c06a5b013d3713af7d7ba9bf143c3ef7a6245a2` |
  | `pre553_original_workload_contract_v2_candidate.py` (A04S owner) | `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` |
  | `tests/test_pre553_original_workload_contract_v2_candidate.py` (A04S test) | `0b9f1addf2b28f2a8e489fe44f1567a137a166f2` |
  | `pre553_c11_repository.py` (C11) | `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` |
  | `pre553_c11_integrity.py` (C11) | `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd` |
  | `pre553_route_b_production.py` (Route B) | `2385cd327dced3c5b887b59085aa0d21b04d78c3` |
  | `pre553_batch_runner.py` (Batch) | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` |

  The A04 binder (`7d8b3902`), A04S contract (`08bb75c4`) and route_b
  (`2385cd32`) prefixes match A04T's own return §5; the C11/Batch blobs match
  independent B01 measurements on another branch.
- **(C) tracked-dirt refusal.** `git status --porcelain -- rawlsing_next/`
  must contain no tracked modifications (` M`/`M `/`D`). Untracked (`??`)
  entries are reported but cannot conceal an edit to a tracked owner.
  Verified live: on the dirty tree the corrected test fails naming exactly
  `M rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py`
  (my own uncommitted fix); on the committed clean tree it passes.
- **(D) external A05 oracle, independently.** The oracle
  (`.../A05-INDEPENDENT-NODROP-ORACLE-R1/repro/a05_oracle.py`) does not exist
  on this branch, so it is never asserted as a local path. The test asserts
  the A05 worktree is at `9491d0296…` and its oracle blob is
  `00a4cc84d321c3fbace0f4aa09be62dbb31994fc`. Worktree absent → explicit
  `pytest.skip` (HOLD, not pass).

## 4. Observed result

Full V2 candidate suite on the new committed clean tree
(`repro/logs/02_full_v2_suite_after_fix.txt`): **44 passed in 24.47 s**
(wall 24.71 s, peak RSS 51.8 MiB), exit 0. The inherited suites embedded in
the 44 all executed with zero skips: A04S 26 here, A04 41 in `hq280-a04`,
A05 18 in `hq280-a05`, owner spot suites here (re-run `-k` filter:
4 passed, 0 skipped).

**44/44 is reported because it was observed**, on commit `574ecf697`,
Python 3.11.3, isolated venv (pytest 9.1.1). No owner, A04, A04S or A05 file
was modified: `git diff` stat for the Gate 1+2 commit touches only the two
test files.
