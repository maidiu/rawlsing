import json

from p41_current_service import CurrentP41Service, GRADE


def test_positive_current_e03_chain_exact_geometry_and_f8_consumption():
    service = CurrentP41Service()
    receipt = service.progressive()
    material = receipt.as_dict()
    assert material["grade"] == GRADE
    assert material["n9_world"]["real_current"] is False
    assert material["n9_world"]["n9_owner_implemented"] is False
    assert material["n9_world"]["n10w_owner_implemented"] is False
    assert [s["step_id"] for s in material["steps"]] == [
        "P_Y_given_A", "P_Y_given_A_B", "P_Y_given_A_B_C"]
    assert [s["denominator"] for s in material["steps"]] == [32, 16, 8]
    assert [s["cells"]["1"]["fraction"] for s in material["steps"]] == [
        {"$exact_fraction": [9, 16]},
        {"$exact_fraction": [5, 8]},
        {"$exact_fraction": [3, 4]},
    ]
    assert all(v["result_state"] == "EXACT_SUPPORTED" for v in material["f8_consumptions"].values())
    assert material["actor_state_present"] is False


def test_as_of_and_rule_clock_change_metadata_not_empirical_geometry():
    service = CurrentP41Service()
    before = service.progressive().as_dict()
    service.as_of("2027-01-01", "2027-01-02", rule_revision=2)
    after = service.progressive().as_dict()
    assert before["steps"] == after["steps"]
    assert before["content_hash"] != after["content_hash"]
    assert after["clocks"]["as_of"] == "2027-01-01"
    assert after["clocks"]["publication"] == "2027-01-02"
    assert after["clocks"]["rule_revision"] == 2
    assert after["clocks"]["clock_domain"].startswith("ADAPTER_TEST_ONLY")


def test_empirical_revocation_refuses_consumer_but_progressive_remains_exact():
    service = CurrentP41Service()
    receipt = service.progressive()
    service.revoke("empirical")
    refused = service.consumer_read()
    assert refused["status"] == "REFUSED"
    assert refused["reason"] == "EMPIRICAL_SCOPE_REVOKED"
    still = service.progressive()
    assert [s["state"] for s in still.as_dict()["steps"]] == [
        "SUPPORTED", "SUPPORTED", "SUPPORTED"]
    archived = service.historical(receipt.content_hash)
    assert archived["archival_only"] is True
    assert archived["fresh_use_authorized"] is False
    assert archived["receipt"]["steps"] == receipt.as_dict()["steps"]


def test_cold_restore_exact_and_tamper_refused():
    service = CurrentP41Service()
    receipt = service.progressive()
    payload = json.dumps(receipt.as_dict())
    restored = service.cold_restore(payload)
    assert restored["status"] == "RESTORED"
    assert restored["content_hash"] == receipt.content_hash
    tampered = receipt.as_dict()
    tampered["steps"][0]["denominator"] = 999
    assert service.validate_receipt(tampered)["status"] == "REFUSED"
    assert service.validate_receipt(tampered)["reason"] == "RECEIPT_HASH_MISMATCH"


def test_replay_is_deterministic_and_receipt_identity_is_content_addressed():
    a = CurrentP41Service().progressive()
    b = CurrentP41Service().progressive()
    assert a.content_hash == b.content_hash
    assert a.as_dict()["steps"] == b.as_dict()["steps"]
