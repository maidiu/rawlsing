#!/usr/bin/env python3
"""W03-A regressions for V550J-001/002/003."""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (
    _enforce_governed_association_lane_authority,
)
from data.ddm_build_copy.ddm_v550j_registry_classifier import AssociationLaneRegistry
from data.ddm_build_copy.ddm_v550j_registry_contract import (
    REGISTRY_AUTHORITY_NOT_APPLICABLE,
    RegistryAuthorityError,
    registry_authority_state,
    require_executable_registry_status,
)

COMPILER_PATH = Path(__file__).with_name("compile_v550j_joint_response_patterns.py")


class _StubRegistry:
    def __init__(self, *, publishability: str) -> None:
        self.publishability = publishability

    def classify_required(self, *, var_code: str, source: str, wave: str, country_code: str):
        assert var_code == "ATTITUDE_X"
        return SimpleNamespace(
            lane="substantive_attitude_association",
            publishability=self.publishability,
            rule_id="TEST-RULE-1",
            match_type="exact",
            authority_source="test_registry",
            authority_status="governed",
        )


class _MissingRuleRegistry:
    def classify_required(self, **kwargs):
        raise RegistryAuthorityError(
            "association_lane_authority_missing",
            "missing governed test rule",
            authority_name="test registry",
        )


def _association_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "associated_var_code": "ATTITUDE_X",
                "association_lane": "substantive_attitude_association",
                "association_lane_publishability": "publishable_lane",
                "association_lane_rule_id": "legacy",
                "association_lane_authority_source": "legacy",
                "association_lane_authority_status": "legacy",
                "association_lane_resolution_type": "semantic_role",
                "association_publication_status": "publishable",
                "association_publication_reason": "legacy hard-coded classifier",
                "would_emit_as_publishable": True,
            }
        ]
    )


def test_v550j_001_threshold_has_no_duplicate_dict_key_and_is_threaded_to_compiler_and_validator() -> None:
    tree = ast.parse(COMPILER_PATH.read_text(encoding="utf-8"))
    duplicate_nodes: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [
            key.value
            for key in node.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        ]
        if keys.count("association_support_threshold") > 1:
            duplicate_nodes.append(node.lineno)
    assert duplicate_nodes == []

    compile_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "compile_v550j_family_tables"
    ]
    assert compile_calls
    for call in compile_calls:
        threshold_kw = next(kw for kw in call.keywords if kw.arg == "association_support_threshold")
        assert isinstance(threshold_kw.value, ast.Name)
        assert threshold_kw.value.id == "association_support_threshold"

    validate_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_validate_v550j_run_outputs"
    ]
    assert validate_calls
    threshold_kw = next(
        kw for kw in validate_calls[-1].keywords if kw.arg == "association_support_threshold"
    )
    assert isinstance(threshold_kw.value, ast.Name)
    assert threshold_kw.value.id == "association_support_threshold"


def test_v550j_002_registry_block_cannot_survive_in_publishable_index() -> None:
    tables = {"joint_pattern_association_index": _association_frame()}
    reconciled = _enforce_governed_association_lane_authority(
        tables,
        registry=_StubRegistry(publishability="blocked_lane"),
        source="GSS",
        wave="2018",
        country_code="US",
    )
    assert reconciled["joint_pattern_association_index"].empty


def test_v550j_002_registry_block_demotes_diagnostic_candidate() -> None:
    tables = {"joint_pattern_association_candidate_trace": _association_frame()}
    reconciled = _enforce_governed_association_lane_authority(
        tables,
        registry=_StubRegistry(publishability="diagnostic_only_lane"),
        source="GSS",
        wave="2018",
        country_code="US",
    )
    row = reconciled["joint_pattern_association_candidate_trace"].iloc[0]
    assert row["association_lane_publishability"] == "diagnostic_only_lane"
    assert row["association_publication_status"] == "blocked_registry_publishability"
    assert bool(row["would_emit_as_publishable"]) is False
    assert row["association_lane_rule_id"] == "TEST-RULE-1"
    assert row["association_lane_resolution_type"] == "exact_registry"


def test_v550j_002_missing_governed_rule_fails_closed() -> None:
    with pytest.raises(RegistryAuthorityError) as excinfo:
        _enforce_governed_association_lane_authority(
            {"joint_pattern_association_index": _association_frame()},
            registry=_MissingRuleRegistry(),
            source="GSS",
            wave="2018",
            country_code="US",
        )
    assert excinfo.value.code == "association_lane_authority_missing"


def test_v550j_002_registry_loader_rejects_missing_publishability(tmp_path: Path) -> None:
    registry_path = tmp_path / "association_lane_registry.yaml"
    registry_path.write_text(
        "rules:\n"
        "  - rule_id: TEST-RULE\n"
        "    source: '*'\n"
        "    country_code: '*'\n"
        "    match_type: exact\n"
        "    var_code: ATTITUDE_X\n"
        "    association_lane: substantive_attitude_association\n",
        encoding="utf-8",
    )
    registry = AssociationLaneRegistry(registry_path)
    with pytest.raises(RegistryAuthorityError) as excinfo:
        registry.load()
    assert excinfo.value.code == "association_lane_registry_rule_incomplete"


def test_v550j_003_draft_family_registry_is_not_executable() -> None:
    with pytest.raises(RegistryAuthorityError) as excinfo:
        require_executable_registry_status(
            "draft",
            authority_name="V550J question-family registry",
            path="question_family_registry.yaml",
        )
    assert excinfo.value.code == "registry_status_not_executable"
    assert excinfo.value.status == "draft"


def test_v550j_003_missing_family_registry_status_is_typed_failure() -> None:
    with pytest.raises(RegistryAuthorityError) as excinfo:
        require_executable_registry_status("", authority_name="V550J question-family registry")
    assert excinfo.value.code == "registry_authority_missing"


def test_v550j_003_no_applicable_family_is_typed_not_applicable() -> None:
    assert registry_authority_state("draft", applicable=False) == REGISTRY_AUTHORITY_NOT_APPLICABLE
