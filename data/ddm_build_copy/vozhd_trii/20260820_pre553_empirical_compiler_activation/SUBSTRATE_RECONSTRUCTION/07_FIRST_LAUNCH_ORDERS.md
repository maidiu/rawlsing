# FIRST LAUNCH ORDER SEQUENCE

## ORDER SR01 — SOURCE BYTE CENSUS — HQ/browser
Status: `ACCEPTED`
Inputs: `surveys.zip`, `WVS Wave 7.sav.zip`, `LiTS_I.dta.zip` retained outside Git as source evidence.
Output: `SOURCE_BYTE_INVENTORY.csv`.
Observed: 35 real source files, 31 SAV, 4 DTA. AppleDouble packaging artifacts excluded.
Gate: G-SR01.

## ORDER SR02 — LEGACY WRITER + DB SURFACE CENSUS — HQ/browser
Status: `ACTIVE`
Inputs: `etl.zip`, `etl(1).zip`, `backfill.zip`, public schema, authority-reconcile schema retained as source/historical evidence.
Outputs: `LEGACY_WRITER_INVENTORY.csv`, `DATABASE_SURFACE_INVENTORY.csv`.
Current static perimeter: 61 historical scripts with relevant empirical surface contact; 63 relevant declared DB surfaces; 25 SAV-reader scripts and zero explicit `user_missing=True` preservation discovered in static scan.
Gate: G-SR02 remains OPEN because static code cannot prove which writers actually executed against the current populated DB.

## ORDER SR02-PG — CURRENT DB WRITE-EPOCH / PROVENANCE RECEIPT — local Codex dumb executor
Status: `RETURN_REQUIRED_R2`
R1 connected successfully but failed in P03 because the original full-response join/group exhausted PostgreSQL temp disk. That failure is classified `PROBE_SHAPE_DEFECT__NO_DB_SEMANTIC_DISPOSITION`.
R2 is checked in. P03/P04 are now information-equivalent low-temp provenance queries. Do not expand/free database disk merely to reproduce the superseded R1 query.
Read `SR02_PG_LOCAL_EXECUTION_ORDER.md` and execute the checked-in `SR02_CURRENT_DB_PROVENANCE_PROBE.sql` exactly. READ ONLY. No semantic interpretation.
Gate contribution: G-SR02.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local Codex dumb executor
Status: `RETURN_REQUIRED_R2`
R1 stopped at exact frozen `EVS 1999.sav` because default pyreadstat text decoding rejected a metadata byte sequence.
R2 is checked in. HQ froze a source-specific `latin1` reader compatibility override for exact SHA-256 `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8`. The override is explicit in code, manifests, and receipt; no other encoding guessing is permitted.
Read `SR03_LOCAL_EXECUTION_ORDER.md` and execute the checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py` against exact files from `SOURCE_BYTE_INVENTORY.csv`. No C11 ingest. No semantic normalization.
Gate: G-SR03.

## ORDER SR04 — CARRIER BAKEOFF — local Codex dumb executor
Status: `BLOCKED_G_SR03_AND_G_SR05_MINIMUM_CONTRACT`
Candidates: Parquet+DuckDB vs DuckDB-native vs PostgreSQL C11 vs SQLite where technically applicable.
Fixtures: WVS7 and LiTS I; EVS 1999 encoding replay becomes an additional decoder-hostile fixture.
Gate: G-SR04.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `FROZEN_PENDING_SR03_RECONCILIATION`
Inputs: frozen C11 M01-M18, I02/I03 contracts, WVS7/LiTS physical evidence, historical loss evidence.
Frozen authorities: `09_SOURCE_NATIVE_CONSTITUTION.md`, `10_FORMAT_DECODER_CONTRACT.md`, `12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`.
Source-specific reader encoding is now explicit replay provenance; automatic encoding guessing is forbidden.
Gate: G-SR05.

No implementation worker launches before G-SR04 + G-SR05 close.
