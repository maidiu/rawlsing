#!/usr/bin/env python3
"""Apply the Postgres facet-ready substrate for the broader builders.

This script does four things in the live Postgres database:

1. Create and populate question_structural_mapping from questions_master_drivers.csv.
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

Source/wave UID fields are additive: raw database source/wave remain the query
coordinates while governed display labels and UIDs travel beside them.
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentityError,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)

QUESTIONS_MASTER = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
OUT_REPORT = ROOT / "data" / "ddm_build_copy" / "reports" / "apply_postgres_facet_ready_substrate_report.json"


# These fields define semantic equality for QSM conflict handling.  Raw
# spelling, display provenance, and load timing are intentionally excluded.
QSM_SEMANTIC_FIELD_INDICES = tuple(range(11, 28))
QSM_SEMANTIC_DB_FIELDS = (
    "legacy_final_driver_id",
    "final_driver_label",
    "final_driver_scope",
    "final_driver_origin",
    "driver_id",
    "driver_facet_id",
    "question_block_id",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
    "mapping_status",
    "evidence_kind",
    "strata_relevance",
    "channel_affordances",
    "forbidden_inference",
    "does_not_measure",
    "review_notes",
)


QUESTION_MAPPING_SQL = """
CREATE TABLE IF NOT EXISTS question_structural_mapping (
    source TEXT NOT NULL,
    wave TEXT NOT NULL DEFAULT '',
    source_family_uid TEXT,
    wave_uid TEXT,
    canonical_display_source TEXT,
    canonical_display_wave TEXT,
    governance_state TEXT,
    closed_35_member BOOLEAN,
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
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source, wave, var_code)
);

ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS source_family_uid TEXT;
ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS wave_uid TEXT;
ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS canonical_display_source TEXT;
ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS canonical_display_wave TEXT;
ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS governance_state TEXT;
ALTER TABLE question_structural_mapping ADD COLUMN IF NOT EXISTS closed_35_member BOOLEAN;

CREATE INDEX IF NOT EXISTS idx_question_structural_mapping_source_wave_var
    ON question_structural_mapping(source, wave, var_code);
CREATE INDEX IF NOT EXISTS idx_question_structural_mapping_uid_var
    ON question_structural_mapping(source_family_uid, wave_uid, var_code);
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


