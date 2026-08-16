from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "section85/code/section85_typed_state.py"
BOUNDED = ROOT / "section85/code/run_bounded_nine_v550j_v551j_v552j.py"
DIAGNOSTIC = ROOT / "section85/code/run_section85_diagnostic_smoke_matrix.py"
AUTHORITY = ROOT / "section85/authority/section85_binding_authority.json"
TYPED_CONTRACT = ROOT / "section85/authority/section85_typed_stage_contract.json"


def load_helper():
    spec = importlib.util.spec_from_file_location("section85_typed_state", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def artifact(name: str, rows: int) -> dict:
    return {
        "artifact": name,
        "path": f"{name}.parquet",
        "artifact_kind": "canonical",
        "row_count": rows,
        "artifact_file_sha256": "a" * 64,
        "logical_content_sha256": "b" * 64,
        "schema_version": "v3.0",
    }


def v551_manifest(*, evidence: str, permission: str, candidates: int, promotable: int, atoms: int) -> dict:
    return {
        "contract_version": "rawlsing_pipeline_boundary_v1",
        "boundary_contract_version": "rawlsing_pipeline_boundary_v1",
        "producer_run_id": "run-a",
        "run_id": "run-a",
        "source": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "shard_id": "",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
        "run_integrity_status": "PASS",
        "evidence_status": evidence,
        "downstream_permission_status": permission,
        "candidate_count": candidates,
        "promotable_candidate_count": promotable,
        "nonpromotable_candidate_count": candidates - promotable,
        "atom_count": atoms,
        "canonical_artifact_names": [
            "directional_candidate_adjudication",
            "relation_evidence_atoms",
            "directional_distribution_coverage",
        ],
        "artifacts": [
            artifact("directional_candidate_adjudication", candidates),
            artifact("relation_evidence_atoms", atoms),
            artifact("directional_distribution_coverage", 0 if candidates == 0 else 1),
        ],
    }


def test_v551_zero_promotable_repair_debt_keeps_integrity_pass() -> None:
    helper = load_helper()
    result = helper.validate_v551_manifest_contract(
        v551_manifest(
            evidence="APPLICABLE_UNRESOLVED",
            permission="DENY",
            candidates=3,
            promotable=0,
            atoms=0,
        )
    )
    assert result["integrity_pass"] is True
    assert result["operation_permitted"] is False
    assert result["canonical_artifacts"]["relation_evidence_atoms"]["row_count"] == 0
    assert result["atom_row_count_is_integrity_gate"] is False


def test_v551_no_applicable_evidence_keeps_integrity_pass_with_zero_atoms() -> None:
    helper = load_helper()
    result = helper.validate_v551_manifest_contract(
        v551_manifest(
            evidence="NOT_APPLICABLE",
            permission="NOT_APPLICABLE",
            candidates=0,
            promotable=0,
            atoms=0,
        )
    )
    assert result["integrity_pass"] is True
    assert result["evidence_status"] == "NOT_APPLICABLE"
    assert result["operation_permitted"] is False


def test_v551_requires_producer_declared_artifact_file_hash() -> None:
    helper = load_helper()
    payload = v551_manifest(
        evidence="PRESENT",
        permission="ALLOW",
        candidates=1,
        promotable=1,
        atoms=1,
    )
    payload["artifacts"][1].pop("artifact_file_sha256")
    with pytest.raises(helper.Section85TypedStateError, match="ARTIFACT_FILE_SHA256_INVALID"):
        helper.validate_v551_manifest_contract(payload)


def test_nonempty_legacy_v551j_ready_boolean_is_not_authoritative() -> None:
    helper = load_helper()
    gate = helper.typed_stage_gate(
        {"ready_for_v552j_joint_evidence": True, "certified_packet_count": 5},
        stage="v551j",
    )
    assert gate["typed_contract_valid"] is False
    assert gate["integrity_pass"] is False
    assert gate["operation_permitted"] is False


def test_nonempty_blocked_v552j_document_never_passes_typed_gate() -> None:
    helper = load_helper()
    gate = helper.typed_stage_gate(
        {"status": "BLOCKED_V552J_INPUT_INVALID", "blocking_issues": ["bad input"]},
        stage="v552j",
    )
    assert gate["typed_contract_valid"] is False
    assert gate["integrity_pass"] is False
    assert gate["operation_permitted"] is False


def test_typed_v552j_no_evidence_can_pass_integrity_without_operation_permission() -> None:
    helper = load_helper()
    gate = helper.typed_stage_gate(
        {
            "contract_version": "rawlsing_pipeline_boundary_v1",
            "run_integrity_status": "PASS",
            "evidence_status": "NOT_APPLICABLE",
            "downstream_permission_status": "NOT_APPLICABLE",
        },
        stage="v552j",
    )
    assert gate["typed_contract_valid"] is True
    assert gate["integrity_pass"] is True
    assert gate["operation_permitted"] is False
    assert gate["valid_nonpresent_evidence_state"] is True


def test_section85_authority_replaces_nonzero_atom_rule_with_typed_contract() -> None:
    binding = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    typed = json.loads(TYPED_CONTRACT.read_text(encoding="utf-8"))
    assert binding["typed_stage_contract"] == "section85_typed_stage_contract.json"
    assert binding["artifact_authority_csv_role"] == "historical_observation_ledger_only_not_readiness_authority"
    assert binding["historical_artifact_ledger_readiness_rules_executable"] is False
    assert typed["global_rules"]["row_count_nonzero_is_run_integrity"] is False
    assert typed["stage_contracts"]["v551"]["atom_row_count_is_integrity_gate"] is False
    assert typed["stage_contracts"]["v551"]["status"] == "ACTIVE_G2_FROZEN"
    assert typed["stage_contracts"]["v551j"]["status"] == "AWAITING_G3B_PRODUCER_HOOK"
    assert typed["stage_contracts"]["v552j"]["status"] == "AWAITING_G4_PRODUCER_HOOK"


def test_active_section85_runners_do_not_gate_on_legacy_v551j_boolean_or_nonempty_v552j_json() -> None:
    bounded = BOUNDED.read_text(encoding="utf-8")
    diagnostic = DIAGNOSTIC.read_text(encoding="utf-8")
    assert 'get("ready_for_v552j_joint_evidence")' not in bounded
    assert "bool(v552j_ready)" not in bounded
    assert 'get("ready_for_v552j_joint_evidence")' not in diagnostic
