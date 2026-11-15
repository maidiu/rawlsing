# FIABC-T1 — Non-Measured Qualification Commands

These commands are for the next local qualification layer. They do **not** authorize measured P2X.

## Static I04 packaging court

```bash
python rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py -v
```

## Compile only the transposed Python surfaces

```bash
python -m py_compile \
  rawlsing_next/ee_p2x_darwin_stage_backend.py \
  rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py \
  rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py \
  WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py \
  rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
```

## Exact Git-blob identity checks

```bash
git hash-object rawlsing_next/ee_p2x_darwin_stage_backend.py
git hash-object rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py
git hash-object rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json
git hash-object rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py
git hash-object WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py
git hash-object rawlsing_next/runtime/ee_p2x/RUNTIME_PACKAGING_BINDING.json
git hash-object rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
```

Expected, in order:

```text
b0115ceffe7203c29646faffcbc5adfcfa373488
9406bacfd928393f6a159a46216aa1f7ec129f34
e04e84b76f8b4eb53905276dd025938bf2e5f6fe
11b28416aac5a4899706150721f2f8ac8bb6ee43
504944f9533b7385d201076e2e834b8a9446dee8
25c56abf292175fa5894e5a65362e239eaa55db1
f8d49baecc0c08c0ca40dde2bfd189398b8c150b
```

## Source-root proof checks

```bash
grep -n 'LITS_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"' rawlsing_next/ee_p2x_darwin_stage_backend.py
grep -n 'SOURCE_SHA="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"' WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py
grep -n '"source_sha256": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"' rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json
grep -n 'SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"' rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py
```

## Guard against worker-return executable locators surviving in the live backend

```bash
! grep -F 'WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py' rawlsing_next/ee_p2x_darwin_stage_backend.py
! grep -F 'WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json' rawlsing_next/ee_p2x_darwin_stage_backend.py
! grep -F 'WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py' rawlsing_next/ee_p2x_darwin_stage_backend.py
```

Do not run the measured P2X driver in this layer.
