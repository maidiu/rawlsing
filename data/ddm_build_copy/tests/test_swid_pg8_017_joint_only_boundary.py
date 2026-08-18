from __future__ import annotations

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (
    _augment_family_questions_from_prepared,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    _base_filter_variables_for_required,
)


GSS_JOINT_VARS = {
    "abany",
    "abdefect",
    "abhlth",
    "abnomore",
    "abrape",
    "absingle",
}


def test_required_base_filter_keeps_only_governed_v551_surface(monkeypatch) -> None:
    selected = [*sorted(GSS_JOINT_VARS), "harmsgrn"]

    def governed_lookup(_family: str, _wave: str, code: str):
        return object() if code == "harmsgrn" else None

    monkeypatch.setattr(
        "data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke.lookup_governed_response_semantics_contract",
        governed_lookup,
    )
    assert _base_filter_variables_for_required("GSS", "2010", selected) == ["harmsgrn"]


def _prepared(*, selected: bool = True, question_id: str = "question_impl.gss.abrape") -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "var_code": "abrape",
                "var_code_norm": "ABRAPE",
                "question_id": question_id,
                "question_text": "Abortion if pregnancy resulted from rape",
                "source": "GSS",
                "wave": "2010",
                "canonical_wave": "2010",
                "joint_configuration_selected": selected,
                "joint_configuration_ids_json": '["JCFG-GSS-ABORTION-CONDITIONS"]',
            },
            {
                "var_code": "abrape",
                "var_code_norm": "ABRAPE",
                "question_id": question_id,
                "question_text": "Abortion if pregnancy resulted from rape",
                "source": "GSS",
                "wave": "2010",
                "canonical_wave": "2010",
                "joint_configuration_selected": selected,
                "joint_configuration_ids_json": '["JCFG-GSS-ABORTION-CONDITIONS"]',
            },
        ]
    )


def _family() -> dict[str, object]:
    return {
        "family_id": "JCFG-GSS-ABORTION-CONDITIONS",
        "item_role_groups": {
            "exception_case": [
                {
                    "var_code": "abrape",
                    "question_implementation_id": "question_impl.gss.abrape",
                    "condition_label": "rape",
                }
            ]
        },
    }


def test_joint_only_metadata_is_completed_from_validated_selected_prepared_rows() -> None:
    out = _augment_family_questions_from_prepared(
        pd.DataFrame(columns=["var_code", "question_id", "source", "wave", "canonical_wave"]),
        _prepared(),
        _family(),
        source="GSS",
        canonical_wave="2010",
    )
    assert len(out) == 1
    assert out.iloc[0]["var_code"] == "ABRAPE"
    assert out.iloc[0]["question_id"] == "question_impl.gss.abrape"
    assert out.iloc[0]["source"] == "GSS"
    assert out.iloc[0]["canonical_wave"] == "2010"
    assert out.iloc[0]["joint_only_metadata_source"] == "validated_prepared_substrate"
    assert not str(out.iloc[0].get("question_use_contract_hash", "")).strip()


def test_existing_quc_row_wins_and_is_not_replaced() -> None:
    quc = pd.DataFrame(
        [{"var_code": "ABRAPE", "question_id": "real-quc", "source": "GSS", "wave": "2010", "canonical_wave": "2010"}]
    )
    out = _augment_family_questions_from_prepared(quc, _prepared(), _family(), source="GSS", canonical_wave="2010")
    assert len(out) == 1
    assert out.iloc[0]["question_id"] == "real-quc"


def test_unselected_prepared_rows_do_not_create_joint_metadata() -> None:
    out = _augment_family_questions_from_prepared(
        pd.DataFrame(columns=["var_code", "question_id", "source", "wave", "canonical_wave"]),
        _prepared(selected=False),
        _family(),
        source="GSS",
        canonical_wave="2010",
    )
    assert out.empty


def test_contradictory_stable_prepared_metadata_fails_closed() -> None:
    frame = _prepared()
    frame.loc[1, "question_id"] = "question_impl.gss.different"
    with pytest.raises(Exception, match="V550J_JOINT_ONLY_METADATA_CONTRADICTION"):
        _augment_family_questions_from_prepared(
            pd.DataFrame(columns=["var_code", "question_id", "source", "wave", "canonical_wave"]),
            frame,
            _family(),
            source="GSS",
            canonical_wave="2010",
        )
