\set ON_ERROR_STOP on
\pset pager off
\pset footer off

\echo '=== SR02 R3 P00 ENVIRONMENT ==='
SELECT current_database() AS database_name,
       current_user AS database_user,
       current_setting('server_version') AS server_version,
       current_setting('transaction_read_only') AS transaction_read_only,
       clock_timestamp() AS probe_time;

BEGIN TRANSACTION READ ONLY;

\echo '=== SR02 R3 P01 STATIC-CONTRACT LIVE SCHEMA PREFLIGHT ==='
\echo '-- Missing required columns from exact user-supplied schema contract (must return zero rows)'
WITH expected(relation_name,column_name) AS (VALUES
 ('survey_microdata_respondents','id'),('survey_microdata_respondents','source'),('survey_microdata_respondents','wave'),('survey_microdata_respondents','country_code'),('survey_microdata_respondents','survey_year'),('survey_microdata_respondents','dataset_id'),('survey_microdata_respondents','source_file'),('survey_microdata_respondents','upload_date'),
 ('survey_microdata_responses','respondent_id'),('survey_microdata_responses','var_code'),('survey_microdata_responses','value_raw'),('survey_microdata_responses','value_text'),('survey_microdata_responses','dataset_id'),('survey_microdata_responses','source_file'),('survey_microdata_responses','upload_date'),
 ('survey_weight_fact','respondent_id'),('survey_weight_fact','weight_name'),('survey_weight_fact','weight_value'),('survey_weight_fact','weight_type'),('survey_weight_fact','source_var'),('survey_weight_fact','source'),('survey_weight_fact','wave'),('survey_weight_fact','is_primary'),('survey_weight_fact','loaded_at'),
 ('respondent_source_wave_identity','raw_db_source'),('respondent_source_wave_identity','raw_db_wave'),('respondent_source_wave_identity','source_family_uid'),('respondent_source_wave_identity','wave_uid'),('respondent_source_wave_identity','canonical_display_source'),('respondent_source_wave_identity','canonical_display_wave'),('respondent_source_wave_identity','governance_state'),('respondent_source_wave_identity','closed_35_member'),('respondent_source_wave_identity','loaded_at'),
 ('question_structural_mapping','source'),('question_structural_mapping','wave'),('question_structural_mapping','question_id'),('question_structural_mapping','var_code'),('question_structural_mapping','mapping_status'),('question_structural_mapping','loaded_at'),('question_structural_mapping','source_family_uid'),('question_structural_mapping','wave_uid'),('question_structural_mapping','canonical_display_source'),('question_structural_mapping','canonical_display_wave'),('question_structural_mapping','governance_state'),('question_structural_mapping','closed_35_member'),
 ('respondent_position_fact','respondent_id'),('respondent_position_fact','source_family'),('respondent_position_fact','wave'),('respondent_position_fact','country_code'),('respondent_position_fact','survey_year'),('respondent_position_fact','sex'),('respondent_position_fact','age'),('respondent_position_fact','age_group'),('respondent_position_fact','education_level'),('respondent_position_fact','income_level'),('respondent_position_fact','religion_label'),('respondent_position_fact','urban_rural'),('respondent_position_fact','region'),('respondent_position_fact','ethnicity'),('respondent_position_fact','language'),('respondent_position_fact','employment'),('respondent_position_fact','marital'),('respondent_position_fact','household_size'),('respondent_position_fact','position_source_table'),('respondent_position_fact','position_completeness_score'),
 ('v_ddm_response_long_facet_ready','respondent_id'),('v_ddm_response_long_facet_ready','source'),('v_ddm_response_long_facet_ready','wave'),('v_ddm_response_long_facet_ready','canonical_wave'),('v_ddm_response_long_facet_ready','country_code'),('v_ddm_response_long_facet_ready','survey_year'),('v_ddm_response_long_facet_ready','var_code'),('v_ddm_response_long_facet_ready','value_raw'),('v_ddm_response_long_facet_ready','value_text'),('v_ddm_response_long_facet_ready','weight_value'),('v_ddm_response_long_facet_ready','weight_name'),('v_ddm_response_long_facet_ready','weight_status'),('v_ddm_response_long_facet_ready','sex'),('v_ddm_response_long_facet_ready','age'),('v_ddm_response_long_facet_ready','age_group'),('v_ddm_response_long_facet_ready','education_level'),('v_ddm_response_long_facet_ready','income_level'),('v_ddm_response_long_facet_ready','religion_label'),('v_ddm_response_long_facet_ready','urban_rural'),('v_ddm_response_long_facet_ready','region'),('v_ddm_response_long_facet_ready','ethnicity'),('v_ddm_response_long_facet_ready','language'),('v_ddm_response_long_facet_ready','employment'),('v_ddm_response_long_facet_ready','marital'),('v_ddm_response_long_facet_ready','household_size'),('v_ddm_response_long_facet_ready','position_source_table'),('v_ddm_response_long_facet_ready','position_completeness_score'),('v_ddm_response_long_facet_ready','question_id'),('v_ddm_response_long_facet_ready','question_block_id'),('v_ddm_response_long_facet_ready','structural_domain_id'),('v_ddm_response_long_facet_ready','driver_id'),('v_ddm_response_long_facet_ready','driver_facet_id'),('v_ddm_response_long_facet_ready','relation_axis_id'),('v_ddm_response_long_facet_ready','target_entity_id'),('v_ddm_response_long_facet_ready','mapping_status'),('v_ddm_response_long_facet_ready','legacy_final_driver_id'),('v_ddm_response_long_facet_ready','legacy_driver_leak_flag'),
 ('survey_microdata_reload_progress','source_family'),('survey_microdata_reload_progress','wave_filter'),('survey_microdata_reload_progress','file_index'),('survey_microdata_reload_progress','row_index'),('survey_microdata_reload_progress','updated_at'),
 ('ddm_inline_respondent_build_progress','source_family'),('ddm_inline_respondent_build_progress','wave_filter'),('ddm_inline_respondent_build_progress','file_index'),('ddm_inline_respondent_build_progress','row_index'),('ddm_inline_respondent_build_progress','updated_at'),
 ('ddm_named_respondent_demographics_progress','source_family'),('ddm_named_respondent_demographics_progress','wave_filter'),('ddm_named_respondent_demographics_progress','chunk_idx'),('ddm_named_respondent_demographics_progress','updated_at'),
 ('ddm_template_rebuild_progress','source_family'),('ddm_template_rebuild_progress','wave'),('ddm_template_rebuild_progress','chunk_idx'),('ddm_template_rebuild_progress','updated_at'),
 ('evs_loader_chunk_progress','source_family'),('evs_loader_chunk_progress','survey_year'),('evs_loader_chunk_progress','source_path'),('evs_loader_chunk_progress','chunk_offset'),('evs_loader_chunk_progress','chunk_rows'),('evs_loader_chunk_progress','respondent_rows'),('evs_loader_chunk_progress','response_rows'),('evs_loader_chunk_progress','completed_at'),
 ('country_identity_repair_runs','repair_run_id'),('country_identity_repair_runs','status'),('country_identity_repair_runs','started_at'),('country_identity_repair_runs','completed_at'),('country_identity_repair_runs','rolled_back_at'),
 ('country_identity_repair_base_snapshot','repair_run_id'),('country_identity_repair_base_snapshot','respondent_id'),('country_identity_repair_base_snapshot','old_country_code'),('country_identity_repair_base_snapshot','corrected_country_code'),('country_identity_repair_base_snapshot','source_family'),('country_identity_repair_base_snapshot','wave'),('country_identity_repair_base_snapshot','snapshot_at'),
 ('country_identity_repair_demo_snapshot','repair_run_id'),('country_identity_repair_demo_snapshot','demo_table_name'),('country_identity_repair_demo_snapshot','respondent_id'),('country_identity_repair_demo_snapshot','old_country_code'),('country_identity_repair_demo_snapshot','corrected_country_code'),('country_identity_repair_demo_snapshot','source_family'),('country_identity_repair_demo_snapshot','wave'),('country_identity_repair_demo_snapshot','snapshot_at'),
 ('country_identity_repair_response_invariants','repair_run_id'),('country_identity_repair_response_invariants','phase'),('country_identity_repair_response_invariants','bucket'),('country_identity_repair_response_invariants','response_row_count'),('country_identity_repair_response_invariants','distinct_respondent_count'),('country_identity_repair_response_invariants','aggregate_digest'),('country_identity_repair_response_invariants','created_at')
), missing AS (
 SELECT e.relation_name,e.column_name
 FROM expected e
 LEFT JOIN information_schema.columns c
   ON c.table_schema='public' AND c.table_name=e.relation_name AND c.column_name=e.column_name
 WHERE c.column_name IS NULL
)
SELECT * FROM missing ORDER BY relation_name,column_name;

