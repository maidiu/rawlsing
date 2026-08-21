# SR07 P2 WVS7 R4 real-source scale confirmation

Disposition: `P2_BLOCKED__RESOURCE_TRIPWIRE`

The exact WVS7 SAV was verified (`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`, 97,220 rows × 613 variables). The accepted `decode_sav(source_path)` path and R4 streaming representation were used without runtime changes.

The bounded 1,024-row court passed: 627,712 events, direct DuckDB count and second query both 627,712, streaming audit 627,712, canonical storage 6,649,174 bytes (10.5927144932708 bytes/event), and cleanup succeeded. A fresh-process repeat matched source identity, frontier, object cardinalities, canonical member bytes, reconstruction samples, and DuckDB results.

The hostile user-missing microproof passed on observed row 49 / Q152 / variable ordinal 224. The reconstructed R4 material retained raw `-2.0`, `FORMAT_USER_MISSING_RANGE`, declaration `[-5.0,-1.0]`, row ordinal, variable ordinal/name, and source SHA without semantic interpretation. Q153–Q155 were also retained as distinct physical slots in the bounded reconstruction sample.

The actual full 59,595,860-event run was supervised externally and terminated at 4,298,940,416 bytes RSS against the 4,294,967,296-byte hard tripwire after 16,302.943611564988 seconds. It did not emit completed full-source traversal or canonical-storage measurements; no projection is substituted.

No source-semantic certification, semantic authority, full C11 release, PostgreSQL, SQLite, persistent DuckDB, or `DATABASE_URL` use was performed. The full-source carrier and scratch driver were not committed.

Required token: `PRE553_SR07_P2_WVS7_R4_REAL_SCALE_RETURNED`
