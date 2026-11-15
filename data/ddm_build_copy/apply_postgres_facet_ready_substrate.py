#!/usr/bin/env python3
"""Apply the Postgres facet-ready substrate for the broader builders.

This script does four things in the live Postgres database:

1. Create and populate question_structural_mapping from the immutable August 14
   R1 question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv authority.
2. Create respondent_position_fact as a view over the respondentsDemo* tables.
3. Create and populate survey_weight_fact from the existing respondent-level
   survey_weight column on the respondentsDemo* tables.
4. Create v_ddm_response_long_facet_ready as the builder-facing join layer.

The script is intentionally idempotent:
- question_structural_mapping is truncated and reloaded each run.
- survey_weight_fact can be replaced for selected families.
- the views are re-created each run.

The weight population is conservative:
- it reuses the curated respondent-level weight already present in the demo layer
- it does not try to infer weights from arbitrary "weight" text in the codebooks
- it marks a single primary weight per respondent so the facet-ready view can
  join a single scalar weight safely.
"""

from __future__ import annotations

import argparse
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

from data.ddm_build_copy.ddm_v550_question_relation_authority import (
    LEGACY_RESIDUAL_ROW_COUNT,
    R1_TARGET_ROW_COUNT,
    derive_legacy_latinobarometro_1995_residual,
)


ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_MASTER = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
QUESTION_MAPPING_AUTHORITY = (
    ROOT / "data" / "ddm_build_copy" / "authority" / "full_question_relation_authority"
    / "R1_20260814" / "question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv"
)
OUT_REPORT = ROOT / "data" / "ddm_build_copy" / "reports" / "apply_postgres_facet_ready_substrate_report.json"


QUESTION_MAPPING_SQL = """
CREATE TABLE IF NOT EXISTS question_structural_mapping (
    source TEXT NOT NULL,
    wave TEXT NOT NULL DEFAULT '',
    question_id TEXT NOT NULL,
    var_code TEXT NOT NULL,
    display_text TEXT,
    legacy_final_driver_id TEXT,
    final_driver_label TEXT,
    final_driver_scope TEXT,
    final_driver_origin TEXT,
    driver_id TEXT,
    driver_facet_id TEXT,
    question_block_id TEXT,
    structural_domain_id TEXT,
    relation_axis_id TEXT,
    target_entity_id TEXT,
    mapping_status TEXT,
    evidence_kind TEXT,
    strata_relevance TEXT,
    channel_affordances TEXT,
    forbidden_inference TEXT,
    does_not_measure TEXT,
    review_notes TEXT,
    canonical_wave TEXT NOT NULL DEFAULT '',
    country_code_scope TEXT NOT NULL DEFAULT '',
    authority_status TEXT NOT NULL DEFAULT '',
    authority_rule_id TEXT NOT NULL DEFAULT '',
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source, wave, var_code)
);

CREATE INDEX IF NOT EXISTS idx_question_structural_mapping_source_wave_var
    ON question_structural_mapping(source, wave, var_code);

CREATE INDEX IF NOT EXISTS idx_question_structural_mapping_block_facet
    ON question_structural_mapping(question_block_id, driver_facet_id);
"""


SURVEY_WEIGHT_FACT_SQL = """
CREATE TABLE IF NOT EXISTS survey_weight_fact (
    respondent_id INT NOT NULL REFERENCES survey_microdata_respondents(id) ON DELETE CASCADE,
    weight_name TEXT NOT NULL,
    weight_value DOUBLE PRECISION,
    weight_type TEXT,
    source_var TEXT,
    source TEXT,
    wave TEXT,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (respondent_id, weight_name)
);

CREATE INDEX IF NOT EXISTS idx_survey_weight_fact_respondent
    ON survey_weight_fact(respondent_id);

CREATE INDEX IF NOT EXISTS idx_survey_weight_fact_source_wave
    ON survey_weight_fact(source, wave);

CREATE INDEX IF NOT EXISTS idx_survey_weight_fact_name
    ON survey_weight_fact(weight_name);
"""