RESPONDENT_SOURCE_WAVE_IDENTITY_SQL = """
CREATE TABLE IF NOT EXISTS respondent_source_wave_identity (
    raw_db_source TEXT NOT NULL,
    raw_db_wave TEXT NOT NULL DEFAULT '',
    source_family_uid TEXT,
    wave_uid TEXT,
    canonical_display_source TEXT,
    canonical_display_wave TEXT,
    governance_state TEXT,
    closed_35_member BOOLEAN,
    resolution_status TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (raw_db_source, raw_db_wave)
);

CREATE INDEX IF NOT EXISTS idx_respondent_source_wave_identity_uid
    ON respondent_source_wave_identity(source_family_uid, wave_uid);
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
    rsi.canonical_display_wave AS canonical_wave,
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
    END AS legacy_driver_leak_flag,

    r.source AS raw_db_source,
    r.wave AS raw_db_wave,
    rsi.canonical_display_source,
    rsi.source_family_uid,
    rsi.wave_uid,
    rsi.governance_state AS source_wave_governance_state,
    rsi.closed_35_member AS source_wave_closed_35_member
FROM survey_microdata_responses resp
JOIN survey_microdata_respondents r
    ON r.id = resp.respondent_id
LEFT JOIN respondent_source_wave_identity rsi
    ON rsi.raw_db_source = r.source
   AND rsi.raw_db_wave = COALESCE(r.wave, '')
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
    WHERE q.source_family_uid = rsi.source_family_uid
      AND UPPER(q.var_code) = UPPER(resp.var_code)
      AND (
          (
              NULLIF(rsi.wave_uid, '') IS NOT NULL
              AND q.wave_uid = rsi.wave_uid
          )
          OR (
              NULLIF(rsi.wave_uid, '') IS NULL
              AND NULLIF(q.wave_uid, '') IS NULL
              AND COALESCE(q.wave, '') = ''
          )
      )
    ORDER BY
        CASE WHEN NULLIF(q.wave_uid, '') IS NOT NULL THEN 0 ELSE 1 END,
        q.loaded_at DESC
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


def semantic_mapping_signature(values: Iterable[Any]) -> tuple[str, ...]:
    """Normalize semantic fields for conflict comparison."""
    return tuple(clean(value) for value in values)


def _candidate_semantic_signature(row: tuple[Any, ...]) -> tuple[str, ...]:
    return semantic_mapping_signature(row[index] for index in QSM_SEMANTIC_FIELD_INDICES)


def quarantine_conflicting_question_mapping_rows(
    rows: Iterable[tuple[Any, ...]],
) -> tuple[list[tuple[Any, ...]], list[tuple[str, str, str]]]:
    """Drop every candidate in each genuinely divergent UID-normalized group."""
    candidates = list(rows)
    groups: dict[tuple[str, str, str], list[tuple[Any, ...]]] = defaultdict(list)
    for row in candidates:
        source_family_uid = clean(row[2])
        wave_uid = clean(row[3])
        if source_family_uid and wave_uid:
            key = (source_family_uid, wave_uid, clean(row[9]).upper())
            groups[key].append(row)

    conflicts = sorted(
        key for key, members in groups.items()
        if len({_candidate_semantic_signature(row) for row in members}) > 1
    )
    conflict_keys = set(conflicts)
    kept = [
        row for row in candidates
        if (
            not clean(row[2])
            or not clean(row[3])
            or (clean(row[2]), clean(row[3]), clean(row[9]).upper()) not in conflict_keys
        )
    ]
    return kept, conflicts


def _identity_fields(source: str, wave: str) -> tuple[str, str, str, str, str, bool | None]:
    """Resolve additive semantic identity without changing raw source/wave fields."""
    if not clean(wave):
        try:
            family = resolve_source_family_identity(source)
        except SourceWaveIdentityError:
            return "", "", "", "", "", None
        return family.source_family_uid, "", family.canonical_display_source, "", "", None
    try:
        identity = resolve_source_wave_identity(source, wave)
    except SourceWaveIdentityError:
        return "", "", "", "", "", None
    return (
        identity.source_family_uid,
        identity.wave_uid,
        identity.canonical_display_source,
        identity.canonical_display_wave,
        identity.governance_state,
        identity.closed_35_member,
    )


def _respondent_identity_row(source: str, wave: str) -> tuple[Any, ...]:
    """Resolve one observed raw respondent coordinate through governed authority."""
    raw_source = clean(source)
    raw_wave = clean(wave)
    if not raw_source:
        return (raw_source, raw_wave, None, None, None, None, None, None, "UNRESOLVED")
    try:
        if not raw_wave:
            family = resolve_source_family_identity(raw_source)
            return (
                raw_source, raw_wave, family.source_family_uid, None,
                family.canonical_display_source, None, None, None,
                "RESOLVED_FAMILY_ONLY",
            )
        identity = resolve_source_wave_identity(raw_source, raw_wave)
    except SourceWaveIdentityError:
        return (raw_source, raw_wave, None, None, None, None, None, None, "UNRESOLVED")
    status = (
        "RESOLVED_CLOSED_35"
        if identity.closed_35_member
        else "RESOLVED_RECOGNIZED_EXCLUDED"
        if identity.governance_state
        else "RESOLVED_NONPRODUCTION"
    )
    return (
        raw_source, raw_wave, identity.source_family_uid, identity.wave_uid,
        identity.canonical_display_source, identity.canonical_display_wave,
        identity.governance_state, identity.closed_35_member, status,
    )


def load_respondent_source_wave_identity(conn) -> int:
    """Materialize the exact observed raw respondent coordinates via the UID kernel."""
    cur = conn.cursor()
    cur.execute(RESPONDENT_SOURCE_WAVE_IDENTITY_SQL)
    cur.execute("""
        SELECT DISTINCT source, COALESCE(wave, '')
        FROM survey_microdata_respondents
        ORDER BY source, COALESCE(wave, '')
    """)
    pairs = cur.fetchall()
    rows = [_respondent_identity_row(source, wave) for source, wave in pairs]
    cur.execute("TRUNCATE respondent_source_wave_identity")
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO respondent_source_wave_identity (
                raw_db_source, raw_db_wave, source_family_uid, wave_uid,
                canonical_display_source, canonical_display_wave,
                governance_state, closed_35_member, resolution_status
            ) VALUES %s
            """,
            rows,
        )
    conn.commit()
    cur.close()
    return len(rows)


def assert_no_conflicting_qsm_uid_rows(conn) -> None:
    """Reject conflicting semantic duplicates before the UID join is published."""
    cur = conn.cursor()
    cur.execute("""
        SELECT source_family_uid, wave_uid, var_code,
               legacy_final_driver_id, final_driver_label, final_driver_scope,
               final_driver_origin, driver_id, driver_facet_id, question_block_id,
               structural_domain_id, relation_axis_id, target_entity_id,
               mapping_status, evidence_kind, strata_relevance,
               channel_affordances, forbidden_inference, does_not_measure,
               review_notes
        FROM question_structural_mapping
        WHERE NULLIF(source_family_uid, '') IS NOT NULL
          AND NULLIF(wave_uid, '') IS NOT NULL
        ORDER BY source_family_uid, wave_uid, UPPER(var_code), loaded_at
    """)
    groups: dict[tuple[str, str, str], set[tuple[str, ...]]] = defaultdict(set)
    for row in cur.fetchall():
        key = (str(row[0]), str(row[1]), str(row[2]).upper())
        groups[key].add(semantic_mapping_signature(row[3:]))
    conflicts = {key: values for key, values in groups.items() if len(values) > 1}
    cur.close()
    if conflicts:
        sample = next(iter(conflicts))
        raise RuntimeError(
            "CONFLICTING_QSM_UID_SEMANTIC_DUPLICATE: "
            f"source_family_uid={sample[0]} wave_uid={sample[1]} var_code={sample[2]}"
        )


