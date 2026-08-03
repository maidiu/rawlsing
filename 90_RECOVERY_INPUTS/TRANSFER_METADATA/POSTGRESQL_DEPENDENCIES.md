# PostgreSQL Dependencies

- PostgreSQL major version observed: `15`
- `psql --version`: `psql (PostgreSQL) 15.14 (Homebrew)`
- `pg_ctl --version`: `pg_ctl (PostgreSQL) 15.14 (Homebrew)`
- Required extension: `pgcrypto` (`CREATE EXTENSION IF NOT EXISTS pgcrypto;`)
- Database encoding assumption: `UTF8`
- Locale assumption: compatible text ordering only; no locale-sensitive ordering is used for authoritative hashes, which sort canonical JSON/text keys in Python.
- Runtime port used by current reproducer: `55432`
- Runtime bind used by current reproducer: `127.0.0.1`
- Schema/search path: `p3a_v27_shadow, public`
- Nondefault startup flags used: `-p 55432 -c listen_addresses=127.0.0.1`
- Generated database/data directory is excluded from the transfer bundle and must be recreated from the included DDL and loaders.