RESPONDENT_POSITION_FACT_SQL = """
CREATE OR REPLACE VIEW respondent_position_fact AS
WITH tables AS (
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name LIKE 'respondentsDemo%'
      AND table_name NOT ILIKE '%unknown%'
    ORDER BY table_name
)
SELECT * FROM (
    SELECT
        respondent_id,
        source_family,
        wave,
        country_code,
        survey_year,
        sex,
        age,
        education_level,
        income_level,
        income_source_note,
        urban_rural,
        religion_label,
        marital,
        employment,
        class_level,
        household_size,
        language,
        region,
        ethnicity,
        position_source_table,
        position_completeness_score
    FROM (
        SELECT
            respondent_id,
            source_family,
            wave,
            country_code,
            survey_year,
            sex,
            age,
            education_level,
            income_level,
            income_source_note,
            urban_rural,
            religion_label,
            marital,
            employment,
            class_level,
            household_size,
            language,
            region,
            ethnicity,
            position_source_table,
            position_completeness_score
        FROM (
            SELECT
                respondent_id,
                source_family,
                wave,
                country_code,
                survey_year,
                sex,
                age,
                education_level,
                income_level,
                income_source_note,
                urban_rural,
                religion_label,
                marital,
                employment,
                class_level,
                household_size,
                language,
                region,
                ethnicity,
                position_source_table,
                position_completeness_score
            FROM respondent_position_fact__staging
        ) s
    ) q
) final;
"""


FACET_READY_VIEW_SQL = """
CREATE OR REPLACE VIEW v_ddm_response_long_facet_ready AS
WITH weight_pick AS (
    SELECT DISTINCT ON (respondent_id)
        respondent_id,
        weight_name,
        weight_value
    FROM survey_weight_fact
    WHERE is_primary
    ORDER BY respondent_id, weight_name
)
SELECT
    r.id AS respondent_id,
    r.source,
    r.wave,
    COALESCE(r.wave, '') AS canonical_wave,
    r.country_code,
    r.survey_year,

    resp.var_code,
    resp.value_raw,
    resp.value_text,

    wp.weight_value,
    wp.weight_name,
    CASE
        WHEN wp.weight_value IS NOT NULL THEN 'weighted_available'
        ELSE 'unweighted_no_weight_detected'
    END AS weight_status,

    pos.sex,
    pos.age,
    CASE
        WHEN NULLIF(pos.age, '')::DOUBLE PRECISION IS NOT NULL
         AND NULLIF(pos.age, '')::DOUBLE PRECISION < 30 THEN '18-29'
        WHEN NULLIF(pos.age, '')::DOUBLE PRECISION IS NOT NULL
         AND NULLIF(pos.age, '')::DOUBLE PRECISION < 45 THEN '30-44'
        WHEN NULLIF(pos.age, '')::DOUBLE PRECISION IS NOT NULL
         AND NULLIF(pos.age, '')::DOUBLE PRECISION < 60 THEN '45-59'
        WHEN NULLIF(pos.age, '')::DOUBLE PRECISION IS NOT NULL THEN '60+'
        ELSE ''
    END AS age_group,
    pos.education_level,
    pos.income_level,
    pos.religion_label,
    pos.urban_rural,
    pos.region,
    pos.ethnicity,
    pos.language,
    pos.employment,
    pos.marital,
    pos.household_size,
    pos.position_source_table,
    pos.position_completeness_score,

    COALESCE(qsm.question_id, resp.var_code) AS question_id,
    qsm.question_block_id,
    qsm.structural_domain_id,
    qsm.driver_id,
    qsm.driver_facet_id,
    qsm.relation_axis_id,
    qsm.target_entity_id,
    qsm.mapping_status,
    qsm.legacy_final_driver_id,
    CASE
        WHEN COALESCE(qsm.legacy_final_driver_id, '') <> ''
         AND COALESCE(qsm.driver_facet_id, '') = ''
        THEN TRUE
        ELSE FALSE
    END AS legacy_driver_leak_flag
FROM survey_microdata_responses resp
JOIN survey_microdata_respondents r
    ON r.id = resp.respondent_id
LEFT JOIN respondent_position_fact pos
    ON pos.respondent_id = r.id
LEFT JOIN weight_pick wp
    ON wp.respondent_id = r.id
LEFT JOIN LATERAL (
    SELECT
        q.question_id,
        q.question_block_id,
        q.structural_domain_id,
        q.driver_id,
        q.driver_facet_id,
        q.relation_axis_id,
        q.target_entity_id,
        COALESCE(q.mapping_status, 'accepted_existing_mapping') AS mapping_status,
        q.legacy_final_driver_id
    FROM question_structural_mapping q
    WHERE q.source = r.source
      AND UPPER(q.var_code) = UPPER(resp.var_code)
      AND (q.wave = COALESCE(r.wave, '') OR q.wave = '' OR q.wave IS NULL)
    ORDER BY CASE WHEN q.wave = COALESCE(r.wave, '') THEN 0 ELSE 1 END, q.loaded_at DESC
    LIMIT 1
) qsm ON TRUE;
"""


