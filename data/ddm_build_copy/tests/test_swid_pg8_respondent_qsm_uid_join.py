from __future__ import annotations

import inspect

from data.ddm_build_copy import apply_postgres_facet_ready_substrate as db
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


def _body() -> str:
    return db.FACET_READY_VIEW_SQL.split("SELECT\n", 1)[1].split(
        "FROM survey_microdata_responses resp", 1
    )[0]


def test_governed_aliases_share_uid_identity_but_not_cross_wave_identity():
    arab_i = resolve_source_wave_identity("Arab Barometer", "I")
    arab_w1 = resolve_source_wave_identity("Arab Barometer", "W1")
    arab_v = resolve_source_wave_identity("Arab Barometer", "V")
    assert (arab_i.source_family_uid, arab_i.wave_uid) == (
        arab_w1.source_family_uid, arab_w1.wave_uid
    )
    assert arab_i.wave_uid != arab_v.wave_uid

    evs_1981 = resolve_source_wave_identity("EVS", "1981")
    evs_w1 = resolve_source_wave_identity("EVS", "W1")
    evs_1999 = resolve_source_wave_identity("EVS", "1999")
    evs_w3 = resolve_source_wave_identity("EVS", "W3")
    assert (evs_1981.source_family_uid, evs_1981.wave_uid) == (
        evs_w1.source_family_uid, evs_w1.wave_uid
    )
    assert evs_1981.wave_uid != evs_1999.wave_uid
    assert evs_1981.wave_uid != evs_w3.wave_uid


def test_identity_materialization_and_uid_join_are_governed_not_spelling_based():
    sql = db.FACET_READY_VIEW_SQL
    body = _body()
    assert "CREATE TABLE IF NOT EXISTS respondent_source_wave_identity" in db.RESPONDENT_SOURCE_WAVE_IDENTITY_SQL
    assert "SELECT DISTINCT source, COALESCE(wave, '')" in inspect.getsource(db.load_respondent_source_wave_identity)
    assert "rsi.raw_db_source = r.source" in sql
    assert "rsi.raw_db_wave = COALESCE(r.wave, '')" in sql
    assert "q.source_family_uid = rsi.source_family_uid" in sql
    assert "q.wave_uid = rsi.wave_uid" in sql
    assert "q.wave = COALESCE(r.wave, '')" not in sql
    assert "q.canonical_display_wave = r.wave" not in sql
    assert "Arab Barometer" not in sql
    assert "EVS" not in sql
    assert "rsi.canonical_display_wave AS canonical_wave" in body
    assert "rsi.canonical_display_source" in body
    assert "rsi.source_family_uid" in body
    assert "rsi.wave_uid" in body
    assert "rsi.governance_state AS source_wave_governance_state" in body
    assert "rsi.closed_35_member AS source_wave_closed_35_member" in body
    assert "r.source AS raw_db_source" in body
    assert "r.wave AS raw_db_wave" in body


def test_blank_wave_family_fallback_does_not_invent_wave_identity():
    source_uid, wave_uid, display_source, display_wave, state, closed = db._identity_fields("EVS", "")
    assert source_uid == "sf_evs_v1"
    assert wave_uid == ""
    assert display_source == "EVS"
    assert display_wave == ""
    assert state == ""
    assert closed is None


def test_recognized_excluded_wave_does_not_become_closed_35():
    values = db._respondent_identity_row("Asian Barometer", "W6")
    assert values[2] == "sf_asian_barometer_v1"
    assert values[3] == "wv_asian_barometer_w6_v1"
    assert values[6] == "RECOGNIZED_EXCLUDED"
    assert values[7] is False
    assert values[8] == "RESOLVED_RECOGNIZED_EXCLUDED"


def test_pg8_historical_prefix_remains_before_additive_identity_fields():
    body = _body()
    historical = (
        "r.id AS respondent_id", "r.source,", "r.wave,",
        "rsi.canonical_display_wave AS canonical_wave", "r.country_code",
        "r.survey_year", "resp.var_code", "resp.value_raw", "resp.value_text",
        "wp.weight_value", "wp.weight_name", "END AS weight_status",
        "pos.sex", "pos.age", "END AS age_group", "pos.education_level",
        "pos.income_level", "pos.religion_label", "pos.urban_rural", "pos.region",
        "pos.ethnicity", "pos.language", "pos.employment", "pos.marital",
        "pos.household_size", "pos.position_source_table",
        "pos.position_completeness_score", "COALESCE(qsm.question_id, resp.var_code) AS question_id",
        "qsm.question_block_id", "qsm.structural_domain_id", "qsm.driver_id",
        "qsm.driver_facet_id", "qsm.relation_axis_id", "qsm.target_entity_id",
        "qsm.mapping_status", "qsm.legacy_final_driver_id", "END AS legacy_driver_leak_flag",
    )
    additive = (
        "r.source AS raw_db_source", "r.wave AS raw_db_wave",
        "rsi.canonical_display_source", "rsi.source_family_uid", "rsi.wave_uid",
        "rsi.governance_state AS source_wave_governance_state",
        "rsi.closed_35_member AS source_wave_closed_35_member",
    )
    historical_positions = [body.index(fragment) for fragment in historical]
    additive_positions = [body.index(fragment) for fragment in additive]
    assert historical_positions == sorted(historical_positions)
    assert additive_positions == sorted(additive_positions)
    assert min(additive_positions) > max(historical_positions)
