# D05 — Populated Empirical Substrate Reality Court

## VERDICT

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

## APPARATUS VERDICT

`CLOSED_EXECUTABLE_FIXED_SEMANTICS`

Those findings are separate.

This worker still has no live populated PostgreSQL database and no exact transactionally consistent production-equivalent populated snapshot. D05 therefore makes **no populated-data claims** about respondent counts, overlap, completeness, weight coverage, routing, topology prevalence, join rates, facet preservation, cache losslessness, or source equivalence.

But the original blocked return is superseded. The database is now the remaining execution blocker; the audit design is no longer one.

## What was wrong with the first return

The first return failed its own contract in three ways:

1. It gave incorrect SHA256 values for the two WVS schema authorities.
2. It promised `AUDIT.sql` and `EXPECTED_OUTPUT_SCHEMAS.json` without actually creating them.
3. It left the future data-bearing worker to make semantic decisions that D05 itself was supposed to fix.

A later hostile pass also caught two subtler audit errors before closure:

4. The first overlap implementation emitted only pairs with positive same-respondent overlap. That would erase zero-overlap pairs—the strongest physical evidence of routed modules or disjoint question incidence. The normative R4 pass now emits **every unordered populated question pair, including overlap = 0**.
5. Cache respondent cardinality parity was initially insufficient: two different respondent-ID sets can have identical counts. R4 now compares exact respondent-ID sets for every cache selection, records deterministic hashes, and reports missing/extra IDs.

## Canonical command

A worker with populated DB access runs exactly:

```bash
DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DBNAME' \
  bash data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/run_d05_empirical_audit.sh
```

**Semantic parameters: none. Worker semantic decisions required: zero.**

The canonical stack is:

1. `run_d05_empirical_audit.py`
2. `audit_d05_identity_overlap_exact.py`
3. `audit_d05_output_semantic_guard.py`
4. `audit_d05_authority_scope_cache.py`
5. `audit_d05_cache_identity_exact.py`

`D05_AUDIT_CONTRACT.json` R4 is the normative machine-readable law. `EXECUTION_KIT.md` explains it for operators.

Every database stage independently opens PostgreSQL `REPEATABLE READ, READ ONLY` and verifies `transaction_read_only = on`. No ingestion, repair, DDL, DML, retention rewrite, or production-code mutation is authorized. Outputs remain under this D05 directory only.

## Fixed physical contract

Fatal core relations:

- `public.survey_microdata_respondents`: `id`, `source`, `wave`, `country_code`, `survey_year`
- `public.survey_microdata_responses`: `respondent_id`, `var_code`, `value_raw`, `value_text`

Expected audited non-core surfaces:

- `public.survey_weight_fact`
- `public.respondent_position_fact`
- `public.question_structural_mapping`
- `public.survey_authority_compendium`
- `public.v_ddm_response_long_facet_ready`
- `public.v_ddm_response_long_facet_ready_authority`
- `public.ddm_demographic_field_register`
- uniquely discoverable `canonical_question_registry`, if installed
- same-schema `question_variable_alias`, if installed

Missing non-core relations/columns are explicit findings. They are never silently replaced by schema inference or guessed aliases.

## What the executable audit now proves or falsifies

### Respondent identity

`RESPONDENT_IDENTITY_AUDIT.csv` measures globally and by source/wave/country:

- respondent rows and distinct IDs;
- null IDs;
- duplicate-ID groups/excess rows;
- IDs occupying multiple source/waves;
- IDs occupying multiple countries;
- IDs occupying multiple survey years;
- response rows and orphan responses.

This makes respondent scope/collision claims first-class evidence instead of burying them in a PK assumption.

### Source / wave / country / year coverage

`SOURCE_WAVE_READINESS.csv` measures populated source, raw wave, canonical wave, country, survey year, respondents, response rows, responding respondents, distinct variables, and row/respondent counts in both facet-ready surfaces.

`GOVERNED_SCOPE_COMPARISON.csv` compares actual population to current production `active_closed_35_waves()`. D05 imports production source/wave canonicalizers rather than maintaining a rival alias ontology.

### Response incidence, duplicates, and cotravel

`RESPONSE_MULTIPLICITY_AUDIT.csv` separately measures raw respondent/var duplicates and canonical respondent/question duplicates, plus min/P50/P90/P99/max questions and response rows per respondent.

`QUESTION_OVERLAP_SUMMARY.csv` contains **all unordered populated question pairs** in every source/wave/country. The pair universe is formed from marginals first; same-respondent overlap is left-joined so zero-overlap pairs remain visible. It reports both marginals, overlap, union, directional overlap percentages, Jaccard, overlap among unique respondent/question cells, duplicate-compromised overlap, and whether cotravel is physically possible.

`QUESTION_OVERLAP_COMPLETENESS.json` reports total pair rows and zero-overlap pair rows, making completeness auditable.

### Position completeness

`POSITION_FIELD_COMPLETENESS.csv` measures coverage and cardinality by source/wave for at least:

sex, age, age_group, education_level, income_level, religion_label, urban_rural, region, ethnicity, language, employment, marital, household_size, class_level.

Additional source-native demographic register entries are reported as candidates only. Register presence is not treated as proof that a field survives physically in respondent facts. Missing values are substrate missingness, never real-world absence.

### Weights

`WEIGHT_COVERAGE.csv` measures any/primary/missing/multiple-primary respondent state, null/zero/negative/non-finite primary values, weight names, types, and source vars. The information-loss audit separately checks whether design variables such as PSU/stratum/cluster/FPC/replicate metadata are exposed.

A scalar weight is never called population truth or design-based inference authority.

### Typed missingness and response topology

