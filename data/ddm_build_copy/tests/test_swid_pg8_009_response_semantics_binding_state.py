from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v550_authority_contract import (
    CERTIFIED,
    REVIEW_REQUIRED,
    derive_question_use_eligibility,
    response_semantics_authority_status,
)
from data.ddm_build_copy.ddm_v550_response_semantics_authority import (
    bind_governed_response_semantics_contracts,
)


def _afro_dememp_live_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source_family": "Afrobarometer",
                "canonical_wave": "R1",
                "var_code": "dememp",
                "is_substantive": True,
                "response_direction": direction,
                "response_intensity": intensity,
                "response_semantics_contract_hash": "",
                "response_semantics_status": "UNRESOLVED_LIVE_BUILD",
                "response_semantics_source": "response_option_map_live_build",
                "response_semantics_authority_status": "",
            }
            for direction, intensity in (
                ("negative", 1.0),
                ("negative", 0.5),
                ("positive", 0.5),
                ("positive", 1.0),
            )
        ]
    )


def test_pr26_governed_binding_state_survives_when_explicit_status_is_not_carried() -> None:
    bound, summary = bind_governed_response_semantics_contracts(
        _afro_dememp_live_rows(),
        live_build=True,
    )
    assert summary["bound_groups"] == 1
    assert summary["unresolved_groups"] == 0
    assert set(bound["response_semantics_status"]) == {"CERTIFIED_GOVERNED_CONTRACT"}
    assert set(bound["response_semantics_authority_status"]) == {"CERTIFIED"}

    # The live V550 harmonization/summary path currently carries the governed
    # status/source/hash triple but not this explicit authority-status column.
    transported = bound.drop(columns=["response_semantics_authority_status"])
    for row in transported.to_dict("records"):
        assert response_semantics_authority_status(row) == CERTIFIED


def test_governed_binding_state_is_enough_for_existing_v551_question_use_gate() -> None:
    bound, _ = bind_governed_response_semantics_contracts(
        _afro_dememp_live_rows(),
        live_build=True,
    )
    semantic = bound.iloc[0].to_dict()
    semantic.pop("response_semantics_authority_status", None)
    result = derive_question_use_eligibility(
        {
            **semantic,
            "semantic_role": "RELATION_EVIDENCE",
            "semantic_role_authority_status": "CERTIFIED",
            "response_topology": "scalar",
            "directionality_authority_status": "CERTIFIED",
            "source_structure_fields_joined": True,
            "source_structure_review_required": False,
            "mapping_status": "complete",
            "relation_axis_id": "institutional_trust",
            "target_entity_id": "government",
            "review_required": False,
            "manual_review_required": False,
            "manual_designation_required": False,
            "authority_review_required": False,
        }
    )
    assert result["response_semantics_authority_status"] == CERTIFIED
    assert result["eligibility_gate_status"] == CERTIFIED
    assert result["allowed_as_v551_relation_evidence"] is True


def test_binding_state_still_requires_source_and_exact_contract_identity() -> None:
    base = {
        "response_semantics_status": "CERTIFIED_GOVERNED_CONTRACT",
        "response_semantics_source": "v550_v551_response_semantics_contract_binding_v1",
        "response_semantics_contract_hash": "governed-hash",
    }
    assert response_semantics_authority_status(base) == CERTIFIED
    assert response_semantics_authority_status({**base, "response_semantics_source": ""}) == REVIEW_REQUIRED
    assert response_semantics_authority_status({**base, "response_semantics_contract_hash": ""}) == REVIEW_REQUIRED
    assert response_semantics_authority_status({**base, "response_semantics_status": "UNRESOLVED_LIVE_BUILD"}) == REVIEW_REQUIRED
