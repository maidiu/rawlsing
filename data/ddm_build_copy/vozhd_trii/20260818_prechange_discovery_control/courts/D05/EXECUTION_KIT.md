# D05 populated-substrate execution kit

Status: `AUDIT_APPARATUS_CLOSED / POPULATED_EVIDENCE_BLOCKED`

Current court verdict remains `BLOCKED_MISSING_POPULATED_DATA_ACCESS`. This file closes the apparatus, not the empirical verdict.

## Canonical execution

There is one no-choice entrypoint:

```bash
DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DBNAME' \
  bash data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/run_d05_empirical_audit.sh
```

The worker does not choose source families, waves, countries, questions, position fields, overlap pairs, authority lanes, cache scopes, or mapping semantics. The runners audit the complete physically populated surfaces selected by the fixed contracts.

`run_d05_empirical_audit.py` is the core database/normalization audit. `audit_d05_authority_scope_cache.py` is automatically run second and adds production-R1 resolution, canonical-registry reconciliation, CLOSED_35 comparison, and selected-cache parity.

Both database runners establish `REPEATABLE READ, READ ONLY` transactions and abort if PostgreSQL does not report `transaction_read_only = on`. They contain no INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, TRUNCATE, COPY-to-database, or repair path. Their only writes are court output files under this D05 directory.

## Runtime dependencies

Required:

- Python 3.10+
- `psycopg2` (already used by the current facet-ready production loader)
- `git`
- PostgreSQL read credentials via `DATABASE_URL`

Required only when materialized V550 shared-substrate parquet files are present and therefore must be audited:

- `pandas`
- a parquet engine available to pandas (the same runtime class V550 uses for parquet materialization)

No populated-data substitute may be supplied as CSV excerpts or schema-only DDL. The database must be production or a transactionally consistent production-equivalent snapshot.

## Fixed relation contract

Fatal core surfaces:

- `public.survey_microdata_respondents`: `id`, `source`, `wave`, `country_code`, `survey_year`
- `public.survey_microdata_responses`: `respondent_id`, `var_code`, `value_raw`, `value_text`

Expected audited surfaces, with missing relations/columns emitted as named findings rather than silently aliased:

- `public.survey_weight_fact`
- `public.respondent_position_fact`
- `public.question_structural_mapping`
- `public.survey_authority_compendium`
- `public.v_ddm_response_long_facet_ready`
- `public.v_ddm_response_long_facet_ready_authority`
- `public.ddm_demographic_field_register`

The exact column lists are normative in `D05_AUDIT_CONTRACT.json` and duplicated as executable constants in the core runner. `canonical_question_registry` and `question_variable_alias` are discovered by relation name across schemas. Exactly one installed canonical-registry schema is allowed. Zero produces `D05_W_CANONICAL_REGISTRY_NOT_INSTALLED`; more than one produces `D05_E_AUTHORITY_SCHEMA_AMBIGUOUS`. The worker does not select one.

## Exact authority semantics

R1 identity is not reimplemented by this court. `audit_d05_authority_scope_cache.py` imports and calls current production functions from:

`data.ddm_build_copy.ddm_v550_question_relation_authority`

Specifically:

- `resolve_question_relation_authority()` for every populated raw source/wave/country/var identity;
- `canonical_source_family()` and `canonical_wave()` for governed identity normalization;
- `active_closed_35_waves()` for the governed closed-wave expectation;
- `load_question_relation_authority()` for the exact active R1 artifact and its SHA256.

That prevents D05 from inventing a parallel source/wave alias law.

## Queries and grains

The SQL in the Python runners is authoritative; there is no second hand-maintained SQL file whose semantics can drift.

The fixed measurement grains are:

- respondent identity: database respondent surrogate `survey_microdata_respondents.id`;
- raw response multiplicity: `(source, wave, country_code, respondent_id, UPPER(var_code))`;
- canonical-question multiplicity: the same respondent grain after the current exact-wave-first QSM resolution rule;
- source coverage: `(source, raw_wave, canonical_wave, country_code, survey_year)`;
- position completeness: `(position_field, source_family, wave)`;
- weight coverage: `(source, wave)` with respondent-level any/primary/multiple-primary states;
- question cotravel: **every unordered pair** of actually populated var codes within `(source, wave, country_code)`; no sample/top-N truncation;
- QSM identity: every raw response row partitioned into exact, fallback, ambiguous, or unmapped;
- R1 authority: every distinct populated `(source, raw_wave, country_code, var_code)` weighted by its raw response-row count;
- raw/facet parity: `(source, wave, country_code, respondent_id, UPPER(var_code))` multiplicity plus raw-code/raw-text multisets when physically exposed;
- cache parity: every `(source, wave, canonical_wave, country_code, var_code)` physically present in every discovered `v550_shared_respondent_substrate.parquet`.

## Missingness and topology law

