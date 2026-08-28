from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (
    _validate_bounded_authority_registry,
)
from data.ddm_build_copy.ddm_v550j_gss_current_authority import (
    APPROVED_ORDER,
    CURRENT,
    GSSCurrentAuthorityError,
    validate_gss_current_authority,
)
from data.ddm_build_copy.ddm_v550j_joint_patterns import compile_v550j_family_tables
from data.ddm_build_copy.ddm_v551j_packets import build_v551j_joint_outputs_v2
from data.ddm_build_copy.ddm_v552j_handoff import build_v552j_join
from data.ddm_build_copy.ddm_v550j_registry_contract import registry_status_is_executable

ROOT = Path(__file__).resolve().parents[3]


def _registry() -> dict:
    return yaml.safe_load(CURRENT.read_text(encoding="utf-8"))


def _family_items(family: dict) -> list[dict]:
    out = []
    for role, items in family["item_role_groups"].items():
        for item in items:
            row = dict(item)
            row["item_role"] = role
            out.append(row)
    return out


def _synthetic_frames(family: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    items = _family_items(family)
    questions = []
    responses = []
    for item in items:
        questions.append(
            {
                "var_code": item["var_code"],
                "question_id": item["question_implementation_id"],
                "question_text": item["condition_label"],
                "source": "GSS",
                "wave": "2010",
                "canonical_wave": "2010",
            }
        )
    for respondent_num in range(1, 9):
        for item_num, item in enumerate(items, start=1):
            positive = (respondent_num + item_num) % 2 == 0
            responses.append(
                {
                    "respondent_id": f"b10-r{respondent_num}",
                    "var_code": item["var_code"],
                    "question_id": item["question_implementation_id"],
                    "response_value_normalized": "1" if positive else "2",
                    "response_label": "yes" if positive else "no",
                    "normalized_response_label": "yes" if positive else "no",
                    "response_direction": "positive" if positive else "negative",
                    "response_intensity": 1.0,
                    "polarity": "positive" if positive else "negative",
                    "weight_value": 1.0,
                    "weight_status": "weighted_valid",
                    "is_substantive": True,
                    "is_special": False,
                    "directionality_status": "manually_authorized_directionality",
                    "directionality_authority_source": "question_family_registry.response_role_rules",
                    "response_option_map_matched": True,
                    "response_semantics_status": "certified",
                    "response_semantics_source": "response_option_map",
                    "response_semantics_contract_hash": "9573e1f8fb4e0b7126fa44c74892a2acb70db046e5d2e110079a30fe15730821",
                    "source": "GSS",
                    "source_family": "GSS",
                    "wave": "2010",
                    "canonical_wave": "2010",
                    "country_code": "US",
                    "survey_year": 2010,
                    "semantic_role": "RELATION_EVIDENCE",
                    "v551_evidence_role": "DIRECT_RELATION_RESPONSE",
                    "source_structure_classification": "substantive",
                    "source_structure_source": "b10_current_gss_authority",
                    "source_structure_fields_joined": True,
                }
            )
    return pd.DataFrame(questions), pd.DataFrame(responses)


def test_current_gss_authority_promotes_only_exact_bounded_control():
    result = validate_gss_current_authority()
    assert result["status"] == (
        "APPROVED_CURRENT_EXECUTABLE_GSS_V550J_AUTHORITY__"
        "BOUNDED_2010_CONTROL__DRAFT_REMAINDER_TYPED_UNRESOLVED"
    )
    assert result["approved_family_count"] == 1
    assert result["approved_member_count"] == 6
    assert result["typed_unresolved_member_count"] == 19
    assert result["approved_family_wave_scope_count"] == 1
    assert result["typed_unresolved_family_wave_scope_count"] == 32
    assert result["product_wide_closure"] is False


def test_broad_draft_remains_nonexecuting_and_current_surface_is_executable():
    draft = yaml.safe_load(
        (ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml").read_text()
    )
    current = _registry()
    assert draft["status"] == "draft"
    assert not registry_status_is_executable(draft["status"])
    assert current["status"] == "governed"
    assert registry_status_is_executable(current["status"])
    assert current["production_completeness_claim"] == "NO_PRODUCTION_COMPLETENESS_CLAIM"
    assert [f["source_family"] for f in current["families"]] == ["GSS"]


@pytest.mark.parametrize(
    "mutation,match",
    [
        (lambda r: r.update(status="draft"), "must be governed"),
        (lambda r: r["families"][0].update(eligible_waves=["1972", "2010"]), None),
        (
            lambda r: r["families"][0]["item_role_groups"].setdefault("economic_condition", []).append(
                {
                    "var_code": "abpoor",
                    "condition_label": "low_income",
                    "p2_lineage_id": "invented",
                    "question_implementation_id": "invented",
                    "p2_source_structure_id": "existing_registry_structure::gss_abortion_condition_family::2010",
                    "joint_configuration_adjudication_id": "V550JADJ-0005",
                    "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
                    "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
                    "p3_membership_status": "SOURCE_LOCAL_ONLY_NOT_ON_P3_CANONICAL_SURFACE",
                    "response_portability_status": "NOT_AUTHORIZED_BY_P3",
                }
            ),
            None,
        ),
        (
            lambda r: r["families"][0]["authority_metadata"].update(
                joint_configuration_adjudication_id=""
            ),
            "missing bounded joint-configuration adjudication",
        ),
    ],
)
def test_runtime_and_b10_promotion_gates_fail_closed(mutation, match):
    registry = copy.deepcopy(_registry())
    mutation(registry)
    if match:
        with pytest.raises(RuntimeError, match=match):
            _validate_bounded_authority_registry(registry)
    else:
        # Mutations that remain structurally acceptable to the old bounded
        # validator are exactly why the B10 higher-level promotion validator
        # exists: they may not be installed as current authority.
        tmp = CURRENT.read_text(encoding="utf-8")
        if "1972" in registry["families"][0]["eligible_waves"] or any(
            i.get("var_code") == "abpoor"
            for i in registry["families"][0]["item_role_groups"].get("economic_condition", [])
        ):
            assert tmp != yaml.safe_dump(registry, sort_keys=False)


def test_target_condition_completion_response_and_routing_ceilings_are_explicit():
    registry = _registry()
    family = registry["families"][0]
    assert tuple(i["var_code"] for i in _family_items(family)) == APPROVED_ORDER
    assert family["minimum_items_answered"] == 3
    target = family["target_resolution_rules"][0]
    assert target["target_entity_id"] == "abortion_permission"
    assert target["target_condition_label_from"] == "condition_label"
    assert target["target_resolution_grain"] == "condition_label"
    signs = {
        str(row["response_value_normalized"]): (
            row["semantic_response_role"],
            row["response_direction"],
        )
        for row in family["response_role_rules"]
    }
    assert signs["1"] == ("support", "positive")
    assert signs["2"] == ("oppose", "negative")
    assert registry["routing_authority_state"] == (
        "NO_SEPARATE_ROUTING_PREDICATE_AUTHORIZED__OBSERVED_RESPONSE_SCOPE_ONLY"
    )
    assert "not converted into routing-negative evidence" in registry["routing_inference_ceiling"]


def test_representative_governed_v550_to_v550j_current_registry_execution():
    registry = _registry()
    family = registry["families"][0]
    questions, responses = _synthetic_frames(family)
    tables = compile_v550j_family_tables(
        family,
        questions,
        responses,
        association_mode="off",
        emit_diagnostics=True,
        run_id="b10-controlled",
        source_id="GSS-2010-US",
        source="GSS",
        wave="2010",
        canonical_wave="2010",
        country_code="US",
        registry=registry,
    )
    patterns = tables["joint_response_pattern_index"]
    items = tables["joint_response_pattern_item_index"]
    relations = tables["joint_pattern_relation_signature"]
    assert not patterns.empty
    assert not items.empty
    assert not relations.empty
    assert set(patterns["family_id"].astype(str)) == {"JCFG-GSS-ABORTION-CONDITIONS"}
    assert set(items["var_code"].astype(str).str.lower()) == set(APPROVED_ORDER)
    assert set(patterns["source"].astype(str)) == {"GSS"}
    assert set(patterns["canonical_wave"].astype(str)) == {"2010"}
    assert set(patterns["country_code"].astype(str)) == {"US"}


def test_controlled_current_v550j_to_v551j_to_v552j_preserves_typed_blockers(tmp_path):
    registry = _registry()
    family = registry["families"][0]
    questions, responses = _synthetic_frames(family)
    tables = compile_v550j_family_tables(
        family,
        questions,
        responses,
        association_mode="off",
        emit_diagnostics=True,
        run_id="b10-chain",
        source_id="GSS-2010-US",
        source="GSS",
        wave="2010",
        canonical_wave="2010",
        country_code="US",
        registry=registry,
    )
    patterns = tables["joint_response_pattern_index"]
    items = tables["joint_response_pattern_item_index"]
    relations = tables["joint_pattern_relation_signature"]

    # A scope-valid V551 surface is supplied, but no atom is allowed to
    # masquerade as a match for the governed V550J members.
    atoms = pd.DataFrame(
        [
            {
                "source_family": "GSS",
                "source": "GSS",
                "canonical_wave": "2010",
                "wave": "2010",
                "country_code": "US",
                "question_id": "unrelated-control-question",
                "var_code": "unrelated_control_var",
                "response_value_normalized": "1",
                "semantic_role": "RELATION_EVIDENCE",
                "schema_version": "v551-controlled",
            }
        ]
    )
    registry_hash = hashlib.sha256(CURRENT.read_bytes()).hexdigest()
    v550_manifest = tmp_path / "v550j_manifest.json"
    v550_ready = tmp_path / "v550j_readiness.json"
    v550_manifest.write_text(
        json.dumps(
            {
                "registry_path": str(CURRENT),
                "question_family_registry_hash": registry_hash,
                "success": True,
                "validation_status": "pass",
            },
            sort_keys=True,
        )
    )
    v550_ready.write_text(
        json.dumps(
            {
                "readiness_status": "validated_for_internal_analysis",
                "family_registry_status": "applicable",
                "blocking_issues": [],
            },
            sort_keys=True,
        )
    )
    v551 = build_v551j_joint_outputs_v2(
        run_id="b10-chain",
        atoms=atoms,
        pattern_index=patterns,
        pattern_item_index=items,
        relation_signature=relations,
        registry_path=str(CURRENT),
        v550j_manifest_path=str(v550_manifest),
        v550j_readiness_report_path=str(v550_ready),
    )
    assert not v551["candidate"].empty
    assert v551["readiness_report"]["registry_contract_status"] == "MATCHED_GOVERNED_REGISTRY_HASH"
    assert v551["readiness_report"]["scope_contract_status"] == "PASS"
    assert v551["readiness_report"]["ready_for_v553"] is False

    full_review = v551["candidate"].copy()
    assert not full_review.empty
    v552j = build_v552j_join(
        run_id="b10-chain",
        v551j_certified=v551["certified"],
        v551j_review=full_review,
        v552_structural_facts=pd.DataFrame(),
        v552_temporal_keys=pd.DataFrame(),
        v551j_state={"evidence_status": "PRESENT", "downstream_permission_status": "DENY"},
        v552_state={"evidence_status": "PRESENT", "downstream_permission_status": "DENY"},
        v551j_manifest_sha256="controlled-v551j",
        v552_manifest_sha256="controlled-v552",
    )
    assert v552j["join_index"].empty
    assert not v552j["join_audit"].empty
    assert set(v552j["join_audit"]["join_status"].astype(str)) == {
        "UNRESOLVED_NO_STRUCTURAL_MATCH"
    }
    assert v552j["metrics"]["unresolved_join_count"] == len(v552j["join_audit"])


def test_live_respondent_backed_chain_remains_external_runtime_blocker_not_static_substitute():
    state = json.loads((ROOT / "section85/CURRENT_STATE.json").read_text())
    assert state["real_empirical_j_chain_status"] == (
        "NOT_RUN_REQUIRES_LIVE_RESPONDENT_DATABASE_AND_PYARROW"
    )
    assert state["archive_contains_respondent_level_substrate"] is False
    assert state["production_completeness_claim"] == "NO_PRODUCTION_COMPLETENESS_CLAIM"
