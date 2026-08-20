-- PRE553 PD01-PG01
-- WVS Wave 7 v6.0.0 populated-Postgres physical reality probes
--
-- READ-ONLY. NO DDL. NO DML. NO C11 WRITES.
--
-- This file answers only: what is physically populated in Postgres?
-- It does NOT certify P05 equivalence, choose structural meaning, infer actor state,
-- or authorize source retirement/cutover.
--
-- Recommended execution:
--   psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 \
--     -f PD01_WVS_W7_POPULATED_PROBES.sql \
--     > PD01_WVS_W7_POPULATED_PROBE_RESULTS.txt 2>&1

\pset pager off
\pset footer off
\pset null '[NULL]'
\timing on

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '15min';
SET LOCAL lock_timeout = '5s';

\echo '===== P00 SESSION AND REQUIRED RELATIONS ====='
SELECT
  current_database() AS database_name,
  current_setting('server_version') AS postgres_version,
  current_setting('transaction_read_only') AS transaction_read_only;

SELECT
  to_regclass('public."respondentsDemoWVSW7"') AS w7_demo_table,
  to_regclass('public.survey_microdata_respondents') AS microdata_respondents,
  to_regclass('public.survey_microdata_responses') AS microdata_responses,
  to_regclass('public.survey_weight_fact') AS survey_weight_fact,
  to_regclass('rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry') AS canonical_question_registry,
  to_regclass('rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance') AS mapping_provenance;

\echo '===== P01 WVS W7 DEMO -> MICRODATA RESPONDENT LINKAGE ====='
SELECT
  COUNT(*) AS demo_w7_rows,
  COUNT(s.id) AS linked_microdata_respondents,
  COUNT(*) - COUNT(s.id) AS orphan_demo_ids,
  COUNT(DISTINCT d.respondent_id) AS distinct_demo_respondent_ids
FROM public."respondentsDemoWVSW7" d
LEFT JOIN public.survey_microdata_respondents s
  ON s.id = d.respondent_id;

\echo '===== P02 WVS W7 RELEASE / FILE / COUNTRY / YEAR OCCUPANCY ====='
SELECT
  s.source,
  s.wave,
  s.dataset_id,
  s.source_file,
  s.country_code,
  MIN(s.survey_year) AS min_year,
  MAX(s.survey_year) AS max_year,
  COUNT(*) AS respondents
FROM public.survey_microdata_respondents s
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id = s.id
GROUP BY 1,2,3,4,5
ORDER BY 1,2,3,4,5;

\echo '===== P03 DEMO METADATA VS RESPONDENT METADATA CONSISTENCY ====='
SELECT
  COUNT(*) FILTER (WHERE d.source_family IS DISTINCT FROM s.source) AS source_mismatches,
  COUNT(*) FILTER (WHERE d.wave IS DISTINCT FROM s.wave) AS wave_mismatches,
  COUNT(*) FILTER (WHERE d.dataset_id IS DISTINCT FROM s.dataset_id) AS dataset_id_mismatches,
  COUNT(*) FILTER (WHERE d.source_file IS DISTINCT FROM s.source_file) AS source_file_mismatches,
  COUNT(*) FILTER (WHERE d.country_code IS DISTINCT FROM s.country_code) AS country_code_mismatches,
  COUNT(*) FILTER (WHERE d.survey_year IS DISTINCT FROM s.survey_year) AS survey_year_mismatches
FROM public."respondentsDemoWVSW7" d
JOIN public.survey_microdata_respondents s
  ON s.id = d.respondent_id;

\echo '===== P04 RESPONSE RELEASE / FILE CONSISTENCY ====='
SELECT
  COUNT(*) AS response_rows,
  COUNT(*) FILTER (WHERE r.dataset_id IS NULL) AS response_dataset_id_null,
  COUNT(*) FILTER (WHERE r.source_file IS NULL) AS response_source_file_null,
  COUNT(*) FILTER (WHERE r.dataset_id IS DISTINCT FROM s.dataset_id) AS response_dataset_mismatch,
  COUNT(*) FILTER (WHERE r.source_file IS DISTINCT FROM s.source_file) AS response_source_file_mismatch
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id = r.respondent_id
JOIN public.survey_microdata_respondents s
  ON s.id = r.respondent_id;

