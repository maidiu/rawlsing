"""A-counter hostile regressions against B's source/operation/routing join."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from rawlsing_next.pre553_r157_projection_adapter import SourceConfig

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

def test_partial_unknown_routing_is_typed_hold_not_false_positive(tmp_path):
    fixture = source_fixture(tmp_path / "partial")
    document = deepcopy(fixture["document"])
    base = document["routing"][0]
    document["routing"] = [
        {**base, "row_selector": [1, 2, 3], "typed_state": "ELIGIBLE_APPLICABLE"},
        {**base, "row_selector": [4, 5], "typed_state": "ROUTING_UNKNOWN"},
    ]
    handoff = build(
        tmp_path / "partial", fixture, name="partial.sqlite",
        config=SourceConfig(document),
    )
    rows = [
        row for row in handoff.operation_fates
        if row["routing_unresolved_keys"]
    ]
    assert rows
    for row in rows:
        assert row["disposition"] != "ELIGIBLE" or not row["source_realized"]
        assert row["operation_source_state"] in {
            "ELIGIBLE_TYPED_HOLD", "HELD_OR_UNKNOWN_SOURCE_STATE",
        }
