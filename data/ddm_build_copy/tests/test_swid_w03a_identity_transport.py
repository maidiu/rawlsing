#!/usr/bin/env python3
"""W03-A V550 source/wave identity transport regressions."""

from __future__ import annotations

import csv
import unicodedata
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_source_wave_identity import (
    GlobalWaveResolutionError,
    ProductionMembershipError,
    load_identity_registry,
    resolve_source_wave_identity,
    resolve_wave_identity,
)
from data.ddm_build_copy.ddm_v550_manifest import build_shard_manifest
from data.ddm_build_copy.ddm_v550_question_use import _select_itinerary
from data.ddm_build_copy.ddm_v550_readiness import _attach_governed_scope_identity
from data.ddm_build_copy.ddm_v550_shards import (
    require_v550_execution_identity,
    shard_id_for,
    v550_identity_fields,
)
from data.ddm_build_copy.plan_v550_wave_shards import _static_plan_from_template
from data.ddm_build_copy.run_v550_shards_from_plan import _build_command, _load_plan_rows


def _uid(source: str, wave: str) -> tuple[str, str]:
    identity = resolve_source_wave_identity(source, wave)
    return identity.source_family_uid, identity.wave_uid


def test_family_scoped_aliases_share_execution_uid() -> None:
    assert _uid("Arab Barometer", "I") == _uid("Arab Barometer", "W1")
    assert _uid("Arab Barometer", "I") == _uid("Arab Barometer", "Wave 1")
    assert _uid("Arab Barometer", "I") == _uid("Arab Barometer", "1")
    assert _uid("EVS", "1981") == _uid("EVS", "W1")
    assert _uid("EVS", "1999") == _uid("EVS", "W3")
    assert _uid("Afrobarometer", "R1") == _uid("Afrobarometer", "ROUND1")
    assert _uid("Afrobarometer", "R1") == _uid("Afrobarometer", "Round 1")


def test_latinobarometro_unicode_aliases_share_uid() -> None:
    source_nfc = unicodedata.normalize("NFC", "Latinobarómetro")
    source_nfd = unicodedata.normalize("NFD", "Latinobarómetro")
    assert _uid(source_nfc, "1995") == _uid(source_nfd, "1995")
    assert _uid(source_nfc, "1995") == _uid("Latinobarometro", "1995")


def test_no_global_bare_w1_resolution() -> None:
    with pytest.raises(GlobalWaveResolutionError):
        resolve_wave_identity("W1")


def test_asian_barometer_w6_recognized_but_not_executable() -> None:
    recognized = resolve_source_wave_identity("Asian Barometer", "W6")
    assert recognized.closed_35_member is False
    with pytest.raises(ProductionMembershipError):
        require_v550_execution_identity("Asian Barometer", "W6")


def test_registry_is_exact_closed_35() -> None:
    registry = load_identity_registry()
    assert len(registry.closed_35_pairs) == 35


def test_v550_identity_fields_preserve_raw_evs_db_wave() -> None:
    fields = v550_identity_fields("EVS", "1981")
    assert fields["raw_db_source"] == "EVS"
    assert fields["raw_db_wave"] == "1981"
    assert fields["wave_uid"] == resolve_source_wave_identity("EVS", "W1").wave_uid
    assert fields["closed_35_member"] is True


def test_redundant_identity_contradiction_fails_closed() -> None:
    evs_1981 = resolve_source_wave_identity("EVS", "1981")
    evs_1999 = resolve_source_wave_identity("EVS", "1999")
    with pytest.raises(BoundaryContractError):
        require_v550_execution_identity(
            "EVS",
            "1981",
            expected_source_family_uid=evs_1981.source_family_uid,
            expected_wave_uid=evs_1981.wave_uid,
            redundant_identity={
                "source": "EVS",
                "wave": "1981",
                "canonical_wave": "W3",
                "source_family_uid": evs_1981.source_family_uid,
                "wave_uid": evs_1999.wave_uid,
            },
        )


def test_historical_shard_identifiers_are_unchanged_and_unicode_physical_ids_remain_distinct() -> None:
    assert shard_id_for("EVS", "1981") == "EVS__1981"
    source_nfc = unicodedata.normalize("NFC", "Latinobarómetro")
    source_nfd = unicodedata.normalize("NFD", "Latinobarómetro")
    assert _uid(source_nfc, "1995") == _uid(source_nfd, "1995")
    assert shard_id_for(source_nfc, "1995") != shard_id_for(source_nfd, "1995")


def test_scope_ingress_keeps_raw_coordinate_and_adds_uid() -> None:
    scope = pd.DataFrame([
        {"source": "EVS", "wave": "1981", "country_code": "IS", "respondents": 10}
    ])
    out = _attach_governed_scope_identity(scope, require_production_membership=True)
    assert out.loc[0, "source"] == "EVS"
    assert out.loc[0, "wave"] == "1981"
    assert out.loc[0, "raw_db_wave"] == "1981"
    assert out.loc[0, "wave_uid"] == resolve_source_wave_identity("EVS", "W1").wave_uid