WEIGHT_ALLOWLIST: dict[str, dict[str, list[str]]] = {
    "GSS": {
        "1972": ["wtssall", "wtssps"],
        "1973": ["wtssall", "wtssps"],
        "1984": ["formwt", "wtssall", "wtssps"],
        "1993": ["wtssall", "wtssps"],
        "2002": ["wtssall", "wtssps"],
        "2010": ["wtss", "wtssall", "wtssnr", "wtssnrps", "wtssps"],
        "2016": ["rweight", "wtss", "wtssall", "wtssnr", "wtssnrps", "wtssps"],
        "2024": ["wtssnrps", "wtssnrps_next", "wtssps", "wtssps_next", "wtssnrps_as", "wtssps_as"],
    },
    "LiTS": {
        "2006": ["weight_0", "weight_1", "weight_2"],
        "II": ["weight", "XCweight"],
        "III": ["weight_population", "weight_sample", "weight_one"],
        "IV": ["weight", "weight_pop", "weight_trt", "weight_pop_trt"],
    },
}


PRIMARY_WEIGHT_ORDER: dict[str, dict[str, list[str]]] = {
    "GSS": {
        "1972": ["wtssps", "wtssall"],
        "1973": ["wtssps", "wtssall"],
        "1984": ["wtssps", "wtssall", "formwt"],
        "1993": ["wtssps", "wtssall"],
        "2002": ["wtssps", "wtssall"],
        "2010": ["wtssnrps", "wtssps", "wtssnr", "wtss", "wtssall"],
        "2016": ["wtssnrps", "wtssps", "wtssnr", "wtss", "wtssall", "rweight"],
        "2024": ["wtssnrps", "wtssnrps_as", "wtssnrps_next", "wtssps", "wtssps_as", "wtssps_next"],
    },
    "LiTS": {
        "2006": ["weight_0", "weight_1", "weight_2"],
        "II": ["weight", "XCweight"],
        "III": ["weight_population", "weight_sample", "weight_one"],
        "IV": ["weight_pop", "weight", "weight_pop_trt", "weight_trt"],
    },
}


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing; the live Postgres database is not reachable.")
    return psycopg2.connect(db_url)