def create_question_mapping_rows(df: pd.DataFrame) -> list[tuple[Any, ...]]:
    """Extract every source-master candidate without semantic precedence."""
    rows: list[tuple[Any, ...]] = []
    for r in df.itertuples(index=False):
        source = clean(getattr(r, "source", ""))
        wave = clean(getattr(r, "wave", ""))
        var_code = clean(getattr(r, "var_name", ""))
        if not source or not var_code:
            continue
        (
            source_family_uid,
            wave_uid,
            canonical_display_source,
            canonical_display_wave,
            governance_state,
            closed_35_member,
        ) = _identity_fields(source, wave)
        question_id = clean(getattr(r, "item_id", "")) or f"{source}:{wave}:{var_code}"
        row = (
            source,
            wave,
            source_family_uid,
            wave_uid,
            canonical_display_source,
            canonical_display_wave,
            governance_state,
            closed_35_member,
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
        rows.append(row)
    return rows


def deduplicate_question_mapping_rows(
    rows: Iterable[tuple[Any, ...]],
) -> list[tuple[Any, ...]]:
    """Deduplicate only after semantic-conflict groups have been removed."""
    deduplicated: dict[tuple[str, str, str], tuple[Any, ...]] = {}
    for row in rows:
        key = (clean(row[0]), clean(row[1]), clean(row[9]))
        if key not in deduplicated:
            deduplicated[key] = row
            continue
        existing = deduplicated[key]
        # Prefer the row with the richer mapping signal.
        existing_score = sum(1 for v in existing if isinstance(v, str) and v)
        new_score = sum(1 for v in row if isinstance(v, str) and v)
        if new_score >= existing_score:
            deduplicated[key] = row
    return list(deduplicated.values())


def ensure_question_mapping(cur) -> None:
    cur.execute(QUESTION_MAPPING_SQL)


def load_question_mapping(conn) -> int:
    df = load_questions_master()
    candidate_rows = create_question_mapping_rows(df)
    conflict_free_rows, quarantined_keys = quarantine_conflicting_question_mapping_rows(candidate_rows)
    rows = deduplicate_question_mapping_rows(conflict_free_rows)
    print(f"QSM semantic conflicts quarantined: {len(quarantined_keys)}", flush=True)
    for source_family_uid, wave_uid, var_code in quarantined_keys:
        print(f"{source_family_uid}|{wave_uid}|{var_code}", flush=True)
    cur = conn.cursor()
    ensure_question_mapping(cur)
    cur.execute("TRUNCATE question_structural_mapping")
    execute_values(
        cur,
        """
        INSERT INTO question_structural_mapping (
            source, wave, source_family_uid, wave_uid, canonical_display_source,
            canonical_display_wave, governance_state, closed_35_member,
            question_id, var_code, display_text, legacy_final_driver_id,
            final_driver_label, final_driver_scope, final_driver_origin, driver_id,
            driver_facet_id, question_block_id, structural_domain_id, relation_axis_id,
            target_entity_id, mapping_status, evidence_kind, strata_relevance,
            channel_affordances, forbidden_inference, does_not_measure, review_notes
        ) VALUES %s
        ON CONFLICT (source, wave, var_code)
        DO UPDATE SET
            source_family_uid = EXCLUDED.source_family_uid,
            wave_uid = EXCLUDED.wave_uid,
            canonical_display_source = EXCLUDED.canonical_display_source,
            canonical_display_wave = EXCLUDED.canonical_display_wave,
            governance_state = EXCLUDED.governance_state,
            closed_35_member = EXCLUDED.closed_35_member,
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
    load_respondent_source_wave_identity(conn)
    assert_no_conflicting_qsm_uid_rows(conn)
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
    conn = connect_db()
    try:
        if args.dry_run:
            qsm = load_questions_master()
            print(f"dry-run: questions_master rows={len(qsm)}")
            print(f"dry-run: families={families if families else 'ALL'}")
            print("dry-run: survey weights will be loaded from respondent_position_fact.survey_weight")
            return 0

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
