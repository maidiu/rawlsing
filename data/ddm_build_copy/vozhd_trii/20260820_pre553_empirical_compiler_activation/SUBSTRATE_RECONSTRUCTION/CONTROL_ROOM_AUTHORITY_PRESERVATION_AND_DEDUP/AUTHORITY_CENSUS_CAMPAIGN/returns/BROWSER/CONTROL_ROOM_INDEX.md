# Control Room — Canonical Navigation Index

Status: `ACTIVE_CANONICAL_PROJECT_MEMORY__AUTHORITY_BINDING_CLOSED__PHYSICAL_CONTRACT_NEXT`

This directory is the Browser/HQ authority-recovery and substrate-reconstruction command record.

It is organized by epistemic function rather than chronology.

## 1. Expected authority obligations

- `AUTHORITY_EXPECTATION_UNIVERSE.csv`

Defines the authority obligation universe and distinguishes expected authority from merely observed files.

## 2. Recovered authority objects

- `AUTHORITY_OBJECT_CENSUS.csv`
- `H005B_AUTHORITY_OBJECT_SUPPLEMENT.csv`

The H005 supplement is a normative extension of the earlier census until a later compaction.

## 3. Physical evidence availability

- `AUTHORITY_PHYSICAL_LOCATION_LEDGER.csv`
- `H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`
- `H005_POST_DELTA_BROWSER_AVAILABLE_EVIDENCE_SUPPLEMENT.csv`

These answer what exact evidence Browser already possesses and what, if anything, requires external/local retrieval.

## 4. Epistemic classification

- `AUTHORITY_EPISTEMIC_CLASSIFICATION.csv`
- `H005B_AUTHORITY_OBJECT_SUPPLEMENT.csv`

Keep accepted/manual authority, current successor authority, historical authority, generated/discovery carriers, mechanical build law, source evidence, negative authority and blocked states distinct.

## 5. Provenance / supersession

- `AUTHORITY_PROVENANCE_AND_SUPERSESSION_DAG.csv`
- `H005B_PROVENANCE_SUPPLEMENT.csv`

Never infer supersession from recency, path, filename, mapping status or physical row order.

## 6. Quality / execution / gaps

- `AUTHORITY_QUALITY_AND_EXECUTION_STATUS.csv`
- `AUTHORITY_GAP_LEDGER.csv`
- `CURRENT35_AUTHORITY_QUALITY_AND_GAP_LEDGER.csv`

The current binding court found zero authority classes at `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

Explicit blocked/unresolved states remain knowledge and must fail closed where their jurisdiction requires resolution.

## 7. Harvest history

- `HARVEST_REQUEST_LEDGER.csv`
- `HARVEST_PACKET_ADJUDICATION_LEDGER.csv`
- `HARVEST-001_ADJUDICATION.md`
- `HARVEST-002_ADJUDICATION.md`
- `HARVEST-003_ADJUDICATION.md`
- `HARVEST-004_ADJUDICATION.md`
- `HARVEST-005L_ADJUDICATION.md`
- `HARVEST-005B_ADJUDICATION.md`

The local harvest queue is currently empty.

## 8. Question identity / current-35 implementation universe

Recovered law:

- `QUESTION_OCCURRENCE_IDENTITY_LAW_RECOVERY.md`

H005 coverage mechanics:

- `H005B_CARRIER_COVERAGE_SUMMARY.csv`
- `H005B_COVERAGE_COUNTS_BY_FAMILY_WAVE.csv`
- `H005B_IDENTITY_COLLISION_AND_CROSSWALK_DEBT.csv`

Governing baseline:

`18,276 exact P2 question implementations / 35 active waves / 9 source families`

The original content-addressed P2 skeleton remains the row-level identity master. No competing question UID is authorized.

## 9. Current-35 usable-universe and authority binding

Governing court:

- `USABLE_UNIVERSE_AND_BINDING_ADJUDICATION.md`

Machine/durable outputs:

- `CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv`
- `NORMALIZED_AUTHORITY_BINDING_MATRIX.csv`
- `AUTHORITY_BINDING_CARDINALITY_AND_CONFLICT_LEDGER.csv`
- `CURRENT35_AUTHORITY_QUALITY_AND_GAP_LEDGER.csv`
- `TRII_CHETIRI_AUTHORITY_REQUIREMENTS.md`

This court closes the previous frontier:

- all 18,276 implementations dispositioned;
- R10F O03/O04 bound;
- R10G semantic coordinates bound;
- R10H O06/O07/O08 bound across all 18,276;
- R10I O09 bound;
- FQRA/QSMv2, QSR, V525b, QRA/response, SWID/source authority preserved at their own grains;
- negative/block/review states preserved;
- no new semantic-authority gap proved.

## 10. Current state / what next?

- `PROGRESS.md`
- `CURRENT_DISCOVERY_STATUS_AND_NEXT_ACTION.md`
- `NEXT_BROWSER_WORK_ORDER.md`
- `NEXT_LOCAL_HARVEST_REQUEST.md`

Current Browser frontier:

`UNIFIED SUBSTRATE SCHEMA, MIGRATION & REPLAY CONTRACT COURT`

Current local frontier:

`NONE__NO_LOCAL_HARVEST_REQUIRED_AT_START`

## 11. End-state architecture

- `UNIFIED_EMPIRICAL_AUTHORITY_SUBSTRATE_PLAN.md`

Target physical shape:

- normalized typed canonical relations;
- versioned Parquet release;
- schemas/manifests/SHA identities;
- deterministic read-only DuckDB compilation/query bundle;
- derived wide compatibility/master views that are explicitly noncanonical;
- explicit provenance, crosswalk, negative-state and supersession relations;
- deterministic replay/conservation validation.

## 12. Trii / Chetiri integration

Control Room reconciles:

`TRII SOURCE TRUTH`
+
`P2 GOVERNED QUESTION IDENTITY`
+
`RECOVERED HISTORICAL + CURRENT EPISTEMIC CAPITAL`
+
`CURRENT NORMALIZED AUTHORITY BINDINGS`
+
`CHETIRI PERSISTENCE / COMPILER / SERVING REQUIREMENTS`

Trii must certify the exact source floor beneath the authority graph.

Chetiri must persist, replay, compile and serve the graph without dropping one-to-many authority, blockers, provenance, historical capital or source identity.

## Governing sequence

`IDENTITY / 18,276 POPULATION RECOVERED`
→ `USABLE-UNIVERSE DISPOSITION COMPLETE`
→ `NORMALIZED AUTHORITY BINDING COMPLETE`
→ `QUALITY / TRUE-GAP COURT COMPLETE`
→ `TRII / CHETIRI REQUIREMENTS EXPLICIT`
→ **`UNIFIED SUBSTRATE SCHEMA + MIGRATION + REPLAY CONTRACT`**
→ `PHYSICAL IMPLEMENTATION`
→ `REPLAY / CONSERVATION / RUNTIME VALIDATION`