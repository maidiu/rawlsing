# Persistence lane return — W04 governed compact persistence

**Status:** `DELIVERED_PENDING_RECEIVING`
**Scope:** one independent lane of the whole W03/W04 MCR-C contract. This return
does not accept the whole contract or replace the independent code/economic
receiver.

**Branch:** `agent/pyat-w03-w04-mcr-persistence-r2`
**Candidate commit:** recorded after the candidate commit is created and pushed.
**Source base:** frozen PR895 `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; source
tree present at the repaired anchor `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`.
PR895 was not advanced or rebased.

## Delivered W04 focus

| Obligation | Result |
|---|---|
| `W04-COLD-PERSIST-REOPEN` | Existing `ParquetC11Carrier` remains the canonical physical carrier; persist/reopen is fsync/replace hardened and tested through the real cold-reopen I03/I05 fixture. |
| `W04-GOVERNED-DEFAULT` | An explicitly configured host policy (`RAWLSING_C11_ACCELERATOR_POLICY`) activates the private accelerator automatically for eligible sourcefree repeat workloads; absent/invalid/unauthorized/absent-root policy makes no cache write. A bare legacy directory environment variable is test-only and cannot become a deployment grant. |
| `W04-AUTHORITY-INVALIDATION` | Cache key and Parquet metadata envelope bind schema, policy root, authority root, source, projection, release, release manifest, replay and member root. Envelope/key mismatch is a safe miss; stale/poison material cannot be returned as a current hit. |
| `W04-ATOMIC-LIFECYCLE` | Cache writes stage in the authorized root, fsync the staged file, atomically replace, and fsync the directory. Interrupted replacement leaves the previous complete cache or a safe miss. Canonical Parquet publishing is separately fsync/replace hardened; interruption leaves no accepted partial release. |
| `W34-PRODUCT-BOUNDARIES` | Accelerator remains derived, disposable and separate from the canonical `ParquetC11Carrier`; deleting the accelerator does not remove the canonical release. Existing I02/C11/I03/I05 public ABIs are unchanged. |

## Exact implementation

Changed/produced code:

- `rawlsing_next/_pre553_c11_execution_view.py` — governed policy resolution,
  cache envelope/key, atomic cache write, safe read/refusal and retention.
- `rawlsing_next/pre553_parquet_carrier.py` — fsync/atomic publication of the
  existing canonical Parquet release; no second store or query engine.
- `rawlsing_next/_pre553_w04_cache.py` — new host-policy/retention/atomic helper.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` — focused
  `cache_policy`, `invalidation`, `recovery` and `boundary` tests.

The reviewed compact body/test blobs remain the basis: production
`986f327aa18053edc61bd837cdded02bbf8388d9` and test
`8e8effa58579af0c3326ecd4af7e159947abe4ec`. No facade, ingest, repository,
benchmark module or peer/HQ artifact was edited.

## Policy and cache contract

A governed policy file has schema `PYAT_C11_ACCELERATOR_POLICY@1` and explicit:

- absolute private host root, owned by the current user and not group/world
  accessible;
- `source_permission` limited to nonrespondent sourcefree values for this lane;
- `authorization_id`;
- `retention_budget` with positive `max_bytes`, `max_files`, `max_age_seconds`.

An absent policy, malformed policy, missing/unowned/non-private root,
unauthorized source permission or exhausted budget yields no cache write. The
legacy `RAWLSING_C11_ACCELERATOR_DIR` path is accepted only for the existing
pytest tests below the platform temporary root; it is not a deployment grant.

The production cache key/envelope includes the source/projection/authority/
release/replay/schema roots and the policy trusted-root identity. A cache is
accepted only when its envelope matches the current exact release and policy;
otherwise it is ignored and rebuilt from the current sealed release. The
canonical Parquet carrier is never treated as the disposable cache, and the cache
is never treated as scientific authority.

## Test evidence

Executed with `/usr/local/bin/python3` 3.11.3:

- Full selected sourcefree set:
  `40 passed in 12.71s` — execution view, cold reopen, carrier execution, I03
  grouping and the new completion tests.
- Source-backed facade regression: `10 passed in 1.09s`.
- `-k cache_policy`: `2 passed`.
- `-k invalidation`: `1 passed`.
- `-k recovery`: `3 passed`.
- `-k boundary`: `1 passed`.

No 100000-event benchmark was run in this lane; the benchmark lane owns that
measurement. Existing review blob evidence was retained, not re-reviewed here.

## Remaining integration / limits

- This is a sourcefree S2 candidate, not native/original35, science, actor,
  protected merge, or a deployment host grant.
- A production host owner must still supply and authorize a policy root and
  retention budget. The test temporary root used by the tests is not that grant.
- Full 12-ID MCR-C completion, independent code/economic review, cross-lane
  integration, and protected receiving remain open.
- No W03 cold-memory or benchmark lane claim is made by this persistence lane.

## Source and evidence

- `01_CHANGED_FILES_AND_BLOBS.tsv` — exact changed files and Git/SHA-256 blobs.
- `02_TEST_RECEIPTS.md` — exact commands and results.
- `03_POLICY_AND_CACHE_CONTRACT.md` — policy/envelope/atomic contract and limits.
- `04_HANDOFF_AND_INTEGRATION.md` — cross-lane handoff.
- `logs/` — raw pytest logs and JUnit receipts.
