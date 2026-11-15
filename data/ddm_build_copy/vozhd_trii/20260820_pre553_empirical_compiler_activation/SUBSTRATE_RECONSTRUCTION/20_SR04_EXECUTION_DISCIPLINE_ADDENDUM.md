# SR04 EXECUTION DISCIPLINE ADDENDUM

Status: `BINDING_HQ_ADDENDUM__SUPERSEDES_EXECUTION_SHAPE_ONLY`

This addendum binds `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md` without changing its candidate set, proving sources, query semantics, correctness threshold, or selection law.

## 1. Required two-stage acceptance

The harness must expose two mechanically separate stages.

### Stage A — implementation contract tests

Runs only on a tiny deterministic synthetic fixture created inside the disposable SR04 work root.

It must complete in seconds, not minutes, and must prove:

- all four logical relations can be materialized by every available candidate;
- all 16 named query IDs execute the **correct frozen logical shape**;
- each candidate query result is normalized and compared to an independent Python oracle;
- intentionally corrupted expected output causes a correctness failure;
- each candidate's stored relations are streamed/read back from that candidate and reproduce the neutral fixture digests;
- intentionally corrupted stored data causes a replay-digest failure;
- PostgreSQL cluster start/connect/query/stop lifecycle works without closing the connection before timing;
- cleanup is confined to the disposable SR04 root;
- no path reads `DATABASE_URL`.

Required stage-A token:

`PRE553_SR04_SYNTHETIC_CONTRACT_TESTS_PASS`

No WVS7/LiTS I raw-source decode is allowed before this token is produced by the current committed harness.

### Stage B — real proving fixture and carrier measurements

Only after Stage A passes may the harness decode the exact frozen WVS7/LiTS I source files and execute the scored bakeoff.

## 2. Neutral fixture checkpoint/reuse

The real neutral fixture is an expensive deterministic derivative of exact frozen source bytes. Once one committed harness version successfully:

1. verifies both source hashes;
2. passes every Section-6 hostile-source invariant in the frozen contract;
3. writes the four neutral Arrow relations;
4. computes their exact canonical relation digests;
5. writes `FIXTURE_MANIFEST.json`, `FIXTURE_DIGESTS.json`, and `QUERY_ORACLE.json`;

that fixture may be retained under a disposable local checkpoint directory and reused by later **implementation-only** harness revisions if and only if all of the following are true:

- source hashes are identical;
- neutral schema version is identical;
- variable-selection algorithm/version is identical;
- all four Arrow files' byte SHA-256 values are recorded and match;
- all four canonical relation digests match;
- `FIXTURE_MANIFEST.json` and `QUERY_ORACLE.json` digests match;
- the later revision did not modify source decoding, neutral-row construction, physical-state classification, raw-value canonicalization, variable selection, respondent identity construction, benchmark coordinate construction, or oracle semantics.

If any of those producer/oracle paths changed, the checkpoint is invalid and Stage B must rebuild from source.

Checkpoint reuse is an execution optimization only. The returned SR04 receipt must state whether the neutral fixture was `BUILT_FROM_RAW_THIS_RUN` or `REUSED_EXACT_DIGEST_CHECKPOINT` and include all checkpoint hashes.

## 3. Query correctness is dispositive

For every candidate and every Q00-Q15:

- execute the candidate SQL;
- normalize the returned result into a canonical JSON-compatible representation;
- compare against the independently computed oracle for that exact query ID;
- weighted floating results use only the frozen tolerance;
- any mismatch yields `CARRIER_DISQUALIFIED_CORRECTNESS` with query ID and expected/observed digest.

Merely executing SQL without error is never correctness.

## 4. Stored read-back is dispositive

Each candidate must reproduce the frozen relation digests by reading/streaming the relations **from its stored physical representation**:

- Parquet: read Parquet files;
- DuckDB-native: `SELECT` from DuckDB tables;
- PostgreSQL: `COPY`/cursor stream from the ephemeral cluster tables;
- SQLite: cursor stream from SQLite tables.

Computing a candidate replay digest from the original pandas/Arrow fixture is forbidden and invalidates that candidate measurement.

## 5. Exact query-shape assertions

The Stage-A tests must include structural assertions for at least:

- Q03: two-variable same-respondent joint;
- Q04: five-variable same-respondent joint across Q152-Q156;
- Q05: I_PSU ordinary/raw=1 risk set AND Q152=1;
- Q06: weighted Q152 calculation from matched respondent W_WEIGHT;
- Q08: branch_id=1 AND Q152×Q153 joint;
- Q09: XOR benchmark coordinate condition + Q152 distribution;
- Q10: all three subgroup conditions + Q152×Q153 joint;
- Q11/Q15: grouped grid outputs, not scalar row counts;
- Q14: both WVS duplicate-target count and LiTS native-id distinct count.

A scalar count is not a lawful substitute for a required distribution/joint/grid.

## 6. Publication discipline

Another full raw-source run is forbidden until:

- `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md` defects are all closed by code inspection/tests;
- the current harness is committed;
- Stage A passes from that exact committed HEAD;
- HQ/Codex return includes the Stage-A token and test receipt.

The worker may iterate quickly on the harness using only Stage A until it passes. It must not repeatedly rebuild WVS7/LiTS I during Stage-A debugging.