WITH expected(relation_name,column_name) AS (VALUES
 ('survey_microdata_respondents','id'),('survey_microdata_respondents','source'),('survey_microdata_respondents','wave'),('survey_microdata_respondents','country_code'),('survey_microdata_respondents','survey_year'),('survey_microdata_respondents','dataset_id'),('survey_microdata_respondents','source_file'),('survey_microdata_respondents','upload_date'),
 ('survey_microdata_responses','respondent_id'),('survey_microdata_responses','var_code'),('survey_microdata_responses','value_raw'),('survey_microdata_responses','value_text'),('survey_microdata_responses','dataset_id'),('survey_microdata_responses','source_file'),('survey_microdata_responses','upload_date'),
 ('survey_weight_fact','respondent_id'),('survey_weight_fact','weight_name'),('survey_weight_fact','weight_value'),('survey_weight_fact','weight_type'),('survey_weight_fact','source_var'),('survey_weight_fact','source'),('survey_weight_fact','wave'),('survey_weight_fact','is_primary'),('survey_weight_fact','loaded_at'),
 ('respondent_source_wave_identity','raw_db_source'),('respondent_source_wave_identity','raw_db_wave'),('respondent_source_wave_identity','source_family_uid'),('respondent_source_wave_identity','wave_uid'),('respondent_source_wave_identity','canonical_display_source'),('respondent_source_wave_identity','canonical_display_wave'),('respondent_source_wave_identity','governance_state'),('respondent_source_wave_identity','closed_35_member'),('respondent_source_wave_identity','loaded_at'),
 ('question_structural_mapping','source'),('question_structural_mapping','wave'),('question_structural_mapping','question_id'),('question_structural_mapping','var_code'),('question_structural_mapping','mapping_status'),('question_structural_mapping','loaded_at'),('question_structural_mapping','source_family_uid'),('question_structural_mapping','wave_uid'),('question_structural_mapping','canonical_display_source'),('question_structural_mapping','canonical_display_wave'),('question_structural_mapping','governance_state'),('question_structural_mapping','closed_35_member'),
 ('respondent_position_fact','respondent_id'),('respondent_position_fact','source_family'),('respondent_position_fact','wave'),('respondent_position_fact','country_code'),('respondent_position_fact','survey_year'),('respondent_position_fact','sex'),('respondent_position_fact','age'),('respondent_position_fact','age_group'),('respondent_position_fact','education_level'),('respondent_position_fact','income_level'),('respondent_position_fact','religion_label'),('respondent_position_fact','urban_rural'),('respondent_position_fact','region'),('respondent_position_fact','ethnicity'),('respondent_position_fact','language'),('respondent_position_fact','employment'),('respondent_position_fact','marital'),('respondent_position_fact','household_size'),('respondent_position_fact','position_source_table'),('respondent_position_fact','position_completeness_score'),
 ('v_ddm_response_long_facet_ready','respondent_id'),('v_ddm_response_long_facet_ready','source'),('v_ddm_response_long_facet_ready','wave'),('v_ddm_response_long_facet_ready','canonical_wave'),('v_ddm_response_long_facet_ready','country_code'),('v_ddm_response_long_facet_ready','survey_year'),('v_ddm_response_long_facet_ready','var_code'),('v_ddm_response_long_facet_ready','value_raw'),('v_ddm_response_long_facet_ready','value_text'),('v_ddm_response_long_facet_ready','weight_value'),('v_ddm_response_long_facet_ready','weight_name'),('v_ddm_response_long_facet_ready','weight_status'),('v_ddm_response_long_facet_ready','sex'),('v_ddm_response_long_facet_ready','age'),('v_ddm_response_long_facet_ready','age_group'),('v_ddm_response_long_facet_ready','education_level'),('v_ddm_response_long_facet_ready','income_level'),('v_ddm_response_long_facet_ready','religion_label'),('v_ddm_response_long_facet_ready','urban_rural'),('v_ddm_response_long_facet_ready','region'),('v_ddm_response_long_facet_ready','ethnicity'),('v_ddm_response_long_facet_ready','language'),('v_ddm_response_long_facet_ready','employment'),('v_ddm_response_long_facet_ready','marital'),('v_ddm_response_long_facet_ready','household_size'),('v_ddm_response_long_facet_ready','position_source_table'),('v_ddm_response_long_facet_ready','position_completeness_score'),('v_ddm_response_long_facet_ready','question_id'),('v_ddm_response_long_facet_ready','question_block_id'),('v_ddm_response_long_facet_ready','structural_domain_id'),('v_ddm_response_long_facet_ready','driver_id'),('v_ddm_response_long_facet_ready','driver_facet_id'),('v_ddm_response_long_facet_ready','relation_axis_id'),('v_ddm_response_long_facet_ready','target_entity_id'),('v_ddm_response_long_facet_ready','mapping_status'),('v_ddm_response_long_facet_ready','legacy_final_driver_id'),('v_ddm_response_long_facet_ready','legacy_driver_leak_flag'),
 ('survey_microdata_reload_progress','source_family'),('survey_microdata_reload_progress','wave_filter'),('survey_microdata_reload_progress','file_index'),('survey_microdata_reload_progress','row_index'),('survey_microdata_reload_progress','updated_at'),
 ('ddm_inline_respondent_build_progress','source_family'),('ddm_inline_respondent_build_progress','wave_filter'),('ddm_inline_respondent_build_progress','file_index'),('ddm_inline_respondent_build_progress','row_index'),('ddm_inline_respondent_build_progress','updated_at'),
 ('ddm_named_respondent_demographics_progress','source_family'),('ddm_named_respondent_demographics_progress','wave_filter'),('ddm_named_respondent_demographics_progress','chunk_idx'),('ddm_named_respondent_demographics_progress','updated_at'),
 ('ddm_template_rebuild_progress','source_family'),('ddm_template_rebuild_progress','wave'),('ddm_template_rebuild_progress','chunk_idx'),('ddm_template_rebuild_progress','updated_at'),
 ('evs_loader_chunk_progress','source_family'),('evs_loader_chunk_progress','survey_year'),('evs_loader_chunk_progress','source_path'),('evs_loader_chunk_progress','chunk_offset'),('evs_loader_chunk_progress','chunk_rows'),('evs_loader_chunk_progress','respondent_rows'),('evs_loader_chunk_progress','response_rows'),('evs_loader_chunk_progress','completed_at'),
 ('country_identity_repair_runs','repair_run_id'),('country_identity_repair_runs','status'),('country_identity_repair_runs','started_at'),('country_identity_repair_runs','completed_at'),('country_identity_repair_runs','rolled_back_at'),
 ('country_identity_repair_base_snapshot','repair_run_id'),('country_identity_repair_base_snapshot','respondent_id'),('country_identity_repair_base_snapshot','old_country_code'),('country_identity_repair_base_snapshot','corrected_country_code'),('country_identity_repair_base_snapshot','source_family'),('country_identity_repair_base_snapshot','wave'),('country_identity_repair_base_snapshot','snapshot_at'),
 ('country_identity_repair_demo_snapshot','repair_run_id'),('country_identity_repair_demo_snapshot','demo_table_name'),('country_identity_repair_demo_snapshot','respondent_id'),('country_identity_repair_demo_snapshot','old_country_code'),('country_identity_repair_demo_snapshot','corrected_country_code'),('country_identity_repair_demo_snapshot','source_family'),('country_identity_repair_demo_snapshot','wave'),('country_identity_repair_demo_snapshot','snapshot_at'),
 ('country_identity_repair_response_invariants','repair_run_id'),('country_identity_repair_response_invariants','phase'),('country_identity_repair_response_invariants','bucket'),('country_identity_repair_response_invariants','response_row_count'),('country_identity_repair_response_invariants','distinct_respondent_count'),('country_identity_repair_response_invariants','aggregate_digest'),('country_identity_repair_response_invariants','created_at')
), missing AS (
 SELECT e.relation_name,e.column_name
 FROM expected e
 LEFT JOIN information_schema.columns c
   ON c.table_schema='public' AND c.table_name=e.relation_name AND c.column_name=e.column_name
 WHERE c.column_name IS NULL
)
SELECT NOT EXISTS (SELECT 1 FROM missing) AS sr02_required_schema_ok \gset
\if :sr02_required_schema_ok
\echo 'SR02_REQUIRED_SCHEMA_PREFLIGHT_PASS'
\else
\echo 'SR02_REQUIRED_SCHEMA_PREFLIGHT_FAIL'
\quit 3
\endif

