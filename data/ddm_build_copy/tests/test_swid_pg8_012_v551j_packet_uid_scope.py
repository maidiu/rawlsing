from __future__ import annotations

import json

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_v551j_packets import (
    _v2_match_atoms_for_item,
    validate_governed_input_scope,
)


AFRO_SOURCE_UID = "sf_afrobarometer_v1"
AFRO_R1_WAVE_UID = "wv_afrobarometer_r1_v1"


def _pattern(*, country: str = "LS") -> dict[str, object]:
    return {
        "source": "Afrobarometer",
        "source_family": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "source_family_uid": AFRO_SOURCE_UID,
        "wave_uid": AFRO_R1_WAVE_UID,
        "country_code": country,
        "pattern_id": "pattern-1",
        "family_id": "family-1",
    }


def _item() -> dict[str, object]:
    return {
        "question_id": "q-dememp",
        "var_code": "dememp",
        "response_value_normalized": "1",
        "semantic_response_role": "support",
        "v551_evidence_role": "RELATION_EVIDENCE",
    }


def _atoms(
    *,
    canonical_wave: str = "ROUND1",
    source: str = "Afrobarometer",
    source_family_uid: str = AFRO_SOURCE_UID,
    wave_uid: str = AFRO_R1_WAVE_UID,
    country: str = "LS",
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source": source,
                "source_family": source,
                "wave": canonical_wave,
                "canonical_wave": canonical_wave,
                "source_family_uid": source_family_uid,
                "wave_uid": wave_uid,
                "country_code": country,
                "question_id": "q-dememp",
                "var_code": "dememp",
                "response_value_normalized": "1",
                "atom_id": "atom-1",
                "atom_contract_hash": "atom-contract-1",
                "response_semantics_contract_hash": "response-contract-1",
                "semantic_response_role": "support",
            }
        ]
    )


def _scope_inputs(*, atom_country: str = "LS") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    atoms = _atoms(country=atom_country)
    pattern_index = pd.DataFrame([_pattern()])
    pattern_items = pd.DataFrame([{"pattern_id": "pattern-1", "item_order": 1}])
    relation_signatures = pd.DataFrame([{"pattern_id": "pattern-1", "relation_signature": "sig"}])
    return atoms, pattern_index, pattern_items, relation_signatures


def test_atom_match_accepts_sanctioned_wave_alias_under_exact_uid_scope() -> None:
    status, basis, matched, reasons = _v2_match_atoms_for_item(_item(), _atoms(), _pattern())

    assert status == "MATCHED_EXACT_V551_ATOM"
    assert basis.startswith("exact_uid_scope+")
    assert len(matched) == 1
    assert matched.iloc[0]["canonical_wave"] == "ROUND1"
    assert matched.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
    assert reasons == []


def test_atom_match_rejects_wrong_declared_uid() -> None:
    with pytest.raises(RuntimeError, match="BLOCKED_V551J_V551_ATOM_IDENTITY"):
        _v2_match_atoms_for_item(
            _item(),
            _atoms(wave_uid="wv_deliberately_wrong_for_pg8_012"),
            _pattern(),
        )


def test_atom_match_rejects_contradictory_label_even_with_expected_uid() -> None:
    with pytest.raises(RuntimeError, match="BLOCKED_V551J_V551_ATOM_IDENTITY"):
        _v2_match_atoms_for_item(
            _item(),
            _atoms(source="EVS", canonical_wave="1981"),
            _pattern(),
        )


def test_scope_audit_accepts_alias_without_rewriting_historical_labels() -> None:
    atoms, pattern_index, pattern_items, relation_signatures = _scope_inputs()

    audit, issues = validate_governed_input_scope(
        run_id="run-1",
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_items=pattern_items,
        relation_signatures=relation_signatures,
        expected_source="Afrobarometer",
        expected_wave="R1",
        expected_country="LS",
    )

    assert issues == []
    assert set(audit["scope_contract_status"]) == {"PASS"}
    by_artifact = {row["artifact_name"]: row for row in audit.to_dict("records")}
    assert json.loads(by_artifact["v551_atoms"]["canonical_wave_values_json"]) == ["ROUND1"]
    assert json.loads(by_artifact["v550j_pattern_index"]["canonical_wave_values_json"]) == ["R1"]
    assert atoms.iloc[0]["canonical_wave"] == "ROUND1"
    assert pattern_index.iloc[0]["canonical_wave"] == "R1"


def test_scope_audit_keeps_country_exact() -> None:
    atoms, pattern_index, pattern_items, relation_signatures = _scope_inputs(atom_country="ZA")

    audit, issues = validate_governed_input_scope(
        run_id="run-1",
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_items=pattern_items,
        relation_signatures=relation_signatures,
        expected_source="Afrobarometer",
        expected_wave="R1",
        expected_country="LS",
    )

    assert "scope_contract_mismatch" in issues
    atom_audit = audit[audit["artifact_name"].eq("v551_atoms")].iloc[0]
    assert atom_audit["scope_contract_status"] == "FAIL_SCOPE_MISMATCH"


def test_scope_audit_rejects_uid_label_contradiction() -> None:
    atoms, pattern_index, pattern_items, relation_signatures = _scope_inputs()
    atoms.loc[:, "source"] = "EVS"
    atoms.loc[:, "source_family"] = "EVS"
    atoms.loc[:, "wave"] = "1981"
    atoms.loc[:, "canonical_wave"] = "1981"

    audit, issues = validate_governed_input_scope(
        run_id="run-1",
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_items=pattern_items,
        relation_signatures=relation_signatures,
        expected_source="Afrobarometer",
        expected_wave="R1",
        expected_country="LS",
    )

    assert "scope_contract_mismatch" in issues
    atom_audit = audit[audit["artifact_name"].eq("v551_atoms")].iloc[0]
    assert atom_audit["scope_contract_status"] == "FAIL_SCOPE_MISMATCH"
