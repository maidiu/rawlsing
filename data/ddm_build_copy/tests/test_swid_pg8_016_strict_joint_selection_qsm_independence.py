from __future__ import annotations

from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    _select_question_variables_from_rows,
)


GSS_JOINT_VARS = [
    "abany",
    "abdefect",
    "abhlth",
    "abnomore",
    "abrape",
    "absingle",
]


def _gss_qsm_rows() -> list[tuple[str, str, str, str]]:
    # Runtime diagnosis: the strict GSS 2010 QSM slice exposed only harmsgrn,
    # while the bounded J authority owns a separate abortion-condition family.
    return [("harmsgrn", "", "", "")]


def _authority() -> dict[str, object]:
    return {"applicable": True, "candidate_vars": list(GSS_JOINT_VARS)}


def test_required_joint_selection_does_not_require_joint_items_to_exist_in_qsm(monkeypatch) -> None:
    def governed_lookup(_family: str, _wave: str, code: str):
        return object() if code == "harmsgrn" else None

    monkeypatch.setattr(
        "data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke.lookup_governed_response_semantics_contract",
        governed_lookup,
    )

    selected = _select_question_variables_from_rows(
        _gss_qsm_rows(),
        family="GSS",
        wave="2010",
        seed=4,
        authority=_authority(),
        joint_mode="required",
    )

    assert set(GSS_JOINT_VARS).issubset(selected)
    assert "harmsgrn" in selected
    assert len(selected) == 7


def test_nonrequired_sampler_keeps_legacy_qsm_availability_gate() -> None:
    selected = _select_question_variables_from_rows(
        _gss_qsm_rows(),
        family="GSS",
        wave="2010",
        seed=4,
        authority=_authority(),
        joint_mode="off",
    )

    assert selected == ["harmsgrn"]
    assert not (set(GSS_JOINT_VARS) & set(selected))