def load_questions_master() -> pd.DataFrame:
    if not QUESTIONS_MASTER.exists():
        raise FileNotFoundError(QUESTIONS_MASTER)
    df = pd.read_csv(QUESTIONS_MASTER, low_memory=False)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    return df


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def create_question_mapping_rows(df: pd.DataFrame) -> list[tuple[Any, ...]]:
    rows: dict[tuple[str, str, str], tuple[Any, ...]] = {}
    for r in df.itertuples(index=False):
        source = clean(getattr(r, "source", ""))
        wave = clean(getattr(r, "wave", ""))
        var_code = clean(getattr(r, "var_name", ""))
        if not source or not var_code:
            continue
        question_id = clean(getattr(r, "item_id", "")) or f"{source}:{wave}:{var_code}"
        row = (
            source,
            wave,
            question_id,
            var_code,
            clean(getattr(r, "display_text", "")),
            clean(getattr(r, "final_driver_id", "")),
            clean(getattr(r, "final_driver_label", "")),
            clean(getattr(r, "final_driver_scope", "")),
            clean(getattr(r, "final_driver_origin", "")),
            clean(getattr(r, "driver_id", "")) or clean(getattr(r, "final_driver_id", "")),
            clean(getattr(r, "driver_facet_id", "")),
            clean(getattr(r, "question_block_id", "")),
            clean(getattr(r, "structural_domain_id", "")),
            clean(getattr(r, "relation_axis_id", "")),
            clean(getattr(r, "target_entity_id", "")),
            clean(getattr(r, "mapping_status", "")) or "accepted_existing_mapping",
            clean(getattr(r, "evidence_kind", "")),
            clean(getattr(r, "strata_relevance", "")),
            clean(getattr(r, "channel_affordances", "")),
            clean(getattr(r, "forbidden_inference", "")),
            clean(getattr(r, "does_not_measure", "")),
            clean(getattr(r, "review_notes", "")),
        )
        key = (source, wave, var_code)
        if key not in rows:
            rows[key] = row
            continue

        existing = rows[key]
        # Prefer the row with the richer mapping signal.
        existing_score = sum(1 for v in existing if isinstance(v, str) and v)
        new_score = sum(1 for v in row if isinstance(v, str) and v)
        if new_score >= existing_score:
            rows[key] = row
    return list(rows.values())


def ensure_question_mapping(cur) -> None:
    cur.execute(QUESTION_MAPPING_SQL)
    cur.execute("ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS canonical_wave TEXT NOT NULL DEFAULT ''")
    cur.execute("ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS country_code_scope TEXT NOT NULL DEFAULT ''")
    cur.execute("ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS authority_status TEXT NOT NULL DEFAULT ''")
    cur.execute("ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS authority_rule_id TEXT NOT NULL DEFAULT ''")


def load_question_mapping_authority() -> pd.DataFrame:
    if not QUESTION_MAPPING_AUTHORITY.exists():
        raise FileNotFoundError(QUESTION_MAPPING_AUTHORITY)
    frame = pd.read_csv(QUESTION_MAPPING_AUTHORITY, dtype=str, keep_default_na=False)
    required = {
        "source", "wave", "question_id", "var_code", "display_text", "legacy_final_driver_id",
        "final_driver_label", "final_driver_scope", "final_driver_origin", "driver_id",
        "driver_facet_id", "question_block_id", "structural_domain_id", "relation_axis_id",
        "target_entity_id", "mapping_status", "evidence_kind", "strata_relevance", "channel_affordances",
        "forbidden_inference", "does_not_measure", "review_notes", "canonical_wave",
        "country_code_scope", "authority_status", "authority_rule_id",
    }
    missing = required - set(frame.columns)
    if missing:
        raise RuntimeError(f"R1 question mapping authority missing columns: {sorted(missing)}")
    if len(frame) != R1_TARGET_ROW_COUNT:
        raise RuntimeError(f"R1 question mapping authority row count changed: {len(frame)}")

    # The frozen R1 surface remains primary.  Only the exact 20-row legacy
    # Latinobarómetro-1995 residue from the hash-pinned 700-row calibration
    # registry is admitted to the runtime union; the other 680 rows remain
    # calibration-only.
    calibration_residual = derive_legacy_latinobarometro_1995_residual(frame)
    residual = pd.DataFrame(
        {
            "source": calibration_residual["source_family"],
            "wave": calibration_residual["canonical_wave"],
            "question_id": calibration_residual["question_id"],
            "var_code": calibration_residual["var_code"],
            "display_text": calibration_residual["question_text"],
            "legacy_final_driver_id": "",
            "final_driver_label": "",
            "final_driver_scope": "",
            "final_driver_origin": "legacy_calibration_residual",
            "driver_id": calibration_residual["driver_id"],
            "driver_facet_id": calibration_residual["driver_facet_id"],
            "question_block_id": calibration_residual["question_block_id"],
            "structural_domain_id": calibration_residual["structural_domain_id"],
            "relation_axis_id": calibration_residual["relation_axis_id"],
            "target_entity_id": calibration_residual["target_entity_id"],
            "mapping_status": calibration_residual["relation_use_status"],
            "evidence_kind": calibration_residual["evidence_disposition"],
            "strata_relevance": "",
            "channel_affordances": "",
            "forbidden_inference": "",
            "does_not_measure": "",
            "review_notes": calibration_residual["review_notes"],
            "canonical_wave": calibration_residual["canonical_wave"],
            "country_code_scope": calibration_residual["country_code_scope"],
            "authority_status": calibration_residual["authority_status"],
            "authority_rule_id": calibration_residual["authority_rule_id"],
        }
    )
    if len(residual) != LEGACY_RESIDUAL_ROW_COUNT:
        raise RuntimeError(f"legacy residual row count changed: {len(residual)}")
    return pd.concat([frame, residual], ignore_index=True)


