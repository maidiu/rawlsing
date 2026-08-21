# VOZHD TRII — SR04 PHYSICAL CARRIER BAKEOFF EXECUTION CONTRACT

Status: `FROZEN_HQ_AUTHORITY__MECHANICAL_IMPLEMENTATION_AND_EXECUTION_ALLOWED`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

This contract selects only the physical persistence/query carrier beneath accepted PRE553 C11/I03 semantics. It does not redesign C11, certify survey meaning, change I03/I05 truth conditions, or touch V553+.

# 1. Candidate set

The candidate IDs are exact:

1. `PARQUET_DUCKDB_DIRECT`
2. `DUCKDB_NATIVE`
3. `POSTGRES_EPHEMERAL`
4. `SQLITE`

No candidate may be silently omitted. A candidate that cannot lawfully/safely execute receives an exact typed nonviability disposition and measurements sufficient to explain why.

`POSTGRES_EPHEMERAL` means a new disposable local PostgreSQL cluster under the SR04 work root. The current Rawlsing database is forbidden as a benchmark target.

# 2. Frozen proving sources

Use only these exact source snapshots:

## WVS7 SAV

- file: `WVS Wave 7.sav`
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- expected rows: `97220`
- reader: `pyreadstat.read_sav(user_missing=True, apply_value_formats=False)`
- no encoding override.

Required WVS hostile variables:

`Q152,Q153,Q154,Q155,Q156,Q157,I_PSU,D_INTERVIEW,B_COUNTRY,W_WEIGHT,S018,Q223`

## LiTS I DTA