def test_scope_ingress_missing_governance_never_defaults_allow() -> None:
    scope = pd.DataFrame([
        {"source": "Asian Barometer", "wave": "W6", "country_code": "XX", "respondents": 10}
    ])
    with pytest.raises(ProductionMembershipError):
        _attach_governed_scope_identity(scope, require_production_membership=True)


def test_static_planner_emits_uid_before_execution_and_omits_asian_w6(tmp_path: Path) -> None:
    template = tmp_path / "respondent_wave_schema_template.csv"
    pd.DataFrame([
        {"source_family": "EVS", "wave": "1981", "total_respondents": 100, "country_calculable_range": "1-1"},
        {"source_family": "Asian Barometer", "wave": "W6", "total_respondents": 100, "country_calculable_range": "1-1"},
    ]).to_csv(template, index=False)
    plan = _static_plan_from_template(template, "r1")
    assert list(plan["source"]) == ["EVS"]
    assert plan.loc[0, "source_family_uid"]
    assert plan.loc[0, "wave_uid"]
    assert plan.loc[0, "raw_db_wave"] == "1981"
    assert plan.loc[0, "shard_id"] == "EVS__1981"
    assert "V550_SOURCE_FAMILY_UID=" in plan.loc[0, "command"]
    assert "V550_WAVE_UID=" in plan.loc[0, "command"]


def test_launcher_rejects_missing_uid_and_preserves_legacy_shard_id(tmp_path: Path) -> None:
    plan = tmp_path / "shard_plan.csv"
    identity = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    row = {
        "run_id": "r1",
        "source": "EVS",
        "source_family": "EVS",
        "wave": "1981",
        "canonical_wave": identity.canonical_display_wave,
        "raw_db_source": "EVS",
        "raw_db_wave": "1981",
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "governance_state": identity.governance_state,
        "closed_35_member": "True",
        "shard_id": "EVS__1981",
        "countries": "[]",
    }
    with plan.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    loaded = _load_plan_rows(plan)
    assert loaded[0]["shard_id"] == "EVS__1981"
    bad = dict(row)
    bad["wave_uid"] = ""
    with plan.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(bad))
        writer.writeheader()
        writer.writerow(bad)
    with pytest.raises(RuntimeError, match="V550_PLAN_UID_IDENTITY_MISSING"):
        _load_plan_rows(plan)


def test_launcher_transports_uid_through_child_environment() -> None:
    identity = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    row = {
        "run_id": "r1",
        "shard_id": "EVS__1981",
        "source": "EVS",
        "wave": "1981",
        "canonical_wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "countries": "[]",
    }
    command = _build_command(
        row,
        response_option_map=None,
        max_depth=None,
        min_cell_n=None,
        min_branch_n=None,
        min_answer_n=None,
        full_readiness=False,
        readiness_only=False,
        readiness_artifact=None,
        readiness_output_root=None,
        stop_after_stage=0,
        shared_respondent_substrate_mode="off",
        joint_configuration_registry_path=None,
        joint_configuration_ids=[],
        resume=False,
        overwrite_shard=False,
        write_csv=True,
        write_parquet=True,
    )
    assert command[:3] == [
        "env",
        f"V550_SOURCE_FAMILY_UID={identity.source_family_uid}",
        f"V550_WAVE_UID={identity.wave_uid}",
    ]


def test_shard_manifest_carries_uid_additively_without_changing_shard_id(tmp_path: Path) -> None:
    manifest = build_shard_manifest(
        run_id="r1",
        shard_id="EVS__1981",
        source="EVS",
        source_family="EVS",
        wave="1981",
        canonical_wave="W1",
        created_at="t0",
        completed_at="t1",
        success=True,
        output_root=tmp_path,
        inputs={},
        rows_by_table={},
        warnings=[],
        errors=[],
        outputs=[],
        bridge_rows=0,
        v551_eligible_count=0,
        v551_excluded_count=0,
        promotable=False,
    )
    assert manifest["shard_id"] == "EVS__1981"
    assert manifest["raw_db_wave"] == "1981"
    assert manifest["wave_uid"] == resolve_source_wave_identity("EVS", "W1").wave_uid


@pytest.mark.xfail(
    strict=True,
    reason="SWID-016 local selector seam remains explicit: whole-file connector replacement is unsafe for the large semantic authority module",
)
def test_itinerary_gate_matches_evs_1981_and_w1_by_governed_uid() -> None:
    itinerary = pd.DataFrame([
        {
            "source": "EVS",
            "wave": "1981",
            "canonical_wave": "W1",
            "review_priority": "high",
            "manual_designation_required": True,
            "primary_docs": "primary",
            "secondary_docs": "secondary",
            "review_notes": "manual gate",
        }
    ])
    selected = _select_itinerary({"source": "EVS", "canonical_wave": "W1"}, itinerary)
    assert selected["manual_designation_required"] is True
    assert selected["review_priority"] == "high"


def test_true_absence_of_itinerary_row_retains_optional_default() -> None:
    itinerary = pd.DataFrame([
        {"source": "EVS", "wave": "1981", "manual_designation_required": True}
    ])
    selected = _select_itinerary({"source": "EVS", "canonical_wave": "W3"}, itinerary)
    assert selected["manual_designation_required"] is False
