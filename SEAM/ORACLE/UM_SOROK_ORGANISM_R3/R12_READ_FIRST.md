# SOROK REMONT R12 — repair of independent R11 negative court

Read `R12_REPAIR_RECEIPT.md`, `R12_SOURCE_SHA256.json`, and the existing 71-record `REMONT/SOROK/OPEN_DEFECTS` pair in the published branch. This is a repair **stacked on** R11 PR #1190, not a protected merge or an alternative organism. Historical R11 source identity: `39f6972089858ee968e73b2e731005c71a8055dd`. Original live REMONT current source as reconciled: #1171 `c0b7cd0589a7aa0ca5bd9f53c42f07ab03933ef7`.

From archive root:
```
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m unittest tests.test_independent_r11_receiving -v
```

Execution: full 246/246 PASS normal and -O; pytest 246 passed + 14 subtests; reviewer 6/6 PASS after reproducing five original red subcases; demo and cold SQLite chain valid. Python 3.11 R12 and new independent receiving remain pending. Original R11 Python 3.11 succeeded on user machine.
