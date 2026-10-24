"""R05V R8 independent positive: request actual fields are ignored, admitted
slot records and trusted original remain fixed."""
from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
import rawlsing_next.pre553_learned_world_composition as i4

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r7probe", BASE / "test_r05v_r7_immutable_probe.py")
r7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r7)

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBS = []


def test_forged_request_actual_fields_do_not_rewrite_admitted_original():
    captured, real_eval = r7._capture()
    assert captured.get("trusted_calls")
    args, kwargs = captured["trusted_calls"][0]
    coordinator = kwargs["trusted_graph_reader"]
    admitted = list(coordinator._admitted_slots.values())[0]
    baseline = coordinator.execute(i4.NativeGraphExecutionRequest((admitted,)))
    forged_ref = ExactRef(
        "R91_FORGED_REQUEST_FIELD", "urn:test:r05v:forged", semantic_hash({"f": 1})
    )
    forged = replace(
        admitted,
        m1_disposition=captured["learned2"].m1_disposition,
        m2_release=captured["learned2"].m2_artifacts.release.ref,
        b5_selection=forged_ref,
        require_current_selection=True,
        target_arity=2,
        joint_order_semantics="MIXED",
        discovery_result=object(),
        discovery_receipt_ref=None,
        discovery_frontier_ref=None,
        recursive_handoff=object(),
        recursive_lineage_refs=(forged_ref,),
        root_parent_ref=forged_ref,
        e41_input=object(),
        repository=object(),
        empirical_query=object(),
        predicate=object(),
        authority_registry=object(),
        consumer_query=object(),
        model_rule=object(),
    )
    bound = coordinator.execute(i4.NativeGraphExecutionRequest((forged,)))
    call_args = args
    call_kwargs = dict(kwargs)
    call_kwargs["composition"] = bound.view.compositions[0]
    call_kwargs["product_graph"] = bound
    call_kwargs["trusted_graph_reader"] = coordinator
    result = real_eval(*call_args, **call_kwargs)
    OBS.append(
        {
            "probe": "forged_request_actual_fields",
            "state": result.state,
            "baseline_original": baseline.original_ref.content_hash,
            "forged_original": bound.original_ref.content_hash,
            "same_original": baseline.original_ref.content_hash == bound.original_ref.content_hash,
            "consumer_hash": None if result.consumer_result is None else result.consumer_result.result_hash,
        }
    )
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r8_observations.json").write_text(
        json.dumps({"schema": "R91_R05V_R8_INDEPENDENT_OBSERVATIONS@1", "probes": OBS}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    assert baseline.original_ref.content_hash == bound.original_ref.content_hash
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_nested_admitted_witness_mutation_does_not_serve_silent_exact():
    captured, real_eval = r7._capture()
    assert captured.get("trusted_calls")
    args, kwargs = captured["trusted_calls"][0]
    coordinator = kwargs["trusted_graph_reader"]
    admitted = list(coordinator._admitted_slots.values())[0]
    witness = admitted.condition_value_witness
    assert witness is not None
    witness.identity_material["probe_mutation"] = "x"
    refusal = None
    result = None
    try:
        bound = coordinator.execute(i4.NativeGraphExecutionRequest((admitted,)))
        call_kwargs = dict(kwargs)
        call_kwargs["composition"] = bound.view.compositions[0]
        call_kwargs["product_graph"] = bound
        call_kwargs["trusted_graph_reader"] = coordinator
        result = real_eval(*args, **call_kwargs)
    except Exception as exc:
        refusal = type(exc).__name__ + ": " + str(exc)
    OBS.append(
        {
            "probe": "nested_admitted_witness_mutation",
            "refusal": refusal,
            "state": None if result is None else result.state,
        }
    )
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r8_observations.json").write_text(
        json.dumps({"schema": "PYAT_R05V_R8_INDEPENDENT_OBSERVATIONS@1", "probes": OBS}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if result is not None:
        assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
