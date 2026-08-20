# FIRST LAUNCH ORDER SEQUENCE

## ORDER SR01 — SOURCE BYTE CENSUS — HQ/browser
Status: `ACCEPTED`
Inputs: `surveys.zip`, `WVS Wave 7.sav.zip`, `LiTS_I.dta.zip` retained outside Git as source evidence.
Output: `SOURCE_BYTE_INVENTORY.csv`.
Observed: 35 governed source files, 31 SAV, 4 DTA. AppleDouble packaging artifacts excluded.
Gate: G-SR01.

## ORDER SR02 — LEGACY WRITER + ACTUAL V550 DB DEPENDENCY GENEALOGY — HQ/browser
Status: `ACTIVE__RUNTIME_CONE_TRACED`
Inputs: `etl.zip`, `etl(1).zip`, `backfill.zip`, exact supplied public schema, authority-reconcile schema, frozen V550 runtime source.
Outputs include:
- `LEGACY_WRITER_INVENTORY.csv`
- `DATABASE_SURFACE_INVENTORY.csv`
- `14_PRE_RECONSTRUCTION_DB_DEPENDENCY_MAP.md`
- `SR02_SCHEMA_REFERENCE_AUDIT.csv`
- `13_DATABASE_PROVENANCE_ADJUDICATION_LAW.md`

Static perimeter: 61 historical scripts with relevant empirical-surface contact; 25 SAV-reader scripts and zero explicit `user_missing=True` preservation discovered in static scan.

Runtime trace correction: not every database surface is an equal pre-reconstruction dependency. Frozen V550 directly/transitively depends on the respondent/response carrier, named demographic→position layer, weights, source/wave identity, QSM, and response-long view. Progress/repair relations are provenance-only. `driver_aggregates` and old `respondents/responses` are peripheral legacy surfaces for this runtime.

Gate: G-SR02 remains OPEN pending the schema-audited R3 live receipt and HQ writer adjudication.

## ORDER SR02-PG — CURRENT RUNTIME-CONE DB PROVENANCE RECEIPT — local Codex dumb executor
Status: `RETURN_REQUIRED_R3`

R1: probe-shape defect exhausted PostgreSQL temp disk.
R2: low-temp shape succeeded through the large scans but exposed HQ's un-audited `driver_aggregates.wave` assumption.

R3 is not a one-column patch. Before R3 launch, HQ:
- traced the actual frozen V550 DB dependency cone;
- removed peripheral legacy surfaces from the live scan;
- checked 155 explicit required relation/column pairs against exact supplied `Rawlsing_WVS_public_schema(2).sql`: 0 mismatches;
- checked all 36 physical `respondentsDemo*` tables: 36/36 contract PASS;
- checked V550-required view columns;
- embedded a live schema preflight before all data scans.

Read `SR02_PG_LOCAL_EXECUTION_ORDER.md` and execute `SR02_CURRENT_DB_PROVENANCE_PROBE.sql` exactly. READ ONLY. No interpretation.
Gate contribution: G-SR02.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local Codex dumb executor
Status: `RETURN_REQUIRED_R2`
R1 stopped at exact frozen `EVS 1999.sav` because default pyreadstat text decoding rejected a metadata byte sequence.
R2 is checked in. HQ froze a source-specific `latin1` reader compatibility override for exact SHA-256 `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8`. The override is explicit in code, manifests, and receipt; no other encoding guessing is permitted.
Read `SR03_LOCAL_EXECUTION_ORDER.md` and execute `SR03_SOURCE_NATIVE_METADATA_PROBE.py` against exact files from `SOURCE_BYTE_INVENTORY.csv`. No C11 ingest. No semantic normalization.
Gate: G-SR03.

## ORDER SR04 — CARRIER BAKEOFF — local Codex dumb executor
Status: `BLOCKED_G_SR03_AND_G_SR05_MINIMUM_CONTRACT`
Candidates: Parquet+DuckDB vs DuckDB-native vs PostgreSQL C11 vs SQLite where technically applicable.
Fixtures: WVS7 and LiTS I; EVS 1999 encoding replay is an additional decoder-hostile fixture.
Gate: G-SR04.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `FROZEN_PENDING_SR03_RECONCILIATION`
Inputs: frozen C11 M01-M18, I02/I03 contracts, WVS7/LiTS physical evidence, historical loss evidence.
Frozen authorities: `09_SOURCE_NATIVE_CONSTITUTION.md`, `10_FORMAT_DECODER_CONTRACT.md`, `12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`.
Source-specific reader encoding is explicit replay provenance; automatic encoding guessing is forbidden.
Gate: G-SR05.

No implementation worker launches before G-SR04 + G-SR05 close.
