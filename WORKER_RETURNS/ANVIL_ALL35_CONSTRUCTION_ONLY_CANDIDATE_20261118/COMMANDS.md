# Candidate commands

Scratch baseline/checkout of exact accepted code:

```bash
git -C /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER \
  archive aee95429609c372564e996c2d3d3eb30e9253cbf rawlsing_next | tar -x -C /tmp/anvil_construction_only_scratch
```

Candidate test run from the isolated scratch tree:

```bash
cd /tmp/anvil_construction_only_scratch
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_all35_construction_only_candidate.py \
  rawlsing_next/tests/test_pyat960_s1e_source_i02.py
```

Result: 13 passed in 3.43 s. The focused candidate test performs one tiny
sourcefree construction, fresh cold reopen, exact body/identity/source/routing
checks, and one pre-read resolver denial.
