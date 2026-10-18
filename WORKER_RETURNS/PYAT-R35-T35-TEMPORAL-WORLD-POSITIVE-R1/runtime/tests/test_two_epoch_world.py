"""Two-epoch native world court over the exact E04/M4/M5 owner chain."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import bootstrap
import two_epoch_world as W
from product.world import SelectedSnapshot
from rawlsing_next.pre553_empirical_objects import semantic_hash

RETURN = bootstrap.RETURN
REPLAY = RETURN / "02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT"


@pytest.fixture(scope="module")
def product():
    return W.build_product()


def test_epoch_views_match_frozen_expectations(product):
    frozen = bootstrap.freeze()["two_epoch_world"]["epochs"]
    for label, expected in (("E1_EARLY_2026", frozen["E1_EARLY_2026"]),
                            ("E2_LATE_2027", frozen["E2_LATE_2027"])):
        view = product["epochs"][label]
        assert view["receipt_state"] == expected["receipt_state"]
        assert view["clock"] == expected["clock"]
        for key, value in expected["structural_values"].items():
            assert view["structural_values"][key]["value"] == value
        assert {key: value["state"] for key, value in
                view["nonparent_routes"].items()} == expected["nonparent_routes"]
        assert [row["feasibility"] for row in
                view["scenario_feasibility"]] == expected["scenario_feasibility"]
        assert [dict(denominator=row["denominator"], cells=row["cells"])
                for row in view["empirical_steps"]] == expected["empirical_steps"]
    assert [row["denominator"] for row in
            product["epochs"]["E1_EARLY_2026"]["empirical_steps"]] == [32, 16, 8]


def test_formal_eligibility_preserved_while_practical_opportunity_changes(product):
    delta = product["consumer_delta"]
    assert delta["formal_eligibility_preserved"] is True
    assert delta["structural"]["training_access"]["epoch_1"] is True
    assert delta["structural"]["training_access"]["epoch_2"] is True
    assert delta["structural"]["training_fee"]["epoch_1"] == 2
    assert delta["structural"]["training_fee"]["epoch_2"] == 6
    assert delta["structural"]["exit_cost"]["epoch_1"] == 2
    assert delta["structural"]["exit_cost"]["epoch_2"] == 8
    assert delta["practical_routes"]["epoch_1"]["training"] == "ELIGIBLE"
    assert delta["practical_routes"]["epoch_2"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert delta["practical_routes"]["epoch_1"]["exit_constraint"] == "WITHIN_MODELED_BUDGET"
    assert delta["practical_routes"]["epoch_2"]["exit_constraint"] == "RESOURCE_CONSTRAINED"
    assert delta["empirical"]["identical"] is True
    assert delta["empirical"]["epoch_1_source_balance"] == [4, 4, 4]
    assert delta["empirical"]["epoch_2_source_balance"] == [4, 4, 4]


def test_legitimate_null_effects_are_explicit(product):
    delta = product["consumer_delta"]
    assert delta["practical_routes"]["epoch_1"]["civil"] == "ELIGIBLE"
    assert delta["practical_routes"]["epoch_2"]["civil"] == "ELIGIBLE"
    assert delta["scenarios"]["changed"] == []
    assert delta["scenarios"]["epoch_1"] == ["FEASIBLE_MODELED_PREMISE",
                                            "FEASIBLE_MODELED_PREMISE"]
    assert len(delta["legitimate_null_effects"]) == 3


def test_formal_eligibility_change_isolated_from_material_change(product):
    formal = product["formal_eligibility_isolation"]
    control = formal["material_control"]
    rule = formal["formal_rule"]
    assert control["training_access"] is True
    assert rule["training_access"] is False
    assert control["training_fee"] == rule["training_fee"] == 2
    assert control["exit_cost"] == rule["exit_cost"] == 2
    assert control["training_route"] == "ELIGIBLE"
    assert rule["training_route"] == "BLOCKED_BY_MODELED_RULE"
    assert control["scenarios"][0] == "FEASIBLE_MODELED_PREMISE"
    assert rule["scenarios"][0] == "INFEASIBLE_MODELED_PREMISE"
    assert formal["material_constraints_held_fixed"] is True
    assert formal["empirical_steps_identical"] is True


def test_clock_cross_product_effective_publication_and_requested_asof(product):
    rows = product["timeline_interventions"]
    assert [row["training_fee"] for row in rows] == [2, 6, 2, 6, 2]
    assert [row["exit_cost"] for row in rows] == [2, 8, 2, 8, 2]
    assert [row["training_route"] for row in rows] == [
        "ELIGIBLE", "BLOCKED_BY_MODELED_RULE", "ELIGIBLE",
        "BLOCKED_BY_MODELED_RULE", "ELIGIBLE"]
    assert rows[0]["valid_at"] == "2027-09-01"
    assert rows[0]["published_asof"] == "2027-05-31"
    assert rows[1]["published_asof"] == "2027-06-01"
    assert rows[2]["valid_at"] == "2026-06-01"
    assert rows[2]["published_asof"] == "2027-09-01"


def test_historical_immutability_and_in_process_replay():
    adapter = W.make_adapter()
    first = W.serve(adapter, W.E1)["receipt"]
    later = W.serve(adapter, W.E2)["receipt"]
    replay = W.serve(adapter, W.E1)["receipt"]
    assert first["receipt_hash"] == replay["receipt_hash"]
    assert first["snapshot_hash"] == replay["snapshot_hash"]
    assert first["structural_values"] == replay["structural_values"]
    assert first["empirical_steps"] == replay["empirical_steps"]
    assert first["receipt_hash"] != later["receipt_hash"]
    archived = adapter.historical_receipt(first["receipt_hash"])
    assert archived["archival_only"] is True
    assert archived["fresh_use_authorized"] is False


def test_structural_permission_revocation_is_selective(product):
    rev = product["revocation"]
    civil = rev["civil_sanction"]
    assert civil["after_state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert civil["after_civil_route"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert civil["after_training_route"] == "ELIGIBLE"
    assert civil["after_exit_constraint"] == "WITHIN_MODELED_BUDGET"
    assert civil["after_civil_value"]["state"] == "REVOKED"
    assert civil["historical"]["archival_only"] is True
    assert civil["historical"]["fresh_use_authorized"] is False
    assert civil["old_receipt_invalidated"] is True
    fee = rev["training_fee"]
    assert fee["civil_only_before_in_unaffected"] is True
    assert fee["civil_only_after_state"] == "SELECTED_WORLD_VALUES_SERVED"
    assert fee["full_after_state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert fee["full_after_training_route"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert fee["full_after_civil_route"] == "ELIGIBLE"


def test_native_field_permission_revocation_is_typed(product):
    revoked = product["revocation"]["native_field"]
    assert revoked["revoked_role"] == "GSS_RURAL_LIGHTING"
    assert revoked["native_state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert revoked["remaining_roles"] == ["NCA_NATIONAL_MOBILE_DATA"]
    assert revoked["after_state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert revoked["refusals"][0]["reason"] == "SOURCE_REVOKED"


def test_source_and_selected_world_mismatch_is_refused(product):
    mismatch = product["mismatch"]
    assert mismatch["foreign_source_world_snapshot"]["refusal"]["refused"] is True
    assert mismatch["foreign_source_world_snapshot"]["refusal"]["type"] == "ValueError"
    assert "UNREGISTERED_SELECTED_SNAPSHOT" in \
        mismatch["foreign_source_world_snapshot"]["refusal"]["message"]
    assert mismatch["foreign_acceptance_into_other_world"]["refusal"]["refused"] is True
    assert "ACCEPTANCE_BINDING_MISMATCH" in \
        mismatch["foreign_acceptance_into_other_world"]["refusal"]["message"]
    assert mismatch["cross_epoch_acceptance_snapshot"]["refusal"]["refused"] is True
    assert "ACCEPTED_SNAPSHOT_SUBSTITUTION" in \
        mismatch["cross_epoch_acceptance_snapshot"]["refusal"]["message"]
    assert mismatch["rehashed_tampered_snapshot"]["refusal"]["refused"] is True
    assert "UNREGISTERED_SELECTED_SNAPSHOT" in \
        mismatch["rehashed_tampered_snapshot"]["refusal"]["message"]


def test_real_tampered_snapshot_object_is_refused():
    adapter = W.make_adapter()
    request = W.make_request(W.E1)
    snapshot = adapter.build_snapshot(request)
    material = json.loads(json.dumps(snapshot.material))
    material["source_permission_root"] = "CALLER_ROOT"
    forged = SelectedSnapshot(material, semantic_hash(material))
    with pytest.raises(ValueError, match="UNREGISTERED_SELECTED_SNAPSHOT"):
        adapter.accept(request, forged)


def test_source_change_and_rule_change_are_orthogonal(product):
    matrix = product["source_versus_rule_matrix"]
    assert matrix["rule_only_change"]["empirical_identical"] is True
    assert matrix["rule_only_change"]["structural_routes_changed"] is True
    assert matrix["source_only_change"]["structural_routes_identical"] is True
    assert matrix["source_only_change"]["empirical_changed"] is True
    assert matrix["source_and_rule"]["empirical_changed"] is True
    assert matrix["source_and_rule"]["structural_routes_changed"] is True
    assert matrix["base_balance"] == [4, 4, 4]
    assert matrix["changed_balance"] == [6, 6, 6]
    assert matrix["changed_E1"]["empirical_steps"][0]["cells"] == {"0": 13, "1": 19}


def test_full_two_epoch_values_read_receipts_are_present(product):
    for label, fee, station in (("E1_EARLY_2026", 2, "ELIGIBLE"),
                                ("E2_LATE_2027", 6, "BLOCKED_BY_MODELED_RULE")):
        receipt = product["epoch_receipts"][label]
        assert receipt["state"] == "SELECTED_WORLD_VALUES_SERVED"
        assert receipt["structural_values"]["training_fee"]["value"] == fee
        assert receipt["structural_values"]["training_access"]["value"] is True
        assert receipt["consumers"][0]["consumer_material"]["consumer"] == "NONPARENT_OPTIONS"
        assert receipt["consumers"][1]["consumer_material"]["consumer"] == (
            "CONCEPTION_SCENARIO_PROPOSALS")
        assert receipt["consumers"][0]["consumer_material"]["structural_routes"]["training"]["state"] == station
        assert receipt["native_field_readset"]["state"] == "TWO_VALUES_READ_TEST_ONLY"
        assert len(receipt["empirical_steps"]) == 3
        assert receipt["operative_N9"] is False
        assert receipt["operative_OC05"] is False
    assert product["total_profiled_calls"] > 0
    assert len(product["native_call_summary"]) >= 6


def test_world_receipt_has_no_n8e_or_sorok_context_and_flags_are_false(product):
    forbidden = bootstrap.freeze()["world_receipt_must_not_contain_tokens"]
    text = json.dumps(dict(epochs=product["epochs"],
                           receipts=product["epoch_receipts"]), sort_keys=True)
    for token in forbidden:
        assert token not in text
    for label in ("E1_EARLY_2026", "E2_LATE_2027"):
        flags = product["epochs"][label]["flags"]
        assert flags["operative_N9"] is False
        assert flags["operative_OC05"] is False
        assert flags["pooling"] is False
        assert flags["person_exposure"] is False
        assert flags["model_use"] is False
        assert flags["issued_EE13"] is False
        assert flags["issued_N5N6"] is False
        assert flags["actor_executions"] == 0
        assert flags["model_calls"] == 0


def test_n8e_is_envelope_absent_hold_and_not_a_world_field(product):
    n8e = product["n8e_input"]
    assert n8e["state"] == "ABSENT_HOLD"
    assert n8e["numeric_delta"] is None
    assert n8e["measured_no_change"] is None
    assert n8e["world_input"] is False
    assert n8e["m4_root_input"] is False
    assert n8e["consumer_input"] is False
    assert n8e["n9_installation_state"] == "NOT_INSTALLED_HOLD"
    adapter = W.make_adapter()
    keys = [record["key"] for record in adapter.service.catalog.records]
    assert set(keys) == set(W.E.STRUCTURAL_KEYS)
    assert not any("N8E" in key or "Q43" in key or "Q31" in key for key in keys)


def test_late_epoch_is_asof_selectable_and_not_operative_current(product):
    control = product["epoch_clock_mode_control"]
    assert control["control_clock"]["mode"] == "AS_OF"
    assert control["identical_institutional_rule"] is True
    assert control["structural_values"]["training_fee"] == 6
    assert control["structural_values"]["training_access"] is True
    assert control["nonparent_routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert product["epochs"]["E2_LATE_2027"]["snapshot_flags"] == {
        "operative_CURRENT": False, "operative_N9": False}


def test_clock_modes_require_explicit_exact_clocks():
    with pytest.raises(W.E.N9SelectedWorldRefusal):
        W.E.SelectedWorldClock("TEST_CURRENT", "2027-09-01", "2027-09-01",
                               test_now=None)
    with pytest.raises(W.E.N9SelectedWorldRefusal):
        W.E.SelectedWorldClock("AS_OF", "2027-9-1", "2027-09-01")
    with pytest.raises(W.E.N9SelectedWorldRefusal):
        W.E.SelectedWorldClock("OPERATIVE", "2027-09-01", "2027-09-01")
    current = W.clock("TEST_CURRENT", "2027-09-01", "2027-09-01",
                      test_now="2027-09-01")
    assert W.make_request(current).clock.test_now == "2027-09-01"
    assert W.E2.mode == "TEST_CURRENT"
    assert W.E2_AS_OF.mode == "AS_OF"


def test_receipt_carries_native_m4_m5_and_two_separate_units(product):
    view = product["epochs"]["E1_EARLY_2026"]
    access = view["structural_values"]["training_access"]
    assert access["field_ref"]
    assert access["rsc_ref"]
    assert access["validation_ref"]
    assert access["currentness_grade"] == "CURRENT_TO_TEST_SELECTION_NOT_OPERATIVE_N9"
    native = view["native_field_readset"]
    assert len(native["values_read"]) == 2
    assert len(view["units"]) == 2
    assert len(view["source_families"]) == 2
    for step in view["empirical_steps"]:
        assert step["evidence_ref"]
        assert step["release_ref"]
        assert step["source_universe_ref"]
    modules = {(row["module"], row["function"]) for row in product["native_call_counts"]}
    assert ("rawlsing_next.m4_v557_v558_publication_repository", "resolve_v558") in modules
    assert ("rawlsing_next.m5_runtime_rsc_peer_prior",
            "materialize_resolved_structural_context") in modules


def test_cold_runs_are_byte_identical_and_match_live_epochs(product):
    cold_a = REPLAY / "cold_a.json"
    cold_b = REPLAY / "cold_b.json"
    replay = REPLAY / "cold_replay.json"
    assert cold_a.exists() and cold_b.exists() and replay.exists()
    assert cold_a.read_bytes() == cold_b.read_bytes()
    evidence = json.loads(replay.read_text())
    assert evidence["byte_identical"] is True
    assert evidence["sha256_equal"] is True
    assert evidence["all_children_exit_zero"] is True
    assert len(evidence["children"]) == 2
    cold = json.loads(cold_a.read_text())
    assert cold["terminal"] == product["terminal"]
    assert cold["epochs"] == product["epochs"]
    assert cold["consumer_delta"] == product["consumer_delta"]


def test_import_preimages_match_frozen_pins(product):
    pins = product["pinned_closure_verification"]
    assert len(pins) == len(bootstrap.freeze()["pinned_closure"])
    assert all(row["match"] is True for row in pins)
    imports = product["import_preimages"]
    assert len(imports) > 25
    pinned = [row for row in imports if row["frozen_pin_present"]]
    assert pinned
    assert all(row["frozen_pin_match"] is True for row in pinned)
    staged = [row for row in imports if row["kind"] == "STAGED_PINNED_NATIVE"]
    assert {row["module"].split(".")[0] for row in staged} >= {"product"}
    assert any(row["source_path"].endswith("e05r_selected_world_adapter.py")
               for row in staged)


def test_v553_candidate_is_evaluated_in_the_world_product(product):
    v553 = product["v553_candidate"]
    assert v553["empty_readiness_error_count"] == 45
    assert v553["candidate_verdict"] == (
        "V553_STRUCTURAL_TEMPORAL_HARMONIZATION_CANDIDATE__NOT_N8E_SURVEY_COMPARATOR")
    assert v553["ghana_use"] is False
    assert v553["n8e_authority_created"] is False
    assert v553["empty_harmonization_report"]["comparison_authority_status"] == \
        "insufficient_multi_wave_authority"


def test_product_terminal_and_assertions_are_green(product):
    assert product["failed_assertions"] == []
    assert product["terminal"] == (
        "TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_CONSUMER_POSITIVE__N8E_ABSENT_HOLD")
    assert product["product_type"] == "TEST_ONLY_SELECTED_INSTITUTIONAL_RULE"
    assert product["authority"]["actor_executions"] == 0
    assert product["authority"]["model_calls"] == 0
    assert product["authority"]["ee12_issued"] is False
    assert product["authority"]["n8e_product"] is False
