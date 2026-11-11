# W04 repair R3 test receipts

Runner: `/usr/local/bin/python3` 3.11.3. Sourcefree S2 only. No 100000-event
benchmark, source/respondent/SAV/DTA/DB read, native/science/actor effect,
environment install or protected merge.

## Full affected sourcefree set

```
/usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/persistence/REPAIR_R3/logs/full_selected_junit.xml
```

Result: `45 passed in 15.52s` (`logs/full_selected.log`).

## Source-backed facade regression

```
/usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py --maxfail=1
```

Result: `10 passed in 4.65s`.

## Focused repair selections

| Selection | Result |
|---|---|
| `-k cache_policy` | `3 passed, 9 deselected` |
| `-k invalidation` | `1 passed, 11 deselected` |
| `-k recovery` | `7 passed, 5 deselected` |
| `-k boundary` | `1 passed, 11 deselected` |

Logs and JUnit receipts are under `logs/`.

## F01 ordinary-process spoof

```
TMPDIR=.../REPAIR_R3/tmp /usr/local/bin/python3 - <<'PY'
# sets PYTEST_CURRENT_TEST + RAWLSING_C11_ACCELERATOR_DIR, no policy
# imports load_policy/_execute; asserts load_policy() is None and zero cache files
...
PY
```

Result: `{'load_policy': None, 'cache_files': 0}` (`logs/f01_ordinary_spoof.log`).

## RED/GREEN anchors

- RED review head: `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`.
- RED findings: independent review `b5f919e65cd2dcc3df46818026a5dc9581566955`,
  `reviews/persistence/FINDINGS.jsonl` (`W04-F01`, `W04-F02`, `W04-F03`).
- GREEN: current candidate full selected suite and repair logs above.
- No prior 100000-event or economic acceptance is inferred from test counts.
