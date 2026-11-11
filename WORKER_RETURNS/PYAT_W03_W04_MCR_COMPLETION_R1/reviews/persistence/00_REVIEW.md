# W04 persistence-lane independent review

**Review:** independent nonauthor W04 persistence-lane review of exact candidate `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`.
**Scope:** W04 persistence lane only (`W04-COLD-PERSIST-REOPEN`, `W04-GOVERNED-DEFAULT`, `W04-AUTHORITY-INVALIDATION`, `W04-ATOMIC-LIFECYCLE`, `W34-PRODUCT-BOUNDARIES`). This is **not** whole W03/W04, whole MCR-C/12-ID, economic, native, source-rights, science, actor, or protected acceptance.
**Reviewer:** existing DeepSeek Flash MAX reviewer, nonauthor of the lane implementation; user-selected HQ delegation. No subworkers.
**Branch/head:** `review/pyat-w03-w04-mcr-w04-r1` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`; clean; `rawlsing_next` source tree full (402 files at HEAD). Worktree is the required review worktree, not the author or completion checkout.
**Verdict:** **`REVISE` at this head** for the W04 lane: two demonstrated defects remain (legacy environment fallback can masquerade as policy authorization; directory-fsync failure is silently swallowed). The positive persistence/canonical-carrier evidence and exact-fact preservation pass at the tested sourcefree S2 scope.

## 1. Contract, lane and prior capital

The frozen MCR-C contract requires 12 IDs; this review covers only the W04/W34 persistence subset and does **not** accept W03 cold-highwater/selected-cell, W34 resource-economy or the whole 12-ID return. PR #895 at `46b7325637e68f78ccc7487d4b1abc7009c5ac0b` and its prior 43-pass sourcefree run are retained as prior capital, not final proof; PR #895 was not touched. The reviewed compact production base blob `986f327aa18053edc61bd837cdded02bbf8388d9` and prior accepted test blob `8e8effa58579af0c3326ecd4af7e159947abe4ec` remain the accepted basis; the prior test blob is unchanged at this head. The production execution-view file is intentionally modified by this lane.

The lane diff from corrected anchor `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc` is 21 files: four source/test files and the lane return/evidence. No facade, ingest, repository, benchmark or route-B query-engine file was changed. Exact source/test blobs and SHA-256:

```text
28a27961f32435665b40ba47e54a73aa2516fc42  e359196c5b42d9c8f54ba1f7b6359f32011edbcbb8a117b27ba39fdfb69758ff  _pre553_c11_execution_view.py
9d4fb2ee7d925156cccad893b02246a36ff329f9  e0f6a3a4ec2f56c8f9f14aedba20521f642d23e74d5f2d10a9fa8e0edf61f210  _pre553_w04_cache.py
b5f8d2cbf90153e382c3a13cdd3ce75d032c7084  8c85f4b583485078b598c7d86381bf19b8e9df352ce262ea32a1da072bec82ad  pre553_parquet_carrier.py
0df94b3649bbc869fe245bc7185e35218fa4d085  5aaa6761c47243066bb11e033e3ce1af20fba57ae4884f2462efb1899233265f  test_pre553_w03_w04_completion.py
```

Prior accepted blobs: `986f327aa18053edc61bd837cdded02bbf8388d9` (execution view base) and `8e8effa58579af0c3326ecd4af7e159947abe4ec` (prior accepted test, unchanged).

## 2. What independently passed

### 2.1 Actual caller path

The W04 accelerator is reached through the real source-backed facade, not only a serialized metadata probe:

```text
execute_route_b_production
  -> build_source_backed_c11_repository
  -> _compact_public_objects
  -> governed policy/key/envelope/cache
  -> C11Repository and CarrierNeutralResearchExecutor I03/I05
