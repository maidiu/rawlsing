# W04 persistence-lane review — commands, hashes and results

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-w04-review-r1`
**Branch:** `review/pyat-w03-w04-mcr-w04-r1`
**Reviewed head:** `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`
**Corrected anchor:** `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`
**Prior source cut:** `46b7325637e68f78ccc7487d4b1abc7009c5ac0b` (PR895; retained, not final)
**Verdict:** `REVISE` for the W04 lane; W04-F01 and W04-F02 require exact repairs.

All commands were run from the required review worktree. HQ/author/completion worktrees were read-only. Writes were confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/persistence/`.

## 1. Worktree, branch and source completeness

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-w04-review-r1
git branch --show-current
git rev-parse HEAD
git status --short
git ls-tree -r --name-only HEAD rawlsing_next | wc -l
find rawlsing_next -type f | wc -l
```

Result:

```text
review/pyat-w03-w04-mcr-w04-r1
605ce4c409857155eaf8dad7ca4e9c2ae0b15638
clean (only the review lease untracked before commit)
402
402
```

The sparse worktree contains the complete `rawlsing_next` source tree; it is not a partial/bad anchor. The 12-ID contract `PYAT_W03_W04_MCR_C_Commission.md` and `WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv` were read; this review is scoped to W04 persistence, not whole MCR-C acceptance.

## 2. Exact source diff and blobs

```sh
git diff --stat 1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc..605ce4c409857155eaf8dad7ca4e9c2ae0b15638
git diff --name-status 1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc..605ce4c409857155eaf8dad7ca4e9c2ae0b15638
git hash-object rawlsing_next/_pre553_c11_execution_view.py rawlsing_next/_pre553_w04_cache.py rawlsing_next/pre553_parquet_carrier.py rawlsing_next/tests/test_pre553_w03_w04_completion.py
shasum -a 256 rawlsing_next/_pre553_c11_execution_view.py rawlsing_next/_pre553_w04_cache.py rawlsing_next/pre553_parquet_carrier.py rawlsing_next/tests/test_pre553_w03_w04_completion.py
```

Result:

```text
28a27961f32435665b40ba47e54a73aa2516fc42  _pre553_c11_execution_view.py
9d4fb2ee7d925156cccad893b02246a36ff329f9  _pre553_w04_cache.py
b5f8d2cbf90153e382c3a13cdd3ce75d032c7084  pre553_parquet_carrier.py
0df94b3649bbc869fe245bc7185e35218fa4d085  test_pre553_w03_w04_completion.py

e359196c5b42d9c8f54ba1f7b6359f32011edbcbb8a117b27ba39fdfb69758ff  _pre553_c11_execution_view.py
e0f6a3a4ec2f56c8f9f14aedba20521f642d23e74d5f2d10a9fa8e0edf61f210  _pre553_w04_cache.py
8c85f4b583485078b598c7d86381bf19b8e9df352ce262ea32a1da072bec82ad  pre553_parquet_carrier.py
5aaa6761c47243066bb11e033e3ce1af20fba57ae4884f2462efb1899233265f  test_pre553_w03_w04_completion.py
```

Prior accepted blobs preserved as basis:

```text
986f327aa18053edc61bd837cdded02bbf8388d9  prior accepted compact production base
8e8effa58579af0c3326ecd4af7e159947abe4ec  prior accepted test blob (unchanged at this head)
```

The lane diff is four source/test files plus documented lane evidence; no facade/ingest/repository/benchmark/route-B query engine file was changed. No second store or query engine is introduced.

## 3. Reproduced tests

Runner: `/usr/local/bin/python3` 3.11.3. `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, TMPDIR under the review lease, no environment install.

### Full selected sourcefree set

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR="$PWD/$OUT/tmp" \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml="$OUT/logs/full_selected_junit.xml"
```

Result: `40 passed in 14.95s` (lane receipt: 40 passed in 12.71s). Log: `logs/full_selected.log`.

### Source-backed facade regression

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py --maxfail=1
```

Result: `10 passed in 1.54s`. Log: `logs/source_backed_facade.log`.

### Focused completion selections

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  -k 'cache_policy or invalidation or recovery or boundary'
```

Result: `7 passed in 3.12s`. Log: `logs/focused_completion.log`. The lane's separate receipts are `2/1/3/1` in its `logs/{cache_policy,invalidation,recovery,boundary}.log`.

### Poison/rehash, stale/torn and revoked run

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py::test_cache_hit_delete_and_rehashed_same_key_poison_rebuild \
  rawlsing_next/tests/test_pre553_c11_execution_view.py::test_stale_cache_and_torn_publication_keep_previous_complete_slot \
  rawlsing_next/tests/test_pre553_c11_execution_view.py::test_revoked_workload_never_opens_warmed_accelerator
```

Result: `3 passed in 2.33s`. Log: `logs/poison_revoke_torn.log`.

## 4. Actual caller and preserved material

