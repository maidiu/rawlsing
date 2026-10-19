"""Sorok C0X — real receiving-consumer court over the actual two-owner product.

Positive evidence is read from the actual repaired C0P facade and the actual
29-module native closure. No fixture receipt is substituted for the owner
output. Provider-state replacement, revocation, temporal unavailability and
owner substitution are exercised at the consumer boundary.
"""
from __future__ import annotations

import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import c0x_world_receiver as RX  # noqa: E402

SELECT = {"valid_at": "2027-09-01", "published_asof": "2027-09-01"}
EARLY = {"valid_at": "2026-02-01", "published_asof": "2026-02-01"}
AFTER_PUB = {"valid_at": "2026-06-01", "published_asof": "2026-03-01"}
PROPOSALS = [dict(scenario_id="S1", route="institutional"),
             dict(scenario_id="S2", route="civil")]


def make(consumer="NONPARENT_OPTIONS"):
    return RX.make_receipt(
        consumer, select_kwargs=SELECT,
        proposals=PROPOSALS if consumer == "CONCEPTION_SCENARIO_PROPOSALS" else None)


def receive(consumer="NONPARENT_OPTIONS"):
    return RX.receive_receipt(make(consumer), {"consumer": consumer})


def test_nonparent_receipt_reads_actual_upstream_selection():
    receipt = make()
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["schema"] == RX.SCHEMA
    assert out["receiver_version"] == RX.RECEIVER_VERSION
    assert out["owner_contracts"][RX.N9]["field_count"] == 17
    assert out["owner_contracts"][RX.N10]["field_count"] == 20
    assert out["owner_contracts"][RX.N9]["contract_version"] == RX.ENV_WORLD
    assert out["owner_contracts"][RX.N10]["contract_version"] == RX.ENV_POSS
    assert len(out["owner_contracts"][RX.N9]["receipt"]["selection"]) == 5
    assert len(out["owner_contracts"][RX.N9]["receipt"]["payloads"]) == 5
    assert len(out["native_units"]) == 1
    assert out["owner_identities"]["distinct"] is True
    assert out["evidence_state"] == "SUPPORTED"
    routes = out["material_world_opportunity"]["structural_routes"]
    assert routes["training"]["state"] == "ELIGIBLE"
    assert routes["civil"]["state"] == "ELIGIBLE"
    assert out["material_world_opportunity"]["route_probability"] is None
    assert out["no_joint_probability"] is True
    assert out["transport"]["json_serializable"] is False
    assert any("parent_receipt_ref" in p
               for p in out["transport"]["non_transportable_fields"])
    assert out["transport_hold"] is True


def test_conception_receipt_reads_actual_upstream_scenarios():
    receipt = make("CONCEPTION_SCENARIO_PROPOSALS")
    out = RX.receive_receipt(receipt, {"consumer": "CONCEPTION_SCENARIO_PROPOSALS"})
    assert out["owner_contracts"][RX.N10]["contract_version"] == RX.ENV_POSS
    assert out["owner_contracts"][RX.N9]["contract_version"] == RX.ENV_WORLD
    assert out["evidence_state"] == "SUPPORTED"
    scenarios = out["material_world_opportunity"]["scenarios"]
    assert len(scenarios) == 2
    assert all(s["selection_weight"] is None for s in scenarios)
    assert out["material_world_opportunity"]["person_generation"] is False
    assert out["material_world_opportunity"]["actual_conception"] is False
    assert out["route_probability"] is None
    assert out["selection_weight"] is None


def test_provider_replacement_changes_material_value_not_stale():
    base = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=SELECT)
    revised = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=SELECT,
                                service_options={"structural_revision": True})
    assert base["material_world_opportunity"]["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert revised["material_world_opportunity"]["structural_routes"]["training"]["state"] == \
        "BLOCKED_BY_MODELED_RULE"
    assert revised["material_world_opportunity"]["structural_routes"]["civil"]["state"] == "ELIGIBLE"
    assert revised["evidence_state"] == "PARTIAL"
    assert "MATERIAL_ROUTE_BLOCKED" in revised["evidence_reasons"]
    assert revised["route_probability"] is None


def test_source_revocation_types_partial_and_preserves_civil():
    port = RX.FACADE.TwoContractPort()
    snap = port.select(**SELECT)
    port._service.catalog.revoke("training_access")
    receipt = port.consume_nonparent(snap)
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    routes = out["material_world_opportunity"]["structural_routes"]
    assert routes["training"]["state"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert routes["civil"]["state"] == "ELIGIBLE"
    assert out["evidence_state"] == "PARTIAL"
    assert "MATERIAL_ROUTE_UNAVAILABLE" in out["evidence_reasons"]
    assert out["route_probability"] is None


def test_temporal_unavailability_fails_closed_without_fabricated_receipt():
    out = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=EARLY)
    assert out["evidence_state"] == "UNKNOWN"
    assert out["owner_contracts"] is None
    assert out["route_probability"] is None
    assert any("UPSTREAM_TEMPORAL" in reason for reason in out["evidence_reasons"])


def test_four_clock_roles_are_preserved_without_collapsing_roles():
    out = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=AFTER_PUB)
    clocks = out["four_clocks"]
    assert clocks["mode"] == "KNOWLEDGE_AS_OF"
    assert clocks["observation_effective"]["valid_from"] == "2026-06-01"
    assert clocks["publication_knowledge"]["published_at"] == "2026-03-01"
    assert clocks["actor_event"]["scene_at"] == "2026-03-01"
    assert clocks["request_currentness"]["requested_at"] == "2026-03-01"
    assert clocks["publication_knowledge"]["knowledge_as_of"] == "2026-03-01"
    assert clocks["actor_event"]["caller_owns_time"] is True
    assert out["actor_clock_is_caller_owned"] is True
    assert out["historical_entitlement_reconstructed"] is False
    assert out["route_probability"] is None
    # The four roles are structural and separately published. Actor/request
    # values may coincide for a caller-owned scene; that is disclosed, not
    # presented as an independent historical reconstruction.
    values = {
        clocks["observation_effective"]["valid_from"],
        clocks["publication_knowledge"]["published_at"],
        clocks["actor_event"]["scene_at"],
        clocks["request_currentness"]["requested_at"],
    }
    assert len(values) == 2


