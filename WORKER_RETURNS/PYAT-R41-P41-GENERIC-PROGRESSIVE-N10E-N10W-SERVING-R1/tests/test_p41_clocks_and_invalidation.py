"""P41 clocks, currentness, selective invalidation and archival serving."""
from __future__ import annotations

import pytest

from fixture import prepare, ref
from p41_service import P41Service


def test_publication_boundary_selects_rule_vintage():
    service = P41Service()
    service.publish_rule_revision(
        "training_fee", 6, effective_from="2027-01-01",
        effective_to="2028-01-01", publication="2027-06-01", revision=2)
    early = service.progressive(
        snapshot=service.current_clock_snapshot("2026-06-01", "2026-04-15"))
    late = service.progressive(
        snapshot=service.current_clock_snapshot("2027-09-01", "2027-09-01"))
    assert early["n9_world"]["rules"]["training_fee"]["value"] == 2
    assert early["n9_world"]["rules"]["training_fee"]["publication"] == "2026-03-01"
    assert early["structural"]["routes"]["training"] == "ELIGIBLE"
    assert late["n9_world"]["rules"]["training_fee"]["value"] == 6
    assert late["structural"]["routes"]["training"] == "BLOCKED_BY_MODELED_RULE"


def test_revocation_is_selective_for_structural_channel():
    service = P41Service()
    first = service.consumer_read()
    invalidation = service.readthrough.invalidate("civil_sanction")
    after = service.consumer_read()
    assert after["material"]["structural_routes"]["civil"]["state"] == \
        "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert after["material"]["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert [step["cells"] for step in after["material"]["empirical"]["steps"]] == \
        [step["cells"] for step in first["material"]["empirical"]["steps"]]
    assert invalidation["historical_receipts_retained"] is True


def test_source_permission_revocation_affects_consumer_channel_only():
    service = P41Service()
    service.readthrough.invalidate("empirical")
    consumer_view = service.consumer_read()
    assert consumer_view["material"]["state"] == \
        "PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT"
    assert consumer_view["material"]["empirical"]["steps"] == []
    producer_view = service.progressive()
    assert [step["state"] for step in producer_view["n10e_steps"]] == \
        ["EXACT_SUPPORTED", "EXACT_SUPPORTED", "EXACT_SUPPORTED"]


def test_declared_no_current_refuses_fresh_serve():
    prepared = prepare()
    service = P41Service(prepared)
    first = service.consumer_read()
    selected = prepared.composition.b5_selection_receipt
    prepared.lifecycle.declare_no_current(
        selected.selection_key_ref,
        expected_previous_receipt_ref=selected.ref,
        event_authority_ref=ref("LifecycleAuthority", "none"),
        event_rule_ref=ref("LifecycleRule", "none"),
        reason_ref=ref("Reason", "none"),
        selection_attestation_ref=ref("SelectionAttestation", "none"))
    with pytest.raises(ValueError):
        service.consumer_read()
    archived = service.historical(first["receipt_hash"])
    assert archived["archival_only"] is True
    assert archived["fresh_use_authorized"] is False
    assert archived["material"] == first["material"]
