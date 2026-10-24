"""R05V independent actual-consumer probes.

Positive setup reuses the actual native M01/C1 fixture chain from the author
test helper. The probes below independently challenge the commissioned full
product/status integration, not the helper's assertions.
"""
from __future__ import annotations

from dataclasses import replace
import inspect
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_world_composition import evaluate_learned_world_consumer
from rawlsing_next.pre553_universal_empirical_extension import (
    EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
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
    (OUTCOMES / "r05v_observations.json").write_text(
        json.dumps(
            {
                "schema": "R91_R05V_INDEPENDENT_OBSERVATIONS@1",
                "probes": OBSERVATIONS,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


@pytest.fixture(scope="module")
def case():
    return _build_case()


def _consume(case, composition):
    return evaluate_learned_world_consumer(
        case["learned"],
        composition=composition,
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )


def test_positive_single_m01_actual_chain(case):
    result = _consume(case, case["composition"])
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.consumer_result.result_state == "EXACT_SUPPORTED"
    sig = inspect.signature(evaluate_learned_world_consumer)
    params = list(sig.parameters)
    _record(
        "single_m01_positive",
        {
            "state": result.state,
            "consumer_state": result.consumer_result.result_state,
            "consumer_hash": result.consumer_result.result_hash,
            "signature": params,
            "single_composition_parameter": "composition" in params,
            "product_graph_parameter": any(
                name in params for name in ("products", "compositions", "product_graph", "e41")
            ),
        },
    )


def test_typed_status_axes_are_preserved_by_consumer(case):
    observed = []
    for state, denominator in (
        ("ZERO_SUPPORT", 0),
        ("VALID_EMPTY", 0),
        ("UNRESOLVED", 16),
    ):
        mutated = replace(
            case["composition"],
            analytical_state=state,
            producer_fact_state=state,
            possibility_slice_evidence_or_null=None,
            raw_denominator_support=denominator,
        )
        result = _consume(case, mutated)
        observed.append(
            {
                "input_state": state,
                "denominator": denominator,
                "state": result.state,
                "reason_code": result.reason_code,
                "consumer_values_read": result.consumer_values_read,
            }
        )
    _record("status_axes", {"observed": observed})
    for entry in observed:
        # A typed ZERO_SUPPORT/VALID_EMPTY/UNRESOLVED result (with its axes,
        # denominator and Z16) must survive, not collapse to generic REFUSED.
        assert entry["state"] != "REFUSED", entry


def test_joint_recursive_discovery_bindings_affect_consumer(case):
    mutated = replace(
        case["composition"],
        joint_component_count=2,
        joint_order_semantics="SEMANTIC_ORDERED",
        discovery_receipt_refs=(
            ExactRef("R91_DISCOVERY", "urn:test:r05v:discovery", semantic_hash({"d": 1})),
        ),
        discovery_frontier_ref=ExactRef(
            "R91_DISCOVERY_FRONTIER", "urn:test:r05v:frontier", semantic_hash({"f": 1})
        ),
        recursive_handoff_refs=(
            ExactRef("R91_RECURSIVE_HANDOFF", "urn:test:r05v:handoff", semantic_hash({"h": 1})),
        ),
        recursive_lineage_refs=(
            ExactRef("R91_RECURSIVE_LINEAGE", "urn:test:r05v:lineage", semantic_hash({"l": 1})),
        ),
        analytical_state="SUPPORTED",
        producer_fact_state="SUPPORTED",
    )
    result = _consume(case, mutated)
    values = result.consumer_values_read or {}
    _record(
        "joint_recursive_binding",
        {
            "state": result.state,
            "consumer_state": None if result.consumer_result is None else result.consumer_result.result_state,
            "values_keys": sorted(values),
            "has_joint": "joint_component_count" in values,
            "has_discovery": "discovery_receipt_refs" in values,
            "has_recursive": "recursive_handoff_refs" in values,
            "has_producer_route": "producer_route" in values,
        },
    )
    assert "joint_component_count" in values
    assert "discovery_receipt_refs" in values
    assert "recursive_handoff_refs" in values
    assert "producer_route" in values


def test_e41_extension_is_not_part_of_the_learned_consumer_binding(case):
    extension = provide_empirical_possibility_slice_ext(**case["context"])
    assert extension.producer_route == EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER
    sig = inspect.signature(evaluate_learned_world_consumer)
    params = set(sig.parameters)
    _record(
        "e41_separate_route",
        {
            "extension_route": extension.producer_route,
            "extension_consumer_state": extension.consumer_result_or_null.result_state,
            "consumer_accepts_extension_result": any(
                name in params for name in ("extension", "extension_result", "e41")
            ),
        },
    )
    assert not any(name in params for name in ("extension", "extension_result", "e41"))