\echo '===== P05 RESPONSE INCIDENCE DENSITY BY RESPONDENT ====='
WITH per_respondent AS (
  SELECT
    r.respondent_id,
    COUNT(*) AS response_rows,
    COUNT(DISTINCT r.var_code) AS distinct_var_codes,
    COUNT(*) FILTER (WHERE r.value_raw IS NULL AND r.value_text IS NULL) AS null_value_rows
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id = r.respondent_id
  GROUP BY r.respondent_id
)
SELECT
  COUNT(*) AS respondents_with_response_rows,
  MIN(response_rows) AS min_response_rows,
  ROUND(AVG(response_rows)::numeric, 3) AS avg_response_rows,
  MAX(response_rows) AS max_response_rows,
  MIN(distinct_var_codes) AS min_distinct_vars,
  ROUND(AVG(distinct_var_codes)::numeric, 3) AS avg_distinct_vars,
  MAX(distinct_var_codes) AS max_distinct_vars,
  SUM(null_value_rows) AS null_value_rows
FROM per_respondent;

\echo '===== P06 PER-VARIABLE COVERAGE / NO-ROW VS NULL VS SOURCE-CODE SURFACE ====='
WITH total AS (
  SELECT COUNT(*)::bigint AS n
  FROM public."respondentsDemoWVSW7"
),
v AS (
  SELECT
    r.var_code,
    COUNT(*) AS rows,
    COUNT(DISTINCT r.respondent_id) AS respondents_with_row,
    COUNT(*) FILTER (WHERE r.value_raw IS NULL AND r.value_text IS NULL) AS null_value_rows,
    COUNT(*) FILTER (WHERE r.value_raw IN (-1,-2,-3,-4,-5)) AS source_negative_code_rows
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id = r.respondent_id
  GROUP BY r.var_code
)
SELECT
  v.var_code,
  v.rows,
  v.respondents_with_row,
  total.n - v.respondents_with_row AS respondents_without_row,
  v.null_value_rows,
  v.source_negative_code_rows
FROM v CROSS JOIN total
ORDER BY v.var_code;

\echo '===== P07 SOURCE-NATIVE IDENTITY / DESIGN / WEIGHT VARIABLES AS RAW INCIDENCE ====='
SELECT
  r.var_code,
  COUNT(*) AS rows,
  COUNT(r.value_raw) AS numeric_rows,
  COUNT(r.value_text) AS text_rows,
  COUNT(DISTINCT r.respondent_id) AS respondents,
  COUNT(DISTINCT COALESCE(r.value_text, r.value_raw::text)) AS distinct_values
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id = r.respondent_id
WHERE r.var_code IN ('D_INTERVIEW','A_WAVE','B_COUNTRY','I_PSU','W_WEIGHT','S018')
GROUP BY r.var_code
ORDER BY r.var_code;

\echo '===== P08 D_INTERVIEW SOURCE-NATIVE IDENTITY INJECTIVITY / COLLISION CHECK ====='
WITH ids AS (
  SELECT
    r.respondent_id,
    d.country_code,
    COALESCE(r.value_text, r.value_raw::text) AS source_interview_id
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id = r.respondent_id
  WHERE r.var_code = 'D_INTERVIEW'
)
SELECT
  COUNT(*) AS rows,
  COUNT(*) FILTER (WHERE source_interview_id IS NULL) AS null_source_ids,
  COUNT(DISTINCT respondent_id) AS rawlsing_respondents,
  COUNT(DISTINCT (country_code, source_interview_id)) AS distinct_country_source_ids,
  COUNT(*) - COUNT(DISTINCT (country_code, source_interview_id)) AS duplicate_country_source_id_rows
FROM ids;

SELECT
  country_code,
  source_interview_id,
  COUNT(*) AS rows,
  COUNT(DISTINCT respondent_id) AS rawlsing_respondents
