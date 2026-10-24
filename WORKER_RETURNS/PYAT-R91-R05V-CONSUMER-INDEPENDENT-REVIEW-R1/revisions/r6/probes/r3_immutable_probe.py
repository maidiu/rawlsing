"""R05V R3 independent actual-graph probes.

The positive setup is the actual native M01/C1 chain. These probes test whether
R3 validates actual owner provenance or only internally consistent route/ref
metadata.
"""
from __future__ import annotations

from dataclasses import replace
import copy
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_world_composition import (
    NativeProductGraph,
    evaluate_learned_world_consumer,
)
from rawlsing_next.pre553_universal_empirical_extension import (
    EXT_ROUTE_DISCOVERY,
    EXT_ROUTE_RECURSIVE,
    provide_empirical_possibility_slice_ext,
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
    (OUTCOMES / "r05v_r3_observations.json").write_text(
        json.dumps({"schema": "R91_R05V_R3_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS}, indent=2, sort_keys=True) + "\n",
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


def test_actual_two_direct_component_positive(case):
    graph = NativeProductGraph((case["composition"], case["composition_b"]))
    result = _consume(case, case["composition"], graph)
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.joint_component_count == 2
    _record("two_direct_positive", {"state": result.state, "joint": result.joint_component_count})


def test_forged_internally_consistent_joint_topology_refuses(case):
    comp = case["composition"]
    topology = copy.deepcopy(comp.target_arity_and_topology)
    topology["arity"] = 2
    topology["components"] = [copy.deepcopy(topology["components"][0]), copy.deepcopy(topology["components"][0])]
    forged = replace(
        comp,
        joint_component_count=2,
        joint_order_semantics=topology["joint_order_semantics"],
        target_arity_and_topology=topology,
        producer_route="DIRECT_I03_TO_POSITIONED_SUBJECT",
    )
    graph = NativeProductGraph((forged,))
    result = _consume(case, forged, graph)
    _record(
        "forged_joint_topology",
        {"state": result.state, "joint": result.joint_component_count, "actual_component_count": 1},
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_forged_discovery_route_refs_refuse(case):
    comp = case["composition"]
    forged_ref = ExactRef("R91_FORGED_DISCOVERY", "urn:test:r05v:discovery", semantic_hash({"d": 1}))
    forged = replace(
        comp,
        producer_route="I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT",
        discovery_receipt_refs=(forged_ref,),
        discovery_frontier_ref=forged_ref,
        recursive_handoff_refs=(),
        recursive_lineage_refs=(),
    )
    graph = NativeProductGraph((forged,))
    result = _consume(case, forged, graph)
    values = result.consumer_values_read or {}
    _record("forged_discovery_route", {"state": result.state, "discovery": values.get("discovery_receipt_refs")})
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_forged_recursive_route_refs_refuse(case):
    comp = case["composition"]
    forged_ref = ExactRef("R91_FORGED_RECURSIVE", "urn:test:r05v:recursive", semantic_hash({"r": 1}))
    forged = replace(
        comp,
        producer_route="MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT",
        recursive_handoff_refs=(forged_ref,),
        recursive_lineage_refs=(forged_ref,),
    )
    graph = NativeProductGraph((forged,))
    result = _consume(case, forged, graph)
    values = result.consumer_values_read or {}
    _record("forged_recursive_route", {"state": result.state, "recursive": values.get("recursive_handoff_refs")})
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_actual_type_e41_forged_route_refuses(case):
    extension = provide_empirical_possibility_slice_ext(**case["context"])
    forged = replace(extension, producer_route=EXT_ROUTE_DISCOVERY)
    graph = NativeProductGraph((case["composition"],), extension_result=forged)
    result = _consume(case, case["composition"], graph)
    values = result.consumer_values_read or {}
    _record("actual_type_e41_forged_route", {"state": result.state, "route": values.get("extension_route")})
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_false_exact_status_disagreement_refuses(case):
    comp = case["composition"]
    forged = replace(comp, analytical_state="ZERO_SUPPORT", producer_fact_state="SUPPORTED", raw_denominator_support=0)
    result = _consume(case, forged)
    _record("status_disagreement", {"state": result.state, "result_state": result.result_state, "denominator": result.denominator})
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
