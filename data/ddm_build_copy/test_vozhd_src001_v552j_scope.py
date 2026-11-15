from __future__ import annotations

import pytest

from data.ddm_build_copy.compile_v552j_structural_handoff import _coherent_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError


def _scope(*, country: str, shard: str) -> dict[str, str]:
    return {
        "run_id": "r1",
        "source": "EVS",
        "wave": "1999",
        "country_code": country,
        "shard_id": shard,
    }


def test_v552j_exact_scope_keeps_matching_country_and_shard() -> None:
    joined = _coherent_scope(
        "r1",
        _scope(country="IS", shard="EVS__1999"),
        _scope(country="IS", shard="EVS__1999"),
    )
    assert joined["country_code"] == "IS"
    assert joined["shard_id"] == "EVS__1999"
    assert joined["scope_kind"] == "shard"


def test_v552j_exact_scope_rejects_wrong_shard_even_when_country_matches() -> None:
    with pytest.raises(BoundaryContractError, match="V552J_CROSS_SCOPE_MISMATCH:shard"):
        _coherent_scope(
            "r1",
            _scope(country="IS", shard="EVS__1999"),
            _scope(country="IS", shard="EVS__1999__wrong"),
        )


def test_v552j_exact_scope_rejects_wrong_country() -> None:
    with pytest.raises(BoundaryContractError, match="V552J_CROSS_SCOPE_MISMATCH:country"):
        _coherent_scope(
            "r1",
            _scope(country="IS", shard="EVS__1999"),
            _scope(country="DE", shard="EVS__1999"),
        )


def test_v552j_multi_country_shard_scope_still_requires_exact_shard() -> None:
    joined = _coherent_scope(
        "r1",
        _scope(country="", shard="EVS__2017"),
        _scope(country="", shard="EVS__2017"),
    )
    assert joined["country_code"] == ""
    assert joined["shard_id"] == "EVS__2017"
    assert joined["scope_kind"] == "shard"
