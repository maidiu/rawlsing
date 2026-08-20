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

## ORDER SR02-PG — CURRENT DB WRITE-EPOCH / PROVENANCE RECEIPT — local dumb executor
Status: `READY_TO_LAUNCH`
Read `SR02_PG_LOCAL_EXECUTION_ORDER.md` and execute the checked-in `SR02_CURRENT_DB_PROVENANCE_PROBE.sql` exactly. READ ONLY. No semantic interpretation.
Gate contribution: G-SR02.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local dumb executor
Status: `READY_TO_LAUNCH`
Read `SR03_LOCAL_EXECUTION_ORDER.md` and execute the checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py` against exact files from `SOURCE_BYTE_INVENTORY.csv`. No C11 ingest. No semantic normalization.
Gate: G-SR03.

## ORDER SR04 — CARRIER BAKEOFF — local dumb executor
Status: `BLOCKED_G_SR03_AND_G_SR05_MINIMUM_CONTRACT`
Candidates: Parquet+DuckDB vs PostgreSQL C11 control.
Fixtures: WVS7 and LiTS I.
Gate: G-SR04.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `ACTIVE_IN_PARALLEL_WITH_SR02_SR03_EXECUTION`
Inputs: frozen C11 M01-M18, I02/I03 contracts, WVS7/LiTS physical evidence, historical loss evidence.
Gate: G-SR05.

No implementation worker launches before G-SR04 + G-SR05 close.
