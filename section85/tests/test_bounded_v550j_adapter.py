from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (  # noqa: E402
    _registry_status_is_executable,
    _validate_bounded_authority_registry,
)
from data.ddm_build_copy.ddm_v550j_joint_patterns import compile_v550j_family_tables  # noqa: E402

SECTION = ROOT / "section85"
AUTH = SECTION / "authority"
OUTPUTS = SECTION / "outputs"


def load_registry() -> dict:
    return yaml.safe_load((AUTH / "bounded_9source_v550j_registry.yaml").read_text(encoding="utf-8"))


def test_draft_registry_is_no_longer_executable() -> None:
    assert not _registry_status_is_executable("draft")
    assert _registry_status_is_executable("governed")


def test_bounded_registry_passes_exact_authority_validation() -> None:
    result = _validate_bounded_authority_registry(load_registry())
    assert result == {"bounded_family_count": 9, "bounded_item_count": 26, "p3_bound_item_count": 3}


def _first_item(registry: dict) -> dict:
    family = registry["families"][0]
    role = next(iter(family["item_role_groups"]))
    return family["item_role_groups"][role][0]


def _drop_first_lineage(registry: dict) -> None:
    _first_item(registry).pop("p2_lineage_id")


def _duplicate_first_item(registry: dict) -> None:
    family = registry["families"][0]
    role = next(iter(family["item_role_groups"]))
    family["item_role_groups"][role].append(copy.deepcopy(family["item_role_groups"][role][0]))


def _drop_adjudication(registry: dict) -> None:
    registry["families"][0]["authority_metadata"].pop("joint_configuration_adjudication_id")


def _promote_p2_inventory(registry: dict) -> None:
    registry["families"][0]["authority_metadata"]["p2_authority_effect"] = "P2_STRUCTURE_IS_J_FAMILY_AUTHORITY"


@pytest.mark.parametrize(
    "mutation,match",
    [
        (lambda r: r.update(status="draft"), "must be governed"),
        (lambda r: r.update(response_portability_status="AUTHORIZED"), "does not authorize response portability"),
        (lambda r: r["families"][0]["authority_metadata"].update(p3_authority_release_id="STALE"), "stale or mismatched"),
        (_drop_first_lineage, "missing source-local lineage"),
        (_duplicate_first_item, "duplicate var_code"),
        (_drop_adjudication, "missing bounded joint-configuration adjudication"),
        (_promote_p2_inventory, "improperly promoted"),
    ],
)
def test_authority_mutations_fail_closed(mutation, match: str) -> None:
    registry = copy.deepcopy(load_registry())
    mutation(registry)
    with pytest.raises(RuntimeError, match=match):
        _validate_bounded_authority_registry(registry)


def _family_items(family: dict) -> list[dict]:
    out = []
    for role, items in family["item_role_groups"].items():
        for item in items:
            x = dict(item)
            x["item_role"] = role
            out.append(x)
    return out