def test_source_permission_and_native_units_preserved():
    out = receive()
    assert out["grade"] == "TEST_FIXTURE_ONLY"
    permission = out["source_permission"]
    assert permission["source_allowed_use_atoms"] == ["TEST_ONLY_CONTEXT"]
    assert permission["effective_use_atoms"] == ["TEST_ONLY_CONTEXT"]
    assert permission["model_use_ref"] is None
    unit = out["native_units"][0]["native_unit_ref"]
    assert unit["kind"] == "NativeUnit"
    assert "SYNTHETIC_INDIVIDUAL_RESPONDENT" in unit["id"]
    assert out["real_use_authorized"] is False


def test_minority_unknown_and_no_joint_probability_preserved():
    out = receive()
    unknown = out["minority_unknown"]
    assert unknown["pruned"] is False
    assert unknown["selection_records"] == 5
    assert unknown["payloads"] == 5
    assert len(unknown["empirical_steps"]) == 3
    assert all(step["cells"] for step in unknown["empirical_steps"])
    limits = out["generated_conditioner_limits"]
    assert limits["generated_criteria_echo"] == []
    assert limits["same_respondent_joint_ref"] is None
    assert limits["composition_mode"] == "REFUSED"
    assert limits["model_use_ref"] is None
    assert limits["actor_generation"] is False
    assert limits["person_generation"] is False
    assert out["owner_contracts"][RX.N10]["receipt"]["alternatives"]["route_probability"] is None


def test_owner_substitution_is_refused():
    nonparent = make()
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(nonparent, {"consumer": "CONCEPTION_SCENARIO_PROPOSALS"})
    assert exc.value.code == "OWNER_SUBSTITUTION"
    conception = make("CONCEPTION_SCENARIO_PROPOSALS")
    with pytest.raises(RX.ReceiverRefusal) as exc2:
        RX.receive_receipt(conception, {"consumer": "NONPARENT_OPTIONS"})
    assert exc2.value.code == "OWNER_SUBSTITUTION"


def test_withheld_owner_contract_is_refused():
    receipt = make()
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(replace(receipt, possibility_receipt=None),
                           {"consumer": "NONPARENT_OPTIONS"})
    assert exc.value.code == "MISSING_OWNER_CONTRACT"
    with pytest.raises(RX.ReceiverRefusal) as exc2:
        RX.receive_receipt(replace(receipt, world_receipt=None),
                           {"consumer": "NONPARENT_OPTIONS"})
    assert exc2.value.code == "MISSING_OWNER_CONTRACT"


def test_swapped_or_forged_owner_contracts_are_refused():
    receipt = make()
    swapped = replace(receipt, world_receipt=receipt.possibility_receipt,
                      possibility_receipt=receipt.world_receipt)
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(swapped, {"consumer": "NONPARENT_OPTIONS"})
    assert exc.value.code == "OWNER_CONTRACT_MISMATCH"
    forged_world = dict(receipt.world_receipt)
    forged_world["contract"] = "FORGED_CONTRACT@9"
    with pytest.raises(RX.ReceiverRefusal) as exc2:
        RX.receive_receipt(replace(receipt, world_receipt=forged_world),
                           {"consumer": "NONPARENT_OPTIONS"})
    assert exc2.value.code == "OWNER_CONTRACT_MISMATCH"


def test_reverse_direction_and_real_use_are_refused():
    receipt = make()
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS",
                                     "direction": "REVERSE_CONDITIONAL"})
    assert exc.value.code == "REVERSE_HELD"
    with pytest.raises(RX.ReceiverRefusal) as exc2:
        RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS",
                                     "use": "REAL_USE"})
    assert exc2.value.code == "PROHIBITED_MODEL_USE"


def test_unknown_demand_has_no_owner_consumer():
    receipt = make()
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(receipt, {"consumer": "MOTHER"})
    assert exc.value.code == "NO_OWNER_CONSUMER_FOR_DEMAND"


def test_receiver_uses_actual_upstream_blob():
    raw = RX.UPSTREAM.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == "855bb72f494d64083cee706e12f4f3d58c47dec3"
    assert Path(RX.FACADE.__file__).resolve() == RX.UPSTREAM.resolve()
    assert RX.RUNTIME.resolve() == (ROOT / "stage/runtime").resolve()


def test_k9_k10_full_corpus_receipt_is_36_green():
    path = ROOT / "evidence/k9k10_executed.xml"
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    assert len(cases) == 36
    assert not any(c.find("failure") is not None or c.find("error") is not None for c in cases)
    k9 = [c for c in cases if c.attrib.get("name", "").startswith("test_k9_")]
    k10 = [c for c in cases if c.attrib.get("name", "").startswith("test_k10_")]
    assert len(k9) == 8
    assert len(k10) == 28
