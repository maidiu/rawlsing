from __future__ import annotations

import copy

import j42_join as J


def fresh_view(**overrides):
    values = {
        "training_access": True,
        "training_fee": 2,
        "exit_cost": 2,
        "civil_open": True,
        "civil_sanction": False,
    }
    values.update(overrides)
    return dict(
        structural_values={
            key: {"value": value, "state": "SUPPORTED_TEST_ONLY",
                  "field_ref": "field:" + key}
            for key, value in values.items()},
        snapshot_hash="s" * 64,
        family="base",
        clock={"mode": "TEST_CURRENT", "valid_at": "2027-09-01",
               "published_asof": "2027-09-01"},
        budget_tokens=5,
        content_hash="v" * 64,
    )


def snapshot(view):
    return J.JoinedSnapshot(view["snapshot_hash"], view["family"],
                            view["clock"]["mode"], view["budget_tokens"])


def e04(view, e41):
    service = J.JoinedService(view, e41)
    result = J.consume(service, snapshot(view), budget_tokens=view["budget_tokens"])
    return result, service


def test_fresh_e41_native_positive_control(fresh_e41):
    assert fresh_e41["steps"]["Y/1"]["denominator"] == 32
    assert fresh_e41["steps"]["Y/1"]["conditioners"] == [["A", 1]]
    assert fresh_e41["steps"]["Y/1"]["evidence_ref"] is not None
    assert fresh_e41["steps"]["A/1"]["denominator"] == 29
    assert fresh_e41["steps"]["Y/1"]["fact_state"] == "SUPPORTED"


def test_j42_adapter_reads_a_evidence_for_a_c_request(fresh_e41):
    adapter = J.E41ProviderAdapter(fresh_e41, {})
    source_step = fresh_e41["steps"]["Y/1"]
    observed_c = adapter.step("Y", (("C", 1),))
    observed_a0 = adapter.step("Y", (("A", 0),))
    control = adapter.step("Y", (("A", 1),))
    joined = J.JoinedService(fresh_view(), fresh_e41)
    joined_result = joined.possibilities(
        snapshot(fresh_view()), conditions=(("C", 1),))
    assert joined_result["steps"][0]["conditioners"] == [["A", 1]]
    assert joined_result["steps"][0]["evidence_ref"] == source_step["evidence_ref"]
    assert observed_c["conditioners"] == [["A", 1]]
    assert observed_a0["conditioners"] == [["A", 1]]
    assert observed_c["evidence_ref"] == source_step["evidence_ref"]
    assert observed_a0["denominator"] == observed_c["denominator"] == 32
    assert observed_c["cells"] == [{"cell": "0", "raw_numerator_support": 14},
                                   {"cell": "1", "raw_numerator_support": 18}]
    assert control["conditioners"] == [["A", 1]]
    assert control["content_hash"] == observed_c["content_hash"]


def test_j42_p41_receipt_names_c_while_dereferencing_a_evidence(
        fresh_e41, prepared_p41):
    view = fresh_view()
    service = J.J42P41Service(view, fresh_e41, prepared_p41)
    receipt = service.progressive(
        target="Y", conditions=(("C", 1),),
        consumer="GENERIC_POSITIONED_SUBJECT", snapshot=snapshot(view))
    assert receipt["query"]["ordered_conditions"] == [["C", 1]]
    assert receipt["query"]["query_identity_hash"] == J.semantic_hash(
        ["Y", (("C", 1),)])
    assert receipt["n10e_steps"][0]["conditioners"] == [["A", 1]]
    assert receipt["n10e_steps"][0]["evidence_ref"] == \
        fresh_e41["steps"]["Y/1"]["evidence_ref"]
    assert receipt["n10e_steps"][0]["denominator"] == 32
    assert receipt["structural"]["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    control = J.J42P41Service(fresh_view(), fresh_e41, prepared_p41).progressive(
        target="Y", conditions=(("A", 1),),
        consumer="GENERIC_POSITIONED_SUBJECT", snapshot=snapshot(view))
    assert control["query"]["ordered_conditions"] == [["A", 1]]
    assert control["n10e_steps"][0]["conditioners"] == [["A", 1]]


def test_j42_e04_promotes_zero_support_step_to_options_produced(fresh_e41):
    mutated = copy.deepcopy(fresh_e41)
    mutated["steps"]["Y/2"]["fact_state"] = "ZERO_SUPPORT"
    mutated["steps"]["Y/2"]["consumer_state"] = None
    view = fresh_view()
    result, service = e04(view, mutated)
    material = result["material"]
    states = [step["state"] for step in material["empirical"]["steps"]]
    assert states == ["EXACT_SUPPORTED", "ZERO_SUPPORT", "EXACT_SUPPORTED"]
    assert material["empirical"]["state"] == "PRODUCTIVE_TEST_ONLY"
    assert material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    assert material["source_balance_reads"][1]["support_state"] == "ZERO_SUPPORT"
    control, _ = e04(view, fresh_e41)
    assert control["material"]["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"


def test_p41_unknown_step_claims_exact_support_on_conditioned_risk_set(
        fresh_e41, prepared_p41):
    mutated = copy.deepcopy(fresh_e41)
    mutated["steps"]["Y/1"]["fact_state"] = "ROUTING_UNKNOWN"
    mutated["steps"]["Y/1"]["consumer_state"] = None
    view = fresh_view()
    receipt = J.J42P41Service(view, mutated, prepared_p41).progressive(
        target="Y", conditions=(("A", 1),),
        consumer="GENERIC_POSITIONED_SUBJECT", snapshot=snapshot(view))
    assert receipt["n10e_steps"][0]["state"] == "ROUTING_UNKNOWN"
    assert receipt["n10w"]["progressive_chain_state"] == "TYPED_PARTIAL_OR_UNKNOWN"
    assert receipt["unknown"]["evidence_state"] == \
        "EXACT_SUPPORT_ON_CONDITIONED_RISK_SET"
    assert receipt["unknown"]["zero_support_steps"] == []
    zero = copy.deepcopy(fresh_e41)
    zero["steps"]["Y/1"]["fact_state"] = "ZERO_SUPPORT"
    zero["steps"]["Y/1"]["consumer_state"] = None
    control = J.J42P41Service(fresh_view(), zero, prepared_p41).progressive(
        target="Y", conditions=(("A", 1),),
        consumer="GENERIC_POSITIONED_SUBJECT", snapshot=snapshot(view))
    assert control["unknown"]["evidence_state"] == "NO_SUPPORTED_EVIDENCE"


def test_j42_absent_structural_state_defaults_to_supported_test_only(fresh_e41):
    view = fresh_view()
    del view["structural_values"]["training_access"]["state"]
    result, service = e04(view, fresh_e41)
    material = result["material"]
    assert material["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    read = next(item for item in service.value_reads
                if item["scope"] == "training_access")
    assert read["state"] == "SUPPORTED_TEST_ONLY"
    unavailable = fresh_view()
    unavailable["structural_values"]["training_access"]["state"] = \
        "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    control, _ = e04(unavailable, fresh_e41)
    assert control["material"]["structural_routes"]["training"]["state"] == \
        "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert control["material"]["state"] == "PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT"
