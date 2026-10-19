"""J42 core join: same-source identity, E41 computed identity, joined consumer,
P41 bound receipt and authorized reverse role."""
from __future__ import annotations

import j42_join as J

EXPECTED = {
    "Y/1": (32, {"0": 14, "1": 18}),
    "Y/2": (16, {"0": 6, "1": 10}),
    "Y/3": (8, {"0": 2, "1": 6}),
}


def cells(step):
    return {cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]}


def test_same_source_identity_with_p41(fresh, p41_rows_hash):
    e41, _ = fresh
    assert e41["world_identity"]["rows_hash"] == p41_rows_hash
    assert e41["world_identity"]["permission_root"] == "TEST_ONLY_E04_SOURCE_ROOT"


def test_e41_computed_chain_identity(fresh):
    e41, _ = fresh
    for key, (denominator, expected_cells) in EXPECTED.items():
        step = e41["steps"][key]
        assert step["denominator"] == denominator, key
        assert cells(step) == expected_cells, key
        assert step["provider_state"] == "EXACT_SUPPORTED_SLICE_PRODUCED", key
        assert step["fact_state"] == "SUPPORTED", key
        assert step["consumer_state"] == "EXACT_SUPPORTED", key
        assert step["evidence_ref"] is not None
        assert step["composed_hash"]
    assert e41["steps"]["A/1"]["denominator"] == 29
    assert cells(e41["steps"]["A/1"]) == {"0": 11, "1": 18}


def test_w41_same_source_computation_matches_e41(fresh):
    e41, w41 = fresh
    view = w41["worlds"][J.view_key("base", "TEST_CURRENT", 5)]
    w41_steps = view["native_consumer"]["empirical_steps"]
    assert [step["denominator"] for step in w41_steps] == [32, 16, 8]
    assert [step["cells"] for step in w41_steps] == [
        {k: v for k, v in cells(e41["steps"][key]).items()}
        for key in ("Y/1", "Y/2", "Y/3")]


def test_joined_consumer_depends_on_e41_and_w41(joined, fresh):
    e41, w41 = fresh
    view_key = J.view_key("fee_only", "TEST_CURRENT", 5)
    entry = next(row for row in joined["views"] if row["key"] == view_key)
    assert entry["actual"] == J.expected_routes("fee_only", "TEST_CURRENT", 5)
    assert entry["actual"]["training"] == "BLOCKED_BY_MODELED_RULE"
    receipt = next(row["joined_receipt"] for row in joined["joined_receipts"]
                   if row["key"] == view_key)
    material = receipt["material"]
    assert material["e41_rows_hash"] == e41["world_identity"]["rows_hash"]
    assert material["w41_snapshot_hash"] == \
        w41["worlds"][view_key]["snapshot_hash"]
    assert [step["denominator"] for step in material["empirical"]["steps"]] \
        == [32, 16, 8]
    assert [cells(step) for step in material["empirical"]["steps"]] == [
        cells(e41["steps"][key]) for key in ("Y/1", "Y/2", "Y/3")]
    assert len(material["e41_composed_hashes"]) == 3
    assert material["service_contract"] == J.J42_CONTRACT
    assert material["route_probability"] is None
    assert material["actor_executions"] == 0 and material["model_calls"] == 0


def test_p41_joined_chain_uses_e41_values(joined, fresh):
    e41, w41 = fresh
    view_key = J.view_key("base", "TEST_CURRENT", 5)
    index = [row["key"] for row in joined["views"]].index(view_key)
    receipt = joined["p41_receipts"][index]
    assert receipt["providers"]["n10e_empirical"].startswith("E41_")
    assert receipt["providers"]["n9_world"].startswith("W41_")
    assert receipt["providers"]["n10w_progressive"].startswith("P41_")
    assert [step["denominator"] for step in receipt["n10e_steps"]] == [32, 16, 8]
    assert [cells(step) for step in receipt["n10e_steps"]] == [
        cells(e41["steps"][key]) for key in ("Y/1", "Y/2", "Y/3")]
    assert receipt["structural"]["routes"] == \
        J.expected_routes("base", "TEST_CURRENT", 5)
    assert receipt["j42_bindings"]["e41_rows_hash"] == \
        e41["world_identity"]["rows_hash"]
    assert receipt["j42_bindings"]["w41_snapshot_hash"] == \
        w41["worlds"][view_key]["snapshot_hash"]
    assert len(receipt["n10w"]["progressive_update_identity"]) == 3
    assert receipt["minorities"]["smallest_cell"] == \
        {"cell": "0", "raw_numerator_support": 2}
    assert receipt["firewall"]["actor_state_present"] is False


def test_reverse_role_is_joined_and_exact(reverse_receipt):
    receipt = reverse_receipt
    assert receipt["query"]["role_class"] == "REVERSE_AUTHORIZED"
    assert [step["denominator"] for step in receipt["n10e_steps"]] == [29]
    assert cells(receipt["n10e_steps"][0]) == {"0": 11, "1": 18}
    assert receipt["providers"]["n10e_empirical"].startswith("E41_")
