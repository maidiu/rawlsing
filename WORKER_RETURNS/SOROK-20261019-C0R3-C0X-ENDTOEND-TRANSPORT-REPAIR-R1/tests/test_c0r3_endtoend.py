"""C0R3 end-to-end owner transport and C10 receiver court.

Exercises the corrected C0P facade and C0X receiver on the exact 29-module
native closure. All scenes, grants and receipts are TEST_ONLY sourcefree.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidate"
RUNTIME = CANDIDATE / "stage" / "runtime"
ORIGINAL = ROOT / "original"
sys.path.insert(0, str(CANDIDATE))
sys.path.insert(0, str(RUNTIME))

import c0x_world_receiver as RX  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

SELECT = {"valid_at": "2027-09-01", "published_asof": "2027-09-01"}
EARLY = {"valid_at": "2026-02-01", "published_asof": "2026-02-01"}
AFTER_PUB = {"valid_at": "2026-06-01", "published_asof": "2026-03-01"}
PROPOSALS = [dict(scenario_id="S1", route="institutional"),
             dict(scenario_id="S2", route="civil")]
EXPECT_NONPARENT = "52e10a2fd0ce21b30f535b2786d45d4bd88817f174caa006e5ba7f0589d851ec"
EXPECT_SCENARIO = "33251a740daff14a0920c4375b0b8577842cf812f5444e07b8313f5730fc3fde"
ROOT_PARENT = {"kind": "OrderedConditionStep", "id": "urn:test:c0p:step:root",
               "hash": semantic_hash("root")}


def make(consumer="NONPARENT_OPTIONS", **kwargs):
    return RX.make_receipt(
        consumer, select_kwargs=kwargs.pop("select_kwargs", SELECT),
        proposals=PROPOSALS if consumer == "CONCEPTION_SCENARIO_PROPOSALS" else None,
        **kwargs)


def receive(consumer="NONPARENT_OPTIONS", **kwargs):
    return RX.receive_receipt(make(consumer, **kwargs), {"consumer": consumer})


def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_path(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def assert_complete_owner_receipts(receipt):
    world = receipt.world_receipt
    poss = receipt.possibility_receipt
    assert len(world) == 17 and set(world) == set(RX.WORLD_FIELDS)
    assert len(poss) == 20 and set(poss) == set(RX.POSS_FIELDS)
    assert world["contract"] == RX.ENV_WORLD
    assert poss["contract"] == RX.ENV_POSS
    assert world["receipt_ref"]["hash"] == receipt.owner_receipt_hash
    assert poss["receipt_ref"]["hash"] == receipt.owner_receipt_hash
    assert len(world["selection"]) == 5
    assert len(world["payloads"]) == 5
    assert len(poss["ordered_steps"]) == 3
    assert poss["ordered_steps"][0]["parent_receipt_ref"] == ROOT_PARENT
    for index, step in enumerate(poss["ordered_steps"][1:], start=1):
        ref = step["parent_receipt_ref"]
        assert isinstance(ref, dict) and set(ref) == {"kind", "id", "hash"}
        assert ref["kind"] == "OrderedConditionStep"
        assert ref["id"] == f"urn:test:c0p:step:NONPARENT_OPTIONS:{index - 1}"
        assert ref["hash"] == poss["ordered_steps"][index - 1]["new_binding"]["hash"]


def test_complete_owner_receipts_transport_and_read_actual_values():
    receipt = make()
    assert_complete_owner_receipts(receipt)
    encoded = json.dumps({"world_receipt": receipt.world_receipt,
                          "possibility_receipt": receipt.possibility_receipt},
                         sort_keys=True, separators=(",", ":"))
    decoded = json.loads(encoded)
    assert decoded["world_receipt"] == receipt.world_receipt
    assert decoded["possibility_receipt"] == receipt.possibility_receipt
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["receiver_revision"] == RX.C0R3_REVISION
    assert out["transport"]["revision"] == RX.C0R3_REVISION
    assert out["transport"]["state"] == "LOSSLESS_TWO_CONTRACT_OBJECT"
    assert out["transport"]["json_serializable"] is True
    assert out["transport"]["owner_receipts_json_roundtrip"] is True
    assert out["transport"]["non_transportable_fields"] == []
    assert out["transport"]["world_receipt_fields"] == 17
    assert out["transport"]["possibility_receipt_fields"] == 20
    assert out["transport_hold"] is False
    assert out["values_read"]
    assert all(value.get("source_ref") for value in out["values_read"]
               if value.get("channel") == "structural")
    assert out["owner_contracts"][RX.N9]["receipt"]["values_read_refs"]
    assert out["owner_contracts"][RX.N10]["receipt"]["values_read_refs"]
    assert out["values_read_refs"] == out["owner_contracts"][RX.N9]["receipt"]["values_read_refs"]
    assert len(out["owner_contracts"][RX.N9]["receipt"]["selection"]) == 5
    assert len(out["owner_contracts"][RX.N10]["receipt"]["ordered_steps"]) == 3
    assert out["material_world_opportunity"]["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert out["route_probability"] is None and out["selection_weight"] is None


def test_conception_consumer_reads_complete_n10_receipt():
    receipt = make("CONCEPTION_SCENARIO_PROPOSALS")
    assert len(receipt.world_receipt) == 17
    assert len(receipt.possibility_receipt) == 20
    out = RX.receive_receipt(receipt, {"consumer": "CONCEPTION_SCENARIO_PROPOSALS"})
    assert out["evidence_state"] == "SUPPORTED"
    assert out["transport"]["json_serializable"] is True
    assert len(out["material_world_opportunity"]["scenarios"]) == 2
    assert all(s["selection_weight"] is None for s in
               out["material_world_opportunity"]["scenarios"])
    assert out["material_world_opportunity"]["person_generation"] is False
    assert out["material_world_opportunity"]["actual_conception"] is False
    assert out["owner_contracts"][RX.N10]["field_count"] == 20


def test_relocated_candidate_preserves_both_owner_sources_and_json_values():
    baseline = make()
    baseline_n10 = make("CONCEPTION_SCENARIO_PROPOSALS")
    assert len(baseline.world_receipt["selection"]) == 5
    assert len(baseline.world_receipt["payloads"]) == 5
    assert len(baseline.possibility_receipt["ordered_steps"]) == 3
    assert baseline.world_receipt["contract"] == RX.ENV_WORLD
    assert baseline_n10.possibility_receipt["contract"] == RX.ENV_POSS
    with tempfile.TemporaryDirectory(prefix="c0r3-relocated-") as directory:
        relocated_path = Path(directory) / "relocated_c0p.py"
        shutil.copyfile(CANDIDATE / "upstream/c0p_two_contract_port.py",
                        relocated_path)
        relocated = load_path(relocated_path, "c0r3_relocated_c0p")
        assert relocated_path.resolve() == Path(relocated.__file__).resolve()
        assert relocated.RUNTIME.resolve() == RUNTIME.resolve()
        assert Path(relocated.__file__).resolve() != Path(
            (CANDIDATE / "upstream/c0p_two_contract_port.py").resolve())
        port = relocated.TwoContractPort()
        snapshot = port.select(**SELECT)
        a = port.consume_nonparent(snapshot)
        b = port.consume_conception_proposals(snapshot, PROPOSALS)
        assert a.owner_receipt_hash == EXPECT_NONPARENT
        assert b.owner_receipt_hash == EXPECT_SCENARIO
        assert a.world_receipt == baseline.world_receipt
        assert b.possibility_receipt == baseline_n10.possibility_receipt
        assert json.dumps(a.as_dict(), sort_keys=True) == json.dumps(
            baseline.world_receipt, sort_keys=True)
        assert json.dumps(b.as_dict(), sort_keys=True) == json.dumps(
            baseline_n10.possibility_receipt, sort_keys=True)
        # Both owner receipt source identities remain the actual relocated
        # native producer bytes, not a caller-carried copy or a dummy hash.
        n9_producer = a.world_receipt["repository_refs"][0]
        assert n9_producer["id"] == "product/nonparent.py"
        assert n9_producer["hash"] == blob(RUNTIME / "product/nonparent.py")
        assert b.lineage["producer"] == "product.scenario.evaluate"
        assert b.lineage["producer_blob"] == blob(RUNTIME / "product/scenario.py")
        assert a.lineage["producer"] == "product.nonparent.consume"
        assert a.lineage["producer_blob"] == blob(RUNTIME / "product/nonparent.py")
        assert a.values_read and b.values_read
        # Determinism of identical calls on identical input.
        a2 = port.consume_nonparent(snapshot)
        assert json.dumps(a2.as_dict(), sort_keys=True) == json.dumps(
            a.as_dict(), sort_keys=True)


def test_temporal_source_ref_is_typed_refusal_not_type_error():
    out = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=EARLY)
    assert out["evidence_state"] == "UNKNOWN"
    assert out["owner_contracts"] is None
    assert out["evidence_reasons"] == ["UPSTREAM_TYPED_TEMPORAL_SOURCE_REFUSAL"]
    assert out["upstream_refusal_code"] == "TEMPORAL_SOURCE_REF_UNAVAILABLE_AT_ASOF"
    assert out["upstream_refusal_fields"]
    assert all("UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK" in field
               for field in out["upstream_refusal_fields"])
    assert out["route_probability"] is None
    assert out["transport"]["state"] == "NO_RECEIPT"


def test_provider_swap_and_source_revocation_are_typed_partial():
    swapped = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=SELECT,
                                service_options={"structural_revision": True})
    assert swapped["evidence_state"] == "PARTIAL"
    assert swapped["material_world_opportunity"]["structural_routes"]["training"]["state"] == \
        "BLOCKED_BY_MODELED_RULE"
    assert swapped["material_world_opportunity"]["structural_routes"]["civil"]["state"] == \
        "ELIGIBLE"

    port = RX.FACADE.TwoContractPort()
    snapshot = port.select(**SELECT)
    port._service.catalog.revoke("training_access")
    receipt = port.consume_nonparent(snapshot)
    revoked = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert revoked["evidence_state"] == "PARTIAL"
    assert revoked["material_world_opportunity"]["structural_routes"]["training"]["state"] == \
        "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert revoked["material_world_opportunity"]["structural_routes"]["civil"]["state"] == \
        "ELIGIBLE"
    assert revoked["transport"]["json_serializable"] is True


def test_owner_substitution_and_invalid_parent_are_refused():
    receipt = make()
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(receipt, {"consumer": "CONCEPTION_SCENARIO_PROPOSALS"})
    assert exc.value.code == "OWNER_SUBSTITUTION"
    broken = copy.deepcopy(receipt)
    broken.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"] = None
    with pytest.raises(RX.ReceiverRefusal) as exc2:
        RX.receive_receipt(broken, {"consumer": "NONPARENT_OPTIONS"})
    assert exc2.value.code == "PARENT_RECEIPT_REF_NOT_EXACT"
    assert exc2.value.detail == "ordered_steps[0].parent_receipt_ref"


def test_corrected_parent_ref_is_materialized_exact_ref():
    receipt = make()
    ref = receipt.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"]
    assert ref == ROOT_PARENT
    assert not callable(ref)
    assert set(ref) == {"kind", "id", "hash"}
    json.dumps(receipt.possibility_receipt)


def test_original_callable_parent_ref_is_refused_and_corrected_is_exact():
    original = load_path(ORIGINAL / "c0p_repaired_author.py", "c0r3_original_c0p")
    port = original.TwoContractPort()
    snapshot = port.select(**SELECT)
    legacy = port.consume_nonparent(snapshot)
    legacy_ref = legacy.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"]
    assert callable(legacy_ref)
    with pytest.raises(TypeError):
        json.dumps(legacy.possibility_receipt)
    with pytest.raises(RX.ReceiverRefusal) as exc:
        RX.receive_receipt(legacy, {"consumer": "NONPARENT_OPTIONS"})
    assert exc.value.code == "PARENT_RECEIPT_REF_NOT_EXACT"
    corrected = make()
    corrected_ref = corrected.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"]
    assert corrected_ref == ROOT_PARENT
    assert not callable(corrected_ref)
    assert RX.receive_receipt(corrected, {"consumer": "NONPARENT_OPTIONS"})["transport"][
        "json_serializable"] is True


def test_native_units_minority_echo_joint_and_permission_limits_held():
    out = receive()
    assert out["minority_unknown"]["pruned"] is False
    assert out["minority_unknown"]["selection_records"] == 5
    assert out["minority_unknown"]["payloads"] == 5
    assert len(out["minority_unknown"]["empirical_steps"]) == 3
    assert out["native_units"][0]["native_unit_ref"]["kind"] == "NativeUnit"
    assert "SYNTHETIC_INDIVIDUAL_RESPONDENT" in out["native_units"][0]["native_unit_ref"]["id"]
    limits = out["generated_conditioner_limits"]
    assert limits["generated_criteria_echo"] == []
    assert limits["same_respondent_joint_ref"] is None
    assert limits["composition_mode"] == "REFUSED"
    assert limits["model_use_ref"] is None
    assert limits["actor_generation"] is False
    assert limits["person_generation"] is False
    assert limits["actual_conception"] is False
    assert out["source_permission"]["source_allowed_use_atoms"] == ["TEST_ONLY_CONTEXT"]
    assert out["source_permission"]["effective_use_atoms"] == ["TEST_ONLY_CONTEXT"]
    assert out["source_permission"]["model_use_ref"] is None
    assert out["real_use_authorized"] is False


def test_four_clock_roles_preserved_without_archival_known_at_claim():
    out = RX.receive_demand("NONPARENT_OPTIONS", select_kwargs=AFTER_PUB)
    clocks = out["four_clocks"]
    assert set(clocks) == {"observation_effective", "publication_knowledge",
                           "actor_event", "request_currentness", "mode"}
    assert clocks["mode"] == "KNOWLEDGE_AS_OF"
    assert clocks["observation_effective"]["valid_from"] == "2026-06-01"
    assert clocks["publication_knowledge"]["published_at"] == "2026-03-01"
    assert clocks["publication_knowledge"]["knowledge_as_of"] == "2026-03-01"
    assert clocks["actor_event"]["caller_owns_time"] is True
    assert clocks["request_currentness"]["requested_at"] == "2026-03-01"
    assert out["actor_clock_is_caller_owned"] is True
    assert out["historical_entitlement_reconstructed"] is False
    assert out["route_probability"] is None


def test_direct_facade_typed_temporal_refusal_not_blank_positive():
    port = RX.FACADE.TwoContractPort()
    snapshot = port.select(**EARLY)
    with pytest.raises(RX.FACADE.TemporalSourceRefUnavailable) as exc:
        port.consume_nonparent(snapshot)
    assert exc.value.code == "TEMPORAL_SOURCE_REF_UNAVAILABLE_AT_ASOF"
    assert exc.value.fields
    assert all("UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK" in field
               for field in exc.value.fields)


def test_same_input_no_change_is_exact_deterministic_replay():
    first = receive()
    second = receive()
    assert first["owner_contracts"][RX.N9]["owner_receipt_hash"] == \
        second["owner_contracts"][RX.N9]["owner_receipt_hash"]
    assert first["owner_contracts"][RX.N10]["owner_receipt_hash"] == \
        second["owner_contracts"][RX.N10]["owner_receipt_hash"]
    assert json.dumps(first["owner_contracts"], sort_keys=True) == \
        json.dumps(second["owner_contracts"], sort_keys=True)
    assert first["evidence_state"] == second["evidence_state"] == "SUPPORTED"
    assert first["route_probability"] is None
    assert first["selection_weight"] is None


def test_cold_process_roundtrip_keeps_complete_contracts():
    probe = ROOT / "tests" / "cold_probe.py"
    outputs = []
    for _ in range(2):
        result = subprocess.run([sys.executable, "-B", str(probe), str(ROOT)],
                                cwd=str(ROOT), capture_output=True, text=True,
                                env={"PYTHONDONTWRITEBYTECODE": "1",
                                     "C0P_RUNTIME": str(RUNTIME)},
                                check=True)
        outputs.append(json.loads(result.stdout))
    first, second = outputs
    assert first == second
    assert first["nonparent"]["world_fields"] == 17
    assert first["nonparent"]["possibility_fields"] == 20
    assert first["nonparent"]["transport"] == "LOSSLESS_TWO_CONTRACT_OBJECT"
    assert first["nonparent"]["parent0"] == ROOT_PARENT
    assert first["nonparent"]["owner_receipt_hash"] == EXPECT_NONPARENT
    assert first["conception"]["owner_receipt_hash"] == EXPECT_SCENARIO
    assert first["conception"]["transport"] == "LOSSLESS_TWO_CONTRACT_OBJECT"
    assert first["nonparent"]["selection"] == 5
    assert first["nonparent"]["ordered_steps"] == 3
    assert first["nonparent"]["json_sha256"] == second["nonparent"]["json_sha256"]