```

The lane tests call `_execute(_fixture())` from the existing Route B fixture and exercise the actual I03/I05 consumers. The cache file is a single `canonical_event_body` Parquet relation plus envelope metadata; the canonical C11 release remains in `ParquetC11Carrier` with its full relational tables. No second store or query engine is introduced.

### 2.2 Policy-file path and authorization edges

An explicit private policy file under `RAWLSING_C11_ACCELERATOR_POLICY` activates the cache; the policy schema, absolute private owned root, nonrespondent sourcefree permission, nonempty authorization id and positive retention budget are validated. The review independently reproduced:

- absent policy/no legacy: no policy, no write;
- configured policy missing/invalid: no fallback, no write;
- policy root relative/missing/0755: rejected;
- final-component policy-root symlink: rejected;
- policy-file symlink and group/world-writable policy file: rejected;
- simulated owner mismatch: rejected;
- legacy directory root outside the platform temp root: rejected.

These are sourcefree fixture-only negative checks; no host deployment grant is inferred.

### 2.3 Cache identity, invalidation and poison/revocation

The cache key/envelope bind schema, source, decoder/transport binding, projection, authority root, release, release manifest, replay, policy trusted-root identity, and event-member root. `_read_bodies` rechecks the expected envelope/key and every body SHA-256 against the selector event ref before returning; a body poison/rehash under an unchanged key is a safe miss and rebuild, not a current SUPPORTED fact. Revoked workload and stale/torn cache tests also refuse before the warmed accelerator. An actual caller-level source/decoder binding change produced a different cache key/file while the C11 release ref remained the same (`logs/source_change_probe.json`). The existing execution-view tests for these paths pass and are part of the reproduced selected suite.

### 2.4 Atomic cache and canonical-carrier lifecycle

The cache writer stages a private `.c11-events-*` file, writes bounded Parquet rows, fsyncs the staged file, atomically replaces the destination and calls a directory fsync. `ParquetC11Carrier.persist` fsyncs each Parquet member, fsyncs the manifest, fsyncs the payload directory, atomically replaces the staged release directory and calls directory fsync on the parent. Tests cover interrupted cache replace, interrupted canonical publish, concurrent cache builders, deletion/rebuild, corruption/trusted rebuild and canonical survival after accelerator deletion.

### 2.5 Exact typed I03/I05 facts

The selected sourcefree suite reproduces the existing Route B/C11/I03/I05 material, including the cold-reopen fixtures with routed/ordered/repeated events, missing optional weight and valid-empty states. `_consumer_material` compares full typed facts, discovery receipts, source releases and repository snapshot identity, not only counts. The cache stores event bodies only; non-event objects, authority snapshots, weights/occurrences/ranks/zero and refusals remain in the canonical release and are reconstructed/validated through the existing repository path.

## 3. Reproduced test results

Runner: `/usr/local/bin/python3` 3.11.3 (same interpreter as the lane), no environment install, TMPDIR under the review lease, sourcefree fixture temp roots only.

```text
40 passed in 14.95s
  test_pre553_c11_execution_view.py
  test_pre553_c11_cold_reopen_i03.py
  test_pre553_carrier_execution.py
  test_pre553_i03_grouping.py
  test_pre553_w03_w04_completion.py

10 passed in 1.54s
  test_pre553_source_backed_c11_facade.py

7 passed in 3.12s
  test_pre553_w03_w04_completion.py -k 'cache_policy or invalidation or recovery or boundary'

3 passed in 2.33s
  test_cache_hit_delete_and_rehashed_same_key_poison_rebuild
  test_stale_cache_and_torn_publication_keep_previous_complete_slot
  test_revoked_workload_never_opens_warmed_accelerator
