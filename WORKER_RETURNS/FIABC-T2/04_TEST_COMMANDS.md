# FIABC-T2 — Non-Measured Qualification Commands

No command in this file was executed by FIABC-T2. These commands do not authorize measured P2X.

## Compile changed execution surfaces

```bash
python -m py_compile \
  rawlsing_next/ee_p2x_darwin_court_driver.py \
  rawlsing_next/ee_p2x_darwin_stage_backend.py \
  rawlsing_next/pre553_candidate_c_production_binding.py \
  rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py \
  rawlsing_next/tests/test_pre553_candidate_c_production_binding.py
```

## Candidate-C production binding qualification

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_candidate_c_production_binding.py
```

## T2 current six-cell contract qualification

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py
```

## Current-manifest static load

```bash
python - <<'PY'
from pathlib import Path
from rawlsing_next.ee_p2x_darwin_court_driver import load_current_execution_manifest

m = load_current_execution_manifest(
    Path("WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json")
)
pairs = [(c["source"], c["candidate"]) for c in m.document["current_capabilities"]]
assert pairs == [
    ("LITS_I","A"), ("LITS_I","B"), ("LITS_I","C"),
    ("WVS7","A"), ("WVS7","B"), ("WVS7","C"),
]
assert all(c["status"] == "CURRENT_EXECUTABLE" for c in m.document["current_capabilities"])
print("PASS__FIABC_T2_CURRENT_SIX_CELL_MANIFEST")
PY
```

## Historical map immutability / non-current-law check

```bash
python - <<'PY'
from hashlib import sha256
from pathlib import Path
from rawlsing_next.ee_p2x_darwin_court_driver import (
    ContinuationMapError,
    load_current_execution_manifest,
)

p = Path("WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json")
assert sha256(p.read_bytes()).hexdigest() == "ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422"
try:
    load_current_execution_manifest(p)
except ContinuationMapError:
    pass
else:
    raise AssertionError("historical continuation map accepted as current capability law")
print("PASS__HISTORICAL_MAP_IMMUTABLE_AND_NONCURRENT")
PY
```

## Candidate-C historical hard-stop removal guard

```bash
! grep -F 'LiTS-C exact F02 q310/q311 reachability nonqualification' rawlsing_next/ee_p2x_darwin_stage_backend.py
! grep -F 'LiTS-C exact current q310/q311 reachability nonqualification' rawlsing_next/ee_p2x_darwin_stage_backend.py
! grep -F 'WVS-C has no backend execution path' rawlsing_next/ee_p2x_darwin_stage_backend.py
grep -F '_compose_current_candidate_c' rawlsing_next/ee_p2x_darwin_stage_backend.py
grep -F '_assert_r5_canonical_source_root' rawlsing_next/ee_p2x_darwin_stage_backend.py
```

## Exact source-root assertions

```bash
grep -F '7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09' WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json
grep -F '2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d' WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json
```

## Still forbidden

Do not invoke the Darwin driver with `--run` or `--resume` for measured P2X in this layer.

Real-source qualification and measured work remain downstream of the remaining execution-envelope/oracle/instrumentation/terminal layers.