def _synthetic_frames(family: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    source = family["source_family"]
    wave = str(family["eligible_waves"][0])
    items = _family_items(family)
    question_rows = []
    response_rows = []
    for item in items:
        question_rows.append(
            {
                "var_code": item["var_code"],
                "question_id": item["question_implementation_id"],
                "question_text": item["condition_label"],
                "source": source,
                "wave": wave,
                "canonical_wave": wave,
            }
        )
    for respondent_num in range(1, 7):
        for item_num, item in enumerate(items, start=1):
            signed = bool(family.get("boundary_rules"))
            positive = (respondent_num + item_num) % 2 == 0
            response_rows.append(
                {
                    "respondent_id": f"r{respondent_num}",
                    "var_code": item["var_code"],
                    "question_id": item["question_implementation_id"],
                    "response_value_normalized": "1" if positive else "2",
                    "response_label": "support" if positive else "oppose",
                    "normalized_response_label": "support" if positive else "oppose",
                    "response_direction": "positive" if positive else "negative",
                    "response_intensity": 1.0,
                    "polarity": "positive" if positive else "negative",
                    "weight_value": 1.0,
                    "weight_status": "weighted_valid",
                    "is_substantive": signed,
                    "is_special": False,
                    "directionality_status": "inferred_from_directionality_overlay" if signed else "forced_unsigned_by_directionality_overlay",
                    "response_option_map_matched": signed,
                    "response_semantics_status": "certified" if signed else "preserved_not_certified",
                    "response_semantics_source": "response_option_map" if signed else "observed_response_row",
                    "response_semantics_contract_hash": "synthetic-canary",
                    "source": source,
                    "wave": wave,
                    "canonical_wave": wave,
                    "country_code": "ZZ",
                    "survey_year": 2000,
                    "semantic_role": "RELATION_EVIDENCE",
                    "v551_evidence_role": "DIRECT_RELATION_RESPONSE" if signed else "TOPOLOGY_ONLY",
                    "source_structure_classification": "substantive" if signed else "context",
                    "source_structure_source": "bounded_v550j_registry",
                    "source_structure_fields_joined": True,
                }
            )
    return pd.DataFrame(question_rows), pd.DataFrame(response_rows)


def test_all_nine_configurations_compile_on_controlled_substrate() -> None:
    registry = load_registry()
    results = []
    for family in registry["families"]:
        questions, responses = _synthetic_frames(family)
        tables = compile_v550j_family_tables(
            family,
            questions,
            responses,
            association_mode="off",
            emit_diagnostics=True,
            source=family["source_family"],
            wave=str(family["eligible_waves"][0]),
            canonical_wave=str(family["eligible_waves"][0]),
            country_code="ZZ",
        )
        patterns = tables["joint_response_pattern_index"]
        items = tables["joint_response_pattern_item_index"]
        audit = tables["joint_pattern_audit"]
        assert not patterns.empty, family["family_id"]
        assert not items.empty, family["family_id"]
        assert set(items["family_id"].astype(str)) == {family["family_id"]}
        results.append(
            {
                "joint_configuration_id": family["family_id"],
                "pattern_rows": len(patterns),
                "item_rows": len(items),
                "audit_rows": len(audit),
            }
        )
    assert len(results) == 9


def test_generated_authority_return_is_explicitly_bounded() -> None:
    result = json.loads((AUTH / "BOUNDED_V550J_AUTHORITY_RETURN.json").read_text())
    assert result["status"] == "PASS_BOUNDED_AUTHORITY_GENERATED"
    assert result["configuration_count"] == 9
    assert result["item_count"] == 26
    assert result["production_completeness_claim"] == "NO_PRODUCTION_COMPLETENESS_CLAIM"
    assert result["response_portability_status"] == "NOT_AUTHORIZED_BY_P3"


def _require_generated_outputs(path: Path) -> None:
    if os.environ.get("RAWLSING_SECTION85_GENERATED_OUTPUT_TESTS") != "1":
        pytest.skip("generated Section85 outputs are an explicit integration fixture")
    assert path.exists(), f"integration fixture missing: {path}"


def test_archive_truth_audit_proves_no_respondent_level_substrate() -> None:
    path = OUTPUTS / "CANARY_ARCHIVE_TRUTH_AUDIT.json"
    _require_generated_outputs(path)
    result = json.loads(path.read_text())
    assert result["status"] == "PASS_STATIC_CANARY_ARCHIVE_TRUTH_AUDIT"
    assert result["scope_count"] == 9
    assert result["respondent_identifier_schema_count"] == 0
    assert result["capability"]["archive_is_sufficient_for_static_authority_binding"] is True
    assert result["capability"]["archive_is_sufficient_for_real_v550j_execution_without_live_database"] is False


def test_live_host_execution_plan_is_exactly_nine_scopes() -> None:
    plan_path = OUTPUTS / "live_host_execution_template" / "reports" / "bounded_nine_canary_execution_plan.json"
    _require_generated_outputs(plan_path)
    payload = json.loads(plan_path.read_text())
    assert payload["preflight"]["status"] == "PASS_PLAN_READY"
    assert payload["preflight"]["scope_count"] == 9
    assert payload["preflight"]["database_required_for_execution"] is True
    assert len(payload["plan"]) == 9
    assert {row["source_family"] for row in payload["plan"]} == {
        "Afrobarometer", "Arab Barometer", "Asian Barometer", "EVS", "GSS",
        "Latinobarómetro", "LiTS", "South Asia", "WVS",
    }
    for row in payload["plan"]:
        assert row["commands"]["v550j"]
        assert row["commands"]["v551j"]
        assert row["commands"]["v552j"]
        assert "--association-mode" in row["commands"]["v550j"]
        assert row["commands"]["v550j"][row["commands"]["v550j"].index("--association-mode") + 1] == "off"


def test_registry_is_backed_by_separate_bounded_adjudication_release() -> None:
    registry = load_registry()
    assert registry["joint_configuration_authority_release_id"] == "V550J-BOUNDED-AUTHORITY-2026-08-02-R1"
    assert registry["joint_configuration_adjudication_set_hash"]
    for family in registry["families"]:
        metadata = family["authority_metadata"]
        assert metadata["joint_configuration_adjudication_id"].startswith("V550JADJ-")
        assert metadata["authority_basis_status"] == "HUMAN_ADJUDICATED_FROM_EXACT_SOURCE_EVIDENCE"
        assert metadata["p2_authority_effect"] in {
            "P2_DISCOVERY_EVIDENCE_ONLY_NOT_J_FAMILY_AUTHORITY",
            "EXISTING_GSS_IMPLEMENTATION_REFERENCE",
        }
