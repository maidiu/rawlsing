from __future__ import annotations

import json

import pandas as pd

from data.ddm_build_copy.ddm_v551_atoms import _producer_lineage
from data.ddm_build_copy.ddm_v550_bridge import (
    V551_BRIDGE_INDEX_SCHEMA,
    _bridge_additional_fields,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    _select_question_variables_from_rows,
)


AFRO_R1_BOUND = {
    "dememp",
    "pfeerd",
    "pfgmp",
    "pfpcrm",
    "pfpsaf",
    "pfrass",
}
AFRO_R1_RUNTIME_DEBT = {
    "dmpext",
    "scint",
    "pfpcr5",
    "rejdic",
    "rejmil",
    "rejtrd",
}


def _duplicate_heavy_afro_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = [
        ("mip1", "", "migration", "joint_family_item"),
        ("mip2", "", "migration", "joint_family_item"),
    ]
    # QSM DISTINCT is across structural columns, not var_code alone.  Repeated
    # governed varcodes must therefore consume only one strict-canary slot.
    for code in ["dememp", "pfeerd", "pfpcrm", "pfpsaf", "pfrass"]:
        for index in range(6):
            rows.append((code, f"axis_{index}", "politics", "relation"))
    rows.append(("pfgmp", "axis_only", "politics", "relation"))
    rows.extend((code, "other_relation", "politics", "relation") for code in sorted(AFRO_R1_RUNTIME_DEBT))
    return rows


def _bridge_fields(contract: dict[str, object], row: dict[str, object] | None = None) -> dict[str, object]:
    return _bridge_additional_fields(
        row=row or {},
        question_contract_row=contract,
        wave="R1",
        row_hash="source-row-hash",
        response_raw="1",
        response_normalized="1",
        support_status="sufficient_support",
        support_companions={},
        direct_relation_table=True,
        empirical_object_type="answer_distribution",
        semantic_role="RELATION_EVIDENCE",
        bridge_evidence_lane="direct_relation_response",
        n_respondents=100,
    )


def test_required_selection_dedupes_qsm_rows_before_twenty_slot_cap() -> None:
    selected = _select_question_variables_from_rows(
        _duplicate_heavy_afro_rows(),
        family="Afrobarometer",
        wave="R1",
        seed=2,
        authority={"applicable": True, "candidate_vars": ["mip1", "mip2"]},
        joint_mode="required",
    )

    assert {"mip1", "mip2"}.issubset(selected)
    assert AFRO_R1_BOUND.issubset(selected)
    assert not (AFRO_R1_RUNTIME_DEBT & set(selected))
    assert len(selected) == len(set(selected))
    assert set(selected) == {"mip1", "mip2", *AFRO_R1_BOUND}


def test_bridge_schema_preserves_existing_quc_row_hash_for_v551_lineage() -> None:
    assert "question_use_contract_hash" in V551_BRIDGE_INDEX_SCHEMA["required_columns"]
    frame = pd.DataFrame.from_records(
        [{"question_use_contract_hash": "quc-row-hash"}],
        columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"],
    )
    assert frame.loc[0, "question_use_contract_hash"] == "quc-row-hash"
    assert _producer_lineage(frame.iloc[0].to_dict()) == (
        "quc-row-hash",
        "",
        "PRODUCER_ROW_HASH_ONLY",
    )


def test_matched_quc_hash_overrides_stale_empirical_copy_with_audit() -> None:
    fields = _bridge_fields(
        {
            "question_use_contract_hash": "governed-quc-hash",
            "review_required": True,
        },
        row={"question_use_contract_hash": "stale-empirical-hash"},
    )
    assert fields["question_use_contract_hash"] == "governed-quc-hash"
    conflicts = json.loads(str(fields["authority_merge_conflicts"]))
    assert any(
        conflict["field"] == "question_use_contract_hash"
        and conflict["candidate_value"] == "stale-empirical-hash"
        and conflict["quc_value"] == "governed-quc-hash"
        for conflict in conflicts
    )


def test_generic_quc_review_is_not_recast_as_manual_review() -> None:
    fields = _bridge_fields(
        {
            "review_required": True,
            "question_use_contract_hash": "quc-row-hash",
            "itinerary_manual_designation_required": False,
            "disallowed_reason": "semantic_role_authority_not_certified",
        }
    )
    assert fields["manual_review_flag"] is False


def test_unresolved_itinerary_manual_gate_remains_fail_closed() -> None:
    fields = _bridge_fields(
        {
            "review_required": True,
            "itinerary_manual_designation_required": True,
            "disallowed_reason": "wave_itinerary_manual_designation_required",
        }
    )
    assert fields["manual_review_flag"] is True
    assert fields["manual_review_reason"] == "wave_itinerary_manual_designation_required"


def test_resolved_itinerary_flag_does_not_resurrect_manual_blocker() -> None:
    fields = _bridge_fields(
        {
            "review_required": True,
            "itinerary_manual_designation_required": True,
            "disallowed_reason": "",
        }
    )
    assert fields["manual_review_flag"] is False


def test_explicit_manual_review_authority_remains_blocking() -> None:
    fields = _bridge_fields(
        {
            "review_required": False,
            "manual_review_required": True,
            "manual_review_reason": "explicit_authority_review",
        }
    )
    assert fields["manual_review_flag"] is True
    assert fields["manual_review_reason"] == "explicit_authority_review"