def load_question_mapping(conn) -> int:
    df = load_question_mapping_authority()
    rows = [tuple(clean(getattr(r, column, "")) for column in (
        "source", "wave", "question_id", "var_code", "display_text", "legacy_final_driver_id",
        "final_driver_label", "final_driver_scope", "final_driver_origin", "driver_id", "driver_facet_id",
        "question_block_id", "structural_domain_id", "relation_axis_id", "target_entity_id", "mapping_status",
        "evidence_kind", "strata_relevance", "channel_affordances", "forbidden_inference", "does_not_measure",
        "review_notes", "canonical_wave", "country_code_scope", "authority_status", "authority_rule_id"
    )) for r in df.itertuples(index=False)]
    cur = conn.cursor()
    ensure_question_mapping(cur)
    cur.execute("TRUNCATE question_structural_mapping")
    execute_values(
        cur,
        """
        INSERT INTO question_structural_mapping (
            source, wave, question_id, var_code, display_text, legacy_final_driver_id,
            final_driver_label, final_driver_scope, final_driver_origin, driver_id,
            driver_facet_id, question_block_id, structural_domain_id, relation_axis_id,
            target_entity_id, mapping_status, evidence_kind, strata_relevance,
            channel_affordances, forbidden_inference, does_not_measure, review_notes,
            canonical_wave, country_code_scope, authority_status, authority_rule_id
        ) VALUES %s
        ON CONFLICT (source, wave, var_code)
        DO UPDATE SET
            question_id = EXCLUDED.question_id,
            display_text = EXCLUDED.display_text,
            legacy_final_driver_id = EXCLUDED.legacy_final_driver_id,
            final_driver_label = EXCLUDED.final_driver_label,
            final_driver_scope = EXCLUDED.final_driver_scope,
            final_driver_origin = EXCLUDED.final_driver_origin,
            driver_id = EXCLUDED.driver_id,
            driver_facet_id = EXCLUDED.driver_facet_id,
            question_block_id = EXCLUDED.question_block_id,
            structural_domain_id = EXCLUDED.structural_domain_id,
            relation_axis_id = EXCLUDED.relation_axis_id,
            target_entity_id = EXCLUDED.target_entity_id,
            mapping_status = EXCLUDED.mapping_status,
            evidence_kind = EXCLUDED.evidence_kind,
            strata_relevance = EXCLUDED.strata_relevance,
            channel_affordances = EXCLUDED.channel_affordances,
            forbidden_inference = EXCLUDED.forbidden_inference,
            does_not_measure = EXCLUDED.does_not_measure,
            review_notes = EXCLUDED.review_notes,
            canonical_wave = EXCLUDED.canonical_wave,
            country_code_scope = EXCLUDED.country_code_scope,
            authority_status = EXCLUDED.authority_status,
            authority_rule_id = EXCLUDED.authority_rule_id,
            loaded_at = NOW()
        """,
        rows,
        page_size=1000,
    )
    conn.commit()
    cur.close()
    return len(rows)


def ensure_weight_table(cur) -> None:
    cur.execute(SURVEY_WEIGHT_FACT_SQL)


