"""ZAK-04S R05/P41 sourcefree differential probe, pre-repair.
Pre-repair version intentionally records the actual selector's current behavior;
it does NOT represent a qualified C->D->M1->V558 relation.
"""
from dataclasses import replace
import json
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


def test_pre_repair_ff_claim_is_ignored_at_actual_p41_reader():
    data, execution, request, baseline = _case()
    _emit("REAL_P41_BASELINE", baseline)
    fields = request.fields
    forged = _ref("a")
    promoted = replace(fields[0], field_ref=forged, relation_ref=forged, role="STRUCTURAL")
    candidate = _r05_request(
        data, actual_execution=execution, fields=(promoted, fields[1]),
        ff_structural_authority_ref=forged,
        relation_transport_ref=forged, relation_transport_authorized=False,
    )
    result = select_r05_world_view(candidate)
    _emit("NEG07_PRE_REPAIR_UNQUALIFIED_CLAIM", result)
    # This observation intentionally tests present (unrepaired) behavior.
    assert result.state == "R05_WORLD_SELECTED_VIEW", result.reason_code
    assert result.view_hash == baseline.view_hash
    swapped = _ref("b")
    severed = select_r05_world_view(replace(
        candidate,
        fields=(replace(promoted, field_ref=swapped, relation_ref=swapped), fields[1]),
        ff_structural_authority_ref=swapped,
        relation_transport_ref=swapped,
    ))
    _emit("UNQUALIFIED_REF_SWAP_NOT_NEG08", severed)
    assert severed.state == "R05_WORLD_SELECTED_VIEW", severed.reason_code
    assert severed.view_hash == baseline.view_hash
    restored = select_r05_world_view(candidate)
    _emit("RESTORED_UNQUALIFIED_CLAIM", restored)
    assert restored.view_hash == result.view_hash
    context = select_r05_world_view(replace(
        candidate, fields=(promoted, replace(fields[1], role="CONTEXT"))
    ))
    _emit("CONTEXT_REFUSAL", context)
    assert context.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
