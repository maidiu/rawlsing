# FIRST LAUNCH ORDER SEQUENCE

## ORDER SR01 — SOURCE BYTE CENSUS — HQ/browser
Status: `ACCEPTED`
Inputs: `surveys.zip`, `WVS Wave 7.sav.zip`, `LiTS_I.dta.zip` retained outside Git as source evidence.
Output: `SOURCE_BYTE_INVENTORY.csv`.
Observed: 35 governed source files, 31 SAV, 4 DTA. AppleDouble packaging artifacts excluded.
Gate: G-SR01.

## ORDER SR02 — LEGACY WRITER + ACTUAL V550 DB DEPENDENCY GENEALOGY — HQ/browser
Status: `LIVE_EXECUTION_ACCEPTED__HQ_CONTENT_ADJUDICATION_PENDING`
Inputs: `etl.zip`, `etl(1).zip`, `backfill.zip`, exact supplied public schema, authority-reconcile schema, frozen V550 runtime source.
Outputs include:
- `LEGACY_WRITER_INVENTORY.csv`
- `DATABASE_SURFACE_INVENTORY.csv`
- `14_PRE_RECONSTRUCTION_DB_DEPENDENCY_MAP.md`
- `SR02_SCHEMA_REFERENCE_AUDIT.csv`
- `13_DATABASE_PROVENANCE_ADJUDICATION_LAW.md`

Static perimeter: 61 historical scripts with relevant empirical-surface contact; 25 SAV-reader scripts and zero explicit `user_missing=True` preservation discovered in static scan.

Runtime trace correction: not every database surface is an equal pre-reconstruction dependency. Frozen V550 directly/transitively depends on the respondent/response carrier, named demographic→position layer, weights, source/wave identity, QSM, and response-long view. Progress/repair relations are provenance-only. `driver_aggregates` and old `respondents/responses` are peripheral legacy surfaces for this runtime.

SR02-PG R3 completed successfully at exact execution head `4713aad8fb5f6dc9b5359c5a2eff11e3dfb1d524`, exit `0`, receipt size `417137`, SHA-256 `c3e507f8661cd2f5e4cbfa5657499bd0426d6b29ea856259a29b6397df9c938a`, schema preflight PASS, completion token present. Execution acceptance does not by itself close G-SR02: HQ must inspect the complete receipt contents and join them to writer genealogy before issuing terminal surface dispositions.

Gate: G-SR02 remains OPEN only for HQ receipt-content adjudication.

## ORDER SR02-PG — CURRENT RUNTIME-CONE DB PROVENANCE RECEIPT — local Codex dumb executor
Status: `EXECUTION_ACCEPTED_R3__NO_FURTHER_LOCAL_RUN_ORDERED`

R1: probe-shape defect exhausted PostgreSQL temp disk.
R2: low-temp shape succeeded through the large scans but exposed HQ's un-audited `driver_aggregates.wave` assumption.
R3: schema-audited runtime-cone probe completed successfully. No additional local SR02 execution is authorized unless HQ finds an exact receipt-content gap.

Gate contribution: G-SR02.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local Codex dumb executor
Status: `RETURN_REQUIRED_R3`

Earlier attempts exposed bounded pyreadstat decoding/chunk-reader compatibility failures. The checked-in Revision-3 probe and `10_FORMAT_DECODER_CONTRACT.md` now freeze an exact six-source compatibility-execution allowlist:

- `EVS 1999.sav`
- `EVS 2008.sav`
- `LiTS_I.dta`
- `LiTS_II.dta`
- `LiTS_III.dta`
- `LiTS_IV.dta`

Each override is hash-bound through `SOURCE_BYTE_INVENTORY.csv`, uses explicit `latin1` only for the pyreadstat physical-census path, and carries authority status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`. No compatibility override certifies the intended source text encoding or semantic meaning of decoded labels.

Read `SR03_LOCAL_EXECUTION_ORDER.md` and execute `SR03_SOURCE_NATIVE_METADATA_PROBE.py` exactly into fresh `SR03_SOURCE_PHYSICAL_MANIFESTS_R3`. No C11 ingest. No semantic normalization. No additional encoding guesses.
Gate: G-SR03.

## ORDER SR04 — CARRIER BAKEOFF — local Codex dumb executor
Status: `BLOCKED_G_SR03_AND_G_SR05_MINIMUM_CONTRACT`
Candidates: Parquet+DuckDB vs DuckDB-native vs PostgreSQL C11 vs SQLite where technically applicable.
Fixtures: WVS7 and LiTS I; legacy compatibility-decoding replay is an additional decoder-hostile fixture.
Gate: G-SR04.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `FROZEN_PENDING_SR03_RECONCILIATION`
Inputs: frozen C11 M01-M18, I02/I03 contracts, WVS7/LiTS physical evidence, historical loss evidence.
Frozen authorities: `09_SOURCE_NATIVE_CONSTITUTION.md`, `10_FORMAT_DECODER_CONTRACT.md`, `12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`.
Source-specific reader compatibility encoding is explicit replay provenance and is kept strictly separate from source-text semantic authority; automatic encoding guessing is forbidden.
Gate: G-SR05.

No implementation worker launches before G-SR04 + G-SR05 close.
