# Execution Entrypoints

Set these paths after unpacking the transfer bundle:

```bash
export RAWLSING_ROOT="$PWD/Rawlsing_J_Family_Authority_Strategy_Handoff_v40_WORKING"
export S62="$RAWLSING_ROOT/62_P3A_V7_CANDIDATE_EVIDENCE_STAGING_AND_ATOMIC_PROMOTION"
export PGDATA="$PWD/postgres_data_55432"
export PGPORT=55432
export PGHOST=127.0.0.1
export PGDATABASE=rawlsing_p3a_v40_test
export PGUSER=rawlsing_p3a_owner
export PGPASSWORD=rawlsing_p3a_dev
export DSN="host=$PGHOST port=$PGPORT dbname=$PGDATABASE user=$PGUSER password=$PGPASSWORD"
export PYTHONPATH="$S62/code:$S62/validation"
mkdir -p "$S62/postgres" "$S62/outputs"
```

## 1. Install Contracts

Contracts are installed into PostgreSQL by the DDL step after the empty database exists. Keep the file path stable:

```bash
test -f "$S62/sql/p3_postgresql_compatible_ddl_v7_v40.sql"
```

## 2. Start PostgreSQL

```bash
test -d "$PGDATA" || initdb -D "$PGDATA" -U "$PGUSER" --encoding=UTF8
pg_ctl -D "$PGDATA" -l "$S62/postgres/v40_pg.log" -o "-p $PGPORT -c listen_addresses=$PGHOST" start
```

## 3. Rebuild From Empty State

```bash
dropdb -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" --if-exists "$PGDATABASE"
createdb -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$PGDATABASE"
psql "$DSN" -v ON_ERROR_STOP=1 -f "$S62/sql/p3_postgresql_compatible_ddl_v7_v40.sql"
```

## 4. Load Frozen P2-Derived Inputs

```bash
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase contracts
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase membership
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase pairs
```

## 5. Stage Candidates

```bash
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase signatures
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase components
```

## 6. Promote Candidates

```bash
python3 "$S62/code/p3a_v40_load.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN" --phase candidates
```

## 7. Produce Packets

```bash
python3 "$S62/code/p3a_v40_packets.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN"
python3 "$S62/code/p3a_v40_reports.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN"
```

## 8. Run q01-q54

```bash
psql "$DSN" -v ON_ERROR_STOP=1 -f "$RAWLSING_ROOT/49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/validation/P3_DDL_VALIDATION_QUERIES_v7.sql" > "$S62/postgres/v40_populated_q01_q54_raw.tsv" 2> "$S62/postgres/v40_populated_q01_q54_stderr.txt"
```

## 9. Run Fixtures

```bash
python3 "$S62/code/p3a_v40_fixture_lifecycle.py" --root "$RAWLSING_ROOT" --section "$S62" --dsn "$DSN"
```

## 10. Run Verifier

```bash
python3 "$S62/validation/verify_handoff_v40.py" --root "$RAWLSING_ROOT"
```

## 11. Tear PostgreSQL Down

```bash
pg_ctl -D "$PGDATA" -m fast stop
pg_isready -h "$PGHOST" -p "$PGPORT" || true
```