\echo '=== SR02 R3 P02 RESPONDENTSDEMO SCHEMA PREFLIGHT ==='
\echo '-- Exact supplied schema contains 36 physical respondentsDemo* tables. All must expose the fields used by respondent_position_fact plus provenance fields.'
WITH demo_tables AS (
 SELECT table_name FROM information_schema.tables
 WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE 'respondentsDemo%'
), required(column_name) AS (VALUES
 ('respondent_id'),('source_family'),('wave'),('dataset_id'),('source_file'),('country_code'),('survey_year'),
 ('sex'),('age'),('education_level'),('income_level'),('income_source_note'),('survey_weight'),('survey_weight_source_var'),
 ('urban_rural'),('religion_label'),('marital'),('employment'),('class_level'),('household_size'),('language'),('region'),('ethnicity'),('loaded_at')
), missing AS (
 SELECT d.table_name,r.column_name
 FROM demo_tables d CROSS JOIN required r
 LEFT JOIN information_schema.columns c
   ON c.table_schema='public' AND c.table_name=d.table_name AND c.column_name=r.column_name
 WHERE c.column_name IS NULL
)
SELECT * FROM missing ORDER BY table_name,column_name;

WITH demo_tables AS (
 SELECT table_name FROM information_schema.tables
 WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE 'respondentsDemo%'
), required(column_name) AS (VALUES
 ('respondent_id'),('source_family'),('wave'),('dataset_id'),('source_file'),('country_code'),('survey_year'),
 ('sex'),('age'),('education_level'),('income_level'),('income_source_note'),('survey_weight'),('survey_weight_source_var'),
 ('urban_rural'),('religion_label'),('marital'),('employment'),('class_level'),('household_size'),('language'),('region'),('ethnicity'),('loaded_at')
), missing AS (
 SELECT d.table_name,r.column_name
 FROM demo_tables d CROSS JOIN required r
 LEFT JOIN information_schema.columns c
   ON c.table_schema='public' AND c.table_name=d.table_name AND c.column_name=r.column_name
 WHERE c.column_name IS NULL
)
SELECT ((SELECT COUNT(*) FROM demo_tables)=36 AND NOT EXISTS (SELECT 1 FROM missing)) AS sr02_demo_schema_ok \gset
\if :sr02_demo_schema_ok
\echo 'SR02_RESPONDENTSDEMO_SCHEMA_PREFLIGHT_PASS'
\else
\echo 'SR02_RESPONDENTSDEMO_SCHEMA_PREFLIGHT_FAIL'
\quit 3
\endif