```

These match the lane's focused claims at the tested scope; no full 12-ID CI, 100000-event benchmark, native/S3/science/actor or protected merge was run.

## 4. Findings — two required defects and one lifecycle gap

### W04-F01 (P1) — legacy environment fallback can masquerade as policy authorization

**Location:** `rawlsing_next/_pre553_w04_cache.py:142-198` (`_legacy_test_policy`, `load_policy`), reached by `rawlsing_next/_pre553_c11_execution_view.py:205-218` and `_compact_public_objects`.

The code treats `PYTEST_CURRENT_TEST` as proof that the process is a pytest test and, if set, accepts `RAWLSING_C11_ACCELERATOR_DIR` below the platform temp root with a hardcoded `PYTEST_TEMP_ROOT_EXPLICIT` policy, `NONRESPONDENT_SOURCEFREE` permission and budget. `PYTEST_CURRENT_TEST` is an ordinary environment variable; any plain process can set it. The independent probe did exactly that in an ordinary Python process (not pytest) and:

- `load_policy()` returned an accepted policy with `authorization_id=PYTEST_TEMP_ROOT_EXPLICIT`;
- `_execute(_fixture())` wrote one `c11-events-*.parquet` cache file under the chosen temp root;
- the legacy root was created by the fallback when absent.

This contradicts the lane claim that “a bare legacy directory environment variable is test-only and cannot become a deployment grant.” The fallback is not cryptographically or process-bound to pytest.

**Minimum exact repair:** remove the `RAWLSING_C11_ACCELERATOR_DIR`/`PYTEST_CURRENT_TEST` fallback from production `load_policy`; make the existing legacy test helper in `test_pre553_c11_execution_view.py` (and any other caller) use an explicit private policy file under `RAWLSING_C11_ACCELERATOR_POLICY` in `tmp_path` (the new completion tests already show the pattern). Do not replace it with another environment marker; if a test-only injection is retained, it must be a non-environment test API unavailable to deployment, and the legacy test blob must be re-reviewed if changed. This preserves the prior accepted source ceiling while removing the deployment masquerade.

### W04-F02 (P2) — directory-fsync failure is swallowed and reported as success

**Location:** `rawlsing_next/_pre553_w04_cache.py:296-306` (`fsync_dir` catches `OSError` and returns), used by `atomic_replace` (`:309-311`) and `pre553_parquet_carrier.py:246,256,282-286`.

The independent probe patched `_pre553_w04_cache.os.fsync` to raise `OSError`. `fsync_dir` returned normally, `atomic_replace` placed the destination, and the destination existed; no exception was surfaced. Thus a failed directory fsync is indistinguishable from success. For the disposable cache this may become a safe miss/rebuild after a crash; for `ParquetC11Carrier.persist`, the method can return a persisted target and report success after a failed parent-directory fsync, so the claimed file+directory durability is not fail-closed. The lane's replace-failure tests do not cover this branch.

**Minimum exact repair:** make `fsync_dir` return a success/failure result or raise on `os.open`/`os.fsync` failure. Cache callers must treat failure as a safe miss/abort (remove the new cache if needed); `ParquetC11Carrier.persist` must raise and clean up/leave no accepted target rather than return success. Add a focused fsync-failure test for both cache and canonical publication. No new engine or store is needed.

### W04-F03 (P3) — crash-orphaned hidden cache staging file survives retention

**Location:** `rawlsing_next/_pre553_w04_cache.py:25` (`CACHE_GLOB = "c11-events-*.parquet"`), `:220-264` (`prune`) and `:300-313` (writer staging prefix `.c11-events-`).

The writer stages with hidden prefix `.c11-events-`, while retention globs only `c11-events-*.parquet`. The independent probe created an old `.c11-events-orphan` under a max_files=1/max_age_seconds=1 policy; `prune` left it present. A hard process crash between staging and commit can therefore leave hidden source-derived cache bytes that are neither reclaimed nor counted against `max_bytes`/`max_files`. Normal abort/replace tests do not cover a hard crash. This is a disposable-cache resource/lifecycle gap, not a false SUPPORTED fact.

**Minimum exact repair:** prune stale hidden `.c11-events-*` staging files by policy age (or a short staging grace period), or stage in a dedicated `staging/` subdirectory cleaned on policy load; include them in retention accounting. They must never be accepted as cache (already true).

## 5. Boundaries and limits

- **No whole-lane/whole-MCR acceptance:** this review accepts only the positive W04 persistence evidence at the tested sourcefree S2 scope. The lane remains `DELIVERED_PENDING_RECEIVING`; two exact repairs are required at this head.
- **Memory/resource utility remains UNPROVED:** no 100000-event benchmark, no cold RSS/wall/disk amortization measurement, no economic acceptance. Test counts are not economic acceptance.
- **No PR895/46b73256 final proof:** PR #895 and the prior 43-pass run are retained as prior capital; no merge, no current protected adoption.
- **No original35/native/science/actor:** no SAV/DTA/DB/original respondent/source-byte read, native/S3 science or actor effect, new issuer, protected merge or CI waiver.
- **No second canonical store/engine:** canonical `ParquetC11Carrier` remains distinct; the cache is derived/disposable and stores event bodies plus envelope metadata.
- **Local S2 only:** tests used explicit nonrespondent sourcefree fixture temp roots; no deployment root or host policy grant is inferred.

## 6. Next exact action

1. Apply W04-F01: remove the environment-only legacy fallback from production `load_policy`; migrate the existing cache test helper to an explicit private policy file under `RAWLSING_C11_ACCELERATOR_POLICY`. Re-run the focused/selected suite and the adversarial counterexample.
2. Apply W04-F02: make directory fsync fail-closed and test cache/canonical fsync failure. Re-run the selected suite and interrupted-publication tests.
3. Apply W04-F03: reclaim stale hidden `.c11-events-*` staging files (or stage in a cleaned subdirectory) and include them in retention/budget. Re-run the lifecycle probe.
4. Re-submit the W04 lane at a new exact head for independent re-review; do not claim whole W03/W04, 12-ID, economic or protected acceptance. PR #895 and protected integration remain untouched; final whole-12 same-head code + economic receiving is still required.

## 7. Review identity and preservation

The review was performed in the required worktree at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`, branch `review/pyat-w03-w04-mcr-w04-r1`, clean. The worktree `rawlsing_next` source tree is full (402 files), not a bad anchor. Exclusive writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/persistence/`. Prior accepted blobs/source ceiling are preserved; no author/HQ/peer/protected write. The actual turn model recorded in `logs/actual-model.json` is `deepseek-v4.1-flash` / `opencode-go` / `max`; no provider/model/account/effort change. Quota `UNKNOWN`.

**Final:** `REVISE` for the W04 persistence lane at `605ce4c`; positive persistence/identity/canonical evidence accepted at tested S2 scope; W04-F01, W04-F02 and W04-F03 require the exact repairs above; whole 12-ID and economic receiving remain open.
