# PRE553 PD01-PG01 — local execution

Assignment: `PRE553-PD01-PG01`

Exact base: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Target: populated Rawlsing Postgres, WVS Wave 7 v6.0.0 physical-reality receipt only.

This is deliberately a dumb local step.

Run:

```bash
psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 \
  -f data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/POPULATED_DATA/PD01_PG01/PD01_WVS_W7_POPULATED_PROBES.sql \
  > PD01_WVS_W7_POPULATED_PROBE_RESULTS.txt 2>&1
```

If Rawlsing uses an existing equivalent configured connection source instead of `DATABASE_URL`, use that existing configuration without changing credentials or database state.

The SQL begins a `READ ONLY` transaction and ends with `ROLLBACK`. It performs no writes, migrations, C11 population, source mutation, or runtime modification.

Do not add exploratory SQL. Do not interpret results locally. Do not inspect unrelated filesystem state.

Return the complete `PD01_WVS_W7_POPULATED_PROBE_RESULTS.txt` receipt unchanged, plus command, redacted connection-source description, exit code, file size, and SHA-256.

If execution fails, preserve and return the complete failure receipt. If configured Postgres access cannot be established, return `BLOCKED_MISSING_POPULATED_POSTGRES_ACCESS` and the exact missing prerequisite.