\echo '=== SR02 R3 P03 RUNTIME RELATION EXISTENCE / KIND ==='
WITH wanted(name,class) AS (VALUES
 ('survey_microdata_respondents','DIRECT_RUNTIME_V550'),
 ('survey_microdata_responses','TRANSITIVE_RUNTIME_V550'),
 ('survey_weight_fact','DIRECT_AND_TRANSITIVE_RUNTIME_V550'),
 ('respondent_source_wave_identity','TRANSITIVE_RUNTIME_V550'),
 ('question_structural_mapping','DIRECT_AND_TRANSITIVE_RUNTIME_V550'),
 ('respondent_position_fact','DIRECT_RUNTIME_V550'),
 ('v_ddm_response_long_facet_ready','DIRECT_RUNTIME_V550'),
 ('v_ddm_response_long_facet_ready_authority','CONDITIONAL_RUNTIME_OVERRIDE'),
 ('survey_authority_compendium','CONDITIONAL_RUNTIME_OVERRIDE')
)
SELECT w.name,w.class,COALESCE(c.relkind::text,'ABSENT') AS relation_kind
FROM wanted w
LEFT JOIN pg_class c ON c.relname=w.name
LEFT JOIN pg_namespace n ON n.oid=c.relnamespace AND n.nspname='public'
ORDER BY w.class,w.name;

