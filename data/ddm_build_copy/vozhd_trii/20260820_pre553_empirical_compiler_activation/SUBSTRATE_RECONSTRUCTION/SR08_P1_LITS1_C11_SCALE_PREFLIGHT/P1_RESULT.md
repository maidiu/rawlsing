# SR08-P1 LiTS I bounded C11 execution-scale preflight

Disposition: `P1_BLOCKED__RESOURCE_TRIPWIRE`

Starting HEAD: `7633f84473dcd63e3acb00247ac094bbc6ef4fde`
Source SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
Shape: 29,002 rows × 1,198 variables
Decoder: `decode_dta(source_path, encoding="latin1")`
Authority: `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`
Scratch driver SHA-256: `cef0c102f3dbaa1802f79a8a84d271db8199c686169a53c615ad6aed2a39b635`

The execution-only candidate authority was explicitly scoped `P1_EXECUTION_ONLY__NO_SOURCE_SEMANTIC_CERTIFICATION`. Physical cells were retained in raw-value payloads with source SHA, row ordinal, variable ordinal/name, raw storage value, physical missing state, source declaration, and raw label where present. Semantic response state was `INVALID_UNRESOLVED`; no native-ID, country, weight, routing, or text-encoding meaning was promoted.

S1 (16 rows) completed: 19,168 events, 3,814,750 Parquet bytes, semantic hash `c0d4a0e74cca3bf615b34095ed143bb1af0693b1920e1644499dff0a16e056c3`, peak supervised RSS 1,131,312 KiB. Direct DuckDB identity/count/multiple-query checks passed; no persistent DuckDB, PostgreSQL, SQLite, or DATABASE_URL path was used.

S2 (64 rows) completed: 76,672 events, 13,823,355 Parquet bytes, semantic hash `5fd28ff55afeb9d1993ce08732808843641667a988e7590c924d3c107b12f6d0`, peak supervised RSS 1,604,384 KiB. A fresh S2 repeat completed at 2,061,024 KiB and matched source SHA, frontier, semantic hash, relation digests, and public/internal object-inventory digests exactly.

S3 (256 rows; 306,688 expected events) was terminated by the external supervisor at the hard 4-GiB RSS tripwire: peak 4,238,408 KiB during full reopen. This is fail-closed scale evidence. S4 was not run.

Full-source estimates are `PROJECTION_ONLY`, based only on completed S1/S2 linear slopes: candidate construction about 145 GiB peak RSS; I02 validation about 158 GiB; Parquet persistence about 303 GiB; full reopen about 437 GiB; Parquet about 5.63 GiB. Full-source materialization is plainly unsafe on this machine.

Required token: `PRE553_SR08_P1_LITS1_C11_SCALE_PREFLIGHT_RETURNED`
