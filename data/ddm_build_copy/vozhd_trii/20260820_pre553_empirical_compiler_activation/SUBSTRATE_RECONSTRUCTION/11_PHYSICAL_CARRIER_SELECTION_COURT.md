# PRE553 SUBSTRATE RECONSTRUCTION — PHYSICAL CARRIER SELECTION COURT

Status: `READY_TO_EXECUTE__G_SR03_G_SR05_ACCEPTED`

Operational execution authority: `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`.

## Governing decision order

The physical carrier is selected in this strict order:

1. **FLAWLESS EFFECTIVENESS** — exact preservation/replay of the frozen carrier fixture and exact answers under I03/I05-equivalent workload semantics.
2. **FAST** — lowest practical latency/throughput cost for Rawlsing's actual analytical workload, not synthetic database prestige tests.
3. **LIGHT** — minimal disk duplication, resident memory, operational services, configuration, maintenance and failure surface.

A faster or lighter carrier that fails information equivalence is disqualified, not traded off.

## Architecture neutrality

C11 is an information/semantic contract, not a database-product contract. Accepted `C11Repository` is explicitly file-neutral. This court selects persistence/query machinery beneath the accepted I02/I03 interfaces. It may not reopen I01-I07 or V553-V558 semantics.

## Candidates

The court tests:

- `PARQUET_DUCKDB_DIRECT` — canonical immutable Parquet relations queried directly by embedded DuckDB;
- `DUCKDB_NATIVE` — the same logical relations materialized in one DuckDB database file;
- `POSTGRES_EPHEMERAL` — the same logical relations in a fresh local disposable PostgreSQL cluster, never the live Rawlsing database;
- `SQLITE` — the same logical relations in a local SQLite file, subject to the same disk/time safety gates.

No candidate receives authority merely because historical Rawlsing already uses it.

## Correctness law

Correctness is absolute. Every candidate must reproduce the same frozen event/respondent/metadata digests and exact query oracle. Wrong answer, lost physical state, respondent reassociation, nondeterministic replay, or unexplained coercion is `CARRIER_DISQUALIFIED_CORRECTNESS`.

SR04 does **not** certify WVS/LiTS survey semantics. G-SR07/G-SR08/G-SR09 own source-semantic certification. SR04 is allowed to use source-native physical facts plus explicitly benchmark-only deterministic coordinates/risk-set flags to exercise the accepted query/discovery shapes without creating survey authority.

## Performance and lightness law

After correctness passes, compare the frozen batch workload. Candidate build/load time is recorded separately from query time. Persistent disk bytes, peak RSS, background-service requirement, configuration burden and number of persistent empirical copies are recorded.

A candidate within 10% of the fastest full frozen batch is an operational speed tie; the lighter tied candidate wins.

A materially heavier carrier may win only if it supplies a measured capability or speed benefit the lighter carrier cannot supply.

## Safety law

The live Rawlsing PostgreSQL database is never written or benchmarked against.

The executor must preserve a hard free-disk reserve and enforce candidate build/query time limits. A candidate that cannot be instantiated safely inside the frozen budget is `OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT`; the executor may not free user data, enlarge disks, change the live DB, or relax the budget.

## Expected but nonbinding hypothesis

`PARQUET_DUCKDB_DIRECT` is the current hypothesis because the substrate is append-only/analytical and C11 caches are nonauthoritative. This hypothesis has zero dispositive weight. Only the bakeoff receipt may select the carrier.
