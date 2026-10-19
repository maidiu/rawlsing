"""C4 clock discipline: observation/effective/publication/as-of stay distinct;
no future rule or evidence may enter an earlier historical comparison."""
from __future__ import annotations

import json

import pytest

import ee1_fixtures as F
import ee1_world
from ee1_historical_consumer import accepted_epoch_facts, archival_comparison
from ee1_temporal_owner import clock_gate

W = ee1_world.W
from product.world import SelectedSnapshot
from rawlsing_next.pre553_empirical_objects import semantic_hash


def test_epoch_selection_excludes_future_rule():
    facts, _ = accepted_epoch_facts()
    assert "2027-06-01" not in facts["E1"]["publication_clocks"]
    assert "2027-01-01" not in facts["E1"]["effective_clocks"]
    assert "2027-06-01" in facts["E2"]["publication_clocks"]
    assert "2027-01-01" in facts["E2"]["effective_clocks"]
    assert facts["E1"]["fee_publication"] == "2026-03-01"
    assert facts["E2"]["fee_publication"] == "2027-06-01"


def test_future_rule_at_historical_asof_typed():
    future = clock_gate(F.future_rule()[1], F.ASOF)
    assert future["state"] == "FUTURE_RULE_AT_HISTORICAL_AS_OF"
    assert future["rule_publication"] == "2027-06-01"
    control = clock_gate(F.comparable_pair()[1], F.ASOF)
    assert control["state"] == "CLOCK_OK"


def test_future_evidence_at_historical_asof_typed():
    period = F.future_evidence()[1]
    result = clock_gate(period, F.ASOF)
    assert result["state"] == "FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF"


def test_observation_after_asof_typed():
    period = F.observation_after_asof()[1]
    result = clock_gate(period, F.ASOF_LATE)
    assert result["state"] == "OBSERVATION_AFTER_AS_OF"


def test_actual_adapter_refuses_forced_future_rule_snapshot():
    adapter = W.make_adapter()
    request = W.make_request(W.E1)
    e1_snapshot = adapter.build_snapshot(request)
    e2_snapshot = W.make_adapter().build_snapshot(W.make_request(W.E2))
    material = json.loads(json.dumps(e1_snapshot.material))
    material["fields"]["training_fee"] = json.loads(
        json.dumps(e2_snapshot.material["fields"]["training_fee"]))
    tampered = SelectedSnapshot(material, semantic_hash(material))
    with pytest.raises(ValueError) as error:
        adapter.accept(request, tampered)
    assert "UNREGISTERED_SELECTED_SNAPSHOT" in str(error.value)


def test_archival_receipt_is_archival_only_and_product_marks_it():
    facts, served = accepted_epoch_facts()
    adapters = served[2]
    record = adapters[0].historical_receipt(facts["E1"]["receipt_hash"])
    assert record["archival_only"] is True
    assert record["fresh_use_authorized"] is False
    product = archival_comparison({"state": "COMPARABLE_PROBE_ONLY"},
                                  epochs=(facts, served))
    assert product["comparison_state"] == \
        "ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE"
    assert product["archival"] == {"archival_only": True,
                                   "fresh_use_authorized": False}
    assert product["archival_receipt"]["receipt_hash_removed"] is True