def determine_weight_type(weight_name: str) -> str:
    name = weight_name.lower()
    if "pop_trt" in name or "population" in name:
        return "population_weight"
    if "sample" in name:
        return "sample_weight"
    if "nr" in name:
        return "nonresponse_adjusted_weight"
    if "ps" in name:
        return "poststratification_weight"
    if "cross" in name or "within" in name:
        return "design_component_weight"
    if name in {"wtss", "wtssall", "weight", "weight_0", "weight_1", "weight_2"}:
        return "primary_weight"
    return "design_weight"


def primary_weight_name(family: str, wave: str, weight_names: Iterable[str]) -> str | None:
    allowed = [w for w in weight_names if w]
    if not allowed:
        return None
    priority = [w.lower() for w in PRIMARY_WEIGHT_ORDER.get(family, {}).get(wave, [])]
    for preferred in priority:
        for candidate in allowed:
            if candidate.lower() == preferred:
                return candidate
    return sorted(allowed, key=lambda v: (v.lower(), v))[0]


def fetch_weight_rows_for_slice(cur, family: str, wave: str) -> list[tuple[Any, ...]]:
    allowed = WEIGHT_ALLOWLIST.get(family, {}).get(wave, [])
    if not allowed:
        return []
    cur.execute(
        """
        SELECT id
        FROM survey_microdata_respondents
        WHERE source = %s AND wave = %s
        ORDER BY id
        """,
        (family, wave),
    )
    respondent_ids = [row[0] for row in cur.fetchall()]
    if not respondent_ids:
        return []

    allowed_upper = [w.upper() for w in allowed]
    insert_rows: list[tuple[Any, ...]] = []
    chunk_size = 1000
    cur.execute(
        """
        CREATE TEMP TABLE IF NOT EXISTS tmp_weight_respondents (
            respondent_id INT PRIMARY KEY
        ) ON COMMIT DROP
        """
    )
    for start in range(0, len(respondent_ids), chunk_size):
        chunk = respondent_ids[start : start + chunk_size]
        chunk_index = start // chunk_size + 1
        total_chunks = (len(respondent_ids) + chunk_size - 1) // chunk_size
        print(
            f"    {family} {wave}: chunk {chunk_index}/{total_chunks} respondents={len(chunk)}",
            flush=True,
        )
        cur.execute("TRUNCATE tmp_weight_respondents")
        execute_values(
            cur,
            "INSERT INTO tmp_weight_respondents (respondent_id) VALUES %s",
            [(int(rid),) for rid in chunk],
            page_size=1000,
        )
        cur.execute(
            """
            SELECT resp.respondent_id, UPPER(resp.var_code) AS var_code, resp.var_code, resp.value_raw
            FROM survey_microdata_responses resp
            JOIN tmp_weight_respondents t
              ON t.respondent_id = resp.respondent_id
              AND UPPER(resp.var_code) = ANY(%s)
            ORDER BY resp.respondent_id, UPPER(resp.var_code)
            """,
            (allowed_upper,),
        )
        grouped: dict[int, list[tuple[str, str, float | None]]] = defaultdict(list)
        for respondent_id, var_code_upper, var_code_raw, value_raw in cur.fetchall():
            value = None if value_raw is None else float(value_raw)
            grouped[int(respondent_id)].append((str(var_code_raw), str(var_code_upper), value))
        for respondent_id, rows in grouped.items():
            chosen = primary_weight_name(family, wave, [r[0] for r in rows])
            for var_code_raw, var_code_upper, value in rows:
                insert_rows.append(
                    (
                        int(respondent_id),
                        var_code_raw,
                        value,
                        determine_weight_type(var_code_raw),
                        var_code_raw,
                        family,
                        wave,
                        var_code_raw == chosen,
                        "Loaded from survey_microdata_responses using explicit allowlist.",
                    )
                )
    return insert_rows


