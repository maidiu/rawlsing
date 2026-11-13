"""A-counter hostile regressions against B's source/operation/routing join."""
from __future__ import annotations

from pathlib import Path

import pytest

from rawlsing_next.pre553_source_i02_handoff import SourceI02Refusal
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture


def _multiowner_fixture(tmp_path: Path, routing_state: str):
    return source_fixture(
        tmp_path / "multiowner",
        routing_state=routing_state,
        config_kwargs={
            "duplicate_slot_owner": True,
            "include_slot_owner_set": True,
        },
    )


def test_multiowner_response_coordinate_unknown_routing_refuses(tmp_path):
    fixture = _multiowner_fixture(tmp_path, "ROUTING_UNKNOWN")
    with pytest.raises(
        SourceI02Refusal, match="OPERATION_ROUTING_FATE_MISMATCH"
    ):
        build(tmp_path / "multiowner", fixture, name="unknown.sqlite")


def test_multiowner_response_coordinate_eligible_routing_preserved(tmp_path):
    fixture = _multiowner_fixture(tmp_path, "ELIGIBLE_APPLICABLE")
    handoff = build(tmp_path / "multiowner", fixture, name="eligible.sqlite")
    assert handoff.stats.event_count == fixture["rows"]
    assert handoff.stats.coordinate_count == fixture["rows"] * 2
    assert handoff.census_audit["operation_source_antijoin"][
        "eligible_realized_count"] > 0
