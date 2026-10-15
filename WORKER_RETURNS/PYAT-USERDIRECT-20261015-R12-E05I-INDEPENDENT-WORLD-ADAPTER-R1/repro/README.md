# Reproduce the E05I court

Run from an isolated private `maidiu/rawlsing` checkout with the sealed commits available and Python 3.11 + pytest. All staged files and generated artifacts stay under this return. `runtime/` is ignored and reconstructible; no Desktop source tree is copied.

```
python3 WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/repro/stage.py
python3 WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/repro/run_suites.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/tests --import-mode=importlib -p no:cacheprovider --junitxml=WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/observations/independent.xml
python3 WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/repro/run_cold.py
```

The independent court deliberately asserts correct contract invariants and retains genuine failures. It has no xfails, skips, owner replacements, mocks or monkeypatches. An exception inside original code is not converted to a positive pass. Some hostile cases deliberately change caller-supplied fixture metadata or the source registry; those attack inputs are identified explicitly. The profiler observes real calls without wrapping or modifying them. Original suite passes do not cancel independent invariant failures.

Stage uses exact `git show COMMIT:PATH` and verifies each full NUL-header Git blob hash against `git rev-parse COMMIT:PATH`. The passport stores exact original suite argv/cwd/exits; the execution receipt stores the independent argv/exit and cold process exits. `source_manifest.json` includes source path, commit, blob, SHA256 and byte count for every staged file. The independent trace records actual `module.__file__`, rechecked Git blob, source commit and actual Python callee frames.
