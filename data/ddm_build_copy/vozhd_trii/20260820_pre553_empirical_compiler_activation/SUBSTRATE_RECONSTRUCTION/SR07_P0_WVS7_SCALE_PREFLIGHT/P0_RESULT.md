# SR07-P0 WVS7 scale preflight result

Disposition: `P0_PASS__FULL_CERTIFICATION_MAY_BE_ADJUDICATED`

The exact source copy entered the accepted SR06 runtime with `decode_sav(source_path)`, no encoding override, and matched SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`. Shape was 97,220 rows by 613 variables. The ordinary WVS path remained metadata-first and chunked; no full frame was required.

The 2,048-row bounded replay consumed exactly 1,255,424 cells per pass. The 8,192-cell batch digest, 32,768-cell batch digest, and deterministic restart 8,192-cell digest were all:

`41864260dd8e2f9e8911ef4a3101d1fa9546405772a72ee294a36798fa2882ae`

All passes preserved row ordinals 1..2048 and variable ordinals 1..613. The process did not retain the complete bounded cell universe merely to hash it. Q152-Q157 each retained nonempty source-native missing declarations; metadata was recorded without semantic interpretation.

Resource evidence: metadata/open took 1.6424 s, RSS rose from 15,699,968 to 94,867,456 bytes. The 8,192-cell pass took 36.0430 s at 34,831 cells/s with 121,163,776-byte process peak; the 32,768-cell pass took 18.7304 s at 67,026 cells/s with 130,990,080-byte process peak; restart 8,192 took 35.6486 s at 35,217 cells/s with 130,990,080-byte process peak.

Full-source physical traversal is `PROJECTION_ONLY`: 59,595,860 cells project to about 28.52 minutes at the 8,192-pass rate or 14.82 minutes at the 32,768-pass rate. This is not executed and is not a certification estimate. Observed bounded-pass memory was stable and safe continuation remained plausible.

This is not source certification. No C11 release, semantic authority, I03/I05 certification, PostgreSQL, database URL, or source modification was used.

Required token: `PRE553_SR07_P0_WVS7_SCALE_PREFLIGHT_RETURNED`
