# Browser Authority Census — Post-HARVEST-004 / H005 Split Progress

Status: `BROWSER_CENSUS__H004_ADJUDICATED__H005_SPLIT__BROWSER_AVAILABILITY_INVENTORY_PUBLISHED__H005L_LOCAL_DELTA_ISSUED__H005B_BROWSER_COURT_READY`

Start SHA: `b824c7d2b618b8e0987f6774b302e875d90b8fdd`
Worker: `agent/vozhd-controlroom-authority-census-browser-r1`

## H004 remains closed

H004 proved the main d62 GSS/LiTS duplicate layer was produced by an identity-migration mismatch:

- `apply_gss_lits_p0_structural_mappings.py` checks existing questions through `item_id`;
- the earlier GSS/LiTS semantic rows were overwhelmingly blank in `item_id`;
- 10,455 second representations were appended whose `(source,wave,var_name)` keys already existed;
- a separate downstream dict keyed by `(source,wave,var_name)` converted physical row order into effective precedence;
- no authority object authorizes last-row-wins as semantic supersession.

Governing disposition remains:

`DUPLICATE_SHADOWING_PRODUCER_PROVED__INCIDENTAL_CARRIER_KEY_COLLISION__NO_SEMANTIC_SUPERSESSION_AUTHORITY`

Prior semantic authority and later structural assertions must be preserved noncollapsingly.

## Browser evidence availability is now explicit

Published:

`H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`

Browser has exact bytes of all four returned harvest packets:

- H001 `e283735f6af208578b373a2e30d8df7fc8ad3f86edc05874fa43e4be9092db78`
- H002 `70789a6556f70c2c6be0771defe00fec918b7e64514e37d82744493431f1dc37`
- H003 `0ad166ec3da232f56a5a0c9612862e99b2091e8ba80626bc76417e7a4524e461`
- H004 `b7ce4c0de1aea7db1e08d4c4faf3447f22809b62b95800502f0f3ee52c0c7abd`

Browser can inspect every member of those ZIPs directly.

The inventory separately records exact Browser-held members including the structure registers, semantic/driver masters, current-35 scope/identity manifests and code, respondent registries, H004 producer lineage and related schema/build objects.

Browser also has connected GitHub access to the accepted/preserved SWID, source-census, FQRA/QSM/QRA/response/manual/negative authority surfaces listed in the inventory.

## Library discovery indexes now hash-bound in the Browser record

Browser materialized and hashed:

- `rawlsing_full_tree.txt` — `3fcc51f1a125f2a1eff90d932133cc033fb1145432b9e25ae3f9542ed09ea145`
- `Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt` — `1e93b7774ffffc977bc80b940becdd7576cda10c6bb4a0c211b01a5634da6668`
- `Rawlsing_repo_tree_dates_sizes_sha256.txt` — `8064b2a6d5fdd7cb3916aedbea59f74728b3dddf7b08ba9384531d95d5cd9c44`

These are discovery/path/SHA aids, not substitutes for target authority bytes or fresh local delta evidence.

## Original H005 mixed two capability domains

The original H005 order asked a local worker both to:

1. discover local-only identity evidence; and
2. build the global candidate universe, cross-carrier joins, collision census and coverage matrix.

That division was unnecessary and operationally poor.

The original `HARVEST-005` is therefore superseded by:

### H005L — Local delta discovery

`NEXT_LOCAL_HARVEST_REQUEST.md`

Local responsibilities are now limited to:

- search `/Users/matthewsmith/Desktop/Rawlsing` and `/Users/matthewsmith/Desktop/RawlsingsExcess`;
- hash H005-responsive identity carriers;
- compare against `H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`;
- return exact bytes only for unseen/distinct content or uniquely necessary local provenance;
- especially recover `questions_master.csv`, current codebook/question-index identity surfaces, local-only distinct FQRA/QSM variants and source-native identity indexes if present.

The local worker must not perform global joins or coverage computation.

### H005B — Browser identity/coverage court

`HARVEST-005B_BROWSER_IDENTITY_COVERAGE_COURT.md`

Browser HQ owns:

- carrier schema census;
- candidate question-occurrence relation;
- indexed relational joins;
- explicit cardinality classification;
- collision census;
- per-family/wave coverage counts;
- identity-law implications and Trii/Chetiri dependency adjudication.

Browser will use indexed relational operations (DuckDB/Polars/pandas merge/hash indexes or equivalent), not naive candidate-by-carrier scans.

## Current Browser-availability gaps motivating H005L

The availability inventory currently marks as not exhaustively Browser-held:

- exact `questions_master.csv` content identities;
- current final codebook/question-index occurrence surfaces;
- local-only distinct FQRA/QSM/QSMv2 identity-bearing variants;
- bounded source-native codebook variable/question identity indexes/manifests needed for occurrence binding.

These are evidence-availability gaps, not proved semantic-authority gaps.

## Current dispositions

- `EXP-006 EARLY_SEMANTIC_MASTER`: V525b accepted authority remains protected.
- `EXP-007 DRIVER_FACET`: d62 identity collision mechanism resolved; structural capital preserved separately from semantic retirement.
- `EXP-030 SUPERSESSION_REGISTRY`: still incomplete globally; row order is specifically rejected as supersession law.
- no expectation is `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Next sequence

`H005L LOCAL EVIDENCE COMPLEMENT`
→ `H005B BROWSER IDENTITY/COVERAGE COURT`
→ `QUESTION OCCURRENCE IDENTITY LAW`
→ `CURRENT-35 USABLE-UNIVERSE BOUNDARY`
→ `NORMALIZED AUTHORITY BINDING`
→ `FULL-UNIVERSE QUALITY COURT`
→ `TRUE GAP ADJUDICATION`
→ `UNIFIED PARQUET/DUCKDB AUTHORITY RELEASE`