FROM (
  SELECT
    r.respondent_id,
    d.country_code,
    COALESCE(r.value_text, r.value_raw::text) AS source_interview_id
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id = r.respondent_id
  WHERE r.var_code = 'D_INTERVIEW'
) x
WHERE source_interview_id IS NOT NULL
GROUP BY 1,2
HAVING COUNT(DISTINCT respondent_id) <> 1
ORDER BY rows DESC, country_code, source_interview_id;

\echo '===== P09 TYPED ABSENCE OCCUPANCY (-1..-5 REMAIN DISTINCT PHYSICAL VALUES) ====='
SELECT
  r.var_code,
  COUNT(*) FILTER (WHERE r.value_raw = -1) AS code_minus_1,
  COUNT(*) FILTER (WHERE r.value_raw = -2) AS code_minus_2,
  COUNT(*) FILTER (WHERE r.value_raw = -3) AS code_minus_3,
  COUNT(*) FILTER (WHERE r.value_raw = -4) AS code_minus_4,
  COUNT(*) FILTER (WHERE r.value_raw = -5) AS code_minus_5,
  COUNT(*) FILTER (WHERE r.value_raw IS NULL AND r.value_text IS NULL) AS null_rows,
  COUNT(*) AS total_rows
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id = r.respondent_id
GROUP BY r.var_code
ORDER BY r.var_code;

\echo '===== P10 Q154/Q155 EXACT RANK-SLOT JOINT ====='
WITH x AS (
  SELECT
    r.respondent_id,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q154') AS q154,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q155') AS q155
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q154','Q155')
  GROUP BY r.respondent_id
)
SELECT q154, q155, COUNT(*) AS n
FROM x
GROUP BY q154, q155
ORDER BY q154, q155;

\echo '===== P11 Q152/Q153 EXACT RANK-SLOT JOINT ====='
WITH x AS (
  SELECT
    r.respondent_id,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q152') AS q152,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q153') AS q153
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q152','Q153')
  GROUP BY r.respondent_id
)
SELECT q152, q153, COUNT(*) AS n
FROM x
GROUP BY q152, q153
ORDER BY q152, q153;

\echo '===== P12 Q156/Q157 EXACT RANK-SLOT JOINT ====='
WITH x AS (
  SELECT
    r.respondent_id,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q156') AS q156,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q157') AS q157
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q156','Q157')
  GROUP BY r.respondent_id
)
SELECT q156, q157, COUNT(*) AS n
FROM x
GROUP BY q156, q157
ORDER BY q156, q157;

\echo '===== P13 RESPONSE TABLE EVENT/MULTIPLICITY REPRESENTATION CONSTRAINT ====='
SELECT
  conname,
  pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'public.survey_microdata_responses'::regclass
  AND contype IN ('p','u','f')
ORDER BY contype, conname;

\echo '===== P14 Q223 COUNTRY-SPECIFIC CODE PRESERVATION ====='
SELECT
  d.country_code,
  r.value_raw,
  r.value_text,
  COUNT(*) AS n
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id=r.respondent_id
WHERE r.var_code='Q223'
GROUP BY d.country_code, r.value_raw, r.value_text
ORDER BY d.country_code, r.value_raw, r.value_text;

\echo '===== P15 WEIGHT-NAME SEPARATION / SOURCE-VAR PROVENANCE ====='
SELECT
  w.weight_name,
  w.weight_type,
  w.source_var,
  w.source,
  w.wave,
  w.is_primary,
  COUNT(*) AS rows,
  COUNT(w.weight_value) AS valued_rows,
  COUNT(*) FILTER (WHERE w.weight_value = 1) AS exactly_one_rows,
  COUNT(*) FILTER (WHERE w.weight_value IS NULL) AS null_rows,
  MIN(w.weight_value) AS min_weight,
  MAX(w.weight_value) AS max_weight,
  AVG(w.weight_value) AS avg_weight
FROM public.survey_weight_fact w
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id=w.respondent_id
GROUP BY 1,2,3,4,5,6
ORDER BY 1,2,3,4,5,6;

