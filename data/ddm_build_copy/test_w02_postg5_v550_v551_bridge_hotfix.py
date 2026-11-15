#!/usr/bin/env python3
"""Post-G5 regressions for the V550 -> V551 bridge applicability hotfix."""
from __future__ import annotations

import json

import pandas as pd

from data.ddm_build_copy.ddm_v550_authority_contract import (
    APPLICABILITY_UNRESOLVED,
    APPLICABLE_BY_AUTHORITY,
    NOT_APPLICABLE_BY_AUTHORITY,
    derive_question_use_eligibility,
)
from data.ddm_build_copy.ddm_v550_question_use import (
    QUESTION_USE_CONTRACT_HASH_COLUMNS,
    _question_use_contract_hash,
    build_question_use_contract,
)
from data.ddm_build_copy.ddm_v550_schema import (
    QUESTION_USE_CONTRACT_SCHEMA,
    V551_BRIDGE_INDEX_SCHEMA,
)
from data.ddm_build_copy.ddm_v550_storage import (
    V550ShardPaths,
    _canonicalize_empty_table_schema,
    write_table,
)
from data.ddm_build_copy.ddm_v551_atoms import validate_v551_bridge_input_contract


def _applicable_row(**overrides):
    row = {
        "semantic_role": "RELATION_EVIDENCE",
        "semantic_role_authority_status": "CERTIFIED",
        "response_semantics_authority_status": "CERTIFIED",
        "response_topology": "scalar",
        "directionality_authority_status": "CERTIFIED",
        "source_structure_fields_joined": True,
        "mapping_status": "complete",
        "relation_axis_id": "institutional_trust",
        "target_entity_id": "government",
        "review_required": False,
    }
    row.update(overrides)
    return row


def test_v551_required_bridge_contract_is_subset_of_v550_schema():
    empty_bridge = pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
    report = validate_v551_bridge_input_contract(empty_bridge)
    assert report["status"] == "PASS"
    assert report["missing_columns"] == []
    assert "directional_applicability_status" in V551_BRIDGE_INDEX_SCHEMA["required_columns"]


def test_schema_limited_serialization_preserves_all_authoritative_applicability_states(tmp_path):
    statuses = [
        APPLICABLE_BY_AUTHORITY,
        NOT_APPLICABLE_BY_AUTHORITY,
        APPLICABILITY_UNRESOLVED,
    ]
    records = []
    for index, status in enumerate(statuses):
        row = {column: "" for column in V551_BRIDGE_INDEX_SCHEMA["required_columns"]}
        row.update(
            run_id="run-hotfix",
            source="Afrobarometer",
            source_family="Afrobarometer",
            wave="R1",
            canonical_wave="R1",
            country_code="LS",
            analysis_scope="country",
            source_table="answer_distribution",
            source_row_hash=f"row-{index}",
            question_id=f"q-{index}",
            var_code=f"v-{index}",
            response_value_normalized=str(index),
            response_family="ordinal_scale",
            directional_applicability_status=status,
            bridge_evidence_lane="relation_evidence",
            is_substantive=True,
            is_missing=False,
            is_special=False,
            response_semantics_contract_hash="semantics-hash",
            semantic_role="RELATION_EVIDENCE",
            semantic_role_authority_status="CERTIFIED",
            response_semantics_authority_status="CERTIFIED",
            directionality_authority_status="CERTIFIED",
            structural_mapping_status="COMPLETE",
            response_option_map_matched=True,
            usable_for_evidence=True,
            allowed_as_v551_relation_evidence=True,
            n_unweighted=10,
        )
        records.append(row)

    serialized = pd.DataFrame.from_records(
        records,
        columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"],
    )
    assert serialized["directional_applicability_status"].tolist() == statuses
    assert validate_v551_bridge_input_contract(serialized)["status"] == "PASS"

    parquet_path = tmp_path / "v551_bridge_index.parquet"
    serialized.to_parquet(parquet_path, index=False)
    reloaded = pd.read_parquet(parquet_path)
    assert reloaded["directional_applicability_status"].tolist() == statuses
    assert validate_v551_bridge_input_contract(reloaded)["status"] == "PASS"


def test_row_level_directional_certification_cannot_manufacture_applicability():
    result = derive_question_use_eligibility(
        _applicable_row(
            directionality_authority_status="",
            directional_certification_status="CERTIFIED",
            current_directional_atom_eligible=True,
            allowed_as_v551_relation_evidence=True,
        )
    )
    assert result["directional_applicability_status"] == APPLICABILITY_UNRESOLVED
    assert result["current_directional_atom_eligible"] is False
    assert result["allowed_as_v551_relation_evidence"] is False


def test_question_use_hash_binds_directional_applicability_status():
    assert "directional_applicability_status" in QUESTION_USE_CONTRACT_HASH_COLUMNS
    base = {column: "" for column in QUESTION_USE_CONTRACT_HASH_COLUMNS}
    applicable = dict(base, directional_applicability_status=APPLICABLE_BY_AUTHORITY)
    not_applicable = dict(base, directional_applicability_status=NOT_APPLICABLE_BY_AUTHORITY)
    unresolved = dict(base, directional_applicability_status=APPLICABILITY_UNRESOLVED)
    hashes = {
        _question_use_contract_hash(applicable),
        _question_use_contract_hash(not_applicable),
        _question_use_contract_hash(unresolved),
    }
    assert len(hashes) == 3


def test_valid_empty_quc_and_bridge_expose_applicability_schema():
    empty_quc = build_question_use_contract(pd.DataFrame())
    empty_bridge = pd.DataFrame.from_records(
        [], columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"]
    )
    assert "directional_applicability_status" in empty_quc.columns
    assert "directional_applicability_status" in empty_bridge.columns
    assert set(QUESTION_USE_CONTRACT_SCHEMA["required_columns"]).issubset(empty_quc.columns)
    assert validate_v551_bridge_input_contract(empty_bridge)["status"] == "PASS"


def test_valid_empty_quc_serialization_and_sidecar_use_canonical_schema(tmp_path):
    fallback = pd.DataFrame(columns=["question_id", "var_code", "semantic_role"])
    canonical = _canonicalize_empty_table_schema(fallback, "question_use_contract")
    assert set(fallback.columns).issubset(canonical.columns)
    assert set(QUESTION_USE_CONTRACT_SCHEMA["required_columns"]).issubset(canonical.columns)
    assert "directional_applicability_status" in canonical.columns

    paths = V550ShardPaths(root=tmp_path / "v550", run_id="run-hotfix", shard_id="shard-hotfix")
    paths.ensure()
    meta = write_table(
        fallback,
        paths=paths,
        table_name="question_use_contract",
        layer="core",
        write_csv=False,
        write_parquet=True,
    )
    reloaded = pd.read_parquet(meta["parquet_path"])
    schema_payload = json.loads(paths.schemas.joinpath("question_use_contract.schema.json").read_text(encoding="utf-8"))
    schema_columns = [row["name"] for row in schema_payload["columns"]]
    assert "directional_applicability_status" in reloaded.columns
    assert "directional_applicability_status" in schema_columns
    assert set(QUESTION_USE_CONTRACT_SCHEMA["required_columns"]).issubset(reloaded.columns)