DK, refusal, IAP/not-asked, generic missingness, and substantive-response status are measured only from physically exposed typed fields. Blank `value_raw` or `value_text` is never semantically reclassified.

Likewise binary/ordinal/nominal/scale/matrix/multi-select topology is never inferred from observed cardinality. `RESPONSE_TOPOLOGY_AUDIT.csv` reports authority topology fields separately from observed response shape.

### Raw → facet-ready information preservation

`FACET_READY_PARITY_AUDIT.csv` full-outer-compares raw and derived relations at:

`source, wave, country_code, respondent_id, UPPER(var_code)`

It measures raw-only rows, derived-only rows, multiplicity mismatches, and raw-code/raw-text multiset mismatches when those target fields are physically exposed.

`audit_d05_output_semantic_guard.py` prevents an absent field from being mislabeled as “preserved with zero mismatches.” Non-exposure is recorded as non-exposure.

The same surface tests whether physical linkage/position columns remain sufficient to form row sets for:

- `P(Y | position)`
- `P(Y | position conjunction)`
- `P(Y | X response)`
- `P(Y | X response AND position)`

Those are reconstructibility claims, not substantive inference authority.

### Canonical question identity

D05 now keeps three identity systems distinct:

1. `IDENTITY_JOIN_AUDIT.csv` — current populated QSM exact/fallback/ambiguous/unmapped partition.
2. `R1_AUTHORITY_JOIN_AUDIT.csv` — production `resolve_question_relation_authority()` for every populated source/wave/country/var identity, including match status and active authority SHA256.
3. `CANONICAL_REGISTRY_JOIN_AUDIT.csv` — exact and alias reconciliation against one uniquely discoverable installed canonical registry schema, if present.

If multiple canonical-registry schemas are installed, D05 fails rather than choosing one.

### Shared respondent cache

Every discovered `v550_shared_respondent_substrate.parquet` is audited.

`CACHE_SELECTED_PARITY.csv` checks selected DB row/respondent cardinality plus position-predicate, typed-missingness, topology, and explicit selection-column preservation.

`CACHE_IDENTITY_EXACT.csv` closes the harder identity question. For every cache source/wave/country/var selection it records:

- cache and DB respondent-ID counts;
- SHA256 of each sorted respondent-ID set;
- missing DB IDs in cache;
- extra cache IDs not in DB;
- exact raw-ID set equality;
- `respondent_id_norm` presence/hash/equality.

Matching counts with different IDs fail `D05_F_SHARED_CACHE_RESPONDENT_ID_DRIFT`.

## Static evidence provenance

The corrected locked identities are:

- `Rawlsing_WVS_public_schema.sql` — `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` — `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`
- `rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip` — `e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861`
- `rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip` — `a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd`
- `rawlsing_chatlog_DDM_chatgpt_1.txt` — `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a`

The runner hashes its fixed checked-in evidence list at execution time and records both SHA256 and Git blob SHA in `STATIC_EVIDENCE_PROVENANCE.csv`. Locked mismatch is fatal `D05_E_STATIC_PROVENANCE_MISMATCH`.

## Machine-readable output law

Exact output schemas, invariants, relation columns, failure codes, grains, and classifications live in `D05_AUDIT_CONTRACT.json` R4. Major outputs include:

- `RELATION_PREFLIGHT.csv`
- `RESPONDENT_IDENTITY_AUDIT.csv`
- `SOURCE_WAVE_READINESS.csv`
- `RESPONSE_MULTIPLICITY_AUDIT.csv`
- `QUESTION_OVERLAP_SUMMARY.csv`
- `QUESTION_OVERLAP_COMPLETENESS.json`
- `POSITION_FIELD_COMPLETENESS.csv`
- `WEIGHT_COVERAGE.csv`
- `TYPED_MISSINGNESS_PREVALENCE.csv`
- `RESPONSE_TOPOLOGY_AUDIT.csv`
- `IDENTITY_JOIN_AUDIT.csv`
- `R1_AUTHORITY_JOIN_AUDIT.csv`
- `CANONICAL_REGISTRY_JOIN_AUDIT.csv`
- `GOVERNED_SCOPE_COMPARISON.csv`
- `FACET_READY_PARITY_AUDIT.csv`
- `CACHE_SELECTED_PARITY.csv`
- `CACHE_IDENTITY_EXACT.csv`
- `INFORMATION_LOSS_AUDIT.csv`
- `STATIC_EVIDENCE_PROVENANCE.csv`
- invariant/failure ledgers and run summaries.

A completing worker is not authorized to modify these semantics to accommodate the database.

## Source-equivalent authority question

Because populated data are still inaccessible here, the current state is:

`UNDETERMINED_DUE_TO_BLOCKED_POPULATED_DATA_ACCESS`

The allowed substantive outcomes remain:

- `PROVED_SOURCE_EQUIVALENT`
- `POTENTIALLY_SOURCE_EQUIVALENT_UNPROVED`
- `DERIVED_CACHE_WITH_KNOWN_LOSS`
- `DERIVED_CACHE_WITH_UNKNOWN_LOSS`
- `NOT_SOURCE_EQUIVALENT`

The proof bar remains hostile: **database-internal parity alone cannot yield `PROVED_SOURCE_EQUIVALENT`.** Source-native evidence must additionally establish routing/not-asked semantics, original labels/codes where not retained, weighting design, geography/demographic detail, multiple-response semantics, source identifiers, and ingest provenance.

## Final court state

Empirical court:

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

Audit apparatus:

`CLOSED_EXECUTABLE_FIXED_SEMANTICS`

The next worker with DB access does not design D05. They run it.
