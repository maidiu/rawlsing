# W04 persistence repair R3 — F01/F02/F03

**Status:** `DELIVERED_PENDING_RECEIVING`

**Branch:** `agent/pyat-w03-w04-mcr-persistence-r2`
**Repair target:** `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`
**Independent review:** `b5f919e65cd2dcc3df46818026a5dc9581566955`
**Source base:** frozen PR895 `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; no PR edit or rebase.
**Scope:** W04 persistence lane only. Whole 12-ID MCR-C, economic, native/S3,
science, actor and protected acceptance remain open.

## Repairs

### W04-F01 — removed legacy environment authorization

The production `load_policy()` now accepts only the explicit private policy file
at `RAWLSING_C11_ACCELERATOR_POLICY`. The former
`PYTEST_CURRENT_TEST` + `RAWLSING_C11_ACCELERATOR_DIR` fallback was removed,
including its code path; no replacement environment marker was introduced.
`LEGACY_ENV` remains only as a historical constant/private test attribute, not an
authorization path.

The existing cache test helper in `test_pre553_c11_execution_view.py` now
creates an explicit private policy file under `RAWLSING_C11_ACCELERATOR_POLICY`
in `tmp_path`. All prior assertions, selectors, poison/ref/topology tests remain
unchanged. An ordinary Python process that sets both spoofed variables produced
`load_policy() is None` and zero cache files (`logs/f01_ordinary_spoof.log`).

### W04-F02 — fail-closed fsync and post-publish cleanup

`fsync_dir` now raises on directory open/fsync failure. Cache publication removes
a destination that became visible before a failed directory fsync, so the caller
sees a safe miss. `ParquetC11Carrier.persist` removes only the newly published
target after a post-replace fsync failure; the prior complete canonical release
remains reopenable. Replace failures remain observed and leave no unaccepted
partial target.

Focused tests cover cache directory fsync failure, cache file fsync failure,
canonical parent-directory fsync failure after publication, interrupted replace,
and prior-good-artifact preservation.

### W04-F03 — hidden crash staging retention

Retention now includes hidden `.c11-events-*` staging files. Stale hidden
staging files are removed by a bounded staging grace/age policy; live concurrent
writers inside the grace window are excluded from budget deletion. Final cache
files and hidden staging participate in orphan accounting, while canonical
Parquet remains outside the disposable cache root. The regression creates an
old hidden orphan, an active hidden staging file and a canonical release, then
verifies the orphan is removed, the active staging survives, and canonical
reopen remains exact.

## Changed files

- `rawlsing_next/_pre553_c11_execution_view.py`
- `rawlsing_next/_pre553_w04_cache.py`
- `rawlsing_next/pre553_parquet_carrier.py`
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py`
- `rawlsing_next/tests/test_pre553_c11_execution_view.py` (only the private
  cache setup helper; no prior assertion changed)

No facade, ingest, repository, benchmark module, peer/HQ or protected file was
edited.

## Evidence

- RED retained from the independent review at `605ce4c4`: legacy fallback wrote
  one cache, directory fsync failure was swallowed with destination present, and
  a hidden staging orphan survived prune.
- GREEN at this candidate:
  - ordinary spoofed process: no policy/no cache write;
  - cache directory/file fsync failure: safe miss and later rebuild;
  - canonical parent fsync failure: new target removed, prior canonical release
    remains reopenable;
  - hidden orphan pruned, active staging preserved, canonical release intact;
  - full selected sourcefree suite: **45 passed in 15.52s**;
  - source-backed facade regression: **10 passed in 4.65s**;
  - focused `cache_policy`: **3 passed**;
  - focused `invalidation`: **1 passed**;
  - focused `recovery`: **7 passed**;
  - focused `boundary`: **1 passed**.

Exact files, blobs and commands are in `01_CHANGED_FILES_AND_BLOBS.tsv`,
`02_TEST_RECEIPTS.md` and `03_RED_TO_GREEN.md`.

## Remaining

Full same-head 12-ID MCR evidence, integrated W03 cold/bench results, independent
code review and independent economic review remain open. This repair does not
claim whole W03/W04 or whole MCR acceptance, a deployment host grant, or
economic PASS. PR #895 remains frozen at `46b73256`.
