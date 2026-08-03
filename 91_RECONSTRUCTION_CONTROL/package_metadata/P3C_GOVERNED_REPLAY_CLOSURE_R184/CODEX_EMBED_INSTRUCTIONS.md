# Codex embedding instructions

Run these commands from the extracted package directory:

```bash
sha256sum -c verification/SHA256SUMS.txt
./unpack_payloads.sh
./setup_python.sh
./start_postgresql.sh
./restore_database.sh
./verify_restored_checkpoint.sh
```

The expected final return is 37 checks passed, zero failed, followed by `restored checkpoint verification PASS`. The post-close matrix must contain exactly 56 PASS lines and no FAIL line.

Then read:

- `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/README_FIRST.md`
- `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/CURRENT_STATE.json`
- `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/EXACT_CONTINUATION.md`
- `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/AUTHORITY_SCOPE.md`

Use the deterministic CSVs under `repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/authority/` as the downstream integration surface. Preserve the restored PostgreSQL database as normalized authority.

Build canonical non-GSS J-family authority in the existing GSS-compatible schema. Do not infer response-value portability from proposition identity. Then proceed V550J → V551J → V552J. Reopen P3C only for a demonstrated failed invariant or unrepresentable concrete case.

The PostgreSQL start helper supports either a non-root caller or a root caller when the local `oai` user exists. A different non-root environment may set `PGDATA`, `PGSOCK`, and `PGPORT` before running it.
