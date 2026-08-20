# CODEX HANDOFF — PRE553 PD01-PG01

Repository: `maidiu/rawlsing`

Branch: `agent/vozhd-trii-pre553-pd01-pg01-local-execution-pack`

Exact campaign base: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Assignment: `PRE553-PD01-PG01`

You are a DUMB READ-ONLY LOCAL POSTGRES EXECUTOR.

Read only these assignment files first:

- `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/POPULATED_DATA/PD01_PG01/PD01_WVS_W7_LOCAL_EXECUTION.md`
- `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/POPULATED_DATA/PD01_PG01/PD01_WVS_W7_POPULATED_PROBES.sql`

Your only mission is to execute that exact SQL against the configured Rawlsing Postgres database and return the complete execution receipt.

Do NOT:
- inspect the broader filesystem;
- search the repository beyond the smallest bounded inspection needed to locate the existing Postgres connection configuration;
- reason about Rawlsing architecture;
- modify code or data;
- run migrations;
- write to Postgres;
- inspect unrelated files;
- generate additional exploratory SQL;
- repair or reinterpret the probe battery;
- perform C11 population or any source adapter work.

The SQL file is authoritative for what to query.

Use the existing Rawlsing database connection configuration. Redact secrets in your return.

Return:
1. exact command executed;
2. connection source used, credentials redacted;
3. exit code;
4. exact path to `PD01_WVS_W7_POPULATED_PROBE_RESULTS.txt`;
5. file size and SHA-256;
6. whether output reached `PRE553 PD01-PG01 COMPLETE`;
7. exact failure evidence if anything failed.

Do not summarize or interpret the SQL results.

Success token:
`PRE553_PD01_PG01_POPULATED_WVS_W7_RECEIPT_COMPLETE`

Blocked token:
`BLOCKED_MISSING_POPULATED_POSTGRES_ACCESS`
