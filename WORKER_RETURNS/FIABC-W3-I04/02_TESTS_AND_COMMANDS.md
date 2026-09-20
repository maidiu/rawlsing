# FIABC-W3-I04 — Tests and Later Commands

## Added test

`rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py`

The test is source-byte/static-contract focused and does not open LiTS-I or WVS7 empirical source bytes.

## Run on the integrated/local tree

From repository root:

```bash
python rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py -v
```

Compile the exact I04 Python surfaces without executing P2X:

```bash
python -m py_compile \
  rawlsing_next/ee_p2x_darwin_stage_backend.py \
  rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py \
  rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py \
  WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py \
  rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
```

Mechanically reconfirm the exact Git blobs:

```bash
git hash-object rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py
git hash-object rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json
git hash-object rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py
git hash-object WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py
```

Expected, in order:

```text
9406bacfd928393f6a159a46216aa1f7ec129f34
e04e84b76f8b4eb53905276dd025938bf2e5f6fe
11b28416aac5a4899706150721f2f8ac8bb6ee43
504944f9533b7385d201076e2e834b8a9446dee8
```

## Integration qualification boundary

After HQ fans in the other Wave-3 implementation branches, rerun the I04 test on the integrated tree before any source×candidate measurement.

This worker does not authorize or specify a measured P2X command. Live materializer consumption belongs to the integrated non-dispositive qualification sequence after the succession-preflight, parity-oracle, equal-work, Candidate-C, and terminal-verifier repairs compose.
