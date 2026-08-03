#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

import duckdb

SQL = """
CREATE OR REPLACE VIEW survey_microdata_respondents AS
WITH piv AS (
  SELECT
    respondent_uid,
    MAX(CASE WHEN position_dimension IN ('sex','gender','sex_gender') THEN canonical_value END) AS sex,
    MAX(CASE WHEN position_dimension IN ('age','age_years') THEN canonical_value END) AS age,
    MAX(CASE WHEN position_dimension IN ('education','education_level') THEN canonical_value END) AS education_level,
    MAX(CASE WHEN position_dimension IN ('income','income_level') THEN canonical_value END) AS income_level,
    MAX(CASE WHEN position_dimension IN ('religion','religion_label') THEN canonical_value END) AS religion_label,
    MAX(CASE WHEN position_dimension IN ('urban_rural','urbanicity') THEN canonical_value END) AS urban_rural
  FROM respondent_position_fact
  GROUP BY respondent_uid
)
SELECT
  r.respondent_uid AS id,
  r.native_respondent_id,
  r.dataset_id,
  r.source_family AS source,
  r.wave,
  r.canonical_wave,
  r.country,
  r.country_code,
  r.survey_year,
  p.sex,
  TRY_CAST(p.age AS DOUBLE) AS age,
  TRY_CAST(p.education_level AS DOUBLE) AS education_level,
  TRY_CAST(p.income_level AS DOUBLE) AS income_level,
  p.religion_label,
  p.urban_rural
FROM respondent_fact r
LEFT JOIN piv p ON p.respondent_uid = r.respondent_uid;

CREATE OR REPLACE VIEW survey_microdata_responses AS
SELECT
  respondent_uid AS respondent_id,
  dataset_id,
  source_family AS source,
  wave,
  raw_variable AS var_code,
  raw_value AS value_raw,
  normalized_value,
  value_label,
  missing_flag,
  final_driver_id,
  question_id,
  question_block_id,
  structural_domain_id,
  driver_facet_id,
  relation_axis_id,
  target_entity_id,
  question_type,
  source_match_type,
  load_batch_id
FROM response_fact;
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--duckdb", required=True)
    args = ap.parse_args()
    con = duckdb.connect(args.duckdb)
    for stmt in SQL.split(";"):
        if stmt.strip():
            con.execute(stmt)
    print(json.dumps({"status": "green", "views": ["survey_microdata_respondents", "survey_microdata_responses"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
