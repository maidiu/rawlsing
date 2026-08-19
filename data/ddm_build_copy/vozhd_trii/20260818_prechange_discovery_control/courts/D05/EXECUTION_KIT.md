# D05 — Populated Empirical Substrate Execution Kit

**Apparatus:** `CLOSED_EXECUTABLE_FIXED_SEMANTICS`  
**Empirical verdict in this worker environment:** `BLOCKED_MISSING_POPULATED_DATA_ACCESS`

The database blocker does not reopen the audit design. A worker with populated database access supplies only a connection string and runs the canonical command.

## Canonical command

```bash
DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DBNAME' \
  bash data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/run_d05_empirical_audit.sh
```

There are **zero semantic command-line choices**. The worker does not select source families, waves, countries, questions, overlap subsets, position fields, authority lanes, response relations, or cache scopes.

## Canonical execution stages

The shell entrypoint runs all stages even when an earlier stage finds a fatal empirical defect, then returns non-zero if any stage failed:

1. `run_d05_empirical_audit.py` — core relation preflight, coverage, multiplicity, positions, weights, mapping, typed missingness, topology, raw/facet parity, information-loss and provenance outputs.
2. `audit_d05_identity_overlap_exact.py` — first-class respondent identity/collision audit and **complete all-pairs question overlap including zero-overlap pairs**. It overwrites the weaker core overlap output with the normative complete surface.
3. `audit_d05_output_semantic_guard.py` — output-only guard that prevents a physically absent `value_raw`/`value_text` field from masquerading as a zero-mismatch preservation result.
4. `audit_d05_authority_scope_cache.py` — current production R1 resolution, canonical-registry/alias reconciliation, `CLOSED_35` population comparison, and materialized shared-cache selected-row/predicate parity.
5. `audit_d05_cache_identity_exact.py` — exact respondent-ID set equality for every materialized shared-cache selection. Matching respondent counts are not sufficient.

Every database stage opens `REPEATABLE READ, READ ONLY` and verifies `transaction_read_only = on`. No stage contains DDL, DML, repair, ingestion, or retention mutation. Files are written only under `courts/D05/`.

## Normative contract

`D05_AUDIT_CONTRACT.json` is the single machine-readable law for:

- required/expected relations and columns;
- physical measurement grains;
- output schemas;
- invariants;
- named failure/warning codes;
- production R1 resolver law;
- source-equivalence classification bar;
- locked external-evidence SHA256 values.

If this prose and the JSON contract conflict, the R4 JSON contract governs.

## Fatal populated-data core

The two fatal relations are:

`public.survey_microdata_respondents`

- `id`
- `source`
- `wave`
- `country_code`
- `survey_year`

`public.survey_microdata_responses`

- `respondent_id`
- `var_code`
- `value_raw`
- `value_text`

Expected non-core audit targets are:

- `public.survey_weight_fact`
- `public.respondent_position_fact`
- `public.question_structural_mapping`
- `public.survey_authority_compendium`
- `public.v_ddm_response_long_facet_ready`
- `public.v_ddm_response_long_facet_ready_authority`
- `public.ddm_demographic_field_register`
- a uniquely discoverable installed `canonical_question_registry`, if present;
- its same-schema `question_variable_alias`, if present.

Absent non-core surfaces are findings, not permission to invent substitutes.

## Respondent identity

`RESPONDENT_IDENTITY_AUDIT.csv` makes identity claims explicit. It measures globally and by source/wave/country:

- respondent row count;
- distinct surrogate IDs;
- null IDs;
- duplicate-ID groups and excess rows;
- IDs spanning multiple source/waves;
- IDs spanning multiple countries;
- IDs spanning multiple survey years;
- response rows;
- orphan response rows.

A duplicate/collision/orphan is a fatal empirical finding. Schema PK/FK declarations are not used as substitutes for populated counts.

## Complete question cotravel coverage

`QUESTION_OVERLAP_SUMMARY.csv` contains **every unordered pair of populated var codes** inside each source/wave/country. The query forms the complete pair universe from marginal respondent incidence and left-joins same-respondent overlap, so pairs with `respondents_overlap = 0` are retained.

For every pair the output contains both marginals, overlap, union, overlap percentages, Jaccard percentage, overlap where both respondent/var cells are unique, duplicate-compromised overlap, and `cotravel_possible`.

`QUESTION_OVERLAP_COMPLETENESS.json` records total pair rows and the number of zero-overlap pairs emitted. Zero overlap is evidence of physical module/routing separation; it is not missing output.

## Multiplicity

`RESPONSE_MULTIPLICITY_AUDIT.csv` measures separately:

- raw `(respondent_id,var_code)` multiplicity;
- excess duplicate raw rows;
- canonical `(respondent_id,question_id)` multiplicity after current mapping;
- distinct questions/respondent and response rows/respondent with min/P50/P90/P99/max.