def load_weights(conn, families: list[str], replace: bool = True) -> tuple[int, int]:
    cur = conn.cursor()
    ensure_weight_table(cur)
    selected_families = [family for family in families if family]
    family_filter_sql = ""
    family_filter_params: list[Any] = []
    if selected_families:
        family_filter_sql = " AND source_family = ANY(%s)"
        family_filter_params.append(selected_families)

    cur.execute(
        f"""
        SELECT
            respondent_id,
            source_family,
            wave,
            survey_weight,
            survey_weight_source_var
        FROM respondent_position_fact
        WHERE survey_weight IS NOT NULL
        {family_filter_sql}
        ORDER BY source_family, wave, respondent_id
        """,
        family_filter_params,
    )
    fetched = cur.fetchall()

    if replace:
        if selected_families:
            cur.execute(
                "DELETE FROM survey_weight_fact WHERE source = ANY(%s)",
                (selected_families,),
            )
        else:
            cur.execute("TRUNCATE survey_weight_fact")
        conn.commit()

    rows: list[tuple[Any, ...]] = []
    for respondent_id, source_family, wave, survey_weight, survey_weight_source_var in fetched:
        source_var = clean(survey_weight_source_var)
        rows.append(
            (
                int(respondent_id),
                source_var or "survey_weight",
                float(survey_weight) if survey_weight is not None else None,
                "primary_weight",
                source_var or None,
                clean(source_family),
                clean(wave),
                True,
                "Loaded from respondent_position_fact survey_weight column.",
            )
        )

    if rows:
        execute_values(
            cur,
            """
            INSERT INTO survey_weight_fact (
                respondent_id, weight_name, weight_value, weight_type,
                source_var, source, wave, is_primary, notes
            ) VALUES %s
            ON CONFLICT (respondent_id, weight_name)
            DO UPDATE SET
                weight_value = EXCLUDED.weight_value,
                weight_type = EXCLUDED.weight_type,
                source_var = EXCLUDED.source_var,
                source = EXCLUDED.source,
                wave = EXCLUDED.wave,
                is_primary = EXCLUDED.is_primary,
                notes = EXCLUDED.notes,
                loaded_at = NOW()
            """,
            rows,
            page_size=1000,
        )
        conn.commit()

    cur.close()
    return len(rows), len(rows)