- file: `LiTS_I.dta`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- expected rows: `29002`
- reader: `pyreadstat.read_dta(user_missing=True, apply_value_formats=False, encoding="latin1")`
- encoding authority status: `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

Required LiTS hostile variables:

`id,country,countryname,weight_0,weight_1,weight_2,q707,q509,q304a,q304b,q204,q203,q201,q501,q503,q505,q306,q307,q301_1,q301_11`

Do not infer semantic meaning from the LiTS compatibility-decoded labels in this court.

# 3. Deterministic 24-variable selection per source

Each source contributes exactly 24 variables.

Algorithm:

1. retain every required hostile variable above in the listed order;
2. verify each required variable exists;
3. append variables in source-native variable ordinal order, skipping duplicates, until exactly 24 variables are selected;
4. freeze the resulting list and ordinals into `FIXTURE_MANIFEST.json` before any candidate is built.

The resulting event fixture contains every respondent row for every selected variable. No respondent sampling is allowed.

Expected event-row count is therefore:

`97220*24 + 29002*24 = 3029328`.

If the generated event count differs, stop with `BLOCKED_SR04_FIXTURE_EVENT_COUNT_MISMATCH`.

# 4. Frozen carrier-neutral logical fixture

Generate one neutral staging fixture outside every candidate's scored storage. Arrow IPC is the staging transport only and has no candidate authority.

Required logical relations:

## `sources`

- `source_id` TEXT
- `source_file` TEXT
- `source_sha256` TEXT
- `source_format` TEXT
- `source_row_count` INTEGER
- `source_variable_count` INTEGER
- `reader_encoding_override` TEXT
- `reader_encoding_authority_status` TEXT

Source IDs are exact: `WVS_W7`, `LITS_I`.

## `respondents`

- `source_id` TEXT
- `row_ordinal` INTEGER, zero-based physical source-row ordinal
- `respondent_key` TEXT, deterministic SHA-256 over exact source SHA + `:` + decimal row ordinal
- `benchmark_coord_a` INTEGER = row_ordinal modulo 2
- `benchmark_coord_b` INTEGER = floor(row_ordinal / 2) modulo 2
- `benchmark_branch_id` INTEGER = row_ordinal modulo 5
- `benchmark_risk_eligible` INTEGER = 0 iff row_ordinal modulo 7 = 0, else 1

The `benchmark_*` fields are explicitly `BENCHMARK_ONLY__NO_SOURCE_SEMANTIC_AUTHORITY`.

## `variables`

- `source_id` TEXT
- `var_name` TEXT
- `var_ordinal` INTEGER
- `variable_label` TEXT
- `missing_spec_json` TEXT
- `value_labels_json` TEXT
- `storage_type` TEXT
- `display_format` TEXT

## `events`

- `source_id` TEXT
- `row_ordinal` INTEGER
- `respondent_key` TEXT
- `var_name` TEXT
- `var_ordinal` INTEGER
- `physical_state` TEXT
- `raw_value_key` TEXT
- `raw_value_num` DOUBLE/REAL nullable
- `raw_value_text` TEXT
- `value_label` TEXT

Required physical states:

- `ORDINARY`
- `SYSTEM_MISSING`
- `SPSS_USER_MISSING`
- `STATA_EXTENDED_MISSING` if observed.

The fixture generator must preserve `user_missing=True` behavior and must classify WVS values against source-native SPSS missing ranges. It may not map source codes to canonical semantic states.

# 5. Canonical raw-value representation

Every event receives a deterministic `raw_value_key` used for exact cross-engine equality:

- system missing: `M:SYSTEM`
- Stata extended missing: `M:STATA:<native-code>`
- numeric finite integer: `N:<integer>`
- numeric finite noninteger: `N:<shortest deterministic decimal representation>`
- string: `S:<exact decoded string>`

`raw_value_text` contains the deterministic textual representation used to construct the key, or empty string for system missing.

All cross-engine digest checks use text/key/state fields rather than binary floating-point serialization.

# 6. Neutral-fixture correctness before candidate work

The mechanical harness must prove, at minimum:

## WVS7

- rows = `97220`;
- Q152 SPSS user-missing total = `2557` with `-1=1620`, `-2=501`, `-5=436`;
- Q153 SPSS user-missing total = `4877` with `-1=957`, `-2=1480`, `-3=2388`, `-5=52`;
- Q154 user-missing = `1802`;
- Q155 user-missing = `3777`;
- Q156 user-missing = `1745`;
- Q157 user-missing = `3626`;
- I_PSU SPSS user-missing raw `-4` = `31137`;
- D_INTERVIEW raw `858069901` occurs `1000` times;
- W_WEIGHT and S018 are distinct variables.

## LiTS I

- rows = `29002`;
- native `id` has `29002` distinct ordinary values;
- each of `weight_0`, `weight_1`, `weight_2` has `29000` ordinary + `2` system-missing values;
- no Stata extended missing value is observed in the selected fixture;
- raw country code `9` occurs `1000` times;
- ordinary labeled codes in the q* variables remain `ORDINARY`, not physical missing merely because their labels may denote DK/refusal/not-applicable.

Any failure stops the court before candidate timing.

# 7. Exact fixture digests

Before candidate creation compute and freeze:

- canonical `sources` digest;
- canonical `respondents` digest;
- canonical `variables` digest;
- canonical `events` digest.

For respondents/events, hash UTF-8 canonical JSON lines in exact sort order:

- respondents: `(source_id,row_ordinal)`;
- events: `(source_id,var_ordinal,row_ordinal)`.

Event digest fields are exactly:

`source_id,row_ordinal,respondent_key,var_name,var_ordinal,physical_state,raw_value_key,raw_value_text,value_label`.

Each candidate must stream the stored data back in those sort orders and reproduce the exact digests. Sampling is insufficient.

# 8. Candidate physical layouts

All candidates store the same four logical relations.

## PARQUET_DUCKDB_DIRECT

- one Parquet file per logical relation;
- events physically ordered by `(source_id,var_ordinal,row_ordinal)`;
- respondents ordered by `(source_id,row_ordinal)`;
- ZSTD compression;
- event row-group target `131072` rows;
- queried directly by an in-process DuckDB connection using Parquet scans/views;
- no DuckDB database file becomes authoritative.

## DUCKDB_NATIVE

- one disposable DuckDB database file;
- four materialized logical tables;
- no semantic denormalization;
- candidate may use DuckDB-native physical ordering but may not add benchmark-answer caches.

## POSTGRES_EPHEMERAL

- one fresh disposable local cluster/database under the SR04 candidate directory;
- never connect to or modify `DATABASE_URL`;
- required indexes after load:
  - events `(source_id,var_name,row_ordinal)`;
  - events `(source_id,row_ordinal,var_name)`;
  - events `(source_id,var_name,physical_state,raw_value_key)`;
  - respondents unique `(source_id,row_ordinal)`;
- normal durable defaults may be relaxed only inside this disposable cluster when the exact setting is recorded. No setting may change query semantics.

## SQLITE

- one SQLite database file;
- same four logical tables;
- required indexes identical in logical key order to PostgreSQL;
- benchmark-only safe bulk-load pragmas may be used if recorded and restored/not relevant after the disposable file is deleted.

# 9. Frozen correctness/query oracle

Compute expected results independently in Python/pandas from the decoded 24-variable wide frames before candidate query execution.

Every candidate executes equivalent SQL for these named queries and must match the oracle exactly except weighted floating sums, which use absolute/relative tolerance `1e-9` after finite-value validation.

1. `Q00_SOURCE_EVENT_COUNTS`
2. `Q01_HOSTILE_STATE_COUNTS`
3. `Q02_WVS_Q152_DISTRIBUTION`
4. `Q03_WVS_Q152_Q153_JOINT`
5. `Q04_WVS_Q152_TO_Q156_5WAY`
6. `Q05_WVS_RISKSET_Q152` — I_PSU physical state `ORDINARY`, Q152 raw `N:1`
7. `Q06_WVS_WEIGHTED_Q152` — sum W_WEIGHT numeric values for Q152 raw `N:1`, ordinary W_WEIGHT only
8. `Q07_WVS_RESPONDENT_LOOKUP` — exact row ordinal `50000`, all selected variables
9. `Q08_BRANCH_CONDITIONED_COTRAVEL` — benchmark_branch_id `1`, Q152 × Q153
10. `Q09_XOR_COORDINATE` — exactly one of benchmark_coord_a/benchmark_coord_b is 1, Q152 distribution
11. `Q10_RECURSIVE_SUBGROUP` — benchmark_risk_eligible=1 AND benchmark_branch_id IN (1,2) AND benchmark_coord_a=1, Q152 × Q153
12. `Q11_SIMPSON_GRID_SHAPE` — grouped counts over benchmark_coord_a × benchmark_branch_id × Q152 raw value
13. `Q12_LITS_WEIGHT_STATE_COUNTS`
14. `Q13_LITS_Q301_1_DISTRIBUTION`
15. `Q14_NATIVE_IDENTITY_HOSTILES` — WVS D_INTERVIEW duplicate target and LiTS id distinct count
16. `Q15_MINORITY_GRID_SHAPE` — Q152 distribution by benchmark_branch_id

The oracle is frozen into `QUERY_ORACLE.json` before the first candidate executes.

# 10. Performance protocol

Correctness gates execute once first. Only passing candidates are timed.

For every passing candidate record:

- candidate build/materialization wall seconds;
- candidate index-build seconds separately where applicable;
- cold open/connect seconds;
- each Q00-Q15 query wall time for 1 unscored warm-up + 5 scored repetitions;
- per-query median and p95;
- one scored sequential Q00-Q15 batch wall time after warm-up;
- candidate persistent disk bytes after build/index and before cleanup;
- peak candidate-process RSS;
- required background-service count;
- dependency/product versions and relevant settings.

No result cache containing precomputed query answers is allowed. Normal engine/page/OS cache behavior is allowed and is why cold and warm measurements are both retained.

# 11. Disk/time safety gate

The harness work root must be under a disposable local temp directory, default `/private/tmp`.

Before staging:

- record free disk bytes;
- reserve at least `5 GiB` free at all times;
- if neutral staging cannot be created while preserving this reserve, return `BLOCKED_INSUFFICIENT_SAFE_LOCAL_DISK` and stop without deleting user files.

Each candidate executes sequentially. Candidate scored storage is deleted after its result/digests/measurements are safely recorded, before the next candidate starts.

Per-candidate hard storage budget:

`min(6 GiB, free_bytes_immediately_before_candidate - 5 GiB)`.

If the computed budget is <= 0, candidate disposition is `OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_RESERVE`.

If candidate storage exceeds the budget, stop that candidate, clean only its disposable directory, and record `OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_BUDGET`.

Per-candidate build/index wall-time ceiling: `600 seconds`.
Per individual query ceiling: `120 seconds`.

A timeout yields `OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__TIME_BUDGET`, not a semantic/correctness failure.

Never delete or modify anything outside the disposable SR04 work root.

# 12. Dependency handling

Required benchmark Python packages:

- existing `pandas` and `pyreadstat` used by SR03;
- `pyarrow` for neutral Arrow IPC and Parquet;
- `duckdb` for both DuckDB candidates;
- PostgreSQL Python driver only for the ephemeral candidate.

If `pyarrow`, `duckdb`, or the PostgreSQL driver is absent, the executor may create an isolated temporary virtual environment under the disposable SR04 root and install only the missing benchmark dependencies. Exact resolved versions and `pip freeze` are recorded in `ENVIRONMENT.json`. No repo/global Python environment may be mutated.

If local PostgreSQL server binaries (`initdb`/`postgres`/`pg_ctl`) are unavailable after checking PATH and `pg_config --bindir`, `POSTGRES_EPHEMERAL` receives `OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__SERVER_BINARIES_UNAVAILABLE`.

# 13. Selection rule

1. Disqualify every candidate with any correctness/digest mismatch.
2. Candidates blocked by disk/time/tool availability are operationally nonviable in the current Rawlsing environment and cannot win over a correct fully measured candidate.
3. Among fully measured correct candidates, fastest scored Q00-Q15 batch wins unless within 10% of the fastest.
4. Candidates within 10% are a speed tie; among them choose the lightest using, in order:
   - fewer required background services;
   - fewer persistent empirical copies;
   - lower persistent disk bytes;
   - lower peak RSS;
   - lower configuration/maintenance burden.
5. The selected product/layout is still replaceable beneath C11; product identity never becomes semantic law.

The harness must mechanically compute a provisional selection from these rules. HQ adjudicates and freezes the final selection.

# 14. Required returned artifact set

Return only the small receipt/metrics package, not candidate databases or neutral staging data:

`SR04_CARRIER_BAKEOFF_RESULTS/`

- `RECEIPT.json`
- `ENVIRONMENT.json`
- `FIXTURE_MANIFEST.json`
- `FIXTURE_DIGESTS.json`
- `QUERY_ORACLE.json`
- `CANDIDATE_RESULTS.json`
- `PROVISIONAL_SELECTION.json`
- `STDOUT.txt`
- `STDERR.txt`

Create a deterministic ZIP of this result directory and return size + SHA-256.

Success token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

The result package must identify the exact repository HEAD containing the executed harness and the exact harness SHA-256.

# 15. Implementation confinement

The local worker may implement or repair **only**:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

and only to satisfy this frozen benchmark contract.

It may not modify `rawlsing_next/**`, source files, Postgres production data, accepted PRE553 runtime tests, or any other governance file.

If a contract ambiguity blocks a deterministic implementation, return `BLOCKED_SR04_CONTRACT_AMBIGUITY:<exact ambiguity>` rather than deciding architecture.