`execute_route_b_production` (`pre553_route_b_production.py:495-570`) calls `build_source_backed_c11_repository` (`pre553_source_backed_c11_facade.py:656-685`), which calls `_compact_public_objects` (`_pre553_c11_execution_view.py:384-513`). The tests use `_execute(_fixture())` and real I03/I05 consumers, not a serialized metadata-only path. `_consumer_material` compares full typed facts, discovery receipts, source releases and repository snapshot identity; the cold-reopen fixtures include routed/ordered/repeated, missing optional weight and valid-empty states. The cache stores only `canonical_event_body`; non-event objects, authority snapshots, weights, occurrences, ranks and zero/refusal states remain in the canonical C11 release.

## 5. Policy and edge-case probe (independent, unanticipated)

`probes/adversarial_probe.py` run in an ordinary Python process (not pytest) with TMPDIR under the review lease:

```text
no_policy_no_legacy = true
legacy_without_pytest = true
legacy_with_pytest_env_only = ACCEPTED (authorization_id=PYTEST_TEMP_ROOT_EXPLICIT,
  source_permission=NONRESPONDENT_SOURCEFREE, root under temp)
legacy_actual_cache_writes = 1
policy_root_symlink_rejected = true
policy_file_symlink_rejected = true
policy_root_0755_rejected = true
owner_mismatch_simulated_rejected = true
policy_root_relative_rejected = true
policy_root_missing_rejected = true
policy_file_group_world_writable_rejected = true
authorization_id_missing_rejected = true
retention_budget_missing_rejected = true
retention_files_after_prune = 1
hidden_staging_orphan_remains = true
legacy_root_outside_temp_rejected = true
invalid_configured_policy_no_legacy_fallback = true
dir_fsync_failure_swallowed = {raised: false, destination_exists: true}
```

The key result is **W04-F01**: an ordinary process can set `PYTEST_CURRENT_TEST` and `RAWLSING_C11_ACCELERATOR_DIR`, obtain the hardcoded `PYTEST_TEMP_ROOT_EXPLICIT` policy, and write a cache. This is not a deployment grant in the intended sense, but the claim “bare legacy environment fallback cannot masquerade” is false because the code uses an ordinary environment variable as its only test boundary.

**W04-F02**: the probe patched `_pre553_w04_cache.os.fsync` to raise; `fsync_dir` swallowed the error, `atomic_replace` returned, and the destination existed. The cache/canonical directory fsync is best-effort, not fail-closed.

**W04-F03**: an old hidden `.c11-events-orphan` staging file under a max_files=1/max_age_seconds=1 policy remained after `prune`; the retention glob only matches `c11-events-*.parquet`. A hard crash between staging and commit can leave hidden source-derived cache bytes outside the budget.

**Actual source-binding change:** with a valid policy file, the first `_execute` produced `c11-events-8.parquet`; changing the stream decoder binding to `eeee…` produced a second `c11-events-a.parquet` while the C11 release ref stayed `C11LogicalRelease|REL-m01|95de34f0…`. The new cache file is a different key, not a hit on the old one (`logs/source_change_probe.json`). This confirms the source/decoder binding is actually used by the caller, not only serialized metadata.

## 6. Lane evidence and prior capital

Lane return/evidence: `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/persistence/{00_RETURN.md,01_CHANGED_FILES_AND_BLOBS.tsv,02_TEST_RECEIPTS.md,03_POLICY_AND_CACHE_CONTRACT.md,04_HANDOFF_AND_INTEGRATION.md}` and `logs/`.

- PR895/source `46b7325637e68f78ccc7487d4b1abc7009c5ac0b` prior 43-pass run retained as prior capital, not final proof.
- Prior accepted compact production blob `986f327aa18053edc61bd837cdded02bbf8388d9` and test blob `8e8effa58579af0c3326ecd4af7e159947abe4ec` retained; the test blob is unchanged at this head.
- No 100000-event benchmark, cold RSS/economic matrix, native/original35/source/SAV/DTA/DB, science/actor, protected merge or CI waiver was run.
- No author/HQ/peer/protected write; only the review lease was written. PR895 was untouched.

## 7. Exact repair list

1. **W04-F01:** remove the `RAWLSING_C11_ACCELERATOR_DIR`/`PYTEST_CURRENT_TEST` fallback from production `load_policy`; migrate the existing test helper to an explicit private policy file under `RAWLSING_C11_ACCELERATOR_POLICY` in `tmp_path` (or a non-environment test-only injection), and re-review any changed prior accepted test blob.
2. **W04-F02:** make `fsync_dir` fail closed; cache callers treat failure as safe miss/abort; canonical `persist` raises/cleans up rather than returning success; add cache/canonical fsync-failure tests.
3. **W04-F03:** reclaim stale hidden `.c11-events-*` staging files (or stage in a cleaned subdirectory) and include them in retention/budget.

After all repairs, re-run the selected suite and adversarial probes at a new exact head. Whole W03/W04, 12-ID MCR-C, independent economic review, protected receiving and final same-head code/economic receiving remain open.

## 8. Retained hashes

`logs/review_hashes.log` retains SHA-256 of the review outputs, source/test blobs, selected logs and probe outputs. The figure `40/10/7/3` is a sourcefree test result, not economic acceptance.

**Final:** `REVISE` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`; W04-F01 P1, W04-F02 P2 and W04-F03 P3 are the minimum exact repairs; positive W04 persistence evidence accepted only at the tested sourcefree S2 scope.
