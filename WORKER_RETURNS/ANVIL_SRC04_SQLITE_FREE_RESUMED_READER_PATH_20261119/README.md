# Resumed release reader-only recovery

The running R6 producer may publish under `<run>/releases`; the frozen reader expects `<run>/private`. This return stages a reader-only entry for the already-running output.

- allow only `<run>/releases/<expected 64-hex digest>` directly under an exact 0700 run root
- verify manifest SHA, stream schema/roots, member hashes/counts, locator, current authority and symlinks through the existing native reader
- no move, rewrite, rebuild, source decode, or real checkpoint access
- optional `--test-current` is sourcefree test-only; actual recovery omits it and uses `sqlite_free_witness._grant`

```bash
PYTHONPATH=WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_RESUMED_READER_PATH_20261119:WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118 \
python3 WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_RESUMED_READER_PATH_20261119/resumed_reader.py \
  --run-root <exact-0700-resumed-run-root> --layout resumed \
  --release-digest <expected-digest> --manifest-sha256 <manifest-sha> \
  --roots-json '<roots-json>' --binding-dir WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118
```