\echo '=== SR02 R3 P04 RUNTIME VIEW DEFINITION FINGERPRINTS ==='
SELECT c.relname AS view_name,
       md5(pg_get_viewdef(c.oid,true)) AS view_definition_md5,
       length(pg_get_viewdef(c.oid,true)) AS view_definition_chars
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public'
  AND c.relname IN ('respondent_position_fact','v_ddm_response_long_facet_ready','v_ddm_response_long_facet_ready_authority')
ORDER BY c.relname;

\echo '=== SR02 R3 P05 RESPONDENT WRITE EPOCHS BY SOURCE/WAVE ==='
SELECT source,wave,dataset_id,source_file,
       COUNT(*) AS respondents,
       MIN(id) AS min_respondent_id,
       MAX(id) AS max_respondent_id,
       MIN(upload_date) AS min_upload_date,
       MAX(upload_date) AS max_upload_date,
       COUNT(DISTINCT upload_date) AS distinct_upload_timestamps
FROM survey_microdata_respondents
GROUP BY source,wave,dataset_id,source_file
ORDER BY source,wave,dataset_id,source_file;

\echo '=== SR02 R3 P06 RESPONSE WRITE EPOCHS BY DATASET/SOURCE FILE — LOW-TEMP ==='
SELECT dataset_id,source_file,
       COUNT(*) AS response_rows,
       MIN(respondent_id) AS min_respondent_id,
       MAX(respondent_id) AS max_respondent_id,
       MIN(upload_date) AS min_upload_date,
       MAX(upload_date) AS max_upload_date
