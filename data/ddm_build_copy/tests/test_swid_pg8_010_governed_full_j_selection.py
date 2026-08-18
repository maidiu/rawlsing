from __future__ import annotations

import random

from data.ddm_build_copy.ddm_v550_response_semantics_authority import (
    lookup_governed_response_semantics_contract,
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


def _afro_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = [
        ("mip1", "", "migration", "joint_family_item"),
        ("mip2", "", "migration", "joint_family_item"),
    ]
    rows.extend((code, "institutional_trust", "politics", "relation") for code in sorted(AFRO_R1_BOUND))
    rows.extend((code, "other_relation", "politics", "relation") for code in sorted(AFRO_R1_RUNTIME_DEBT))
    rows.extend((f"struct{i:02d}", "", "demography", "context") for i in range(1, 13))
    return rows


def _legacy_selection(
    rows: list[tuple[str, str, str, str]],
    *,
    seed: int,
    authority: dict[str, object],
) -> list[str]:
    """Frozen pre-PG8-010 sampler for exact joint_mode=off comparison."""
    rng = random.Random(seed)
    selected: list[str] = []
    available = {code.upper(): code for code, *_ in rows}
    if authority.get("applicable"):
        for code in authority.get("candidate_vars") or []:
            code = str(code)
            if code.upper() in available and available[code.upper()] not in selected:
                selected.append(available[code.upper()])
            if len(selected) >= 6:
                break
    relation_rows = [code for code, axis, _, evidence in rows if axis or "relation" in evidence.lower()]
    structural_rows = [code for code, _, domain, _ in rows if domain]
    for pool, target in ((relation_rows, 8), (structural_rows, 6)):
        choices = [code for code in pool if code not in selected]
        rng.shuffle(choices)
        selected.extend(choices[: max(0, min(target, 20 - len(selected)))])
    remaining = [code for code, *_ in rows if code not in selected]
    rng.shuffle(remaining)
    selected.extend(remaining[: max(0, 20 - len(selected))])
    rng.shuffle(selected)
    return selected[:20]


def test_frozen_afro_r1_binding_surface_matches_pg8_runtime_diagnosis() -> None:
    for code in AFRO_R1_BOUND:
        assert lookup_governed_response_semantics_contract("Afrobarometer", "R1", code) is not None
    for code in AFRO_R1_RUNTIME_DEBT:
        assert lookup_governed_response_semantics_contract("Afrobarometer", "R1", code) is None


def test_required_full_j_uses_joint_items_plus_exact_governed_v551_surface() -> None:
    authority = {"applicable": True, "candidate_vars": ["mip1", "mip2"]}
    selected = _select_question_variables_from_rows(
        _afro_rows(),
        family="Afrobarometer",
        wave="R1",
        seed=0,
        authority=authority,
        joint_mode="required",
    )

    assert {"mip1", "mip2"}.issubset(selected)
    assert AFRO_R1_BOUND.issubset(selected)
    assert not (AFRO_R1_RUNTIME_DEBT & set(selected))
    assert set(selected) == {"mip1", "mip2", *AFRO_R1_BOUND}


def test_joint_mode_off_preserves_exact_legacy_20var_sampler(monkeypatch) -> None:
    rows = _afro_rows()
    authority = {"applicable": True, "candidate_vars": ["mip1", "mip2"]}
    seed = 17

    def forbidden_lookup(*_args, **_kwargs):
        raise AssertionError("joint_mode=off must not consult V551 binding authority for slice selection")

    monkeypatch.setattr(
        "data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke.lookup_governed_response_semantics_contract",
        forbidden_lookup,
    )
    selected = _select_question_variables_from_rows(
        rows,
        family="Afrobarometer",
        wave="R1",
        seed=seed,
        authority=authority,
        joint_mode="off",
    )

    assert selected == _legacy_selection(rows, seed=seed, authority=authority)
    assert len(selected) == 20
