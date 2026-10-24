"""R05V R2 independent graph probes.

The positive setup is the actual native M01/C1 chain. These probes challenge
whether the successor validates actual graph/E41/status evidence or merely
echoes copied fields.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_world_composition import (
    NativeProductGraph,
    evaluate_learned_world_consumer,
)
from rawlsing_next.tests.test_universal_learned_consumer import _build_case

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r2_observations.json").write_text(
        json.dumps(
            {"schema": "R91_R05V_R2_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


@pytest.fixture(scope="module")
def case():
    return _build_case()


def _consume(case, composition, graph=None):
    return evaluate_learned_world_consumer(
        case["learned"],
        composition=composition,
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=graph,
    )


def test_actual_single_component_positive(case):
    graph = NativeProductGraph((case["composition"],))
    result = _consume(case, case["composition"], graph)
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.consumer_result.result_state == "EXACT_SUPPORTED"
    _record(
        "single_component_positive",
        {"state": result.state, "consumer_hash": result.consumer_result.result_hash},
    )


def test_copied_joint_discovery_recursive_labels_are_not_a_trusted_graph(case):
    forged_ref = ExactRef(
        "R91_FORGED_GRAPH", "urn:test:r05v:forged", semantic_hash({"forged": 1})
    )
    mutated = replace(
        case["composition"],
        joint_component_count=2,
        joint_order_semantics="SEMANTIC_ORDERED",
        discovery_receipt_refs=(forged_ref,),
        discovery_frontier_ref=forged_ref,
        recursive_handoff_refs=(forged_ref,),
        recursive_lineage_refs=(forged_ref,),
    )
    graph = NativeProductGraph((mutated,))
    result = _consume(case, mutated, graph)
    values = result.consumer_values_read or {}
    _record(
        "copied_graph_labels",
        {
            "state": result.state,
            "joint_component_count": values.get("joint_component_count"),
            "discovery_receipt_refs": values.get("discovery_receipt_refs"),
            "recursive_handoff_refs": values.get("recursive_handoff_refs"),
            "actual_component_joint_count": case["composition"].joint_component_count,
        },
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert values.get("joint_component_count") == case["composition"].joint_component_count
    assert forged_ref.as_dict() not in (values.get("discovery_receipt_refs") or [])


def test_non_supported_analytical_state_cannot_be_false_exact(case):
    mutated = replace(
        case["composition"],
        analytical_state="ZERO_SUPPORT",
        producer_fact_state="SUPPORTED",
        raw_denominator_support=0,
    )
    result = _consume(case, mutated)
    _record(
        "false_exact_state",
        {
            "analytical_state": mutated.analytical_state,
            "producer_fact_state": mutated.producer_fact_state,
            "observed_state": result.state,
            "observed_result_state": result.result_state,
            "observed_denominator": result.denominator,
        },
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.result_state != "SUPPORTED"


def test_duplicate_component_count_or_order_must_refuse(case):
    graph = NativeProductGraph((case["composition"], case["composition"]))
    result = _consume(case, case["composition"], graph)
    values = result.consumer_values_read or {}
    _record(
        "duplicate_component",
        {
            "state": result.state,
            "joint_component_count": values.get("joint_component_count"),
            "component_hashes": values.get("component_consumer_result_hashes"),
        },
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_fake_e41_extension_route_cannot_be_echoed(case):
    class FakeExtension:
        composition_result = None
        producer_route = "FAKE_ROUTE"

    fake = FakeExtension()
    fake.composition_result = case["composition"]
    graph = NativeProductGraph(
        compositions=(case["composition"],),
        extension_result=fake,
    )
    result = _consume(case, case["composition"], graph)
    values = result.consumer_values_read or {}
    _record(
        "fake_e41_route",
        {"state": result.state, "extension_route": values.get("extension_route")},
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
