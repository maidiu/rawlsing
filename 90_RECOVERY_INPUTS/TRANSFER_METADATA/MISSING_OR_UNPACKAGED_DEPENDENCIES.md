# Missing Or Unpackaged Dependencies

The transfer ZIP includes the copied v40 working tree with embedded ZIP archives, bytecode, caches, and generated database state excluded.

## Not Included

- PostgreSQL server/client binaries. Use the versions recorded in `POSTGRESQL_DEPENDENCIES.md`.
- Python interpreter and third-party packages. Use `PYTHON_DEPENDENCIES.txt`.
- PostgreSQL data directory `/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/postgres_data_55432`; it is generated runtime state and must be recreated from included DDL and loaders.
- Prior cumulative ZIP archives and duplicate upstream ZIPs; these were intentionally excluded from the transfer bundle.

## Included In Transfer For Inheritance Claims

- `57_P3A_V7_CANDIDATE_IDENTITY_MIGRATION_AND_FIXTURE_CLOSURE/P3A_V35_CANDIDATE_IDENTITY_MIGRATION.csv` MISSING FROM TRANSFER COPY
- `57_P3A_V7_CANDIDATE_IDENTITY_MIGRATION_AND_FIXTURE_CLOSURE/P3A_V35_ALL_CANDIDATE_HASH_RECONCILIATION.csv` MISSING FROM TRANSFER COPY
- `49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/validation/P3_DDL_VALIDATION_QUERIES_v7.sql` MISSING FROM TRANSFER COPY

## External Immutable v35 Package

No dependency is claimed on an unpackaged external v35 ZIP unless the receiving environment chooses to audit against it independently. The operative inherited files needed by the current v40 execution are present in the transfer tree and listed above with exact hashes where found.