def create_respondent_position_view(conn) -> None:
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS v_ddm_response_long_facet_ready")
    cur.execute("DROP VIEW IF EXISTS respondent_position_fact")
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'respondentsDemo%' AND table_name NOT ILIKE '%unknown%' ORDER BY table_name")
    tables = [row[0] for row in cur.fetchall()]
    if not tables:
        raise RuntimeError("No respondentsDemo* tables were found in the live Postgres database.")
    selects: list[str] = []
    for table in tables:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            """,
            (table,),
        )
        cols = {row[0] for row in cur.fetchall()}

        def col(name: str, sql_type: str = "TEXT") -> str:
            if name in cols:
                return name
            return f"NULL::{sql_type} AS {name}"

        completeness_fields = [
            name
            for name in [
                "source_family",
                "wave",
                "country_code",
                "survey_year",
                "sex",
                "age",
                "education_level",
                "income_level",
                "income_source_note",
                "survey_weight",
                "survey_weight_source_var",
                "urban_rural",
                "religion_label",
                "marital",
                "employment",
                "class_level",
                "household_size",
                "language",
                "region",
                "ethnicity",
            ]
            if name in cols
        ]
        if completeness_fields:
            completeness_expr = " + ".join(
                f"CASE WHEN {name} IS NOT NULL AND {name}::TEXT <> '' THEN 1 ELSE 0 END"
                for name in completeness_fields
            )
        else:
            completeness_expr = "0"

        selects.append(
            f"""
        SELECT
            respondent_id,
            {col('source_family')},
            {col('wave')},
            {col('country_code')},
            {col('survey_year', 'INT')},
            {col('sex')},
            {col('age')},
            CASE
                WHEN NULLIF({col('age')}, '')::DOUBLE PRECISION IS NOT NULL
                 AND NULLIF({col('age')}, '')::DOUBLE PRECISION < 30 THEN '18-29'
                WHEN NULLIF({col('age')}, '')::DOUBLE PRECISION IS NOT NULL
                 AND NULLIF({col('age')}, '')::DOUBLE PRECISION < 45 THEN '30-44'
                WHEN NULLIF({col('age')}, '')::DOUBLE PRECISION IS NOT NULL
                 AND NULLIF({col('age')}, '')::DOUBLE PRECISION < 60 THEN '45-59'
                WHEN NULLIF({col('age')}, '')::DOUBLE PRECISION IS NOT NULL THEN '60+'
                ELSE ''
            END AS age_group,
            {col('education_level')},
            {col('income_level')},
            {col('income_source_note')},
            {col('survey_weight', 'DOUBLE PRECISION')},
            {col('survey_weight_source_var')},
            {col('urban_rural')},
            {col('religion_label')},
                {col('marital')},
                {col('employment')},
                {col('class_level')},
                {col('household_size')},
                {col('language')},
                {col('region')},
                {col('ethnicity')},
                '{table}'::TEXT AS position_source_table,
                ({completeness_expr})::INT AS position_completeness_score
            FROM "{table}"
            """
        )

    sql = "CREATE OR REPLACE VIEW respondent_position_fact AS\n" + "\nUNION ALL\n".join(selects)
    cur.execute(sql)
    conn.commit()
    cur.close()


def create_facet_ready_view(conn) -> None:
    cur = conn.cursor()
    cur.execute(FACET_READY_VIEW_SQL)
    conn.commit()
    cur.close()


def verify(conn) -> dict[str, Any]:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM question_structural_mapping")
    qsm_count = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM survey_weight_fact")
    weight_count = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM survey_weight_fact WHERE is_primary")
    weight_primary_count = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM respondent_position_fact")
    position_count = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM v_ddm_response_long_facet_ready")
    facet_ready_count = int(cur.fetchone()[0])
    cur.close()
    return {
        "question_structural_mapping_rows": qsm_count,
        "survey_weight_fact_rows": weight_count,
        "survey_weight_fact_primary_rows": weight_primary_count,
        "respondent_position_fact_rows": position_count,
        "facet_ready_response_rows": facet_ready_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply the Postgres facet-ready substrate.")
    parser.add_argument(
        "--family",
        action="append",
        default=[],
        help="Restrict survey weight loading to one or more families. Defaults to all families with respondent-level weights.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the intended actions without mutating the database.",
    )
    parser.add_argument(
        "--no-replace",
        action="store_true",
        help="Do not delete existing survey_weight_fact rows for the selected families/waves before reload.",
    )
    parser.add_argument(
        "--views-only",
        action="store_true",
        help="Only recreate respondent_position_fact and v_ddm_response_long_facet_ready; skip mapping and weights.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT / ".env")
    args = parse_args()
    families = [f.strip() for f in args.family if f.strip()]
    if args.dry_run:
        qsm = load_question_mapping_authority()
        print(f"dry-run: R1 question mapping authority={QUESTION_MAPPING_AUTHORITY}")
        print(f"dry-run: R1 question mapping rows={len(qsm)}")
        print(f"dry-run: families={families if families else 'ALL'}")
        print("dry-run: survey weights will be loaded from respondent_position_fact.survey_weight")
        return 0
    conn = connect_db()
    try:

        if not args.views_only:
            print("creating question_structural_mapping...")
            qsm_count = load_question_mapping(conn)
            print(f"  loaded {qsm_count} mapping rows")

        print("creating respondent_position_fact view...")
        create_respondent_position_view(conn)
        print("  respondent_position_fact view applied")

        if not args.views_only:
            print("creating survey_weight_fact table...")
            cur = conn.cursor()
            ensure_weight_table(cur)
            conn.commit()
            cur.close()

            print(f"loading survey weights for families={families if families else 'ALL'}...")
            weight_rows, primary_rows = load_weights(conn, families, replace=not args.no_replace)
            print(f"  loaded {weight_rows} weight rows ({primary_rows} primary)")

        print("creating v_ddm_response_long_facet_ready view...")
        create_facet_ready_view(conn)
        print("  v_ddm_response_long_facet_ready view applied")

        if not args.views_only:
            report = verify(conn)
            OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
            OUT_REPORT.write_text(pd.Series(report).to_json(indent=2), encoding="utf-8")
            print(report)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
