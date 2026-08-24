# Control Room — Canonical Navigation Index

Status: `ACTIVE_CANONICAL_PROJECT_MEMORY`

This directory is the Browser/HQ authority-recovery command record for the empirical substrate reconstruction.

It is organized by epistemic function rather than chronology.

## 1. What authority is expected?

- `AUTHORITY_EXPECTATION_UNIVERSE.csv`

This is the obligation universe: what kinds of semantic/source/structural/manual authority Rawlsing must possess or explicitly lack.

## 2. What objects have been found?

Primary historical/current census:

- `AUTHORITY_OBJECT_CENSUS.csv`

H005 recovered-object extension:

- `H005B_AUTHORITY_OBJECT_SUPPLEMENT.csv`

The supplement is a normative extension of the object census for P2/H005-recovered objects until the next full census compaction. It must not be ignored merely because those rows are not yet physically merged into the older CSV.

## 3. Where are the bytes?

- `AUTHORITY_PHYSICAL_LOCATION_LEDGER.csv`
- `H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`
- `H005_POST_DELTA_BROWSER_AVAILABLE_EVIDENCE_SUPPLEMENT.csv`

The H005 supplement records Browser-held evidence acquired after the original availability inventory.

## 4. What epistemic kind of object is each thing?

- `AUTHORITY_EPISTEMIC_CLASSIFICATION.csv`
- `H005B_AUTHORITY_OBJECT_SUPPLEMENT.csv`

Distinguish accepted/manual authority, mechanical carriers/build law, generated/discovery material, provenance/audit objects, negative authority and blocked states.

## 5. How do authority objects relate/supersede one another?

Primary DAG:

- `AUTHORITY_PROVENANCE_AND_SUPERSESSION_DAG.csv`

H005 extension:

- `H005B_PROVENANCE_SUPPLEMENT.csv`

Never infer supersession from recency, path, filename, mapping-status label or physical row order.

## 6. What is good/live/executable/blocked?

- `AUTHORITY_QUALITY_AND_EXECUTION_STATUS.csv`
- `AUTHORITY_GAP_LEDGER.csv`

The gap ledger distinguishes existing authority, unlocated authority, unproved succession, explicit blockers and genuinely missing authority.

Only `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED` may authorize new substantive semantic/manual authority.

## 7. Harvest/evidence history

Requests:

- `HARVEST_REQUEST_LEDGER.csv`

Packet adjudications:

- `HARVEST_PACKET_ADJUDICATION_LEDGER.csv`

Detailed courts:

- `HARVEST-001_ADJUDICATION.md`
- `HARVEST-002_ADJUDICATION.md`
- `HARVEST-003_ADJUDICATION.md`
- `HARVEST-004_ADJUDICATION.md`
- `HARVEST-005L_ADJUDICATION.md`
- `HARVEST-005B_ADJUDICATION.md`

## 8. Question identity / current-35 implementation universe

Recovered law:

- `QUESTION_OCCURRENCE_IDENTITY_LAW_RECOVERY.md`

H005 mechanical summaries:

- `H005B_CARRIER_COVERAGE_SUMMARY.csv`
- `H005B_COVERAGE_COUNTS_BY_FAMILY_WAVE.csv`
- `H005B_IDENTITY_COLLISION_AND_CROSSWALK_DEBT.csv`

Governing baseline:

`18,276 exact P2 question implementations / 35 active waves / 9 source families`

The exact row-level P2 skeleton remains its original content-addressed authority object; Browser did not create a renamed duplicate.

## 9. Current state / what next?

- `PROGRESS.md`
- `CURRENT_DISCOVERY_STATUS_AND_NEXT_ACTION.md`
- `NEXT_BROWSER_WORK_ORDER.md`
- `NEXT_LOCAL_HARVEST_REQUEST.md`

At present the local harvest queue is empty. Browser/HQ owns the next usable-universe and normalized-authority-binding court.

## 10. End-state architecture

- `UNIFIED_EMPIRICAL_AUTHORITY_SUBSTRATE_PLAN.md`

The target is a normalized governed authority system built around the recovered P2 implementation identity, current source-wave/source-native identity, separately-grained authority assertions, explicit negative/provenance/supersession state, versioned Parquet canonical relations, deterministic DuckDB query compilation and derived compatibility/master views.

## 11. Trii / Chetiri integration

Control Room is the reconciliation layer between:

`TRII SOURCE TRUTH`
+
`P2 GOVERNED QUESTION IDENTITY`
+
`RECOVERED EPISTEMIC CAPITAL`
+
`CURRENT AUTHORITY BINDINGS`
+
`CHETIRI PERSISTENCE / COMPILER REQUIREMENTS`

Trii source certification must protect exact source identity/evidence beneath the implementation spine.

Chetiri must persist/replay/serve the authority universe without dropping semantic/manual/structural/response/routing/negative/provenance/supersession information.

## Current governing sequence

`IDENTITY / 18,276 POPULATION RECOVERED`
→ `USABLE-UNIVERSE DISPOSITION`
→ `NORMALIZED AUTHORITY BINDING`
→ `QUALITY / CONFLICT / TRUE GAP COURT`
→ `TRII / CHETIRI REQUIREMENTS`
→ `UNIFIED SUBSTRATE SCHEMA + MIGRATION`
→ `REPLAY / VALIDATION`
