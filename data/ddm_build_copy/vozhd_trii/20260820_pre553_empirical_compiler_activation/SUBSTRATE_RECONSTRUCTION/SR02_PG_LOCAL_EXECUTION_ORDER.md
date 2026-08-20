# SR02-PG — DUMB LOCAL DB PROVENANCE RECEIPT — REVISION 2

Repository: `maidiu/rawlsing`
Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ in the launch command. Verify it before execution; do not substitute `latest` or another branch.

MISSION: Execute the checked-in `SR02_CURRENT_DB_PROVENANCE_PROBE.sql` against the current Rawlsing Postgres database READ ONLY and return its complete output unchanged.

REVISION-2 NOTE:
The first SR02 execution reached P03 and failed because the original query joined/grouped the full response carrier and exhausted PostgreSQL temporary disk. That was a probe-shape defect, not a database semantic failure. Revision 2 replaces P03/P04 with information-equivalent low-temp provenance queries. Do NOT free/expand database disk merely to reproduce the superseded query.

The runner has no authority to interpret the database, fix data, alter SQL, modify code, or inspect unrelated machine state.

Required preflight:
- `git rev-parse --show-toplevel`
- `git remote -v`
- `git status -sb`
- `git rev-parse HEAD`
- verify exact HQ launch HEAD;
- verify `DATABASE_URL` or already-governed connection mechanism;
- do not print secrets.

Set:
`ORDER_ROOT=data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION`

Execution (fresh R2 receipt; do not overwrite the failed R1 receipt):
`psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 -f "$ORDER_ROOT/SR02_CURRENT_DB_PROVENANCE_PROBE.sql" > SR02_CURRENT_DB_PROVENANCE_RESULTS_R2.txt 2>&1`

Return:
- exact checkout HEAD;
- exact command;
- exit code;
- result path;
- byte size;
- SHA-256;
- complete `SR02_CURRENT_DB_PROVENANCE_RESULTS_R2.txt`;
- completion token;
- `git status -sb` after execution.

Success token inside SQL output:
`PRE553_SR02_CURRENT_DB_PROVENANCE_RECEIPT_COMPLETE`

No database writes. No runtime writes. No interpretation. Do not commit execution output unless HQ separately orders it.
