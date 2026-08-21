# SR07-P1 WVS7 bounded C11 execution-scale preflight

Disposition: `P1_BLOCKED__RESOURCE_TRIPWIRE`

The exact WVS7 source matched SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d` and shape 97,220 rows by 613 variables. The accepted unmodified decoder was invoked as `decode_sav(source_path)` with no encoding override. Scratch driver SHA-256: `3c9b89c0eae20c19139aa8a11c1b80eec1de6394078ab08e4b65905f06203eeb`.

The hostile microproof found an observed Q152 cell at source row 49, variable ordinal 224: raw `-2.0`, physical state `FORMAT_USER_MISSING_RANGE`, declaration `-5.0..-1.0`. The execution-only projection preserved raw value, physical state, declaration, row ordinal, variable ordinal/name, and raw label material. No semantic meaning was assigned.

S1 completed the actual decoder → execution-only projection → physical-to-I02 bridge → `validate_c11_source_release()` → Parquet persist → reopen → verified direct DuckDB path for 32 rows and 19,616 events. Peak RSS was 969,048,064 bytes; Parquet bytes were 7,086,206. Direct DuckDB returned the exact event frontier, opened exact release identity, supported multiple queries, and created no persistent `.duckdb`.

S2 completed the same path for 128 rows and 78,464 events. Candidate, validation, persistence, and reopen peak RSS were respectively 803,733,504; 848,945,152; 3,248,009,216; and 3,302,440,960 bytes. Parquet bytes were 26,944,776. Post-disposal current RSS was 814,964,736 bytes. Direct DuckDB checks passed.

The fresh-process S2 repeat matched source identity, semantic release hash `faf7058b3186ceddd3a96b9aa1a55927231dd7c3d6b212b7009cffa0ab3aefea`, all relation logical digests, public inventory hash `2162d74fd02ad2811df004f8e411dd6f40a38b21e41a6f2ef95d405c511c39ae`, internal inventory hash `7db36c9d4d31a4c813776a1632bcdcb58914213a9e0f087025ae98a46e864734`, object counts, and Parquet disk bytes. Parquet byte-for-byte comparison was not performed; semantic/logical equality is dispositive.

S3 (512 rows; 313,856 events) was attempted in a fresh externally supervised child. The 4 GiB RSS tripwire fired at 4,296,179,712 bytes after 366.151 seconds; the child terminated with SIGKILL. S4 was not run.

Full WVS7 estimates are `PROJECTION_ONLY`, based on two-point linear extrapolation from completed S1/S2. Candidate construction projects to about 489 GiB peak RSS, I02 validation to 524 GiB, persistence to 2,135 GiB, and full reopen to 2,186 GiB; projected Parquet disk is about 18.7 GiB. These estimates are not execution and are superseded by the observed S3 tripwire.

The authority status for all created snapshots was `P1_EXECUTION_ONLY__NO_SOURCE_SEMANTIC_CERTIFICATION`. No native identity, country meaning, missingness semantics, routing, or weight role was inferred. PostgreSQL, SQLite, `DATABASE_URL`, persistent DuckDB, runtime modification, and source modification were not used.

Required token: `PRE553_SR07_P1_WVS7_C11_SCALE_PREFLIGHT_RETURNED`
