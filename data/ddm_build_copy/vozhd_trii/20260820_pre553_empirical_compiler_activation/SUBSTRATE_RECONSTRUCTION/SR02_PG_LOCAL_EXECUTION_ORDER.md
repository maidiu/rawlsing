# SR02-PG — DUMB LOCAL DB PROVENANCE RECEIPT — REVISION 3

Repository: `maidiu/rawlsing`
Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it exactly. Do not substitute `latest`.

## MISSION

Execute the checked-in `SR02_CURRENT_DB_PROVENANCE_PROBE.sql` against the current Rawlsing Postgres database READ ONLY and return its complete output unchanged.

## WHY R3 EXISTS

R1 contained an unnecessarily expensive full response↔respondent aggregate and exhausted PostgreSQL temp disk.

R2 fixed that shape but exposed a second HQ defect: P11 assumed `driver_aggregates.wave` although the exact supplied schema defines `driver_aggregates.survey_year`.

HQ has now completed the static reconciliation that should have preceded R1:

- traced the frozen pre-reconstruction V550 runtime database dependency cone;
- classified unrelated legacy surfaces out of the live probe;
- checked **155 explicit required relation/column pairs** against exact `Rawlsing_WVS_public_schema(2).sql`: zero mismatches;
- checked all **36 physical `respondentsDemo*` tables** for every field R3 uses: 36/36 PASS;
- checked V550-required view columns against the supplied view definitions;
- embedded a live schema preflight at the beginning of R3 so live schema drift fails before any large scan.

Binding HQ authorities:

- `14_PRE_RECONSTRUCTION_DB_DEPENDENCY_MAP.md`
- `13_DATABASE_PROVENANCE_ADJUDICATION_LAW.md`
- `SR02_SCHEMA_REFERENCE_AUDIT.csv`

Do not reopen or reinterpret them.

## EXECUTOR AUTHORITY

You may:

- verify exact checkout/head;
- use the already-governed `DATABASE_URL` connection mechanism without printing secrets;
- execute the checked-in SQL exactly once into a fresh R3 receipt;
- compute file size/SHA-256 and return the receipt.

You may not:

- alter SQL;
- free/expand PostgreSQL storage;
- modify database contents;
- modify runtime/governance;
- inspect unrelated machine state;
- interpret or repair returned data;
- merge R1/R2 partial output into R3;
- commit execution artifacts.

## PREFLIGHT

Run only:

- `git rev-parse --show-toplevel`
- `git remote -v`
- `git status -sb`
- `git rev-parse HEAD`
- verify exact HQ launch HEAD;
- verify `DATABASE_URL` or the already-governed local connection mechanism without exposing credentials.

Set:

`ORDER_ROOT=data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION`

## EXECUTION

Fresh R3 receipt only:

`psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 -f "$ORDER_ROOT/SR02_CURRENT_DB_PROVENANCE_PROBE.sql" > SR02_CURRENT_DB_PROVENANCE_RESULTS_R3.txt 2>&1`

Do not impose a 30-second wrapper timeout. Allow the checked-in read-only probe to finish or fail naturally.

## RETURN TO HQ

Return:

- exact checkout HEAD;
- exact command;
- exit code;
- result path;
- byte size;
- SHA-256;
- complete `SR02_CURRENT_DB_PROVENANCE_RESULTS_R3.txt`;
- completion token presence/absence;
- `git status -sb` after execution.

Required success token:

`PRE553_SR02_CURRENT_DB_PROVENANCE_RECEIPT_COMPLETE`

If the embedded live-schema preflight fails, return that failure unchanged. Do not troubleshoot it locally.