FROM survey_microdata_responses
GROUP BY dataset_id,source_file
ORDER BY dataset_id,source_file;

\echo '=== SR02 R3 P07 WEIGHT WRITE EPOCHS ==='
SELECT source,wave,weight_name,weight_type,source_var,is_primary,
       COUNT(*) AS rows,
       COUNT(*) FILTER (WHERE weight_value IS NULL) AS null_weight_rows,
       MIN(loaded_at) AS min_loaded_at,
       MAX(loaded_at) AS max_loaded_at
FROM survey_weight_fact
GROUP BY source,wave,weight_name,weight_type,source_var,is_primary
ORDER BY source,wave,weight_name,source_var,is_primary;

\echo '=== SR02 R3 P08 SOURCE/WAVE IDENTITY CURRENT STATE / LOAD EPOCHS ==='
SELECT raw_db_source,raw_db_wave,canonical_display_source,canonical_display_wave,
       source_family_uid,wave_uid,governance_state,closed_35_member,
       COUNT(*) AS rows,
       MIN(loaded_at) AS min_loaded_at,
       MAX(loaded_at) AS max_loaded_at
FROM respondent_source_wave_identity
GROUP BY raw_db_source,raw_db_wave,canonical_display_source,canonical_display_wave,
         source_family_uid,wave_uid,governance_state,closed_35_member
ORDER BY raw_db_source,raw_db_wave;

