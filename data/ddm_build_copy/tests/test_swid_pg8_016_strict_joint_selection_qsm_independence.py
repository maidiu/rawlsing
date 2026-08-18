from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml

from data.ddm_build_copy.build_determinicity_wave_shard_v550 import (
    _apply_question_filter_exact_first,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    _base_filter_variables_for_required,
    _select_question_variables_from_rows,
)


ROOT = Path(__file__).resolve().parents[3]
GSS_BOUNDED_REGISTRY = ROOT / "section85" / "authority" / "registry_gss.yaml"
EXPECTED_GSS_JOINT_VARS = {
    "abany",
    "abdefect",
    "abhlth",
    "abnomore",
    "abrape",
    "absingle",
}


def _governed_gss_joint_vars() -> list[str]:
    payload = yaml.safe_load(GSS_BOUNDED_REGISTRY.read_text(encoding="utf-8"))
    assert payload["status"] == "governed"
    assert payload["source_family"] == "GSS"
    family = next(
        row
        for row in payload["families"]
        if row["family_id"] == "JCFG-GSS-ABORTION-CONDITIONS"
        and "2010" in {str(value) for value in row.get("eligible_waves", [])}
    )
    values: list[str] = []
    for rows in (family.get("item_role_groups") or {}).values():
        for row in rows or []:
            code = str(row.get("var_code") or "").strip()
            if code and code not in values:
                values.append(code)
    return values


GSS_JOINT_VARS = _governed_gss_joint_vars()


def _gss_qsm_rows() -> list[tuple[str, str, str, str]]:
    # Runtime diagnosis: the strict GSS 2010 QSM slice exposed only harmsgrn,
    # while the bounded J authority owns a separate abortion-condition family.
    return [("harmsgrn", "", "", "")]


def _authority() -> dict[str, object]:
    return {"applicable": True, "candidate_vars": list(GSS_JOINT_VARS)}


def _governed_lookup(_family: str, _wave: str, code: str):
    return object() if code == "harmsgrn" else None


def test_bounded_gss_registry_is_exact_six_and_excludes_draft_abpoor() -> None:
    assert set(GSS_JOINT_VARS) == EXPECTED_GSS_JOINT_VARS
    assert len(GSS_JOINT_VARS) == 6
    assert "abpoor" not in GSS_JOINT_VARS


def test_required_joint_selection_does_not_require_joint_items_to_exist_in_qsm(monkeypatch) -> None:
    monkeypatch.setattr(
        "data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke.lookup_governed_response_semantics_contract",
        _governed_lookup,
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


def test_required_v550_base_filter_excludes_registry_only_joint_items(monkeypatch) -> None:
    monkeypatch.setattr(
        "data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke.lookup_governed_response_semantics_contract",
        _governed_lookup,
    )
    selected = [*GSS_JOINT_VARS, "harmsgrn"]
    assert _base_filter_variables_for_required("GSS", "2010", selected) == ["harmsgrn"]


def test_v550_base_filter_still_fails_closed_for_unknown_identifier() -> None:
    mapping = pd.DataFrame(
        [
            {
                "question_id": "question.impl.gss.harmsgrn",
                "var_code": "harmsgrn",
            }
        ]
    )
    with pytest.raises(RuntimeError, match=r"question filter identifier not found: abrape"):
        _apply_question_filter_exact_first(
            mapping,
            ["abrape"],
            source="GSS",
            wave="2010",
        )


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
