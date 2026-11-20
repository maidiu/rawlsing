# Exact test receipt

## Command

```bash
cd "$P0_WORKTREE"
/usr/bin/time -l env PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  -m pytest -q -o addopts='' -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/ANVIL_P0_TWO_SAVED_WAVES_NATIVE_I03_20261120_R3/evidence/native_stream_26.junit.xml \
  rawlsing_next/tests/test_pre553_anvil_stream_native_i03.py \
  rawlsing_next/tests/test_pre553_anvil_stream_carrier_qualification.py
```

## Results

- `test_pre553_anvil_stream_native_i03.py`: **8/8 pass**
- `test_pre553_anvil_stream_carrier_qualification.py`: **18/18 pass**
- Total: **26 passed**, 0 failed, 0 skipped
- Pytest time: 1.46 s
- Wall time: 1.96 s
- Max RSS: 117,522,432 bytes
- Swaps: 0

## Sparse fixture first fault

The first invocation collected 26 tests but failed 2 cases because the sparse
checkout omitted the already-committed R2 typed-decision fixture. The exact
HEAD blob was restored with `git show HEAD:<path>`; no product code changed.
The full 26-test rerun then passed. See `evidence/native_stream_26.out` and
`evidence/native_stream_26.junit.xml`.