\echo '=== SR02 R3 P09 QUESTION STRUCTURAL MAPPING CURRENT STATE / LOAD EPOCHS ==='
SELECT source_family_uid,wave_uid,source,wave,mapping_status,
       COUNT(*) AS rows,
       MIN(loaded_at) AS min_loaded_at,
       MAX(loaded_at) AS max_loaded_at
FROM question_structural_mapping
GROUP BY source_family_uid,wave_uid,source,wave,mapping_status
ORDER BY source_family_uid,wave_uid,source,wave,mapping_status;

\echo '=== SR02 R3 P10 NAMED RESPONDENTSDEMO OCCUPANCY / LOAD EPOCHS ==='
SELECT format(
  'SELECT %L AS table_name, COUNT(*) AS rows, COUNT(DISTINCT respondent_id) AS distinct_respondents, MIN(loaded_at) AS min_loaded_at, MAX(loaded_at) AS max_loaded_at FROM public.%I;',
  c.relname,c.relname)
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r' AND c.relname LIKE 'respondentsDemo%'
ORDER BY c.relname
\gexec

\echo '=== SR02 R3 P11 NAMED RESPONDENTSDEMO SOURCE/WAVE/DATASET OCCUPANCY ==='
SELECT format(
  'SELECT %L AS table_name, source_family, wave, dataset_id, source_file, COUNT(*) AS rows FROM public.%I GROUP BY source_family,wave,dataset_id,source_file ORDER BY source_family,wave,dataset_id,source_file;',
  c.relname,c.relname)
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r' AND c.relname LIKE 'respondentsDemo%'
ORDER BY c.relname
\gexec

\echo '=== SR02 R3 P12 PROVENANCE-ONLY RELOAD/BUILD PROGRESS ==='
\echo '-- survey_microdata_reload_progress'
TABLE survey_microdata_reload_progress;
\echo '-- ddm_inline_respondent_build_progress'
SELECT * FROM ddm_inline_respondent_build_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- ddm_named_respondent_demographics_progress'
SELECT * FROM ddm_named_respondent_demographics_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- ddm_template_rebuild_progress'
SELECT * FROM ddm_template_rebuild_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- evs_loader_chunk_progress'
SELECT * FROM evs_loader_chunk_progress ORDER BY 1,2 LIMIT 5000;

\echo '=== SR02 R3 P13 PROVENANCE-ONLY COUNTRY IDENTITY REPAIR EVIDENCE ==='
SELECT * FROM country_identity_repair_runs ORDER BY started_at,repair_run_id LIMIT 5000;
SELECT 'country_identity_repair_base_snapshot' AS relation,COUNT(*) AS rows,MIN(snapshot_at) AS min_snapshot_at,MAX(snapshot_at) AS max_snapshot_at FROM country_identity_repair_base_snapshot
UNION ALL
SELECT 'country_identity_repair_demo_snapshot',COUNT(*),MIN(snapshot_at),MAX(snapshot_at) FROM country_identity_repair_demo_snapshot
UNION ALL
SELECT 'country_identity_repair_response_invariants',COUNT(*),MIN(created_at),MAX(created_at) FROM country_identity_repair_response_invariants;

\echo '=== SR02 R3 P14 CONDITIONAL OVERRIDE SURFACE OCCUPANCY ==='
SELECT to_regclass('public.v_ddm_response_long_facet_ready_authority') AS authority_response_view,
       to_regclass('public.survey_authority_compendium') AS authority_compendium;
SELECT CASE
  WHEN to_regclass('public.survey_authority_compendium') IS NOT NULL THEN
    'SELECT source,wave,COUNT(*) AS rows,MIN(loaded_at) AS min_loaded_at,MAX(loaded_at) AS max_loaded_at FROM public.survey_authority_compendium GROUP BY source,wave ORDER BY source,wave;'
  ELSE
    'SELECT ''survey_authority_compendium_absent''::text AS status;'
END
\gexec

\echo '=== SR02 R3 COMPLETE ==='
ROLLBACK;
SELECT 'PRE553_SR02_CURRENT_DB_PROVENANCE_RECEIPT_COMPLETE' AS completion_token;
