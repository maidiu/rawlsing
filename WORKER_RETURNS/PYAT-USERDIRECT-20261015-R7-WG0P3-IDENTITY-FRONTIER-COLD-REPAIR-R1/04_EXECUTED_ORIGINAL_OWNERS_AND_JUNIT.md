# Executed Original Owners and JUnit

## Real Owner Calls (Verified by WG0J)

| Owner | Calls | Method |
|-------|-------|--------|
| `ingest_c11_source_release` | 3 | REAL C11 seal |
| `execute_empirical_query` | 3 | REAL I03 computation |
| `BatchExecutionRunner.run` | 1 | REAL batch execution |

## Owner Blobs (Pinned)

| Module | Blob SHA |
|--------|----------|
| `pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` |
| `pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `pre553_c11_repository.py` | `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` |
| `pre553_c11_ingest.py` | `37cd35fa2e3420a3eea272a2902e96ab9ba38aba` |
| `pre553_c11_integrity.py` | `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd` |
| `pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` |
| `pre553_empirical_authority.py` | `ca65a7fd4d52f0c44447434559b1d09412e7aa39` |

## JUnit

- File: `observations/junit_wg0p3.xml`
- Tests: 36
- Passed: 36
- Failed: 0
- Errors: 0
- Skipped: 0

## Test Coverage

All 20 WG0J failure clusters covered plus additional hostiles:
- Swapped release identity
- Stripped HELD frontier
- Stale permission
- Cold payload forgery
- Native missing codes
- MR inconsistency
- Data leaf mutation

## Preserved Values

- ORD-01: 1/2/2/1/0 over 6
- ORD-05: 0/2/1/1/0 over 4
- MR-02: 4 profiles over 4, indicator totals {food:2, rent:2, health:2, education:1, none:1}

## Positive Conditional

One PRODUCED conditional through ordinary batch product path: joint respondent risk set R_JOINT_ORD_RT, same-person joined carrier/risk evidence, result yes=1/no=1/denominator=2.