Multiple responses are therefore not silently collapsed.

## Position completeness

`POSITION_FIELD_COMPLETENESS.csv` measures coverage/cardinality by field/source/wave for the governed surface:

sex, age, age_group, education_level, income_level, religion_label, urban_rural, region, ethnicity, language, employment, marital, household_size, class_level.

`age_group` is explicitly a facet-derived coordinate where appropriate. Additional source-native demographic candidates from `ddm_demographic_field_register` are reported as candidates only; register presence is not proof of respondent-fact survival.

Null/blank position values mean database missingness only.

## Typed missingness and topology

DK, refusal, IAP/not-asked, missing, and substantive-response prevalence are computed only from explicit typed columns such as `is_dk`, `is_refusal`, `is_iap`, `is_missing`, and `is_valid_substantive_response`. Blank `value_raw`/`value_text` is never reinterpreted as one of those categories.

Question topology is never guessed from response cardinality. `RESPONSE_TOPOLOGY_AUDIT.csv` places observed cardinality beside physically exposed question/topology/handling authority; if the authority field is absent, the result says so.

## Weights

`WEIGHT_COVERAGE.csv` measures any/primary/missing/multiple-primary respondent state, total and primary rows, null/zero/negative/non-finite primary values, and actual weight names/types/source vars.

The information-loss surface separately checks whether PSU/stratum/cluster/FPC/replicate design metadata are represented. A scalar weight is never called design-based inference authority or population truth.

## Raw-to-facet preservation

`FACET_READY_PARITY_AUDIT.csv` full-outer-compares raw responses with each available facet-ready relation at:

`source,wave,country_code,respondent_id,UPPER(var_code)`

It measures missing raw rows, derived-only rows, multiplicity differences, and `value_raw` / `value_text` multiset differences when those target fields physically exist.

`audit_d05_output_semantic_guard.py` converts absent target fields to `NOT_EXPOSED`; an absent field can never appear as “zero mismatches.”

The same output records whether physical respondent linkage and position columns are sufficient to reconstruct the row sets needed for:

- `P(Y | position)`
- `P(Y | position conjunction)`
- `P(Y | X response)`
- `P(Y | X response AND position)`

These are reconstructibility flags, not substantive inference authority.

## Three separate question-identity courts

D05 refuses to collapse three different identity mechanisms:

1. `IDENTITY_JOIN_AUDIT.csv` — current populated QSM exact/fallback/ambiguous/unmapped row partition.
2. `R1_AUTHORITY_JOIN_AUDIT.csv` — current production `resolve_question_relation_authority()` for every populated raw source/wave/country/var identity. D05 imports the production source/wave normalizers rather than cloning them.
3. `CANONICAL_REGISTRY_JOIN_AUDIT.csv` — exact canonical-registry and alias reconciliation when exactly one installed registry schema exists.

`GOVERNED_SCOPE_COMPARISON.csv` compares actual populated waves with production `active_closed_35_waves()`.

## Shared-cache truth

Every discovered `data/ddm_repository_copy/v550/**/v550_shared_respondent_substrate.parquet` is audited.

`CACHE_SELECTED_PARITY.csv` measures selected DB row/respondent cardinality plus position-field, typed-missingness, topology, and explicit selection-column preservation.

`CACHE_IDENTITY_EXACT.csv` closes the cardinality loophole. For every cache source/wave/country/var selection it computes exact respondent-ID sets on both sides and records:

- cache and DB ID-set cardinality;
- deterministic SHA256 of each sorted ID set;
- missing DB IDs in cache;
- extra cache IDs not in DB;
- exact raw-ID set equality;
- presence/hash/equality of `respondent_id_norm`.

No respondent IDs themselves are exported. Matching counts with different sets fail `D05_F_SHARED_CACHE_RESPONDENT_ID_DRIFT`.

## Static evidence provenance

At run time the core audit SHA256-hashes every checked-in static evidence file on its fixed list and records the Git blob SHA. Hash-addressed external evidence remains a separate provenance class.

Locked identities are:

- `Rawlsing_WVS_public_schema.sql` — `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` — `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`
- `rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip` — `e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861`
- `rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip` — `a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd`
- `rawlsing_chatlog_DDM_chatgpt_1.txt` — `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a`

Mismatch is fatal `D05_E_STATIC_PROVENANCE_MISMATCH`.

## Source-equivalence bar

Database-internal parity is not source equivalence. `PROVED_SOURCE_EQUIVALENT` remains unavailable unless source-native evidence also establishes routing/not-asked semantics, original labels/codes where not retained, weighting design, geographic detail, demographic coordinates, multiple-response semantics, source identifiers, and ingest provenance.

Therefore a database-only run can discover known loss or establish potential equivalence, but it cannot launder missing source-native evidence into a proof.
