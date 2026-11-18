# Candidate commands and evidence

Baseline checkout of the exact accepted code:

```bash
git -C /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER \
  archive aee95429609c372564e996c2d3d3eb30e9253cbf rawlsing_next \
  | tar -x -C /tmp/anvil_construction_only_scratch
```

Focused native-child proof (one producer child, then fresh reader children):

```bash
cd /tmp/anvil_construction_only_scratch
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_all35_construction_only_candidate.py
```

Existing Q2 regression together with focused proof:

```bash
cd /tmp/anvil_construction_only_scratch
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_all35_construction_only_candidate.py \
  rawlsing_next/tests/test_pyat960_s1e_source_i02.py
```

Patch application check against a clean `aee954` archive:

```bash
git apply --check candidate.patch  # exit 0
```

The producer and reader are distinct native child processes. The reader refuses
if the recorded producer PID is still alive. Positive mode compares full family,
`RespondentIdentity`, and `RoutingEligibilityFact` payload digests. Negative
modes are `wrong_current`, `revoked`, and `wrong_root`.
