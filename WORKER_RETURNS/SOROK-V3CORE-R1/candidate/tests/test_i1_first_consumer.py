from __future__ import annotations

from pathlib import Path

import pytest

from v3core_adapter.contracts import ClockDomain, Status
from v3core_adapter.i1_consumer import project_actual_market_event
from v3core_adapter.ledger import HistoricalProjection
from v3core_adapter.quarantine import forbidden_default_reasons


def test_i1_actual_offscreen_market_event_changes_historical_material_projection(
    tmp_path: Path,
) -> None:
    consumer_root = tmp_path / "i1-consumer"
    ledger = tmp_path / "v3core-projection.json"
    result = project_actual_market_event(consumer_root, projection_path=ledger)
    assert result.status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert result.source_clock_domain == ClockDomain.CURRENT_C12_ACTOR_WORLD
    assert result.source_clock == 40
    assert result.cash_before == 54.0
    assert result.cash_after == 56.0
    assert result.completed_units_before == 3.0
    assert result.completed_units_after == 4.0
    assert result.position_before == "workshop"
    assert result.position_after == "market"
    assert result.material_index_before == pytest.approx(11.3)
    assert result.material_index_after == pytest.approx(11.6)
    assert result.material_index_delta == pytest.approx(0.3)
    assert result.state_hash_before != result.state_hash_after
    assert result.year_record is not None
    assert result.event_id in result.year_record.source_event_ids
    assert result.canonical_c9_claimed is False
    assert result.rival_store_created is False
    assert result.c12_verify_before["ok"] is True
    assert result.c12_verify_after["ok"] is True
    assert result.c12_verify_before["counts"] == result.c12_verify_after["counts"]
    assert result.c12_verify_after["authenticity"]["code"] == "OWNER_ANCHOR_REQUIRED"
    assert ledger.exists()
    loaded = HistoricalProjection.load(ledger)
    assert loaded.state_hash() == result.state_hash_after
    assert loaded.state.capacity.money == 56.0
    assert loaded.material_facts["completed_units"] == 4.0
    assert loaded.material_facts["position"] == "market"
    assert forbidden_default_reasons(loaded.state) == []


def test_i1_consumer_does_not_manufacture_identity_or_class_traits(tmp_path: Path) -> None:
    result = project_actual_market_event(tmp_path / "i1-two")
    assert result.year_result.committed is True
    details = result.year_record.event_dispositions[0].details
    assert details["event_kind"] == "OFFSCREEN_REPAIR"
    assert details["response_kind"] == "PERFORMED_OFFSCREEN_WORK"
    assert not any(
        token in str(details).lower()
        for token in ("class_origin", "ethnicity", "religion", "enneagram", "wound", "personality_type")
    )