\echo '===== P16 W_WEIGHT / S018 RAW RESPONSE VS WEIGHT-FACT COVERAGE ====='
SELECT
  r.var_code,
  COUNT(*) AS response_rows,
  COUNT(DISTINCT r.respondent_id) AS response_respondents,
  COUNT(*) FILTER (WHERE r.value_raw IS NULL) AS raw_null_rows,
  MIN(r.value_raw) AS min_raw,
  MAX(r.value_raw) AS max_raw
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id=r.respondent_id
WHERE r.var_code IN ('W_WEIGHT','S018')
GROUP BY r.var_code
ORDER BY r.var_code;

\echo '===== P17 I_PSU OCCUPANCY / -4,-5 DESIGN ABSENCE ====='
SELECT
  r.value_raw,
  r.value_text,
  COUNT(*) AS n
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id=r.respondent_id
WHERE r.var_code='I_PSU'
GROUP BY r.value_raw, r.value_text
ORDER BY r.value_raw, r.value_text;

\echo '===== P18 SAME-RESPONDENT 5-WAY RECONSTRUCTIBILITY: Q177-Q181 ====='
WITH w7 AS (
  SELECT r.respondent_id, r.var_code, r.value_raw
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q177','Q178','Q179','Q180','Q181')
), p AS (
  SELECT
    respondent_id,
    MAX(value_raw) FILTER (WHERE var_code='Q177') AS q177,
    MAX(value_raw) FILTER (WHERE var_code='Q178') AS q178,
    MAX(value_raw) FILTER (WHERE var_code='Q179') AS q179,
    MAX(value_raw) FILTER (WHERE var_code='Q180') AS q180,
    MAX(value_raw) FILTER (WHERE var_code='Q181') AS q181
  FROM w7
  GROUP BY respondent_id
)
SELECT q177,q178,q179,q180,q181,COUNT(*) AS n
FROM p
GROUP BY 1,2,3,4,5
ORDER BY n DESC,1,2,3,4,5
LIMIT 500;

\echo '===== P19 2-WAY / 3-WAY / 5-WAY NONNULL SUPPORT COUNTS ====='
WITH p AS (
  SELECT
    r.respondent_id,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q177') AS q177,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q178') AS q178,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q179') AS q179,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q180') AS q180,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q181') AS q181
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q177','Q178','Q179','Q180','Q181')
  GROUP BY r.respondent_id
)
SELECT
  COUNT(*) AS any_battery_respondents,
  COUNT(*) FILTER (WHERE q177 IS NOT NULL AND q178 IS NOT NULL) AS support_2way,
  COUNT(*) FILTER (WHERE q177 IS NOT NULL AND q178 IS NOT NULL AND q179 IS NOT NULL) AS support_3way,
  COUNT(*) FILTER (
    WHERE q177 IS NOT NULL AND q178 IS NOT NULL AND q179 IS NOT NULL
      AND q180 IS NOT NULL AND q181 IS NOT NULL
  ) AS support_5way
FROM p;

\echo '===== P20 CONDITIONED RAW VS NAMED-WEIGHT PHYSICAL JOIN (NO STRUCTURAL INTERPRETATION) ====='
WITH q AS (
  SELECT
    r.respondent_id,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q177') AS q177,
    MAX(r.value_raw) FILTER (WHERE r.var_code='Q178') AS q178
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d
    ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q177','Q178')
  GROUP BY r.respondent_id
),
w AS (
  SELECT respondent_id, weight_name, weight_value
  FROM public.survey_weight_fact
  WHERE weight_name IN ('W_WEIGHT','S018')
)
SELECT
  d.country_code,
  d.sex,
  w.weight_name,
  q.q177,
  q.q178,
  COUNT(*) AS raw_n,
  SUM(w.weight_value) AS weight_sum,
  COUNT(*) FILTER (WHERE w.weight_value IS NULL) AS null_weight_rows
FROM q
JOIN public."respondentsDemoWVSW7" d
  ON d.respondent_id=q.respondent_id
LEFT JOIN w
  ON w.respondent_id=q.respondent_id
WHERE q.q177 IS NOT NULL OR q.q178 IS NOT NULL
GROUP BY 1,2,3,4,5
ORDER BY 1,2,3,4,5
LIMIT 1000;

