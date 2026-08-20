\set ON_ERROR_STOP on
\pset pager off
\pset footer off
\echo '=== SR02 P00 ENVIRONMENT ==='
SELECT current_database() AS database_name,
       current_user AS database_user,
       current_setting('server_version') AS server_version,
       current_setting('transaction_read_only') AS transaction_read_only,
       clock_timestamp() AS probe_time;

BEGIN TRANSACTION READ ONLY;

\echo '=== SR02 P01 CORE RELATION EXISTENCE ==='
WITH wanted(name) AS (VALUES
 ('survey_microdata_respondents'),('survey_microdata_responses'),('survey_weight_fact'),
 ('survey_microdata_reload_progress'),('respondent_source_wave_identity'),('question_structural_mapping'),
 ('driver_aggregates'),('respondents'),('responses'),('variables'),('questions'),
 ('ddm_inline_respondent_build_progress'),('ddm_named_respondent_demographics_progress'),
 ('ddm_template_rebuild_progress'),('evs_loader_chunk_progress'),
 ('country_identity_repair_runs'),('country_identity_repair_base_snapshot'),
 ('country_identity_repair_demo_snapshot'),('country_identity_repair_response_invariants'))
SELECT w.name,
       CASE WHEN c.oid IS NULL THEN 'ABSENT' ELSE c.relkind::text END AS relation_kind
FROM wanted w
LEFT JOIN pg_class c ON c.relname=w.name
LEFT JOIN pg_namespace n ON n.oid=c.relnamespace AND n.nspname='public'
ORDER BY w.name;

\echo '=== SR02 P02 RESPONDENT WRITE EPOCHS BY SOURCE/WAVE ==='
SELECT source, wave, dataset_id, source_file,
       COUNT(*) AS respondents,
       MIN(id) AS min_respondent_id,
       MAX(id) AS max_respondent_id,
       MIN(upload_date) AS min_upload_date,
       MAX(upload_date) AS max_upload_date,
       COUNT(DISTINCT upload_date) AS distinct_upload_timestamps
FROM survey_microdata_respondents
GROUP BY source,wave,dataset_id,source_file
ORDER BY source,wave,dataset_id,source_file;

\echo '=== SR02 P03 RESPONSE WRITE EPOCHS BY DATASET/SOURCE FILE — LOW-TEMP SHAPE ==='
-- Deliberately avoids joining/grouping the full response table against respondents.
-- dataset_id/source_file are already source-wave provenance fields on the response rows.
-- This preserves the SR02 provenance question while keeping aggregate cardinality tiny.
SELECT dataset_id, source_file,
       COUNT(*) AS response_rows,
       MIN(respondent_id) AS min_respondent_id,
       MAX(respondent_id) AS max_respondent_id,
       MIN(upload_date) AS min_upload_date,
       MAX(upload_date) AS max_upload_date
FROM survey_microdata_responses
GROUP BY dataset_id,source_file
ORDER BY dataset_id,source_file;

\echo '=== SR02 P04 RESPONDENT ID RANGE BY SOURCE/WAVE — RESPONDENT TABLE ONLY ==='
-- Response-row counts are supplied by P03. Do not rejoin 48M response rows here.
SELECT source,wave,dataset_id,source_file,
       COUNT(*) AS respondents,
       MIN(id) AS min_respondent_id,
       MAX(id) AS max_respondent_id
FROM survey_microdata_respondents
GROUP BY source,wave,dataset_id,source_file
ORDER BY source,wave,dataset_id,source_file;

\echo '=== SR02 P05 WEIGHT WRITE EPOCHS ==='
SELECT source,wave,weight_name,weight_type,source_var,is_primary,
       COUNT(*) AS rows,
       COUNT(*) FILTER (WHERE weight_value IS NULL) AS null_weight_rows,
       MIN(loaded_at) AS min_loaded_at,
       MAX(loaded_at) AS max_loaded_at
