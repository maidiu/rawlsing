import csv
import hashlib
from pathlib import Path

import pandas as pd

from data.ddm_build_copy.apply_postgres_facet_ready_substrate import (
    QUESTION_MAPPING_SQL,
    load_question_mapping_authority,
)
from data.ddm_build_copy.ddm_v550_shared_cache import question_structural_mapping_select_columns
from data.ddm_build_copy.ddm_v550_question_relation_authority import (
    CALIBRATION_AUTHORITY_PATH,
    FULL_AUTHORITY_PATH,
    LEGACY_RESIDUAL_ROW_COUNT,
    R1_TARGET_ROW_COUNT,
    active_closed_35_waves,
    apply_question_relation_authority,
    derive_legacy_latinobarometro_1995_residual,
    load_question_relation_authority,
    resolve_question_relation_authority,
)


def test_r1_package_checksum_and_full_runtime_index_are_exact():
    package = FULL_AUTHORITY_PATH.parent
    for row in csv.DictReader((package / "SHA256SUMS.csv").open(newline="")):
        data = (package / row["file"]).read_bytes()
        assert len(data) == int(row["bytes"])
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
    index = load_question_relation_authority()
    assert index.path == FULL_AUTHORITY_PATH
    assert len(index.rows) == 18518
    assert len(active_closed_35_waves()) == 35


def test_calibration_registry_remains_separate_from_active_r1_runtime():
    calibration = pd.read_csv(CALIBRATION_AUTHORITY_PATH, dtype=str, keep_default_na=False)
    assert len(calibration) == 700
    assert load_question_relation_authority().path != CALIBRATION_AUTHORITY_PATH


def test_r1_dispositions_and_fail_closed_blockers_are_consumed():
    directional = resolve_question_relation_authority(
        source_family="Afrobarometer", canonical_wave_value="R1", country_code="BF", var_code="demele"
    )
    assert directional.resolved
    assert directional.authority_row["authority_status"] == "GOVERNED_QSMV2_RELATION_AUTHORITY"
    assert directional.authority_row["driver_id"]

    context = resolve_question_relation_authority(
        source_family="GSS", canonical_wave_value="1972", country_code="US", var_code="age"
    )
    assert context.resolved
    assert context.authority_row["authority_status"] == "GOVERNED_NON_DIRECTIONAL_DISPOSITION"
    assert not apply_question_relation_authority(context.authority_row)["current_directional_atom_eligible"]

    asian = resolve_question_relation_authority(
        source_family="Asian Barometer", canonical_wave_value="W6", country_code="CN", var_code="anything"
    )
    assert asian.status == "BLOCKED_EXCLUDED_ASIAN_W6"


def test_postgres_mapping_loader_uses_exact_full_r1_live_surface():
    frame = load_question_mapping_authority()
    assert len(frame) == R1_TARGET_ROW_COUNT + LEGACY_RESIDUAL_ROW_COUNT
    assert len(frame.iloc[:R1_TARGET_ROW_COUNT]) == R1_TARGET_ROW_COUNT
    residual = frame.iloc[R1_TARGET_ROW_COUNT:]
    assert len(residual) == 20
    assert set(residual["source"]) == {"Latinobarómetro"}
    assert set(residual["canonical_wave"]) == {"1995"}
    assert list(frame.columns)[-4:] == ["canonical_wave", "country_code_scope", "authority_status", "authority_rule_id"]
    assert frame["authority_status"].isin({
        "GOVERNED_QSMV2_RELATION_AUTHORITY", "GOVERNED_MANUAL_RELATION_AUTHORITY",
        "FROZEN_ACCEPTED_GSS", "GOVERNED_NON_DIRECTIONAL_DISPOSITION",
        "GOVERNED_ADMINISTRATIVE_DISPOSITION", "EXCLUDED_INACTIVE_WAVE",
        "BLOCKED_STRUCTURAL_MAPPING_AUTHORITY", "BLOCKED_SOURCE_AUTHORITY",
        "BLOCKED_IDENTITY_OR_AUTHORITY_JOIN",
    }).all()


def test_legacy_residual_is_exactly_the_twenty_row_calibration_difference():
    r1 = pd.read_csv(FULL_AUTHORITY_PATH, dtype=str, keep_default_na=False)
    residual = derive_legacy_latinobarometro_1995_residual(r1)
    calibration = pd.read_csv(CALIBRATION_AUTHORITY_PATH, dtype=str, keep_default_na=False)
    assert len(residual) == 20
    assert set(residual["question_id"]) == set(calibration.loc[
        (calibration["source_family"] == "Latinobarómetro") & (calibration["canonical_wave"] == "1995"),
        "question_id",
    ])
    assert set(residual["question_id"]).isdisjoint(set(r1["question_id"]))
    assert set(residual["var_code"].str.casefold()).issubset(set(r1["var_code"].str.casefold()))
    assert len(calibration) - len(residual) == 680
    for _, legacy in residual.iterrows():
        primary = r1[
            (r1["source"].map(str.casefold) == str(legacy["source_family"]).casefold())
            & (r1["canonical_wave"] == legacy["canonical_wave"])
            & (r1["country_code_scope"] == legacy["country_code_scope"])
            & (r1["var_code"].str.casefold() == str(legacy["var_code"]).casefold())
        ]
        assert len(primary) == 1


def test_qsm_selector_requests_r1_identity_fields_when_postgres_exposes_them(monkeypatch):
    class FakeConn:
        pass

    def fake_read_sql_query(sql, conn, params):
        assert "information_schema.columns" in sql
        return pd.DataFrame({"column_name": [
            "source", "wave", "question_id", "var_code", "canonical_wave",
            "country_code_scope", "authority_status", "authority_rule_id",
        ]})

    monkeypatch.setattr(pd, "read_sql_query", fake_read_sql_query)
    selected = question_structural_mapping_select_columns(FakeConn())
    assert selected[-4:] == ["canonical_wave", "country_code_scope", "authority_status", "authority_rule_id"]
    for field in ("canonical_wave", "country_code_scope", "authority_status", "authority_rule_id"):
        assert f"{field} TEXT NOT NULL DEFAULT ''" in QUESTION_MAPPING_SQL
