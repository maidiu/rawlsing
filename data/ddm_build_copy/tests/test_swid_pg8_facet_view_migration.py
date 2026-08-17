from __future__ import annotations

from data.ddm_build_copy import apply_postgres_facet_ready_substrate as db


HISTORICAL_PREFIX = (
    "r.id AS respondent_id",
    "r.source,",
    "r.wave,",
    "rsi.canonical_display_wave AS canonical_wave",
    "r.country_code",
    "r.survey_year",
    "resp.var_code",
    "resp.value_raw",
    "resp.value_text",
    "wp.weight_value",
    "wp.weight_name",
    "END AS weight_status",
    "pos.sex",
    "pos.age",
    "END AS age_group",
    "pos.education_level",
    "pos.income_level",
    "pos.religion_label",
    "pos.urban_rural",
    "pos.region",
    "pos.ethnicity",
    "pos.language",
    "pos.employment",
    "pos.marital",
    "pos.household_size",
    "pos.position_source_table",
    "pos.position_completeness_score",
    "COALESCE(qsm.question_id, resp.var_code) AS question_id",
    "qsm.question_block_id",
    "qsm.structural_domain_id",
    "qsm.driver_id",
    "qsm.driver_facet_id",
    "qsm.relation_axis_id",
    "qsm.target_entity_id",
    "qsm.mapping_status",
    "qsm.legacy_final_driver_id",
    "END AS legacy_driver_leak_flag",
)

ADDITIVE_FIELDS = (
    "r.source AS raw_db_source",
    "r.wave AS raw_db_wave",
    "rsi.canonical_display_source",
    "rsi.source_family_uid",
    "rsi.wave_uid",
    "rsi.governance_state AS source_wave_governance_state",
    "rsi.closed_35_member AS source_wave_closed_35_member",
)


def _select_body() -> str:
    sql = db.FACET_READY_VIEW_SQL
    return sql.split("SELECT\n", 1)[1].split("FROM survey_microdata_responses resp", 1)[0]


def test_facet_ready_view_is_additive_after_frozen_historical_prefix():
    body = _select_body()
    positions = [body.index(fragment) for fragment in HISTORICAL_PREFIX]
    assert positions == sorted(positions)

    additive_positions = [body.index(fragment) for fragment in ADDITIVE_FIELDS]
    assert additive_positions == sorted(additive_positions)
    assert min(additive_positions) > max(positions)


def test_facet_ready_view_preserves_raw_coordinates_and_governed_identity_provenance():
    sql = db.FACET_READY_VIEW_SQL
    body = _select_body()

    assert "r.source AS raw_db_source" in body
    assert "r.wave AS raw_db_wave" in body
    assert "rsi.canonical_display_wave AS canonical_wave" in body
    assert "rsi.canonical_display_source" in body
    assert "rsi.source_family_uid" in body
    assert "rsi.wave_uid" in body
    assert "rsi.governance_state AS source_wave_governance_state" in body
    assert "rsi.closed_35_member AS source_wave_closed_35_member" in body

    assert "q.source_family_uid" in sql
    assert "q.wave_uid" in sql
    assert "q.canonical_display_source" not in sql
    assert "q.canonical_display_wave" not in sql
    assert "q.wave = COALESCE(r.wave, '')" not in sql