FROM survey_weight_fact
GROUP BY source,wave,weight_name,weight_type,source_var,is_primary
ORDER BY source,wave,weight_name;

\echo '=== SR02 P06 RELOAD PROGRESS ==='
TABLE survey_microdata_reload_progress;

\echo '=== SR02 P07 KNOWN BUILD/REPAIR PROGRESS TABLE CONTENTS ==='
\echo '-- ddm_inline_respondent_build_progress'
SELECT * FROM ddm_inline_respondent_build_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- ddm_named_respondent_demographics_progress'
SELECT * FROM ddm_named_respondent_demographics_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- ddm_template_rebuild_progress'
SELECT * FROM ddm_template_rebuild_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- evs_loader_chunk_progress'
SELECT * FROM evs_loader_chunk_progress ORDER BY 1,2 LIMIT 5000;
\echo '-- country_identity_repair_runs'
SELECT * FROM country_identity_repair_runs ORDER BY 1 DESC LIMIT 5000;

\echo '=== SR02 P08 COUNTRY IDENTITY REPAIR SNAPSHOT OCCUPANCY ==='
SELECT 'country_identity_repair_base_snapshot' AS relation, COUNT(*) AS rows FROM country_identity_repair_base_snapshot
UNION ALL SELECT 'country_identity_repair_demo_snapshot', COUNT(*) FROM country_identity_repair_demo_snapshot
UNION ALL SELECT 'country_identity_repair_response_invariants', COUNT(*) FROM country_identity_repair_response_invariants;

\echo '=== SR02 P09 NAMED RESPONDENTSDEMO TABLE OCCUPANCY / LOAD EPOCHS ==='
SELECT format(
  'SELECT %L AS table_name, COUNT(*) AS rows, MIN(loaded_at) AS min_loaded_at, MAX(loaded_at) AS max_loaded_at, COUNT(DISTINCT respondent_id) AS distinct_respondents FROM public.%I;',
  c.relname,c.relname)
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r' AND c.relname LIKE 'respondentsDemo%'
ORDER BY c.relname
\gexec

\echo '=== SR02 P10 NAMED RESPONDENTSDEMO SOURCE/WAVE/DATASET OCCUPANCY ==='
SELECT format(
  'SELECT %L AS table_name, source_family, wave, dataset_id, source_file, COUNT(*) AS rows FROM public.%I GROUP BY source_family,wave,dataset_id,source_file ORDER BY source_family,wave,dataset_id,source_file;',
  c.relname,c.relname)
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r' AND c.relname LIKE 'respondentsDemo%'
ORDER BY c.relname
\gexec

\echo '=== SR02 P11 DRIVER AGGREGATE SOURCE/WAVE OCCUPANCY ==='
SELECT source,wave,COUNT(*) AS rows
FROM driver_aggregates
GROUP BY source,wave
ORDER BY source,wave;

\echo '=== SR02 P12 OLD RESPONDENTS/RESPONSES OCCUPANCY ==='
SELECT 'respondents' AS relation, COUNT(*) AS rows FROM respondents
UNION ALL SELECT 'responses', COUNT(*) FROM responses;

\echo '=== SR02 P13 SOURCE-WAVE IDENTITY OCCUPANCY ==='
SELECT raw_db_source,raw_db_wave,canonical_display_source,canonical_display_wave,
       source_family_uid,wave_uid,governance_state,closed_35_member
FROM respondent_source_wave_identity
ORDER BY raw_db_source,raw_db_wave;

\echo '=== SR02 P14 QUESTION MAPPING OCCUPANCY ==='
SELECT source_family_uid,wave_uid,mapping_status,COUNT(*) AS rows
FROM question_structural_mapping
GROUP BY source_family_uid,wave_uid,mapping_status
ORDER BY source_family_uid,wave_uid,mapping_status;

\echo '=== SR02 COMPLETE ==='
ROLLBACK;
SELECT 'PRE553_SR02_CURRENT_DB_PROVENANCE_RECEIPT_COMPLETE' AS completion_token;