\echo '===== P21 AUTHORITY-RECONCILE SCHEMA PRESENCE ====='
SELECT
  (to_regclass('rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry') IS NOT NULL)::int AS auth_registry_present,
  (to_regclass('rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance') IS NOT NULL)::int AS mapping_provenance_present
\gset

\if :mapping_provenance_present
  \echo '===== P22 RAW -> CANONICAL MAPPING / PROVENANCE OCCUPANCY ====='
  SELECT
    raw_source,
    raw_wave,
    canonical_source,
    canonical_wave,
    identity_match_type,
    COUNT(*) AS mappings,
    COUNT(*) FILTER (WHERE authority_source_path IS NULL) AS missing_authority_path,
    COUNT(*) FILTER (WHERE authority_row_identity IS NULL) AS missing_authority_row
  FROM rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance
  WHERE lower(raw_source) LIKE '%wvs%'
     OR lower(canonical_source) LIKE '%wvs%'
     OR upper(raw_wave) = 'W7'
     OR upper(canonical_wave) = 'W7'
  GROUP BY 1,2,3,4,5
  ORDER BY 1,2,3,4,5;

  SELECT
    raw_source,
    raw_wave,
    raw_var_code,
    canonical_source,
    canonical_wave,
    canonical_var_code,
    identity_match_type,
    authority_source_path,
    authority_row_identity,
    migration_run_id
  FROM rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance
  WHERE (lower(raw_source) LIKE '%wvs%' OR lower(canonical_source) LIKE '%wvs%'
         OR upper(raw_wave) = 'W7' OR upper(canonical_wave) = 'W7')
    AND (
      authority_source_path IS NULL
      OR authority_row_identity IS NULL
      OR raw_var_code IS NULL
      OR canonical_var_code IS NULL
    )
  ORDER BY raw_source, raw_wave, raw_var_code;
\else
  \echo 'P22 SKIPPED: question_structural_mapping_provenance relation absent'
\endif

\if :auth_registry_present
  \echo '===== P23 CANONICAL QUESTION / TOPOLOGY / AUTHORITY OCCUPANCY ====='
  SELECT
    canonical_source,
    canonical_wave,
    response_topology,
    directional_certification_status,
    authority_semantic_role,
    COUNT(*) AS questions,
    COUNT(*) FILTER (WHERE authority_source_path IS NULL) AS missing_authority_path,
    COUNT(*) FILTER (WHERE authority_row_identity IS NULL) AS missing_authority_row
  FROM rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry
  WHERE lower(canonical_source) LIKE '%wvs%'
     OR upper(canonical_wave) = 'W7'
  GROUP BY 1,2,3,4,5
  ORDER BY 1,2,3,4,5;

  SELECT
    canonical_source,
    canonical_wave,
    canonical_var_code,
    question_id,
    response_topology,
    disposition,
    authority_semantic_role,
    authority_source_path,
    authority_row_identity
  FROM rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry
  WHERE (lower(canonical_source) LIKE '%wvs%' OR upper(canonical_wave) = 'W7')
    AND (
      authority_source_path IS NULL
      OR authority_row_identity IS NULL
      OR response_topology IS NULL
      OR canonical_var_code IS NULL
    )
  ORDER BY canonical_source, canonical_wave, canonical_var_code;
\else
  \echo 'P23 SKIPPED: canonical_question_registry relation absent'
\endif

\echo '===== P24 PHYSICAL SOURCE CHECKSUM / REPLAY GAP ====='
SELECT
  'survey_microdata_respondents contains dataset_id/source_file but no immutable source checksum column in the supplied public schema; pair this receipt with an exact retained raw-source manifest/checksum before M17/M18 or P05 certification.' AS finding;

\echo '===== P25 FINAL READ-ONLY ASSERTION ====='
SELECT current_setting('transaction_read_only') AS transaction_read_only_before_rollback;

ROLLBACK;

\echo '===== PRE553 PD01-PG01 COMPLETE ====='
\echo 'Return the entire stdout/stderr receipt unchanged to HQ/browser adjudication.'
