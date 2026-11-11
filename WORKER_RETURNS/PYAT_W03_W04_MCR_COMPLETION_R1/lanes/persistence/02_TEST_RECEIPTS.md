# Persistence lane test receipts

Runner: `/usr/local/bin/python3` 3.11.3. Sourcefree S2 only. No 100000-event
benchmark, source/respondent/SAV/DTA/DB read, native/science/actor effect, or
protected merge was performed.

## Full selected sourcefree set

Command:

```
/usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/persistence/logs/full_selected_junit.xml
```

Result: `40 passed in 12.71s` (`logs/full_selected.log`).

## Source-backed facade regression

Command:

```
/usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py --maxfail=1
```

Result: `10 passed in 1.09s`.

## Focused completion selections

| Selection | Command | Result |
|---|---|---|
| `cache_policy` | `pytest ... test_pre553_w03_w04_completion.py -k cache_policy --junitxml=logs/cache_policy_junit.xml` | `2 passed, 5 deselected` |
| `invalidation` | `pytest ... -k invalidation --junitxml=logs/invalidation_junit.xml` | `1 passed, 6 deselected` |
| `recovery` | `pytest ... -k recovery --junitxml=logs/recovery_junit.xml` | `3 passed, 4 deselected` |
| `boundary` | `pytest ... -k boundary --junitxml=logs/boundary_junit.xml` | `1 passed, 6 deselected` |

## What the tests exercise

- Policy root absent/malformed/unowned/unauthorized/too-small: no cache writes.
- Authorized private sourcefree policy: automatic repeat cache activation.
- Envelope/key mismatch on authority, source, projection, release, replay,
  schema, policy root or member root: safe miss.
- Poisoned/rehashed body and revoked workload: not returned as a current fact.
- Interrupted cache replacement: previous complete cache retained, no partial
  final file.
- Interrupted canonical Parquet publish: no accepted partial release; trusted
  rebuild works.
- Canonical Parquet survives deletion of the disposable accelerator and still
  reopens the actual I03/I05 consumers.
- Existing cold-reopen fresh-process tests remain passing at the same fixture
  scope.
