"""Q2 B-role source/operation/fate anti-join and no-drop courts."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

import rawlsing_next.pre553_source_i02_handoff as handoff_module
from rawlsing_next.pre553_source_i02_handoff import (
    SourceI02Hold,
    SourceI02Refusal,
)
from rawlsing_next.tests.test_pyat960_s1e_support import (
    build,
    orphan_slot,
    source_fixture,
)
from rawlsing_next.tests.test_universal_grammar import _occurrence


def _forbid_source(monkeypatch):
    called = []

    def forbidden(*args, **kwargs):
        called.append((args, kwargs))
        raise AssertionError("source opened after pre-source refusal")

    monkeypatch.setattr(handoff_module, "decode_sav", forbidden)
    monkeypatch.setattr(handoff_module, "decode_dta", forbidden)
    return called


def test_s1e_eligible_operation_on_unprojected_slot_refuses_before_source(
    tmp_path, monkeypatch
):
    fixture = source_fixture(
        tmp_path / "orphan-eligible",
        extra_physical_slots=(orphan_slot(),),
        inventory_occurrences=(
            _occurrence("q101"),
            _occurrence("country"),
            _occurrence("orphan"),
        ),
    )
    called = _forbid_source(monkeypatch)
    target = tmp_path / "orphan-eligible" / "out.sqlite"
    with pytest.raises(
        SourceI02Refusal, match="ELIGIBLE_OPERATION_TARGET_NOT_PROJECTED"
    ):
        build(
            tmp_path / "orphan-eligible",
            fixture,
            name=target.name,
        )
    assert called == []
    assert target.exists() is False


def test_s1e_held_unprojected_operation_is_typed_not_silently_positive(
    tmp_path,
):
    fixture = source_fixture(
        tmp_path / "orphan-held",
        extra_physical_slots=(orphan_slot(),),
        inventory_occurrences=(
            _occurrence("q101"),
            _occurrence("country"),
            _occurrence("orphan", route_state="UNKNOWN"),
        ),
    )
    handoff = build(tmp_path / "orphan-held", fixture, name="held.sqlite")
    audit = handoff.census_audit["operation_source_antijoin"]
    assert audit["held_unrealized_count"] > 0
    assert audit["unrealized_eligible_count"] == 0
    assert audit["native_first_reader_state"].startswith("HOLD_DEPENDENCY")
    unrealized = [
        row for row in handoff.operation_fates
        if row["disposition"] != "ELIGIBLE" and not row["source_realized"]
    ]
    assert unrealized
    for row in unrealized:
        assert row["operation_source_state"] == "HELD_OR_UNKNOWN_SOURCE_STATE"
        assert row["native_first_reader_state"].startswith("HOLD_DEPENDENCY")
        assert row["issued_receipt_refs"] == ()
    assert Path(handoff.destination).is_file()


@pytest.mark.parametrize("routing_state", ("ROUTING_UNKNOWN", "NOT_ASKED"))
def test_s1e_eligible_response_with_no_eligible_routing_refuses(
    tmp_path, monkeypatch, routing_state
):
    fixture = source_fixture(
        tmp_path / "routing",
        routing_state=routing_state,
    )
    called = _forbid_source(monkeypatch)
    target = tmp_path / "routing" / "out.sqlite"
    with pytest.raises(
        SourceI02Refusal, match="OPERATION_ROUTING_FATE_MISMATCH"
    ):
        build(tmp_path / "routing", fixture, name=target.name)
    assert called == []
    assert target.exists() is False


def test_s1e_unrealized_occurrence_dimension_is_typed_hold(
    tmp_path, monkeypatch
):
    fixture = source_fixture(
        tmp_path / "option",
        inventory_occurrences=(
            _occurrence("q101", option_id="9"),
            _occurrence("country"),
        ),
    )
    called = _forbid_source(monkeypatch)
    target = tmp_path / "option" / "out.sqlite"
    with pytest.raises(
        SourceI02Hold, match="OPERATION_OCCURRENCE_DIMENSION_NOT_REALIZED"
    ):
        build(tmp_path / "option", fixture, name=target.name)
    assert called == []
    assert target.exists() is False


def test_s1e_realized_occurrence_dimension_is_accepted(tmp_path):
    fixture = source_fixture(
        tmp_path / "option-ok",
        inventory_occurrences=(
            _occurrence("q101", option_id="1"),
            _occurrence("country"),
        ),
    )
    handoff = build(tmp_path / "option-ok", fixture, name="ok.sqlite")
    audit = handoff.census_audit["operation_source_antijoin"]
    assert audit["eligible_operation_count"] == audit["eligible_realized_count"]
    q101_rows = [
        realization
        for row in handoff.operation_fates
        for realization in row["source_realization"]
        if realization["item_id"] == "q101"
    ]
    assert q101_rows
    assert all(realization["occurrence_realized"] for realization in q101_rows)


def test_s1e_operation_fates_are_realization_not_labels(tmp_path):
    fixture = source_fixture(tmp_path / "realization")
    handoff = build(tmp_path / "realization", fixture, name="real.sqlite")
    audit = handoff.census_audit["operation_source_antijoin"]
    assert audit["operation_count"] == len(fixture["frontier"].operations)
    assert audit["eligible_realized_count"] == audit["eligible_operation_count"]
    assert audit["source_realized_operation_count"] > 0
    eligible = [
        row for row in handoff.operation_fates
        if row["disposition"] == "ELIGIBLE"
    ]
    assert eligible
    for row in eligible:
        assert row["source_realized"] is True
        assert row["source_realization"]
        assert any(
            realization["emitted"] > 0
            for realization in row["source_realization"]
        )
        preimage = row["source_preimage"]
        assert preimage["operation_hash_matches"] is True
        assert preimage["source_authority_ref"]
        assert preimage["source_decision_ref"]
        assert preimage["science_eligibility_decision_ref"]
        assert preimage["u_item_ref"]
        assert row["native_first_reader_state"].startswith("HOLD_DEPENDENCY")
        assert row["issued_receipt_refs"] == ()


def test_s1e_returned_operation_fates_preserve_measure_and_weight_fates(tmp_path):
    """G5 defect 2: the returned ledger, not just the frontier, keeps measure."""
    fixture = source_fixture(
        tmp_path / "measure-fates",
        values=(0.0, 1.0, 0.0, 1.0, 0.0),
    )
    handoff = build(tmp_path / "measure-fates", fixture, name="fates.sqlite")
    rows = tuple(handoff.operation_fates)
    assert Counter(row["measure_kind"] for row in rows) == {
        "SAMPLE": 16,
        "POPULATION": 6,
    }
    for row in rows:
        measure = row["source_preimage"]["measure"]
        assert row["measure_kind"] == measure["measure_kind"]
        assert row["measure_id"] == measure["measure_id"]
        assert row["weight_ref"] == measure["weight_ref"]
        assert row["estimand"] == measure["estimand"]
        assert row["design_ref"] == measure["design_ref"]
        assert row["variance_policy"] == measure["variance_policy"]
        preimage = row["source_preimage"]
        assert preimage["source_sha256"] == handoff.source_sha256
        assert preimage["operation_hash"] == row["operation_hash"]
        assert preimage["operation_hash_matches"] is True
        assert preimage["source_id"]
        assert preimage["wave"]
        assert preimage["edition"]
        assert "instrument_ref" in preimage
        assert "universe_scope" in preimage

    sample = [row for row in rows if row["measure_kind"] == "SAMPLE"]
    population = [row for row in rows if row["measure_kind"] == "POPULATION"]
    assert len(sample) == 16
    assert len(population) == 6
    assert {row["disposition"] for row in population} == {"HELD"}
    assert {row["disposition"] for row in sample} == {"ELIGIBLE", "HELD"}
    # The fixture truth: RAW sample operations remain valid without invented
    # weights; population estimators remain held with exact owner fields.
    assert all(row["weight_ref"] is None for row in sample)
    assert all(row["weight_ref"] is None for row in population)
    assert all(row["estimand"] for row in sample)
    assert all(row["estimand"] for row in population)
    assert all(row["variance_policy"] for row in sample)
    assert all(row["design_ref"] is None for row in sample)
    assert all(row["design_ref"] is None for row in population)
