# Exact 459 blobs and non-vendor red/restore

**F1 base:** `1973d28ed4ba4c9e58c9d96fbe358445dddc929c`

**F2 launch:** `83be0a8c676242c920e0c414695f9dcda1c476e3`

**R2 source:** `598d9e9eaba5143950c63317705fd09104fbf463`, tree `1161ce3d990ca78fe1b97c915dc86e559f17236b`

## Original RED

The original F1 verifier is extracted from immutable commit `1973d...` as `/tmp/f2_f1_original_verify.py` (SHA-256 `18dbd92f...`). A copy of the exact 459-file base is changed only in `joined/session.py`; all paths and `SOURCE_MANIFEST.json` remain unchanged.

```sh
printf '\n# F2_NONVENDOR_TAMPER\n' >> /tmp/f2_r2_tamper/joined/session.py
python3 /tmp/f2_f1_original_verify.py --dest /tmp/f2_r2_tamper --repo "$F2_REPO"
```

Observed:

```text
exit 0
{
  "schema": "RRIF_E_R2_BASE_VALIDATION@1",
  "ok": true,
  "errors": [],
  "expected_files": 459,
  "actual_files": 459,
  "vars": 444
}
```

The original F1 `apply.sh` on the same tampered target also proceeded:

```text
exit 0
RRIF_E_PACKET_APPLIED_NOT_MERGED
final regular files: 640
```

That was the exact reviewer RED. The manifest remained `7cfcb467...`.

## Repaired RED

The corrected verifier is at the F1 packet path on the F2 branch, SHA-256 `029fd404a96388a2c3b74d2f38858916f8ad8ba2c66013a4f453c8c7784f1cc3`.

```sh
python3 "$PACKET/verify_r2_base.py" --dest /tmp/f2_r2_tamper --repo "$F2_REPO"
```

Observed:

```text
exit 1
{
  "schema": "RRIF_E_R2_BASE_VALIDATION@1",
  "ok": false,
  "errors": [
    "R2_BLOB_MISMATCH:joined/session.py"
  ],
  "expected_files": 459,
  "actual_files": 459,
  "vars": 444
}
```

The manifest SHA stayed `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`; the path count stayed 459.

Corrected `apply.sh` stops before writing:

```text
exit 3
RRIF_E_BASE_R2_IDENTITY_MISMATCH: STOP before write
```

Destination fingerprint before and after the failed apply is identical; the target remains 459 files. Receipts: `receipts/apply_stop_before.sha`, `receipts/apply_stop_after.sha`, `receipts/apply_stop_unchanged.txt`.

## Restore

Replacing the tampered `joined/session.py` with the exact original bytes and re-running the corrected verifier:

```text
exit 0
expected_files: 459
actual_files: 459
errors: []
```

The original file blob is `ea820ec3e30a2825c3d0d8c5dc66e812afdda40b08f9cc0a8c868c8b3e0dd0da`.

## Complete-tree checks

The corrected verifier does all of the following before returning success:

- obtains all 459 records from `git ls-tree -r -z 598d9e9e...` under the exact R2 subtree;
- carries mode, object type, Git blob object id and path;
- walks the destination with `lstat` and does not follow symlinks;
- rejects symlinks, non-regular nodes and mode/type mismatches;
- requires exactly the expected 459 regular files, with no missing or extra path;
- computes the Git SHA-1 blob of every actual file's bytes and compares it with the expected blob for all 459 files;
- retains the exact manifest SHA and 444 vendor row checks.

The regression covers:

- exact R2 PASS;
- non-vendor tamper FAIL and exact restore PASS;
- vendor tamper FAIL;
- symlink substitution FAIL;
- `apply.sh` exit 3 with byte-identical destination.

## Commands and JUnit

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -o addopts='' -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-RRIF-E-F2-FULL-R2-BLOB-GATE-R1/tests/test_verify_r2_base_full_blob.py \
  --junitxml=WORKER_RETURNS/SOROK-RRIF-E-F2-FULL-R2-BLOB-GATE-R1/junit/f2_blob_gate.xml
```

Observed: `1 passed`.

| Evidence | Location |
|---|---|
| original F1 verifier RED | `receipts/original_f1_red.json` |
| original F1 apply RED | `receipts/original_f1_apply_red.out` |
| corrected verifier RED | `receipts/f2_tamper_red.json` |
| corrected apply STOP | `receipts/apply_stop.out`, `receipts/apply_stop.err` |
| exact restore | `receipts/f2_exact_restore.json` |
| F2 regression JUnit | `junit/f2_blob_gate.xml` |
| exact code diff | `receipts/verify_r2_base.diff` |