Blank/null response values are never promoted into DK, refusal, IAP, or not-asked states. Those are measured only from explicit typed columns. If those columns are absent, the output says `COLUMN_NOT_EXPOSED` and emits `D05_W_TYPED_MISSINGNESS_NOT_EXPOSED`.

Likewise, binary/ordinal/nominal/scale/matrix/multi-select meaning is never inferred from the number of observed response values. `RESPONSE_TOPOLOGY_AUDIT.csv` reports physically exposed authority topology/classification alongside observed cardinality and respondent/var multiplicity so the two cannot be conflated.

## Weight law

The runner measures any weight, primary weight, missing primary weight, multiple primary weights, null/zero/negative/non-finite primary values, weight names, weight types, and source vars. It separately records whether PSU/stratum/cluster/FPC/replicate-design metadata are represented. A scalar primary weight is never called population truth or design-based inference authority.

## Facet-ready preservation law

For each available facet-ready relation, the runner performs a full outer comparison against the raw response substrate at respondent/var multiplicity grain. It reports:

- raw rows missing from facet;
- facet rows without raw parents;
- respondent/var keys whose multiplicity changed;
- raw-code multiset mismatches where `value_raw` is physically exposed;
- raw-text multiset mismatches where `value_text` is physically exposed;
- whether respondent linkage is sufficient for `P(Y | position)`, conjunctions of positions, `P(Y | X response)`, and `P(Y | X response AND position)`.

A view that lacks a raw field is evidence of non-exposure, not evidence of value preservation.

## Shared-cache law

The cache audit auto-discovers all files named `v550_shared_respondent_substrate.parquet` below `data/ddm_repository_copy/v550/`. It never treats absence as proof of loss; absence yields `D05_W_SHARED_CACHE_NOT_MATERIALIZED` and leaves cache losslessness unproved.

For every materialized cache it checks:

- selected DB row count vs cache row count for every cache source/wave/country/var;
- selected DB respondent count vs cache respondent count;
- explicit selection columns (`selection_role`, `base_fixture_selected`, `joint_configuration_selected`);
- required position-predicate columns;
- typed missingness columns;
- topology fields.

A cache can therefore be correctly identified as selective while still being tested for losslessness over the exact selection it claims to materialize.

## Static provenance law

At run time, every file named in the runner's `STATIC_FILES` list is SHA256-hashed and its Git blob SHA is recorded in `STATIC_EVIDENCE_PROVENANCE.csv`. External/hash-addressed evidence is kept distinct from checked-in evidence.

Locked conversation-input identities from `evidence/conversation_inputs/SHA256SUMS.txt` are:

- `Rawlsing_WVS_public_schema.sql` — `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` — `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`
- `rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip` — `e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861`
- `rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip` — `a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd`
- `rawlsing_chatlog_DDM_chatgpt_1.txt` — `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a`

The first D05 return contained incorrect values for the two schema hashes. Those values are superseded by the manifest identities above. Runtime mismatch is fatal: `D05_E_STATIC_PROVENANCE_MISMATCH`.

## Outputs

Core required/preferred outputs:

- `SOURCE_WAVE_READINESS.csv`
- `POSITION_FIELD_COMPLETENESS.csv`
- `QUESTION_OVERLAP_SUMMARY.csv`
- `WEIGHT_COVERAGE.csv`
- `IDENTITY_JOIN_AUDIT.csv`
- `RESPONSE_MULTIPLICITY_AUDIT.csv`

Additional closure outputs:

- `RELATION_PREFLIGHT.csv`
- `TYPED_MISSINGNESS_PREVALENCE.csv`
- `RESPONSE_TOPOLOGY_AUDIT.csv`
- `FACET_READY_PARITY_AUDIT.csv`
- `R1_AUTHORITY_JOIN_AUDIT.csv`
- `CANONICAL_REGISTRY_JOIN_AUDIT.csv`
- `GOVERNED_SCOPE_COMPARISON.csv`
- `CACHE_SELECTED_PARITY.csv`
- `INFORMATION_LOSS_AUDIT.csv`
- `STATIC_EVIDENCE_PROVENANCE.csv`
- `INVARIANT_RESULTS.csv`
- `FAILURES.csv`
- `EXTENDED_FAILURES.csv`
- `AUDIT_RUN.json`
- `EXTENDED_AUDIT_SUMMARY.json`

Every exact header and allowed source-equivalence classification is fixed in `D05_AUDIT_CONTRACT.json`.

## Source-equivalence bar

The apparatus may establish DB-internal row/predicate preservation or known loss. It may not return `PROVED_SOURCE_EQUIVALENT` merely because raw DB rows and derived views/cache agree. Proving source equivalence additionally requires source-native evidence for routing/not-asked semantics, original response labels/codes where not retained, weighting design, geography/demographic detail, and ingest provenance. Until those are physically verified, the strongest lawful outcome remains `POTENTIALLY_SOURCE_EQUIVALENT_UNPROVED`.
