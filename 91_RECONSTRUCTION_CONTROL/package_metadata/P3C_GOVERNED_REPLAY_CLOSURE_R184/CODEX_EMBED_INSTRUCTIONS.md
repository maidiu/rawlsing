# Codex embedding instructions

1. Run `unpack_payloads.sh`.
2. Treat the unpacked repository as the integration tree. The Git bundle is the authoritative history backup.
3. Start PostgreSQL 15 from the included `offline_runtime` and run `restore_database.sh`.
4. Verify the restored state:

```bash
python repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/validation/validate_p3c_governed_replay_v1.py \
  --section repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION \
  --dsn 'host=127.0.0.1 port=55432 dbname=rawlsing_p3c_work user=oai'
```

Expected: 37 checks passed, zero failed. Also confirm 56 PASS lines in `P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt`.

5. Read:
   - `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/README_FIRST.md`
   - `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/CURRENT_STATE.json`
   - `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/EXACT_CONTINUATION.md`
   - `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/AUTHORITY_SCOPE.md`
6. Use the deterministic CSVs under `authority/` as the downstream integration surface; preserve the database as normalized authority.
7. Build canonical non-GSS J-family authority in the existing GSS-compatible schema. Do not infer response-value portability from proposition identity.
8. Proceed V550J → V551J → V552J. Reopen P3C only for a demonstrated failed invariant or unrepresentable concrete case.
