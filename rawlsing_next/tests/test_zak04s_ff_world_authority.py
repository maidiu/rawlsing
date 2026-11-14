"""ZAK04S actual sourcefree R05/P41 authority regressions (not native FF).

The genuine selected C->D->M1->V558 product has CONTEXT use, not a
qualified Field Forge N9 STRUCTURAL admission.  The REF swap below therefore
does NOT execute NEG08's admitted FF causal pair, and is never labeled so.
"""
from dataclasses import replace
from types import SimpleNamespace
import json
import pytest
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_universal_world_binding import (
    R05WorldField, select_r05_world_view, _pinned_p41_runtime,
)
from rawlsing_next.tests.test_universal_world_binding import (
    _actual_execution_for, _build_r05_learned_inprocess, _r05_request,
)


def _case():
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, str(_pinned_p41_runtime()))
    assert execution.execution_handle, "Real trusted coordinator must provide a valid handle"
    request = _r05_request(data, actual_execution=execution)
    baseline = select_r05_world_view(request)
    assert baseline.state == "R05_WORLD_SELECTED_VIEW", baseline.reason_code
    values = baseline.consumer_values_read
    assert values["t0_routes"]["training"] == "ELIGIBLE"
    assert values["t1_routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert values["t0_n10e_steps"][0]["content_hash"] == values["consumer_result_hash"]
    assert values["coordinator_original_ref"] is not None
    return data, execution, request, baseline


def _ref(value: str):
    return ExactRef("ZAK04S_UNQUALIFIED_FF_PROVENANCE", "urn:zak04s:unqualified:" + value, value * 64)


def _emit(label, view):
    print("ZAK04S_OBSERVATION " + json.dumps({
        "case": label, "state": view.state, "reason": view.reason_code,
        "view_hash": view.view_hash,
        "t0_receipt_hash": (view.consumer_values_read or {}).get("t0_receipt_hash"),
        "t1_receipt_hash": (view.consumer_values_read or {}).get("t1_receipt_hash"),
    }, sort_keys=True), flush=True)


@pytest.fixture(scope="module")
def world_baseline():
    data, execution, request, baseline = _case()
    assert baseline.consumer_values_read["t0_receipt_hash"]
    assert baseline.consumer_values_read["t1_receipt_hash"]
    assert baseline.consumer_values_read["t0_receipt_hash"] != baseline.consumer_values_read["t1_receipt_hash"]
    _emit("REAL_P41_BASELINE", baseline)
    return data, execution, request, baseline


def test_actual_p41_owned_structural_positive_and_restore(world_baseline):
    _data, _execution, request, baseline = world_baseline
    restored = select_r05_world_view(request)
    _emit("REAL_P41_REPLAY", restored)
    assert restored.state == "R05_WORLD_SELECTED_VIEW"
    assert restored.view_hash == baseline.view_hash
    assert restored.consumer_values_read["t0_n10e_steps"][0]["content_hash"] == restored.consumer_values_read["consumer_result_hash"]


@pytest.mark.parametrize("attack", [
    "authority", "admission", "relation_ref", "field_ref",
    "transport_ref", "transport_bool", "full", "positive_looking",
])
def test_neg07_unqualified_ff_structural_claims_denied_by_real_selector(world_baseline, attack):
    data, execution, request, baseline = world_baseline
    forged = _ref("a")
    fields = request.fields
    kwargs = {}
    if attack == "authority":
        kwargs["ff_structural_authority_ref"] = forged
    elif attack == "admission":
        kwargs["ff_structural_admission"] = SimpleNamespace(typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE")
    elif attack == "relation_ref":
        fields = (replace(fields[0], relation_ref=forged), fields[1])
    elif attack == "field_ref":
        fields = (replace(fields[0], field_ref=forged), fields[1])
    elif attack == "transport_ref":
        kwargs["relation_transport_ref"] = forged
    elif attack == "transport_bool":
        kwargs["relation_transport_authorized"] = True
    elif attack == "positive_looking":
        kwargs["ff_structural_admission"] = SimpleNamespace(
            typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE",
            target_use="STRUCTURAL_MEDIATION_INPUT",
            source_universe_refs=(data["source_universe_ref"],),
            structural_semantic_identity_refs=(forged,),
        )
    else:
        fields = (replace(fields[0], role="STRUCTURAL", relation_ref=forged, field_ref=forged), fields[1])
        kwargs.update(ff_structural_authority_ref=forged,
                      ff_structural_admission=SimpleNamespace(typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE"),
                      relation_transport_ref=forged, relation_transport_authorized=True)
    candidate = replace(request, fields=fields, **kwargs)
    # No invalid-handle short circuit.  All learned/source/P41 inputs stay valid.
    assert candidate.execution_handle == request.execution_handle
    assert candidate.learned_consumer is request.learned_consumer
    refused = select_r05_world_view(candidate)
    _emit("NEG07_" + attack, refused)
    assert refused.state == "REFUSED"
    assert refused.reason_code == "R05_FF_ANCESTRY_NOT_TRUSTED"
    assert select_r05_world_view(request).view_hash == baseline.view_hash


def test_unqualified_ref_severance_is_not_a_fake_neg08(world_baseline):
    _data, _execution, request, baseline = world_baseline
    a, b = _ref("a"), _ref("b")
    fields = request.fields
    forged = replace(request,
                     fields=(replace(fields[0], relation_ref=a, field_ref=a), fields[1]),
                     ff_structural_authority_ref=a, relation_transport_ref=a,
                     relation_transport_authorized=True)
    removed = replace(forged,
                      fields=(replace(forged.fields[0], relation_ref=b, field_ref=b), fields[1]),
                      ff_structural_authority_ref=b, relation_transport_ref=b)
    for label, candidate in (
        ("UNQUALIFIED_A_NOT_NEG08", forged),
        ("UNQUALIFIED_B_NOT_NEG08", removed),
        ("UNQUALIFIED_A_RESTORED", forged),
    ):
        refused = select_r05_world_view(candidate)
        _emit(label, refused)
        assert refused.state == "REFUSED"
        assert refused.reason_code == "R05_FF_ANCESTRY_NOT_TRUSTED"
    world_restored = select_r05_world_view(request)
    _emit("REAL_P41_RESTORED", world_restored)
    assert world_restored.view_hash == baseline.view_hash


def test_context_refusal_and_other_existing_guard_precedence(world_baseline):
    _data, _execution, request, baseline = world_baseline
    forged = _ref("c")
    fields = request.fields
    context = replace(request,
                      fields=(fields[0], replace(fields[1], role="CONTEXT")),
                      ff_structural_authority_ref=forged)
    refused = select_r05_world_view(context)
    _emit("CONTEXT_REFUSAL", refused)
    assert refused.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    cross_unit = replace(request, fields=(
        replace(fields[0], unit="person", relation_ref=forged),
        replace(fields[1], unit="household", relation_ref=forged)))
    assert select_r05_world_view(cross_unit).reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"
    bad_handle = replace(request, execution_handle="r06ctx-bogus",
                         ff_structural_authority_ref=forged)
    assert select_r05_world_view(bad_handle).reason_code == "TRUSTED_EXECUTION_HANDLE_INVALID"
    assert select_r05_world_view(request).view_hash == baseline.view_hash
