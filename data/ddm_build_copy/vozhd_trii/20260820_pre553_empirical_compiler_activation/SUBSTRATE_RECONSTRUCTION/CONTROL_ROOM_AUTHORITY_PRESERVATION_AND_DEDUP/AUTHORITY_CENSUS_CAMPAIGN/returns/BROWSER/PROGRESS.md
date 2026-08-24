# Browser Authority Census — Post-HARVEST-004 Progress

Status: `BROWSER_CENSUS__HARVEST_004_ADJUDICATED__D62_IDENTITY_COLLISION_PROVED__SEMANTIC_ROW_ORDER_PRECEDENCE_REJECTED__H005_IDENTITY_COVERAGE_BASELINE_ISSUED`

Start SHA: `b824c7d2b618b8e0987f6774b302e875d90b8fdd`
Worker: `agent/vozhd-controlroom-authority-census-browser-r1`

## HARVEST-004 integrity

Browser inspected the actual returned ZIP and independently verified:

- packet SHA-256 `b7ce4c0de1aea7db1e08d4c4faf3447f22809b62b95800502f0f3ee52c0c7abd`;
- size `14,235,501` bytes;
- ZIP integrity;
- all `111/111` internal checksum entries;
- requested receipt set present;
- no updater/compiler execution by the local worker.

## D62 duplicate producer and identity seam proved

Recovered exact producer:

- `apply_gss_lits_p0_structural_mappings.py`
- SHA-256 `6ddb066f76001488debcb822352aa39b5eabe3fd544d832eed783080e41ea6b9`

The producer intentionally appends GSS/LiTS questions that it believes are absent from `questions_master_drivers.csv`, but its absence test is based on `item_id` only.

Exact d62 row geometry proves the failure mode:

- `d62accad...`: 28,983 rows / 18,519 distinct `(source,wave,var_name)` keys;
- first segment: 18,528 rows / 18,519 natural keys;
- appended tail: 10,455 rows, exactly 6,021 GSS + 4,434 LiTS;
- all 10,455 tail natural keys already exist in the first segment;
- 10,454/10,455 corresponding first-segment GSS/LiTS rows have blank `item_id`;
- all 10,455 appended tail rows have distinct nonblank `item_id` values.

The updater therefore mistook already-present semantic question rows for missing rows because the old representation lacked the newer identity field and appended second representations of the same questions.

## Downstream row order was accidental precedence, not authority

The historical question-structure builder consumes the driver master through a dict keyed by `(source,wave,var_name)`. Duplicate rows therefore collapse to the last physical row.

H003 had already proved that this exact lookup reproduces Register B and the full Register A→B 2,148-row / 13,330-cell delta. H004 now proves why those later rows existed.

No recovered authority defines last-row-wins as semantic supersession law. The recovered producer explicitly calls its work a first-pass scaffold requiring review, and the migration contract requires preserving existing columns and backing up before writes.

Governing ruling:

`DUPLICATE_SHADOWING_PRODUCER_PROVED__INCIDENTAL_CARRIER_KEY_COLLISION__NO_SEMANTIC_SUPERSESSION_AUTHORITY`

The old semantic judgment and the later structural assertion must therefore be preserved noncollapsingly unless a separate positive authority proves a real semantic supersession.

## Register A→d62 residuals

Of the 2,148 nine-field Register-A→d62 changes:

- 2,056 are inside the proved duplicate-shadow mechanism;
- 92 are single-key in-place remapping/normalization changes;
- 81 of those 92 change only `final_driver_label`;
- 11 change only `semantic_secondary_driver`, all Arab Barometer W8.

Recovered `apply_arab_barometer_w8_p0_structural_mappings.py` explains the mechanical clearing of those 11 secondary-driver fields during direct P0 structural promotion. H004 does not prove all 92 changes are lossless semantic supersessions, so prior and later assertions remain preserved for later scope-quality adjudication.

## Exact transient pre-A master remains unrecovered but nonblocking

Only two physical driver-master identities were recovered in H004:

- accepted V525b `53feb282...` / 6,211 rows;
- later d62 `d62accad...` / 28,983 rows.

V525b is not the immediate Register-A master: only 5,128 Register-A keys match it and 1,963 matched nine-field projections differ.

The exact transient full pre-shadow master was not recovered. Register A remains a positive downstream witness of the effective pre-shadow semantic/driver projection for its covered keys. No regeneration or guessed reconstruction is authorized.

The historical filesystem census identifies `build_questions_master_drivers.py` SHA `e056bd2b8b388a8ad133b8a98682e68fb1612aedf6e6689122054d8c26925b6b`, but H004 did not package its bytes. This is recorded historical provenance residue, not a blocker to the H004 duplicate-producer ruling.

## V525b small pre-existing identity imperfection

H004 also established that the 6,211-row V525b driver master has:

- 6,202 distinct `(source,wave,var_name)` keys;
- 7 duplicate natural keys;
- 9 duplicate-excess rows;
- 4 blank natural-key rows.

This is preserved for the future question-identity audit. It is not the cause of the later 10,455-row GSS/LiTS duplicate layer.

## Unified empirical-authority implication

H004 materially confirms the previously logged architecture direction:

- one governed question-occurrence identity spine;
- separate normalized authority assertions at their true cardinalities;
- prior semantic authority and later structural mappings must not compete through duplicate physical rows;
- no implicit row-order precedence;
- negative/review/pending states remain first-class;
- future Parquet canonical relations + deterministic DuckDB bundle + derived monster master view remain the planned end state.

## Current dispositions

- `EXP-006 EARLY_SEMANTIC_MASTER`: accepted V525b authority protected; later heuristic semantic carrier and flat d62 carrier do not prove lossless semantic succession.
- `EXP-007 DRIVER_FACET`: d62 duplicate producer/cause resolved; later structural capital exists but must be preserved separately from semantic retirement; full current quality remains pending.
- `EXP-030 SUPERSESSION_REGISTRY`: no global registry yet; H004 specifically rejects row order as a supersession rule.
- no expectation is `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Next local request

Issued:

`HARVEST-005 — CURRENT-35 QUESTION-OCCURRENCE IDENTITY AND EXISTING-AUTHORITY COVERAGE BASELINE`

H005 will mechanically enumerate the current-35 candidate question-occurrence universe and cross-carrier coverage/cardinality without deduplicating, inventing canonical UIDs, adjudicating semantics or treating uncovered as missing authority.

After H005 adjudication, the intended sequence is:

`QUESTION IDENTITY LAW -> CURRENT-35 USABLE-UNIVERSE BOUNDARY -> NORMALIZED AUTHORITY BINDING -> FULL-UNIVERSE QUALITY COURT -> TRUE GAP ADJUDICATION -> UNIFIED PARQUET/DUCKDB AUTHORITY RELEASE`
